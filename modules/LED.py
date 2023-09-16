import pinOut
import RPi.GPIO as GPIO
import pandas as pd


class LED:
    freq = 1000 # measured as 870Hz, shouldn't affect the behaviour
    duty = 0

    def __init__(self):
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

    def convert_watt_to_percent(watt): # 1000 W/m^2 -> 100% PWM
        return (watt / 1000) * 100

    def set_brightness(watt):
        set_brightness_percent(convert_watt_to_percent(watt))

    def get_values_from_file(file):
        brightness_df = pd.read_csv(file, sep='\t', usecols = ['Gg_pyr'], header=0, index_col=False, dtype = float)
        return brightness_df