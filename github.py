import requests
import json

API_URL = 'https://api.github.com'
SETTINGS = "settings.williames" #settings file


def getToken():


def getValue(key):
	with open(SETTINGS) as f:
		for line in f:
			if key in line:
				return line.split(" ")[1]

	return ""
		
def addProperty(key, value):
	with open(SETTINGS, "a") as sett:
		sett.write(key, " ", value "\n")
		return True

	return False #something bad happenesd

