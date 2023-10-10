import spidev
import RPi.GPIO as GPIO
import pinOut
import time

class SPI:

    NUM_CHANNELS = 8
    REGISTER_ADDRESS = 0x010
    WRITE_VALUE = 0x10

    def __init__(self, spiBus=0, spiDevice=0):
        self.setup_spi(spiBus, spiDevice)
        self.setup_gpio()
        self.reset_adc()
        GPIO.add_event_detect(pinOut.ADC1_DRDY, GPIO.FALLING, callback=self.data_ready_callback)

    def setup_spi(self, spiBus, spiDevice):
        """Setup SPI parameters."""
        self.spi = spidev.SpiDev()
        self.spi.open(spiBus, spiDevice)
        self.spi.max_speed_hz = 1950
        self.spi.mode = 0

    def setup_gpio(self):
        """Setup GPIO pins."""
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pinOut.ADC12_RESET, GPIO.OUT)
        GPIO.setup(pinOut.ADC1_DRDY, GPIO.IN)

    def reset_adc(self):
        """Reset the ADC."""
        GPIO.output(pinOut.ADC12_RESET, GPIO.LOW)
        time.sleep(0.01)
        GPIO.output(pinOut.ADC12_RESET, GPIO.HIGH)

    def data_ready_callback(self, channel):
        """Handle data ready interrupt."""
        data = self.read_adc_register()
        print("ADC Data Callback: ", data)

    def read_adc_register(self):
        """Read data from ADC register."""
        cmd = (1 << 7) | self.REGISTER_ADDRESS
        resp = self.spi.xfer2([cmd, self.REGISTER_ADDRESS])
        if len(resp) < 2:
            print("Incomplete data received from ADC!")
            return None
        return bin(resp[1])
        
    def write_adc_register(self):
        """Write data to ADC register and verify."""
        cmd = [self.REGISTER_ADDRESS, self.WRITE_VALUE]
        self.spi.xfer2(cmd)

        # Verification
        readValue = self.read_adc_register()
        if readValue != self.WRITE_VALUE:
            print(f"Write mismatch! Expected {self.WRITE_VALUE} but got {readValue} at address {self.REGISTER_ADDRESS}.")

    def close_spi(self):
        """Cleanup function."""
        self.spi.close()
        GPIO.cleanup()
    
    def fetch_adc_data(self):
        """Fetch data for all ADC channels."""
        return [self.read_adc_register() for _ in range(self.NUM_CHANNELS)]