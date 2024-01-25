from config import *

import time
import board
import neopixel

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)


# ws2812.py
def blink_red(duration):
    pixels = neopixel.NeoPixel(board.D18, 8, brightness=1.0 / 32, auto_write=False)

    pixels.fill(RED)
    pixels.show()

    time.sleep(duration)

    pixels.fill(BLACK)
    pixels.show()


def blink_green(duration):
    pixels = neopixel.NeoPixel(board.D18, 8, brightness=1.0 / 32, auto_write=False)

    pixels.fill(GREEN)
    pixels.show()

    time.sleep(duration)

    pixels.fill(BLACK)
    pixels.show()
