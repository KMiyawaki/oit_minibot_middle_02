#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import os


def main():
    user = os.environ.get("USER")
    map_data = glob.glob(
        '/home/' + user + '/catkin_ws/src/oit_minibot_middle_02/maps/*.yaml')

    print('select map')
    for i in range(0, len(map_data)):
        map_data[i] = map_data[i].replace(
            '/home/' + user + '/catkin_ws/src/oit_minibot_middle_02/maps/', '')
        map_data[i] = map_data[i].replace('.yaml', '')
        print(str(i) + " " + map_data[i])

    a = int(input('> '))

    os.system(
        'roslaunch oit_minibot_middle_02 navigation.launch map_name:=' + map_data[a])


if __name__ == '__main__':
    main()
