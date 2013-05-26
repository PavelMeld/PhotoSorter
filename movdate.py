#!/usr/bin/python
import sys
import os
from videoutils import read_littleend, get_1904_date

########################################################################
##
##
##						Recursive MOV file processing
##
##
########################################################################
def trace_atom(handle):
	atom_start = handle.tell();				# Getting size of current atom
	handle.seek(0,os.SEEK_END);
	file_end   = handle.tell();

	handle.seek(atom_start,os.SEEK_SET);
	size = 1
	
	while size>0:							# Tracing current atom
		atom_start = handle.tell();
		size = read_littleend(handle);			# atom size
		fourcc =handle.read(4);				# atom type

		if size == 1:
			size = read_littleend(handle);
			full_size = size;
			full_size<<=32;
			size = read_littleend(handle);
			full_size |= size;
		else:
			full_size = size;
		# try to find internal atoms
		if fourcc=="moov" or fourcc == "trak" or fourcc=="mdia":           
			res = trace_atom(handle);
			if res != None:
				return res;
		if fourcc=="mdhd":
			cryation_date = read_littleend(handle);	 # skipping 4 bytes
			creation_date = read_littleend(handle);     # reading 4 bytes of date
			exif_date = get_1904_date(creation_date)
			return exif_date
		handle.seek(atom_start + size,os.SEEK_SET);
		if handle.tell() == file_end:
			break

	return None;


########################################################################
#
#
#						Read Date from MOV
#
#
########################################################################
def read_mov_date(fileName):
	try:
		h = open(fileName,"rb");
	except IOError:
		print "File '{}' not found".format(fileName)
		return None;

	print "Reading file '{}'".format(fileName)
	res = trace_atom(h);
	h.close();
	return res


if __name__ == "__main__":
	if len(sys.argv)<2:
		print "Syntax: movdate.py <mov file>"
	else:
		res = read_mov_date(sys.argv[1])
		if res != None:
			print res
		
