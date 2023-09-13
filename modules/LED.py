import pinOut
import RPi.GPIO as GPIO

class LED:
    def init():
        freq = 1000
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(LED_driver1,GPIO.OUT)
        pwm1 = GPIO.PWM(LED_driver1,freq)
        pwm1.start(0)

    def set_brightness_percent(percent):
        if percent >= 0 and percent <= 100:
            self.ChangeDutyCycle(percent)