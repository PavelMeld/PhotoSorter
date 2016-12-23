#!/bin/sh

if [ ! -f mts/avchd2srt-core ] ; then 
	echo "Compiling MTS subtitle extractor"
	make -C mts
fi
