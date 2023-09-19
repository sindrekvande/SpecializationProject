import time
import sys

from modules.ADC import ADC # Ikke sikker på om dette fungerer som jeg tror
from modules.DAC import DAC
from modules.LED import LED
from modules.menu import menu
from modules.pinOut import pinOut
from modules.SoCperformance import SoCperformance 
from modules.SPI import SPI
import parameters as pm

# Make bluetooth connection
perf = SoCperformance()

# Menu?
start_menu = menu(sys.args)

# Initialize LED
led_control = LED(star_menu.inputFile)

# Initialize ADC

# Initialize DAC

# Loop: Simulate light, measure values, track performance of SoC, save to file
for key, irrValue in led_control.brightness_df.items():
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
    start_menu.append_to_file(outputValues)



# End