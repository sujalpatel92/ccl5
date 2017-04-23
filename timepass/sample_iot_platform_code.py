from __future__ import print_function
from pyicloud import PyiCloudService
import sqlite3
import bottle, json, time, sys, os, datetime
from bottle import get,post,request,response,route,run,Bottle
from rocket import Rocket
import logging

# debug variable for light state
lState = "off"
# debug variable for dummy id
last_dummy_number = 0
# debug list to maintain id's dispatched to pi
id_given_to_pi = list()
send_confirm_pi = list()
# dict to store Light state of all pi's
deviceLEDState = dict()
# list of registered devices
registeredDevices = list()
# dict to store last connected time of pi
pi_last_connected = dict()
# list to store device id's whose confirmation is awaited
await_pi_confirm = list()
# global variables
gps = "0,0"
rpm = "0"
af = "0"

#debug list for dynamic logging
device_logger = dict()

#logging related initializations
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

handler = logging.FileHandler('lab5.log')
handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)
"""
This class is used to decode json file.
The output can be either dictionary or list
"""
class JsonDecode():

    @staticmethod
    def get_list(data):
        retval = []
        for item in data:
            if isinstance(item,unicode):
                item = item.encode('utf-8')
            elif isinstance(item, list):
                item = JsonDecode.get_list(item)
            elif isinstance(item, dict):
                item = JsonDecode.get_dict(item)
            retval.append(item)
        return retval

    @staticmethod
    def get_dict(data):
        retval = {}
        for key,value in data.iteritems():
            if isinstance(key,unicode):
                key = key.encode('utf-8')
            if isinstance(value,unicode):
                value = value.encode('utf-8')
            elif isinstance(value,list):
                value = JsonDecode.get_list(value)
            elif isinstance(value,dict):
                value = JsonDecode.get_dict(value)
            retval[key] = value
        return retval

#dynamic logger initialization
def generateLoggerHandler(pi_id):
	#logging related initializations
	logger = logging.getLogger(pi_id)
	logger.setLevel(logging.DEBUG)

	file_name = '/var/www/html/' + str(pi_id) + '.log'
	handler = logging.FileHandler(file_name)
	handler.setLevel(logging.DEBUG)

	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	handler.setFormatter(formatter)

	logger.addHandler(handler)
	return logger

# bottle necessary initialization for creating deployable app
app = Bottle(__name__)
# for debugging
app.debug = True

# function to return ip address of the requester
@app.route('/myip')
#@app.get('/myip')
#@app.post('/myip')
def showip():
	ip = request['REMOTE_ADDR']
	print(ip)
	return {'ip':ip}

"""
This function is used to get the light status for a raspberry pi
input: request object with params = {'DeviceId':<id>} form
return: stored state of the LED on that pi
"""
@app.get('/light/status')
def tellLightState():
	# need to complete implementation. currently partial implementation
	global deviceLEDState, logger, device_logger
	deviceid = request.params["DeviceId"]
	if deviceid in deviceLEDState:
		if deviceid in pi_last_connected:
			now = datetime.datetime.now()
			pi_last_connected[deviceid] = str(now)
		logger.info('Sending Light Status %s to pi with ID: %s', deviceLEDState[deviceid],deviceid)
		device_logger[deviceid].info('Sending Light Status %s',deviceLEDState[deviceid])
		return {'light':deviceLEDState[deviceid]}
	else:
		return bottle.HTTPResponse(status=404)

"""
This function is used to update the LED status of pi from the user end
input request object with body = {'DeviceId':<id>, 'Light':<state>}
return HTTP 200 on sucessful status change else HTTP 500
"""
@app.post('/light/status')
def setLightState():
	# need to complete implementation. currently partial implementation.
	global lState, logger, device_logger
	payload = json.dumps(request.json)
	print(payload)
	tmp = json.loads(payload, object_hook = JsonDecode.get_dict)
	print(tmp['light'])
	lState = tmp['light']
	pi_id = tmp['pi_id']
	deviceLEDState[pi_id] = lState
	logger.info('Received Light State %s for pi with ID: %s', tmp['light'], tmp['pi_id'])
	device_logger[pi_id].info('Received Light State %s from front end', tmp['light'])
	return bottle.HTTPResponse(status=200)

