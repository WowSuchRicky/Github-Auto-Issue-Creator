DEBUG = False

def debug_print(*arg):
	if DEBUG:
		string = ""
		for a in arg:
			string = string + " " + a
		string = string.strip()

		print string
