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
geturl = "http://35.162.32.72:8000/light/status"
DeviceId="[your DeviceID]"
payload= {'DeviceId': DeviceId}


rget = requests.get(geturl,params = payload,verify = False)
while rget.status_code!=404:
        rget = requests.get(geturl,params = payload,verify = False)
        data= json.loads(rget.text)
        if data["light"]=="off":
                print 0
                gpio.output(11, gpio.LOW)
				logging.debug("Light_Status: OFF")
        elif data["light"]=="on":
                print 1
                gpio.output(11, gpio.HIGH)
				logging.debug("Light_Status: ON")
        time.sleep(1)
