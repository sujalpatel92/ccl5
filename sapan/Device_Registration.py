import requests
import time

#code for log
import logging

#import RPi.GPIO as gpio

#gpio.setmode(gpio.BOARD)
#gpio.setup(11, gpio.OUT)

#code for log
LOG_FILENAME = "pi_logs.txt"
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG,format='%(asctime)s %(message)s')

url = "http://35.162.32.72"
geturl = "http://35.162.32.72:8080/light/status"
DeviceId="CLOUD001"
payload= {'DeviceId': DeviceId}
import json

body = {'DeviceId':DeviceId}
header = {'Content-Type':'application/json', 'Accept':'application/json'}
response = requests.post('"http://35.162.32.72:8080/registerdevice/pi', headers = header, data = json.dumps(body), verify = False)
if response.status_code == 200:
    print "Registered"
    logging.debug("PI_Registered")

	
rget = requests.get(geturl,params = payload,verify = False)
while rget.status_code!=404:
        rget = requests.get(geturl,params = payload,verify = False)
        data= json.loads(rget.text)
        if data["light"]=="off":
                print 0
                logging.debug("Light_Status: OFF")
                #gpio.output(11, gpio.LOW)
        elif data["light"]=="on":
                print 1
                logging.debug("Light_Status: ON")
                #gpio.output(11, gpio.HIGH)
        time.sleep(1)
