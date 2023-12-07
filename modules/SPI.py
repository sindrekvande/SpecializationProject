import spidev
import RPi.GPIO as GPIO
import modules.pinOut as pinOut
import atimer
import asyncio
#import import_main
import messages as msg
import time

class SPI:
    adc1_ch0_values = []
    adc1_ch1_values = []
    adc1_ch2_values = []
    adc1_ch3_values = []
    adc1_ch4_values = []
    adc1_ch5_values = []
    adc1_ch6_values = []
    adc1_ch7_values = []
    adc2_ch0_values = []
    adc2_ch1_values = []
    adc2_ch2_values = []
    adc2_ch3_values = []
    adc2_ch4_values = []
    adc2_ch5_values = []
    adc2_ch6_values = []
    adc2_ch7_values = []

    output = []

    def __init__(self): 
        self.spi = spidev.SpiDev()
        self.setup_gpio()

        self.reset_adc()

        self.setup_spi(1000000, 0)
        self.write_adc_internal_register(0x011, 0b01100100, self.spi) #High Resolution Mode  
        self.close_spi()

        self.setup_spi(1000000, 1)
        self.write_adc_internal_register(0x011, 0b01100100, self.spi) #High Resolution Mode  
        self.close_spi()

        self.setup_spi(10000000, 0)
        self.write_adc_sigma_delta(0x013, 0b10010000, self.spi) #Set SD-output
        self.close_spi()

        self.setup_spi(10000000, 1)
        self.write_adc_sigma_delta(0x013, 0b10010000, self.spi) #Set SD-output
        self.close_spi()

        self.setup_spi(10000000, 0)
        self.write_adc_sigma_delta(0x012, 0b00001000, self.spi) #Synchronize ADCs
        self.write_adc_sigma_delta(0x012, 0b00001001, self.spi) #Synchronize ADCs
        self.close_spi()

        GPIO.add_event_detect(pinOut.ADC1_DRDY, GPIO.FALLING, callback=self.data_ready_callback)
        
    def setup_spi(self, frequency, spiDevice, spiBus = 0):
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
        self.setup_spi(12500000, 0)
        self.response1 = self.spi.xfer2([0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
        self.close_spi()

        self.setup_spi(12500000, 1)
        self.response2 = self.spi.xfer2([0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
        self.close_spi()

        self.output_value(self.response1, self.response2)

    def read_adc_register(self, address, spi):
        """Read data from ADC register."""
        cmd = (1 << 7) | address
        resp = spi.xfer2([cmd, 0x00])
        if len(resp) < 2:
            print("Incomplete data received from ADC!")
            return None
        return [bin(resp[0]), bin(resp[1])]
        
    def write_adc_internal_register(self, address, value, spi):
        """Write data to ADC register and verify, under internal register mode."""
        cmd = [address, value]
        spi.xfer2(cmd)

        # Verification
        readValue = self.read_adc_register(address, spi)
        if readValue[1] != bin(value):
            print(f"Write mismatch! Expected {bin(value)} but got {readValue[1]} at address {hex(address)}. Header: {readValue[0]}")
        else:
            print(f"Write succesfull! {bin(value)} at address {hex(address)}.")

    def write_adc_sigma_delta(self, address, value, spi):
        """Write data to ADC register under sigma-delta mode."""
        cmd = [address, value]
        spi.xfer2(cmd)

    def output_value(self, response1, response2):
        for i in range(8):

            adc1_dec_channel = [response1[1 + i * 4], response1[2 + i * 4], response1[3 + i * 4]]
            adc2_dec_channel = [response2[1 + i * 4], response2[2 + i * 4], response2[3 + i * 4]]
            adc1_hex_channel = [hex(d)[2:].zfill(2) for d in adc1_dec_channel]
            adc2_hex_channel = [hex(d)[2:].zfill(2) for d in adc2_dec_channel]
            adc1_hex_string_channel = ''.join(adc1_hex_channel)
            adc2_hex_string_channel = ''.join(adc2_hex_channel)

            #adc1_voltage_channel = (int(adc1_hex_string_channel, 16) - 3760000) / 1360000
            #adc2_voltage_channel = (int(adc2_hex_string_channel, 16) - 3760000) / 1360000
            adc1_voltage_channel = (int(adc1_hex_string_channel, 16) / int(0x800000)) * 3.3
            adc2_voltage_channel = (int(adc2_hex_string_channel, 16) / int(0x800000)) * 3.3

            if adc1_voltage_channel > 3.3:
                adc1_voltage_channel -= 6.6

            if adc2_voltage_channel > 3.3:
                adc2_voltage_channel -= 6.6

            #print(adc2_voltage_channel)

            if i == 0:
                self.adc1_ch0_values.append(adc1_voltage_channel)
                self.adc2_ch0_values.append(adc2_voltage_channel)
            elif i == 1:
                self.adc1_ch1_values.append(adc1_voltage_channel) #Voltage related to current, but not current?
                self.adc2_ch1_values.append(adc2_voltage_channel)
            elif i == 2:
                self.adc1_ch2_values.append(adc1_voltage_channel)
                self.adc2_ch2_values.append(adc2_voltage_channel)
            elif i == 3:
                self.adc1_ch3_values.append(adc1_voltage_channel)
                self.adc2_ch3_values.append(adc2_voltage_channel / (8.06 * 25)) #current
            elif i == 4:
                self.adc1_ch4_values.append(adc1_voltage_channel)
                self.adc2_ch4_values.append(adc2_voltage_channel / (4.02 * 25)) #current
            elif i == 5:
                self.adc1_ch5_values.append(adc1_voltage_channel)
                self.adc2_ch5_values.append(adc2_voltage_channel / (4.02 * 25)) #current
            elif i == 6:
                self.adc1_ch6_values.append(adc1_voltage_channel)
                self.adc2_ch6_values.append(adc2_voltage_channel / (8.06 * 25)) #current
            elif i == 7:
                self.adc1_ch7_values.append(adc1_voltage_channel)
                self.adc2_ch7_values.append(adc2_voltage_channel / (8.06 * 25)) #current
            

            #setattr(self, f'adc1_ch{i}_values', getattr(self, f'adc1_ch{i}_values', []) + [adc1_voltage_channel])
            #setattr(self, f'adc2_ch{i}_values', getattr(self, f'adc2_ch{i}_values', []) + [adc2_voltage_channel])
    def average_and_update(self):
        for i in range(8):
                if i == 0:
                    adc1_channel_sums = sum(self.adc1_ch0_values)
                    adc2_channel_sums = sum(self.adc2_ch0_values)
                    adc1_channel_lengths = len(self.adc1_ch0_values)
                    adc2_channel_lengths = len(self.adc2_ch0_values)
                    self.adc1_ch0_values = []
                    self.adc2_ch0_values = []
                elif i == 1:
                    adc1_channel_sums = sum(self.adc1_ch1_values)
                    adc2_channel_sums = sum(self.adc2_ch1_values)
                    adc1_channel_lengths = len(self.adc1_ch1_values)
                    adc2_channel_lengths = len(self.adc2_ch1_values)
                    self.adc1_ch1_values = []
                    self.adc2_ch1_values = []
                elif i == 2:
                    adc1_channel_sums = sum(self.adc1_ch2_values)
                    adc2_channel_sums = sum(self.adc2_ch2_values)
                    adc1_channel_lengths = len(self.adc1_ch2_values)
                    adc2_channel_lengths = len(self.adc2_ch2_values)
                    self.adc1_ch2_values = []
                    self.adc2_ch2_values = []
                elif i == 3:
                    adc1_channel_sums = sum(self.adc1_ch3_values)
                    adc2_channel_sums = sum(self.adc2_ch3_values)
                    adc1_channel_lengths = len(self.adc1_ch3_values)
                    adc2_channel_lengths = len(self.adc2_ch3_values)
                    self.adc1_ch3_values = []
                    self.adc2_ch3_values = []
                elif i == 4:
                    adc1_channel_sums = sum(self.adc1_ch4_values)
                    adc2_channel_sums = sum(self.adc2_ch4_values)
                    adc1_channel_lengths = len(self.adc1_ch4_values)
                    adc2_channel_lengths = len(self.adc2_ch4_values)
                    self.adc1_ch4_values = []
                    self.adc2_ch4_values = []
                elif i == 5:
                    adc1_channel_sums = sum(self.adc1_ch5_values)
                    adc2_channel_sums = sum(self.adc2_ch5_values)
                    adc1_channel_lengths = len(self.adc1_ch5_values)
                    adc2_channel_lengths = len(self.adc2_ch5_values)
                    self.adc1_ch5_values = []
                    self.adc2_ch5_values = []
                elif i == 6:
                    adc1_channel_sums = sum(self.adc1_ch6_values)
                    adc2_channel_sums = sum(self.adc2_ch6_values)
                    adc1_channel_lengths = len(self.adc1_ch6_values)
                    adc2_channel_lengths = len(self.adc2_ch6_values)
                    self.adc1_ch6_values = []
                    self.adc2_ch6_values = []
                elif i == 7:
                    adc1_channel_sums = sum(self.adc1_ch7_values)
                    adc2_channel_sums = sum(self.adc2_ch7_values)
                    adc1_channel_lengths = len(self.adc1_ch7_values)
                    adc2_channel_lengths = len(self.adc2_ch7_values)
                    self.adc1_ch7_values = []
                    self.adc2_ch7_values = []

                #adc1_channel_value = adc1_channel_sums[i] / adc1_channel_lengths[i]
                #adc2_channel_value = adc2_channel_sums[i] / adc2_channel_lengths[i]
                adc1_channel_value = adc1_channel_sums / adc1_channel_lengths
                adc2_channel_value = adc2_channel_sums / adc2_channel_lengths

                #setattr(spi, f'adc1_ch{i}_values', [])
                #setattr(spi, f'adc2_ch{i}_values', [])

                msg.messages[msg.adc_channels[i]] = adc1_channel_value
                msg.messages[msg.adc_channels[i+8]] = adc2_channel_value

    def close_spi(self):
        """Cleanup function."""
        self.spi.close()

async def SPIcoroutine():
    spi = SPI()

    try:
        timer = atimer.Timer(1)
        timer.start()

        timeout = 5
        start_time = time.time()

        while msg.testActive:
            await timer
            #adc1_channel_sums = spi.adc2_ch1_values[0]
            #adc2_channel_sums = spi.adc2_ch2_values[0]
            #adc1_channel_sums = [sum(getattr(spi, f'adc1_ch{i}_values')) for i in range(8)]
            #adc2_channel_sums = [sum(getattr(spi, f'adc2_ch{i}_values')) for i in range(8)]
            #adc1_channel_lengths = [len(getattr(spi, f'adc1_ch{i}_values')) for i in range(8)]
            #adc2_channel_lengths = [len(getattr(spi, f'adc2_ch{i}_values')) for i in range(8)]

            for i in range(8):
                if i == 0:
                    adc1_channel_sums = sum(spi.adc1_ch0_values)
                    adc2_channel_sums = sum(spi.adc2_ch0_values)
                    adc1_channel_lengths = len(spi.adc1_ch0_values)
                    adc2_channel_lengths = len(spi.adc2_ch0_values)
                    spi.adc1_ch0_values = []
                    spi.adc2_ch0_values = []
                elif i == 1:
                    adc1_channel_sums = sum(spi.adc1_ch1_values)
                    adc2_channel_sums = sum(spi.adc2_ch1_values)
                    adc1_channel_lengths = len(spi.adc1_ch1_values)
                    adc2_channel_lengths = len(spi.adc2_ch1_values)
                    spi.adc1_ch1_values = []
                    spi.adc2_ch1_values = []
                elif i == 2:
                    adc1_channel_sums = sum(spi.adc1_ch2_values)
                    adc2_channel_sums = sum(spi.adc2_ch2_values)
                    adc1_channel_lengths = len(spi.adc1_ch2_values)
                    adc2_channel_lengths = len(spi.adc2_ch2_values)
                    spi.adc1_ch2_values = []
                    spi.adc2_ch2_values = []
                elif i == 3:
                    adc1_channel_sums = sum(spi.adc1_ch3_values)
                    adc2_channel_sums = sum(spi.adc2_ch3_values)
                    adc1_channel_lengths = len(spi.adc1_ch3_values)
                    adc2_channel_lengths = len(spi.adc2_ch3_values)
                    spi.adc1_ch3_values = []
                    spi.adc2_ch3_values = []
                elif i == 4:
                    adc1_channel_sums = sum(spi.adc1_ch4_values)
                    adc2_channel_sums = sum(spi.adc2_ch4_values)
                    adc1_channel_lengths = len(spi.adc1_ch4_values)
                    adc2_channel_lengths = len(spi.adc2_ch4_values)
                    spi.adc1_ch4_values = []
                    spi.adc2_ch4_values = []
                elif i == 5:
                    adc1_channel_sums = sum(spi.adc1_ch5_values)
                    adc2_channel_sums = sum(spi.adc2_ch5_values)
                    adc1_channel_lengths = len(spi.adc1_ch5_values)
                    adc2_channel_lengths = len(spi.adc2_ch5_values)
                    spi.adc1_ch5_values = []
                    spi.adc2_ch5_values = []
                elif i == 6:
                    adc1_channel_sums = sum(spi.adc1_ch6_values)
                    adc2_channel_sums = sum(spi.adc2_ch6_values)
                    adc1_channel_lengths = len(spi.adc1_ch6_values)
                    adc2_channel_lengths = len(spi.adc2_ch6_values)
                    spi.adc1_ch6_values = []
                    spi.adc2_ch6_values = []
                elif i == 7:
                    adc1_channel_sums = sum(spi.adc1_ch7_values)
                    adc2_channel_sums = sum(spi.adc2_ch7_values)
                    adc1_channel_lengths = len(spi.adc1_ch7_values)
                    adc2_channel_lengths = len(spi.adc2_ch7_values)
                    spi.adc1_ch7_values = []
                    spi.adc2_ch7_values = []

                #adc1_channel_value = adc1_channel_sums[i] / adc1_channel_lengths[i]
                #adc2_channel_value = adc2_channel_sums[i] / adc2_channel_lengths[i]
                adc1_channel_value = adc1_channel_sums / adc1_channel_lengths
                adc2_channel_value = adc2_channel_sums / adc2_channel_lengths

                #setattr(spi, f'adc1_ch{i}_values', [])
                #setattr(spi, f'adc2_ch{i}_values', [])

                msg.messages[msg.adc_channels[i]] = adc1_channel_value
                msg.messages[msg.adc_channels[i+8]] = adc2_channel_value
                
            #if time.time() - start_time >= timeout:
            #    break

        timer.close()
        spi.close_spi()
        GPIO.cleanup()
    
    except KeyboardInterrupt:
        print("\nExiting...")
        timer.close()
        spi.close_spi()
        GPIO.cleanup()
    