"""
This function is used to register the pi.
This end-point will be called from pi and pi will be registered in device registry
input: request object with body = {'DeviceID':<id>}
return: HTTP 200 on successful or HTTP 500
"""
@app.post('/registerdevice/pi')
def registerpi():
	# need to complete implementation. Currently partial implementation
	global registeredDevices, await_pi_confirm, logger, device_logger
	payload = json.loads(json.dumps(request.json), object_hook = JsonDecode.get_dict)
	print(payload["DeviceId"])
	pi_id = payload["DeviceId"]
	if pi_id in registeredDevices:
		return bottle.HTTPResponse(status=200)
	else:
		if pi_id not in id_given_to_pi:
			return bottle.HTTPResponse(status=404)
		#registeredDevices.append(pi_id)
		#deviceLEDState[pi_id] = "off"
		now = datetime.datetime.now()
		pi_last_connected[pi_id] = str(now)
		if pi_id in await_pi_confirm:
			await_pi_confirm.remove(pi_id)
		if pi_id in id_given_to_pi:
			id_given_to_pi.remove(pi_id)
			send_confirm_pi.append(pi_id)
		logger.info('PI Register request received from pi with ID: %s',pi_id)
		return bottle.HTTPResponse(status=200)

"""
This function is used to register the pi from front end
input: request obejct with body = {'DeviceId':<id>}
return: HTTP 200 on successful or HTTP 500
"""
@app.post('/registerdevice/frontend')
def registerfromfrontend():
	# need to check if this implementation is really needed
	global await_pi_confirm, registeredDevices
	payload = json.loads(json.dumps(request.json), object_hook = JsonDecode.get_dict)
	pi_id = payload["DeviceId"]
	await_pi_confirm.append(pi_id)
	"""
	*WARNING*
	Blocking call here
	need to upgrade this call with locking or remove it altogether
	"""
	while pi_id in await_pi_confirm:
		pass
	if pi_id in registeredDevices:
		return bottle.HTTPResponse(status = 200)
	else:
		return bottle.HTTPResponse(status = 500)

"""
Dummy function for the sake of frontend development
"""
@app.get('/registerpi/get_pi_id/dummy')
def getDummyId():
    # partial implementation
    global logger
    dummy_id = generateID()
    id_given_to_pi.append(dummy_id)
    logger.debug('Generated Pi ID: %s',dummy_id)
    return {'pi_id':dummy_id}

"""
Another dummy function for sake of frontend development
"""
@app.get('/registerpi/get_pi_confirmation')
def get_pi_confirmation():
    # partial implementation. Need to implement this completely
    global logger, device_logger
    print(request["REMOTE_ADDR"])
    print(request.params)
    print(request.params["pi_id"])
    print(str(request.params["pi_id"]).split('|'))
    pi_id = str(request.params["pi_id"]).split('|')[0]
    print(pi_id)
    print(send_confirm_pi)
    print(id_given_to_pi)
    if pi_id in send_confirm_pi:
	send_confirm_pi.remove(pi_id)
	registeredDevices.append(pi_id)
	deviceLEDState[pi_id] = "off"
	logger.info('PI successfully registered with pi ID: %s', pi_id)
	logs = generateLoggerHandler(pi_id)
	device_logger[pi_id] = logs
	device_logger[pi_id].info('PI successfully registered.')
        return bottle.HTTPResponse(status=200)
    elif pi_id in registeredDevices:
	logger.error('PI already registered with pi ID: %s', pi_id)
	return bottle.HTTPResponse(status=403)
    else:
	logger.error('Wrong PI ID requested to register from front end. Incorrect pi ID: %s', pi_id)
    	return bottle.HTTPResponse(status=404)	

