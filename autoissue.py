#!/usr/bin/python
#from os import listdir, path
import os

blacklist = [".git", "autoissue.py", "README"] #blacklist for file/dir names

#issue class, just has the content and lineNumber fields right now.
class Issue:
	def __init__(self, issueContent, lineNumber, fileName):
		self.data = []
		self.issue = issueContent
		self.line = lineNumber
		self.fileName = fileName


#Function that gets all of the files (and folders) in a folder
def getFiles(directory):
	#List all sub-directories and files
	fileList = []
	blacklisted = False

	for d in os.listdir(directory):
		d = directory + "/" + d #make the format actually work for our function calls

		#print d, os.path.isdir(d) #debug

		#if the "file" is a directory...
		if os.path.isdir(d) and not ".git" in d: #we never want .git files; excluded to prevent stdout pollution
			for file in getFiles(d): #recursively iterate through the subfolders
				fileList.append(file)

		#otherwise the file is indeed a file (excluding the current file, autoissue.py)	
		#make sure our file isn't blacklisted before actually adding it to the list
		else:
			#iterate through our blacklist
			for black in blacklist:
				if black in d:
					blacklisted = True

			if not blacklisted:
				fileList.append(d)

			else:
				print "Excluded file (blacklist): ", d

	#return list of actual files to open
	return fileList


#Function which takes a file and returns a list of Issues
def lookForIssue(file):	#reads through an input file and returns a list of issues to be posted to github repo
	#local variables
	lineNumber = 1
	issueList = []

	if not ".git" in file:
		with open(file) as f:
			print "Searching for TODOs in: ", file
			for line in f:
				if "TODO" in line:
					iss = Issue(parseString(line), lineNumber, file)
					issueList.append(iss)
					lineNumber = 0;

				lineNumber += 1

	return issueList


#function that parses out the portion enclosed in the TODO ... ODOT in the string
def parseString(string):
	startIndex = string.index("TODO") + 6 #+6 is to account for "TODO: "
	endIndex = string.index("ODOT")
	return string[startIndex:endIndex]


def unitTest():
	#local variables
	issueList = []
	files =	getFiles(".")
	for file in files:
		for issue in lookForIssue(file):
			issueList.append(issue)



	print "\n\n\n\n ISSUES TO BE ADDED TO THE REPO:"
	for issue in issueList:
		print issue.issue, " in file: ", issue.fileName, "on line: ", issue.line



unitTest()
