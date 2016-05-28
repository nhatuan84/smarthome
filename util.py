from sqlite import *

def checkInput(floor, device, alias):
	if(len(floor) == 0 or len(device) == 0 or len(alias) == 0):
		return False
	else:
		ins = SmatHomeDb()
		cursor = ins.selectKey('floor')
		ins.close()
		pos = floor.find('/')
		tmp = floor[0:pos]
		for row in cursor:
			if(row[0] == tmp):
				return True
	return False
def saveInput(floor, device, alias):
	ins = SmatHomeDb()
	ins.insert(floor, alias, device)
	ins.close()
			
			