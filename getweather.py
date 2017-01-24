#!/usr/bin/env python
# coding: utf-8
# JH 2017-01-09

import time
import os
import json
import urllib2

# get the weather data into a text file
# must be run once a day at 6am
def getForecaWeatherData() :
	# get weather json data from Foreca
	url = "http://apitest.foreca.net/?lon=18.42&lat=-33.92&key=8UHAw41oBzi73lyzuSAGu3pyg&format=json"
	s = urllib2.urlopen(url).read()
	text_file = open('/home/pi/bmv/weather_data.txt', 'w')
	text_file.write(s)
	text_file.close()

getForecaWeatherData()
