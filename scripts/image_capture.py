#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

import cv2
import roslib.packages
import rospy
import sensor_msgs
from cv_bridge import CvBridge, CvBridgeError


class SensorMessageGetter(object):
    def __init__(self, topic, msg_type, msg_wait=1.0):
        self.msg_wait = msg_wait
        self.topic = topic
        self.msg_type = msg_type

    def get_msg(self):
        message = None
        try:
            message = rospy.wait_for_message(
                self.topic, self.msg_type, self.msg_wait)
        except rospy.exceptions.ROSException as e:
            rospy.logdebug(e)
        return message


def main():
    rospy.init_node('image_capture')
    topic_name = rospy.get_param('~topic_name', '/image')
    file_name = rospy.get_param('~file_name', '')
    time_limit = rospy.get_param('~time_limit', 3)
    pkg_name = 'oit_minibot_middle_02'
    dir = roslib.packages.get_pkg_dir(pkg_name) + '/camera_images/'

    bridge = CvBridge()
    msg_getter = SensorMessageGetter(
        topic_name, sensor_msgs.msg.Image, time_limit)
    msg = msg_getter.get_msg()
    if msg:
        try:
            cv_image = bridge.imgmsg_to_cv2(msg, 'bgr8')
            if file_name == '':
                d = datetime.datetime.now()
                file_name = d.strftime('%Y%m%d_%H%M%S.jpg')
            cv2.imwrite(dir + file_name, cv_image)
            rospy.loginfo("Saved %s", file_name)
        except CvBridgeError as e:
            print(e)
    else:
        rospy.logerr("Time out")


if __name__ == '__main__':
    main()
