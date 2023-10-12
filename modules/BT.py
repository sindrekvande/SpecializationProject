from bleak import *
import asyncio
import os, sys, pexpect, time
import import_main
import parameters as pm

class BTconnect:
    device = '' #E0:21:78:85:2A:FB
    perfomance = 0
    #testActive = True

    async def __aenter__(self):
        await self.scan()
        if device == '': exit()
        self.client = BleakClient(self.device)
        try:
            await self.client.connect()
            print(f"Connected: {self.client.is_connected}")
            paired = await self.client.pair(protection_level=2)
            print(f"Paired: {paired}")
            await self.find_service()
            await self.client.disconnect()

            #await self.waitForDevice()
        except:
            print('Unpairing device to try again.')
            self.unpairDevice()
            self.__aenter__()
            #print('Delete paired device on Pi, and/or erase+flash nRF')

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass
    #    self.unpairDevice()
    
    async def find_service(self):
        #async with BleakClient(self.device) as client:
        for service in self.client.services:
            print("{0} : {1}".format(service.uuid, service.description))
            if pm.BTservice in service.uuid[:8]:
                #print('Service {0} found'.format(pm.BTservice)) # Use this to find the correct service
                for char in service.characteristics:
                    print(char.properties)
                    '''
                    if 'read' in char.properties:
                        try:
                            value = await self.client.read_gatt_char(char.uuid)
                            self.perfomance = value[0]
                            print(value[0])
                        except:
                            print('could not read')
                    '''
                    if ('notify' or 'indicate') in char.properties:
                        #try:
                            #await self.client.start_notify(char.uuid, self.callback)
                        #if pm.BTservice in service.uuid[0:8]:
                        self.serviceChar = char.uuid
                            #print('Waiting for change')
                            #await asyncio.sleep(5.0)
                            #await self.client.stop_notify(char.uuid)
                        #except:
                            #print('could not start notify')
    
    def callback(self, sender: BleakGATTCharacteristic, data: bytearray):
        print(f"{sender}: {data[0]}")
        #Send data[0] to the file
        self.performance = data[0]

    async def scan(self):
        dev = await BleakScanner.discover()
        for i in range(0,len(dev)):
            #print("["+str(i)+"]"+str(dev[i]))
            if (str(dev[i])[-len(pm.BTname):] == pm.BTname):
                self.device = str(dev[i])[:-(len(pm.BTname)+2)]
                print('Device called {0} found with MAC {1}'.format(pm.BTname,self.device))
        if self.device == '':
            print('Device by the name of {0} could not be found'.format(pm.BTname))

    async def waitForDevice(self, performance, testActive):
        disconnected_event = asyncio.Event()
        def disconnected_callback(client):
            print("Disconnected event")
            disconnected_event.set()
        while testActive:
            try:
                async with BleakClient(self.device, disconnected_callback=disconnected_callback) as client:
                    print("Starting notify")
                    await client.start_notify(self.serviceChar, self.callback)
                    print("Waiting for disconnect")
                    await disconnected_event.wait()
                    print("Disconnected")
                    performance = self.perfomance #This only works if there are only ONE notification
                    disconnect_event.clear()
            except:
                await asyncio.sleep(pm.btInterval)


    def pairDevice(self): #Only needed if pairing with equal numbers validation
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
            await asyncio.sleep(1)
            response=p.after
            p.sendline("pair "+self.device)
            #time.sleep(4)
            #p.expect("[agent] Confirm passkey .* (yes/no):")
            p.expect("Request confirmation")
            await asyncio.sleep(5)
            p.sendline("yes")
            p.waitnoecho()
            p.expect("Pairing successful")
            p.expect("#")
            p.sendline("trust "+self.device)
            #time.sleep(1)
            p.expect(mylist)
            await asyncio.sleep(1)
            response=p.after
        p.sendline("quit")
        p.close()
        #time.sleep(1)
        return

    def unpairDevice(self):
        response=''
        p = pexpect.spawn('bluetoothctl', encoding='utf-8')
        p.logfile_read = sys.stdout
        p.expect('#')
        p.sendline("remove "+self.device)
        await asyncio.sleep(2)
        p.expect("#")
        p.sendline("remove "+self.device)
        p.expect("#")
        p.sendline("quit")
        p.close()

async def BTcorutine(performance, testActive):
    async with BTconnect() as BT:
        await BT.waitForDevice(performance, testActive)