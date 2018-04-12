#!/bin/bash

sudo hciconfig hci0
sudo hciconfig hci0 piscan
sudo sdptool add --channel=1 SP
python3 /home/pi/tjproject/main.py