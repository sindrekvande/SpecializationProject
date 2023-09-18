import time
import sys

from modules.ADC import ADC # Ikke sikker på om dette fungerer som jeg tror
from modules.DAC import DAC
from modules.LED import LED
from modules.pinOut import pinOut
from modules.SoCperformance import SoCperformance 
from modules.SPI import SPI

# Make bluetooth connection
perf = SoCperformance()

# Menu?
inputFilePath = "/home/pi/Desktop/SpecializationProject/datasets/"
outputFilePath = "/home/pi/Desktop/SpecializationProject/measurements/"

inputFileDefault = 'tng00001_2020-09'
outputFileDefault = 'tng00001_2020-09_measurments'

if len(sys.argv) >= 2:
    inputFile = inputFilePath + sys.argv[0] + '.tsv'
    outputFile = outputFilePath + sys.argv[1] + '.tsv'
elif len(sys.argv) >= 1:
    inputFile = inputFilePath + sys.argv[0] + '.tsv'
    outputFile = outputFilePath + sys.argv[0] + '_measurments.tsv'
else:
    inputFile = inputFilePath + inputFileDefault + '.tsv'
    outputFile = outputFilePath + outputFileDefault + '.tsv'


# Initialize LED
led_control = LED(file)

# Initialize ADC

# Initialize DAC

# Loop: Simulate light, measure values, track performance of SoC, save to file
for key, value in led_control.brightness_df.items():
    # Set brighness on led from file value
    led_control.set_brightness(value)

    # Let values settle
    time.sleep(0.01)

    # Measure ADC values
    
    # Get number of packages from SoC
    
    # Save to file



# End