#! /usr/bin/python

import sys
import os
import re
import base64
import shutil
import argparse

def _dir(path):
	if not os.path.isdir(path):
		raise argparse.ArgumentTypeError('%s is not a directory' % path)
	else:
		return os.path.normpath(path)

def _strip(dirname):
	dirname = re.sub(r'\s+\d+$', '', dirname)		
	if re.match(r'^\d+\s*$', dirname) is not None:
		dirname = re.sub(r'^\d+\s*', '', dirname)
	return dirname

def _flat(src, dest, start, test):
	i = start
	for dirpath, dirnames, filenames in os.walk(src):
		dir_created = False
		for filename in filenames:
			filepath = os.path.join(dirpath, filename)
			d, f = os.path.split(filepath[len(src) + 1:])
			d = _strip(d)
			newdir = os.path.join(dest, '%03d_%s' % (i, base64.urlsafe_b64encode(d)))
			newpath = os.path.join(newdir, f)
			if not os.path.isdir(newdir):
				if not test:
					os.makedirs(newdir)
				dir_created = True
			print('%s -> %s' % (filepath, newpath))
			if not test:
				shutil.copy(filepath, newpath)
		if dir_created:
			i += 1

def _defaut_out(src):
	return '%s.flat' % os.path.normpath(src)

def main():
	parser = argparse.ArgumentParser(description='flat original directory')
	parser.add_argument('-s', '--start', help='start index', type=int, default=0)
	parser.add_argument('-o', '--output', help='output directory')
	parser.add_argument('-t', '--test', action='store_true', help='list results')
	parser.add_argument('dir', type=_dir, help='input directory')
	args = parser.parse_args()
	test = args.test
	start = args.start
	src = args.dir
	dest = _defaut_out(src) if args.output is None else args.output
	_flat(src, dest, start, test) 

if __name__ == '__main__':
	main()
