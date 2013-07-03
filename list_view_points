#! /usr/bin/python

import os
import base64
import argparse
import xlwt

def _dir(path):
	if not os.path.isdir(path):
		raise argparse.ArgumentTypeError('%s is not a directory' % path)
	else:
		return path

def _addrow(st, index, no, route):
	st.write(index, 0, no)
	st.write(index, 1, route)	

def _list(dir, toxls):
	if toxls:
		wb = xlwt.Workbook(encoding='utf-8') 
		st = wb.add_sheet('list')
		st.write(0, 0, 'no')
		st.write(0, 1, 'route')
		st.write(0, 2, 'name')
		st.write(0, 3, 'tag')
		index = 1;
	for dirpath, dirnames, filenames in os.walk(dir):
		for filename in sorted(filenames):
			if not filename.startswith('.'):
				no = filename[0:3]
				name, ext = os.path.splitext(filename[4:])
				route = base64.urlsafe_b64decode(name)
				if toxls:
					_addrow(st, index, no, route)
					index += 1
				else:
					line = '%s %s' % (no, route)
					print(line)
		for dirname in dirnames:
			no = dirname[0:3]
			route = base64.urlsafe_b64decode(dirname[4:])
			if toxls:
				_addrow(st, index, no, route)
				index += 1
			else:
				line = '%s %s' % (no, route)
				print(line)
	if toxls:
		wb.save('list.xls')


def main():
	parser = argparse.ArgumentParser(description='list view points')
	parser.add_argument('dir', type=_dir, help='directory to list')	
	parser.add_argument('-x', '--xls', action="store_true", help='output to xls')
	args = parser.parse_args()
	_list(args.dir, args.xls)

if __name__ == '__main__':
	main()
