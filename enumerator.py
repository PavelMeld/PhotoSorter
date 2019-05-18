#!/usr/bin/python
import os
import re

g_cache = {};

def enumerate_by_mask_cached(cached, mask, what="files", verbose=False):
	res = []
	for filename in cached:
		if not re.search(mask, filename, re.I):
			continue;
		res.append(filename);
	return res;


def enumerate_by_mask(root, mask, what="files", verbose=False):
	res = [];

	if verbose:
		print "Getting file list at "+root,
	result = os.walk(root)
	if verbose:
		print " done"

	if verbose:
		print "Sorting items ",

	cache = [];

	for diritem in result:
		(search_path, dir_list, file_list) = diritem

		if what == "files":
			items = file_list;
		if what == "dirs":
			items = dir_list;

		for filename in items:
			full_path = os.path.join(diritem[0], filename);
			cache.append(full_path);
			if not re.search(mask, filename, re.I):
				continue;
			res.append(full_path);

	if verbose:
		print " done"

	return (res, cache);


def enumerate_similar_dirs(root, dirname, verbose=False):
	if g_cache.has_key(root):
		if verbose:
			print "Found cached "+root;
		return enumerate_by_mask_cached(g_cache[root], dirname+".*", "dirs", verbose)
	
	if verbose:
		print "Wait a minute, filling directory cache ..."

	(res, cache) = enumerate_by_mask(root, dirname+".*", "dirs", verbose);
	g_cache[root] = cache;

	return res;


def update_similar_dirs_cache(root, dirname, verbose=False):
	if g_cache.has_key(root) == True and not dirname in g_cache[root]:
		g_cache[root].append(dirname);



def enumerate_media_files(root, verbose=False):
	return enumerate_by_mask(root, '\.(:?(jpg)|(mov)|(avi)|(mp4)|(mts))$', "files", verbose)[0]
