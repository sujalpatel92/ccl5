import json, requests as req
import time
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

handler = logging.FileHandler('gps_simulator.log')
handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)

url = "http://0.0.0.0:8500/setgps"

lat, lon = 0, 0
while True:
	lat += 1
	lon += 1
	gps = str(lon) + "," + str(lat)
	print gps
	body = {"gps" : gps}
	logger.debug("Posting GPS %s",gps)
	header = {'Content-Type':'application/json', 'Accept':'application/json'}
	response = req.post(url, headers = header, data = json.dumps(body), verify = False)
	time.sleep(1)
