#!/usr/bin/python
# -*- coding: UTF-8 -*-
from PIL import Image
from PIL.ExifTags import TAGS
import enumerator
import sys
import os
import re
import shutil
import avidate, movdate, mp4date

def getHumanSize(byteSize):
	if byteSize < 1024: 
		suffix = 'b';
		div = 1;
	elif byteSize < 1024 * 1024:
		suffix = 'kb'
		div = 1024
	elif byteSize < 1024 *1024*1024:
		suffix = 'Mb';
		div = 1024 * 1024;
	else:
		suffix = 'Gb';
		div = 1024 * 1024 * 1024
	return '{:.2f}{}'.format(1.0 * byteSize/div, suffix)

################################################################################
#
#
#	Get EXIF using PIL
#
#
################################################################################
def get_exif(fn):
	ret = {}
	i = Image.open(fn)
	try:
		info = i._getexif();
	except AttributeError:
		return None
		
	if info == None:
		return ret
	for tag, value in info.items():
		decoded = TAGS.get(tag, tag)
		ret[decoded] = value

	if ret.has_key('DateTimeOriginal')==False:
		return None;

	res = ret['DateTimeOriginal'];

	res = re.match('^([^\s]+)\s', res);
	if res == None:
		return None;

	res = re.sub(':', '_', res.group(1))
	res = re.sub('\000', '_', res)
	return res


if len(sys.argv)!=3:
	print "Usage: sorter.py <source> <destination>"
	sys.exit();

source 		= sys.argv[1];
destination = sys.argv[2];

print "Source      path '",source,"'";
print "Destination path '",destination,"'";


if os.path.exists(source) == False:
	print "Source dir", source," not exists!"
	sys.exit();

if os.path.exists(destination) == False:
	print "Destination dir", destination," not exists!"
	sys.exit();

totalBytes = 0

for filename in enumerator.enumerate(sys.argv[1]):
	name = os.path.basename(filename);
	ssize = os.path.getsize(filename)
	totalBytes += ssize
	namestart = os.path.splitext(name)[0]
	ext = os.path.splitext(name)[1]

	info = None;

	if re.search('\.jpg$',ext,re.I):
		try:
			info = get_exif(filename)
		except IOError:
			info = None;
	elif re.search('\.avi$',ext,re.I):
		info = avidate.read_avi_date(filename)
	elif re.search('\.mov$',ext,re.I):
		info = movdate.read_mov_date(filename)
	elif re.search('\.mp4$',ext,re.I):
		info = mp4date.read_mp4_date(filename)

	if info == None:
		dst = 'NOT_DATED';
	elif len(info) == 0:
		dst = 'NOT_DATED';
	else:
		dst = info;

	fulldest = os.path.join(destination, dst, name)
	destdir = os.path.join(destination, dst)

	print name,'->',fulldest, '(', getHumanSize(ssize),')'

	if os.path.exists(destdir) == False:
		print 'Creating directory ...'
		os.mkdir(destdir)

	n = 0
	while True:
		if os.path.exists(fulldest) == False:
			print 'Copying...'
			shutil.copy(filename, fulldest)
			break;

		ssize = os.path.getsize(filename)
		dsize = os.path.getsize(fulldest)

		if ssize == dsize:
			print 'File exists'
			break;

		fulldest = os.path.join(destination, dst, namestart+"_"+str(n)+ext)
		print 'File name is busy, trying', fulldest

		n = n + 1
	
	pass


print 'Total', totalBytes,' (', getHumanSize(totalBytes),')'
