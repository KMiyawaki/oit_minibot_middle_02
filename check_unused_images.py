#!/usr/bin/env python
# -*- coding: utf-8 -*-
import glob
import re

def grep(path, word):
    result = []
    with open(path) as f:
        lines = f.readlines()
        for l in lines:
            l = l.strip()
            if word in l:
                start = l.find(word)
                l = './images/' + l[start + len(word) + 1:-1]
                result.append(l)
    return result

def main():
    files = glob.glob("./docs/*.md")
    used = []
    for file in files:
        add = grep(file, '../images')
        if add:
            used = used + add
    # print(used)
    crnts = glob.glob("./images/*.*")
    # print(crnts)
    for c in crnts:
        if c in used:
            continue
        print('rm -f', c)

if __name__ == '__main__':
    main()
