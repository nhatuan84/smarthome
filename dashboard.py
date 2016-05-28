import Tkinter
from Tkinter import *
from ttk import *
import sqlite3
from sqlite import *
from exframe import *
from exframe2 import *
import time
import thread

class DashBoard:
	root = None
	observable = None
	monitor = None
	setting = None
	
	def __init__(self):
		self.observable = Observable()
		self.root 	   = Tk()   
		menubar = Menu(self.root)
		filemenu = Menu(menubar, tearoff=0)
		filemenu.add_command(label="Settings", command=self.donothing)
		filemenu.add_separator()
		filemenu.add_command(label="Exit", command=self.root.quit)
		menubar.add_cascade(label="Menu", menu=filemenu)

		s = ttk.Style()
		s.configure('TNotebook', tabposition='ne')
		notebook = Notebook(self.root, width = 600, height = 500)
		
		self.monitor = ExFrame(self.root, "*")
		self.observable.register(self.monitor.getObs())
		notebook.add(self.monitor, text="Monitor")
		
		self.setting = ExFrame2(self.root)
		notebook.add(self.setting, text="Settings")

		notebook.bind_all("<<NotebookTabChanged>>", self.tabChangedEvent)
		notebook.pack(fill = Tkinter.BOTH)

		self.label = Label(self.root,text="")
		self.label.pack()
		
		self.root.config(menu=menubar)
		
		try:
			thread.start_new_thread( self.worker, ("Thread-1", 2, ) )
		except:
			print "Error: unable to start thread"

		self.root.mainloop() 
		
	def worker(self, threadName, delay):
		i = 0
		topics = []
		ins = SmatHomeDb()
		cursor = ins.selectKey('floor')			
		for row in cursor:
			topics.append(row[0])
		ins.close()
		#while(True):		
		#	for topic in topics:
		#		i = i + 1
		#		if(i == 1000):
		#			i = 1
		#		self.observable.update_observers(topic, str(i))
		#		time.sleep(delay);
		
	def donothing(self):
		filewin = Toplevel(self.root)
		button = Button(filewin, text="Do nothing button")
		button.pack()
	def tabChangedEvent(self,event):
		status = event.widget.tab(event.widget.index("current"),"text")
		if(status == "Monitor"):
			self.monitor.refresh()
		self.label.configure(text=status)		
    
def main():	
	window = DashBoard()
  
main()
