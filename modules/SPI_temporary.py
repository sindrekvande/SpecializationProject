import spidev
import RPi.GPIO as GPIO
import pinOut
import time

class SPI:

    NUM_CHANNELS = 8

    def __init__(self, spiBus=0, spiDevice=0):
        self.setup_spi(spiBus, spiDevice)
        self.setup_gpio()
        self.reset_adc()
        #GPIO.add_event_detect(pinOut.ADC1_DRDY, GPIO.FALLING, callback=self.data_ready_callback)

    #def __init__(self, spi_bus=0, spi_device=0):
    #    # SPI setup
    #    self.spi = spidev.SpiDev()
    #    self.spi.open(spi_bus, spi_device)
    #    self.spi.max_speed_hz = 1950  # Set SPI speed (modify as needed)
    #    self.spi.mode = 0
#
    #    # GPIO setup
    #    GPIO.setmode(GPIO.BOARD)  # Use BOARD numbering
#
    #    GPIO.setup(pinOut.ADC12_RESET, GPIO.OUT)
    #    GPIO.setup(pinOut.ADC1_DRDY, GPIO.IN)
#
    #    # Reset ADC on initialization
    #    self.reset_adc()
#
    #    # Set up an interrupt on the falling edge of DRDY
    #    GPIO.add_event_detect(pinOut.ADC1_DRDY, GPIO.FALLING, callback=self.data_ready_callback)

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
        data = self.read_adc_register(0x000) 
        print(f"ADC Data Callback: {data}")

    def read_adc_register(self, address):
        """Read data from ADC register."""
        cmd = (1 << 7) | address
        resp = self.spi.xfer2([cmd, 0x00])
        if len(resp) < 2:
            print("Incomplete data received from ADC!")
            return None
        return resp[1]
        
    def write_adc_register(self, address, value):
        """Write data to ADC register and verify."""
        cmd = [address, value]
        self.spi.xfer2(cmd)

        # Verification
        readValue = self.read_adc_register(address)
        if readValue != value:
            print(f"Write mismatch! Expected {value} but got {readValue} at address {address}.")

    def close_spi(self):
        """Cleanup function."""
        self.spi.close()
        GPIO.cleanup()
    
    def fetch_adc_data(self):
        """Fetch data for all ADC channels."""
        return [self.read_adc_register(0x000) for _ in range(self.NUM_CHANNELS)]

if __name__ == '__main__':
    adc = SPI()

    adc.write_adc_register(0x000, 0x00)
    print(f"Read value from register 0x000: {adc.read_adc_register(0x000)}")

    adc.write_adc_register(0x000, 0x10)
    print(f"Read value from register 0x000: {adc.read_adc_register(0x000)}")

    adc.write_adc_register(0x001, 0x20)
    print(f"Read value from register 0x001: {adc.read_adc_register(0x001)}")

    adc.write_adc_register(0x001, 0x30)
    print(f"Read value from register 0x001: {adc.read_adc_register(0x001)}")
    
    try:
        while True:
            pass  # Infinite loop to keep script running and process callbacks
    
    except KeyboardInterrupt:
        print("\nExiting...")
        adc.close()