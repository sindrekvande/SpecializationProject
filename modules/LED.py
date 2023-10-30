import pinOut
import RPi.GPIO as GPIO
import pandas as pd
import asyncio
import atimer
from file_handler import file
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
            msg.ledPercent = percent
    
    def get_brightness_percent(self):
        return self.duty

    def calibrate():
        pass # do some sort of calibration with the pyranometer

    def convert_watt_to_percent(self, watt): # 1000 W/m^2 -> 100% PWM
        return ((watt / pm.MaxLedWatt) * 100)

    def set_brightness(self, watt):
        self.set_brightness_percent(self.convert_watt_to_percent(watt))



async def LEDcoroutine(file_handler: file):
    # Initialize LED
    led_control = LED(file_handler.inputFile)

    if pm.rampUp:
        timer = atimer.Timer(pm.timeStep/pm.rampUpStep)
        timer.start()
        for key, irrValue in led_control.brightnessDF.itertuples():
            nextValue = led_control.single_value(key + 1)
            for i in range(0,pm.rampUpStep, 1):
                tempValue = irrValue + ((irrValue - nextValue) * i)/pm.rampUpStep
                led_control.set_brightness(tempValue)
                msg.irrValue = tempValue
                #await asyncio.sleep(pm.timeStep/pm.rampUpStep)
                await timer
                file_handler.append_to_file()
                msg.resetBTmessages()
        
        timer.close()
    else:
        timer = atimer.Timer(pm.timeStep)
        timer.start()
        for key, irrValue in led_control.brightnessDF.itertuples():
            # Set brighness on led from file value
            led_control.set_brightness(irrValue)
            msg.irrValue = irrValue
            # Wait for next value
            #await asyncio.sleep(pm.timeStep)
            await timer
            file_handler.append_to_file()
            msg.resetBTmessages()
        
        timer.close()
    
    
    # End the other corutines
    msg.testActive = False