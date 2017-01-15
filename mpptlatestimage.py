#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Create an image of the BMV latest chart using PIL/pillow
# PIL allows .png .jpg .gif or .bmp file formats
from PIL import Image, ImageDraw, ImageFont

# some color constants for PIL
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
green = (0,128,0)
width = 800
height = 480

# create empty PIL image and draw "context" to draw on
# PIL draws in memory only, but the image can be saved
image = Image.new("RGB", (width, height), white)
draw = ImageDraw.Draw(image)

fontSize = 24
fnt = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', fontSize)

left = 20
textFillBlue = (0, 0, 255, 255)
draw.text((left,0), "MPPT 100/50 Current Status:", fill=textFillBlue, font=fnt)

y = fontSize * 2

# Read and display the latest MPPT data
#tfile = open("/home/pi/bmv/bmv.latest", "r")
tfile = open("/var/tmp/mppt.latest", "r")
if tfile :
    for line in tfile :
        s = line.replace("<TD>", "")
        s = s.replace("</TD>", " ")
        draw.text((left,y), s, fill=textFillBlue, font=fnt)
        y = y + fontSize * 1.5
    tfile.close()

# PIL image can be saved as .png .jpg .gif or .bmp file
filename = "/var/www/mpptcurrent.jpg"
image.save(filename)



