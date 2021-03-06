#!/usr/bin/env python
# JH 2017-01-09
# Run python scripts to generate BMV/MPPT monitor RSS feed 

import time
import os
#import subprocess

# Use python-imaging to create jpgs
from PIL import Image, ImageDraw, ImageFont

# some color constants for PIL
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
green = (0,128,0)
width = 800
height = 480

#write the "BMV latest" image
def writeBMVLatestImage() :
	# create empty PIL image and draw "context" to draw on
	# PIL draws in memory only, but the image can be saved
	image = Image.new("RGB", (width, height), white)
	draw = ImageDraw.Draw(image)
	fontSize = 24
	fnt = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', fontSize)
	left = 20
	textFillBlue = (0, 0, 255, 255)
	draw.text((left,0), "BMV-700 Current Status:", fill=textFillBlue, font=fnt)
	y = fontSize * 2

	# Read and display the "current/latest" BMV data
	#tfile = open("/home/pi/bmv/bmv.latest", "r")
	tfile = open("/var/tmp/bmv.latest", "r")
	if tfile :
		for line in tfile :
			draw.text((left, y), line, fill=textFillBlue, font=fnt)
			y = y + fontSize * 1.5
		tfile.close()

	# PIL image can be saved as .png .jpg .gif or .bmp file
	filename = "/var/www/bmvcurrent.jpg"
	image.save(filename)

# Write the "last hour" image
def writeBMVLastHourImage() :
	# get last 120 lines (60 minutes) of the bmv log
	#os.system("tail --lines=120 /home/pi/bmv/bmv.log > /var/www/cgi-bin/chart.log")
	os.system("tail --lines=120 /var/tmp/bmv.log > /var/tmp/bmv_chart.log")

	# parse the log file into an array of values
	charge = []			# Array of SOC values
	power = []			# Array of Power (W) values
	ticks = 0
	y = 0
	tfile = open("/var/tmp/bmv_chart.log", "r")
	if tfile :
		for line in tfile :
			s = line.split(',')
			#print s[5]
			if (len(s) > 5 and s[5] != "SOC") :		# skip header line
				y = int(s[5])		# 1000 = 100% (SOC)
				charge.append(y)
				y = int(s[3])       # Power (W)
				power.append(y)
				ticks = int(s[0])   # time of log
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
	if (len(charge) > 0) :
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
	if (len(charge) > 0) :
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
	logTime = time.asctime(time.localtime(ticks))
	draw.text((left, 460), logTime, fill=textFillBlack, font=fnt)

	# PIL image can be saved as .png .jpg .gif or .bmp file
	filename = "/var/www/bmvlasthour.jpg"
	image.save(filename)

	
# Write the MPPT latest image
def writeMPPTLatestImage() :
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

# Write the rss file
def writeRSSFile(image1, image2, image3) :
	tfile = open("/var/www/index.rss", "w")
	tick1 = time.time()
	tick2 = tick1 + 1
	tick3 = tick2 + 1
	tfile.write('<?xml version="1.0" encoding="UTF-8" ?>\n')
	tfile.write('<rss version="2.0" xmlns:media="http://search.yahoo.com/mrss/">\n')
	tfile.write('<channel>\n')
	tfile.write('  <title>Home Monitor</title>\n')
	tfile.write('  <ttl>2</ttl>\n')
	tfile.write('  <link>http://10.0.0.85/index.html</link>\n')
	tfile.write('  <description>BMV / MPPT Monitor</description>\n')
	tfile.write('  <item>\n')
	tfile.write('    <title>Item 1</title>\n')
	tfile.write('    <link>http://10.0.0.85/index.html</link>\n')
	tfile.write('    <description>BMV Latest</description>\n')
	tfile.write('    <media:content url="http://10.0.0.85/%s" type="image/jpeg" />\n' % image1)
	tfile.write('    <guid>%s</guid>\n' % str(tick1))
	tfile.write('  </item>\n')
	tfile.write('  <item>\n')
	tfile.write('    <title>Item 2</title>\n')
	tfile.write('    <link>http://10.0.0.85/index.html</link>\n')
	tfile.write('    <description>BMV Last Hour</description>\n')
	tfile.write('    <media:content url="http://10.0.0.85/%s" type="image/jpeg" />\n' % image2)
	tfile.write('    <guid>%s</guid>\n' % str(tick2))
	tfile.write('  </item>\n')
	tfile.write('  <item>\n')
	tfile.write('    <title>Item 3</title>\n')
	tfile.write('    <link>http://10.0.0.85/index.html</link>\n')
	tfile.write('    <description>MPPT Latest</description>\n')
	tfile.write('    <media:content url="http://10.0.0.85/%s" type="image/jpeg" />\n' % image3)
	tfile.write('    <guid>%s</guid>\n' % str(tick3))
	tfile.write('  </item>\n')
	tfile.write('</channel>\n')
	tfile.write('</rss>\n')
	tfile.close()
	return

#writeBMVLatestImage()
#writeBMVLastHourImage()
#writeMPPTLatestImage()
#writeRSSFile("bmvcurrent.jpg", "bmvlasthour.jpg", "mpptcurrent.jpg")

# wait for other BMV logging processes to actually generate some log data
print "Waiting 5 minutes for BMV and MPPT logging processes..."
time.sleep(300)

prevTick = time.time()

print "Starting RSS image generator..."
while True:
	time.sleep(30)
	ticks = time.time()
	if (ticks - prevTick > 59) :
		prevTick = ticks
		#subprocess.call(['python', '/var/www/cgi-bin/bmvlatestimage.py'])
		#subprocess.call(['python', '/var/www/cgi-bin/bmvlasthourimage.py'])
		#subprocess.call(['python', '/var/www/cgi-bin/mpptlatestimage.py'])
		print "Writing images"
		writeBMVLatestImage()
		writeBMVLastHourImage()
		writeMPPTLatestImage()
		writeRSSFile("bmvcurrent.jpg", "bmvlasthour.jpg", "mpptcurrent.jpg")



