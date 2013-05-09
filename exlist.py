#! /usr/bin/python
# coding:utf8

import os
import base64
import argparse
import shutil
import xlrd
import json
import codecs

def _dir(dirpath):
	if not os.path.isdir(dirpath):
		raise argparse.ArgumentTypeError('%s is not a directory' % dirpath)
	else:
		return dirpath

def _get_pics_dir(dirpath):
	return os.path.join(dirpath, 'pics')

def _clean(dirpath):
	shutil.rmtree(dirpath, ignore_errors=True)
	os.makedirs(_get_pics_dir(dirpath))

def _copyicon(indir, outdir, name):
	src = os.path.join(_get_pics_dir(indir), u'景点', name + '.jpg')
	if os.path.exists(src):
		shutil.copyfile(src, _get_pics_dir(outdir))
	else:
		src = os.path.join(_get_pics_dir(indir), u'景点', name, name + '.jpg')
		shutil.copyfile(src, os.path.join(_get_pics_dir(outdir), name + '.jpg'))

def main():
	parser = argparse.ArgumentParser(description='list view points')
	parser.add_argument('indir', type=_dir, help='directory contains attractions\' info')	
	parser.add_argument('-o', '--outdir', default='buildings', help='output directory')
	args = parser.parse_args()
	_clean(args.outdir)
	wb = xlrd.open_workbook(os.path.join(args.indir, 'data.xls'))
	st = wb.sheet_by_name(u'景点')
	items = []
	for i in xrange(1, st.nrows):
		item = {}
		item['name'] = st.cell_value(i, 0)
		item['icon'] = item['name']
		_copyicon(args.indir, args.outdir, item['name'])
		item['desc'] = st.cell_value(i, 1)
		items.append(item)
	d = {}
	d['items'] = items
	jsonfile = os.path.join(args.outdir, 'buildings.json')
	with codecs.open(jsonfile, 'w', encoding='utf-8') as fp:
		escaped_content = json.dumps(d, indent=4)
		fp.write(escaped_content.decode('unicode-escape'))

if __name__ == '__main__':
	main()
