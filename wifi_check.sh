#!/bin/bash
echo "WfifiCheck running as: $(whoami)"

echo "Delay Start for 5 minutes"
sleep 300

echo "Starting WiFi Check every minute"
while true ; do
   if ifconfig | grep -q "inet 192." ; then
      sleep 60
   else
      sleep 30
      echo "Network connection down! Check again."
      if ifconfig | grep -q "inet 192." ; then
         sleep 60
      else
         echo "Network connection still down! Attempting reconnection."
         ip link set wlan0 down
         sleep 10
         ip link set wlan0 up
         sleep 60
      fi
   fi
done

