# Stirring subsystem: illustrative circuit design

The schematic adapts the course motor/Hall assembly to the current Arduino Nano ESP32. It is an example design, not a tested wiring prescription. Component values are illustrative; the actual assembly pinout, USB/VBUS current capacity, motor startup/stall current and measured performance must be checked before assembly.

## What changed from the proposal

- Use the current 5 V DC motor and Hall encoder rather than the older optical encoder.
- The course motor handout confirms **70 pulses per revolution of the geared-down output shaft**. Do not divide by the 10:1 gear ratio again.
- The motor and Hall sensor share the +5 V supply, but have separate motor-return and sensor-ground connections. Switch only the motor return; Hall ground must remain at common ground.
- The course requires supply from the Arduino 5 V rail, not an external motor supply. For a USB-powered Nano ESP32 this is **VBUS**. There is no VBUS 5 V output when powered solely from VIN. Do not substitute 6 V or 12 V, or inject an external supply into VBUS alongside USB.
- The older motor starter code uses Uno/Nano AVR registers (TCCR1A/TCCR1B), which must be replaced with Nano ESP32-compatible PWM configuration. Retain the measurement/control concept rather than copying those registers.
- Include a flyback diode across the motor and the handout's 470 uF supply decoupling capacitor.
- Add a 5 V-tolerant, 3.3 V-powered Hall signal buffer and a MOSFET gate driver to avoid applying 5 V to Nano GPIO or assuming the IRLB8748 has guaranteed low on-resistance at a 3.3 V gate voltage.

## Important conflict in the supplied specifications

The motor handout states that a 5 V supply gives approximately 10,000 motor RPM and 1,000 geared output RPM. It suggests control in the order of 300-1,000 RPM. The older general bioreactor specification calls for 500-1,500 RPM, within +/-20 RPM. These are not consistent. This design uses an **800 RPM example target**, within their overlapping range, and does not claim that the assembly can achieve 1,500 RPM. Confirm the intended assessed upper speed with a PGTA. Do not overvolt the motor to meet the older number.

## Components and values

| Reference | Example selection | Role |
|---|---|---|
| U1 | Existing Nano ESP32, USB powered | Local RPM feedback controller |
| M1 / H1 | Course 5 V motor and Hall assembly | Stirring and 70-pulse/output-revolution feedback |
| U2 | SN74LVC1G17, powered from 3.3 V | Non-inverting Schmitt buffer; input tolerates up to 5.5 V |
| R1 | 10 kohm, 0.25 W, optional | Hall pull-up to +5 V, only if required by actual output circuit |
| C4 | 100 nF ceramic | U2 local 3.3 V bypass |
| U3 | TC4420, PDIP-8, powered from VBUS +5 V | Non-inverting 3.3 V-to-5 V gate driver |
| C3 | 1 uF, >=10 V ceramic | U3 local VDD bypass; place close to pins |
| R2 | 100 kohm, 0.25 W | Driver input pull-down |
| R3 | 100 ohm, 0.25 W | MOSFET gate series resistor |
| R4 | 100 kohm, 0.25 W | Gate-to-source pull-down |
| Q1 | IRLB8748, TO-220 | Low-side motor switch |
| D1 | 1N5822 Schottky, 3 A / 40 V | Flyback diode; band/cathode to motor +5 V |
| C1 | 470 uF, >=10 V electrolytic | Local motor/Hall supply decoupling; positive terminal to +5 V |

U2, U3 and the 1N5822 are example additions, not confirmed kit contents. The SN74LVC1G17 is a surface-mount part and needs an appropriate adapter or board. An ordinary 74HC buffer is not a drop-in 5 V-tolerant substitute at a 3.3 V supply. The course's listed 1N4001 can be assessed for low-frequency use, but diode current, thermal performance and switching behaviour must match the chosen PWM and motor current. A small signal diode must not be assumed adequate simply because it appears in an old drawing.

## Exact wiring

All +5 V labels in this sheet mean the same Nano VBUS rail, and all grounds are connected. The Hall buffer uses the separate Nano 3V3 rail.

