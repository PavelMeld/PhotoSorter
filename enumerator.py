#!/usr/bin/python
import os
import re

def enumerate(root):
	result = os.walk(root)
	for diritem in result:
		for filename in diritem[2]:
			if not re.search('\.(:?(jpg)|(mov)|(avi)|(mp4)|(mts))$',filename, re.I):
				continue
			full_name = os.path.join(diritem[0],filename)
			yield full_name
