import thread

class Controller():
	def __init__(self, model, view):
		self.model = model
		self.view = view
		self.model.setCallbacks(self.mqtt_on_connect, self.mqtt_on_message, self.mqtt_on_publish, self.mqtt_on_subscribe, self.mqtt_on_log)
		
		try:
			thread.start_new_thread( self.worker, (self.model.topic, 1, ) )
		except:
			print "Error: unable to start thread"
		
	def worker(self, threadName, delay):
		self.model.run()
		
	def mqtt_on_connect(self, mqttc, obj, flags, rc):
		#print("rc: "+str(rc))
		pass

	def mqtt_on_message(self, mqttc, obj, msg):
		self.view.updateTree(msg.topic, str(msg.payload))

	def mqtt_on_publish(self, mqttc, obj, mid):
		#print("mid: "+str(mid))
		pass

	def mqtt_on_subscribe(self, mqttc, obj, mid, granted_qos):
		#print("Subscribed: "+str(mid)+" "+str(granted_qos))
		pass

	def mqtt_on_log(self, mqttc, obj, level, string):
		pass#print(string)
		
	def publish(self, topic, value):
		self.model.publish(topic, value)
		