1. Nano VBUS -> assembly common +5 V supply. Hall GND -> common GND. Assembly motor return -> Q1 drain. Verify the assembly connector, rather than relying solely on wire colours.
2. Q1 source -> common GND. D1 anode -> drain/motor return; D1 cathode (band) -> +5 V. C1 connects across +5 V and common GND, near the assembly supply.
3. Hall output -> U2 input A. Fit R1 to +5 V only if the Hall output needs a pull-up. Determine whether the existing output is open collector/open drain or push-pull and whether it already includes a pull-up. The buffer accepts a valid 5 V Hall waveform and emits 3.3 V logic.
4. For SN74LVC1G17 **DBV/SOT-23-5**: pin 1 NC, pin 2 A input, pin 3 GND, pin 4 Y output, pin 5 VCC = 3.3 V. U2 Y -> Nano D2. Other packages can have different pin assignments; verify the exact purchased package. C4 connects VCC to GND at U2.
5. Nano D10 -> U3 input pin 2; R2 from pin 2 to GND. U3 pins 1 and 8 -> +5 V; pins 4 and 5 -> GND. Pin 3 NC. Tie output pins 6 and 7 together -> R3 -> Q1 gate. R4 connects gate to source. C3 bypasses U3 VDD to GND locally.
6. Route motor current directly back to the power-return point. Keep the Hall return and signal away from the switched-current path and use a short patch lead.

The course requires Arduino-supplied 5 V, but does not provide motor starting/stall current or a validated USB/VBUS current budget. For an illustrative load calculation only, 0.30 A running current at 5 V would be 1.5 W; this is **not a measured motor specification**. Verify motor, controller and other VBUS loads against the actual board, connector, cable and USB source limits. The 470 uF capacitor suppresses short transients; it cannot compensate for an undersized steady-state supply. If the available VBUS path is inadequate, resolve the supply arrangement with teaching staff.

## RPM calculation and feedback

With 70 rising edges per output revolution:

`RPM = 60 * frequency_Hz / 70`

`RPM = 60,000,000 / (70 * pulse_period_us)`

| Output RPM | Pulse frequency | Pulse period |
|---|---|---|
| 500 | 583.33 Hz | 1714.29 us |
| 800 | 933.33 Hz | 1071.43 us |
| 1000 | 1166.67 Hz | 857.14 us |
| 1500 | 1750 Hz | 571.43 us; mathematical conversion, not a claim of achievable speed |

Count only one edge per pulse, such as RISING. Counting both edges without changing the factor doubles the reported speed.

A simple pulse count over just 10 ms changes in increments of about 85.7 RPM, too coarse to directly demonstrate +/-20 RPM. The course uses pulse timing and a 10 ms control update. Use period measurement or a suitably designed longer-window estimator, reject implausible glitches, and stop treating an old period as a current speed once pulses cease. Keep the interrupt handler short; copy shared timing data consistently before processing it in the main loop.

Start at an 800 RPM target, ramp PWM gradually, and record measured speed versus duty. PWM duty changes the motor's switched supply, but speed is not a guaranteed linear function of duty under load. Establish achievable speed under the real stirring load before tuning a PI controller. Controller gains are intentionally not invented. Include duty saturation, integral anti-windup and missing-pulse/stall handling; on a stall, stop and investigate rather than repeatedly applying full power.

Verify RPM with the lab tachometer, record steady-state error and fluctuations, and test a setpoint step and a load change. Report the actual achieved range and tolerance if the target cannot be met.

## Shared controller pin plan

These are schematic board labels, not raw ESP32 GPIO numbers:

| Subsystem | Pins |
|---|---|
| Heating, existing drawing | A0 temperature; D5 heater command |
| Stirring | D2 Hall input; D10 motor command |
| pH | A1 pH input; D6 acid; D9 alkali |

The sheets show the same system controller, not three additional Nano boards. Check the pin-numbering mode and the team's UART/SPI/I2C allocation before implementation.

## Sources

- Current course kit: https://moodle.ucl.ac.uk/mod/page/view.php?id=9105524
- Motor handout and starter material: https://moodle.ucl.ac.uk/mod/folder/view.php?id=9105547
- Extracted current motor instructions: `material_review/MotorHallSensorInstructions.txt`
- Nano ESP32 VBUS and GPIO: https://docs.arduino.cc/tutorials/nano-esp32/cheat-sheet/
- Hall buffer: https://www.ti.com/lit/ds/symlink/sn74lvc1g17.pdf
- TC4420 driver: https://ww1.microchip.com/downloads/en/DeviceDoc/21419D.pdf
- MOSFET: https://www.infineon.com/assets/row/public/documents/24/49/infineon-irlb8748-datasheet-en.pdf
- Flyback diode: https://www.vishay.com/docs/88526/1n5820.pdf
