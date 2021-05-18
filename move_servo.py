from adafruit_servokit import ServoKit
import time

class servoOne:

    def __init__(self):
        self.kit = ServoKit(channels=16)
        # pulse width range changes the pulse range, increasing sweep distance
        self.kit.servo[0].set_pulse_width_range(1000, 2500)

    def moveServo(self):
	# Pull trigger, 90 degrees counter-clockwise
        self.kit.servo[0].angle = 180
        time.sleep(.5)
    def resetServo(self):
	# release trigger, 90 degrees clockwise
        self.kit.servo[0].angle = 50
        time.sleep(.5)
