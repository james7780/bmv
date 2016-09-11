#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#print "Content-type: text/plain;charset=utf-8"
print "Content-type: text/html"
print
print "<!DOCTYPE HTML>"
print "<html>"
print "<head>"
print "<title>BMV-700 Current Status</title>"
print "<style>"
print "body { font-family: Verdana } "
print ".text { color: blue; border: 1px solid red; margin: 4px; padding: 4px; }"
print "</style>"
print "</head>"
print "<body>"
print "<H1>BMV-700 Current Status:</H1>"
print "<div class = \"text\">"

# Read and display the "current/latest" BMV data
#tfile = open("/home/pi/bmv/bmv.latest", "r")
tfile = open("/var/tmp/bmv.latest", "r")
if tfile :
#	s = tfile.read()
#	s.replace("\r", "<br>")
#	print s
#	tfile.close()
	for line in tfile :
		print line
		print "<br>"
	tfile.close()

print "</div>"
print "</body>"
print "</html>"



