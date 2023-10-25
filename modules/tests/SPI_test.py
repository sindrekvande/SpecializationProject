import time
import import_modules
import SPI
import pinOut

if __name__ == '__main__':
    spi = SPI.SPI()
    
    try:
        while True:
            time.sleep(1)  # Infinite loop to keep script running and process callbacks NEED TIMER
    
    except KeyboardInterrupt:
        print("\nExiting...")
        spi.close_spi()