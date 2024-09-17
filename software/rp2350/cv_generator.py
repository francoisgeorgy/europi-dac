"""
DAC CV Generator
author: François Georgy (https://github.com/francoisgeorgy)
date: 2023-06-30
labels: dac, cv, tuner

Output to CV3..6 a voltage defined by Knob1 and Knob2.

Knob-1 sets the integer part from 0 to 9.
Knob-2 sets the fractional part from 0 to 99.

This allows to output a voltage in the range 0.00 to 9.99V.
"""
from time import sleep

from europi import cv1, cv2, cv3, cv4, cv5, cv6, k1, k2, oled, ain
from europi_script import EuroPiScript


class CvGenerator(EuroPiScript):
    @classmethod
    def display_name(cls):
        return "DAC CV Generator"

    def __init__(self):
        super().__init__()

    def main(self):
        padding = 5  # pixels left and right
        while True:
            v = k1.read_position(10) + k2.read_position(100) / 100.0
            v1 = cv1.voltage(v)
            v2 = cv2.voltage(v)
            v3 = cv3.voltage(v)
            v4 = cv4.voltage(v)
            v5 = cv5.voltage(v)
            v6 = cv6.voltage(v)
            vin = ain.read_voltage()
            oled.fill(0)
            oled.text(f"{v:2.2f}V v3={v3}", 5, 4)
            oled.text(f"Vin={vin}", 5, 15)
            oled.show()
            sleep(0.1)


if __name__ == "__main__":
    oled.contrast(0)  # dim the display
    CvGenerator().main()
