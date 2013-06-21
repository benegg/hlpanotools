#! /usr/bin/python
# coding:utf-8

import xlrd
import xlwt
import argparse
import os
import shutil
import base64


def _target(value):
	if os.path.isfile(value):
		return file(value, 'r') 
	elif os.path.isdir(value):
		return os.path.normpath(value)
	else:
		raise argparse.ArgumentTypeError('invalid path to target')

def genxls(f, path):
	wb = xlwt.Workbook(encoding='utf8')
	st = wb.add_sheet('vp-aera')
	st.write(0, 0, 'no.')
	st.write(0, 1, 'path')
	st.write(0, 2, 'name')
	st.srite(0, 3, 'tag')
	index = 0
	for line in f:
		line = line.strip()
		if line:
			index += 1
			values = line.split(' ')	
			st.write(index, 0, values[0])
			st.write(index, 1, values[1])
	wb.save(path)

def applyxls(dir, xlspath):
	wb = xlrd.open_workbook(xlspath)
	st = wb.sheet_by_name('vp-aera')	
	for i in xrange(1, st.nrows):
		no = st.cell_value(i, 0).strip()
		path = st.cell_value(i, 1).strip().encode('utf-8')
		name = st.cell_value(i, 2).strip()
		pano = '%s_%s.jpg' % (no, base64.urlsafe_b64encode(path))
		target_dir = os.path.join(dir, name)
		if not os.path.isdir(target_dir):
			os.mkdir(target_dir)
		pano_path = os.path.join(dir, pano) 
		shutil.move(pano_path, target_dir)
		print '%s -> %s' % (pano_path, target_dir)

def main():
	parser = argparse.ArgumentParser(description='panoramas to aera mapping')	
	parser.add_argument('target', type=_target, help='text file to generate xls from or panoramas directory to apply mapping to')
	parser.add_argument('-a', '--apply', action='store_true', help='group panoramas by aera')
	args = parser.parse_args()
	if not args.__dict__['apply']:
		genxls(args.target, 'vpmap.xls')
	else:
		applyxls(args.target, 'vpmap.xls')

if __name__ == '__main__':
	main()
