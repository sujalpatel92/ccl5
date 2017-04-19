from __future__ import print_function
import bottle, json, time, sys, os, datetime
from bottle import get,post,request,response,route,run,Bottle
from rocket import Rocket
import logging

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

app = Bottle(__name__)
app.debug = True

gps = "0,0"
rpm = "0"

@app.post('/setgps')
def setGPS():
	global gps
	payload = json.dumps(request.json)
	tmp = json.loads(payload, object_hook = JsonDecode.get_dict)
	print(tmp)
	gps = tmp["gps"]
	return bottle.HTTPResponse(status = 200)

@app.get('/getgps')
def getGPS():
	global gps,rpm
	return {"gps" : gps, "rpm" : rpm}

@app.post('/setrpm')
def setRPM():
	global rpm
	payload = json.dumps(request.json)
        tmp = json.loads(payload, object_hook = JsonDecode.get_dict)
        print(tmp)
        rpm = tmp["rpm"]
        return bottle.HTTPResponse(status = 200)


def run_server():
        server = Rocket(
                interfaces = ('0.0.0.0', 8500),
                method = 'wsgi',
                app_info = {'wsgi_app': app})
        server.start()

run_server()
