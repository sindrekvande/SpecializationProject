import spidev
import RPi.GPIO as GPIO
import pinOut
import time
import asyncio

class SPI:

    NUM_CHANNELS = 8
    counter = 0

    def __init__(self): #spiDevice=0 (ADC1), spiDevice=1 (ADC2)
        self.spi = spidev.SpiDev()
        self.setup_spi(0, 0, 1000000)
        self.setup_gpio()
        self.reset_adc()
        
        self.write_adc_register(0x014, 0b00000000) #Divide clock
        self.write_adc_register(0x011, 0b01100100) #High Resolution Mode
        
        self.close_spi()

        self.setup_spi(0, 1, 25000000)
        self.setup_gpio()


        self.write_adc_register(0x013, 0b10010000) #Set SD-output

        GPIO.add_event_detect(pinOut.ADC1_DRDY, GPIO.FALLING, callback=self.data_ready_callback)
        
    def setup_spi(self, spiBus, spiDevice, frequency):
        """Setup SPI parameters."""
        self.spi.open(spiBus, spiDevice)
        self.spi.max_speed_hz = frequency
        self.spi.mode = 0

    def setup_gpio(self):
        """Setup GPIO pins."""
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pinOut.ADC12_RESET, GPIO.OUT)
        GPIO.setup(pinOut.ADC1_DRDY, GPIO.IN)
        GPIO.setup(pinOut.SPI_1_CS_ADC1, GPIO.OUT)
        GPIO.setup(pinOut.SPI_1_CS_ADC2, GPIO.OUT)
        GPIO.setup(pinOut.RPI_GPIO_22, GPIO.OUT)

    def reset_adc(self):
        """Reset the ADC."""
        GPIO.output(pinOut.ADC12_RESET, GPIO.LOW)
        time.sleep(0.01)
        #await asyncio.sleep(0.01)
        GPIO.output(pinOut.ADC12_RESET, GPIO.HIGH)
        time.sleep(0.01)

    def data_ready_callback(self, channel):
        """Handle data ready interrupt."""
        #self.counter += 1
        # Disable DRDY interrupt
        #GPIO.remove_event_detect(pinOut.ADC1_DRDY)
        #print("---------------------------------------------")
        #print("----")
        #for i in range(self.NUM_CHANNELS):
        resp = self.spi.xfer2([0x8000, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,0x00, 0x00])
        #callback_result = [[bin(resp[0]), bin(resp[1]), bin(resp[2]), bin(resp[3])],
        #                   [bin(resp[4]), bin(resp[5]), bin(resp[6]), bin(resp[7])], 
        #                   [bin(resp[8]), bin(resp[9]), bin(resp[10]), bin(resp[11])],
        #                   [bin(resp[12]), bin(resp[13]), bin(resp[14]), bin(resp[15])],
        #                   [bin(resp[16]), bin(resp[17]), bin(resp[18]), bin(resp[19])],
        #                   [bin(resp[20]), bin(resp[21]), bin(resp[22]), bin(resp[23])],
        #                   [bin(resp[24]), bin(resp[25]), bin(resp[26]), bin(resp[27])],
        #                   [bin(resp[28]), bin(resp[29]), bin(resp[30]), bin(resp[31])]]
        #
        #return print(callback_result)

        #GPIO.output(pinOut.RPI_GPIO_22, GPIO.LOW)
        #GPIO.output(pinOut.RPI_GPIO_22, GPIO.HIGH)
        #GPIO.output(pinOut.RPI_GPIO_22, GPIO.LOW)

    def read_adc_register(self, address):
        """Read data from ADC register."""
        cmd = (1 << 7) | address
        resp = self.spi.xfer2([cmd, 0x00])
        if len(resp) < 2:
            print("Incomplete data received from ADC!")
            return None
        return [bin(resp[0]), bin(resp[1])]
        #return bin(resp[1])
        
    def write_adc_register(self, address, value):
        """Write data to ADC register and verify."""
        cmd = [address, value]
        self.spi.xfer2(cmd)

        # Verification
        readValue = self.read_adc_register(address)
        if readValue[1] != bin(value):
            print(f"Write mismatch! Expected {bin(value)} but got {readValue[1]} at address {hex(address)}. Header: {readValue[0]}")
        else:
            print(f"Write succesfull! {bin(value)} at address {hex(address)}.")

    def close_spi(self):
        """Cleanup function."""
        self.spi.close()
        GPIO.cleanup()
    