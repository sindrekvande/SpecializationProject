import time
import sys
import asyncio
import RPi.GPIO as GPIO
import pigpio

#from modules.ADC import ADC # Ikke sikker på om dette fungerer som jeg tror
#from modules.DAC import DAC
from modules.LED import LED, LEDcoroutine
from modules.file_handler import file
import modules.pinOut as pinOut
from modules.BT import BTconnect, BTcoroutine 
from modules.SPI import SPI, SPIcoroutine
import parameters as pm

async def main():

    # Initialize files
    file_handler = file()

    # Initialize LED
    # led_control = LED(file_handler.inputFile)

    # Initialize ADC

    # initialize BT
    #BT = await BTconnect.create()

    # Start corutines: Simulate light, measure values, track performance of DUT, save to file
    LEDtask = asyncio.create_task(LEDcoroutine(file_handler))
    #BTtask = asyncio.create_task(BTcoroutine(BT))
    ADCtask = asyncio.create_task(SPIcoroutine())

    await LEDtask
    #await BTtask
    await ADCtask

    # End

asyncio.run(main())