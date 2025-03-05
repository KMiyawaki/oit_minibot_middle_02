#!/bin/bash
# sudo apt-get install liburdfdom-tools
function main(){
    cd "$(dirname "$0")"
    rosrun xacro xacro minibot_middle_02.xacro -o /tmp/robot.urdf
    check_urdf /tmp/robot.urdf
}

main "$@"
