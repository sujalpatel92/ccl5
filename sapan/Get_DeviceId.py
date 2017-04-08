import requests
import json

geturl = "http://35.162.32.72:8000/registerpi/get_pi_id/dummy"

rget = requests.get(geturl,verify = False)
data= json.loads(rget.text)
print "Your Device ID is \""+str(data["pi_id"])+"\" Please register it by editing and executing Device_Registration.py"