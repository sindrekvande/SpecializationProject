import time
import sys
import os

absolute_path = os.path.dirname(__file__)
relative_path = ".."
full_path = os.path.join(absolute_path, relative_path)
sys.path.insert(0, full_path)

import LED

LED = LED.LED()

def test1(LED):
    while True:
        for duty in range(0, 101, 1):
            LED.set_brightness_percent(duty)
            time.sleep(0.5)
        time.sleep(1)

        for duty in range(100, -1, -1):
            LED.set_brightness_percent(duty)
            time.sleep(0.5)
        time.sleep(1)

def test2(LED):
    LED.set_brightness_percent(50)
    while True:
        time.sleep(1)

test2(LED)
