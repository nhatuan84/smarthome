import Tkinter
from Tkinter import *
from ttk import *
import sqlite3
from sqlite import *
from exframe import *
from exframe2 import *
from exframe3 import *
from dialog import *
import thread
import sys

class DashBoard:
	root = None
	monitor = None
	setting = None
	system = None
	observable = None
	
	def __init__(self):
		self.root 	   = Tk()   
		self.root.title('MQTT monitor')
		self.observable = Observable()
		menubar = Menu(self.root)
		filemenu = Menu(menubar, tearoff=0)
		filemenu.add_command(label="connect to", command=self.connect)
		filemenu.add_command(label="about", command=self.about)
		filemenu.add_separator()
		filemenu.add_command(label="Exit", command=self.root.quit)
		menubar.add_cascade(label="Menu", menu=filemenu)

		s = ttk.Style()
		s.configure('TNotebook', tabposition='n')
		notebook = Notebook(self.root, width = 600, height = 600)
		
		self.monitor = ExFrame(self)
		self.observable.register(self.monitor.getObs())
		notebook.add(self.monitor, text="Monitor")
		
		self.setting = ExFrame2(self)
		notebook.add(self.setting, text="Manage")
		
		self.system = ExFrame3(self)
		self.observable.register(self.system.getObs())
		notebook.add(self.system, text="System")

		notebook.bind_all("<<NotebookTabChanged>>", self.tabChangedEvent)
		notebook.pack(fill = Tkinter.BOTH)
		
		self.root.config(menu=menubar)
		self.root.mainloop() 
	def getObservable(self):
		return self.observable
	def connect(self):
		d = Dialog(self.root, 'server ip')
		self.root.wait_window(d.top)	
		if(d.getVal() != None):
			self.getObservable().update_observers('mqttserver', d.getVal().strip())
	def about(self):
		tkMessageBox.showinfo("about", "nha.tuan84@gmail.com")
	def tabChangedEvent(self,event):
		tabtext = event.widget.tab(event.widget.index("current"),"text");
		if(tabtext == "Monitor"):
			self.monitor.refresh()
		elif(tabtext == "Manage"):
			self.setting.refresh()
		elif(tabtext == "System"):
			pass#self.system.refresh()
		
    
def main():	
	window = DashBoard()
  
main()
