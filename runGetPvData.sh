#!/bin/bash

# Zeitstempel im Format: JAHR-MONAT-TAG_STUNDE-MINUTE-SEKUNDE
TIMESTAMP=$(date +"%Y%m%d-%H-%M-%S")
LOGFILE="getPvData_${TIMESTAMP}.log"
#ERRFILE="getPvData_err_${TIMESTAMP}.log"
echo "Logfile $LOGFILE"

cd /home/tom/SunnyBeamTS

#  stdout in LOGFILE und stderr in beide files
echo "activate python env" 2>&1 | tee $LOGFILE
source /home/tom/.env/bin/activate 2>&1 | tee $LOGFILE
pip -V

echo "run getPvData" 2>&1 | tee $LOGFILE
python3 ./getPvData.py  2>&1 | tee $LOGFILE
