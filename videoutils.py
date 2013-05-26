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
		num |= ord(data[n]) << n*8
	return num;

########################################################################
##
##
##	Function reads LITTLE endian data into Intel-oriented variables
##
##
########################################################################
def read_littleend(file, bitsize=32):
	cnt = bitsize/8
	data = file.read(cnt);
	num = 0
	for n in range(0,cnt):
		num<<=8
		num|=ord(data[n])
	return num;
