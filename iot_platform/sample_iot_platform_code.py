from __future__ import print_function
import bottle
from bottle import get,post,request,response,route,run
import json

lState = "off"
 
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


@route('/myip')
def showip():
	ip = request['REMOTE_ADDR']
	print(ip)
	return bottle.HTTPResponse(status=200)

@get('/light/status')
def tellLightState():
	global lState
	theBody = json.dumps({'light': lState})
	return {'light':lState}

@post('/light/status')
def setLightState():
	global lState
	payload = json.dumps(request.json)
	print(payload)
	tmp = json.loads(payload, object_hook = JsonDecode.get_dict)
	print(tmp['light'])
	lState = tmp['light']
	return bottle.HTTPResponse(status=200)

@post('/sample')
def seepost():
	print(request.body)

run(host = "0.0.0.0", port = 8080)
