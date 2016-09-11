#!/usr/bin/env python
# JH 2015-07-05
# Read data from the GPIO serial attached to a BMV-700 
# battery monitor, and log to a file

import time
import serial

# open the GPIO "UART" serial port at 19200 baud
bmvSerial = serial.Serial("/dev/ttyAMA0", baudrate=19200, timeout=3.0)
prevLogTick = 0

print "Starting VE.Direct monitor"
while True:
	s = bmvSerial.readline()
	s = s.strip("\r\n")
	print s
	values = s.split('\t')
#	print values
	if len(values) == 2 :
		#dataDict[values[0]] = values[1]
		# New frame?
		# Write current data set to "current" data file AND log file
		ticks = time.time()
		if values[0] == "PID" and (ticks - prevLogTick > 29.0) :
			prevLogTick = ticks
#			writeDataToCurrentFile(ticks)
#			writeDataToHistoryFile(ticks)
#			writeDataToLogFile(ticks)
			print("Ticks: %.0f" % ticks)
#			print("SOC: %s" % dataDict.get("SOC", "???"))


