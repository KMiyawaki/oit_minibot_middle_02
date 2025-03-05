#!/bin/bash
# sudo apt install ros-noetic-urdf-tutorial
function main(){
    cd "$(dirname "$0")"
    rosrun xacro xacro minibot_middle_02.xacro -o /tmp/robot.urdf
    roslaunch urdf_tutorial display.launch model:=/tmp/robot.urdf
}

main "$@"
