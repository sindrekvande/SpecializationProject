from bleak import *
import asyncio

import os
import sys

absolute_path = os.path.dirname(__file__)
relative_path = ".."
full_path = os.path.join(absolute_path, relative_path)
sys.path.insert(0, full_path)
import parameters as pm

class SoCperformance:
    def __init__(self, client):
        self.perfomance = 0
        self.client = client
        #asyncio.run(self.connectBLE())
    '''
    async def connectBLE(self):
        self.client = BleakClient(pm.SoCMAC)
        #await client.pair()
        await self.client.connect()
        #await self.client.start_notify('57a70000-9350-11ed-a1eb-0242ac120002', self.callback)
        if self.client.is_connected():
            print('BLE device connected')
        else:
            print('No connection established')
        return self.client
    '''
    def readBLE(self):
        for service in client.services:
            print("{0} : {1}".format(service.uuid, service.description))
            #for char in service.characteristics:
            #    if 'read' in char.properties:
            #        data = await client.read_gatt_char(service.uuid)
            #        print(data)
    
    def callback(self, sender: BleakGATTCharacteristic, data: bytearray):
        print(f"{sender}: {data}")

    def storePerfData(self, file, data):
        pass # Write data to file