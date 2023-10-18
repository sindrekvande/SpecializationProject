import time
import sys
import asyncio

from modules.ADC import ADC # Ikke sikker på om dette fungerer som jeg tror
from modules.DAC import DAC
from modules.LED import LED, LEDcorutine
from modules.file_handler import file_handler
from modules.pinOut import pinOut
from modules.BT import BTconnect, BTcorutine 
from modules.SPI import SPI
import parameters as pm

async def main():
    # Initialize files
    file_handler = file_handler()

    # Initialize LED
    # led_control = LED(file_handler.inputFile)

    # Initialize ADC

    # initialize BT
    BT = await BTconnect.create()

    # Loop: Simulate light, measure values, track performance of SoC, save to file
    LEDtask = asyncio.create_task(LEDcorutine(file_handler))
    BTtask = asyncio.create_task(BTcorutine(BT))
    #stop = asyncio.create_task(ADCcorutine())

    await LEDtask
    await BTtask
    #await stop

    # End

asyncio.run(main())