"""
This function is to de-register the pi
"""
@app.route('/deregisterpi')
def deRegisterPi():
	global registeredDevices, deviceLEDState, logger
	pi_id = str(request.params["pi_id"]).split('|')[0]
	if pi_id in registeredDevices:
		registeredDevices.remove(pi_id)
	else:
		return bottle.HTTPResponse(status=500)
	if pi_id in deviceLEDState:
		del deviceLEDState[pi_id]
	else:
		return bottle.HTTPResponse(status=500)
	logger.info('PI deregistered successfully. pi ID: %s', pi_id)
	device_logger[pi_id].info('PI successfully deregistered.')
	del device_logger[pi_id]
	return bottle.HTTPResponse(status=200)

"""
This function returns logs for pi address
"""
@app.get('/getlogs')
def getLogs():
	global logger
	pi_id = str(request.params["pi_id"]).split('|')[0]
	print(pi_id, 'inside getLogs')
	f = open('iotplatform.log','r')
	lines = f.readlines()
	log_array = []
	for line in lines:
		if pi_id in line:
			log_array.append(line)
	f.close()
	print(log_array)
	return {'logs':log_array}

"""
This function returns ip of page where to redirect to get logs
"""
@app.get('/getlogip')
def getLogIP():
	global logger, device_logger
	pi_id = str(request.params["pi_id"]).split('|')[0]
	url = "http://35.162.32.72/" + str(pi_id) + '.log'
	#return {'url':url}
	return bottle.HTTPResponse(url)

#Lab5 related functions
"""
"""
@app.post('/report')
def report_from_pi2():
	global logger, device_logger, gps, rpm, af
	payload = json.loads(json.dumps(request.json), object_hook = JsonDecode.get_dict)
	gps = payload['gps']
	rpm = payload['rpm']
	af = payload['air_flow']
	print(payload)
	logger.debug("Received Report from Pi")
	return bottle.HTTPResponse(status = 200)

"""
"""
@app.get('/gps')
def getGPS():
	global gps
	logger.debug("Sending GPS to Pi")
	return {"gps" : gps}
	
"""
"""
@app.get('/gps_based_light')
def getLight():
	global gps
	apple_id = ""
	password = ""
	conn = sqlite3.connect('id_pass.db')
	cur = conn.cursor()
	cur.execute("SELECT * FROM pass")
	data = cur.fetchall()
	if len(data) == 0:
        	conn.close()
        	print("Error fetching data")
	elif len(data) > 0:
        	for item in data:
                	apple_id = str(item[0])
	                password = str(item[1])
		conn.close()
	api = PyiCloudService(apple_id, password)
	if api.requires_2fa:
		import click
		print("Two-factor authentication required. Your trusted devices are:")

		devices = api.trusted_devices
		for i, device in enumerate(devices):
			print("  %s: %s" % (i, device.get('deviceName',"SMS to %s" % device.get('phoneNumber'))))

		device = click.prompt('Which device would you like to use?', default=0)
		device = devices[device]
		if not api.send_verification_code(device):
			print("Failed to send verification code")
			sys.exit(1)

		code = click.prompt('Please enter validation code')
		if not api.validate_verification_code(device, code):
			print("Failed to verify verification code")
			sys.exit(1)
	tmp = json.loads(json.dumps(api.iphone.location()))
	tmp2 = str(tmp["longitude"]) + "," + str(tmp["latitude"])
	return {"gps":tmp2}

"""
This function generates ID for pi
"""
def generateID():
    global last_dummy_number
    last_dummy_number+= 1
    dummy_id = "DummyID" + str(last_dummy_number)
    return dummy_id

"""
This function creates the Rocket server object using bottle deployable app object
parameters:
interfaces = (<server address>,<port>)
method = 'wsgi' as bottls is the wsgi based webserver micro-framework for python
app_info = {'wsgi_app':<bottle deployable object>}

"""
def run_server():
	server = Rocket(
		interfaces = ('0.0.0.0', 9200),
		method = 'wsgi',
		app_info = {'wsgi_app': app})
	server.start()

# main code entry point
if __name__ == "__main__" :
	#run(host = "0.0.0.0", port = 8080)
	run_server()
