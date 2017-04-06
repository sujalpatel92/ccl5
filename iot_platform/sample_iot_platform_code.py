from __future__ import print_function
import bottle
from bottle import get,post,request,response,route,run
import json

# debug variable for light state
lState = "off"
# dict to store Light state of all pi's
deviceLEDState = dict()
# list of registered devices
registeredDevices = list()

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

# function to return ip address of the requester
@route('/myip')
def showip():
	ip = request['REMOTE_ADDR']
	print(ip)
	return {'ip':ip}

"""
This function is used to get the light status for a raspberry pi
input: request object with params = {'DeviceId':<id>} form
return: stored state of the LED on that pi
"""
@get('/light/status')
def tellLightState():
	global deviceLEDState
	deviceid = request.params["DeviceId"]
	if deviceid in deviceLEDState:
		return {'light':deviceLEDState[deviceid]}
	else:
		return bottle.HTTPResponse(status=404)

"""
This function is used to update the LED status of pi from the user end
input request object with body = {'DeviceId':<id>, 'Light':<state>}
return HTTP 200 on sucessful status change else HTTP 500
"""
@post('/light/status')
def setLightState():
	# need to complete implementation. currently partial implementation.
	global lState
	payload = json.dumps(request.json)
	print(payload)
	tmp = json.loads(payload, object_hook = JsonDecode.get_dict)
	print(tmp['light'])
	lState = tmp['light']
	deviceLEDState["CLOUD001"] = lState
	return bottle.HTTPResponse(status=200)

"""
This function is used to register the pi.
This end-point will be called from pi and pi will be registered in device registry
input: request object with body = {'DeviceID':<id>}
return: HTTP 200 on successful or HTTP 500
"""
@post('/registerdevice/pi')
def registerpi():
	# need to complete implementation. Currently partial implementation
	global registeredDevices
	payload = json.loads(json.dumps(request.json), object_hook = JsonDecode.get_dict)
	print(payload["DeviceId"])
	if payload["DeviceId"] in registeredDevices:
		return bottle.HTTPResponse(status=200)
	else:
		registeredDevices.append(payload["DeviceId"])
		deviceLEDState[payload["DeviceId"]] = "off"
		return bottle.HTTPResponse(status=200)

# need to add if __name__ check here.
run(host = "0.0.0.0", port = 8080)
