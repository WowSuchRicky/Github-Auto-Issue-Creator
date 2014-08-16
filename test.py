from autoissue import findIssuesInFile
from autoissue import getFiles
from autoissue import Issue
from autoissue import parseIssueFromRawComment
import unittest

debug = False

TEST_PREFIX = "test/parsingtests/tag_parse/inputs/"

def getExpected(file, t, l, i):
	title = None
	label = []
	issue = None
	if t:
		title = "Title"
	if l:
		label = ['bug']
	if i:
		issue = 55
	if debug:
		print "title:", "YES," if t else "NO,", "label:", "YES," if l else "NO,", "issue:", "YES" if i else "NO"
	return Issue(title, "This is a test", 0, file, label, issue)

def getIssueFromFile(file):
	testfile = TEST_PREFIX + file
	with open(testfile) as f:
		comment = f.read()
	result = parseIssueFromRawComment(comment, 0, testfile)
	result.title = "Title"
	return result

class TestCommentParsing(unittest.TestCase):

	def testFiles(self):
		files = getFiles("test/parsingtests/comment_parse/inputs")
		for file in files:
			numFound = len(findIssuesInFile(file))
			with open(file.replace("input", "output")) as f:
				expected = int(f.read())
			self.assertEqual(numFound, expected)

	def testBlockIssue(self):
		self.assertEqual(getIssueFromFile("block_comment_issue"), getExpected(file, False, True, False))
	def testBlockIssueLabel(self):
		self.assertEqual(getIssueFromFile("block_comment_issue_label"), getExpected(file, False, True, True))
	def testBlockIssueLabelTitle(self):
		self.assertEqual(getIssueFromFile("block_comment_issue_label_title"), getExpected(file, True, True, True))
	def testBlockIssueTitle(self):
		self.assertEqual(getIssueFromFile("block_comment_issue_title"), getExpected(file, True, True, False))
	def testBlockIssueTitleLabel(self):
		self.assertEqual(getIssueFromFile("block_comment_issue_title_label"), getExpected(file, True, True, True))
	def testBlockLabel(self):
		self.assertEqual(getIssueFromFile("block_comment_label"), getExpected(file, False, False, True))
	def testBlockLabelIssue(self):
		self.assertEqual(getIssueFromFile("block_comment_label_issue"), getExpected(file, False, True, True))
	def testBlockLabelIssueTitle(self):
		self.assertEqual(getIssueFromFile("block_comment_label_issue_title"), getExpected(file, True, True, True))
	def testBlockLabelTitle(self):
		self.assertEqual(getIssueFromFile("block_comment_label_title"), getExpected(file, True, False, True))
	def testBlockLabelTitleIssue(self):
		self.assertEqual(getIssueFromFile("block_comment_label_title_issue"), getExpected(file, True, True, True))
	def testBlockNone(self):
		self.assertEqual(getIssueFromFile("block_comment_none"), getExpected(file, False, False, False))
	def testBlockTitle(self):
		self.assertEqual(getIssueFromFile("block_comment_title"), getExpected(file, True, False, False))
	def testBlockTitleIssue(self):
		self.assertEqual(getIssueFromFile("block_comment_title_issue"), getExpected(file, True, True, False))
	def testBlockTitleIssueLabel(self):
		self.assertEqual(getIssueFromFile("block_comment_title_issue_label"), getExpected(file, True, True, True))
	def testBlockTitleLabel(self):
		self.assertEqual(getIssueFromFile("block_comment_title_label"), getExpected(file, True, False, True))
	def testBlockTitleLabelIssue(self):
		self.assertEqual(getIssueFromFile("block_comment_title_label_issue"), getExpected(file, True, True, True))

	def testBlockIssue(self):
		self.assertEqual(getIssueFromFile("line_comment_issue"), getExpected(file, False, True, False))
	def testLineIssueLabel(self):
		self.assertEqual(getIssueFromFile("line_comment_issue_label"), getExpected(file, False, True, True))
	def testLineIssueLabelTitle(self):
		self.assertEqual(getIssueFromFile("line_comment_issue_label_title"), getExpected(file, True, True, True))
	def testLineIssueTitle(self):
		self.assertEqual(getIssueFromFile("line_comment_issue_title"), getExpected(file, True, True, False))
	def testLineIssueTitleLabel(self):
		self.assertEqual(getIssueFromFile("line_comment_issue_title_label"), getExpected(file, True, True, True))
	def testLineLabel(self):
		self.assertEqual(getIssueFromFile("line_comment_label"), getExpected(file, False, False, True))
	def testLineLabelIssue(self):
		self.assertEqual(getIssueFromFile("line_comment_label_issue"), getExpected(file, False, True, True))
	def testLineLabelIssueTitle(self):
		self.assertEqual(getIssueFromFile("line_comment_label_issue_title"), getExpected(file, True, True, True))
	def testLineLabelTitle(self):
		self.assertEqual(getIssueFromFile("line_comment_label_title"), getExpected(file, True, False, True))
	def testLineLabelTitleIssue(self):
		self.assertEqual(getIssueFromFile("line_comment_label_title_issue"), getExpected(file, True, True, True))
	def testLineNone(self):
		self.assertEqual(getIssueFromFile("line_comment_none"), getExpected(file, False, False, False))
	def testLineTitle(self):
		self.assertEqual(getIssueFromFile("line_comment_title"), getExpected(file, True, False, False))
	def testLineTitleIssue(self):
		self.assertEqual(getIssueFromFile("line_comment_title_issue"), getExpected(file, True, True, False))
	def testLineTitleIssueLabel(self):
		self.assertEqual(getIssueFromFile("line_comment_title_issue_label"), getExpected(file, True, True, True))
	def testLineTitleLabel(self):
		self.assertEqual(getIssueFromFile("line_comment_title_label"), getExpected(file, True, False, True))
	def testLineTitleLabelIssue(self):
		self.assertEqual(getIssueFromFile("line_comment_title_label_issue"), getExpected(file, True, True, True))


def main():
	unittest.main()

if __name__ == '__main__':
	main()
