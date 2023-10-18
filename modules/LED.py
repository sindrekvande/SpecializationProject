import pinOut
import RPi.GPIO as GPIO
import pandas as pd
import asyncio
from file_handler import file_handler
import import_main
import parameters as pm
import messages as msg

class LED:
    freq = 1000 # measured as 870Hz, shouldn't affect the behaviour
    duty = 0

    def __init__(self, file):
        self.get_values_from_file(file)
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pinOut.LED_DRV_DIM,GPIO.OUT)
        self.pwm = GPIO.PWM(pinOut.LED_DRV_DIM,self.freq)
        self.pwm.start(self.duty)

    def set_brightness_percent(self, percent): # programmed = measured: 50 = 50, 25 = 28, 75 = 73
        if percent >= 0 and percent <= 100:
            self.pwm.ChangeDutyCycle(percent)
            self.duty = percent
    
    def get_brightness_percent(self):
        return self.duty

    def calibrate():
        pass # do some sort of calibration with the pyranometer

    def convert_watt_to_percent(self, watt): # 1000 W/m^2 -> 100% PWM
        return ((watt / 1000) * 100)

    def set_brightness(self, watt):
        self.set_brightness_percent(self.convert_watt_to_percent(watt))

    def get_values_from_file(self, file):
        self.brightnessDF = pd.read_csv(file, sep='\t', usecols = [pm.column],  dtype = float, nrows = (pm.numberOfDays*60*24)) # header=0, index_col=False, 
        return self.brightnessDF

    def __str__(self):
        self.brightnessDF

    def single_value(self, index):
        return self.brightnessDF.loc[index, pm.column]

    def filter_NaN_values(self, file):
        NaNCounter = 0
        self.get_values_from_file(file)

        for key, irrvalue in self.brightnessDF.itertuples():   
            if pd.isna(irrvalue) and NaNCounter == 0:
                previousValue = self.single_value(key - 1)
                #Check if next values are NaN
                for nextValueIndex in range(1, len(self.brightnessDF) - key):
                        NaNCounter += 1
                        nextValue = self.single_value(key + nextValueIndex)
                        if pd.notna(nextValue):
                            break
            if NaNCounter > 0:
                self.brightnessDF.loc[key, pm.column] = (previousValue + nextValue)/2
                NaNCounter -= 1
                    
        return self.brightnessDF
    
    def brightness_interpolation(self):
        fadeDuration = 2.0

        for key, irrValue in self.brightnessDF.itertuples():
            currentBrightness = 0
            stepSize = (irrValue - currentBrightness)/pm.rampUpStep

            for _ in range(pm.rampUpStep):
                currentBrightness += stepSize
                self.set_brightness(currentBrightness)
                self.time.sleep(fadeDuration/pm.rampUpStep)
        
        self.set_brightness(irrValue)

        #time.sleep(0.5)?

async def LEDcorutine(file_handler: file_handler):
    # Initialize LED
    led_control = LED(file_handler.inputFile)

    if pm.rampUp:
        for key, irrValue in led_control.brightnessDF.itertuples():
            nextValue = led_control.single_value(key + 1)
            for i in range(0,pm.rampUpStep, 1):
                led_control.set_brightness(irrValue + ((irrValue - nextValue) * i)/pm.rampUpStep)
                await asyncio.sleep(pm.timeStep/pm.rampUpStep)
    else:
        for key, irrValue in led_control.brightnessDF.itertuples():
            # Set brighness on led from file value
            led_control.set_brightness(irrValue)

            # Wait for next value
            await asyncio.sleep(pm.timeStep)
    
    # End the other corutines
    msg.testActive = False