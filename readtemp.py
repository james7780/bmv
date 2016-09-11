#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# JH 2014-06-26

sensorID1 = "28-0000053cfc10"
sensorID2 = "28-0000053d00bf"

#print "Content-type: text/plain;charset=utf-8"
print "Content-type: text/html"
print
print "<!DOCTYPE HTML>"
print "<html><head><title>Rasperry Pi Temp Monitor</title></head>"
print "<style>"
print "body { font-family: Verdana } "
print ".tempReading { color: blue; border: 1px solid red; margin: 4px; padding: 4px; } "
print "</style>"
print "<body>"
print "<H1>Water Temp Monitor</H1>"

print "<div class = \"tempReading\">"
# open the temp sensor
print ("Reading temp from sensor " + sensorID1 + "<br>")
tfile = open("/sys/bus/w1/devices/" + sensorID1 + "/w1_slave")
# read the temp sensor output
text = tfile.read()
# close the temp sensor "file"
tfile.close()
# split the text and get the 2nd line
secondLine = text.split("\n")[1]
# split the line into words, and get the 10th word
tempData = secondLine.split(" ")[9]
# remove "t=" and convert to a float
temperature = float(tempData[2:])
# display as degrees C
temperature = temperature / 1000
print "DS18B20 (1) temp = ", temperature, " degrees"
print "</div>"

print "<div class = \"tempReading\">"
# open the temp sensor
print ("Reading temp from sensor " + sensorID2 + "<br>")
tfile = open("/sys/bus/w1/devices/" + sensorID2 + "/w1_slave")
# read the temp sensor output
text = tfile.read()
# close the temp sensor "file"
tfile.close()
# split the text and get the 2nd line
secondLine = text.split("\n")[1]
# split the line into words, and get the 10th word
tempData = secondLine.split(" ")[9]
# remove "t=" and convert to a float
temperature = float(tempData[2:])
# display as degrees C
temperature = temperature / 1000
print "DS18B20 (2) temp = ", temperature, " degrees"
print "</div>"

print "</body>"
print "</html>"

