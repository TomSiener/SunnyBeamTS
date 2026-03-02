"""Sunnybeamtool usage example"""

import asyncio
import logging

from sunnybeamtool.sunnybeamtool import SunnyBeam

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)


async def main():
    s_beam = SunnyBeam()

    while True:
        try:
            logging.debug("example get_manufacturer")            
            print(await s_beam.get_manufacturer())
            
            logging.debug("example get_manufacturer")
            print(await s_beam.get_product())
            
            logging.debug("example get_serial_number")
            print(await s_beam.get_serial_number())

            logging.debug("example get_measurements")
            data = await s_beam.get_measurements()
            print("get_measurements:", data)
            
            logging.debug("example get_manufacturer")
            data = await s_beam.get_today_measurements()
            print("get_today_measurements:", data)

            data = await s_beam.get_last_month_measurements()
            print("get_last_month_measurements:", data)

        except ConnectionError as e:
            print(str(e))

        await asyncio.sleep(5)


if __name__ == "__main__":

    loop = asyncio.new_event_loop()
    loop.create_task(main())
    loop.run_forever()
