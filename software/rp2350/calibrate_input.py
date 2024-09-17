"""
Custom calibration
author: François Georgy (https://github.com/francoisgeorgy)
date: 2023-01-20
labels: calibration

The user can fine-tune each calibration point during the procedure. For example, if the user does not has a precise
voltage source but has a precise voltage meter. In that case, it can measure the real voltage applied to analog-in
and fine-tune the value used by the calibration procedure.
To do that, use the knobs as is :
- Knob-1 : adjust the first decimal digit
- Knob-2 : adjust the second decimal digit
This results in a fine-tuning range of -0.50V to +0.49V

A detailed documentation about the calibration process
is available at https://francoisgeorgy.ch/modular/europi/custom-calibration-details/
"""
from time import sleep

import time

from utils.calibrator import Calibrator
from europi import oled, k1, k2
from utils.simple_state_machine import STATE_END


class CalibrateInput(Calibrator):

    @classmethod
    def display_name(cls):
        """Push this script to the end of the menu."""
        return "~Calibrate In"

    def __init__(self):
        super().__init__()

        self.points = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        self.readings = []
        self.current_point = 0
        self.current_reading = 0

        # fmt: off
        self.m.state("start") \
            .when("B2").do(self.do_init_input_calibration).goto("power_reminder", self.display_power_reminder)

        self.m.state("power_reminder") \
            .when("B1").goto("start") \
            .when("B2").goto("current_point", self.display_current_point)

        # .when("B1").do(self.display_start_menu).goto("start") \
        self.m.state("current_point") \
            .when("B1").goto(STATE_END) \
            .when("B2").do(self.do_calibrate_point).goto("result", self.display_result) \
            .when("K1").do(self.do_adjust10th).do(self.display_current_point) \
            .when("K2").do(self.do_adjust100th).do(self.display_current_point) \
            .when("refresh_display").do(self.display_current_point)

        self.m.state("result") \
            .when("B1").do(self.do_retry).goto("current_point", self.display_current_point) \
            .when("B2").do(self.do_select_next_point_or_save)

        self.m.state("all_done") \
            .when("B2").do(self.do_reset)

        self.m.state("error") \
            .when("B2").do(self.do_reset)

        self.m.state("abort") \
            .when("B2").do(self.do_reset)
        # fmt: on

    def reading_to_voltage(self, reading):
        try:
            index = next(index for index, v in enumerate(self.readings) if v >= reading) - 1
        except StopIteration:
            index = len(self.readings) - 1
        if index < 0:
            cv = 0
        else:
            cv = self.points[index] + self.ain_gradients[index] * (reading - self.readings[index])
        return max(min(cv, 12), 0)

    def save_on_disk(self):
        oled.centre_text("Saving values...")
        with open(f"lib/input_calibration_values.py", "w") as file:
            file.write(f"INPUT_CALIBRATION_POINTS = {self.points}\n")
            file.write(f"INPUT_CALIBRATION_VALUES = {self.readings}\n")
        self.center_text(
            "Saving done."
        )

    # --------------------------------------------------------------------------
    # STATES

    def display_current_point(self, action=None):
        v = self.sample_ain()
        self.center_text(
            f"Apply {self.points[self.current_point]:0.2f} V",
            f"adc: {v}",
            "Abort        OK"
        )

    def display_result(self, action=None):
        self.center_text(
            f"{self.points[self.current_point]}V = {self.current_reading}",
            " ",
            "Retry   Confirm"
        )

    # --------------------------------------------------------------------------
    # TRANSITIONS

    def do_init_input_calibration(self, action):
        self.current_point = 0
        self.current_reading = 0

    def do_adjust10th(self, action=None):
        self.points[self.current_point] = self.change_10th_bipolar(
            self.points[self.current_point], k1.read_position(10)
        )

    def do_adjust100th(self, action=None):
        self.points[self.current_point] = self.change_decimal(
            self.points[self.current_point], 2, int(k2.read_position(10))
        )

    def do_calibrate_point(self, action):
        self.current_reading = self.sample_ain()

    def do_select_next_point_or_save(self, action=None):
        # save current reading :
        self.readings.append(self.current_reading)
        # select next calibration point :
        self.current_point += 1
        if self.current_point == len(self.points):
            self.save_on_disk()  # FIXME: should be in do_save_result()
            time.sleep(1)
            self.display_done()
            return "all_done"
        else:
            self.display_current_point()
            return "current_point"

    def do_retry(self, action):
        # TODO: discard last result
        self.display_current_point()
        pass

    def main(self):

        k1prev = k1.read_position(10)
        k2prev = k2.read_position(10)

        self.display_power_reminder()
        self.m.start("power_reminder")
        while True:
            self.m.execute()
            # The simple state machine is only able to handle one action at a time.
            # This is why we use if..elif below.
            if k1.read_position(10) != k1prev:
                k1prev = k1.read_position(10)
                self.knob1()
            elif k2.read_position(10) != k2prev:
                k2prev = k2.read_position(10)
                self.knob2()
            elif self.m.in_state("current_point"):
                self.m.do_action("refresh_display")
                sleep(0.2)


if __name__ == "__main__":
    oled.contrast(0)  # dim the display
    CalibrateInput().main()
