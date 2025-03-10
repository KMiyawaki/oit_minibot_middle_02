#!/bin/bash

function extract_map_origin(){
  if [ $# -ne 1 ]; then
    echo "usage:${0} map_yaml" 1>&2
    exit 1
  fi
  local ORIGIN=$(grep origin ${1})
  ORIGIN=${ORIGIN/origin:/}
  ORIGIN=${ORIGIN/[/}
  ORIGIN=${ORIGIN/]/}
  ORIGIN=$(echo ${ORIGIN})
  ORIGIN=${ORIGIN//,/ }
  echo "${ORIGIN}"
}

function calc() {
  awk "BEGIN {print $*}"
}

function main(){
  if [ $# -ne 1 ]; then
    echo "usage:${0} map_yaml" 1>&2
    exit 1
  fi
  if [ -z ${1##*.} ] || [ ${1##*.} != 'yaml' ]; then
    echo "error: specify *.yaml file" 1>&2
    exit 1
  fi
  local -r MAP_DIR=`dirname ${1}`
  local MAP_NAME=`basename ${1}`
  readonly MAP_NAME=${MAP_NAME%.*}
  local -r MAP_YAML=${MAP_NAME}.yaml
  local -r MAP_PGM=${MAP_NAME}.pgm
  local -r MAP_PNG=${MAP_NAME}_border.png
  local -r SIMULATION_WORLD=${MAP_NAME}.world

  echo "Add black border into ${MAP_DIR}/${MAP_PGM}... "
  ./add_map_image_border.sh ${MAP_DIR}/${MAP_PGM}
  echo "Generated ${MAP_DIR}/${MAP_PNG}"
  local -r IMG_WIDTH=$(identify -format "%w" ${MAP_DIR}/${MAP_PNG})
  local -r IMG_HEIGHT=$(identify -format "%h" ${MAP_DIR}/${MAP_PNG})
  local -r MAP_WIDTH=$(calc "${IMG_WIDTH} * 0.05")
  local -r MAP_HEIGHT=$(calc "${IMG_HEIGHT} * 0.05")
  local -r ORIGIN=$(extract_map_origin "${MAP_DIR}/${MAP_YAML}")
  local OX=
  local OY=
  local OZ=
  read OX OY OZ <<< "${ORIGIN}"
  readonly OX;  readonly OY;  readonly OZ
  local CX=$(calc "${MAP_WIDTH} / 2 + ${OX}")
  local CY=$(calc "${MAP_HEIGHT} / 2 + ${OY}")
  CX=$(printf "%.2f" ${CX})
  CY=$(printf "%.2f" ${CY})
  readonly CX;  readonly CY

  local MAP_INC="./stage/map.inc"
  local DEVIDE_INC="./stage/device.inc"
  if [ ${MAP_DIR} != '.' ]; then
    MAP_INC=".${MAP_INC}"
    DEVIDE_INC=".${DEVIDE_INC}"
  fi
  # Make stage simulator world file
cat << EOF > ${MAP_DIR}/${SIMULATION_WORLD}
include "${MAP_INC}"
include "${DEVIDE_INC}"

# set the resolution of the underlying raytrace model in meters
resolution 0.02

interval_sim 25  # simulation timestep in milliseconds

# configure the GUI window
window
(
  size [700.000 400.000]
  scale 20
)

# load an environment bitmap
floorplan
(
  bitmap "./${MAP_PNG}"
  size [${MAP_WIDTH} ${MAP_HEIGHT} 1.5]
  pose [${CX} ${CY} 0 0 0]
)

robot
(
  # can refer to the robot by this name
  name "r0"
  pose [0 0 0 0]
)

human_block(
  pose [0 -2 0 0]
  color "yellow"
)

ellipse_block(
  pose [0.8 -2 0 0]
  color "blue"
)

middle_block(
  pose [0 2 0 0]
  color "yellow"
)

middle_block(
  pose [0.6 2 0 0]
  color "red"
)

middle_block(
  pose [1.2 2 0 0]
  color "blue"
)
EOF
}

main "$@"