#! /usr/bin/python

import argparse
import os
import xlrd
import json
import codecs

def main():
	parser = argparse.ArgumentParser(description='gather hotspot image list')
	parser.add_argument('workbook', type=file, help='workbook contains hotspot image info')
	args = parser.parse_args()
	wbfile = args.workbook.name
	args.workbook.close()
	wb = xlrd.open_workbook(wbfile)
	images = set()
	for sheet in wb.sheets():
		for i in xrange(1, sheet.nrows):
			image = sheet.cell_value(i, 2).strip()
			if image:
				images.add(image)
	for image in images:
		print('hs%s.png' % image)

if __name__ == '__main__':
	main()
