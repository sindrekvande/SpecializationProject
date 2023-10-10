import time
import spidev
import import_modules
import SPI

if __name__ == '__main__':
    spi = SPI.SPI()
    
    #adc.write_adc_register()
    #print(f"Read value from REGISTER_ADDRESS: {adc.read_adc_register()}")

    #print(adc.fetch_adc_data())
    
    try:
        while True:
            pass  # Infinite loop to keep script running and process callbacks
    
    except KeyboardInterrupt:
        print("\nExiting...")
        spi.close_spi()