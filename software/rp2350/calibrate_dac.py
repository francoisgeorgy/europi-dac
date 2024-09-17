"""
Calibration of the DAC outputs
author: François Georgy (https://github.com/francoisgeorgy)
date: 2023-05-20
labels: calibration

The output calibration is fully automatic and no fine tuning can be done or is necessary.
"""
from time import sleep

from utils.calibrator import Calibrator
from europi import oled, k1, k2, dac, DAC_CHANNEL, EUROPI_OUTPUT_6, EUROPI_OUTPUT_5, EUROPI_OUTPUT_4, EUROPI_OUTPUT_3

try:
    from input_calibration_values import INPUT_CALIBRATION_VALUES
except ImportError:
    print("using default calibrations values from INPUT_CALIBRATION_VALUES")
    from default_calibration import INPUT_CALIBRATION_VALUES


class CalibrateDAC(Calibrator):

    @classmethod
    def display_name(cls):
        """Push this script to the end of the menu."""
        return "~Calibrate DAC"

    def __init__(self):
        super().__init__()

        self.file_created = False
        self.compute_ain_gradients(INPUT_CALIBRATION_VALUES)

        # fmt: off
        self.m.state("start") \
            .when("B1").do(self.display_power_reminder).goto("start") \
            .when("B2").do(self.do_connect_dac_output1_calibration)
        self.m.state("start_dac_output1").when("B2").do(self.do_calibrate_dac_output1).goto("dac_output1_done")
        self.m.state("dac_output1_done") .when("B2").do(self.do_connect_dac_output2_calibration)
        self.m.state("start_dac_output2").when("B2").do(self.do_calibrate_dac_output2).goto("dac_output2_done")
        self.m.state("dac_output2_done") .when("B2").do(self.do_connect_dac_output3_calibration)
        self.m.state("start_dac_output3").when("B2").do(self.do_calibrate_dac_output3).goto("dac_output3_done")
        self.m.state("dac_output3_done") .when("B2").do(self.do_connect_dac_output4_calibration)
        self.m.state("start_dac_output4").when("B2").do(self.do_calibrate_dac_output4).goto("all_done", self.display_done)
        self.m.state("all_done").when("B2").do(self.do_reset)
        self.m.state("error").when("B2").do(self.do_reset)
        # fmt: on

    def save_state(self):
        pass

    def reading_to_voltage(self, reading):
        try:
            index = next(index for index, v in enumerate(INPUT_CALIBRATION_VALUES) if v >= reading) - 1
        except StopIteration:
            index = len(INPUT_CALIBRATION_VALUES) - 1
        if index < 0:
            cv = 0
        else:
            cv = self.points[index] + self.ain_gradients[index] * (reading - INPUT_CALIBRATION_VALUES[index])
        return max(min(cv, 12), 0)

    def cv_to_reading(self, cv):
        try:
            index = next(index for index, v in enumerate(self.points) if v >= cv) - 1
        except StopIteration:
            index = len(self.points) - 1
        if index < 0:
            return INPUT_CALIBRATION_VALUES[0]
        else:
            return int(INPUT_CALIBRATION_VALUES[index] + (cv - self.points[index]) / self.ain_gradients[index])

    def calibrate_dac_output(self, channel):
        """
        :param channel: DAC channel [0..3]
        """
        if channel == 0:
            ch = dac.dac.a
        elif channel == 1:
            ch = dac.dac.b
        elif channel == 2:
            ch = dac.dac.c
        elif channel == 3:
            ch = dac.dac.d

        self.center_text(
            "Calibrating",
            f"0 V (DAC)",
            "please wait..."
        )
        dac_value = 0
        cal_values = [dac_value]
        # cv1.duty_u16(duty)

        ch.value = dac_value
        sleep(0.5)
        reading = self.sample_ain()
        self.center_text(
            f"Cal {0}V (DAC {channel})",
            f"adc: {reading}",
            f"ain: {self.reading_to_voltage(reading):0.3} V"
        )
        for v in range(1, 11):
            expected_reading = self.cv_to_reading(v)
            _v = round((4096 / (3.3*3.2)) * 0.9)      # 3.3 is the DAC Vcc, 3.2 is the output stage gain
            while abs(reading - expected_reading) > 0.002 and reading < expected_reading:
                # The closer we get to the expected voltage (reading), the finer
                # we adjust (increase) the CV1 duty cycle and we also give CV1
                # a little more time to stabilize.
                # wait = 0
                if reading / expected_reading < 0.5:
                    dac_value += 100
                elif reading / expected_reading < 0.8:
                    dac_value += 50
                elif reading / expected_reading < 0.95:
                    dac_value += 10
                # elif reading / expected_reading < 0.99:
                #     dac_value += 20
                #     wait = 0.1
                else:
                    dac_value += 1
                #     wait = 0.2
                # dac_value += 1
                wait = 0.1
                ch.value = dac_value
                if wait:
                    sleep(wait)  # wait for the output to stabilize
                reading = self.sample_ain()
                self.center_text(
                    f"Cal {v}V (DAC {channel})",
                    f"{dac_value} {(reading/expected_reading*100):0.1f}%",
                    f"ain: {self.reading_to_voltage(reading):0.2f} V",
                )
            cal_values.append(dac_value)
            # Display the result before continuing with the next calibration point :
            self.center_text(
                f"Cal {v}V (DAC {channel})",
                f"dac = {dac_value}",
                f"ain: {self.reading_to_voltage(reading):0.2f} V"
            )
            sleep(1)
        return cal_values

    def reset_dac_output(self, channel):
        """
        :param channel: DAC channel [0..3]
        """
        ch = None
        # select the channel :
        if channel == 0:
            ch = dac.dac.a
        elif channel == 1:
            ch = dac.dac.b
        elif channel == 2:
            ch = dac.dac.c
        elif channel == 3:
            ch = dac.dac.d
        # set it to zero :
        if ch is not None:
            ch.value = 0

    def execute_dac_outputs_calibration(self, channel):
        """
        :param channel: DAC channel [0..3]
        """
        cal_values = self.calibrate_dac_output(channel)
        self.center_text(
            f"DAC ch.{channel}",
            "saving values",
            "        B2:next"
        )
        with open(f"lib/dac_calibration_values.py", "a+") as file:
            if not self.file_created:
                # first channel, declare the output data structure:
                file.write(f"\nOUTPUT_DAC_CALIBRATION_VALUES = [None, None, None, None]\n")
                self.file_created = True
            values = ", ".join(map(str, cal_values))
            file.write(f"OUTPUT_DAC_CALIBRATION_VALUES[{channel}] = [{values}]\n")
        sleep(1)
        self.center_text(
            f"DAC ch.{channel} OK",
            "",
            "        B2:next"
        )
        self.reset_dac_output(channel)
        sleep(1)

    # --------------------------------------------------------------------------
    # STATES

    def display_start_menu(self, action=None):
        self.center_text(
            f"      DAC      ",
            "  calibration  ",
            "          B2:go"
        )

    # --------------------------------------------------------------------------
    # TRANSITIONS

    def do_retry(self, action):
        # TODO: discard last result
        # self.display_current_point()
        pass

    def do_connect_dac_output1_calibration(self, action):
        """
        Europi output 3 is connected to DAC output "D" (channel 3)
        """
        self.display_connect_output(EUROPI_OUTPUT_3)
        return "start_dac_output1"

    def do_connect_dac_output2_calibration(self, action):
        """
        Europi output 4 is connected to DAC output "B" (channel 1)
        """
        self.display_connect_output(EUROPI_OUTPUT_4)
        return "start_dac_output2"

    def do_connect_dac_output3_calibration(self, action):
        """
        Europi output 5 is connected to DAC output "C" (channel 2)
        """
        self.display_connect_output(EUROPI_OUTPUT_5)
        return "start_dac_output3"

    def do_connect_dac_output4_calibration(self, action):
        """
        Europi output 6 is connected to DAC output "A" (channel 0)
        """
        self.display_connect_output(EUROPI_OUTPUT_6)
        return "start_dac_output4"

    def do_calibrate_dac_output1(self, action):
        """
        Calibrate Europi output 3 that is connected to DAC output "D" (channel 3)
        """
        self.execute_dac_outputs_calibration(DAC_CHANNEL[EUROPI_OUTPUT_3])

    def do_calibrate_dac_output2(self, action):
        """
        Calibrate Europi output 4 that is connected to DAC output "B" (channel 1)
        """
        self.execute_dac_outputs_calibration(DAC_CHANNEL[EUROPI_OUTPUT_4])

    def do_calibrate_dac_output3(self, action):
        """
        Calibrate Europi output 5 that is connected to DAC output "C" (channel 2)
        """
        self.execute_dac_outputs_calibration(DAC_CHANNEL[EUROPI_OUTPUT_5])

    def do_calibrate_dac_output4(self, action):
        """
        Calibrate Europi output 6 that is connected to DAC output "A" (channel 0)
        """
        self.execute_dac_outputs_calibration(DAC_CHANNEL[EUROPI_OUTPUT_6])

    def main(self):
        k1prev = k1.read_position(10)
        k2prev = k2.read_position(10)

        self.display_start_menu()
        self.m.start("start")
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


if __name__ == "__main__":
    oled.contrast(0)  # dim the display
    CalibrateDAC().main()
