import sys
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

class MQTTC:
	
	def __init__(self, server, topic, clientid=None):
		self.server = server
		self.topic = topic
		self.mqttc = mqtt.Client(clientid)
		
	def setCallbacks(self, mqtt_on_connect, mqtt_on_message, mqtt_on_publish, mqtt_on_subscribe, mqtt_on_log):
		self.mqttc.on_message = mqtt_on_message
		self.mqttc.on_connect = mqtt_on_connect
		self.mqttc.on_publish = mqtt_on_publish
		self.mqttc.on_subscribe = mqtt_on_subscribe
		self.mqttc.on_log = mqtt_on_log
	def publish(self, topic, value):
		publish.single(topic, value, hostname=self.server)
	def run(self):
		self.mqttc.connect(self.server, 1883, 60)
		self.mqttc.subscribe(self.topic, 0)
		rc = 0
		while rc == 0:
			rc = self.mqttc.loop()
		return rc

