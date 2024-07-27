#!/bin/bash
rosrun xacro xacro --inorder minibot_middle_02.xacro -o /tmp/robot.urdf
check_urdf /tmp/robot.urdf
