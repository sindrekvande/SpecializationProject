import spidev
import RPi.GPIO as GPIO
import modules.pinOut as pinOut
import atimer
import asyncio
#import import_main
import messages as msg
import time

class SPI:

    NUM_CHANNELS = 8
    responses = []
    ch0_values = []
    ch1_values = []
    ch2_values = []
    ch3_values = []
    ch4_values = []
    ch5_values = []
    ch6_values = []
    ch7_values = []
    counter = 0

    def __init__(self): #spiDevice=0 (ADC1), spiDevice=1 (ADC2)
        self.spi = spidev.SpiDev()
        self.setup_spi(0, 0, 1000000)
        self.setup_gpio()
        self.reset_adc()
        
        #self.write_adc_register(0x014, 0b00000000) #Set status header
        self.write_adc_register(0x011, 0b01100100) #High Resolution Mode
        
        self.close_spi()

        self.setup_spi(0, 1, 20000000)
        self.setup_gpio()

        print(f"Channel 0 status register: {self.read_adc_register(0x04c)}")
        print(f"Channel 1 status register: {self.read_adc_register(0x04d)}")
        print(f"Channel 2 status register: {self.read_adc_register(0x04e)}")
        print(f"Channel 3 status register: {self.read_adc_register(0x04f)}")
        print(f"Channel 4 status register: {self.read_adc_register(0x050)}")
        print(f"Channel 5 status register: {self.read_adc_register(0x051)}")
        print(f"Channel 6 status register: {self.read_adc_register(0x052)}")
        print(f"Channel 7 status register: {self.read_adc_register(0x053)}")

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

    def reset_adc(self):
        """Reset the ADC."""
        GPIO.output(pinOut.ADC12_RESET, GPIO.LOW)
        time.sleep(0.01)
        GPIO.output(pinOut.ADC12_RESET, GPIO.HIGH)
        time.sleep(0.01)

    def data_ready_callback(self, channel):
        """Handle data ready interrupt."""
        self.response = self.spi.xfer2([0x8000, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
        self.output_value(self.response)

    def read_adc_register(self, address):
        """Read data from ADC register."""
        cmd = (1 << 7) | address
        resp = self.spi.xfer2([cmd, 0x00])
        if len(resp) < 2:
            print("Incomplete data received from ADC!")
            return None
        return [bin(resp[0]), bin(resp[1])]
        
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

    def output_value(self, response):
        channel_offset = 0

        for i in range(8):
            dec_channel = [self.response[1 + i * 4], self.response[2 + i * 4], self.response[3 + i * 4]]
            hex_channel = [hex(d)[2:].zfill(2) for d in dec_channel]
            hex_string_channel = ''.join(hex_channel)
            voltage_channel = (int(hex_string_channel, 16) / 8388607) * 2.499999702

            setattr(self, f'ch{i}_values', getattr(self, f'ch{i}_values', []) + [voltage_channel])

    def close_spi(self):
        """Cleanup function."""
        self.spi.close()
        GPIO.cleanup()

async def SPIcoroutine():
    spi = SPI()

    try:
        timer = atimer.Timer(1)
        timer.start()

        timeout = 5
        start_time = time.time()

        while msg.testActive:
            await timer
            channel_sums = [sum(getattr(spi, f'ch{i}_values')) for i in range(8)]
            channel_lengths = [len(getattr(spi, f'ch{i}_values')) for i in range(8)]

            for i in range(8):
                channel_value = channel_sums[i] / channel_lengths[i]
                setattr(spi, f'ch{i}_values', [])
                print(len(spi.ch2_values))
                print(channel_value)

                if i == 0:
                    msg.adc2ch0 = channel_value
                elif i == 1:
                    msg.adc2ch1 = channel_value
                elif i == 2:
                    msg.adc2ch2 = channel_value
                elif i == 3:
                    msg.adc2ch1 = channel_value
                elif i == 4:
                    msg.adc2ch2 = channel_value
                elif i == 5:
                    msg.adc2ch1 = channel_value
                elif i == 6:
                    msg.adc2ch2 = channel_value
                elif i == 7:
                    msg.adc2ch1 = channel_value

            #if time.time() - start_time >= timeout:
            #    break

        #print(msg.adc2ch2)
        timer.close()
        spi.close_spi()
    
    except KeyboardInterrupt:
        print("\nExiting...")
        timer.close()
        spi.close_spi()
    