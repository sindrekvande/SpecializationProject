import asyncio
import time
import params as pm
from datetime import datetime
import atimer

#variable = 0

class testClass:
    async def testFunc(self):
        #global variable
        #variable[0] = 1
        #i = 99
        pm.messages[pm.msIrrValue] = 100
        while pm.testActive:
            await asyncio.sleep(1)
            #i -= 1
            #self.setValue(i)
            pm.messages[pm.msIrrValue] -= 1
            #print(pm.messages[pm.msIrrValue])

    async def testFunc2(self):
        while pm.testActive:
            print(self.getValue())
            await asyncio.sleep(1)

    async def stopFunc(self):
        timer = atimer.Timer(1)
        timer.start()
        for i in range(0, 10, 1):
            print(f"Time: {datetime.now().strftime('%H:%M:%S.%f')}")
            #await asyncio.sleep(1)
            await timer
        timer.close()
        print("Done")
        pm.testActive = False

    def setValue(self, number):
        pm.messages[pm.msIrrValue] = number
    
    def getValue(self):
        return pm.messages[pm.msIrrValue]