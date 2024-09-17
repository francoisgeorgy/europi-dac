from machine import Pin, I2C
from mcp4728 import MCP4728
from ssd1306 import SSD1306_I2C
from time import sleep

if __name__ == "__main__":

    DAC_ADDR = 0x60

    oled = SSD1306_I2C(128, 32, I2C(0, sda=Pin(0), scl=Pin(1)))
    oled.contrast(0)  # dim the display
    oled.fill(0)
    oled.text("All outs max", 5, 5)
    oled.show()

    ldac = Pin(13, mode=Pin.OUT, pull=Pin.PULL_DOWN, value=0)  # LDAC must be low to transfer the value immediately
    dac = MCP4728(I2C(1, sda=Pin(14), scl=Pin(15), freq=400000), DAC_ADDR)

    dac.a.vref = 0  # 0 (VDD) or 1 (Internal 2.048V)
    dac.a.gain = 1
    dac.b.vref = 0
    dac.b.gain = 1
    dac.c.vref = 0
    dac.c.gain = 1
    dac.d.vref = 0
    dac.d.gain = 1

    dac.a.value = 4095
    dac.b.value = 4095
    dac.c.value = 4095
    dac.d.value = 4095

    while True:
        sleep(0.5)
