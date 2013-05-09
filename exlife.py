#! /usr/bin/python
# -*-coding:utf-8-*-

import xlrd
import json
import codecs
import shutil
import os
import re
import base64
import hashlib
import argparse

def _dir(path):
	if not os.path.isdir(path):
		raise argparse.ArgumentTypeError('%s is not a directory' % path)
	else:
		return path	

def _get_pics_dir(out):
	return os.path.join(out, 'pics')

def _get_xls(dir):
	return os.path.join(dir, 'data.xls')	

def _clean(out):
	shutil.rmtree(out, ignore_errors=True)
	os.makedirs(_get_pics_dir(out))

def _copy_shop_pic(dir, out, category, name):
	src = u'%s/pics/%s/%s/shop.jpg' % (dir, category, name)
	root, ext = os.path.splitext(src)
	dest = hashlib.md5(file(src, 'rb').read()).hexdigest() + ext
	shutil.copyfile(src, os.path.join(_get_pics_dir(out), dest))
	return dest

def _write_json(obj, jsonfile):
	with codecs.open(jsonfile, 'w', encoding='utf-8') as fp:
		escaped_content = json.dumps(obj, indent=4)
		fp.write(escaped_content.decode('unicode-escape'))

def _extract_enter(dir, out, jsonfile):
	wb = xlrd.open_workbook(_get_xls(dir))
	sheet = wb.sheet_by_name(u'娱乐')
	shops = []
	for i in xrange(1, sheet.nrows):
		row = sheet.row_values(i)
		shop = {}
		shop['name'] = row[0]
		shop['address'] = row[3]
		shop['tel'] = row[4]
		shop['pic'] = _copy_shop_pic(dir, out, u'娱乐', shop['name'])
		lat, lng = row[5].split(',')
		shop['latitude'], shop['longitude'] = float(lat), float(lng)
		shop['price'] = int(row[6])
		shop['mark'] = float(row[7])
		shop['comments'] = [re.sub(u'^点评\\d+：', '', line) for line in row[8].strip().splitlines()]
		shops.append(shop)
	_write_json(shops, os.path.join(out, jsonfile))


def _copy_dish_pic(dir, out, shop_name, name):
	src = u'%s/pics/美食/%s/菜/%s.jpg' % (dir, shop_name, name)
	root, ext = os.path.splitext(src)
	dest = hashlib.md5(file(src, 'rb').read()).hexdigest() + ext
	shutil.copyfile(src, os.path.join(_get_pics_dir(out), dest))
	return dest

def _extract_dishes(dir, out, shop_name, dishes_str):
	dishes = []
	names = dishes_str.split(',')
	for name in names:
		pic = _copy_dish_pic(dir, out, shop_name, name)
		dish = {}
		dish['name'] = name
		dish['pic'] = pic
		dishes.append(dish)
	return dishes

def _extract_food(dir, out, jsonfile):
	wb = xlrd.open_workbook(_get_xls(dir))
	sheet = wb.sheet_by_name(u'美食')
	shops = []
	for i in xrange(1, sheet.nrows):
		row = sheet.row_values(i)
		shop = {}	
		shop['name'] = row[0]
		shop['address'] = row[3]
		shop['tel'] = row[4]
		shop['pic'] = _copy_shop_pic(dir, out, u'美食', shop['name'])
		lat, lng = row[5].split(',')
		shop['latitude'], shop['longitude'] = float(lat), float(lng)
		shop['price'] = int(row[6])
		shop['mark'] = float(row[7])
		dishes_str = row[8].strip()
		shop['recommended_dishes'] = _extract_dishes(dir, out, shop['name'], dishes_str)			
		shop['comments'] = [re.sub(u'^点评\\d+：', '', line) for line in row[9].strip().splitlines()]
		shops.append(shop)
	_write_json(shops, os.path.join(out, jsonfile))

def _copy_room_pic(dir, out, hotel, room):
	src = u'%s/pics/住宿/%s/房间/%s.jpg' % (dir, hotel, room)
	root, ext = os.path.splitext(src)
	dest = hashlib.md5(file(src, 'rb').read()).hexdigest() + ext
	shutil.copyfile(src, os.path.join(_get_pics_dir(out), dest))
	return dest

def _get_hotel(hotels, name):
	return next(hotel for hotel in hotels if hotel['name'] == name)
	
def _extract_hotel(dir, out, jsonfile):
	wb = xlrd.open_workbook(_get_xls(dir))
	sheet = wb.sheet_by_name(u'住宿')
	hotels = []
	for i in xrange(1, sheet.ncols):
		col = sheet.col_values(i)
		hotel = {}	
		hotel['name'] = col[0].strip()
		hotel['star'] = int(col[2])
		hotel['address'] = col[4]
		hotel['tel'] = col[5]
		hotel['pic'] = _copy_shop_pic(dir, out, u'住宿', hotel['name'])
		lat, lng = col[6].split(',')
		hotel['latitude'], hotel['longitude'] = float(lat), float(lng)
		hotel['price'] = int(col[7])
		hotel['mark'] = float(col[8])
		hotel['comments'] = [re.sub(u'^点评\\d+：', '', line) for line in col[9].strip().splitlines()]
		hotel['rooms'] = []
		hotels.append(hotel)

	for i in xrange(14, sheet.nrows):
		room = {}
		row = sheet.row_values(i)
		room['type'] = row[0]
		room['price'] = int(row[1])
		room['remark'] = row[2]
		hotel = row[3].strip()
		room['pic'] = _copy_room_pic(dir, out, hotel, room['type'])
		hotel = _get_hotel(hotels, hotel)
		hotel['rooms'].append(room)
	_write_json(hotels, os.path.join(out, jsonfile))


def _extract_info(dir, out):
	_extract_enter(dir, out, 'enter.json')		
	_extract_hotel(dir, out, 'hotel.json')
	_extract_food(dir, out, 'food.json')

def main():
	parser = argparse.ArgumentParser(description='extract life info')
	parser.add_argument('dir', type=_dir, help='directory which contains information')
	parser.add_argument('-o', '--output', default='life', help='output directory')
	args = parser.parse_args()
	out = args.output
	_clean(out)
	_extract_info(args.dir, out)	

if __name__ == '__main__':
	main()
