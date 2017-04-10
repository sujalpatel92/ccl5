import requests
import time
import RPi.GPIO as gpio
import json
import logging

LOG_FILENAME = "pi_logs.txt"
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG,format='%(asctime)s %(message)s')

gpio.setmode(gpio.BOARD)
gpio.setup(11, gpio.OUT)



url = "http://35.162.32.72"
geturl = "http://35.162.32.72:8005/light/status"
connecturl = "http://35.162.32.72:8005/connect/pi"

DeviceId="88521B7AD79BE277"
Email = "sapan2211@gmail.com"
payload= {'DeviceId': DeviceId, 'Email': Email}

flag=0
logging.debug("Connected to IoT Platform")
rget = requests.get(connecturl,params = payload,verify = False)
while rget.status_code!=404:
	logging.debug("Fetching Light State from IoT Platform")
	rget = requests.get(geturl,params = payload,verify = False)
        if rget.status_code == 404:
		break
	data= json.loads(rget.text)
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
        time.sleep(1)
	logging.debug("Connected to IoT Platform")
	rget = requests.get(connecturl, params = payload, verify = False)
logging.debug("Device Disconnected")
