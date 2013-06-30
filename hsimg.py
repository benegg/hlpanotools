#! /usr/bin/python
# -*-coding:utf-8-*-

import argparse
import os
import xlrd
import json
import codecs
import sys
import locale
import shutil

def main():
	parser = argparse.ArgumentParser(description='gather hotspot image list')
	parser.add_argument('workbook', type=file, help='workbook contains hotspot image info')
	parser.add_argument('-o', '--out', help='directory to store generated dummy images')
	args = parser.parse_args()
	out = args.out
	wbfile = args.workbook.name
	args.workbook.close()
	wb = xlrd.open_workbook(wbfile)
	images = set()
	for sheet in wb.sheets():
		for i in xrange(1, sheet.nrows):
			image = sheet.cell_value(i, 2).strip()
			if image:
				images.add(image)
	sys.stdout = codecs.getwriter(locale.getpreferredencoding())(sys.stdout)

	if out:
		shutil.rmtree(out, ignore_errors=True)	
		os.mkdir(out)
	for image in images:
		hs = '%s@2x.png' % image
		print(hs)
		if out:
			f = open(os.path.join(out, hs), 'w')
			f.close()

if __name__ == '__main__':
	main()
