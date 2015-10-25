import requests
import json
import getpass
import os
import util
from autoissue import injectNumber
from urlparse import urljoin


API_URL = 'https://api.github.com'
SETTINGS = 'settings.williames' #settings file
HEADERS = {'Content-type':'application/json'}
TOKEN_KEY = 'auth_token'

def getToken():
	val = getValue(TOKEN_KEY)
	if val is not None:
		return val

	#generate a token
	username = raw_input('Github username: ')
	password = getpass.getpass('Github password: ')

	url = urljoin(API_URL, 'authorizations')
	payload = {'note' : 'auto-issue-creator', 'scopes' : ['repo']}
	r = requests.post(url, auth = (username, password), data = json.dumps(payload),)

	if r.status_code is requests.codes['created']:
		token = json.loads(r.text or r.content)['token']
		if not addProperty(TOKEN_KEY, token):
			print "Could not write authorization token to settings file. Please add the following line to " + SETTINGS + ":\n" + "auth_token " + token
		return token
	else:
		print "Failed to generate a new authorization token"
		print r.text
		return None

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


def getRepo():
	val = getValue("repo")

	if val is not None:
		return val # return the repo saved in the settings file

	# Get the active git repo
	origin = False
	with open('.git/config') as f:
		for line in f:
			if "[remote \"origin\"]" in line: 
				origin = True
			if "url = " in line and origin:
				r = line.split("=")[1].split("github.com/")[1].split("/")[1].replace(".git\n", "")
				origin = False

	# Add to our settings file
	if r:
		addProperty("repo", r)
		return r

def getOwner():
	val = getValue("owner")
	if val is not None:
		return val # return the owner saved in the settings file


	# Get the active git repo
	with open('.git/config') as f:
		origin = False
		for line in f:
			if "[remote \"origin\"]" in line: 
				origin = True
			if "url = " in line and origin:
				r = line.split("=")[1].split("github.com/")[1].split("/")[0]
				origin = False

	# Add to our settings file
	if r:
		addProperty("owner", r)
		return r


def createIssues(issues, debug = False):
	beforeIssues = getIssueNumberList()
	afterIssues = []

	if debug:
		print "Debug mode on. Not actually creating issues in repo"
	else:
		for issue in issues:
			if issue.issue_num is not None:
				afterIssues.append(issue.issue_num)
			else:
				number = createIssue(issue)
				# inject issue number tag into TODO comment
				injectNumber(issue, number)

		util.debug_print("before issues:\n", str(beforeIssues), "\nafter issues:\n", str(afterIssues))
		removeIssuesInDiff(beforeIssues, afterIssues)


def createIssue(issue):
	print "CREATING ISSUE: ", issue.issue, " in file: ", issue.fileName, " on line: ", issue.line, " with label: ", issue.label

	title = "*AutoIssue* " + issue.title
	body = issue.issue
	assignee = getOwner()
	labels = [] if issue.label is None else issue.label

	data = {"title" : title, "body" : body, "state" : "open", "labels" : labels}

	url = urljoin(API_URL, "/".join(["repos", getOwner(), getRepo(), "issues"]))
	url = url + "?access_token=" + getToken()

	util.debug_print("Issue create request url =", url)

	r = requests.post(url, data = json.dumps(data), headers = HEADERS)

	if r.status_code is requests.codes['created']:
		j = json.loads(r.text or r.content)
		print "Successfully created issue", j['number']
		return j['number']
	else:
		print "Something went wrong while attempting to create the issue on Github"
		print "{}:{}".format("Status", r.status_code)
		print r.text



def getIssueNumberList():
	list = []

	url = urljoin(API_URL, "/".join(["repos", getOwner(), getRepo(), "issues"]))
	url = url + "?access_token=" + getToken()

	r = requests.get(url)

	if r.ok:
		j = json.loads(r.text or r.content)
		for issue in j:
			if "*AutoIssue*" in issue['title']:
				list.append(issue['number'])
		return list
	else:
		print "Something went wrong while getting the list of existing issues in the repository."
		print "{}:{}".format("Status", r.status_code)
		print r.text
		return None

def removeIssuesInDiff(beforeIssues, afterIssues):
	def diff(a, b):
		b = set(b)
		return [aa for aa in a if aa not in b]

	data = {"state" : "closed"}

	for issue in diff(beforeIssues, afterIssues):
		url = urljoin(API_URL, "/".join(["repos", getOwner(), getRepo(), "issues", str(issue)]))
		url = url + "?access_token=" + getToken()
		r = requests.post(url, data = json.dumps(data), headers = HEADERS)
		if r.ok:
			print "Closed issue", issue
		else:
			print "Failed to close issue", issue
			print r.text
