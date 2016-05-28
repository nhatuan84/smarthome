from observable import Observable
from observer import Observer
 
 
class FrameObs(Observer):
	callback = None
	def __init__(self, callback):
		self.callback = callback
	def update(self, *args, **kwargs):
		self.callback(args, kwargs)
        