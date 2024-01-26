from config import * 
import RPi.GPIO as GPIO

class BuzzerControl:
    @staticmethod
    def changeBuzzerState(state):
        GPIO.output(buzzerPin, not state)