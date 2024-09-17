"""
Calibratrion base class
author: François Georgy (https://github.com/francoisgeorgy)
date: 2024-09-15
labels: calibration

"""
from machine import Pin, ADC, PWM, I2C, reset

from utils.simple_state_machine import SimpleStateMachine
from europi import oled, b1, b2, k1, k2, dac, DEFAULT_SAMPLES, ain
from europi_script import EuroPiScript

try:
    from input_calibration_values import INPUT_CALIBRATION_VALUES
except ImportError:
    # print("using default calibrations values from INPUT_CALIBRATION_VALUES")
    from default_calibration import INPUT_CALIBRATION_VALUES


class Calibrator(EuroPiScript):

    @classmethod
    def display_name(cls):
        """Push this script to the end of the menu."""
        return "~Calibrator"

    def __init__(self):
        super().__init__()
        self.ain = ADC(0)
        self.usb = Pin(24, Pin.IN)
        self.points = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        self.in_values = INPUT_CALIBRATION_VALUES
        self.ain_gradients = []
        # self._gradients = []
        self.m = SimpleStateMachine()
        b1.handler(self.button1)
        b2.handler(self.button2)

    def set_in_values(self, values):
        self.in_values = values

    def change_decimal(self, n, position, digit):
        s = list(f"{(n * 10 ** position):0.4f}")
        s[-6] = str(digit)  # -6 is the digit at the left of the dot (xxx.xxxx)
        return float("".join(s)) / (10 ** position)

    def change_10th_bipolar(self, n, delta):
        return n + (delta - 5) / 10

    def center_text(self, line1, line2="", line3=""):
        oled.centre_text("\n".join([line1, line2, line3]))

    def sample_ain(self, samples=DEFAULT_SAMPLES):
        """Over-samples the ADC and returns the average.
        """
        value = 0
        for _ in range(samples):
            value += self.ain.read_u16()
        return round(value / samples)

    def compute_ain_gradients(self, input_calibration_values):
        """
        Compute correction gradients for the analog input:
        :param input_calibration_values:
        :return:
        """
        for index, value in enumerate(input_calibration_values[:-1]):
            try:
                self.ain_gradients.append(1 / (input_calibration_values[index + 1] - value))
            except ZeroDivisionError:
                raise Exception(
                    "The input calibration process did not complete properly. Please complete again with rack power turned on"
                )
        self.ain_gradients.append(self.ain_gradients[-1])

    def button1(self):
        self.m.do_action("B1")

    def button2(self):
        self.m.do_action("B2")

    def knob1(self):
        self.m.do_action("K1")

    def knob2(self):
        self.m.do_action("K2")

    def reading_to_voltage(self, reading):
        try:
            index = next(index for index, v in enumerate(self.in_values) if v >= reading) - 1
        except StopIteration:
            index = len(self.in_values) - 1
        if index < 0:
            cv = 0
        else:
            cv = self.points[index] + self.ain_gradients[index] * (reading - self.in_values[index])
        return max(min(cv, 12), 0)

    def cv_to_reading(self, cv):
        try:
            index = next(index for index, v in enumerate(self.points) if v >= cv) - 1
        except StopIteration:
            index = len(self.points) - 1
        if index < 0:
            return self.readings[0]
        else:
            return int(self.readings[index] + (cv - self.points[index]) / self.ain_gradients[index])

    # --------------------------------------------------------------------------
    # STATES

    def display_power_reminder(self, action=None):
        if self.usb.value() == 1:
            self.center_text(
                "Confirm rack",
                "power is ON",
                "Back    Confirm")
        else:
            self.center_text(
                "Rack power",
                "is ON.",
                "       Continue")

    def display_output_calibration(self, action=None):
        self.center_text(
            "Values saved",
            "Press B2 to",
            "calib. outputs"
        )

    def display_connect_output(self, output, action=None):
        self.center_text(
            f"Plug out {output} into",
            "analogue in.",
            "             OK"
        )

    def display_done(self, action=None):
        self.center_text(
            "All done!",
            " ",
            "B2 to restart"
        )

    def display_error(self, action=None):
        self.center_text(
            "ERROR",
            "Invalid data",
            "B2 to restart"
        )

    # --------------------------------------------------------------------------
    # TRANSITIONS

    def do_reset(self, action):
        oled.fill(0)
        oled.show()
        reset()
