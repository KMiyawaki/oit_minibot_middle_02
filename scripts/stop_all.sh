#!/bin/bash

function main(){
    $HOME/catkin_ws/src/oit_minibot_middle_02/scripts/stop_recording.sh
    echo "Kill all ros nodes!"
    ps aux | grep ros | grep -v grep | awk '{ print "kill -9", $2 }' | sh
}

main "$@"
