#!/bin/bash

# Workaround to execute smergify.py from client
# Replace /home/pi/smergify/ with your own path to the script folder

export PYTHONPATH="$PYTHONPATH:/home/pi/smergify/"
nohup python3 /home/pi/smergify/smergify.py "$@" >/dev/null 2>&1
