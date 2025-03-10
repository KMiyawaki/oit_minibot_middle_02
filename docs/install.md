- 前 [他のソフトのインストール方法](./install_tools.md)
- [トップページに戻る](../README.md)

---

# システムのインストール方法

ロボットには動作に必要なソフトが全てインストールされているため、通常はこの手順を実施する必要はありませんが、参考資料として付録に入れています。

リポジトリをクローンしモータコントローラや`LiDAR`のソフト等をインストール・セットアップします。

```shell
cd ~/catkin_ws/src
git clone https://github.com/KMiyawaki/oit_minibot_middle_02.git
cd ~/catkin_ws/src/oit_minibot_middle_02
./install.sh
./install_ydlidar.sh
cd ~/catkin_ws/src/ydlidar_ros_driver/startup
sudo initenv.sh
sudo reboot
```

設定ファイルを置きます。

```shell
roscd oit_minibot_middle_02/script
emacs settings.sh
```

以下を貼り付けます。

その後、コメントにある通り、`~/.bashrc`の末尾に`source ${HOME}/catkin_ws/src/oit_minibot_middle_02/scripts/settings.sh`の一行を貼り付けます。

```shell
# Add the following line to the bottom of ~/.bashrc
# source ${HOME}/catkin_ws/src/oit_minibot_middle_02/scripts/settings.sh

export OIT_MINIBOT_MIDDLE_02_TELEOP="joy"
export OIT_MINIBOT_MIDDLE_02_JOY="/dev/input/by-id/usb-Logicool_Logicool_Cordless_RumblePad_2-joystick"
export OIT_MINIBOT_MIDDLE_02_ROBOCLAW="/dev/ttyAMA1"
export OIT_MINIBOT_MIDDLE_02_YDLIDAR="/dev/ttyAMA2" # USB接続時は "/dev/ydlidar"
export OIT_MINIBOT_MIDDLE_02_CREATE_STAGE=1
export OIT_MINIBOT_MIDDLE_02_STOP_RECORDING=0
export OIT_MINIBOT_MIDDLE_02_CAMERA_FLIP="true"
export OIT_MINIBOT_MIDDLE_02_CAMERA_DEVICE_ID="0"
export OIT_MINIBOT_MIDDLE_02_CAMERA_RATE="15"
export OIT_MINIBOT_MIDDLE_02_CAMERA_IMAGE_WIDTH="640"
export OIT_MINIBOT_MIDDLE_02_CAMERA_IMAGE_HEIGHT="480"
export OIT_MINIBOT_MIDDLE_02_USE_TTS="true"
```

サンプルプログラムをコピーします。

```shell
cp ~/catkin_ws/src/oit_minibot_middle_02/samples/* ~/catkin_ws/src/beginner_tutorials/scripts/
```

---

- 前 [他のソフトのインストール方法](./install_tools.md)
- [トップページに戻る](../README.md)
