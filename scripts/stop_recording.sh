#!/bin/bash

function main() {
    local -r DIST=`~/catkin_ws/src/oit_minibot_middle_02/scripts/get_ros_distoro.sh`
    source /opt/ros/${DIST}/setup.bash
    source ~/catkin_ws/devel/setup.bash
    source ~/.bashrc
    local -r BAG_ORG="$HOME/.ros"
    local -r BAG_FILTER="${BAG_ORG}/`date --iso-8601`-*.bag"
    local -r PKG=`rospack find oit_minibot_middle_02`
    local -r BAG_DST="${PKG}/bags"

    while true
    do
        rosnode list|grep record > /dev/null
        if [ $? -ne 0 ]; then
            echo "rosbag recording has stopped."
            break
        fi
        rosnode kill /record
        echo "Waiting for killing rosbag record..."
        sleep 1
    done
    local -r BAGS=`find ${BAG_FILTER}`
    for bag in ${BAGS}
    do
        com="mv ${bag} ${BAG_DST}"
        echo ${com}
        eval ${com}
        sleep 1
    done
}

main "$@"
