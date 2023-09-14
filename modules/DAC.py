import pinOut
import RPi.GPIO as GPIO
import SPI

class DAC(SPI):
    def __init__(self, bus = 1, device = 0):
        super().__init__(bus, device)