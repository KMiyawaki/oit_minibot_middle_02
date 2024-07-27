#!/usr/bin/env python
# -*- coding: utf_8 -*-

import os
import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge


class PiCamera(object):
    def __init__(self):
        self.cap = cv2.VideoCapture(rospy.get_param("~device", 0))
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, rospy.get_param("~width", 640))
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT,
                     rospy.get_param("~height", 480))
        self.cap.set(cv2.CAP_PROP_FPS, rospy.get_param("~fps", 640))
        self.pub_image = rospy.Publisher('~image', Image, queue_size=1)
        self.bridge = CvBridge()

    def spin(self):
        ret, frame = self.cap.read()
        if ret and frame is not None:
            msg = self.bridge.cv2_to_imgmsg(frame, 'bgr8')
            self.pub_image.publish(msg)

    def __del__(self):
        self.cap.release()


def main():
    script_name = os.path.basename(__file__)
    node_name = os.path.splitext(script_name)[0]
    rospy.init_node(node_name)
    process_rate = rospy.get_param("~process_rate", 30.0)
    node = PiCamera()
    rate = rospy.Rate(process_rate)
    rospy.loginfo("Start %s with process rate %f Hz",
                  node_name, process_rate)

    while not rospy.is_shutdown():
        node.spin()
        rate.sleep()
    rospy.loginfo("Exiting %s", node_name)


if __name__ == '__main__':
    main()
