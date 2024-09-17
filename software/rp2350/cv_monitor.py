"""
Voltage Monitor
author: François Georgy (https://github.com/francoisgeorgy)
date: 2023-01-25
labels: cv, tuner

Display the Analog In measured voltage, and the min and max values.

Button B1 resets the min and max values.
"""
from time import sleep

from europi import oled, ain, b1, cv1
from europi_script import EuroPiScript


class CvMonitor(EuroPiScript):

    @classmethod
    def display_name(cls):
        return "CV Monitor"

    def __init__(self):
        super().__init__()
        self.v_min = 100000
        self.v_max = -100
        b1.handler(self.reset_min_max)

    def reset_min_max(self):
        self.v_min = 100000
        self.v_max = -100

    def main(self):
        padding = 5
        while True:
            v = ain.read_voltage()
            if v < self.v_min:
                self.v_min = v
            if v > self.v_max:
                self.v_max = v
            oled.fill(0)
            oled.text(f"{v:2.2f}V   {ain.last_reading}", padding, 0)
            oled.text(f"{self.v_min:2.2f}  {self.v_max:2.2f}", padding, 20)
            oled.show()
            sleep(0.2)


if __name__ == "__main__":
    oled.contrast(0)  # dim the display
    CvMonitor().main()
