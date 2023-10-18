import time
import spidev
import import_modules
import SPI

if __name__ == '__main__':
    spi = SPI.SPI()

    """Init Σ-∆ data conversion"""

    print(f"Read value from 0x011: {spi.read_adc_register(0x011)}")
    """Set high resolution"""
    spi.write_adc_register(0x011, 0b01100100)
    print(f"Read value from 0x011: {spi.read_adc_register(0x011)}")

    print("-----------------------------------------------------")

    """CHx_REF_MONITOR to enable diagnostic mux"""
    print(f"Read value from CHx_CONFIG: {spi.read_adc_register(0x000)}")
    spi.write_adc_register(0x000, 0b00110000)
    spi.write_adc_register(0x001, 0b00110000)
    spi.write_adc_register(0x002, 0b00110000)
    spi.write_adc_register(0x003, 0b00110000)
    spi.write_adc_register(0x004, 0b00110000)
    spi.write_adc_register(0x005, 0b00110000)
    spi.write_adc_register(0x006, 0b00110000)
    spi.write_adc_register(0x007, 0b00110000)
    print(f"Read value from CHx_CONFIG: {spi.read_adc_register(0x000)}")

    print("-----------------------------------------------------")

    """Set SPI_SLAVE_MODE_EN"""
    print(f"Read value from CHx_CONFIG: {spi.read_adc_register(0x013)}")

    print("-----------------------------------------------------")

    """Set SPI_SLAVE_MODE_EN"""
    print(f"Read value from CHx_CONFIG: {spi.read_adc_register(0x014)}")

    #print(f"Read value from REGISTER_ADDRESS: {spi.read_adc_register()}")
    #spi.write_adc_register()
    #print(f"Read value from REGISTER_ADDRESS: {spi.read_adc_register()}")

    #print(spi.fetch_adc_data())
    
    try:
        while True:
            pass  # Infinite loop to keep script running and process callbacks
    
    except KeyboardInterrupt:
        print("\nExiting...")
        spi.close_spi()