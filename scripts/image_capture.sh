#!/bin/bash

function main(){
    local -r PACKAGE="oit_minibot_middle_02"
    local -r DIST=`${HOME}/catkin_ws/src/${PACKAGE}/scripts/get_ros_distoro.sh`
    source /opt/ros/${DIST}/setup.bash
    source ${HOME}/catkin_ws/devel/setup.bash
    source ${HOME}/catkin_ws/src/${PACKAGE}/scripts/settings.sh
    local -r IMAGE_DIR="${HOME}/catkin_ws/src/${PACKAGE}/camera_images"
    
    rosrun ${PACKAGE} image_capture.py
    pcmanfm ${IMAGE_DIR}
}

main "$@"
