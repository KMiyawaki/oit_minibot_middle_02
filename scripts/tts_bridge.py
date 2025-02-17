#!/usr/bin/env python
# -*- coding: utf-8 -*-

import actionlib
import japanese_text_to_speech.msg
import rospy
from std_msgs.msg import String

simple_client = None
speed_rate = 1.0


def callback(msg):
    global simple_client
    rospy.loginfo('%s: recv speech request %s' % (rospy.get_name(), msg.data))
    rospy.loginfo('Sending goal to server')
    goal = japanese_text_to_speech.msg.SpeakGoal()
    goal.text = msg.data
    goal.speed_rate = speed_rate
    simple_client.send_goal_and_wait(goal)
    return


def main():
    global simple_client, speed_rate
    rospy.init_node('tts_bridge')
    action_name = rospy.get_param('~action_name', 'japanese_text_to_speech')
    speed_rate = rospy.get_param('~speed_rate', speed_rate)
    simple_client = actionlib.SimpleActionClient(
        action_name, japanese_text_to_speech.msg.SpeakAction)

    rospy.loginfo('Waiting japanese_text_to_speech server')
    simple_client.wait_for_server()
    rospy.loginfo('Connected to japanese_text_to_speech server')
    rospy.Subscriber('~speech', String, callback, queue_size=1)
    rospy.spin()


if __name__ == '__main__':
    main()
