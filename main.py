#!/usr/bin/python
#from os import listdir, path
import os
#issue class, just has the content and lineNumber fields right now.
class Issue:
	def __init__(self, issueContent, lineNumber):
		self.data = []
		self.issue = issueContent
		self.line = lineNumber


#Function that gets all of the files (and folders) in a folder
def getFiles(directory):
	#List all sub-directories and files
	fileList = []

	for d in os.listdir(directory):
		d = directory + "/" + d #make the format actually work for our function calls

		#print d, os.path.isdir(d) #debug

		#if the "file" is a directory...
		if os.path.isdir(d):
			for file in getFiles(d): #recursively iterate through the subfolders
				fileList.append(file)

		#otherwise the file is indeed a file
		else:
			if not "main.py" in d:
				fileList.append(d)

	#return list of actual files to open
	return fileList


#Function which takes a file and returns a list of Issues
def lookForIssue(file):	#reads through an input file and returns a list of issues to be posted to github repo
	#local variables
	lineNumber = 1
	issueList = []

	with open(file) as f:
		print "Opened: ", file
		for line in f:
			if "TODO" in line:
				iss = Issue(parseString(line), lineNumber)
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
		print issue.issue, " on line: ", issue.line



unitTest()
