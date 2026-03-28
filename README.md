# SunnyBeamToolTS

#GetPVData.py  liest die PV-DAten ser SunnyBoys über USB vom SunnyBeam-Display aus.

  - ```get_measurements()``` current production (power in W, daily energy in kWh, total energy in kWh)
  - ```get_today_measurements()``` historical power of the current day (datetime, power in W)
  - ```get_last_month_measurements()``` historical energy per day of the last month (datetime, energy in kWh)

```**froniussimulator_3_noCheckMK.py**``` siumuliert einen Fronius SmartMeter um die PV-Daten dem Fonius Gen24 Wechselrichter über ModbusTCP bereitzustellen

```**froniussimulator_wallbox.py**```  siumuliert einen Fronius SmartMeter um den Wallbox-Verbrauch dem Fonius Gen24 Wechselrichter über ModbusTCP bereitzustellen

***wifi_check.sh*** prüft alle Minute das vorhandensein der IP-Adresse und rebootet im Fehlefall

