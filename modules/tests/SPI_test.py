import time
import spidev
import import_modules
#import RPi.GPIO as GPIO
import SPI
import pigpio
import pinOut

if __name__ == '__main__':
    spi = SPI.SPI()
    
    try:
        while True:
            pass  # Infinite loop to keep script running and process callbacks
    
    except KeyboardInterrupt:
        print("\nExiting...")
        spi.close_spi()