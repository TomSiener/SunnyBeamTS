#!/bin/bash

# Zeitstempel im Format: JAHR-MONAT-TAG_STUNDE-MINUTE-SEKUNDE
TIMESTAMP=$(date +"%Y%m%d-%H-%M-%S")
#LOGFILE="getPvData_${TIMESTAMP}.log"
LOGFILE="/dev/null"
#ERRFILE="getPvData_err_${TIMESTAMP}.log"
echo "Logfile $LOGFILE"

cd /home/tom/SunnyBeamTS

#stdout und stderr in LOGFILE und console
echo "activate python env"

#source funktioniert mit redirect nicht mehr
source /home/tom/.env/bin/activate
pip -V
echo "run getPvData" 
python3 ./getPvData.py 2>&1 | tee $LOGFILE
echo "after getPvData" 

