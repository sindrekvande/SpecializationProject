import pinOut
import RPi.GPIO as GPIO
import SPI

class ADC(SPI):
    def __init__(self, bus = 0, device = 0):
        super().__init__(bus, device)