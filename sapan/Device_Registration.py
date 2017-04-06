import requests
import time
#import RPi.GPIO as gpio

#gpio.setmode(gpio.BOARD)
#gpio.setup(11, gpio.OUT)

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

	
rget = requests.get(geturl,params = payload,verify = False)
while rget.status_code!=404:
        rget = requests.get(geturl,params = payload,verify = False)
        data= json.loads(rget.text)
        if data["light"]=="off":
                print 0
                #gpio.output(11, gpio.LOW)
        elif data["light"]=="on":
                print 1
                #gpio.output(11, gpio.HIGH)
        time.sleep(1)
