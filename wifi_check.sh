#!/bin/bash
echo "WfifiCheck running as: $(whoami)"

echo "Delay Start for 5 minutes"
sleep 300

echo "Starting WiFi Check every minute"
while true ; do
   if ifconfig | grep -q "inet 192." ; then
      sleep 60
   else
      echo "Network connection down! Check again."
      sleep 60      
      if ifconfig | grep -q "inet 192." ; then
         sleep 60
      else
         echo "Network connection still down. Rebooting."
         reboot
         #echo "Network connection still down! Attempting reconnection."
         #echo "systemctl restart NetworkManager"
         #systemctl restart NetworkManager
         #ip link set wlan0 down
         #echo "nmcli radio wifi off"
         #nmcli radio wifi off
         #sleep 10
         #echo "nmcli radio wifi on"
         #nmcli radio wifi on
         sleep 60
      fi
   fi
done

