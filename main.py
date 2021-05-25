import numpy as np
import cv2
import os
import threading
import time
from test_move_servo import servoOne
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

# servo motor, second thread
trigger = servoOne()

def move_servo():
	event.wait()
	while event.is_set():
		#realign()
		pass
		# reinitialize event to wait
		if not event.is_set():
			pass
			#event.wait()


def realign():
	try:
		global increment
		# face coordinates, top left bottom right
		x1 = faces[0][0]
		y1 = faces[0][1]
		x2 = faces[0][2]
		y2 = faces[0][3]
		# center of facial box
		center_x = x1+x2
		center_y = y1+(y2//2)
		# targeting system coordinates based on center of facial box, fixed size
		x3 = center_x-15
		y3 = center_y-15
		x4 = center_x+15
		y4 = center_y+15
		start_pos = [x3,y3]
		end_pos = [x4,y4]
		if center_coords[0] < x1 and increment >= 2:
			increment -= 2
			trigger.moveServoX(increment)
			if center_coords[0] <= center_x and center_coords[0] >= x1 :
				print('We are inside!')
				increment = increment
		if center_coords[0] > center_x and increment <= 168:
			increment += 2
			trigger.moveServoX(increment)
			if center_coords[0] <= center_x and center_coords[0] >= x1 : 
				print('We are inside!')
				increment = increment
	except IndexError:
		pass

def main():

	if camera_feed.isOpened(): # grab first frame
		cam, frame = camera_feed.read()
	else:
		cam = False

	while cam:

		event.clear()
		global faces
		global center_coords
		center_mass = cv2.circle(frame, (325,250), 2, (0,255,0),2)
		center_coords = [325,250]
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
				#event.set()
				realign()
		# resize frame
		#frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
		cv2.imshow('main window', frame)
		cam, frame = camera_feed.read()
		key = cv2.waitKey(20)
		# broken, use ctrl+c to terminate
		if key == 27: # exit on ESC
			break


if __name__=="__main__":
	increment = 90
	inside_box = False
	event = threading.Event()
	t1 = threading.Thread(target=main)
	t2 = threading.Thread(target=realign)
	t1.start()
	t2.start()

cv2.destroyWindow('main window')
sys.exit()
################################
