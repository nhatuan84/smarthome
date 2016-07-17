from Tkinter import *
from ttk import *
import ttk
import time
import Tkinter as tkinter
import Tkinter as tk
from sqlite import *
from util import *
import tkMessageBox
from sqlite import *
from element import *
from util import *

class ExFrame2(Frame):
	parent = None
	alias = None
	floor = None
	device = None
	tree = None
	donelist = []
	topics = []
	floorcontent = None
	devicecontent = None
	aliascontent = None
	menu = None
	map = {}
	unode = None
	def __init__(self, parent):
		Frame.__init__(self, parent.root)
		self.parent = parent
		self.floorcontent = tk.StringVar()	
		self.devicecontent = tk.StringVar()
		self.aliascontent = tk.StringVar()		
		initMapping1(self.map)		
		self.initUI()

	def checkInput(self):
		if(checkInput(self.floor.get(), self.device.get(), self.alias.get()) == True):
			saveInput(self.floor.get(), self.device.get(), self.alias.get())
			self.unode = None
			self.refresh()
			self.parent.getObservable().update_observers('update', 'done')
			tkMessageBox.showinfo("notification", "done")		
		else:
			tkMessageBox.showinfo("notification", "add failed")
	def checkUpdate(self):
		if(checkInput(self.floor.get(), self.device.get(), self.alias.get()) == True):
			if(self.unode != None):
				updateInput(self.unode.id, self.floor.get(), self.device.get(), self.alias.get())
				self.unode = None
				self.refresh()
				self.parent.getObservable().update_observers('update', 'done')
				tkMessageBox.showinfo("notification", "update done")
		else:
			tkMessageBox.showinfo("notification", "update failed")
			
	def shownode(self, event):
		tree = event.widget
		item = tree.focus()
		item_tag = self.tree.item(item)['tags'][0]
		self.floorcontent.set(item_tag)
		self.devicecontent.set(self.map[item_tag].device)
		
	def refresh(self):	
		self.done = False
		if(self.tree.get_children()):
			self.donelist = []
			self.topics = []
			self.map.clear()
			initMapping1(self.map)
			self.tree.delete(*self.tree.get_children())
			
		ins = SmatHomeDb()
		cursor = ins.selectKey()			
		for row in cursor:
			el = Element(row[0], row[1], row[2], row[3])
			self.topics.append(el)
		ins.close()	
		
		for topic in self.topics:
			time.sleep(0.01)
			addNode(self.tree, self.donelist, topic.floor, topic.alias)
		self.done = True	
	
	def menudeletecallback(self):		
		if(self.tree.focus()):
			item = self.tree.focus()
			item_id = self.tree.item(item)['tags'][0]
			ins = SmatHomeDb()
			ins.delete(item_id)
			ins.close()
			self.parent.getObservable().update_observers('delete', 'done')
			self.refresh()
		
	def menuupdatecallback(self):
		item = self.tree.focus()
		item_tag = self.tree.item(item)['tags'][0]
		self.floorcontent.set(item_tag)
		self.devicecontent.set(self.map[item_tag].device)
		self.aliascontent.set(self.map[item_tag].alias)
		self.unode = self.map[item_tag]
	
	def popup(self, event):
		self.menu.post(event.x_root, event.y_root)
		
	def initUI(self):
		self.pack(fill=BOTH, expand=True)

		self.columnconfigure(1, weight=1)
		self.columnconfigure(3, pad=7)
		self.rowconfigure(3, weight=1)
		self.rowconfigure(9, pad=7)

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
		
		lbl0 = Label(self, text="manage node")
		lbl0.grid(row=5, column=2)
		
		f3 = Frame(self)
		f3.grid(row=6, column=2)
		
		lbl1 = Label(f3, text="floor", width=6)
		lbl1.pack(side = LEFT)           

		self.floor = Entry(f3, width=88, textvariable=self.floorcontent)
		self.floor.pack(side = RIGHT)
		
		f2 = Frame(self)
		f2.grid(row=7, column=2) 
		
		lbl2 = Label(f2, text="device", width=6)
		lbl2.pack(side = LEFT)           

		self.device = Entry(f2, width=88, textvariable=self.devicecontent)
		self.device.pack(side = RIGHT)
		
		f1 = Frame(self)
		f1.grid(row=8, column=2) 
		
		lbl3 = Label(f1, text="name", width=6)
		lbl3.pack(side = LEFT)          

		self.alias = Entry(f1, width=88, textvariable=self.aliascontent)
		self.alias.pack(side = RIGHT) 
		
		bottomframe = Frame(self)
		bottomframe.grid(row=9, column=2) 

		save = Button(bottomframe, text="Add", command=self.checkInput)
		save.pack(side = LEFT)  
		
		update = Button(bottomframe, text="Update", command=self.checkUpdate)
		update.pack(side = RIGHT) 

		self.menu = Menu(self.tree, tearoff=0)
		self.menu.add_command(label="Delete", command=self.menudeletecallback)
		self.menu.add_command(label="Update", command=self.menuupdatecallback)
		
		self.tree.bind("<Button-3>", self.popup)