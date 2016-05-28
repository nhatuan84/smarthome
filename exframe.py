from Tkinter import Tk, Text, BOTH, W, N, E, S
from ttk import Frame, Button, Label, Style
import ttk
from frameobs import *
import os
import glob
import Tkinter as tkinter
import Tkinter as tk	
from sqlite import *
from element import *

class ExFrame(Frame):
	tree = None
	obs = None
	filter = None
	topics = []
	done = False
	donelist = []
	
	def __init__(self, parent, filter):
		Frame.__init__(self, parent)          
		self.parent = parent
		self.obs = FrameObs(self.callback)
		self.filter = filter
		
		self.initUI()
		
	def callback(self, *args, **kwargs):
		if(self.done == True and self.filter != None and str(args[0][0]).startswith(self.filter) or '*' in self.filter):
			if(self.tree.item(str(args[0][0]))):
				self.tree.set(self.tree.item(str(args[0][0]))['tags'][0], 1, str(args[0][1]))
		else:
			print(self.filter + ' not match \n')
	
	def getObs(self):
		return self.obs
		
	def shownode(self, event):
		tree = event.widget
		item = tree.focus()
		item_id = self.tree.item(item)['tags'][0]
		
	def addNode(self, topic):
		tag = ''
		es = topic.floor.split('/')
		tag = es[0]
		if(es[0] not in self.donelist):	
			id = self.tree.insert("", "end", tag, text=es[0], tags = (tag,))
			self.donelist.append(tag)
		parent = es[0]
		for e in es[1:]:				
				tag = tag + '/' + e
				if(tag not in self.donelist):
					id = self.tree.insert(parent, "end", tag, text=e, tags = (tag,))
					self.donelist.append(tag)
				parent = tag

	def refresh(self):		
		self.done = False
		ins = SmatHomeDb()
		cursor = ins.selectKey()			
		for row in cursor:
			el = Element(row[1], row[2], row[3])
			self.topics.append(el)
		ins.close()
		#self.tree.delete(*self.tree.get_children())

		for topic in self.topics:
			self.addNode(topic)
		self.done = True
		
	def initUI(self):
		self.done = False
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
		
		cbtn = Button(self, text="Close")
		cbtn.grid(row=5, column=2)    

		self.done = True
