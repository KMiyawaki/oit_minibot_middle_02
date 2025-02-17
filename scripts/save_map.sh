#!/bin/bash

function main(){
    local -r PACKAGE="oit_minibot_middle_02"
    local -r DIST=`${HOME}/catkin_ws/src/${PACKAGE}/scripts/get_ros_distoro.sh`
    source /opt/ros/${DIST}/setup.bash
    source ${HOME}/catkin_ws/devel/setup.bash
    source ${HOME}/catkin_ws/src/${PACKAGE}/scripts/settings.sh
    
    local -r MAP_NAME="`date '+%Y%m%d_%H%M%S'`"
    local -r MAP_DIR="${HOME}/catkin_ws/src/${PACKAGE}/maps/${MAP_NAME}"
    mkdir ${MAP_DIR}
    rosrun map_server map_saver -f ${MAP_NAME}
    mv ${MAP_NAME}.pgm ${MAP_NAME}.yaml ${MAP_DIR}
    if [ ${OIT_MINIBOT_MIDDLE_02_CREATE_STAGE} -eq 1 ]; then
        echo "Create Stage simulation world"
        cd "${HOME}/catkin_ws/src/${PACKAGE}/maps"
        ./make_stage_world.sh ./${MAP_NAME}/${MAP_NAME}.yaml 
    fi
    pcmanfm ${MAP_DIR}
}

main "$@"
