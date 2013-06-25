#! /usr/bin/env python

import xlwt
import xlrd
import xlutils
import argparse
from xlutils.copy import copy

def getlist(path):
	l = []
	wb = xlrd.open_workbook(path)
	st = wb.sheet_by_index(0)
	for i in xrange(st.nrows):
		value = st.cell_value(i, 0)
		l.append(value.strip())
	return l

def add_marks(xls, spots_to_show):
	rb = xlrd.open_workbook(xls)
	rs = rb.sheet_by_index(0)
	wb = copy(rb)
	ws = wb.get_sheet(0)
	for i in xrange(1, rs.nrows):
		spot = rs.cell_value(i, 0)
		if spot in spots_to_show:
			ws.write(i, 4, 'Y')
			spots_to_show.remove(spot)
			print 'mark %s' % spot
	if spots_to_show:
		for i in xrange(1, rs.nrows):
			spot = rs.cell_value(i, 0)
			if spot in spots_to_show:
				ws.write(i, 4, 'Y')
				spots_to_show.remove(spot)
				print 'mark %s' % spot
	wb.save(xls)

def main():
	parser = argparse.ArgumentParser(description='add mark to the spot shown in list') 
	parser.add_argument('-l', '--list', type=file, required=True, help='spots to show in list')
	parser.add_argument('xls', type=file, help='workbook to edit')
	args = parser.parse_args()
	spots_to_show = getlist(args.list.name)
	add_marks(args.xls.name, spots_to_show)
	if spots_to_show:
		spots_to_show = ['[%s]' % i for i in spots_to_show]
		add_marks(args.xls.name, spots_to_show)
		if spots_to_show:
			print '%d spots not found' % len(spots_to_show)
			for spot in spots_to_show:
				print spot[1:-1].encode('utf-8')
	

if __name__ == '__main__':
	main()
