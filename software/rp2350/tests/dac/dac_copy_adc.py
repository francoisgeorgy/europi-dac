from machine import Pin, ADC, I2C
from mcp4728 import MCP4728
from ssd1306 import SSD1306_I2C
from time import sleep

if __name__ == "__main__":

    DAC_ADDR = 0x60

    # smps = Pin(23, mode=Pin.OUT, value=1)

    oled = SSD1306_I2C(128, 32, I2C(0, sda=Pin(0), scl=Pin(1)))
    oled.contrast(0)  # dim the display
    oled.fill(0)
    oled.text("DAC copy ADC", 5, 4)
    oled.show()
    sleep(0.5)

    adc = ADC(Pin(27, Pin.IN, Pin.PULL_DOWN))

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

    v = round(4096 / 3.3)

    dac.a.value = v
    dac.b.value = v
    dac.c.value = v
    dac.d.value = v

    SAMPLES = 16
    while True:
        value = 0
        for _ in range(SAMPLES):
            value += adc.read_u16()
            # value += adc.read_u16() & 0xFFC0
        value = value - 150
        if value < 0:
            value = 0
        value = int(value / SAMPLES)
        value12 = value >> 4
        v = value / 65535 * 3
        o = int(value / 65536 * 4095)
        dac.a.value = o
        dac.b.value = o
        dac.c.value = o
        dac.d.value = o
        oled.fill(0)
        oled.text(f"{value:5}  {value12:3}", 0, 0)
        oled.text(f"{v:0.3f}", 0, 12)
        oled.text(f"{o:4}", 0, 24)
        oled.show()
        sleep(0.1)

