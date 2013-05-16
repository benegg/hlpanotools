#! /usr/bin/python

import sys
import os
import shutil
import argparse
import base64

def _isdir(path):
	if not os.path.isdir(path):
		raise argparse.ArgumentTypeError('%s is not a directory' % path)
	else:
		return path
	
def _mktour(src, dest):
	for dirpath, dirnames, filenames in os.walk(src):
		[shutil.rmtree(os.path.join(dirpath, d)) for d in dirnames]
		paths = ['"%s"' % os.path.join(dirpath, filename) for filename in filenames]	
		scriptpath = sys.path[0]
		cmd = '%s/krpanotools-1.16.1-mac64/kmakemultires %s/krpanotools-1.16.1-mac64/templates/vtour-normal.config %s' % (scriptpath, scriptpath, ' '.join(paths))
		print(cmd)
		os.system(cmd)
	normdir = os.path.normpath(dirpath)
	srctour = os.path.join(normdir, 'vtour')
	shutil.rmtree(dest, ignore_errors=True)
	shutil.move(srctour, dest)

def _create_tmp(src, tmp):
	for dirpath, dirnames, filenames in os.walk(src):
		for filename in filenames:
			if not filename.startswith('.'):
				basename, ext  = os.path.splitext(filename)
				destname = filename
				if len(basename) > 4:
					num, b64name = basename[0:4], basename[4:]
					try:
						destname = base64.urlsafe_b64decode(b64name)
						destname = num + destname.replace(os.path.sep, '-') + ext
					except TypeError:
						pass
				linkfrom = os.path.join(src, filename)
				linkto = os.path.join(tmp, destname)
				print '%s -> %s' % (linkfrom, linkto)
				os.symlink(linkfrom, linkto)

def main():
	print sys.path[0] 
	parser = argparse.ArgumentParser(description='make pano tour')
	parser.add_argument('-p', '--preview', action='store_true', help='open tour after making')
	parser.add_argument('dir', type=_isdir, help='panorama directory')
	args = parser.parse_args()
	ndir = os.path.normpath(args.dir)
	tmp, dest = ndir + '.tmp', ndir + '.tour'
	shutil.rmtree(tmp, ignore_errors=True)
	shutil.rmtree(dest, ignore_errors=True)
	os.mkdir(tmp)
	_create_tmp(ndir, tmp)
	_mktour(tmp, dest)
	shutil.rmtree(tmp, ignore_errors=True)
	if args.preview:
		os.system('open %s/tour.html' % dest)

if __name__ == '__main__':
	main()
