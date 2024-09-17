
try:
    from lib.input_calibration_values import INPUT_CALIBRATION_VALUES
except ImportError:
    print("using default calibrations values from INPUT_CALIBRATION_VALUES")
    from default_calibration import INPUT_CALIBRATION_VALUES


def clamp(v, low, high):
    """Returns a value that is no lower than 'low' and no higher than 'high'."""
    return max(min(v, high), low)


MIN_INPUT_VOLTAGE = 0
MAX_INPUT_VOLTAGE = 12

MIN_VOLTAGE = MIN_INPUT_VOLTAGE
MAX_VOLTAGE = MAX_INPUT_VOLTAGE

#
# Compute correction gradients for the analog input:
#
_gradients = []
for index, value in enumerate(INPUT_CALIBRATION_VALUES[:-1]):
    try:
        _gradients.append(1 / (INPUT_CALIBRATION_VALUES[index + 1] - value))
    except ZeroDivisionError:
        raise Exception(
            "The input calibration process did not complete properly. Please complete again with rack power turned on"
        )
_gradients.append(_gradients[-1])

while True:
    raw_reading = int(input('? '))
    reading = raw_reading - INPUT_CALIBRATION_VALUES[0]
    max_value = max(
        reading,
        INPUT_CALIBRATION_VALUES[-1] - INPUT_CALIBRATION_VALUES[0],
    )
    percent = max(reading / max_value, 0.0)
    # low precision vs. high precision
    if len(_gradients) == 2:
        cv = 10 * max(
            reading / (INPUT_CALIBRATION_VALUES[-1] - INPUT_CALIBRATION_VALUES[0]),
            0.0,
        )
    else:
        index = int(percent * (len(INPUT_CALIBRATION_VALUES) - 1))
        cv = index + (_gradients[index] * (raw_reading - INPUT_CALIBRATION_VALUES[index]))
    print(f'{raw_reading:5} --> {clamp(cv, MIN_VOLTAGE, MAX_VOLTAGE)}V')
