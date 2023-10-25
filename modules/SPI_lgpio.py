import lgpio as sbc
import pinOut_lgpio
import time
import asyncio

class SPI:

    NUM_CHANNELS = 8
    counter = 0

    def __init__(self): #spiDevice=0 (ADC1), spiDevice=1 (ADC2)
        handle_gpio = gpiochip_open(0)
        handle_spi = spi_open(1, 0, 50000, 0)
    
        self.setup_gpio()
        self.reset_adc()

    def setup_gpio(self):
        """Setup GPIO pins."""
        sbc.gpio_claim_output(self.handle_gpio, pinOut_lgpio.ADC12_RESET)
        sbc.gpio_claim_alert(self.handle_gpio, pinOut_lgpio.ADC1_DRDY, sbc.FALLING_EDGE)
        sbc.gpio_claim_output(self.handle_gpio, pinOut_lgpio.RPI_GPIO_22)

    def reset_adc(self):
        """Reset the ADC."""
        sbc.gpio_write(self.handle_gpio, pinOut_lgpio.ADC12_RESET, 0)
        time.sleep(0.01)
        sbc.gpio_write(self.handle_gpio, pinOut_lgpio.ADC12_RESET, 1)
        time.sleep(0.01)

    def cbf(self, chip, gpio, level, tick):
        """Handle data ready interrupt."""

        sbc.gpio_write(pinOut_lgpio.RPI_GPIO_22, 0)
        sbc.gpio_write(pinOut_lgpio.RPI_GPIO_22, 1)
        sbc.gpio_write(pinOut_lgpio.RPI_GPIO_22, 0)

if __name__ == '__main__':
    spi = SPI()

    sbc.callback(spi.handle_gpio, pinOut_lgpio.ADC1_DRDY, sbc.FALLING_EDGE, spi.cbf)
    
    try:
        while True:
            time.sleep(1)  # Infinite loop to keep script running and process callbacks NEED TIMER
    
    except KeyboardInterrupt:
        print("\nExiting...")