#!/usr/bin/python
import os
import re

def enumerate_by_mask(root, mask, what="files"):
    res = [];
    result = os.walk(root)

    for diritem in result:
        (search_path, dir_list, file_list) = diritem

        if what == "files":
            items = file_list;
        if what == "dirs":
            items = dir_list;

        for filename in items:
            if not re.search(mask, filename, re.I):
                continue;
            full_path = os.path.join(diritem[0], filename);
            res.append(full_path);
    return res;

def enumerate_similar_dirs(root, dirname):
    return enumerate_by_mask(root, dirname+".*", "dirs");


def enumerate_media_files(root):
    return enumerate_by_mask(root, '\.(:?(jpg)|(mov)|(avi)|(mp4)|(mts))$');
