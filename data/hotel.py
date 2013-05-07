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

out = 'hotel'

def get_pics_dir():
	return os.path.join(out, 'pics')

def clean():
	shutil.rmtree(out, ignore_errors=True)
	os.makedirs(get_pics_dir())

clean()
wb = xlrd.open_workbook('data.xls')
sheet = wb.sheet_by_name(u'住宿')

def copy_hotel_pic(name):
	src = u'pics/住宿/%s/shop.jpg' % name
	root, ext = os.path.splitext(src)
	dest = hashlib.md5(file(src, 'rb').read()).hexdigest() + ext
	shutil.copyfile(src, os.path.join(get_pics_dir(), dest))
	return dest

def copy_room_pic(hotel, room):
	src = u'pics/住宿/%s/房间/%s.jpg' % (hotel, room)
	root, ext = os.path.splitext(src)
	dest = hashlib.md5(file(src, 'rb').read()).hexdigest() + ext
	shutil.copyfile(src, os.path.join(get_pics_dir(), dest))
	return dest

def get_hotel(hotels, name):
	return next(hotel for hotel in hotels if hotel['name'] == name)
	
hotels = []
for i in xrange(1, sheet.ncols):
	col = sheet.col_values(i)
	hotel = {}	
	hotel['name'] = col[0].strip()
	hotel['star'] = int(col[2])
	hotel['address'] = col[4]
	hotel['tel'] = col[5]
	hotel['pic'] = copy_hotel_pic(hotel['name'])
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
	room['pic'] = copy_room_pic(hotel, room['type'])
	hotel = get_hotel(hotels, hotel)
	hotel['rooms'].append(room)	

with codecs.open(os.path.join(out, 'hotel.json'), 'w', encoding='utf-8') as fp:
	escaped_content = json.dumps(hotels, indent=4)
	fp.write(escaped_content.decode('unicode-escape'))

