#!/bin/bash

# Zeitstempel im Format: JAHR-MONAT-TAG_STUNDE-MINUTE-SEKUNDE
TIMESTAMP=$(date +"%Y%m%d-%H-%M-%S")

#LOGFILE="server_pymodbus1-${TIMESTAMP}.log"
LOGFILE="/dev/null"
echo "Logfile $LOGFILE"

cd /home/tom/SunnyBeamTS

#stdout und stderr in LOGFILE und console
echo "activate python env" #2>&1 | tee $LOGFILE

#source funktioniert mit redirect nicht mehr
source /home/tom/.env/bin/activate #2>&1 | tee $LOGFILE
pip -V

echo "run froniussimulator_wallbox"
python3 ./froniussimulator_wallbox.py 2>&1 | tee $LOGFILE
echo "after froniussimulator_wallbox"
