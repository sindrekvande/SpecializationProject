import pinOut
import spidev
import RPi.GPIO as GPIO

class SPI:
    def __init__(self, spi_bus = 0, ce_pin = 0):
        """
        Initializes the device, takes SPI bus address (0 on newer Raspberry models)
        Sets the channel to either CE= = 0 (GPIO 8) or CE1 = 1 (GPIO 7)
        """

        if spi_bus not in [0,1]:
            raise ValueError('wrong SPI-bus: {0} setting (use 0 or 1)!'.format(spi_bus))

        if ce_pin not in [0,1]:
            raise ValueError('wrong CE-setting: {0} setting (use 0 for CE0 or 1 for CE1)!'.format(ce_pin))

        self.spi = spidev.SpiDev()
        self.spi.open(spi_bus, ce_pin)
        self.spi.max_speed_hz = 976000 #Default = 125000000 (too high?)

        pass

    #def trans(self, payload = 0x00):
    #    self.spi.open(bus, device)
    #    ret = self.spi.xfer(payload)
    #    self.spi.close()
    #    return ret

    def adc_transaction(self, adc_channel, payload = [0x00, 0x00]):
        """
        Read SPI data from ADC, 8 channels
        """
        if adc_channel > 7 or adc_channel < 0:
            return -1

        bytes_received = self.spi.xfer2(payload) #TESTVERDIER BRUKES NÅ

        MSB_1 = bytes_received[1]
        MSB_1 = MSB_1 >> 1

        MSB_0 = bytes_received[0] & 0b00011111
        MSB_0 MSB_0 << 7

        return MSB_0 + MSB_1

    def convert_to_voltage(self, adc_output, vref=3.3):
        """
        Converts analouge voltage from digital output (0-4095)
        Vref could be adhusted (standard 3V3 rail Rpi)
        """
        return adc_output * (vref / (2 ** 12 - 1))

    def close_spi(self):
        self.spi.close()