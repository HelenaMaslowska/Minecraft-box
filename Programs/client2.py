import paho.mqtt.client as mqtt 
import time
def on_connect(client, userdata, flags, rc):
	if rc == 0:
		print("Connected success")
	else:
		print(f"Connected fail with code {rc}")
		return
	client.subscribe("#")
	for i in range(5):
		# the four parameters are topic, sending content, QoS and whether retaining the message respectively
		client.publish('raspberry/topic', payload=i, qos=0, retain=False)
		print(f"send {i} to raspberry/topic")
		time.sleep(1)

def on_message(client, userdata, msg):
	print(msg.topic, msg.payload)

client = mqtt.Client() 
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883, 60)
 
client.loop_forever()

