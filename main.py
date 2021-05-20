import numpy as np
import cv2
import os
import threading
import time
from move_servo import servoOne
import sys

"""
This project is:

A raspberry pi project that utilizes the rp camera module, a servo motor and a servo controller.
The opencv2 haarcascade allows us to track faces, which we can then use to send electricity to the servo motor,
pulling the trigger mechanism.
"""

print('Initializing. . .')

cv2.namedWindow('main window')
camera_feed = cv2.VideoCapture(0)

# face tracking
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# window dimensions
width = 1200
height = 1080
dim = (width, height)

# servo motor, second thread
trigger = servoOne()
def move_servo():
	event.wait()
	while event.is_set():
		trigger.moveServo()
		trigger.resetServo()
		# reinitialize event to wait
		if not event.is_set():
			event.wait()


def main():

	if camera_feed.isOpened(): # grab first frame
		cam, frame = camera_feed.read()
	else:
		cam = False

	while cam:
		event.clear()
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		faces = face_cascade.detectMultiScale(gray, 1.3, 5)

		for (x,y,w,h) in faces:
			img = cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
			gray_2 = gray[y:y+h, x:x+w]
			color = img[y:y+h, x:x+w]

			# This returns True while a face is detected. Since img refers to an array,
			# we must add any()/all(), meaning if anything in the array returns True,
			# return True, or if ALL items in array return True, return True.
			if img.any():
				# activate the servo motor by setting its event flag
				event.set()

		# resize frame
		frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
		cv2.imshow('main window', frame)
		cam, frame = camera_feed.read()
		key = cv2.waitKey(20)
		# broken, use ctrl+c to terminate
		if key == 27: # exit on ESC
			break


if __name__=="__main__":
	event = threading.Event()
	t1 = threading.Thread(target=main)
	t2 = threading.Thread(target=move_servo)
	t1.start()
	t2.start()

cv2.destroyWindow('main window')
sys.exit()
################################
