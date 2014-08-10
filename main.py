#!/usr/bin/python
from os import listdir

#issue class, just has the content and lineNumber fields right now.
class Issue:
	def __init__(self, issueContent, lineNumber):
		self.data = []
		self.issue = issueContent
		self.line = lineNumber

#local variables:
issueList = []
lineNumber = 1

#List all sub-directories and files
iss = Issue("", "")
for d in listdir("test"):
	d = "test/" + d
	with open(d) as f:
		print "Opened: ", d
		for line in f:
			if "TODO" in line:
				iss = Issue(line, lineNumber)
				issueList.append(iss)
				lineNumber = 0;
			lineNumber = lineNumber + 1

print "\n\n\n\n ISSUES TO BE ADDED TO THE REPO:"
for issue in issueList:
	print issue.issue, " on line: ", issue.line