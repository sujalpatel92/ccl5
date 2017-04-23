from pyicloud import PyiCloudService
import sqlite3
import json
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

handler = logging.FileHandler('gps_from_phone.log')
handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)

apple_id = ""
password = ""
conn = sqlite3.connect('id_pass.db')
cur = conn.cursor()
cur.execute("SELECT * FROM pass")
data = cur.fetchall()
if len(data) == 0:
        conn.close()
        print "Error fetching data"
elif len(data) > 0:
        for item in data:
                apple_id = str(item[0])
                password = str(item[1])
conn.close()
api = PyiCloudService(apple_id, password)
if api.requires_2fa:
    import click
    print "Two-factor authentication required. Your trusted devices are:"

    devices = api.trusted_devices
    for i, device in enumerate(devices):
        print "  %s: %s" % (i, device.get('deviceName',
            "SMS to %s" % device.get('phoneNumber')))

    device = click.prompt('Which device would you like to use?', default=0)
    device = devices[device]
    if not api.send_verification_code(device):
        print "Failed to send verification code"
        sys.exit(1)

    code = click.prompt('Please enter validation code')
    if not api.validate_verification_code(device, code):
        print "Failed to verify verification code"
        sys.exit(1)

print api.devices
lon, lat = [], []
#while True:
tmp = json.loads(json.dumps(api.iphone.location()))
#print tmp["longitude"], tmp["latitude"]
#if tmp["longitude"] not in lon : lon.append(tmp["longitude"])
#if tmp["latitude"] not in lat: lat.append(tmp["latitude"])

import requests as req
import time


url = "http://0.0.0.0:8500/setgps"

while True:
	tmp = json.loads(json.dumps(api.iphone.location()))
	lat = tmp["latitude"]
	lon = tmp["longitude"]
	gps = str(lon) + "," + str(lat)
	print gps
	logger.debug("Posting GPS coordinates %s",gps)
	body = {"gps" : gps}
	header = {'Content-Type':'application/json', 'Accept':'application/json'}
	response = req.post(url, headers = header, data = json.dumps(body), verify = False)
	time.sleep(1)
