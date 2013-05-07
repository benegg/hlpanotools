#! /usr/bin/python
# coding=utf-8

import json
import codecs
import argparse
import xlwt
import os

def info(file):
	print('attractions extracted to %s' % file)

def _write_txt(content, filename):
	with codecs.open('%s.txt' % filename, 'w', encoding='utf-8') as fp:
		for item in content['items']:
			name = item['name']	
			desc = item['desc']
			line = '%s: %s' % (name, desc)
			fp.write(line + '\n')
		info('%s.txt' % filename)

def _write_xls(content, filename):
	wb = xlwt.Workbook(encoding='utf-8')	
	sheet = wb.add_sheet(u'景点')
	sheet.write(0, 0, u'名称')
	sheet.write(0, 1, u'文字介绍')
	for i, item in enumerate(content['items']):
		sheet.write(i + 1, 0, item['name'])
		sheet.write(i + 1, 1, item['desc'])
	wb.save('%s.xls' % filename)
	info('%s.xls' % filename)

def main():
	parser = argparse.ArgumentParser(description='extract attractions infomation')
	parser.add_argument('-f', '--format', choices=['xls', 'txt'], default='txt', help='specify output format')
	parser.add_argument('-o', '--output', help='output file name')
	parser.add_argument('file', type=argparse.FileType('r'))
	args = parser.parse_args()
	if args.output is None:
		args.output = args.file.name
	filename,ext = os.path.splitext(args.output)
	content = json.load(args.file)
	_write_xls(content, filename) if args.format == 'xls' else _write_txt(content, filename)

if __name__ == '__main__':
	main()
