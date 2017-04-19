import json, requests as req
import time
from random import randint

url = "http://ec2-35-162-32-72.us-west-2.compute.amazonaws.com:8500/setrpm"

rpm = 0
while True:
	rpm = randint(1,9) * 1000
	print rpm
	body = {"rpm" : rpm}
	header = {'Content-Type':'application/json', 'Accept':'application/json'}
	response = req.post(url, headers = header, data = json.dumps(body), verify = False)
	time.sleep(2)
