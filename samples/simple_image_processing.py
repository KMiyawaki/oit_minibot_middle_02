#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from threading import Lock

import cv2
import rospy
from cv_bridge import CvBridge
from sensor_msgs.msg import Image

cv_bridge = CvBridge()


def get_cv_img_from_image_msg(msg):
    global cv_bridge
    return cv_bridge.imgmsg_to_cv2(msg, "bgr8")


class SensorMessageGetter(object):
    def __init__(self, topic, msg_type, msg_converter):
        self.msg_converter = msg_converter
        self.lock = Lock()
        self.msg = None
        self.sub = rospy.Subscriber(topic, msg_type, self.on_msg)

    def on_msg(self, msg):
        self.lock.acquire()
        self.msg = msg
        self.lock.release()

    def get(self):
        val = None
        self.lock.acquire()
        if self.msg is not None:
            val = self.msg_converter(self.msg)
        self.lock.release()
        return val


def extract_color(time_limit, range=[(90, 80, 80), (120, 255, 255)], image='/image'):
    func = sys._getframe().f_code.co_name
    rospy.loginfo('Executing ' + func)
    pub = rospy.Publisher(image + '_out', Image, queue_size=10)
    time = 0
    start_time = rospy.get_time()
    sensor_msg = SensorMessageGetter(image, Image, get_cv_img_from_image_msg)
    disp_rate = 0.5  # 表示倍率
    cv2.namedWindow('result')

    # 一定時間画像処理する
    while time < time_limit:
        cv_img = sensor_msg.get()
        if cv_img is not None:
            hsv = cv2.cvtColor(cv_img, cv2.COLOR_BGR2HSV)  # HSV 形式に変換
            area = cv2.inRange(hsv, range[0], range[1])
            result = cv_img.copy()
            result[area > 128] = [255, 255, 255]  # 抽出できた範囲を白で塗りつぶす
            cv2.imshow('result', cv2.resize(
                result, None, fx=disp_rate, fy=disp_rate))
        time = rospy.get_time() - start_time
        cv2.waitKey(10)  # 10ミリ秒待つ。OpenCVではこの関数を呼ばないと画面更新されない


def main():
    script_name = os.path.basename(__file__)
    node_name = os.path.splitext(script_name)[0]
    rospy.init_node(node_name)
    rospy.sleep(1)
    extract_color(30)


if __name__ == '__main__':
    main()
