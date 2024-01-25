from config import *  # pylint: disable=unused-wildcard-import
import RPi.GPIO as GPIO
import time

class BuzzerControl:
    @staticmethod
    def changeBuzzerState(state):
        GPIO.output(buzzerPin, not state)