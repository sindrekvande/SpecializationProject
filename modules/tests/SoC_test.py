import time
import asyncio
from bleak import *
import import_path
from SoCperformance import SoCperformance
import parameters as pm

async def test():
    client = BleakClient(pm.SoCMAC)
    await client.pair()
    async with BleakClient(pm.SoCMAC) as client:
        #soc = SoCperformance(client)
        #soc.readBLE()
        #await client.pair()
        #await client.connect()
        for service in client.services:
            print("{0} : {1}".format(service.uuid, service.description))

        while True:
            time.sleep(2)
            

asyncio.run(test())