#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import os
import sys
from threading import Lock

import actionlib
import rospy
from angles import normalize_angle
from geometry_msgs.msg import Pose2D, Twist
from japanese_text_to_speech.msg import SpeakAction, SpeakGoal
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion


def get_theta(odom):
    q = (odom.pose.pose.orientation.x,
         odom.pose.pose.orientation.y,
         odom.pose.pose.orientation.z,
         odom.pose.pose.orientation.w)
    euler = euler_from_quaternion(q)
    return euler[2]


def get_pose_from_odom(odom):
    pose = Pose2D()
    pose.x = odom.pose.pose.position.x
    pose.y = odom.pose.pose.position.y
    pose.theta = get_theta(odom)
    return pose


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


def go_straight_by_time(time_limit, linear_vel, cmd_vel="/cmd_vel"):
    func = sys._getframe().f_code.co_name
    rospy.loginfo('Executing ' + func)
    pub = rospy.Publisher(cmd_vel, Twist, queue_size=10)
    vel = Twist()
    vel.linear.x = linear_vel
    vel.angular.z = 0
    time = 0
    start_time = rospy.get_time()
    rate = rospy.Rate(20)  # 20Hzでループを回す
    while time < time_limit:
        pub.publish(vel)
        time = rospy.get_time() - start_time
        rospy.loginfo('%.2f sec', time)
        rate.sleep()
    vel.linear.x = 0
    vel.angular.z = 0
    pub.publish(vel)


def turn_by_time(time_limit, angular_vel, cmd_vel="/cmd_vel"):
    func = sys._getframe().f_code.co_name
    rospy.loginfo('Executing ' + func)
    pub = rospy.Publisher(cmd_vel, Twist, queue_size=10)
    vel = Twist()
    vel.linear.x = 0
    vel.angular.z = angular_vel
    time = 0
    start_time = rospy.get_time()
    rate = rospy.Rate(20)  # 20Hzでループを回す
    while time < time_limit:
        pub.publish(vel)
        time = rospy.get_time() - start_time
        rospy.loginfo('%.2f sec', time)
        rate.sleep()
    vel.linear.x = 0
    vel.angular.z = 0
    pub.publish(vel)


def go_straight_by_odom(distance, linear_vel, time_limit=999, odom='/odom', cmd_vel="/cmd_vel"):
    func = sys._getframe().f_code.co_name
    rospy.loginfo('Executing ' + func)
    pub = rospy.Publisher(cmd_vel, Twist, queue_size=10)
    vel = Twist()
    vel.linear.x = linear_vel
    vel.angular.z = 0
    time = 0
    start_time = rospy.get_time()
    rate = rospy.Rate(20)  # 20Hzでループを回す

    sensor_msg = SensorMessageGetter(odom, Odometry, get_pose_from_odom)
    start_pose = None

    # 初期位置が得られるまで待機する
    while time < time_limit and start_pose is None:
        start_pose = sensor_msg.get()
        rate.sleep()

    # 所定の距離を移動するまで速度指令を送信する
    while time < time_limit:
        pose = sensor_msg.get()
        dx = pose.x - start_pose.x
        dy = pose.y - start_pose.y
        moved = math.hypot(dx, dy)
        rospy.loginfo(
            'Odom pose(x, y, theta)=(%.2f, %.2f, %.2f) %.2f/%.2f', pose.x, pose.y, math.degrees(pose.theta), moved, distance)
        if moved < distance:
            pub.publish(vel)
            time = rospy.get_time() - start_time
            rate.sleep()
        else:
            break
    vel.linear.x = 0
    vel.angular.z = 0
    pub.publish(vel)


def turn_by_odom(angle, angular_vel, time_limit=999, odom='/odom', cmd_vel="/cmd_vel"):
    func = sys._getframe().f_code.co_name
    rospy.loginfo('Executing ' + func)
    pub = rospy.Publisher(cmd_vel, Twist, queue_size=10)
    vel = Twist()
    vel.linear.x = 0
    vel.angular.z = angular_vel
    time = 0
    start_time = rospy.get_time()
    rate = rospy.Rate(20)  # 20Hzでループを回す

    sensor_msg = SensorMessageGetter(odom, Odometry, get_pose_from_odom)
    pre_pose = None
    moved = 0

    # 初期位置が得られるまで待機する
    while time < time_limit and pre_pose is None:
        pre_pose = sensor_msg.get()
        rate.sleep()

    # 所定の距離を移動するまで速度指令を送信する
    while time < time_limit:
        pose = sensor_msg.get()
        dtheta = abs(normalize_angle(pose.theta - pre_pose.theta))
        pre_pose = pose
        moved = moved + dtheta
        rospy.loginfo(
            'Odom pose(x, y, theta)=(%.2f, %.2f, %.2f) %.2f/%.2f', pose.x, pose.y, math.degrees(pose.theta),
            math.degrees(moved), math.degrees(angle))
        if moved < angle:
            pub.publish(vel)
            time = rospy.get_time() - start_time
            rate.sleep()
        else:
            break
    vel.linear.x = 0
    vel.angular.z = 0
    pub.publish(vel)


def text_to_speech(ac, text, speed_rate=1.0, time_limit=20):
    goal = SpeakGoal()
    goal.text = text
    goal.speed_rate = speed_rate
    ac.send_goal(goal)
    ac.wait_for_result(rospy.Duration(time_limit))


def main():
    script_name = os.path.basename(__file__)
    node_name = os.path.splitext(script_name)[0]
    rospy.init_node(node_name)
    rospy.sleep(1)

    # 音声合成用 Action Client
    ac_tts = actionlib.SimpleActionClient(
        'japanese_text_to_speech', SpeakAction)
    while not ac_tts.wait_for_server(rospy.Duration(5)):
        rospy.loginfo(
            'Waiting for the japanese_text_to_speech action server to come up')
    rospy.loginfo('The japanese_text_to_speech server comes up')

    # 広いところで実行すること
    # 一定時間走る
    text_to_speech(ac_tts, '動きます！')
    go_straight_by_time(3.0, 0.15)
    turn_by_time(3.0, math.radians(30))
    turn_by_time(3.0, math.radians(-30))
    go_straight_by_time(3.0, -0.15)
    # オドメトリ情報を使って走る
    text_to_speech(ac_tts, '動きます！')
    go_straight_by_odom(0.6, 0.2)
    turn_by_odom(math.radians(90), math.radians(30))
    turn_by_odom(math.radians(90), math.radians(-30))
    go_straight_by_odom(0.6, -0.2)
    text_to_speech(ac_tts, '終わります！')


if __name__ == '__main__':
    main()
