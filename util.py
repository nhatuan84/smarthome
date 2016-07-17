from sqlite import *
from element import *
from Tkinter import *

color = 'beige'

def checkInput(floor, device, alias):
	if(len(floor) == 0 or len(device) == 0 or len(alias) == 0):
		return False
	else:
		#ins = SmatHomeDb()
		#cursor = ins.selectKey('floor')	
		#pos = floor.find('/')
		#tmp = floor[0:pos]
		#for row in cursor:
		#	if(row[0] == tmp):
		#		ins.close()
		#		return True
		#ins.close()
		return True
	return False
def saveInput(floor, device, alias):
	try:
		ins = SmatHomeDb()
		ins.insert(floor, alias, device)
	finally:
		ins.close()
def updateInput(id, floor, device, alias):
	try:
		ins = SmatHomeDb()
		ins.update(id, floor, alias, device)
	finally:
		ins.close()	
def addNode(tree, donelist, topic, alias = ''):
	global color
	tag = ''
	es = topic.split('/')
	tag = es[0]
	id = None
	if(es[0] not in donelist):	
		id = tree.insert("", "end", tag, text=es[0], tags = (tag,))
		tree.tag_configure(id, background='darkorange')
		donelist.append(tag)
	parent = es[0]
	i = 0	
	for e in es[1:]:				
			tag = tag + '/' + e
			if(tag not in donelist):
				if(color == 'beige'):
					color = 'whitesmoke'
				else:
					color = 'beige'
				id = tree.insert(parent, "end", tag, text=e, tags = (tag,))
				tree.tag_configure(id, background=color)
				donelist.append(tag)
			parent = tag
	tree.set(tree.item(tag)['tags'][0], 2, alias)
	
def initMapping(map):
	try:
		ins = SmatHomeDb()
		cursor = ins.selectKey()
		for row in cursor:
			map[row[3]] = row[1]
	finally:
		ins.close()
	return map
	
def initMapping1(map):
	try:
		ins = SmatHomeDb()
		cursor = ins.selectKey()
		for row in cursor:
			el = Element(row[0], row[1], row[2], row[3])
			map[row[1]] = el
	finally:
		ins.close()
	return map
	
def getMap(map, fulltopic):
	if(map.has_key(fulltopic)):
		return map[fulltopic]
	else:
		pos = fulltopic.rfind('/')
		if(pos == -1):
			return fulltopic
		else:
			tmp = fulltopic[0:pos]
			tmp = getMap(map, tmp)
			tmp = tmp + fulltopic[pos:len(fulltopic)]
			return tmp;
			
			
			
			
			