#! /usr/bin/python

import os
import re
import argparse

def _strip(dir, test):
	for dirpath, dirnames, filenames in os.walk(dir, topdown=False):
		for dirname in dirnames:
			dirname1 = re.sub(r'\s+\d+$', '', dirname)		
			if re.match(r'^\d+\s*$', dirname1) is not None:
				dirname1 = re.sub(r'^\d+\s*', '', dirname1)
			if (dirname1 != dirname) and not test:
				os.rename(os.path.join(dirpath, dirname), os.path.join(dirpath, dirname1))
			print('%s -> %s' % (dirname, dirname1))

def main():
	parser = argparse.ArgumentParser(description='strip number prefix and date surfix')
	parser.add_argument('-t', '--test', action='store_true', help='list without convert')
	parser.add_argument('dir', help='directory to proceed')
	args = parser.parse_args()
	test = args.test
	_strip(args.dir, test)

if __name__ == '__main__':
	main()
