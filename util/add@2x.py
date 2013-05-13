#! /usr/bin/python

import os

for dirpath, dirnames, filenames in os.walk('.'):
	for filename in filenames:
		if filename.endswith('.png'):
			filename2x = filename[:-4] + '@2x.png'
			print filename2x
			os.rename(filename, filename2x)
