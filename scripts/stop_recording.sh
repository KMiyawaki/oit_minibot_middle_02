#!/bin/bash

function main() {
    local -r PACKAGE="oit_minibot_middle_02"
    local -r DIST=`${HOME}/catkin_ws/src/${PACKAGE}/scripts/get_ros_distoro.sh`
    source /opt/ros/${DIST}/setup.bash
    source ~/catkin_ws/devel/setup.bash
    source ${HOME}/catkin_ws/src/${PACKAGE}/scripts/settings.sh
    rosnode list|grep -q record
    if [ $? -eq 1 ]; then
        echo "rosbag record is not running. exit."
        return 0
    fi

    local -r BAG_ORG="$HOME/.ros"
    local -r BAG_FILTER="${BAG_ORG}/`date --iso-8601`-*.bag"
    local -r PKG=`rospack find ${PACKAGE}`
    local -r BAG_DST="${PKG}/bags"
    local -r PID=`rosnode info /record 2>/dev/null|grep Pid|cut -d' ' -f2`
    rosnode kill /record
    echo "Waiting for killing rosbag record PID=${PID}..."
    while true
    do
        ps -p ${PID}  --no-headers|grep ${PID} > /dev/null
        if [ $? -ne 0 ]; then
            echo "rosbag recording has stopped."
            break
        fi
        echo "Waiting for terminating rosbag record... Do not close. Do not press Ctrl+C."
        sleep 3
    done
}

main "$@"
