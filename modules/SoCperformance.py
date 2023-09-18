from bleak import *
import asyncio

MAC = '90:81:58:D9:6E:90'

class SoCperformance:
    def __init__(self):
        self.perfomance = 0
        asyncio.run(self.connectBLE())
    
    async def connectBLE(self):
        async with BleakClient(MAC) as client:
            await client.pair()
            await client.connect()
            if client.is_connected():
                print('Bluetooth LE device connected')
            else:
                print('No connection established')
                return
            for service in client.services:
                print("[Service] {0}: {1}".format(service.uuid, service.description))
                for char in service.characteristics:
                    if 'read' in char.properties:
                        data = await client.read_gatt_char(service.uuid)
            