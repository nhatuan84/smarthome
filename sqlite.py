#!/usr/bin/python

import sqlite3
import os
from threading import Thread, Lock

class SmatHomeDb:
	conn = None
	mutex = None
	
	def __init__(self):
		self.mutex = Lock()
		if(os.path.isfile('smarthome.db') == False):	
			try:
				self.mutex.acquire()
				self.conn = sqlite3.connect('smarthome.db')		
				self.conn.execute('''CREATE TABLE smarthome
					   (id 	       INTEGER  PRIMARY KEY    AUTOINCREMENT,
					   floor           TEXT    NOT NULL,
					   alias           TEXT    NOT NULL,
					   device          TEXT    NOT NULL,
					   CONSTRAINT floor_unique UNIQUE(floor)
					   CONSTRAINT device_unique UNIQUE(device));''')	
			finally:
				self.mutex.release()
		else:
			try:
				self.mutex.acquire()
				self.conn = sqlite3.connect('smarthome.db')
			finally:
				self.mutex.release()
	def insert(self, floor, alias, device):
		try:
			self.mutex.acquire()
			self.conn.execute("INSERT INTO smarthome (floor,alias,device) \
				  VALUES ('" + floor + "','" + alias + "', '" + device + "')");
			self.conn.commit()
		finally:
			self.mutex.release()
	def update(self, idx, floor, alias, device):
		try:
			self.mutex.acquire()
			self.conn.execute("UPDATE smarthome set floor=?, alias=?, device=? where id=?", (floor, alias, device, idx))
			self.conn.commit()
		finally:
			self.mutex.release()
	def selectKey(self, key='*'):
		try:
			self.mutex.acquire()
			cursor = self.conn.execute("SELECT " + key + " from smarthome group by length(floor)")	
			return cursor
		finally:
			self.mutex.release()
		return None
	def delete(self, floor):
		try:
			self.mutex.acquire()
			self.conn.execute("delete from smarthome where floor = '%s' " % floor)
			self.conn.commit()
		finally:
			self.mutex.release()
	def close(self):
		self.conn.close()

