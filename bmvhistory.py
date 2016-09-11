#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#print "Content-type: text/plain;charset=utf-8"
print "Content-type: text/html"
print
print "<!DOCTYPE HTML>"
print "<html>"
print "<head>"
print "<title>BMV-700 Historical Data</title>"
print "<style>"
print "body { font-family: Verdana } "
print "</style>"
print "</head>"
print "<body>"
print "<H2>BMV-700 Historical Data:</H2>"
print "<div>"

# Read and display the "historical" BMV data
#tfile = open("/home/pi/bmv/bmv.history", "r")
tfile = open("/var/tmp/bmv.history", "r")
if tfile :
	for line in tfile :
		print line
		print "</br>"
	tfile.close()

print "</div>"
print "</body>"
print "</html>"



