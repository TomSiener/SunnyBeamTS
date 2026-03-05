#!/bin/bash

# Zeitstempel im Format: JAHR-MONAT-TAG_STUNDE-MINUTE-SEKUNDE
TIMESTAMP=$(date +"%Y%m%d-%H-%M-%S")
LOGFILE="server_pymodbus1-${TIMESTAMP}.log"
#ERRFILE="getPvData_err_${TIMESTAMP}.log"
echo "Logfile $LOGFILE"

cd /home/tom/SunnyBeamTS

#stdout und stderr in LOGFILE und console
echo "activate python env" 2>&1 | tee $LOGFILE

#source funktioniert mit redirect nicht mehr
source /home/tom/.env/bin/activate #2>&1 | tee $LOGFILE
pip -V

echo "run server_pymodbus1.py" 2>&1 | tee $LOGFILE
python3 ./server_pymodbus1.py --comm tcp --port 502
#2>&1 | tee $LOGFILE
echo "after server_pymodbus1.py" 2>&1 | tee $LOGFILE
