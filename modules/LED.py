import pinOut
import RPi.GPIO as GPIO
import pandas as pd
import menu
from tests import import_path
import parameters as pm

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
        self.brightness_df = pd.read_csv(file, sep='\t', usecols = [pm.column],  dtype = float, nrows = (pm.numberOfDays*60*24)) # header=0, index_col=False, 
        return self.brightness_df

    def __str__(self):
        self.brightness_df

    def singe_value(self, index):
        return self.brightness_df.iat[index, pm.column]

    def filter_NaN_values(self):
        for key, value in led_control.brightness_df.items():
            irrValue + ((irrValue - nextValue) * i)/pm.rampUpStep
            if pd.isna(value):
                filtered_df = 