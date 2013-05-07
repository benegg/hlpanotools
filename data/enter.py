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

out = 'enter'

def get_pics_dir():
	return os.path.join(out, 'pics')

def clean():
	shutil.rmtree(out, ignore_errors=True)
	os.makedirs(get_pics_dir())

clean()
wb = xlrd.open_workbook('data.xls')
sheet = wb.sheet_by_name(u'娱乐')

def copy_shop_pic(name):
	src = u'pics/娱乐/%s/shop.jpg' % name
	root, ext = os.path.splitext(src)
	dest = hashlib.md5(file(src, 'rb').read()).hexdigest() + ext
	shutil.copyfile(src, os.path.join(get_pics_dir(), dest))
	return dest

shops = []
for i in xrange(1, sheet.nrows):
	row = sheet.row_values(i)
	shop = {}
	shop['name'] = row[0]
	shop['address'] = row[3]
	shop['tel'] = row[4]
	shop['pic'] = copy_shop_pic(shop['name'])
	lat, lng = row[5].split(',')
	shop['latitude'], shop['longitude'] = float(lat), float(lng)
	shop['price'] = int(row[6])
	shop['mark'] = float(row[7])
	shop['comments'] = [re.sub(u'^点评\\d+：', '', line) for line in row[8].strip().splitlines()]
	shops.append(shop)
	#print(shop)

with codecs.open(os.path.join(out, 'enter.json'), 'w', encoding='utf-8') as fp:
	escaped_content = json.dumps(shops, indent=4)
	fp.write(escaped_content.decode('unicode-escape'))

