from __future__ import print_function
import logger
import bottle, json, time, sys, os, datetime, random
from bottle import get,post,request,response,route,run,Bottle
from rocket import Rocket

# global variables
# to print debug statements
print_debug = True
# store generated id's based on request from pi
id_given_to_pi = list()
# store id's waiting to be registered from web
confirm_id_from_web = list()
# store the registered_pi's
registered_pi = list()
# maintain time of last access by pi
pi_last_connected = dict()
# maintain the state of LED of connected pi's. By default it is "off"
pi_LED_state = dict()
# logger for iotplatform
platform_log = logger.get_custom_logger(__name__, "iotplatform.log")
# dict to store logger handles for devices
device_log = dict()
# end global variables
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

# bottle app initialization
app = Bottle(__name__)
app.debug = True

# start bottle app REST API definitions
"""
Endpoint to get device id for pi
"""
@app.get('/registerpi/get_pi_id')
def get_pi_id():
    global platform_log
    if print_debug:
        print("Request for ID received")
    pi_id = generateID()
    id_given_to_pi.append(pi_id)
    platform_log.info('Generated PI ID: %s', pi_id)
    if print_debug:
        print("Generated ID: ",pi_id)
        print("id_given_to_pi ->", id_given_to_pi)
    return {'pi_id' : pi_id}

"""
Endpoint to register device to platform from pi
"""
@app.post('/registerpi/registerdevice')
def register_pi_from_device():
    # need to complete implementation. Currently partial implementation
    global platform_log, device_log, registered_pi
    payload = json.loads(json.dumps(request.json), object_hook = JsonDecode.get_dict)
    if print_debug:
        print("ID received: ",payload["DeviceId"])
    pi_id = payload["DeviceId"]
    if print_debug:
        print("Request to register device ID: ",pi_id)
    if pi_id in registered_pi:
        if print_debug:
            print("PI already registered")
        return bottle.HTTPResponse(status = 200)
    else:
        if pi_id not in id_given_to_pi:
            if print_debug:
                print("Incorrect ID from PI")
            return bottle.HTTPResponse(status = 404)
        #setup pi last connected here
        if pi_id in id_given_to_pi:
            id_given_to_pi.remove(pi_id)
            confirm_id_from_web.append(pi_id)
        platform_log.info("Register request received from pi for ID: %s", pi_id)
        if print_debug:
            print("Register request received from pi for ID: ",pi_id)
        return bottle.HTTPResponse(status = 200)
"""
Endpoint to register device to platform from web ui
"""
@app.get('/registerpi/get_pi_confirmation')
def get_pi_confirmation():
    # partial implementation. Need to implement this completely
    global platform_log, device_log, confirm_id_from_web, registered_pi, pi_LED_state
    if print_debug:
        print(request.params["pi_id"])
        print(confirm_id_from_web)
    pi_id = str(request.params["pi_id"]).split('|')[0]
    if pi_id in confirm_id_from_web:
        confirm_id_from_web.remove(pi_id)
        registered_pi.append(pi_id)
        pi_LED_state[pi_id] = "off"
        platform_log.info("Device Successfully registered with ID: %s", pi_id)
        device_log[pi_id] = logger.get_custom_logger(pi_id)
        device_log[pi_id].info('PI successfully registered.')
        if print_debug:
            print("PI successfully registered")
        return bottle.HTTPResponse(status = 200)
    elif pi_id in registered_pi:
        if print_debug:
            print("PI already registered")
        platform_log.error("WEB UI PI ID already registered before.")
        return bottle.HTTPResponse(status = 403)
    else:
        platform_log.error('Wrong PI ID requested to register from front end. Incorrect pi ID: %s', pi_id)
        if print_debug:
            print('Wrong PI ID requested to register from front end')
        return bottle.HTTPResponse(status = 404)
"""
Endpoint to deregister pi from web ui
"""
@app.get('/deregisterpi')
def deregister_pi():
    global platform_log, device_log, registered_pi, pi_LED_state
    if print_debug:
        print(request.params["pi_id"])
    pi_id = str(request.params["pi_id"]).split('|')[0]
    if pi_id in registered_pi:
        registered_pi.remove(pi_id)
    else:
        bottle.HTTPResponse(status = 500)
    if pi_id in pi_LED_state:
        del pi_LED_state[pi_id]
    else:
        bottle.HTTPResponse(status = 500)
    platform_log.info("PI with ID: %s Successfully deregistered.", pi_id)
    if pi_id in device_log:
        device_log[pi_id].info("PI deregistered.")
        del device_log[pi_id]
    if print_debug:
        print("PI deregistered")
    return bottle.HTTPResponse(status = 200)

"""
Endpoint to get light state from pi
"""
@app.get('/light/status')
def get_LED_status():
    global pi_LED_state, platform_log, device_log
    pi_id = request.params["DeviceId"]
    if pi_id in pi_LED_state:
        led_state = pi_LED_state[pi_id]
        platform_log.info("Sending Light State %s to PI ID: %s", led_state, pi_id)
        device_log[pi_id].info("Sending Light Status %s to device", led_state)
        return {'light' : led_state}
    else:
        return bottle.HTTPResponse(status = 404)

"""
Endpoint to set light state from pi
"""
@app.post('/light/status')
def set_LED_status():
    global pi_LED_state, platform_log, device_log
    payload = json.loads(json.dumps(request.json), object_hook = JsonDecode.get_dict)
    if print_debug:
        print(payload)
        print(payload['light'])
        print(payload['pi_id'])
    led_state = payload['light']
    pi_id = payload['pi_id']
    pi_LED_state[pi_id] = led_state
    platform_log.info("Received Light State %s for PI ID: %s from WEB UI", led_state, pi_id)
    device_log[pi_id].info('Received Light State %s from front end', led_state)
    return bottle.HTTPResponse(status = 200)

"""
Endpoint to get logs from pi.
"""
@app.get('/getlogs')
def get_log_ip():
    global logger, device_log
    if print_debug:
        print(request.params["pi_id"])
    pi_id = str(request.params["pi_id"]).split('|')[0]
    url = "http://35.162.32.72/" + str(pi_id) + '.log'
    platform_log.info("Got request for logs of device ID: %s", pi_id)
    return bottle.HTTPResponse(url)

"""
Endpoint for getting IoT platform logs
"""
@app.get('/getlogsiot')
def get_logs_iot_ip():
    global logger
    if print_debug:
        print(request.params["email"])
    platform_log.info("Got request for logs of IoT Platform")
    url = "http://35.162.32.72/iotplatform.log"
    return bottle.HTTPResponse(url)
# end bottle app REST API definitions
# start regular functions
"""
This function generates ID for pi
"""
def generateID():
    generated_id = ''.join(random.choice('0123456789ABCDEF') for i in range(16))
    print(generated_id)
    while not ((generated_id not in id_given_to_pi) and (generated_id not in confirm_id_from_web) and (generated_id not in registered_pi)):
        generated_id = ''.join(random.choice('0123456789ABCDEF') for i in range(16))
        print(generated_id)
    return generated_id

"""
This function deploys bottle app on Rocket server
"""
def run_server():
    global platform_log
    if print_debug:
        print("Starting iotplatform")
    server = Rocket(
        interfaces = ('0.0.0.0', 8005),
        method = 'wsgi',
        app_info = {'wsgi_app': app})
    server.start()
    platform_log.info("Started Server")
# end regular functions

# code entry point
if __name__ == "__main__" :
    run_server()
