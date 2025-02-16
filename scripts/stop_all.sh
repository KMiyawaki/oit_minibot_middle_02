#!/bin/bash

function main(){
    local -r PACKAGE="oit_minibot_middle_02"
    local -r DIST=`${HOME}/catkin_ws/src/${PACKAGE}/scripts/get_ros_distoro.sh`
    source /opt/ros/${DIST}/setup.bash
    source ${HOME}/catkin_ws/devel/setup.bash
    source ${HOME}/catkin_ws/src/${PACKAGE}/scripts/settings.sh

    ${HOME}/catkin_ws/src/${PACKAGE}/scripts/stop_recording.sh

    echo "Kill all ros nodes!"
    rosnode list | awk '{ print "rosnode kill", $1 }' | sh
    while true
    do
        rosnode list | grep -v rosout > /dev/null
        if [ $? -ne 0 ]; then
            echo "Killed all ros nodes."
            break
        fi
        echo "Waiting for terminating all ros nodes... Do not close. Do not press Ctrl+C."
        sleep 1
    done
    echo "Close roscore"
    ps aux | grep ros | grep -v grep | awk '{ print "kill -9", $2 }' | sh
    echo "Close terminals"
    ps aux | grep xterm | grep -v grep | awk '{ print "kill -9", $2 }' | sh
    echo "Done"
}

main "$@"
