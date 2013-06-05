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
	
def convert(dir, outdir, smaller):
	root = ET.parse(os.path.join(dir, 'tour.xml'))
	surfixes = ['r', 'l', 'u', 'd', 'f', 'b']

	for scene in root.findall('scene'):
		prefix = scene.attrib['title']
		print('processing %s' % prefix)
		cube = scene.find('image/mobile/cube').attrib['url'] if smaller else scene.find('image/cube').attrib['url'] 
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
			shutil.copyfile(src, dest)

def main():
	parser = argparse.ArgumentParser(description='convert tour to dev format')	
	parser.add_argument('tour', help='tour directory')
	parser.add_argument('-s', '--smaller', action='store_true', default=False, help='generate smaller cube images')
	args = parser.parse_args()	
	ndir = os.path.normpath(args.tour)
	outdir = '%s.dev' % os.path.splitext(ndir)[0]
	shutil.rmtree(outdir, ignore_errors=True)
	os.makedirs(outdir)
	convert(ndir, outdir, args.smaller)

if __name__ == '__main__':
	main()
