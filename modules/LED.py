import pinOut
import RPi.GPIO as GPIO

class LED:
    freq = 1000
    duty = 0

    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pinOut.LED_DRV_DIM,GPIO.OUT)
        self.pwm = GPIO.PWM(pinOut.LED_DRV_DIM,self.freq)
        self.pwm.start(self.duty)

    def set_brightness_percent(self, percent):
        if percent >= 0 and percent <= 100:
            self.pwm.ChangeDutyCycle(percent)
            self.duty = percent
    
    def get_brightness_percent(self):
        return self.duty