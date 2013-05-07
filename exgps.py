#! /usr/bin/python
#coding=utf-8

from xml.etree import ElementTree as et
import argparse
import os
import sys
import sqlite3
import xlwt

KMLNS = '{http://earth.google.com/kml/2.0}' 

def _parse_file(path):
	placemarks = []
	root = et.parse(path)
	aera = root.find("%sDocument/%sname" % (KMLNS, KMLNS)).text;
	xml_placemarks = root.findall("%sDocument/%sFolder[1]/%sPlacemark" % (KMLNS, KMLNS, KMLNS))
	for xml_placemark in xml_placemarks:
		desc = xml_placemark.find("%sdescription" % KMLNS).text
		coord = xml_placemark.find("%sPoint/%scoordinates" % (KMLNS, KMLNS)).text
		desc_sections = desc.splitlines()
		if desc_sections[1]:
			accuracy = desc_sections[-1][4:-2]
			names = desc_sections[1:-4]
			name = '|'.join(names)
			if name[-1] == '|':
				name = name[0:-1]
			coord_sections = coord.split(',')
			lng = coord_sections[0];
			lat = coord_sections[1];
			alt = coord_sections[2];
			placemark = {'name':name, 'lat':float(lat), 'lng':float(lng), 'alt':float(alt), 'accuracy':float(accuracy), 'aera':aera}	
			placemarks.append(placemark)
	return placemarks

def _parse_dir(path):
	for dirpath, dirnames, filenames in os.walk(path):
		placemarks = []
		for filename in filenames:
			filepath = os.path.join(dirpath, filename)
			placemarks.extend(_parse_file(filepath))	
	return placemarks

def _parse_placemarks(path):
	return _parse_dir(path) if os.path.isdir(path) else _parse_file(path)

def _exported_info(path):
	print 'GPS extracted to %s.' % path

def _write_db(placemarks, path):
	db = sqlite3.connect(path)
	c = db.cursor()
	c.execute('drop table if exists placemark')
	c.execute('create table placemark (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, lat REAL, lng REAL, alt REAL, accuracy REAL, aera TEXT)')
	for placemark in placemarks:
		c.execute('insert into placemark (name, lat, lng, alt, accuracy, aera) values (?, ?, ?, ? ,?, ?)', (placemark['name'], placemark['lat'], placemark['lng'], placemark['alt'], placemark['accuracy'], placemark['aera']))
	db.commit()
	db.close()
	_exported_info(path)

def _write_xls(placemarks, path):
	workbook = xlwt.Workbook(encoding='utf-8')
	sheet = workbook.add_sheet('placemarks')
	sheet.write(0, 0, 'name')
	sheet.write(0, 1, 'altitude')
	sheet.write(0, 2, 'longitude')
	sheet.write(0, 3, 'latitude')
	sheet.write(0, 4, 'acurracy')
	sheet.write(0, 5, 'aera')
	for i, placemark in enumerate(placemarks):
		index = i + 1
		sheet.write(index, 0, placemark['name'])
		sheet.write(index, 2, placemark['lat'])	
		sheet.write(index, 3, placemark['lng'])	
		sheet.write(index, 1, placemark['alt'])
		sheet.write(index, 4, placemark['accuracy'])	
		sheet.write(index, 5, placemark['aera'])
	workbook.save(path)	
	_exported_info(path)

def main():
	parser = argparse.ArgumentParser(description='parse geo locations from kml')	
	parser.add_argument('-f', '--format', choices=['xls', 'sqlite'], default='xls', help='output format')
	parser.add_argument('target', help='kml file or directory')
	parser.add_argument('-p', '--preview', action='store_true', help='preview after extraction')
	args = parser.parse_args()
	if not os.path.exists(args.target):
		print 'invalid path: %s' % args.target
	else:
		placemarks = _parse_placemarks(args.target)
		target = os.path.normpath(args.target)
		dir, name = os.path.split(target)
		if (os.path.isfile(target)):
			name, ext = os.path.splitext(name)
		if (args.format == 'xls'):
			path = os.path.join(dir, '%s.xls' % name)
			_write_xls(placemarks, path)
			if args.preview:
				os.system('open %s' % path)
		else:
			path = os.path.join(dir, '%s.db' % name)
			_write_db(placemarks, path)

if __name__ == '__main__':
	main()
