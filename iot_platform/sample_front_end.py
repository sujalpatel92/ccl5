from flask import Flask,redirect
from flask import render_template
from flask import request
import os, json
import time
import paho.mqtt.client as mqtt
import ssl
import requests

light_state = "none"

def on_connect(mqttc, obj, flags, rc):
    global light_state
    print rc
    if rc==0:
        payload = "{\"state\":{\"desired\":{\"light\":\""+light_state+"\"}}}"
        print payload
        mqttc.subscribe("$aws/things/Raspberry_pi_3/shadow/update/delta", qos=0)
        mqttc.publish("$aws/things/Raspberry_pi_3/shadow/update", payload, 0 ,True)

def send_update():
    global light_state
    print "sending update"
    mqtt_client = mqtt.Client(client_id="Raspberry_pi_3", clean_session = True)
    mqtt_client.on_connect = on_connect
    mqtt_client.tls_set("./VeriSign-Class 3-Public-Primary-Certification-Authority-G5.pem", certfile = "./0dd82902e6-certificate.pem.crt", keyfile="./0dd82902e6-private.pem.key", tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)

    mqtt_client.connect("aokbbvlik7wrd.iot.us-west-2.amazonaws.com", port=8883)
    payload = "{\"state\":{\"desired\":{\"light\":\""+light_state+"\"}}}"
    mqtt_client.publish("$aws/things/Raspberry_pi_3/shadow/update", payload, 0 ,True)

app = Flask(__name__)

port = 8883

@app.route('/')
def hello():
	return render_template('index.html')

@app.route('/light/<command>', methods=['GET', 'POST'])
def light_route(command):
    global light_state
    print command
    #myData = {'command' : command}
    #client.publishEvent("raspberrypi", deviceId, "light", "json", myData)
    light_state = command
    #send_update()
    header = {'Content-Type':'application/json', 'Accept':'application/json'}
    body = {'light':light_state}
    requests.post('http://ec2-35-162-32-72.us-west-2.compute.amazonaws.com:8000/light/status', headers = header, data = json.dumps(body), verify = False)
    return redirect("/", code=302)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
