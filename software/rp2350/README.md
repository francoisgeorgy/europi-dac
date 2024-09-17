How to use the new Pi Pico 2 with EuroPi 
========================================

Pimoroni offers a Pico 2 board that is a drop-in replacement for the Pico :

[Pimoroni Pico Plus 2](https://shop.pimoroni.com/products/pimoroni-pico-plus-2?variant=42092668289107)

### To use this board : 

1. Download and install the Pimoroni firmware from https://github.com/pimoroni/pimoroni-pico-rp2350

Select the **pico_plus2_rp2350** MicroPython Flavour. 
The current release (september 16th) is [pico_plus2_rp2350-v0.0.7-pimoroni-micropython.uf2](https://github.com/pimoroni/pimoroni-pico-rp2350/releases/download/v0.0.7/pico_plus2_rp2350-v0.0.7-pimoroni-micropython.uf2). 

2. Install the ssd1306 package.
3. Install the EuroPi software from the source files. 
You must not install the `micropython-europi` package nor use a `europi-vX.Y.Z.uf2` file.
4. Adapt the EuroPi scripts to work with the Pico 2.



### Software changes for the Pico 2 : 

The only change that really needs to be made is related to the ADC. We need to use the ADC channel number instead
of the Pin number.

In `europi.py`, replace :  

    ain = AnalogueInput(PIN_AIN)
    k1 = Knob(PIN_K1)
    k2 = Knob(PIN_K2)

with : 
    
    ain = AnalogueInput(0)
    k1 = Knob(1)          
    k2 = Knob(2)          

