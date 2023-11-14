import spidev
import RPi.GPIO as GPIO
import modules.pinOut as pinOut
import atimer
import asyncio
#import import_main
import messages as msg
import parameters as pm
import time
from smbus2 import SMBus

class I2C:
    DEVICE_BUS = 1
    DEVICE_ADDR = 0x70
    states = []
    
    def __init__():
        #pinOut.UART_TXD # 14
        #pinOut.UART_RXD # 15
        self.setup_gpio()

        GPIO.add_event_detect(pinOut.UART_TXD, GPIO.FALLING, callback=self.data_ready_callback)

    
    def setup_gpio(self):
        """Setup GPIO pins."""
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pinOut.UART_TXD, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.setup(pinOut.UART_RXD, GPIO.OUT)
        GPIO.output(pinOut.UART_RXD, GPIO.HIGH)

    def callback(self):
        bus = SMBus(self.DEVICE_BUS)
        data = self.bus.read_byte(DEVICE_ADDR)
        self.states.append(data)
        bus.close()
        self.reset_state()

    def reset_state():
        GPIO.output(pinOut.UART_RXD, GPIO.LOW) # Insert delay if this doesn't work
        GPIO.output(pinOut.UART_RXD, GPIO.HIGH)

    def sum_states():
        resulting_list = [sum((byte >> i) & 1 for byte in self.states) for i in range(8)]
        ######################
        # Send to msg.messages
        ######################
        self.states = []


def I2Ccoroutine():
    state = I2C()

    timer = atimer.Timer(pm.timeStep/pm.rampUpStep) # substitute with mutex?
    timer.start()

    while(msg.testActive):
        await timer
        state.sum_states()
