import os

SETTINGS = 'settings.williames' #settings file

def getValue(key):
	if os.path.exists(SETTINGS):
		with open(SETTINGS) as f:
			for line in f:
				if key in line:
					return line.split(" ", 1)[1].strip(" \n")
	return None

def addProperty(key, value):
	with open(SETTINGS, "a+") as sett: # Will create the file if it does not exist
		sett.write(key + " " + value + "\n")
		return True

	return False
