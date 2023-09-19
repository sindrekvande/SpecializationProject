import time
import sys

from modules.ADC import ADC # Ikke sikker på om dette fungerer som jeg tror
from modules.DAC import DAC
from modules.LED import LED
from modules.menu import menu
from modules.pinOut import pinOut
from modules.SoCperformance import SoCperformance 
from modules.SPI import SPI

# Make bluetooth connection
perf = SoCperformance()

# Menu?
start_menu = menu(sys.args)

# Initialize LED
led_control = LED(star_menu.inputFile)

# Initialize ADC

# Initialize DAC

# Loop: Simulate light, measure values, track performance of SoC, save to file
for key, value in led_control.brightness_df.items():
    outputValues = []
    # Set brighness on led from file value
    led_control.set_brightness(value)

    # Let led brightness, voltages and currents settle
    time.sleep(0.01)

    # Measure ADC values
    
    # Get number of packages from SoC
    
    # Save to file
    start_menu.append_to_file(outputValues)



# End