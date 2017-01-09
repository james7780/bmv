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
			y = 1000 - int(s[5])
			charge.append(y)
			y = int(s[3])
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
width = 800
height = 480

# create empty PIL image and draw "context" to draw on
# PIL draws in memory only, but the image can be saved
image = Image.new("RGB", (width, height), white)
draw = ImageDraw.Draw(image)

# draw axes
draw.line((0, 0, 0, 480), black)
draw.line((0, 480, 480, 480), black)
draw.line((0, 240, 480, 240), black)
draw.line((0, 0, 480, 0), black)

# Draw SOC polyline
#print "  cx.strokeStyle = 'blue';"
x = 0
vprev = 0
for v in charge :
	if x > 0 :
		#print "  cx.lineTo(" + str(x) + ", " + str(v) + ");"
		draw.line((x-1, vprev, x, v), blue)
	vprev = v
	x = x + 1

# Draw power polyline
#print "  cx.strokeStyle = 'green';"
x = 0
for v in power :
	v = 250 - v / 4
	if x > 0 :
		draw.line((x-1, vprev, x, v), green)
	vprev = v
	x = x + 1
	
# Draw SOC Y axis labels at the left edge
fnt = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 10)
#draw.text((20,20), "Hello World!", fill=(255, 0, 0, 128), font=fnt)
#print "  cx.translate(-10, 0);"
#print "  cx.scale(0.25, 1);"
#print "  cx.font = 'bold 10pt Verdana';"
#print "  cx.fillStyle = 'blue';"
#print "  cx.fillText('100%', 0, 0);"
#print "  cx.fillText('90%', 0, 100);"
#print "  cx.fillText('80%', 0, 200);"
#print "  cx.fillText('75%', 0, 250);"
#print "  cx.fillText('50%', 0, 500);"
#print "  cx.fillText('SOC', 0, 125);"
textFillBlue = (0, 0, 255, 255)
draw.text((0,0), "100%", fill=textFillBlue, font=fnt)
draw.text((0,100), "90%", fill=textFillBlue, font=fnt)
draw.text((0,200), "80%", fill=textFillBlue, font=fnt)
draw.text((0,240), "75%", fill=textFillBlue, font=fnt)
draw.text((0,500), "50%", fill=textFillBlue, font=fnt)
draw.text((0,125), "SOC", fill=textFillBlue, font=fnt)
# Draw power Y axis labels at the right edge
#print "  cx.fillStyle = 'green';"
#print "  cx.fillText('1000W', 530, 0);"
#print "  cx.fillText('500W', 530, 125);"
#print "  cx.fillText('250W', 530, 187);"
#print "  cx.fillText('0 W', 530, 250);"
#print "  cx.fillText('250W', 530, 312);"
#print "  cx.fillText('500W', 530, 375);"
#print "  cx.fillText('-1000W', 530, 500);"
#print "  cx.fillText('P (in)', 530, 100);"
#print "  cx.fillText('P (out)', 530, 400);"
textFillGreen = (0, 200, 0, 255)
draw.text((530,0), "1000W", fill=textFillGreen, font=fnt)
draw.text((530,125), "500W", fill=textFillGreen, font=fnt)
draw.text((530,187), "250W", fill=textFillGreen, font=fnt)
draw.text((530,250), "0W", fill=textFillGreen, font=fnt)
draw.text((530,312), "-250W", fill=textFillGreen, font=fnt)
draw.text((530,375), "-500W", fill=textFillGreen, font=fnt)
draw.text((530,500), "-1000W", fill=textFillGreen, font=fnt)
draw.text((530,100), "P (in)", fill=textFillGreen, font=fnt)
draw.text((530,400), "P (out)", fill=textFillGreen, font=fnt)

# PIL image can be saved as .png .jpg .gif or .bmp file
filename = "../bmvlasthour.jpg"
image.save(filename)

