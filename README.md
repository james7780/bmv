Victron BMV-700 and MPPT Monitor for Raspberry Pi

James Higgs 2015-2016
james7780@yahoo.com

WARNING: THIS SETUP IS ONLY A GUIDELINE. MNWFY (May not work for you).

Requirements:

Raspberry Pi
Custom GPIO to VE.Direct cable
USB to TTL 3.3V serial cable (FTDI cable), with custom/hack VE.Direct connector

Configuration:

Raspberry Pi has lighttpd web server installed and RAM disk enabled (see "Installation.txt")
GPIO serial connection is configured as in "RPi to BMV-700.txt"

These files go in /home/pi/bmv:
bmv.py
bmvhistory.py
bmvlatest.py
lasthour.py
mppt.py
mpptlatest.py

These files go in /var/www/
index.html

These files go in /var/www/cgi-bin:
bmvhistory.py
bmvlatest.py
lasthour.py
mpptlatest.py

The logged data files will be written to /var/tmp (RAM disk if you enabled the RAM disk)

Access the web server using <rpi local ip address>/index.html

