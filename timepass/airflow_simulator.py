import json, requests as req
import time
from random import randint
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

handler = logging.FileHandler('airflow_simulator.log')
handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)


url = "http://0.0.0.0:8500/setaf"

airflow = 0
while True:
	airflow = randint(1, 9) * 1000
	print(airflow)
	logger.debug("Airflow posted %s",airflow)
	body = {"air_flow" : airflow}
	header = {'Content-Type':'application/json', 'Accept':'application/json'}
	response = req.post(url, headers = header, data = json.dumps(body), verify = False)
	time.sleep(1)
