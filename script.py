import cv2
from os.path import exists
from time import sleep
from threading import Thread, Event
from math import ceil
import ctypes

import telebot
import json

cap = cv2.VideoCapture(0)

PHOTO_PATH = 'photo.png'
DATA_PATH = 'data.json'
CONFIG_PATH = 'config.json'

# user_here shows if user is using pc
user_here = True

# Create the haar cascade
faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# To call thread only once
thread_running = False

def user_leave_event(event: Event):
	global user_here
	global thread_running
	
	thread_running = True
	
	# Time - delay between user is confirmed to leave
	# Frequency - how often should it be checked until confirming
	await_time = 5
	await_frequency = 0.5
	
	for i in range(ceil(await_time / await_frequency)):
		sleep(await_frequency)
		if (event.is_set()):
			thread_running = False
			return
	
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
		
		def send_photo():
			if not (exists(DATA_PATH) and exists(CONFIG_PATH) and exists(PHOTO_PATH)):
				return
			
			with open(DATA_PATH) as file:
				data = json.load(file)
			with open(CONFIG_PATH) as file:
				config = json.load(file)
				
			if data['ENABLED'] == 'False':
				return
			
			bot = telebot.TeleBot(config['BOT_TOKEN'])
			
			with open(PHOTO_PATH, 'rb') as photo:
				# Send the photo
				bot.send_photo(data['CHAT_ID'], photo)
			
			ctypes.windll.user32.LockWorkStation()
		
		# When user leaves, start user_leave_event thread
		if len(faces) == 0 and user_here and not thread_running:
			event.clear()
			thread = Thread(target=user_leave_event, args=(event, ))
			thread.start()
		# When face is detected, break thread or, if thread is finished, send photo and lock screen
		elif len(faces) > 0:
			if thread_running:
				event.set()
			elif not user_here:
				event.set()
				user_here = True
				cv2.imwrite(PHOTO_PATH, frame)
				send_photo()
			
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	# When everything done, release the capture
	cap.release()
	cv2.destroyAllWindows()

if __name__ == '__main__':
	main()