import requests
import time
import RPi.GPIO as gpio
import json
import logging
import sys

LOG_FILENAME = "pi_logs.txt"
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG,format='%(asctime)s %(message)s')

gpio.setmode(gpio.BOARD)
gpio.setup(11, gpio.OUT)

lat = sys.argv[1]
gps_current = str(lat) + ",150"

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
	logging.debug("Fetching Light State from IoT Platform")
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
	gps_tmp = gps_in.split(",")
	gps_tmp2 = gps_current.split(",")
	if int(gps_tmp2[0]) - int(gps_tmp[0]) <= 2:
		gpio.output(11, gpio.HIGH)
	if int(gps_tmp2[0]) - int(gps_tmp[0]) <= -10:
		gpio.output(11, gpio.LOW)
	time.sleep(1)
	logging.debug("Connected to IoT Platform")
	#rget = requests.get(connecturl, params = payload, verify = False)
logging.debug("Device Disconnected")
