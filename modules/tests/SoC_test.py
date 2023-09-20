import time
import asyncio
from bleak import *
import import_path
from SoCperformance import SoCperformance
import parameters as pm

async def test():
    client = BleakClient(pm.SoCMAC)
    #print('defined')
    #await client.connect()
    #print('connected')
    paired = await client.pair(protection_level=2)
    #print('paired')
    async with BleakClient(pm.SoCMAC) as client:
        #await client.pair(protection_level=1)
        soc = SoCperformance(client)
        soc.readBLE()
        
        
        #for service in client.services:
        #    print("{0} : {1}".format(service.uuid, service.description))

        while True:
            time.sleep(2)
            

asyncio.run(test())