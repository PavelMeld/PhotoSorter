#!/usr/bin/python
# -*- coding: UTF-8 -*-
from PIL import Image
from PIL.ExifTags import TAGS
import enumerator

def get_exif(fn):
	ret = {}
	i = Image.open(fn)
	try:
		info = i._getexif();
	except AttributeError:
		return ret
		
	if info == None:
		return ret
	for tag, value in info.items():
		decoded = TAGS.get(tag, tag)
		ret[decoded] = value
	return ret

for filename in enumerator.enumerate('/home/mpv'):
	print filename
	try:
		info = get_exif(filename)
		if info.has_key('DateTimeOriginal'):
			print info['DateTimeOriginal']
		else:
			print 'No date in EXIF'
	except IOError:
		print 'no EXIF'
