#!/usr/bin/python
import sys
import os

LEAP_YEAR_SECONDS  = (366*24*60*60)
USUAL_YEAR_SECONDS = (365*24*60*60)

########################################################################
##
##
##						Get date from seconds since 1#1#1904
##
##
########################################################################
month_days = [31,28,31,30,31,30,31,31,30,31,30,31];
#	           J   F  M  A  M Jn Jl  A  S  O  N  D

def get_1904_date(seconds):

	y = 1904;
	leap = 0;			# 1904 was a leap year

	while True:
		if leap == 0:
			year_seconds = LEAP_YEAR_SECONDS;
		else:
			year_seconds = USUAL_YEAR_SECONDS;

		if seconds>=LEAP_YEAR_SECONDS:
			if leap == 0:
				leap = 3;
			else:
				leap-=1
			seconds -= year_seconds;
			y += 1
			continue;

		if leap == 0:
			month_days[1] = 29;
		else:
			month_days[1] = 28;

		for m in range(0,12):
			if seconds>= month_days[m] * 24*60*60:
				seconds-=(month_days[m] * 24*60*60);
			else:
				break;

		d = seconds/(24*60*60);

		break;

	return "{:04}_{:02}_{:02}".format(y,m+1,d+1)

########################################################################
##
##
##	Function reads BIG endian data into Intel-oriented variables
##
##
########################################################################
def read_bigend(file):
	data = file.read(4);
	num=0;
	for n in range(0,4):
		num<<=8;
		num |= ord(data[n]);
	return num;

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
		size = read_bigend(handle);			# atom size
		fourcc =handle.read(4);				# atom type

		if size == 1:
			size = read_bigend(handle);
			full_size = size;
			full_size<<=32;
			size = read_bigend(handle);
			full_size |= size;
		else:
			full_size = size;
		# try to find internal atoms
		if fourcc=="moov" or fourcc == "trak" or fourcc=="mdia":           
			res = trace_atom(handle);
			if res != None:
				return res;
		if fourcc=="mdhd":
			creation_date = read_bigend(handle);	 # skipping 4 bytes
			creation_date = read_bigend(handle);     # reading 4 bytes of date
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
		print "Syntax: videodate.py <avi/mov file>"
	else:
		res = read_mov_date(sys.argv[1])
		if res != None:
			print res
		
