from config import *

import time
import board
import neopixel


class LedControl:
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLACK = (0, 0, 0)
    
    @staticmethod
    def blink_red(duration):
        pixels = neopixel.NeoPixel(board.D18, 8, brightness=1.0 / 32, auto_write=False)

        pixels.fill(LedControl.RED)
        pixels.show()

        time.sleep(duration)

        pixels.fill(BLACK)
        pixels.show()

    @staticmethod
    def blink_green(duration):
        pixels = neopixel.NeoPixel(board.D18, 8, brightness=1.0 / 32, auto_write=False)

        pixels.fill(LedControl.GREEN)
        pixels.show()

        time.sleep(duration)

        pixels.fill(BLACK)
        pixels.show()

    @staticmethod
    def turnOnColor(color):
        pixels = neopixel.NeoPixel(board.D18, 8, brightness=1.0 / 32, auto_write=False)
        pixels.fill(color)
        pixels.show()

    @staticmethod
    def turnOffLed():
        pixels = neopixel.NeoPixel(board.D18, 8, brightness=1.0 / 32, auto_write=False)
        pixels.fill(LedControl.BLACK)
        pixels.show()


        


