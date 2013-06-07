#! /usr/bin/env python
# coding:utf-8

import xlrd
import argparse
import sys
import codecs

def dump(xls, isheet):
	sys.stdout = codecs.getwriter('utf8')(sys.stdout)
	wb = xlrd.open_workbook(xls)
	st = wb.sheet_by_index(isheet)
	for i in xrange(st.nrows):
		for j in xrange(st.ncols):
			cell = st.cell_value(i, j)
			if not cell:
				cell = '<null>'
			print cell,
		print ''

def main():
	parser = argparse.ArgumentParser(description='dump xls content')
	parser.add_argument('xls', help='xls to dump')
	parser.add_argument('-i', '--index', type=int, default=0, help='sheet index')
	args = parser.parse_args()
	dump(args.xls, args.index)

if __name__ == '__main__':
	main()
