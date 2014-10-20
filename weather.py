#!/usr/bin/env python
# -*- coding: utf-8 -*-

############ Version information ##############
__version__ = "0.2"
__program__ = "Weather Monitor v" + __version__
__description__ = 'Writes weatherdata to an LCD display'
__author__ = "Jan Rude, Peter Franzreb"
__licence__ = "BSD Licence"
###############################################

try:
	import serial
except:
	print 'You need to install pySerial (https://pypi.python.org/pypi/pyserial)'
	exit(-1)
import requests
import json
import httplib
import time
import sys

def main(argv):
	port = raw_input('\nUSB Port to Arduino:\t')
	lang = raw_input('\nLanguage (de/en/it/fr):\t')
	print 'Setting up connection...'
	try:
		ser = serial.Serial(port, 9600)
		ser.isOpen()
		print 'done'
		while True:
			location = raw_input('\nPlease provide a City (Enter "exit" to leave):\t')
			if location == "exit":
				break
			else:
				if sys.platform == 'win32':
					location = win_encode(location)
				else:
					location = encode(location)
				location = location.replace(' ', '%20')
				try:
					path = '/data/2.5/find?q=LOCATION&units=metric&lang=' + lang
					path = path.replace('LOCATION', location)
					conn = httplib.HTTPConnection("api.openweathermap.org", timeout=10)
					conn.request("GET", path)
					r1 = conn.getresponse()
					data = json.load(r1)
				
					city = str((data['list'][0]['name']).encode('utf8'))
					if '?' in city:
						city = location
					else:
						city = encode(city)
					country = str(data['list'][0]['sys']['country'])
					temp = str(data['list'][0]['main']['temp'])
					humidity = str(data['list'][0]['main']['humidity'])
					sky = str((data['list'][0]['weather'][0]['description']).encode('utf8'))
					sky = encode(sky)
					print('Weather for ' + city + '/' + country)
					print 'Temp:', temp, 'C'
					print 'Humidity:', humidity, '%'
					print "Sky: " + sky
					print ''

					ser.write(city +'/' + country + '\n')
					ser.write('  ' + temp + chr(223) + 'C\n')
					ser.write('  ' + humidity + '%\n')
					ser.write('  ' + sky + '\n')
					time.sleep(1.5)
				except Exception, e:
					print e
	except Exception, e:
		print e
	finally:	
		ser.close()
		print '\nconnection closed'
		return True

def encode(tag):
	tag = tag.replace('\xc3\xa4', 'ae')
	tag = tag.replace('\xc3\xb6', 'oe')
	tag = tag.replace('\xc3\xbc', 'ue')
	tag = tag.replace('\xc3\x9f', 'ss')
	return tag

def win_encode(userinput):
	userinput = userinput.replace('\x84', 'ae')
	userinput = userinput.replace('\x94', 'oe')
	userinput = userinput.replace('\x81', 'ue')
	userinput = userinput.replace('\xe1', 'ss')
	return userinput

if __name__ == "__main__":
	print('\n' + 50*'*')
	print('\t' + __program__ )
	print('\t' + __description__)
	print('\t' + '(c)2014 by ' + __author__)
	print(50*'*')
	sys.exit( not main( sys.argv ) )
