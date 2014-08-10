#!/usr/bin/python
#from os import listdir, path
import os

blacklist = [".git", "autoissue.py", "README"] #blacklist for file/dir names

#issue class, just has the content and lineNumber fields right now.
class Issue:
	def __init__(self, issueContent, lineNumber, fileName, label):
		self.data = []
		self.issue = issueContent
		self.line = lineNumber
		self.fileName = fileName
		self.label = label


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

	with open(file) as f:
		print "Searching for TODOs in: ", file
		for line in f:
			if "TODO" in line:
				iss = generateIssue(line, lineNumber, file)
				issueList.append(iss)
				lineNumber = 0;

			lineNumber += 1

	return issueList


#function that parses out the portion enclosed in the TODO ... ODOT in the string and returns the completed obj
def generateIssue(issueText, lineNumber, fileName):
	args = ["@label"]
	label = ""

	#search for any sort of arguments in the todo
	splitString = issueText.split(" ") #tokenize the input string to try to find args
	for arg in args:
		for token in splitString:
			if arg in token:
				label = token.split(":")[1]
				print "arg found! ", arg, ": ", label


	startIndex = issueText.index("TODO") + 6 #+6 is to account for "TODO: "
	endIndex = issueText.index("ODOT")
	return Issue(issueText[startIndex:endIndex], lineNumber, fileName, label)

def getIssueList(dir):
	#local variables
	if dir is None
		dir = "."

	issueList = []
	files =	getFiles(dir)


	for file in files:
		for issue in lookForIssue(file):
			issueList.append(issue)



	print "\n\n\n\n ISSUES TO BE ADDED TO THE REPO:"
	for issue in issueList:
		print issue.issue, " in file: ", issue.fileName, "on line: ", issue.line, " with label: ", issue.label


	return issueList

def main():
	issueList = getIssueList();

if __name__ == "__main__":
    main()