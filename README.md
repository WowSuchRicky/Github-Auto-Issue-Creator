If you have lines of code in your program that have a portion such as: "//TODO: Fix this part" and want to keep track of these, this is your tool!

This seems to work fine on Unix-based OSs (Linux, OS X, etc..) however, not quite on Windows.
To get it to work on Windows:

1. Download pip (We've included a copy in /setup if you'd like, but we still recommend downloading the latest) (https://raw.githubusercontent.com/pypa/pip/master/contrib/get-pip.py) and run it (python get-pip.py)

2. Run "C:\Python27\Scripts\pip.exe install requests"

3. It should now work fine! Feel free to proceed to the rest of the instructions.

Searches through all current files and subfolders for these lines, and creates an issue in the respective Github repo automatically. 

Simply run the tool (python autoissue.py) and it'll do all of the work for you, after prompting you for your Github Credentials (which will request a token that will be saved, so you shouldn't have to enter your info more than once).

Feel free to submit pull requests/issues/etc. or contact us.
