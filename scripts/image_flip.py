#!/usr/bin/env python
# -*- coding: utf_8 -*-

import os

import cv2
import rospy
from cv_bridge import CvBridge
from sensor_msgs.msg import Image


class ImageFlip(object):
    def __init__(self):
        self.pub_image = rospy.Publisher('~image_out', Image, queue_size=1)
        self.sub_image = rospy.Subscriber(
            '~image_in', Image, self.on_msg, queue_size=1)
        self.bridge = CvBridge()

    def on_msg(self, msg):
        img = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
        img_flip = cv2.flip(img, 0)
        msg = self.bridge.cv2_to_imgmsg(img_flip, 'bgr8')
        self.pub_image.publish(msg)


def main():
    script_name = os.path.basename(__file__)
    node_name = os.path.splitext(script_name)[0]
    rospy.init_node(node_name)
    node = ImageFlip()
    rospy.loginfo("Start %s", node_name)
    rospy.spin()
    rospy.loginfo("Exiting %s", node_name)


if __name__ == '__main__':
    main()
