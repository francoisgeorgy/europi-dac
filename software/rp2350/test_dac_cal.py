
try:
    from lib.dac_calibration_values import OUTPUT_DAC_CALIBRATION_VALUES
except ImportError:
    print("using default calibrations values from OUTPUT_DAC_CALIBRATION_VALUES")
    from default_calibration import OUTPUT_DAC_CALIBRATION_VALUES


def clamp(v, low, high):
    """Returns a value that is no lower than 'low' and no higher than 'high'."""
    return max(min(v, high), low)


MIN_INPUT_VOLTAGE = 0
MAX_INPUT_VOLTAGE = 12

MIN_VOLTAGE = MIN_INPUT_VOLTAGE
MAX_VOLTAGE = MAX_INPUT_VOLTAGE

channel = 3

#
# Compute correction gradients for the DAC channel:
#
_gradients = []
for index, value in enumerate(OUTPUT_DAC_CALIBRATION_VALUES[channel][:-1]):
    _gradients.append(OUTPUT_DAC_CALIBRATION_VALUES[channel][index + 1] - value)
_gradients.append(_gradients[-1])

while True:
    voltage = float(input('? '))

    voltage = clamp(voltage, MIN_VOLTAGE, MAX_VOLTAGE)
    index = int(voltage // 1)
    v = round(OUTPUT_DAC_CALIBRATION_VALUES[channel][index] + (_gradients[index] * (voltage % 1)))
    if v > 4095:
        v = 4095

    print(f'{voltage:5} --> {v}')
