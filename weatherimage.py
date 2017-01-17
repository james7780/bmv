#!/usr/bin/env python
# JH 2017-01-09
# Run python scripts to generate BMV/MPPT monitor RSS feed 

import time
import os
import json
import urllib2

# Use python-imaging to create jpgs
from PIL import Image, ImageDraw, ImageFont

# some color constants for PIL
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
PASTEL_BLUE = (64, 155, 235)
RED = (255, 0, 0)
PASTEL_RED = (240, 210, 210)
GREEN = (0,128,0)
PASTEL_GREEN = (210, 245, 210)
YELLOW = (255, 255, 0)
WIDTH = 800
HEIGHT = 480
LEFT = 16
RIGHT = 783
STRIPHEIGHT = 48
FONTSIZE = 28
MARGIN = 8
textFillBlack = (0, 0, 0, 255)

# draw the title strip for an image
def drawTitleStrip(draw, fillColour, fgColour, titleText, timeString) :
	draw.rectangle((LEFT, MARGIN, RIGHT, MARGIN + STRIPHEIGHT), fill=fillColour)
	fnt = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', FONTSIZE)
	draw.text((LEFT + MARGIN + 1, MARGIN + MARGIN + 1), titleText, fill=(64, 64, 64, 255), font=fnt)
	draw.text((LEFT + MARGIN, MARGIN + MARGIN), titleText, fill=textFillBlack, font=fnt)
	#draw.text((400 + MARGIN, MARGIN + MARGIN), timeString, fill=textFillBlack, font=fnt)

# draw a strip of data to the image
def drawStrip(draw, y0, fillColour, fgColour, meterColour, fnt, label, icon, meterValue, textValue) :
	draw.rectangle((LEFT, y0, RIGHT, y0 + STRIPHEIGHT), fill=fillColour)
	draw.text((LEFT + MARGIN, y0 + MARGIN), label, fill=textFillBlack, font=fnt)
	draw.text((RIGHT - 220, y0 + MARGIN), textValue, fill=textFillBlack, font=fnt)
	if (meterValue != 0) :
		drawMeter(draw, 250, y0 + MARGIN, 300, FONTSIZE, meterColour, meterValue)

# draw a horizontal meter/guage
def drawMeter(draw, x0, y0, width, height, meterColour, value) :
	draw.rectangle((x0, y0, x0 + width * value, y0 + height), fill=meterColour)
	draw.rectangle((x0, y0, x0 + width, y0 + height), outline=BLACK)

# decode Foreca weather code (eg: "d421")
def decodeWeatherCode(code) :
        # First number indicates cloud cover
        cloudCode = int(code[1])
        s = ['Clear', 'Almost clear', 'Half cloudy', 'Broken', 'Overcast', 'Thin high clouds', 'Fog'][cloudCode]
        s += ', '
        # Second number indicates precipitation rate
        rainCode = int(code[2])
        s += ['No rain', 'Slight Rain', 'Showers', 'Rain', 'Thunder'][rainCode]
        # 3rd number indicates type of precipitation (rain/sleet/snow) - ignore this for Cape Town
        return s

# draw a strip of data to the image
def drawWeatherStrip(draw, y0, fnt, dateLabel, temp, conditionCode, windSpeed, indDir, rain, humidity) :
	draw.rectangle((LEFT, y0, RIGHT, y0 + STRIPHEIGHT), fill=PASTEL_GREEN)
	ty = y0 + MARGIN
	tx = LEFT + MARGIN
	draw.text((tx, ty), dateLabel, fill=textFillBlack, font=fnt)
	conditions = decodeWeatherCode(conditionCode)
	draw.text((tx + 200, ty), str(temp) + '°C ' + conditions, fill=textFillBlack, font=fnt)
	draw.text((tx + 400, ty), 'Wind ' + windDir + ' ' + str(windSpeed * 3.6) + ' km/h, Rain ' + str(rain) + 'mm, Hum. ' + str(humidity) + '%', fill=textFillBlack, font=fnt)

# generate the weather image
# must be run once a day at 6am
def writeWeatherImage() :
	# create empty PIL image and draw "context" to draw on
	# PIL draws in memory only, but the image can be saved
	image = Image.new("RGB", (WIDTH, HEIGHT), WHITE)
	draw = ImageDraw.Draw(image)
	fnt = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', FONTSIZE)
	textFillBlue = (0, 0, 255, 255)
	drawTitleStrip(draw, PASTEL_BLUE, BLACK, "Weather - Cape Town")

	# get weather json data from Foreca
	url = "http://apitest.foreca.net/?lon=24.934&lat=60.1755&key=8UHAw41oBzi73lyzuSAGu3pyg&format=json"
	s = urllib2.urlopen(url).read()
	j = json.opens(s)
	if (len[j] > 0) :
		cc = j['cc']                    # "Current conditions"
		forecastArray = j['fcd']        # "Forecast data" (array of 10)
	
		# Display today's weather
		timeStamp = cc['dt']
		temp = cc['t']
		feelsLike = cc['tf']
		humidity = cc['rh']
		dewPoint = cc['dp']
		windSpeed = cc['ws']    # m/s
		windDir = cc['wn']      # 'N', 'SE' etc
		rain = cc['p']          # mm
		uv = cc['uv']           # 0 to 11
		drawWeatherStrip(draw, MARGIN + 60, fnt, timeStamp, temp, cc['s'], windSpeed, windDir, rain, humidity)

		# Display 6-day forecast data
		y = MARGIN + 60 + STRIPHEIGHT
		for data in forecastArray[1:6] :
			drawWeatherStrip(draw, y, fnt, data['dt'], data['t'], data['s'], data['ws'], data['wn'], data['p'], data['rh'])
			y += STRIPHEIGHT

		# draw time stamp
		draw.text((MARGIN * 2, 400), timeStamp, fill=textFillBlack, font=fnt)


	# Save as JPEG
	filename = "/var/www/weather.jpg"
	image.save(filename, quality=90)

