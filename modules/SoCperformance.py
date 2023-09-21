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
    device = ''
    async def __aenter__(self):
        await self.scan()
        self.client = BleakClient(self.device)
        await self.client.connect()
        await self.find_service()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.disconnect()

    def __init__(self):
        self.perfomance = 0
        #self.client = client
        #asyncio.run(self.scan())
    
    async def connectBLE(self):
        #self.client = BleakClient(pm.SoCMAC)
        #await client.pair()
        ##await self.client.connect()
        #await self.client.start_notify('57a70000-9350-11ed-a1eb-0242ac120002', self.callback)
        async with BleakClient(pm.SoCMAC) as client:
            if client.is_connected:
                print('BLE device connected')
            else:
                print('No connection established')
        #return self.client
    
    async def find_service(self):
        #async with BleakClient(self.device) as client:
        for service in self.client.services:
            #print("{0} : {1}".format(service.uuid, service.description))
            if pm.SoCservice in service.uuid[:8]:
                print('Service {0} found'.format(pm.SoCservice)) # Use this to fint the correct service
                for char in service.characteristics:
                    #print(char.properties)
                    if 'read' in char.properties:
                        try:
                            value = await self.client.read_gatt_char(char.uuid)
                            self.serviceChar = char.uuid
                            self.perfomance = value[0]
                            print(value[0])
                        except:
                            print('could not read')

    async def scan(self):
        dev = await BleakScanner.discover()
        for i in range(0,len(dev)):
            #print("["+str(i)+"]"+str(dev[i]))
            if (str(dev[i])[-len(pm.SoCname):] == pm.SoCname):
                self.device = str(dev[i])[:-(len(pm.SoCname)+2)]
                print('Device called {0} found with MAC {1}'.format(pm.SoCname,self.device))
        if self.device == '':
            print('Device by the name of {0} could not be found'.format(pm.SoCname))
    '''
    def callback(self, sender: BleakGATTCharacteristic, data: bytearray):
        print(f"{sender}: {data}")
    '''
    def storePerfData(self, file, data):
        pass # Write data to file