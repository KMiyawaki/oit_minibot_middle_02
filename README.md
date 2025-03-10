# Minibot middle ver.2 の使い方

演習用小型ロボット`Minibot middle ver.2`（以降単に「ロボット」と表記します）の使い方です。

本ドキュメントをよく読んでロボットをお使いください。

## 目次

- [ロボットの構成](./docs/structure.md)
- [ロボットの電源を入れる](./docs/power_on.md)
- [無線LANへの接続とオンラインマニュアルの閲覧](./docs/wifi.md)
- [ロボットをジョイスティックで動かす（テレオペレーション）](./docs/teleop.md)
- [地図を作る（SLAM）](./docs/slam.md)
- [自律移動する（ナビゲーション）](./docs/navigation.md)
- [`Linux`ファイル操作の基本](./docs/file.md)
- [カメラ画像をキャプチャする](./docs/camera_capture.md)
- [ロボット搭載のコンピュータでシミュレータを起動する](./docs/simulation.md)
- [サンプルプログラムを実行する](./docs/samples.md)
- [ロボットの電源を切り、充電する](./docs/power_off.md)
- [ロボットのソフトをアップデートする](./docs/update.md)

付録

- [外部モニタの利用](./docs/dual_monitor.md)
- [他のソフトのインストール方法](./docs/install_tools.md)
- [システムのインストール方法](./docs/install.md)

## 履歴

- 2025/03/10 初版

<!--
## メモ

`motor_acceleration: 11500 # ticks`から計算される加速度よりも大幅に大きな値を`planner_local.yaml`に設定しているが、この値だと、速度変化がスムーズになる。
-->
