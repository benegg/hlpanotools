#! /usr/bin/python

import argparse
import os
import xlwt
import xlrd
import json
import itertools
import codecs

aeras = ['Chu xi', 'Gao bei', 'Hong keng', 'Nan xi']

def _dir(path):
	if not os.path.isdir(path):
		raise argparse.ArgumentTypeError('%s is not a directory' % path)
	else:
		return path

def main():
	parser = argparse.ArgumentParser(description='generate hotspot mapping')
	parser.add_argument('-a', '--add', action='store_true', help='add image info from hotspot mapping')
	parser.add_argument('dir', type = _dir, help='root Tour3D directory contains hotspot info')
	args = parser.parse_args()

	dir = args.dir
	xls = 'hsmap.xls'

	if args.add:
		apply_mapping(dir, xls)
	else:
		gen_mapping(dir, xls)

def gen_mapping(dir, xls):
	wb = xlwt.Workbook(encoding='utf8')
	for aera in aeras:
		st = wb.add_sheet(aera)
		st.write(0, 0, 'from')
		st.write(0, 1, 'to')
		st.write(0, 2, 'image')
		index = 1
		for dirpath, dirnames, filenames in os.walk(os.path.join(dir, aera)):
			for filename in filenames:
				if filename.endswith('.json'):
					with open(os.path.join(dirpath, filename), 'r') as fp:
						content = json.load(fp, encoding='utf8')
						fname = os.path.splitext(filename)[0]
						for hs in content['hotspots']:
							tname = os.path.splitext(hs['href'])[0]
							st.write(index, 0, fname)
							st.write(index, 1, tname)
							index += 1
	wb.save(xls)

def find_image(image_list, tname):
	return next(itertools.ifilter(lambda x: x[0] == tname, image_list), None)[1]

def apply_mapping(dir, xls):
	wb = xlrd.open_workbook(xls)
	hsdict = {}
	for aera in aeras:
		st = wb.sheet_by_name(aera)
		for i in xrange(1, st.nrows):
			fname = st.cell_value(i, 0)
			tname = st.cell_value(i, 1)
			image = st.cell_value(i, 2)
			jsonfile = os.path.join(dir, aera, fname + '.json')
			if not hsdict.has_key(jsonfile):
				hsdict[jsonfile] = [(tname, image)]
			else:
				hsdict[jsonfile].append((tname, image))	
	for item in hsdict.items():
		jsonfile = item[0]
		with open(jsonfile, 'r') as fp:	
			content = json.load(fp, encoding='utf8')
		for hs in content['hotspots']:
			tname = os.path.splitext(hs['href'])[0]
			image = find_image(item[1], tname)
			if image is None:
				print 'no image info for %s' % tname 
			else:
				hs['image'] = 'hs%s.png' % image
				print '%s <- %s' % (tname, hs['image'])
		with codecs.open(jsonfile, 'w', encoding='utf8') as fp:
			value = json.dumps(content, indent=4, separators=(',', ': '))
			fp.write(value.decode('unicode-escape'))

if __name__ == '__main__':
	main()
