#!/usr/bin/python

import os
import sys
import re
import struct
from videoutils import read_bigend

strd_result = None

########################################################################
##
##
##	Function parses date string from AVI file according some format
##
##
########################################################################
def parse_idit_date(idit_date):
	month =[ "Jan", "Feb", "Mar", "Apr", 
			 "May", "Jun", "Jul", "Aug",
			 "Sep", "Oct", "Nov", "Dec"];
	fmt = re.search('\w+\s+(\w+)\s+(\d+)\s+[0-9:]+\s+(\d+)', idit_date);
	#				 ---    --- 	---      ---      ---
	#		Day Name -'      |	     |    	  |		   |
	#			 Month Name -'	     |	     Time     Year
	#			    	  Day number-'
	if fmt==None:
		return None;

	mnth  = month.index(fmt.group(1)) + 1
	year  = fmt.group(3)
	day   = fmt.group(2)

	return "{}_{:02}_{}".format(year, mnth, day)

########################################################################
##
##
##	Function parses date string from AVI file according some format
##		* FUJI_F30
##
##
########################################################################
def parse_strd_date(strd_data):
	res = re.search('(\d{4}:\d{2}:\d{2}) \d{2}:\d{2}:\d{2}', strd_data)
	if res == None:
		return None
	
	res = re.sub(':','_', res.group(1))
	return res

########################################################################
##
##
##					Recursive AVI List processing
##
##
########################################################################
def read_list_data(handle, end_pos, level):
	pos= handle.tell()
	prefix = '\t'*level;

	while pos<end_pos:
		fcc  = handle.read(4)
		try:
			size = read_bigend(handle)
		except IndexError:
			print 'Can\'t read size, fcc is ', fcc
			return None

		if fcc=='LIST':
			list_end = handle.tell() + size 
			ltype  = handle.read(4)
			print prefix, 'LIST type = ', ltype,' size = ', size

			res = read_list_data(handle, list_end, level + 1)
			if res != None:							# Date was found
				return res;

		else:
			print prefix,'Chunk ', fcc, 'Size is ', size;
			chunk_end = handle.tell() + size

			if fcc == 'IDIT':				# Usual date chunk
				res = handle.read(size)
				print ' IDIT style info found :', res
				return parse_idit_date(res)

			if fcc == 'strd':				# Codec-specific data
				res = handle.read(size)
				date = parse_strd_date(res)
				if date != None:
					global strd_result
					print prefix,' Codec style info found'
					strd_result = date

			handle.seek(chunk_end, os.SEEK_SET)
			if handle.tell()%2:
				handle.seek(1, os.SEEK_CUR)

		pos = handle.tell()


	return None
########################################################################
##
##
##						Read Date from AVI
##
##
########################################################################
def	read_avi_date(fileName):
	global strd_result

	try:
		h = open(fileName,"rb");
	except IOError:
		print "File '{}' not found".format(fileName)
		return None;

	strd_result = None;

	print "Reading file '{}'".format(fileName)

#hdr  - AVIRIFFHEADER
#	FOURCC riff;
#	32BIT  size;
#   FOURCC ftype;

#chunk- AVICHUNK
#    FOURCC fcc;
#    DWORD  size;

	fcc  = h.read(4);					# Main header
	size = read_bigend(h);
	ftype= h.read(4);

	if fcc != 'RIFF':
		print 'Not a RIFF file'
		h.close()
		return None
	print 'RIFF file, type {}'.format(ftype)

	start = h.tell()
	h.seek(0, os.SEEK_END)
	end_pos = h.tell()
	h.seek(start, os.SEEK_SET)

	result = read_list_data(h,end_pos, 0)
	h.close()

	if result == None:					# we either have IDIT or strd
		return strd_result				# information
	
	return result

if __name__ == "__main__":
	if len(sys.argv)<2:
		print "Syntax: avidate.py <mov file>"
	else:
		res = read_avi_date(sys.argv[1])
		if res != None:
			print res
		
