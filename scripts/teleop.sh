#!/bin/bash

function main(){
    local -r PACKAGE="oit_minibot_middle_02"
    local -r DIST=`${HOME}/catkin_ws/src/${PACKAGE}/scripts/get_ros_distoro.sh`
    source /opt/ros/${DIST}/setup.bash
    source ${HOME}/catkin_ws/devel/setup.bash
    source ${HOME}/catkin_ws/src/${PACKAGE}/scripts/settings.sh
    if [ `rosnode list|grep oit_roboclaw_driver` ]; then
        roslaunch ${PACKAGE} teleop_select.launch
    else
        roslaunch ${PACKAGE} teleop.launch
    fi
}

main "$@"
