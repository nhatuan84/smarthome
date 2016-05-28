from Tkinter import Tk, Text, TOP, BOTH, X, N, LEFT
from ttk import Frame, Label, Entry, Button
from sqlite import *
from util import *
import tkMessageBox

class ExFrame2(Frame):
	alias = None
	floor = None
	device = None
	def __init__(self, parent):
		Frame.__init__(self, parent)   		 
		self.parent = parent
		self.initUI()

	def checkInput(self):
		if(checkInput(self.floor.get(), self.device.get(), self.alias.get()) == True):
			saveInput(self.floor.get(), self.device.get(), self.alias.get())
			tkMessageBox.showinfo("notification", "Done")
		else:
			tkMessageBox.showinfo("notification", "Failed")
	def initUI(self):

		frame1 = Frame(self)
		frame1.pack(fill=X)

		lbl1 = Label(frame1, text="floor", width=6)
		lbl1.pack(side=LEFT, padx=5, pady=5)           

		self.floor = Entry(frame1)
		self.floor.pack(fill=X, padx=5, expand=True)

		frame2 = Frame(self)
		frame2.pack(fill=X)

		lbl2 = Label(frame2, text="device", width=6)
		lbl2.pack(side=LEFT, padx=5, pady=5)        

		self.device = Entry(frame2)
		self.device.pack(fill=X, padx=5, expand=True)

		frame3 = Frame(self)
		frame3.pack(fill=X)

		lbl3 = Label(frame3, text="alias", width=6)
		lbl3.pack(side=LEFT, padx=5, pady=5)        

		self.alias = Entry(frame3)
		self.alias.pack(fill=X, padx=5, expand=True)  

		frame4 = Frame(self)
		frame4.pack(fill=X)

		save = Button(frame4, text="Save", width=6, command=self.checkInput)
		save.pack(side=LEFT, padx=5, pady=5) 

		cancel = Button(frame4, text="Cancel", width=6)
		cancel.pack(side=LEFT, padx=5, pady=5) 
