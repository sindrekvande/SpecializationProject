import time
import spidev
import import_path
import SPI

if __name__ == '__main__':
    SPI = SPI.SPI()

    try:
        while True:
            adc_output = SPI.adc_transaction(0)
            adc_voltage = SPI.convert_to_voltage(adc_output)
            print("ADC output: %d" % adc_output)
            print("ADC voltage: %0.2f V \n" % adc_voltage)

            time.sleep(1)

    except (KeyboardInterupt):
        print('\n', "Exit on Ctrl-C")

    except:
        print("Other error or exception")
        raise
