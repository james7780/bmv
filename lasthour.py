#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#import sh
import time
import os

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

print "Content-type: text/html"
print "Cache-Control: max-age=0, no-cache, no-store"
print "Pragma: no-cache"
print
print "<!DOCTYPE HTML>"
print "<html>"
print "<head>"
print "<title>BMV-700 Recent Chart</title>"
print "<meta http-equiv='Expires' content='0'/>"
print "<style>"
print "body { margin: 4px; padding: 4px; } "
print "</style>"
print "</head>"
print "<body>"
print "<H2>BMV-700 data over last hour:</H2>"
localtime = time.asctime(time.localtime(time.time()))
print "<div>Time = " + localtime + "</div>"
print "<canvas id='myCanvas' width='640' height='540'></canvas>"
print "<script>"
print "  var canvas = document.getElementById('myCanvas');"
print "  var cx = canvas.getContext('2d');"
# set scaling to match input range to canvas extents
print "  cx.scale(4, 1);"
# offset axes and grpah from the left edge
print "  cx.translate(10, 10);"
print "  cx.beginPath();"
print "  cx.moveTo(0, 0);"
print "  cx.lineTo(0, 500);"
print "  cx.lineTo(120, 500);"
print "  cx.moveTo(0, 250);"
print "  cx.lineTo(120, 250);"
print "  cx.moveTo(0, 0);"
print "  cx.lineTo(120, 0);"
print "  cx.stroke();"
# Draw SOC polyline
print "  cx.beginPath();"
print "  cx.strokeStyle = 'blue';"
x = 0
for v in charge :
	if x == 0 :
		print "  cx.moveTo(" + str(x) + ", " + str(v) + ");"
	else :
		print "  cx.lineTo(" + str(x) + ", " + str(v) + ");"
	x = x + 1
print "  cx.stroke();"
# Draw power polyline
print "  cx.beginPath();"
print "  cx.strokeStyle = 'green';"
x = 0
for v in power :
	v = 250 - v / 4
	if x == 0 :
		print "  cx.moveTo(" + str(x) + ", " + str(v) + ");"
	else :
		print "  cx.lineTo(" + str(x) + ", " + str(v) + ");"
	x = x + 1
print "  cx.stroke();"
# Draw SOC Y axis labels at the left edge
print "  cx.translate(-10, 0);"
print "  cx.scale(0.25, 1);"
print "  cx.font = 'bold 10pt Verdana';"
print "  cx.fillStyle = 'blue';"
print "  cx.fillText('100%', 0, 0);"
print "  cx.fillText('90%', 0, 100);"
print "  cx.fillText('80%', 0, 200);"
print "  cx.fillText('75%', 0, 250);"
print "  cx.fillText('50%', 0, 500);"
print "  cx.fillText('SOC', 0, 125);"
# Draw power Y axis labels at the right edge
print "  cx.fillStyle = 'green';"
print "  cx.fillText('1000W', 530, 0);"
print "  cx.fillText('500W', 530, 125);"
print "  cx.fillText('250W', 530, 187);"
print "  cx.fillText('0 W', 530, 250);"
print "  cx.fillText('250W', 530, 312);"
print "  cx.fillText('500W', 530, 375);"
print "  cx.fillText('-1000W', 530, 500);"
print "  cx.fillText('P (in)', 530, 100);"
print "  cx.fillText('P (out)', 530, 400);"
print "</script>"
print "</body>"
print "</html>"
  
