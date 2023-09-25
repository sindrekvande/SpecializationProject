import time
import sys
import os
import pandas as pd
import import_modules
from LED import LED

file = "/home/pi/Desktop/SpecializationProject/datasets/autumn.tsv"

LED = LED(file)

def test1(LED):
    while True:
        for duty in range(0, 101, 1):
            LED.set_brightness_percent(duty)
            time.sleep(0.5)
        time.sleep(1)

        for duty in range(100, -1, -1):
            LED.set_brightness_percent(duty)
            time.sleep(0.5)
        time.sleep(1)

def test2(LED):
    LED.set_brightness_percent(50)
    while True:
        time.sleep(1)

def test3(LED):
    for key, value in LED.brightnessDF.items():
        LED.set_brightness(value)

def test4(LED):
    LED.filter_NaN_values(file)
    for key, value in LED.brightnessDF.itertuples():
        if pd.isna(value):
            print("ERROR: NaN detected in file")
            return -1
    
    print("NaN filtered")

test3(LED)
