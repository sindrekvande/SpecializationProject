import time
import asyncio
from bleak import *
import os
import sys
from threading import *
#from bluepy.btle import *

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
        #soc.waitForDevice()
        
        print('Disconnecting in:')
        print('5...')
        time.sleep(1)
        print('4...')
        time.sleep(1)
        print('3...')
        time.sleep(1)
        print('2...')
        time.sleep(1)
        print('1...')
        time.sleep(1)
        print('done')
'''
def test3():
    peripheral = Peripheral('E0:21:78:85:2A:FB', 'random')
    peripheral.connect()
    peripheral.pair()

test3()
'''
async def test4():
    await asyncio.sleep(2.0)
    print("Inside test4()_________________________")

async def main():
    task2 = asyncio.create_task(test2())
    task4 = asyncio.create_task(test4())
    await asyncio.wait([task2, task4])

asyncio.run(test2())