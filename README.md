# SunnyBeamToolTS

  - läuft auf tomspi2 und ist per USB mit dem Sunny-Beam-Display verbunden um die PV-DAten dem Fronius-WR bereitzustellen.
  - stellt zusätzlich die Daten dem Homeassistant (tomspi3) per MQTT bereit.
  - liest den Wallbox Verbrauch per MQTT vom Homeassistant und stellt sie auch dem WR als Verbraucher bereit.
  - wird vom Homeassistnat überwacht und ggf. neu gestartet.

### GetPVData.py  
  liest die PV-Daten der SunnyBoys über USB vom SunnyBeam-Display aus.

  - ```get_measurements()``` current production (power in W, daily energy in kWh, total energy in kWh)          <- verwendet
  - ```get_today_measurements()``` historical power of the current day (datetime, power in W)                   <- nicht verwendet
  - ```get_last_month_measurements()``` historical energy per day of the last month (datetime, energy in kWh)   <- nicht verwendet

### froniussimulator_pv.py
    siumuliert einen Fronius SmartMeter um die PV-Daten dem Fonius Gen24 Wechselrichter über ModbusTCP bereitzustellen

### froniussimulator_wallbox.py
    siumuliert einen Fronius SmartMeter um den Wallbox-Verbrauch dem Fonius Gen24 Wechselrichter über ModbusTCP bereitzustellen

### wifi_check.sh   
    prüft alle Minute das vorhandensein der IP-Adresse und rebootet im Fehlerfall

-----------------------------------------------------------------

### run...sh
    starten die python env und die obigen Python Scrypte

---------------------------------------------------------------
### Unterordner **services**
    systemd service unit files zum starten der obigen scripte als systemd-services
