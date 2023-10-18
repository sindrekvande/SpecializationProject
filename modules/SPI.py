import spidev
import RPi.GPIO as GPIO
import pinOut
import time
import asyncio

class SPI:

    NUM_CHANNELS = 8

    def __init__(self, spiBus=0, spiDevice=0):
        self.setup_spi(spiBus, spiDevice)
        self.setup_gpio()
        self.reset_adc()
        #GPIO.add_event_detect(pinOut.ADC1_DRDY, GPIO.FALLING, callback=self.data_ready_callback)

    def setup_spi(self, spiBus, spiDevice):
        """Setup SPI parameters."""
        self.spi = spidev.SpiDev()
        self.spi.open(spiBus, spiDevice)
        self.spi.max_speed_hz = 1000000
        self.spi.mode = 0

    def setup_gpio(self):
        """Setup GPIO pins."""
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pinOut.ADC12_RESET, GPIO.OUT)
        GPIO.setup(pinOut.ADC1_DRDY, GPIO.IN)

    async def reset_adc(self):
        """Reset the ADC."""
        GPIO.output(pinOut.ADC12_RESET, GPIO.LOW)
        #time.sleep(0.01)
        await asyncio.sleep(0.01)
        GPIO.output(pinOut.ADC12_RESET, GPIO.HIGH)

    def data_ready_callback(self, channel):
        """Handle data ready interrupt."""
        data = self.read_adc_register(0x011)
        print("ADC Data Callback: ", data)

    def read_adc_register(self, address):
        """Read data from ADC register."""
        cmd = (1 << 7) | address
        resp = self.spi.xfer([cmd, 0x00, 0x00, 0x00])
        if len(resp) < 2:
            print("Incomplete data received from ADC!")
            return None
        #return [bin(resp[0]), bin(resp[1]), bin(resp[2]), bin(resp[3])]
        return bin(resp[1])
        
    def write_adc_register(self, address, value):
        """Write data to ADC register and verify."""
        cmd = [address, value]
        self.spi.xfer(cmd)

        # Verification
        readValue = self.read_adc_register(address)
        if readValue != bin(value):
            print(f"Write mismatch! Expected {bin(value)} but got {readValue} at address {hex(address)}.")
        else:
            print(f"Write succesfull! {bin(value)} at address {hex(address)}.")

    def close_spi(self):
        """Cleanup function."""
        self.spi.close()
        GPIO.cleanup()
    
    def fetch_adc_data(self):
        """Fetch data for all ADC channels."""
        return [self.read_adc_register(0x000) for _ in range(self.NUM_CHANNELS)]