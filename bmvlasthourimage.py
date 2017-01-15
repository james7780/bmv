#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Create an image of the BMV latest chart using PIL/pillow
# PIL allows .png .jpg .gif or .bmp file formats
import time
import os
from PIL import Image, ImageDraw, ImageFont

# get last 120 lines (60 minutes) of the bmv log
#os.system("tail --lines=120 /home/pi/bmv/bmv.log > /var/www/cgi-bin/chart.log")
os.system("tail --lines=120 /var/tmp/bmv.log > /var/www/cgi-bin/chart.log")

# parse the log file into an array of values
charge = []			# Array of SOC values
power = []			# Array of Power (W) values
y = 0
tfile = open("/var/www/cgi-bin/chart.log", "r")
if tfile :
	for line in tfile :
		s = line.split(',')
		#print s[5]
		if len(s) > 5 :
			y = int(s[5])		# 1000 = 100% (SOC)
			charge.append(y)
			y = int(s[3])       # Power (W)
			power.append(y)
	tfile.close()
else :
	print "Could not open log file tail!"

# get current time as a string
localtime = time.asctime(time.localtime(time.time()))

# some color constants for PIL
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
green = (0,128,0)

# create empty PIL image and draw "context" to draw on
# PIL draws in memory only, but the image can be saved

image = Image.new("RGB", (800, 480), white)
draw = ImageDraw.Draw(image)

# draw axes
top = 40
left = 60
height = 400
width = 680
right = left + width
bottom = top + height
middle = top + height/2
draw.line((left, top, left, bottom), black)
draw.line((left, bottom, right, bottom), black)
draw.line((left, middle, right, middle), black)
draw.line((left, top, right, top), black)

# Draw SOC polyline (SOC range 500 to 1000)
#print "  cx.strokeStyle = 'blue';"
x = 0
vprev = 0
xstep = width / len(charge)
for v in charge :
	v = top + (1000 - v) * height / 500
	if x > 0 :
		draw.line((left + (x-1) * xstep, vprev, left + x * xstep, v), blue)
	vprev = v
	x = x + 1

# Draw power polyline (range -1000 to 1000 W)
#print "  cx.strokeStyle = 'green';"
x = 0
xstep = width / len(charge)
for v in power :
	v = middle - (v * height / 2000)
	if x > 0 :
		draw.line((left + (x-1) * xstep, vprev, left + x * xstep, v), green)
	vprev = v
	x = x + 1
	
# Draw SOC Y axis labels at the left edge
fnt = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 20)
textFillBlue = (0, 0, 255, 255)
draw.text((0,top), "100%", fill=textFillBlue, font=fnt)
draw.text((0,top + height * 0.2), "90%", fill=textFillBlue, font=fnt)
draw.text((0,top + height * 0.4), "80%", fill=textFillBlue, font=fnt)
draw.text((0,top + height * 0.5), "75%", fill=textFillBlue, font=fnt)
draw.text((0,bottom), "50%", fill=textFillBlue, font=fnt)
draw.text((0,top + height * 0.25), "SOC", fill=textFillBlue, font=fnt)

# Draw power Y axis labels at the right edge
textFillGreen = (0, 200, 0, 255)
draw.text((right,top), "1000W", fill=textFillGreen, font=fnt)
draw.text((right,top + height * 0.25), "500W", fill=textFillGreen, font=fnt)
draw.text((right,top + height * 0.375), "250W", fill=textFillGreen, font=fnt)
draw.text((right,top + height * 0.5), "0W", fill=textFillGreen, font=fnt)
draw.text((right,top + height * 0.625), "-250W", fill=textFillGreen, font=fnt)
draw.text((right,top + height * 0.75), "-500W", fill=textFillGreen, font=fnt)
draw.text((right,bottom), "-1000W", fill=textFillGreen, font=fnt)
draw.text((right,top + height * 0.2), "P (in)", fill=textFillGreen, font=fnt)
draw.text((right,top + height * 0.8), "P (out)", fill=textFillGreen, font=fnt)

textFillBlack = (0, 0, 0, 255)
draw.text((left, 0), "BMV-700 Last Hour SOC and Power", fill=textFillBlack, font=fnt)

# PIL image can be saved as .png .jpg .gif or .bmp file
filename = "/var/www/bmvlasthour.jpg"
image.save(filename)

