import json, requests as req
import time
from random import randint

url = "http://0.0.0.0:8500/setrpm"

rpm = 0
while True:
	rpm = randint(1,9) * 1000
	print rpm
	body = {"rpm" : rpm}
	header = {'Content-Type':'application/json', 'Accept':'application/json'}
	response = req.post(url, headers = header, data = json.dumps(body), verify = False)
	time.sleep(2)
