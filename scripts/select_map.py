#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import os
import sys

import roslib.packages


def main(launch):
    pkg_name = 'oit_minibot_middle_02'
    path = roslib.packages.get_pkg_dir(pkg_name) + '/maps/'
    map_data = glob.glob(path + '**/*.yaml', recursive=True)
    if not map_data:
        print('マップがありません')
        return
    for i, m in enumerate(map_data):
        map_data[i] = m.replace(path, '').replace('.yaml', '')
    map_data.sort(reverse=True)
    for i, m in enumerate(map_data):
        print("[%2d] %s" % (i, m))
    idx = 0
    if len(map_data) > 1:
        print('マップ番号を 0 -- %d で入力してください。それ以外の番号でキャンセルします' %
              (len(map_data) - 1))
        idx = int(input('番号？ > '))
        if idx < 0 or len(map_data) <= idx:
            return
    command = 'roslaunch %s %s map_name:=%s' % (
        pkg_name, launch, map_data[idx])
    os.system(command)


if __name__ == '__main__':
    launch = 'navigation.launch'
    if len(sys.argv) > 1:
        launch = 'stage_navigation.launch'
    main(launch)
