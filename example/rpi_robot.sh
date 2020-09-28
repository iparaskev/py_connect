#!/bin/bash

python3 rpi_sonar_left.py &
python3 rpi_sonar_right.py &
python3 rpi_tfmini_front.py &
python3 rpi_motor_controller.py &
