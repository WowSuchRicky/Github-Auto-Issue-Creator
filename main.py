#!/usr/bin/python
from os import listdir

#issue class, just has the content and lineNumber fields right now.
class Issue:
	def __init__(self, issueContent, lineNumber):
		self.data = []
		self.issue = issueContent
		self.line = lineNumber


#Function which takes a file and returns a list of Issues
def lookForIssue(file):	#reads through an input file and returns a list of issues to be posted to github repo
	#local variables
	lineNumber = 1
	issueList = []

	with open(file) as f:
		print "Opened: ", d
		for line in f:
			if "TODO" in line:
				iss = Issue(line, lineNumber)
				issueList.append(iss)
				lineNumber = 0;
			lineNumber = lineNumber + 1

	return issueList



#local variables
issueList = []

#List all sub-directories and files
for d in listdir("test"):
	d = "test/" + d
	for issue in lookForIssue(d):
		issueList.append(issue)

print "\n\n\n\n ISSUES TO BE ADDED TO THE REPO:"
for issue in issueList:
	print issue.issue, " on line: ", issue.line