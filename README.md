####About
If you have lines of code in your program that have a portion such as: "//TODO: Fix this part" and want to keep track of these, this is your tool! It searches through all current files and subfolders for these lines, and creates an issue in the respective Github repo automatically. 

This seems to work fine on Unix-based OSs (Linux, OS X, etc..) however, not quite on Windows.

####Extra steps to install/run on Windows:
0. Download Python 2.7 from [here](https://www.python.org/downloads/)
1. Download pip (we've included a copy in `/setup` if you'd like, but we still recommend downloading the latest [here](https://raw.githubusercontent.com/pypa/pip/master/contrib/get-pip.py) and run it (`python get-pip.py`)
2. Run `C:\Python27\Scripts\pip.exe install requests`
3. It should now work fine! Feel free to proceed to the rest of the instructions.


Simply create the autoissue.whitelist file containing regular expressions that will match the type of files to be searched, copy (autoissue.py, github.py, and util.py) and run the tool (`python autoissue.py`) and it'll do all of the work for you, after prompting you for your Github credentials (which will request a token that will be saved, so you shouldn't have to enter your info more than once).

## Command line arguments
```
Usage: python ./autoissue.py [FLAGS]
   -d --debug : debug mode; issues will not actually be pushed/synced, this is mainly for development/testing.
   -i --interactive : show a list of issues first and prompt one at a time before adding them to GitHub, BitBucket, etc.
   -p --path path : specify the path to the git repo you'd like to work with
   -s --start startToken : specify the token that will be used to parse for todos (Default: 'TODO')
```

Feel free to submit pull requests/issues/etc. or contact us.

Unless specified otherwise, the MIT License ([link](http://opensource.org/licenses/MIT)) applies to all of this code. By executing or even downloading the source code, you're agreeing to comply with all MIT license specifics. 
