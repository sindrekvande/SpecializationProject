from bleak import *
import asyncio
import os, sys, pexpect, time
import import_main
import parameters as pm

class SoCperformance:
    device = '' #E0:21:78:85:2A:FB
    async def __aenter__(self):
        await self.scan()
        '''
        if self.device == '':
            self.__aenter__()
        else:
            self.pairDevice()
        '''
        self.client = BleakClient(self.device)
        
        try:
            await self.client.connect()
            print(self.client.is_connected)
            paired = await self.client.pair(protection_level=4)
            print(f"Paired: {paired}")
            await self.find_service()
        except:
            print('Delete paired device on Pi, and/or erase+flash nRF')

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.disconnect()

    def __init__(self):
        self.perfomance = 0
    
    async def find_service(self):
        #async with BleakClient(self.device) as client:
        for service in self.client.services:
            print("{0} : {1}".format(service.uuid, service.description))
            if True:# pm.SoCservice in service.uuid[:8]:
                #print('Service {0} found'.format(pm.SoCservice)) # Use this to fint the correct service
                for char in service.characteristics:
                    print(char.properties)
                    if 'read' in char.properties:
                        try:
                            value = await self.client.read_gatt_char(char.uuid)
                            self.serviceChar = char.uuid
                            self.perfomance = value[0]
                            print(value[0])
                        except:
                            print('could not read')
                            
                    if ('notify' or 'indicate') in char.properties:
                        try:
                            await self.client.start_notify(char.uuid, self.callback)
                            print('Waiting for change')
                            await asyncio.sleep(5.0)
                            await self.client.stop_notify(char.uuid)
                        except:
                            print('could not start notify')
    
    def callback(self, sender: BleakGATTCharacteristic, data: bytearray):
        print(f"{sender}: {data[0]}")

    async def scan(self):
        dev = await BleakScanner.discover()
        for i in range(0,len(dev)):
            #print("["+str(i)+"]"+str(dev[i]))
            if (str(dev[i])[-len(pm.SoCname):] == pm.SoCname):
                self.device = str(dev[i])[:-(len(pm.SoCname)+2)]
                print('Device called {0} found with MAC {1}'.format(pm.SoCname,self.device))
        if self.device == '':
            print('Device by the name of {0} could not be found'.format(pm.SoCname))

    def pairDevice(self):
        response=''
        p = pexpect.spawn('bluetoothctl', encoding='utf-8')
        p.logfile_read = sys.stdout
        p.expect('#')
        p.sendline("remove "+self.device)
        p.expect("#")
        p.sendline("scan on")

        mylist = ["Discovery started","Failed to start discovery","Device "+self.device+" not available","Failed to connect","Connection successful", "Changing "+self.device+" trust succeeded"]
        while response != "Changing "+self.device+" trust succeeded":
            p.expect(mylist)
            time.sleep(1)
            response=p.after
            p.sendline("pair "+self.device)
            #time.sleep(4)
            #p.expect("[agent] Confirm passkey .* (yes/no):")
            p.expect("Request confirmation")
            time.sleep(5)
            p.sendline("yes")
            p.waitnoecho()
            p.expect("Pairing successful")
            p.expect("#")
            p.sendline("trust "+self.device)
            #time.sleep(1)
            p.expect(mylist)
            time.sleep(1)
            response=p.after
        p.sendline("quit")
        p.close()
        #time.sleep(1)
        return