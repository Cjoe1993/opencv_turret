from adafruit_servokit import ServoKit
import time

class servoOne:

    def __init__(self):
        self.kit = ServoKit(channels=16)
        # pulse width range changes the pulse range, increasing sweep distance
        self.kit.servo[0].set_pulse_width_range(1000, 2500)
        self.kit.servo[1].set_pulse_width_range(1000, 2500)
        self.kit.servo[2].set_pulse_width_range(1000, 2500)
    def moveServoX(self,degrees):
        self.kit.servo[0].angle = degrees
    def resetServoX(self,degrees):
        self.kit.servo[0].angle = degrees
    def moveServoY(self,degrees):
        self.kit.servo[1].angle = degrees
    def resetServoY(self,degrees):
        self.kit.servo[1].angle = degrees
    def pullTrigger(self):
        self.kit.servo[2].angle = 180
        time.sleep(.5)
    def depressTrigger(self):
        self.kit.servo[2].angle = 50
        time.sleep(.5)
