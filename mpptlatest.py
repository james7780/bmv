#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#print "Content-type: text/plain;charset=utf-8"
print "Content-type: text/html"
print
print "<!DOCTYPE HTML>"
print "<html>"
print "<head>"
print "<title>MPPT Current Status</title>"
print "<style>"
print "body { font-family: Verdana } "
print ".text { color: blue; border: 1px solid red; margin: 4px; padding: 4px; }"
print "</style>"
print "</head>"
print "<body>"
print "<H1>MPPT 100/50 Current Status:</H1>"
print "<div class = \"text\">"
print "<TABLE>"
# Read and display the latest MPPT data
#tfile = open("/home/pi/bmv/bmv.latest", "r")
tfile = open("/var/tmp/mppt.latest", "r")
if tfile :
#	s = tfile.read()
#	s.replace("\r", "<br>")
#	print s
#	tfile.close()
	for line in tfile :
		print "<TR>"
		print line
		print "</TR>"
	tfile.close()

print "</TABLE>"
print "</div>"
print "</body>"
print "</html>"



