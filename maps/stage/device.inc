# https://player-stage-manual.readthedocs.io/en/latest/

define UTM-30LX ranger
(
  # https://www.hokuyo-aut.co.jp/search/single.php?serial=21
  sensor(                         
    range [ 0.0  30.0 ]
    fov 270.25
    samples 1081
  )
  # generic model properties
  color "black"
  size [ 0.06 0.06 0.09 ]
  update_interval 25
)

define YDLIDAR_T-mini_Plus ranger
(
  # https://www.ydlidar.com/products/view/27.html
  sensor(                         
    range [ 0.0  12.0 ]
    fov 360
    samples 500
  )
  # generic model properties
  color "black"
  size [ 0.0386 0.0386 0.0339 ]
  update_interval 125
)

define RaspberryPi_Camera_Module_v2 camera
(
  # https://www.raspberrypi.com/documentation/accessories/camera.html#hardware-specification
  # https://player-stage-manual.readthedocs.io/en/latest/WORLDFILES/#3211-camera
  resolution [ 640 480 ]
  range [ 0.2 20.0 ]
  fov [ 62.2 48.8 ]
  pantilt [ 0.0 0.0 ]

  # model properties
  size [ 0.01 0.025 0.025 ]
  color "green"
)

define triangle model(
  block( 
    points 3
    point[0] [0.05 0.0]
    point[1] [0.0  0.025]
    point[2] [0.0 -0.025]
    z [0 0.1]
  )
  color "green"
)

define robot position
(
  size   [0.225 0.225 0.1793]
  origin [-0.0675 0 0 0] # move rotation center forward
  gui_nose 1
  drive "diff"
  YDLIDAR_T-mini_Plus(pose [ 0.0257 0 0.0683 0 ])
  RaspberryPi_Camera_Module_v2(pose [ 0 0 -0.01975 0 ])
  triangle(
    pose [-0.085 0 0 0 ]
    size [ 0.15  0.15 0.01]
  )
  velocity_bounds     [-0.4 0.4 0 0 0 0 -270 270]
  acceleration_bounds [-1.2 1.2 0 0 0 0 -270 270]
  update_interval 50
)
