#! /usr/bin/env python
# coding:utf-8

import argparse
import os
import base64
import re
import sys
import codecs
import locale

def tobase64(string, reverse):
	prefix, ext = '', ''
	if re.match(r'\d{3}_.*', string):
		prefix, string = string[:4], string[4:]
	m = re.match(r'^(.*)(\.\w+)$', string)
	if m:
		string, ext = m.groups()
	string = base64.urlsafe_b64decode(string) if reverse else base64.urlsafe_b64encode(string)
	return prefix + string + ext

def main():
	sys.stdout = codecs.getwriter(locale.getpreferredencoding())(sys.stdout)	
	reload(sys)
	parser = argparse.ArgumentParser(description='convert string to url safe base64')
	parser.add_argument('string', help='string to convert')
	parser.add_argument('-r', '--reverse', action='store_true', help='convert from base64')
	args = parser.parse_args()
	print tobase64(args.string, args.reverse)

if __name__ == '__main__':
	main()
