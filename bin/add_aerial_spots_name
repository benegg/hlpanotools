#! /usr/bin/env python
# coding:utf-8

import xlrd
import json
import argparse
import codecs

def get_spot_name(raw_name):
	raw_name = raw_name.strip()
	name = raw_name[1:-1] + u'景区' if raw_name.startswith('[') else raw_name
	return name

def gather_spots_info(xls):
	wb = xlrd.open_workbook(xls)
	st = wb.sheet_by_index(0)
	d = {}
	for i in xrange(1, st.nrows):
		spot_name = get_spot_name(st.cell_value(i, 0)).strip()
		spot_id_str = st.cell_value(i, 3)
		if spot_id_str:
			spot_id = int(spot_id_str)
			d[spot_id] = spot_name
	return d

def add_name(pano, dic):
	with codecs.open(pano, 'r', encoding='utf-8') as fp:
		data = json.load(fp, encoding='utf-8')
		hotspots = data['hotspots']
		for hotspot in hotspots:
			href = hotspot['href']
			sid = int(href[0:3])
			hotspot['image'] = hotspot['image'].replace('hotspots', 'landmarks')
			if dic.has_key(sid):
				name = dic[sid]
				hotspot['name'] = name
				print '%s -> %s' % (name, href)
			else:
				print 'spot name for %s not found' % href
	with codecs.open(pano, 'w', encoding='utf-8') as fp: 
		escaped_content = json.dumps(data, indent=4, separators=(',', ': ')) 
		fp.write(escaped_content.decode('unicode-escape'))

def main():
	parser = argparse.ArgumentParser(description='add aerial spots name')
	parser.add_argument('spots', type=file, help='workbook contains spots information')
	parser.add_argument('panos', nargs='+', help='aerial pano json')
	args = parser.parse_args()
	d = gather_spots_info(args.spots.name)
	for pano in args.panos:
		add_name(pano, d)

if __name__ == '__main__':
	main()
