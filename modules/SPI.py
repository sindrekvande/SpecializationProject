import pinOut
import spidev
import RPi.GPIO as GPIO

class SPI:
    def __init__(self, bus = 0, device = 0):
        self.bus = bus
        self.device = device
        self.spi = spidev.SpiDev()

    def trans(self, payload = 0x00):
        self.spi.open(bus, device)
        ret = self.spi.xfer(payload)
        self.spi.close()
        return ret