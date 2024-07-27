#!/bin/bash

function main(){
    local -r PACKAGE="oit_minibot_middle_02"
    local -r DIST=`${HOME}/catkin_ws/src/${PACKAGE}/scripts/get_ros_distoro.sh`
    source /opt/ros/${DIST}/setup.bash
    source ${HOME}/catkin_ws/devel/setup.bash
    source ${HOME}/catkin_ws/src/${PACKAGE}/scripts/settings.sh
    
    local -r MAP_NAME="map_`date '+%Y%m%d_%H%M%S'`"
    rosrun map_server map_saver -f ${MAP_NAME}
    mv ${MAP_NAME}.pgm ${MAP_NAME}.yaml ~/catkin_ws/src/${PACKAGE}/maps
    pcmanfm ~/catkin_ws/src/${PACKAGE}/maps
}

main "$@"
