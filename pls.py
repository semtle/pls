#!/usr/bin/env python

import sys
import subprocess
import os
import re
import urllib2

def printHelp():
	print 'Usage:\n'
	print '\tpls [options] [search terms]\n'
	print 'Options:\n'
	print '\t-c: open using Chrome\n'
	print '\t-f: open using Firefox\n'
	print '\t-l: I\'m Feeling Lucky\n'
	print '\t-h: display usage information\n'
	print 'Notes:'
	print '\t- search terms do not need to be enclosed in quotes.'
	print '\t- any special characters (*, ", $, etc...) will be consumed by the shell before the script can even get its hands on them. To use these literal characters in a search query, escape them with \.'

query = ''
browser = 'xdg-open' # system default browser - thanks: http://stackoverflow.com/questions/5116473/linux-command-to-open-url-in-default-browser
DEVNULL = open(os.devnull, 'w')

for arg in sys.argv[1:]: # skip first argument in sys.argv because it's the name of the script
	if arg == '-c':
		browser = 'google-chrome'
	elif arg == '-f':
		browser = 'firefox'
	elif arg == '-i':
		pass # images
	elif arg == '-s':
		pass # scholar
	elif arg == '--help' or arg == '-h':
		printHelp()
		exit(0)
	elif arg == '-l':
		pass # process this later
	else:
		query += arg
		query += '+'

# thanks: http://stackoverflow.com/questions/15478127/remove-final-character-from-string-python
query = query[:-1] # remove final '+' added by for loop

url = 'https://www.google.com/search?q=' + query

if '-l' in sys.argv:
	req = urllib2.Request(url, headers={'User-Agent' : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.30 (KHTML, like Gecko) Ubuntu/11.04 Chromium/12.0.742.112 Chrome/12.0.742.112 Safari/534.30"}) 
	con = urllib2.urlopen(req).read() # get html source
	searchObj = re.search( r'<h3 class="r"><a href="(.*?)"', con) # get first occurrence of a result and capture its url
	url = searchObj.group(1)

subprocess.call([browser, url], stdout=DEVNULL, stderr=subprocess.STDOUT) # shhhh - redirect browser output to /dev/null
# thanks: http://stackoverflow.com/questions/11269575/how-to-hide-output-of-subprocess-in-python-2-7
