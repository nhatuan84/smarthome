from Tkinter import *
from ttk import *
import ttk
import Tkinter as tkinter
import Tkinter as tk
from frameobs import *
import os
import sys
import time
from sqlite import *
from element import *
from util import *
from dialog import *
from mqttc import *
from controller import *

class ExFrame3(Frame):
	parent = None
	tree = None
	filter = None
	topics = []
	done = False
	donelist = []
	menu = None
	obs = None
	
	def __init__(self, parent):
		Frame.__init__(self, parent.root)  
		self.parent = parent
		self.done = False        
		self.initUI()
		self.obs = FrameObs(self.obscallback)
		self.done = True
		self.setFilter()
		
	def getObs(self):
		return self.obs
	def obscallback(self, *args, **kwargs):	
		if(args[0][0]  == 'mqttserver'):
			self.server = str(args[0][1])
			modelmqttc = MQTTC(self.server, "$SYS/#")
			controller = Controller(modelmqttc, self)
			
	def updateTree(self, topic, val):
		#should sleep :)
		time.sleep(0.44)
		try:
			if(self.done == True and topic.startswith(self.filter)):
				try:
					self.tree.set(str(topic), 1, str(val))				
				except Exception as e:
					print '3 - ' + str(e)
					addNode(self.tree, self.donelist, str(topic))
					self.tree.set(topic, 1, str(val))
					sys.exc_clear()
		except Exception as e:
			print '4 - ' + str(e)
			sys.exc_clear()
			
	def setFilter(self, filter = ''):
		self.filter = filter
		
	def shownode(self, event):
		tree = event.widget
		item = tree.focus()
		item_id = self.tree.item(item)['tags'][0]

	def menupublishcallback(self):
		if(self.tree.focus()):
			item = self.tree.focus()
			item_id = self.tree.item(item)['tags'][0]
			d = Dialog(self.tree, item_id)
			self.tree.wait_window(d.top)
		
	def menugraphcallback(self):
		pass
		
	def refresh(self):
		pass
	
	def popup(self, event):
		self.menu.post(event.x_root, event.y_root)
	
	def initUI(self):		
		self.pack(fill=BOTH, expand=True)

		self.columnconfigure(1, weight=1)
		self.columnconfigure(3, pad=7)
		self.rowconfigure(3, weight=1)
		self.rowconfigure(5, pad=7)

		self.tree = ttk.Treeview(self)	
		self.tree["columns"]=("1","2")
		self.tree.column("1", width=50 )
		self.tree.column("2", width=50)	
		self.tree.heading("1", text="value")
		self.tree.heading("2", text="name")
		
		ysb = ttk.Scrollbar(self, orient=tk.VERTICAL, command= self.tree.yview)
		xsb = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command= self.tree.xview)
		self.tree['yscroll'] = ysb.set
		self.tree['xscroll'] = xsb.set		
		
		self.tree.grid(row=1, column=0, columnspan=4, rowspan=3, sticky=E+W+S+N)
		ysb.grid(row=1, column=5, rowspan=3, sticky=S+N)
		xsb.grid(row=4, column=0, columnspan=4, sticky=E+W)
		self.tree.bind('<Double-Button-1>', self.shownode)  
		
		self.menu = Menu(self.tree, tearoff=0)
		#self.menu.add_command(label="Publish", command=self.menupublishcallback)
		#self.menu.add_command(label="Graph", command=self.menugraphcallback)
		
		self.tree.bind("<Button-3>", self.popup)
		
