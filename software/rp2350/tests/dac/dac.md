Custom board with MCP4728 DAC
=============================

| Front-board jack | Pico PWM / DAC output |
|------------------|-----------------------|
| Output 1         | PWM1                  |
| Output 2         | PWM2                  |
| Output 3         | DAC D ch 3            |
| Output 4         | DAC B ch 1            |
| Output 5         | DAC C ch 2            |
| Output 6         | DAC A ch 0            |

Firmware 
--------

New classes : 

    OutputPWM
    OutputDAC

Changed class : 

    Output is parent of OutputPWM and OutputDAC
