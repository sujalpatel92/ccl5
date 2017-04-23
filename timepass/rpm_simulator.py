import json, requests as req
import time
from random import randint
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

handler = logging.FileHandler('iotplatform.log')
handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)

url = "http://0.0.0.0:8500/setrpm"

rpm = 0
while True:
	rpm = randint(1,9) * 1000
	print rpm
	logger.debug("Posting RPM %s",rpm)
	body = {"rpm" : rpm}
	header = {'Content-Type':'application/json', 'Accept':'application/json'}
	response = req.post(url, headers = header, data = json.dumps(body), verify = False)
	time.sleep(2)
