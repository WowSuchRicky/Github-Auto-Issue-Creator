import requests
import json
import getpass
import os
from urlparse import urljoin


API_URL = 'https://api.github.com'
SETTINGS = "settings.williames" #settings file

HEADERS = {'Content-type':'application/json'}

def getToken():
	val = getValue("auth_token")
	if val is not None:
		return val
	
	#generate a token
	username = raw_input('Github username: ')
	password = getpass.getpass('Github password: ')

	url = urljoin(API_URL, 'authorizations')
	payload = {'note' : 'auto-issue-creator'}
	r = requests.post(url, auth = (username, password), data = json.dumps(payload),)

	# TODO error handling

	if r.ok:
		token = json.loads(r.text or r.content)['token']
		if not addProperty('auth_token', token):
			print "Could not write authorization token to settings file. Please add the following line to " + SETTINGS + ":\n" + "auth_token " + token
		return token

def getValue(key):
	if not os.path.exists(SETTINGS):
		open(SETTINGS, 'a').close()
	with open(SETTINGS) as f:
		for line in f:
			if key in line:
				return line.split(" ", 1)[1].strip(" \n")
	return None
		
def addProperty(key, value):
	with open(SETTINGS, "a+") as sett:
		sett.write(key + " " + value + "\n")
		return True

	return False #something bad happened


def getRepo():
	val = getValue("repo")
	if val is not None:
		return val

	with open('.git/config') as f:
		for line in f:
			if "url = " in line:
				r = line.split("=")[1].split("github.com/")[1].split("/")[1].replace(".git\n", "")
	
	if r:
		addProperty("repo", r)
		return r

def getOwner():
	val = getValue("owner")
	if val is not None:
		return val

	with open('.git/config') as f:
		for line in f:
			if "url = " in line:
				r = line.split("=")[1].split("github.com/")[1].split("/")[0]

	if r:
		addProperty("owner", r)
		return r


def createIssues(issues):
	for issue in issues:
		createIssue(issue)

def createIssue(issue):
	print "CREATING ISSUE: ", issue.issue, " in file: ", issue.fileName, " on line: ", issue.line, " with label: ", issue.label

	if issue.label is None:
		labels = []
	else:
		labels = [issue.label]
	
	data = {"title" : "{} : {}".format(issue.fileName, issue.line), "body" : issue.issue, "assignee" : "tylermuch", "milestone" : None, "state" : "open", "labels" : labels}
	
	url = urljoin(API_URL, "/".join(["repos", getOwner(), getRepo(), "issues"]))
	url = url + "?access_token=" + getToken()

	print "url = " + url

	r = requests.post(url, data = json.dumps(data), headers = HEADERS)

	if r.ok:
		print "SUCCESS"
		j = json.loads(r.text or r.content)
		return j['number']
	else:
		print "Not OK"
		print r.text
		print "{}:{}".format("Status", r.status_code)



def getIssueNumberList():

	list = []

	url = urljoin(API_URL, "/".join(["repos", getOwner(), getRepo(), "issues"]))
	url = url + "?access_token=" + getToken()

	r = requests.get(url)

	if r.ok:
		j = json.loads(r.text or r.content)
		for issue in j:
			list.append(issue['number'])
		return list
	#TODO: error handling
	else:
		print "Not OK"
		print r.text
		print "{}:{}".format("Status", r.status_code)
		return None