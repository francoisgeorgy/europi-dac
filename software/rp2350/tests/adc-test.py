from machine import Pin, ADC, I2C
from ssd1306 import SSD1306_I2C
from time import sleep

knob1 = ADC(1)
# knob1 = ADC(Pin(27, Pin.IN, Pin.PULL_DOWN))
knob2 = ADC(2)
# knob2 = ADC(Pin(28, Pin.IN, Pin.PULL_DOWN))
oled = SSD1306_I2C(128, 32, I2C(0, sda=Pin(0), scl=Pin(1)))
smps = Pin(23, mode=Pin.OUT, value=1)


def read_adc(mask=0xff80):
    samples = 16
    s10 = []
    s11 = []
    s20 = []
    s21 = []
    for i in range(samples):
        sample1 = knob1.read_u16()
        sample2 = knob2.read_u16()
        s10.append(sample1)
        s11.append(sample1 & mask)
        s20.append(sample2)
        s21.append(sample2 & mask)
    return round(sum(s10) / samples), round(sum(s11) / samples), \
        round(sum(s20) / samples), round(sum(s21) / samples)


# def raw(iterations=10, delay=0.1):
#     for i in range(iterations):
#         raw, masked = read_adc()
#         print(raw)
#         sleep(delay)
#
#
# def main(iterations=10, delay=0.1):
#     for i in range(iterations):
#         raw, masked = read_adc()
#         print(f"{raw:5} {masked:5}  {raw:04x}  {masked:04x}  {raw:016b}  {masked:016b}")
#         sleep(delay)


if __name__ == "__main__":

    oled.contrast(0)  # dim the display

    while True:
        raw1, masked1, raw2, masked2 = read_adc()
        oled.fill(0)
        oled.text(f"{raw1:5}", 5, 4)
        oled.text(f"{masked1:5}", 5, 20)
        oled.text(f"{raw2:5}", 65, 4)
        oled.text(f"{masked2:5}", 65, 20)
        oled.show()
        sleep(0.1)
