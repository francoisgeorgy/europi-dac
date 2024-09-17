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

#### Power supply : 

This custom PCB swaps the 10-pin Eurorack power connector for a 16-pin one and removes the onboard power regulator, 
opting to use the 5V directly from the Eurorack power supply instead.


## Schematic

Here is the schematic of this PCB : [dac-board-v2.1.pdf](hardware%2Fdac-board-v2.1%2Fplot%2Fdac-board-v2.1.pdf)


## Why build this custom PCB?

This PCB project was mainly a fun excuse to experiment and learn:

- [KiCad](https://www.kicad.org/) practice: a good opportunity to get better at PCB design.
- SMD assembly with [JLCPCB](https://jlcpcb.com/): tried out having the board made and assembled by an external provider.
- Eurorack power filtering: played around with filtering power right on the PCB.
- DAC vs PWM outputs: wanted to see if DAC outputs really outperform PWM for basic CV voltages.
- Just for fun: because DIY projects are always more fun!


## License

This custom PCB is licensed under the same terms and conditions as the original EuroPi. 

This module, and any documentation included in this repository, is entirely "free" software and hardware, 
under different licenses depending on the software, hardware, and documentation itself.

* Software: [Apache 2.0](software/LICENSE)
* Hardware: [CERN OHL-S v2](hardware/LICENSE)
* Documentation: [CC0 1.0](LICENSE)

