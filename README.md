# A 4 channels DAC for the EuroPi

This is a custom PCB that add a four channels DAC to the [EuroPi](https://allensynthesis.co.uk/modules/europi.html).

The DAC is a [MCP4728](https://www.microchip.com/en-us/product/mcp4728) : 

* 12-Bit Resolution
* 4 Buffered Voltage Outputs
* Single-Supply Operation: 2.7V to 5.5V
* On-Board Non-Volatile Memory (EEPROM)
* Normal or Power-Down Mode
* Internal or External Voltage Reference Selection
* Rail-to-Rail Output
* Low Power Consumption
* ±0.2 LSB DNL (typical)
* Address bits: User Programmable toEEPROM
* Standard (100 kbps), Fast (400 kbps) and High Speed (3.4 Mbps) Modes

The voltage reference is a [LM4040](https://www.analog.com/en/products/lm4040.html), 3.0V. 

The DAC outputs are connected to the EuroPi 3, 4, 5 and 6 outputs as follows : 

| EuroPi output | DAC channel |
|--------------:|------------:|
|             1 |             |
|             2 |             |
|             3 |           D |
|             4 |           B |
|             5 |           C |
|             6 |           A |

This specific order of the channels was chosen to facilitate the PCB routing. 

The EuroPi outputs 1 and 2 do not change and are still driven with a PWM output from the Pico.
