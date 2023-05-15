import cv2
from gtts import gTTS
from playsound import playsound
import screen_brightness_control as sbc
from os.path import exists
from time import sleep
from threading import Thread, Event
from math import ceil

cap = cv2.VideoCapture(0)

# some variables.
# user_here shows if user is using pc
# texts are what the Artificial Intelligence says
# and sound_names are paths where mp3s are saved
user_here = True
goodbye_text = 'Goodbye'
goodbye_sound_name = 'bye.mp3'
hello_text = 'Hello'
hello_sound_name = 'hi.mp3'

# Create the haar cascade
faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# creating sounds
if not exists(hello_sound_name):
	audio = gTTS(text=hello_text, lang="en", slow=False)
	audio.save(hello_sound_name)

if not exists(goodbye_sound_name):
	audio = gTTS(text=goodbye_text, lang="en", slow=False)
	audio.save(goodbye_sound_name)

# get initial brightness
initial_brightness = sbc.get_brightness()

# to call thread only once
thread_running = False

def screensave(event: Event):
	global user_here
	global thread_running
	
	thread_running = True
	
	step1_await_time = 5
	step1_await_frequency = 0.5
	
	for i in range(ceil(step1_await_time / step1_await_frequency)):
		sleep(step1_await_frequency)
		if (event.is_set()):
			thread_running = False
			return
	
	playsound(goodbye_sound_name)	
	sbc.set_brightness(0)
	user_here = False
	thread_running = False
	
def main():
	global user_here
	global thread_running
	
	event = Event()
	
	while True:
		# Capture frame-by-frame
		ret, frame = cap.read()
	
		# Our operations on the frame come here
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	
		# Detect faces in the image
		faces = faceCascade.detectMultiScale(
			gray,
			scaleFactor=1.1,
			minNeighbors=5,
			minSize=(30, 30)
		)
		
		# when you leave the screen, start screensaver
		if len(faces) == 0 and user_here and not thread_running:
			event.clear()
			thread = Thread(target=screensave, args=(event, ))
			thread.start()
		# when you come back, either break thread or, if it finished, say hi and restore brightness
		elif len(faces) > 0:
			if thread_running:
				event.set()
			elif not user_here:
				event.set()
				playsound(hello_sound_name)
				sbc.set_brightness(initial_brightness[0])
				user_here = True
			
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	# When everything done, release the capture
	cap.release()
	cv2.destroyAllWindows()
	
main()