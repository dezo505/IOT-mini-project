#!/usr/bin/env python3
import time
from PIL import Image, ImageDraw, ImageFont
import lib.oled.SSD1331 as SSD1331
import os
 
class DrawControl:
    disp = SSD1331.SSD1331()      
    fontLarge = ImageFont.truetype('./lib/oled/Font.ttf', 10)
 
    @staticmethod
    def writeMessage(messageLine1, messageLine2):
        DrawControl.disp.Init()
        Image1 = Image.new("RGB", (DrawControl.disp.width, DrawControl.disp.height))
        draw = ImageDraw.Draw(Image1)
        draw.text((0, 0), messageLine1, font=DrawControl.fontLarge, fill="WHITE")
        draw.text((0, 40), messageLine2, font=DrawControl.fontLarge, fill="WHITE")
        DrawControl.disp.ShowImage(Image1, 0, 0)
 

