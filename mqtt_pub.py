import paho.mqtt.client as mqttclient
import time
import random
import json


def on_connect(client,userdata,flags,rc) :
    if rc==0:
        print("client is connected")
        global connected
        connected = True
    else:
        print("connection failed")

connected=False
broker_address="front.dii.unitn.it"
port=10883
user="keizer"
password="tryingtoiot"
topic="/cabinet/"

f = open('jsontest.json')
  
data = json.load(f)
data = json.dumps(data)

client = mqttclient.Client("MQTT", True, None, mqttclient.MQTTv31)
client.username_pw_set(user,password=password)
client.on_connect = on_connect
client.connect(broker_address,port=port)
client.loop_start()

while connected!=True:
    time.sleep(0.2)
try:
    while True:
        client.publish(topic,data)

except KeyboardInterrupt:
    print("exiting")
    client.disconnect()
    client.loop_stop()