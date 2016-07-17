from Tkinter import *

#Note: if want to get return value by ref, use list as a param

class Dialog:
	topic = None
	ret = None
	def __init__(self, parent, topic):
		top = self.top = Toplevel(parent)
		top.title('input value')
		self.topic = topic
		Label(top, text=self.topic).pack()
		self.e = Entry(top, width=40)
		self.e.pack(padx=5)

		ok = Button(top, text="OK", command=self.ok)
		ok.pack(padx=5, pady=5, side = LEFT)

		cancel = Button(top, text="Cancel", command=self.cancel)
		cancel.pack(padx=5, pady=5, side = LEFT)

	def ok(self):
		self.ret = self.e.get()
		self.top.destroy()
		
	def getVal(self):
		return self.ret

	def cancel(self):
		self.top.destroy()