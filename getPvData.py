import os
import time
import struct
from dotenv import load_dotenv
import paho.mqtt.client as mqtt
from datetime import datetime
from pymodbus.client import ModbusTcpClient
import asyncio
import logging
from aiologger import Logger as asyncLogger

from sunnybeamtool.sunnybeamtool import SunnyBeam


logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)

# --- LADE KONFIGURATION ---
load_dotenv() # Liest die .env Datei ein

# --- KONFIGURATION ---
MQTT_AKTIV   = True
MODBUS_AKTIV = False
INTERVALL    = 10

# Fronius GEN24 Spezial-Einstellungen
FRONIUS_IP      = os.getenv("FRONIUS_IP")
FRONIUS_PORT    = 502
# Register 40097 (Wirkleistung) im SunSpec Smart Meter Modell
# Falls 40097 nicht geht, probiere 40098 oder den Offset 40096
WR_REGISTER     = 40097
SMART_METER_ID  = 200   # Wichtig für Fronius Smart Meter Simulation
WATT_SIMULATION = 550.5 # Dein simulierter Zählerwert (Watt)

# MQTT Einstellungen
MQTT_BROKER = os.getenv("MQTT_BROKER")
MQTT_USER   = os.getenv("MQTT_USER")
MQTT_PW     = os.getenv("MQTT_PW")
MQTT_TOPIC  = "PV/SunnyBeam/"

#Korrektur des TotalWerts damit es keinen Spring gibt von 0 auf 43000
ENERGY_TOTAL_KORR = -43800

# --- INITIALISIERUNG ---
client_mqtt = None
client_mb   = None

if MQTT_AKTIV:
    # Pflicht für Paho 2.1: CallbackAPIVersion angeben
    logging.info("connecting to MQTT ...") 
    client_mqtt = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client_mqtt.username_pw_set(MQTT_USER, MQTT_PW)

if MODBUS_AKTIV:
    logging.info("connecting to Fronius ({FRONIUS_IP}}:{FRONIUS_PORT}) ...") 
    client_mb = ModbusTcpClient(FRONIUS_IP, port=FRONIUS_PORT)
    logging.debug("after connecting to Fronius1") 

async def main():
    try:
        _LOGGER = asyncLogger.with_default_handlers(level=logging.INFO)                
        _LOGGER.info("connecting to SunnyBeam ...") 
        s_beam = SunnyBeam()
        await asyncio.sleep(2)
        data = await s_beam.get_measurements()
        _LOGGER.info("get_measurements:", data)
    
        if MQTT_AKTIV:
            _LOGGER.info(f"connecting to {MQTT_BROKER} ")
            client_mqtt.connect(MQTT_BROKER, 1883)
            client_mqtt.loop_start()
            _LOGGER.info("✅ MQTT 2.1 verbunden")

        if MODBUS_AKTIV:
            if client_mb.connect():
                _LOGGER.info(f"✅ Modbus verbunden (Fronius ID {SMART_METER_ID})")
            else:
                _LOGGER.warning("❌ Modbus Verbindung zu Fronius fehlgeschlagen")

        while True:
            jetzt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            status_msg = f"[{jetzt}] "

            # SunnyBeam auslesen
            try:
                data = await s_beam.get_measurements()
                _LOGGER.info(data)            
            except Exception as err:
                _LOGGER.warning(f"Unexpected {err=}, {type(err)=}")
                await asyncio.sleep(60)
                continue
    
            # 1. MQTT Senden
            if MQTT_AKTIV:
                client_mqtt.publish(MQTT_TOPIC + "power" , data.get("power"))
                client_mqtt.publish(MQTT_TOPIC + "energy_today" , data.get("energy_today"))
                client_mqtt.publish(MQTT_TOPIC + "energy_total" , data.get("energy_total")+ENERGY_TOTAL_KORR)
                client_mqtt.publish(MQTT_TOPIC + "update_time" , jetzt)
                status_msg += "MQTT-Werte gesendet. "
    
            # 2. Modbus Senden (Fronius Float32)
            if MODBUS_AKTIV and client_mb.connected:
                # Fronius erwartet Big Endian für Bytes und Words
                builder = BinaryPayloadBuilder(byteorder=Endian.BIG, wordorder=Endian.BIG)
                builder.add_32bit_float(float(WATT_SIMULATION))
                payload = builder.to_registers()
    
                # write_registers (Plural!), da ein Float 2 Register belegt
                res = client_mb.write_registers(WR_REGISTER, payload, slave=SMART_METER_ID)

                if not res.isError():
                    status_msg += f"Modbus: {WATT_SIMULATION}W an Reg {WR_REGISTER}."
                else:
                    status_msg += f"Modbus FEHLER: {res}"

            _LOGGER.info(status_msg)
            await asyncio.sleep(INTERVALL)

    except KeyboardInterrupt:
        _LOGGER.info("\nBeendet.")
    finally:
        if client_mqtt:
            client_mqtt.loop_stop()
            client_mqtt.disconnect()
        if client_mb:
            client_mb.close()
        await _LOGGER.shutdown()

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.create_task(main())
    loop.run_forever()
