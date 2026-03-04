#!/bin/bash

# Zeitstempel im Format: JAHR-MONAT-TAG_STUNDE-MINUTE-SEKUNDE
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
LOGFILE="getPvData_${TIMESTAMP}.log"
ERRFILE="getPvData_err_${TIMESTAMP}.log"

cd /home/tom//SunnyBeamTS

#  stdout in LOGFILE und stderr in beide files
echo "activate python env" 1>> "$LOGFILE" 2> >(tee -a "$LOGFILE" > "$ERRFILE")
source /home/tom/.env/bin/activate #1>> "$LOGFILE" 2> >(tee -a "$LOGFILE" > "$ERRFILE")

echo "run getPvData" 1>> "$LOGFILE" 2> >(tee -a "$LOGFILE" > "$ERRFILE")
python ./getPvData.py #1>> "$LOGFILE" 2> >(tee -a "$LOGFILE" > "$ERRFILE")

