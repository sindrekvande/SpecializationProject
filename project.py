import time
import concurrent.futures
import spidev
import RPi.GPIO as GPIO

def SPI_init():
    bus = 0
    device = 1
    spi = spidev.SpiDev()
    spi.open(bus, device)

def SPI_trans(payload):
    return spi.xfer(payload)

def ADC_read(dev, reg_addr, reg_data):
    SPI_trans(dev)

def PWM_init():
    LED_driver1 = 33
    LED_driver2 = 35
    freq = 100
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(LED_driver1,GPIO.OUT)
    GPIO.setup(LED_driver2,GPIO.OUT)
    pwm1 = GPIO.PWM(LED_driver1,freq)
    pwm2 = GPIO.PWM(LED_driver2,freq)
    pwm1.start(0)
    pwm2.start(0)
    return pwm1, pwm2

def PWM_set_percent(channel,percent, pwm):
    if channel == 1:
        pwm.ChangeDutyCycle(percent)
    else:
        pwm.ChangeDutyCycle(percent)

print("starting...")

pwm1, pwm2 = PWM_init()

while True:
    for duty in range(0, 101, 1):
        PWM_set_percent(1, duty, pwm1)
        PWM_set_percent(2, 100-duty, pwm2)
        time.sleep(0.5)
    time.sleep(1)

    for duty in range(100, -1, -1):
        PWM_set_percent(1, duty, pwm1)
        PWM_set_percent(2, 100-duty, pwm2)
        time.sleep(0.5)
    time.sleep(1)