#! /usr/bin/python

import os
import base64
import argparse


def _dir(path):
	if not os.path.isdir(path):
		raise argparse.ArgumentTypeError('%s is not a directory' % path)
	else:
		return path

def _list(dir):
	for dirpath, dirnames, filenames in os.walk(dir):
		for filename in filenames:
			if not filename.startswith('.'):
				prefix = filename[0:3]
				name, ext = os.path.splitext(filename[4:])
				chname = base64.urlsafe_b64decode(name)
				line = '%s %s' % (prefix, chname)
				print(line)
		for dirname in dirnames:
			prefix = dirname[0:3]
			chname = base64.urlsafe_b64decode(dirname[4:])
			line = '%s %s' % (prefix, chname)	
			print(line)

def main():
	parser = argparse.ArgumentParser(description='list view points')
	parser.add_argument('dir', type=_dir, help='directory to list')	
	args = parser.parse_args()
	_list(args.dir)

if __name__ == '__main__':
	main()
