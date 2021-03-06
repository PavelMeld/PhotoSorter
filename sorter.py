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
import mtsdate
import argparse

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
# Returns True incase file dest_dir/fname exists and has sieze fsize
#
#
################################################################################
def file_exists(dest_dir, fname, fext, fsize):
	suff = "";
	n = 0;
	while True:
		testdest = os.path.join(dest_dir, fname + suff + fext)

		if os.path.exists(testdest) == False:
			return False;


		dsize = os.path.getsize(testdest)
		if fsize == dsize:
			print "File exists";
			return True;

		suff = "_" + str(n);
		n = n + 1;

	return False;

################################################################################
#
#
# Returns List of dirs with name dirname*
#
#
################################################################################
def get_candidate_dirs(root, dirname, verbose = False):
	return enumerator.enumerate_similar_dirs(root, dirname, verbose);

################################################################################
#
#
#		Get EXIF using PIL
#
#
################################################################################
def get_exif(fn):
	ret = {}
	i = Image.open(fn)
	try:
		info = i._getexif();
	except :
		return None
			
	if info == None:
		return None;
	for tag, value in info.items():
		decoded = TAGS.get(tag, tag)
		ret[decoded] = value

	if ret.has_key('DateTimeOriginal')==False:
		return None;

	res = ret['DateTimeOriginal'];

	print "jdt", res,

	res = re.match('^([^\s]+)\s', res);
	if res == None:
		return None;

	res = re.sub(':', '_', res.group(1))
	res = re.sub('\000', '_', res)
	return res


cmd = argparse.ArgumentParser(description='PhotoSorter')
cmd.add_argument("-m", "--mode", default="copy", choices=['copy', 'test']);
cmd.add_argument("source");
cmd.add_argument("destination");

args = cmd.parse_args();

source			= args.source;
destination		= args.destination
mode			= args.mode;
test			= False;

if mode != 'copy':
	test = True;

print "Source	   path '",source,"'";
print "Destination path '",destination,"'";


if os.path.exists(source) == False:
	print "Source dir", source," not exists!"
	sys.exit();

if mode != 'test':
	if os.path.exists(destination) == False:
		print "Destination dir", destination," not exists!"
		sys.exit();

totalBytes = 0


for filename in enumerator.enumerate_media_files(source, verbose=test):

	if test:
		print "Reading info of " + filename,

	name = os.path.basename(filename)
	file_size = os.path.getsize(filename)
	totalBytes += file_size
	namestart = os.path.splitext(name)[0]
	ext = os.path.splitext(name)[1]

	info = None;

	#
	# Essential date extraction
	#
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
	elif re.search('\.mts$',ext,re.I):
		info = mtsdate.read_mts_date(filename)
	
	
	# 
	# Name-based date extraction
	#

	if info == None or info == "1904_01_01":
		whatsapp = re.search('(?:img|vid)-(\d{4})(\d{2})(\d{2})-wa', filename, re.I) 
		if whatsapp:
			info = whatsapp.group(1) + "_" + whatsapp.group(2) + "_" + whatsapp.group(3);
	

	#
	# If still nothing
	#
	if info == None:
		dst = 'NOT_DATED';
	elif len(info) == 0:
		dst = 'NOT_DATED';
	else:
		dst = info;

	if test:
		print " done, dst is ", dst;

	if test:
		print "Getting candidate list",
	default_dest_dir = os.path.join(destination, dst)
	candidates		 = get_candidate_dirs(destination, dst, test);
	candidates.append(default_dest_dir);

	if test:
		print "done",

	print filename,

	if mode == 'test':
		print " testing", 

	for testdir in candidates:
		if file_exists(testdir, namestart, ext, file_size):
			print "found in " + testdir;
			break;
	else:
		# Copying
		fulldest = os.path.join(default_dest_dir, name)

		if mode == 'test':
			print " skipped"
			continue;

		print '->',fulldest, '(', getHumanSize(file_size),')'

		if os.path.exists(default_dest_dir) == False:
			print 'Creating directory ... '+default_dest_dir
			os.mkdir(default_dest_dir)
			enumerator.update_similar_dirs_cache(destination, dst);

		n = 0
		while True:
			if os.path.exists(fulldest) == False:
				print 'Copying...'
				shutil.copy(filename, fulldest)
				break;

			fulldest = os.path.join(default_dest_dir, name)
			fulldest = os.path.join(default_dest_dir, namestart+"_"+str(n)+ext)
			print 'File name is busy, trying', fulldest

			n = n + 1


print 'Total', totalBytes,' (', getHumanSize(totalBytes),')'
