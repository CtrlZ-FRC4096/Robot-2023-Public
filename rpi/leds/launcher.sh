#!/bin/sh
#launcher.sh

#cd /
#cd home/pi/leds

LOGFILE=log.txt

writelog() {
  now=`date`
  echo "$now $*" >> $LOGFILE
}

while true ; do
  sudo python /home/pi/leds/robot_leds1.py
  writelog "Exited with status $?"
  writelog "Restarting"
done