from test import *
import time
from concurrent.futures import ProcessPoolExecutor

import params as pm


'''
print(pm.dict)
print(pm.dcTime)



tc.testFunc()

print(pm.dict)
print(pm.dcTime)
'''
async def main():
    tc = testClass()

    #executor = ProcessPoolExecutor(3)
    #loop = asyncio.new_event_loop()
    one = asyncio.create_task(tc.testFunc())
    two = asyncio.create_task(tc.testFunc2())
    stop = asyncio.create_task(tc.stopFunc())
    #asyncio.coroutines([tc.testFunc(), tc.testFunc2(), tc.stopFunc()])

    await one
    await two
    await stop

asyncio.run(main())