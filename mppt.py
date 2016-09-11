#!/usr/bin/env python
# JH 2015-10-03
# Read data from the GPIO serial attached to a MPPT 100/50 
# solar charger, and log to a file

import time
import serial

# open the GPIO "UART" serial port at 19200 baud
# TODO : Use and alternate serial port to read the BMV simultaneously
bmvSerial = serial.Serial("/dev/ttyAMA0", baudrate=19200, timeout=3.0)

# open the log file for appending to
# 2015-09-20 - Log to RAMDISK mounted on /var/tmp
#logFile = open("/home/pi/bmv/bmv.log", "a")
logFile = open("/var/tmp/mppt.log", "a")
logFile.write("Ticks,V,I,VPV,PPV,CS,H19,H20,H21,H22,H23\n")

dataDict = {}

# Write the current MPPV dictionary data to the "current data" file
def writeDataToCurrentFile(ticks) :
	#tfile = open("/home/pi/bmv/bmv.latest", "w")
	tfile = open("/var/tmp/mppt.latest", "w")
	localtime = time.asctime(time.localtime(ticks))
	tfile.write("<TD>Time</TD><TD>%s</TD>\n" % localtime)
	#tfile.write("PID=%s\n" % dataDict.get("PID", "???"))
	f = float(dataDict.get("V", "0")) / 1000.0
	tfile.write("<TD>Batt. Voltage</TD><TD>%.3f V</TD>\n" % f)
	f = float(dataDict.get("I", "0")) / 1000.0
	tfile.write("<TD>Batt. Current</TD><TD>%.3f A</TD>\n" % f)
	f = float(dataDict.get("VPV", "0")) / 1000.0
	tfile.write("<TD>Panel Voltage</TD><TD>%.3f V</TD>\n" % f)
	tfile.write("<TD>Panel Power</TD><TD>%s W</TD>\n" % dataDict.get("PPV", "???"))
	tfile.write("<TD>Charge State</TD><TD>%s (3 = Bulk, 4 = Absorbtion, 5 = Float)</TD>\n" % dataDict.get("CS", "???"))
	tfile.write("<TD></TD><TD></TD>\n");
	f = float(dataDict.get("H19", "0")) / 100.0
	tfile.write("<TD>Yield Total</TD><TD>%.1f kWh</TD>\n" % f)
	f = float(dataDict.get("H20", "0")) / 100.0
	tfile.write("<TD>Yield Today</TD><TD>%.3f kWh</TD>\n" % f)
	tfile.write("<TD>Max. Power Today</TD><TD>%s W</TD>\n" % dataDict.get("H21", "???"))
	f = float(dataDict.get("H22", "0")) / 100.0
	tfile.write("<TD>Yield Yesterday</TD><TD>%.3f kWh</TD>\n" % f)
	tfile.write("<TD>Max. Power Yesterday</TD><TD>%s W</TD>\n" % dataDict.get("H23", "???"))
	tfile.close()
	return 0

# Write the current data to the log file
def writeDataToLogFile(ticks) :
	#"Ticks,V,I,VPV,PPV,CS\n")
	logFile.write("%.0f," % ticks)
	logFile.write("%s," % dataDict.get("V", "?"))
	logFile.write("%s," % dataDict.get("I", "?"))
	logFile.write("%s," % dataDict.get("VPV", "?"))
	logFile.write("%s," % dataDict.get("PPV", "?"))
	logFile.write("%s\n" % dataDict.get("CS", "?"))
	return

# Previous log tick - used for logging only every 10 seconds
prevLogTick = time.time()

print "Starting MPPT monitor/logger..."
while True:
	s = bmvSerial.readline()
#	print s
	s = s.strip("\r\n")
	values = s.split('\t')
#	print values
	if len(values) == 2 :
		dataDict[values[0]] = values[1]
		# New frame?
		# Write current data set to "current" data file AND log file
		ticks = time.time()
		if values[0] == "PID" and (ticks - prevLogTick > 29.0) :
			prevLogTick = ticks
			writeDataToCurrentFile(ticks)
			#writeDataToHistoryFile(ticks)
			writeDataToLogFile(ticks)
			print("Ticks: %.0f" % ticks)
			print("VPV: %s" % dataDict.get("VPV", "???"))


