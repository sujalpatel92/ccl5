import json, requests as req
import time

url = "http://0.0.0.0:8500/setgps"

lat, lon = 0,0
while True:
	lat += 1
	lon += 1
	gps = str(lat) + "," + str(lon)
	print gps
	body = {"gps" : gps}
	header = {'Content-Type':'application/json', 'Accept':'application/json'}
	response = req.post(url, headers = header, data = json.dumps(body), verify = False)
	time.sleep(1)
