#! /usr/bin/env python

import argparse
import os
import sys
import shutil

def _dir(value):
	if not os.path.isdir(value):
		raise argparse.ArgumentTypeError('%s is not a directory' % value)
	return os.path.normpath(value)

def default_out(src):
	return '%s.flat' % os.path.normpath(src)

def stitch(target, out, config):
	for dirpath, dirnames, filenames in os.walk(target):
		for dirname in dirnames:
			srcdir = os.path.join(dirpath, dirname)
			for i in xrange(7):
				fjpg = os.path.join(srcdir, '%d.jpg' % i)
				tjpg = os.path.join('/tmp', 'pano%d.jpg' % i)
				print('%s -> %s' % (fjpg, tjpg))
				shutil.copyfile(fjpg, tjpg)
				if i == 6:
					os.system('convert -rotate -90 %s %s' % (tjpg, tjpg))
			tool = os.path.join(sys.path[0], 'PTStitcherNG0.7b', 'mac', 'PTStitcherNG')
			stitched = os.path.join(out, dirname + '.jpg')
			stitchcmd = '%s -o %s %s' % (tool, stitched, config)
			print stitchcmd
			os.system(stitchcmd)

def main():
	parser = argparse.ArgumentParser(description='auto stitch')
	parser.add_argument('-o', '--out', type=_dir, help='output directory')
	parser.add_argument('config')
	parser.add_argument('target', type=_dir)
	args = parser.parse_args()
	out = args.out if args.out else default_out(args.target)
	shutil.rmtree(out, ignore_errors=True)
	os.mkdir(out)
	stitch(args.target, out, args.config)

if __name__ == '__main__':
	main()
