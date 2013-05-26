#!/usr/bin/python
import sys
import os
from videoutils import read_littleend, get_1904_date

########################################################################
##
##
##						Recursive MP4 file processing
##
##
########################################################################
def trace_box(handle, stop_pos = None):
	start = handle.tell()
	handle.seek(0,os.SEEK_END);
	file_end   = handle.tell();
	handle.seek(start,os.SEEK_SET);

	if stop_pos == None:
		stop_pos = file_end;

	while handle.tell() < stop_pos:
		box_start = handle.tell()
		last_box = 0;
		if box_start >= file_end:
			break;

		size = read_littleend(handle, 32)
		name = handle.read(4)

		if size == 1:
			size = read_littleend(handle, 64)
			print 'Reading extended size'
		elif size == 0:
			size = stop_pos - box_start
			last_box = 1

		if name=='uuid':
			name = file.read(16)
			print 'Reading extended name'

		print 'Box {} size {} bytes'.format(name,size)

		if name=='moov':
			res = trace_box(handle, box_start+size)
			if res != None:
				return res

		if name=='mvhd': # Extends FullBox
			ver   = handle.read(1)
			flags = read_littleend(handle, 24)
			ver = ord(ver)
			if ver ==0:
				time = read_littleend(handle, 32)
			else:
				time = read_littleend(handle, 64)
			return get_1904_date(time)



		handle.seek(box_start + size,os.SEEK_SET);

		if last_box:
			break;

	return None
	

########################################################################
#
#
#						Read Date from MP4
#
#
########################################################################
def read_mp4_date(fileName):
	try:
		h = open(fileName,"rb");
	except IOError:
		print "File '{}' not found".format(fileName)
		return None;

	print "Reading file '{}'".format(fileName)
	res = trace_box(h);
	h.close();
	return res

if __name__ == "__main__":
	if len(sys.argv)<2:
		print "Syntax: mp4date.py <mp4 file>"
	else:
		res = read_mp4_date(sys.argv[1])
		if res != None:
			print res
