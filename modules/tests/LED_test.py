import LED
import time

LED = LED()

while True:
    for duty in range(0, 101, 1):
        LED.set_brightness_percent(duty)
        time.sleep(0.5)
    time.sleep(1)

    for duty in range(100, -1, -1):
        LED.set_brightness_percent(duty)
        time.sleep(0.5)
    time.sleep(1)