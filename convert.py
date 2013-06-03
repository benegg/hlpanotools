#! /usr/bin/python

import os
import xml.etree.ElementTree as ET
import shutil
import json
import argparse

def get_scene_href(root, linkedscene):
	for scene in root.findall('scene'):
		title = scene.attrib['title']
		name = scene.attrib['name']
		if name.lower() == linkedscene.lower():
			return title
	
def convert(dir, outdir, larger):
	root = ET.parse(os.path.join(dir, 'tour.xml'))
	surfixes = ['r', 'l', 'u', 'd', 'f', 'b']

	for scene in root.findall('scene'):
		prefix = scene.attrib['title']
		print('processing %s' % prefix)
		cube = scene.find('image/cube').attrib['url'] if larger else scene.find('image/mobile/cube').attrib['url']
		j = dict()

		images = ['%s_%s.jpg' % (prefix, surfix) for surfix in surfixes]
		j['images'] = images
	
		view = scene.find('view')
		camera = dict()
		camera['ath'] = float(view.attrib['hlookat'])
		camera['atv'] = float(view.attrib['vlookat'])
		camera['fov'] = float(view.attrib['fov'])
		j['camera'] = camera

		hotspots = []
		for hs in scene.findall('hotspot'):
			hotspot = dict()
			hotspot['ath'] = float(hs.attrib['ath'])
			hotspot['atv'] = float(hs.attrib['atv'])
			hotspot['height'] = 0.08
			hotspot['width'] = 0.08
			linkedscene = hs.attrib['linkedscene']
			hotspot['href'] = '%s.json' % get_scene_href(root, linkedscene)
			hotspot['image'] = '';
			hotspots.append(hotspot)
		j['hotspots'] = hotspots

		content = json.dumps(j, indent=4, separators=(',', ': ')) 
		f = open('%s/%s.json' % (outdir, prefix), 'w')
		f.write(content)
		for surfix in surfixes:
			src = os.path.join(dir, cube % surfix)
			dest = '%s/%s_%s.jpg' % (outdir, prefix, surfix)
			print src
			shutil.copyfile(src, dest)

def main():
	parser = argparse.ArgumentParser(description='convert tour to dev format')	
	parser.add_argument('tour', help='tour directory')
	parser.add_argument('-x', '--larger', action='store_true', default=False, help='generate 2048x2048 images')
	args = parser.parse_args()	
	ndir = os.path.normpath(args.tour)
	outdir = "%s/%s" % ('dev', os.path.split(ndir)[1])
	shutil.rmtree(outdir, ignore_errors=True)
	os.makedirs(outdir)
	convert(ndir, outdir, args.larger)

if __name__ == '__main__':
	main()
