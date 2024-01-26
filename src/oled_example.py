from main.oled_control import *

import time
from PIL import Image, ImageDraw, ImageFont
import os
 
if __name__ == "__main__":
    DrawControl.writeMessage(backgroundColor="GREEN", fontColor="WHITE")
    time.sleep(2)
    DrawControl.writeMessage(backgroundColor="RED", fontColor="WHITE")
    time.sleep(2)
    DrawControl.writeMessage(backgroundColor="BLACK", fontColor="WHITE")
    time.sleep(2)
    DrawControl.clear()