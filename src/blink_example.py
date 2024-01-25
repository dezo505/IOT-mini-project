import time

from src.main.blink import blink_green, blink_red


def example_usage():
    blink_green(1)
    blink_red(1)

    time.sleep(1)

    blink_green(2)
    blink_green(2)


if __name__ == "__main__":
    example_usage()