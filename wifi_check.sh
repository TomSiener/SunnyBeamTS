#!/bin/bash

echo "Starting WiFi Check every minute"
while true ; do
   if ifconfig | grep -q "inet 192." ; then
      sleep 60
   else
      echo "Network connection down! Check again."
      if ifconfig | grep -q "inet 192." ; then
         sleep 60
      else
         echo "Network connection still down! Attempting reconnection."
         ifdown --force wlan0
         sleep 10
         ifup --force wlan0
         sleep 60
      fi
   fi
done

