#! /usr/bin/env python
# coding:utf-8

import argparse
import os
import xml.etree.ElementTree as ET
import shutil

def comxml(src, dest):
	dest.extend(src.findall('scene'))

def combine(src, dest):
	shutil.rmtree(dest, ignore_errors=True)
	os.mkdir(dest)
	os.system('cp -rv %s %s' % (src[0], dest))
	destpanosdir = os.path.join(dest, 'panos')
	destxml = os.path.join(dest, 'tour.xml')
	desttree = ET.parse(destxml)
	destroot = desttree.getroot()
	for item in src[1:]:
		itempanos = os.path.join(item, 'panos', '*')
		itemxml = os.path.join(item, 'tour.xml')
		os.system('cp -rv %s %s' % (itempanos, destpanosdir)) 
		itemtree = ET.parse(itemxml)
		comxml(itemtree.getroot(), destroot)
	desttree.write(destxml)

def main():
	parser = argparse.ArgumentParser(description='combine multiple tours')
	parser.add_argument('tours', nargs='*', help='tours to combine')
	parser.add_argument('-o', '--output', required=True, help='combined tour directory')
	args = parser.parse_args()
	if len(args.tours) < 2:
		print 'please specify at least two tours to combine.'
	else:
		combine(args.tours, args.output)

if __name__ == '__main__':
	main()
