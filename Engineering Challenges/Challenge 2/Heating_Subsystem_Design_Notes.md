# Heating subsystem: illustrative circuit design

This design develops page 5 of `Engineering Challenges Presentation.pdf` into an electrical schematic. The original page is a functional block diagram; its overall feedback concept is sensible, but it is insufficient as a wiring diagram. Example values below are internally consistent starting points, not measured results or proof of the required +/-0.5 C performance.

## Changes to the original slide

- Use the current kit's Arduino Nano ESP32 rather than an Arduino Uno. The Nano ESP32 uses 3.3 V I/O.
- Draw the 10 kohm fixed resistor and 10 kohm NTC as a real divider with the midpoint connected to A0. The sensor is supplied from the Nano's 3V3 rail, not the heater rail.
- Use the IRLB8748 as a low-side switch: heater to drain, source to supply return. Gate control is relative to the source.
- Add a non-inverting TC4420 gate driver, powered from 6 V. Its TTL-compatible input accepts the 3.3 V controller output; it drives the MOSFET gate at approximately 6 V. The IRLB8748 has guaranteed on-resistance at 4.5 V and 10 V gate drive, but not at 3.3 V. Threshold voltage is not a full-conduction specification.
- State the heater supply. A 3 ohm, 30 W-rated heater does not always dissipate 30 W. This example uses regulated 6 V for approximately 2 A and 12 W when on. Do not substitute a raw battery whose maximum voltage has not been checked.
- Show a common electrical return, while keeping the high-current heater return separate from sensitive sensor wiring until the common return point.

## Component values

| Reference | Example selection | Function |
|---|---|---|
| U1 | Arduino Nano ESP32, USB powered | Sensor acquisition and local feedback control |
| TH1 | Kit 10 kohm NTC at 25 C; actual curve to be calibrated | Liquid temperature sensor |
| R1 | 10 kohm, 1%, 0.25 W | Fixed upper divider resistor |
| R2 | 1 kohm, 0.25 W | ADC input series resistor |
| C1 | 100 nF ceramic | ADC noise filtering |
| U2 | TC4420, non-inverting, PDIP-8 | 3.3 V logic input to approximately 6 V MOSFET gate drive |
| R3 | 100 kohm, 0.25 W | Driver-input pull-down while GPIO is floating |
| R4 | 100 ohm, 0.25 W | Gate series resistor |
| R5 | 100 kohm, 0.25 W | Gate-to-source pull-down |
| C2 | 100 nF, >=16 V ceramic | Driver bypass capacitor |
| C3 | 1 uF, >=16 V ceramic | Driver local decoupling |
| Q1 | Kit IRLB8748 N-channel MOSFET | Low-side heater switching |
| H1 | Kit 3 ohm, 30 W-rated immersed heater | Operated at approximately 12 W in this example |
| F1 | 3 A DC fuse, example only | Heater wiring fault protection; coordinate with wiring and supply |
| SW1 | SPST switch, rated >=5 A at 12 V DC | Manual heater enable/disconnect |
| Supply | Regulated 6 V DC, >=3 A capability | Heater and driver; Nano powered separately over USB |

The TC4420 is an additional component; availability in the kit has not been established. A MOSFET with on-resistance explicitly specified at 2.5/3.3 V could permit a simpler direct-GPIO design, but that substitution needs a suitable part and thermal assessment. Do not simply omit U2 while assuming the IRLB8748 has a guaranteed 3.3 V on-resistance.

## Exact connections

Named nets in the schematic represent electrically connected nodes even where no continuous wire is drawn. All GND symbols belong to one return net; both +6 V labels belong to the regulated 6 V supply.

1. Nano 3V3 -> R1 -> divider midpoint -> TH1 -> GND.
2. Divider midpoint -> R2 -> Nano A0. C1 connects A0 to GND.
3. Nano D5 -> TC4420 pin 2. R3 connects pin 2 to GND. D5 is an example board pin label, not a raw ESP32 GPIO number.
4. TC4420 PDIP-8 pins 1 and 8 -> +6 V; pins 4 and 5 -> GND. Tie duplicate output pins 6 and 7 together -> R4 -> Q1 gate. Pin 3 is not connected. Place C2/C3 directly across U2 supply and ground with short connections.
5. R5 connects Q1 gate to Q1 source.
6. +6 V -> F1 -> SW1 -> H1 -> Q1 drain. Q1 source -> supply negative.
7. Nano GND, thermistor return, driver ground and supply negative share the common return. Use separate heater-current wiring to that point; do not pass the heater current through the Nano, USB ground path, or a solderless breadboard power rail.
8. For the actual IRLB8748 TO-220 part, verify its datasheet orientation: gate, drain, source; metal tab is drain. Check the package before connecting.

