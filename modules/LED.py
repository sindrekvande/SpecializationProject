import modules.pinOut as pinOut #LIGHT ON
import modules.pinOut_lgpio as pinOut_lgpio
import modules.SPI as SPI
#import pinOut #LIGHT OFF
import RPi.GPIO as GPIO
import pigpio
import pandas as pd
import asyncio
import atimer
from modules.file_handler import file #LIGHT ON
#from file_handler import file #LIGHT OFF
#import import_main #LIGHT OFF
import parameters as pm 
import messages as msg

class LED:
    freq = 1000 # measured as 870Hz, shouldn't affect the behaviour
    duty = 0
    dutyRange = pm.MaxLedWatt*10

    def __init__(self, file):
        #self.get_values_from_file(file)
        self.pi = pigpio.pi()
        self.pi.set_mode(pinOut_lgpio.LED_DRV_DIM, pigpio.OUTPUT)
        self.pi.set_PWM_range(pinOut_lgpio, self.dutyRange)
        self.pi.set_PWM_frequency(pinOut_lgpio.LED_DRV_DIM, self.freq)

        self.set_brightness_percent(0)
    '''
    def set_brightness_percent(self, percent): # programmed = measured: 50 = 50, 25 = 28, 75 = 73
        if percent >= 0 and percent <= 100:
            #self.pwm.ChangeDutyCycle(percent)
            self.pi.set_PWM_dutycycle(pinOut_lgpio.LED_DRV_DIM, self.dutyRange * (percent/100))
            self.duty = percent
            msg.messages[msg.ledPercent] = percent
    '''
    def get_brightness_percent(self):
        return self.duty

    def calibrate():
        pass # do some sort of calibration with the pyranometer

    #def convert_watt_to_percent(self, watt): # 1000 W/m^2 -> 100% PWM
    #    return ((watt / pm.MaxLedWatt) * 100)

    def set_brightness(self, watt):
        self.pi.set_PWM_dutycycle(pinOut_lgpio.LED_DRV_DIM, watt*10)
        self.duty = watt/pm.MaxLedWatt
        msg.messages[msg.ledPercent] = self.duty
        #self.set_brightness_percent(self.convert_watt_to_percent(watt))

async def LEDcoroutine(file_handler: file):
    # Initialize LED
    led_control = LED(file_handler.inputFile)
    spi = SPI.SPI()

    if pm.rampUp:
        timer = atimer.Timer(pm.timeStep/pm.rampUpStep)
        timer.start()
        for key, irrValue in file_handler.brightnessDF.itertuples():
            nextValue = file_handler.single_value(key + 1)
            for i in range(0,pm.rampUpStep, 1):
                tempValue = irrValue + ((irrValue - nextValue) * i)/pm.rampUpStep
                led_control.set_brightness(tempValue)
                msg.messages[msg.irrValue] = tempValue
                #await asyncio.sleep(pm.timeStep/pm.rampUpStep)
                await timer
                spi.average_and_update()
                file_handler.append_to_file()
                msg.resetBTmessages()
        
        timer.close()
    else:
        timer = atimer.Timer(pm.timeStep)
        timer.start()
        for key, irrValue in file_handler.brightnessDF.itertuples():
            # Set brighness on led from file value
            led_control.set_brightness(irrValue)
            msg.messages[msg.irrValue] = irrValue
            # Wait for next value
            #await asyncio.sleep(pm.timeStep)
            await timer
            spi.average_and_update()
            file_handler.append_to_file()
            msg.resetBTmessages()
        
        timer.close()
    
    spi.close_spi()
    GPIO.cleanup()
    # End the other corutines
    msg.messages[msg.testActive] = False