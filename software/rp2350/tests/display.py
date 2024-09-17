import sys
import time

from machine import I2C
from machine import Pin
from ssd1306 import SSD1306_I2C

OLED_SDA = 0
OLED_SCL = 1
OLED_WIDTH = 128
OLED_HEIGHT = 32
I2C_CHANNEL = 0
I2C_FREQUENCY = 400000

i2c = I2C(I2C_CHANNEL, sda=Pin(OLED_SDA), scl=Pin(OLED_SCL), freq=I2C_FREQUENCY)

if len(i2c.scan()) == 0:
    print("ERROR: OLED display not found")
    sys.exit()

display = SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c)

display.fill(0)
display.text("Hi from Europi", 0, 0)
display.text("running RP2350", 0, 12)
display.show()

time.sleep(10)
display.poweroff()
