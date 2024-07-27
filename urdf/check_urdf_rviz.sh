#!/bin/bash
rosrun xacro xacro --inorder minibot_middle_02.xacro -o /tmp/robot.urdf
roslaunch urdf_tutorial display.launch model:=/tmp/robot.urdf
