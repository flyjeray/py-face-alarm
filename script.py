import cv2
from gtts import gTTS
from playsound import playsound
import screen_brightness_control as sbc
from os.path import exists
from time import sleep
from threading import Thread, Event

cap = cv2.VideoCapture(0)

# some variables.
# texts are what the Artificial Intelligence says
# and sound_names are paths where mp3s are saved
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

def screensave(event: Event):
	playsound(goodbye_sound_name)
	
	sleep(3)
	if (event.is_set()):
		return
	sbc.set_brightness(0)
	
	sleep(5)
	if (event.is_set()):
		return
	
def main():
	person_here = True
	thread = None
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
		if len(faces) == 0 and person_here:
			event.clear()
			thread = Thread(target=screensave, args=(event, ))
			thread.start()
			person_here = False
		# when you come back, say hi and restore brightness
		elif len(faces) > 0 and not person_here:
			event.set()
			playsound(hello_sound_name)
			sbc.set_brightness(initial_brightness[0])
			person_here = True
			
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	# When everything done, release the capture
	cap.release()
	cv2.destroyAllWindows()
	
main()