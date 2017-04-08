from __future__ import print_function
import bottle, json, time, sys, os, datetime
from bottle import get,post,request,response,route,run,Bottle
from rocket import Rocket

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


"""
This class is used to decode josn file.
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
	global deviceLEDState
	deviceid = request.params["DeviceId"]
	if deviceid in deviceLEDState:
		if deviceid in pi_last_connected:
			now = datetime.datetime.now()
			pi_last_connected[deviceid] = str(now)

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
	global lState
	payload = json.dumps(request.json)
	print(payload)
	tmp = json.loads(payload, object_hook = JsonDecode.get_dict)
	print(tmp['light'])
	lState = tmp['light']
	deviceLEDState["DummyID1"] = lState
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
	global registeredDevices, await_pi_confirm
	payload = json.loads(json.dumps(request.json), object_hook = JsonDecode.get_dict)
	print(payload["DeviceId"])
	pi_id = payload["DeviceId"]
	if pi_id in registeredDevices:
		return bottle.HTTPResponse(status=200)
	else:
		if pi_id not in id_given_to_pi:
			return bottle.HTTPResponse(status=404)
		registeredDevices.append(pi_id)
		deviceLEDState[pi_id] = "off"
		now = datetime.datetime.now()
		pi_last_connected[pi_id] = str(now)
		if pi_id in await_pi_confirm:
			await_pi_confirm.remove(pi_id)
		if pi_id in id_given_to_pi:
			id_given_to_pi.remove(pi_id)
			send_confirm_pi.append(pi_id)
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
    dummy_id = generateID()
    id_given_to_pi.append(dummy_id)
    return {'pi_id':dummy_id}

"""
Another dummy function for sake of frontend development
"""
@app.get('/registerpi/get_pi_confirmation')
def get_pi_confirmation():
    # partial implementation. Need to implement this completely
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
        return bottle.HTTPResponse(status=200)
    elif pi_id in registeredDevices:
	return bottle.HTTPResponse(status=403)
    else:
    	return bottle.HTTPResponse(status=404)	

"""
This function is to de-register the pi
"""
@app.route('/deregisterpi')
def deRegisterPi():
	global registeredDevices, deviceLEDState
	pi_id = str(request.params["pi_id"]).split('|')[0]
	if pi_id in registeredDevices:
		registeredDevices.remove(pi_id)
	else:
		return bottle.HTTPResponse(status=500)
	if pi_id in deviceLEDState:
		del deviceLEDState[pi_id]
	else:
		return bottle.HTTPResponse(status=500)
	return bottle.HTTPResponse(status=200)

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
		interfaces = ('0.0.0.0', 8000),
		method = 'wsgi',
		app_info = {'wsgi_app': app})
	server.start()

# main code entry point
if __name__ == "__main__" :
	#run(host = "0.0.0.0", port = 8080)
	run_server()
