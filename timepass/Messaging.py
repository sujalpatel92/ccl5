import requests
import time
import RPi.GPIO as gpio
import json
import logging
import sys

LOG_FILENAME = "pi_receiver.log"
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG,format='%(asctime)s %(message)s')

gpio.setmode(gpio.BOARD)
gpio.setup(11, gpio.OUT)

lat = 3298640
lon = -9677585

url = "http://35.162.32.72"
geturl = "http://35.162.32.72:9200/gps"
connecturl = "http://35.162.32.72:8005/connect/pi"

DeviceId="88521B7AD79BE277"
Email = "sapan2211@gmail.com"
payload= {'DeviceId': DeviceId, 'Email': Email}

flag=0
logging.debug("Connected to IoT Platform")
#rget = requests.get(connecturl,params = payload,verify = False)
while True:
	logging.debug("Fetching GPS from IoT Platform")
	rget = requests.get(geturl,params = payload,verify = False)
        if rget.status_code == 404:
		break
	data= json.loads(rget.text)
        '''
	if data["light"]=="off":
                print 0
                gpio.output(11, gpio.LOW)
		if flag==1:
			logging.debug("Light_Status: OFF")
			flag=0
        elif data["light"]=="on":
                print 1
                gpio.output(11, gpio.HIGH)
		if flag==0:
			logging.debug("Light_Status: ON")
			flag=1
        '''
	gps_in = data["gps"]
	logging.debug("GPS received %s", gps_in)
	gps_tmp = gps_in.split(",")
	#gps_tmp2 = gps_current.split(",")
	lon_in = int(float(gps_tmp[0]) * (10**5))
	lat_in = int(float(gps_tmp[1]) * (10**5))
	print lon_in, lat_in
	if abs(abs(lon) - abs(lon_in)) <= 12 and abs(abs(lat) - abs(lat_in)) <= 12:
		gpio.output(11, gpio.HIGH)
		logging.debug("Light is ON")
	else:
		gpio.output(11, gpio.LOW)
		logging.debug("Light is Off")
	time.sleep(1)
	#logging.debug("Connected to IoT Platform")
	#rget = requests.get(connecturl, params = payload, verify = False)
logging.debug("Device Disconnected")

