import requests
import json

geturl = "http://35.162.32.72:8005/registerpi/get_pi_id"

rget = requests.get(geturl,verify = False)
data= json.loads(rget.text)
print "Your Device ID is \""+str(data["pi_id"])+"\" Please register it by editing and executing Device_Registration.py"
