"""See menu.md for details."""
# from bootloader import BootloaderMenu
from calibrate_input import CalibrateInput
from europi import bootsplash, usb_connected, oled
# from calibrate import Calibrate

# This is a fix for a USB connection issue documented in GitHub issue #179, and its removal condition is set out in
# GitHub issue #184
if usb_connected.value() == 0:
    from time import sleep
    sleep(0.5)

# Reset the module state and display bootsplash screen.
bootsplash()

EUROPI_SCRIPT_CLASSES = [
    CalibrateInput
]


if __name__ == "__main__":
    oled.contrast(0)  # dim the display
    # BootloaderMenu(EUROPI_SCRIPT_CLASSES).main()
    CalibrateInput().main()
