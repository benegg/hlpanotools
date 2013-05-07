#! /bin/bash

dirs=`ls virgin.flat`

for dir in ${dirs[*]};do
	newfile=./pano.flat/$dir.jpg
	echo $newfile 
	touch $newfile
done
