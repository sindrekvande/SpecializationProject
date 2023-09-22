import time
import asyncio
from bleak import *
import os
import sys

import import_modules
from SoCperformance import SoCperformance
import parameters as pm
'''
async def test():
    async with BleakClient(pm.SoCMAC) as client:
        if client.is_connected:
            print('connected')
        
        
        #for service in client.services:
        #    print("{0} : {1}".format(service.uuid, service.description))

        while True:
            time.sleep(2)
            

asyncio.run(test())
'''
async def test2():
    async with SoCperformance() as soc:
        print('Disconnecting in: 3...')
        time.sleep(1)
        print('2...')
        time.sleep(1)
        print('1...')
        time.sleep(1)
        print('done')

asyncio.run(test2())