## Sensing calculations

For the divider orientation shown:

`Vadc = V3V3 * Rntc / (R1 + Rntc)`

`Rntc = R1 * Vadc / (V3V3 - Vadc)`

At 25 C, Rntc = R1 = 10 kohm, giving Vadc = 1.65 V for an actual 3.30 V rail. Increasing temperature lowers NTC resistance and lowers Vadc. Swapping the fixed resistor and NTC is also valid, but reverses the voltage-temperature relationship and changes the conversion equation.

An illustrative beta-model conversion is:

`T_kelvin = 1 / (1/298.15 + ln(Rntc/10000)/B)`

`T_celsius = T_kelvin - 273.15`

For B = 3950 K **as an arbitrary example**, approximately:

| Temperature | NTC resistance | Divider voltage |
|---|---|---|
| 25 C | 10.00 kohm | 1.650 V |
| 30 C | 8.04 kohm | 1.470 V |
| 35 C | 6.51 kohm | 1.301 V |

The kit's actual ND06P00103K beta/curve must come from its datasheet or calibration. Do not treat 3950 K as its verified coefficient. Obtain ADC voltage with suitable board configuration and calibration; do not copy an Uno's 5 V / 1023 conversion into ESP32 code. Rail faults and disconnected sensors must be detected before applying the resistance conversion.

The divider draws approximately 0.165 mA at 25 C and dissipates approximately 0.27 mW in the NTC. Sensor self-heating and probe placement still need checking. The filter time constant is approximately (R2 + R1 parallel TH1) * C1 = 0.6 ms at 25 C.

## Heating and feedback

`I_on = Vsupply / Rheater`

`P_on = Vsupply^2 / Rheater`

`P_average approximately duty_fraction * P_on`

For a nominal 3 ohm heater:

| Supply | On-state current | On-state power |
|---|---|---|
| 6 V | 2 A | 12 W |
| 9 V | 3 A | 27 W |
| 12 V | 4 A | 48 W |

The drawn circuit uses only the 6 V case. A 9 V version would require a suitable regulated supply, revised current/wiring/fuse assessment, and thermal testing. A 12 V version with a 3 ohm heater would exceed its stated 30 W rating at full duty. Limiting average PWM power alone does not establish that such over-rated instantaneous operation is permitted by the heater manufacturer.

Twelve watts is an initial, kit-aligned example, not proof that the vessel can reach/hold 35 C against its heat losses. For 250 mL of water, neglecting the vessel and losses, raising 20 C to 30 C requires about 10450 J, or 14.5 minutes at 12 W. Real heating takes longer and may fail to reach a target if heat loss equals available power.

Start with a 30 C target and simple hysteresis (for example on below 29.8 C, off above 30.2 C) or slow time-proportioned control with a trial 1-second window. These are starting choices, not validated settings. Record the response and tune based on the measured lag and overshoot. A narrow switching band does not prove +/-0.5 C actual liquid accuracy. PI/PID gains must be determined from the real thermal response rather than invented.

The local controller should start with the heater off, turn it off on invalid/stale sensor data, and enforce a separate over-temperature limit (for example 40 C, subject to the rig's approved limits). A power MOSFET can fail short; software shutdown is not an independent thermal cutoff. Assess an independent cutoff if required by the lab. Test immersed according to the lab instructions.

An ordinary resistive heater does not require the motor's flyback diode. The actual harness may still require transient suppression after checking cable inductance and the drain waveform.

## References

- Current kit: https://moodle.ucl.ac.uk/mod/page/view.php?id=9105524
- Nano ESP32 official specifications: https://store.arduino.cc/products/nano-esp32
- IRLB8748 datasheet: https://www.infineon.com/assets/row/public/documents/24/49/infineon-irlb8748-datasheet-en.pdf
- TC4420 datasheet (PDIP-8 pin mapping and TTL input thresholds): https://ww1.microchip.com/downloads/en/DeviceDoc/21419D.pdf
- Course calibration/testing: https://moodle.ucl.ac.uk/mod/resource/view.php?id=9105564
