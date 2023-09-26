import time
import sys

from modules.ADC import ADC # Ikke sikker på om dette fungerer som jeg tror
from modules.DAC import DAC
from modules.LED import LED
from modules.file_handler import file_handler
from modules.pinOut import pinOut
from modules.SoCperformance import SoCperformance 
from modules.SPI import SPI
import parameters as pm

async def main():
    async with SoCperformance as soc:
        # Menu?
        file_handler = file_handler()

        # Initialize LED
        led_control = LED(file_handler.inputFile)

        # Initialize ADC

        # Initialize DAC

        # Loop: Simulate light, measure values, track performance of SoC, save to file
        for key, irrValue in led_control.brightnessDF.itertuples():
            outputValues = []
            nextValue = led_control.single_value(key + 1)
            if pm.rampUp == True:
                for i in range(0,pm.rampUpStep, 1):
                    led_control.set_brightness(irrValue + ((irrValue - nextValue) * i)/pm.rampUpStep)
                    time.sleep(pm.timeStep/(pm.rampUpStep*60))
            else:
                # Set brighness on led from file value
                led_control.set_brightness(irrValue)

                # Let led brightness, voltages and currents settle
                time.sleep(pm.timeStep/60)

            # Measure ADC values
            
            # Get number of packages from SoC
            
            # Save to file
            file_handler.append_to_file(outputValues)



        # End

asyncio.run(main())