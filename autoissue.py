#!/usr/bin/python
#from os import listdir, path
import os, argparse, re, errno
from util import debug_print

#global vars
blacklist = [".git", "autoissue.py*", "github.py*", "README.md", "util.py*", "settings.williames", ".gitignore", "setup", "*.DS_Store", "test/parsingtests", "test.py*"] #blacklist for file/dir names (added .DS_Store because super annoying)
startToken = "TODO"
endToken = "ODOT"

#issue class, just has the content and lineNumber fields right now.
class Issue:
	def __init__(self, title, issueContent, lineNumber, fileName, label, inum):
		self.data = {}
		self.title = title
		self.issue = issueContent
		self.line = lineNumber
		self.fileName = fileName
		self.label = label
		self.issue_num = inum

	def __str__(self):
		return "Issue: {}\n\tIssue#: {}\n\tFile: {}\n\tLine: {}\n\tLabels: {}\n\tContent: {}\n".format(self.title, self.issue_num, self.fileName, self.line, self.label, self.issue)

	def __cmp__(self, other):
		return self.title == other.title \
		and self.issue == other.issue \
		and	self.line  == other.line \
		and	self.fileName  == other.fileName \
		and	self.label == other.label \
		and	self.issue_num == other.issue_num \

# Returns whitelist in regex form
def getWhitelistRegex():
	whitelistinfile = None
	while whitelistinfile is None:
		try:
			with open("autoissue.whitelist") as file:
				whitelistinfile = [item.strip() for item in file.readlines()]
		except IOError as (eno, strerror):
			if eno == errno.ENOENT:
				open("autoissue.whitelist", "w")

	whitelist = []

	for entry in whitelistinfile:
		if os.path.isdir(entry):
			entry += "/*"
		whitelist.append(entry.replace("*", "(.*)"))
	return whitelist

#Function that gets all of the whitelisted files (and folders) in a folder
def getFiles(directory = "."):
	fileList = []
	for root, dirs, files in os.walk(directory):
		for fileName in files:
			relDir = os.path.relpath(root, directory)
			relFile = os.path.join(relDir if relDir is not "." else "", fileName)
			if any([re.match(pattern + "$", relFile) is not None for pattern in getWhitelistRegex()]):
				fileList.append(relFile)


	return fileList

def getIssues():
	files = getFiles()
	issues = []
	for file in files:
		issues += findIssuesInFile(file)
	return issues


# returns a list of the Issues in this file
def findIssuesInFile(file):
	lineNumber = 0
	issueList = []

	with open(file, 'r') as f:
		data = f.readlines()

	debug_print("Searching for issues in:", file, "(lines: {})".format(len(data)))

	while lineNumber < len(data):
		issueString = ""
		if startToken in data[lineNumber]:
			# TODO: change to check if // comes just before startToken. This will cover the case where the comment comes after code in the line. Also, handle this case.
			if data[lineNumber].strip().startswith("//"):
				startingLine = lineNumber
				issueString += data[lineNumber]
				lineNumber += 1
				while lineNumber < len(data):
					line = data[lineNumber]
					if line.strip(): # if the line is not empty
						if line.startswith("//"):
							issueString += line[2:]
						else:
							lineNumber -= 1 # since we increment outside of this loop
							break
					lineNumber += 1
			elif data[lineNumber].strip().startswith("/*"):
				startingLine = lineNumber
				issueString += data[lineNumber]
				if not issueString.strip().endswith("*/"):
					lineNumber += 1
					while lineNumber < len(data):
						line = data[lineNumber]
						if line.strip():
							issueString += line
							if line.strip().endswith("*/"):
								break
						lineNumber += 1
			else:
				lineNumber += 1
				break
			issueList.append(parseIssueFromRawComment(issueString, startingLine, file))
		lineNumber += 1
	return issueList


# returns an Issue
def parseIssueFromRawComment(comment, line, file):
	data = {}
	title = None
	labels = []
	inum = None
	tags_regex = "\[(.*?)\]"
	r = re.compile(tags_regex)
	tags = r.findall(comment)

	# If no [title:] tag is specified, then the first line is autmatically the title
	for tag in tags:
		if ":" not in tag:
			# This is the issue number tag
			inum = int(tag) # Should eventually check to be sure there are only numbers in here
		else:
			t, v = tag.split(":")
			if t.lower() == "title":
				title = v
			elif t.lower() == "label":
				labels = [x.strip() for x in v.split(",")]

	if title is None:
		title = comment.splitlines()[0] # Make the title the first line of the comment

	content = re.sub(tags_regex, "", comment)
	content = re.sub("(//(\s*)TODO)|(/\*(\s*)TODO)|(\*/)", "", content).strip()
	issue = Issue(title, content, line + 1, file, labels, inum)
	issue.data = data
	return issue

def injectNumber(issue, number):
	with open(issue.fileName, 'r') as file:
		data = file.readlines()

	lineNumber = issue.line - 1
	line = data[lineNumber]
	startIndex = line.index(startToken) + len(startToken)
	data[lineNumber] = data[lineNumber][:startIndex] + " [" + str(number) + "] " + data[lineNumber][startIndex:]

	with open(issue.fileName, 'w') as file:
		file.writelines(data)

def main():
	from github import createIssues
	parser = argparse.ArgumentParser(description="Auto-Issue-Creator argument parser")
	parser.add_argument("-s", "--start", help="the token that begins the TODO: (ie. 'TODO')")
	parser.add_argument("-d", "--debug", action='store_true', help="enable debug mode (no POSTing to github)")

	args = vars(parser.parse_args())

	if args["start"] != None:
		global startToken #set scope
		startToken = args["start"]
		print "Starting token set as: ", startToken
	else:
		print "Using default starting token: ", startToken

	#see if we're in debug mode
	if args["debug"]:
		debug = True
		print "Debug mode enabled"
	else:
		debug = False

	issueList = getIssues()
	for issue in issueList:
		print issue
	createIssues(issueList, debug)

if __name__ == "__main__":
    main()
