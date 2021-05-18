import numpy as np
import cv2
import os
import time
from move_servo import servoOne
"""
This project is:

A raspberry pi project that utilizes the rp camera module, a servo motor and a servo controller.
The opencv2 haarcascade allows us to track faces, which we can then use to send electricity to the servo motor,
pulling the trigger mechanism.
"""


cv2.namedWindow('main window') # the second arg '16' removes native buttons on top of window. Buttons include zoom in/out, screen capture. Could be useful
camera_feed = cv2.VideoCapture(0)

# face tracking
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# servo motor
trigger = servoOne()

if camera_feed.isOpened(): # grab first frame
	cam, frame = camera_feed.read()
else:
	cam = False

while cam:

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
		"""
		The trigger code needs to be inserted into a separate thread, otherwise the
		sleep() methods will cause the facial recognition algorithm to also cease.
		"""
			# activate the servo motor
			trigger.moveServo()
			# return to neutral position
			trigger.resetServo()

	cv2.imshow('main window', frame)

	cam, frame = camera_feed.read()
	key = cv2.waitKey(20)

	if key == 27: # exit on ESC
		break

cv2.destroyWindow('main window')

################################
