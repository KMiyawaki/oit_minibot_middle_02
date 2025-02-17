#!/bin/bash

function main(){
    local -r TARGET_ROS=`./scripts/get_ros_distoro.sh`
    local -r ROS_SETUP="/opt/ros/${TARGET_ROS}/setup.bash"
    local -r WS_SETUP="${HOME}/catkin_ws/devel/setup.bash"
    source ${ROS_SETUP}
    source ${WS_SETUP}
    sudo apt install -y open-jtalk open-jtalk-mecab-naist-jdic hts-voice-nitech-jp-atr503-m001 alsa-utils
    
    cd ${HOME}/catkin_ws/src
    git clone https://github.com/ActiveIntelligentSystemsLab/japanese_tts_ros.git
    cd ${HOME}/catkin_ws
    catkin_make

    cd ${HOME}/catkin_ws/src/japanese_tts_ros
    wget https://sourceforge.net/projects/mmdagent/files/MMDAgent_Example/MMDAgent_Example-1.8/MMDAgent_Example-1.8.zip
    unzip MMDAgent_Example-1.8.zip
    rm -fr MMDAgent_Example-1.8.zip
}

main "$@"
