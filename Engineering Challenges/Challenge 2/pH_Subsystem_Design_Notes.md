# pH subsystem: illustrative circuit design

This design retains the course PH-100ATC probe, SEN0161 conditioner and two 6 V, 1 A peristaltic pumps. It develops the functional proposal into a circuit with separate sensing and pump-power paths. Values are examples; no physical circuit, pH calibration, flow calibration or dosing test has been performed.

`pH_Subsystem_Schematic.pdf` has two sheets: the main circuit and explicit driver/pump supply decoupling. The corresponding editable SVGs and PNGs are supplied separately.

## What changed from the proposal

- Use the current Nano ESP32 with 3.3 V analog inputs. The original SEN0161 operates from 5.00 V and has an analog output. Do not assume that an Uno wiring example can be used unchanged on the Nano ESP32.
- Preserve the supplied pH conditioner between the glass electrode and ADC. It provides the high input impedance and signal conditioning required by the electrode. The raw BNC electrode is not an ordinary ADC voltage source.
- Include a 10 kohm / 10 kohm divider to halve the conditioned output voltage. This example assumes the conditioned output remains between 0 and 5 V, mapping it to 0-2.5 V. Confirm the actual output bounds and board revision before connecting. The divider is not a universal clamp against arbitrary faults or negative voltages.
- Give each pump its own low-side MOSFET, flyback diode and driver channel. A single electronic switch cannot independently choose acid and alkali.
- Use IRLB8748 MOSFETs with approximately 6 V gate drive. Do not directly drive an IRF520 or IRLB8748 from 3.3 V while assuming a guaranteed low on-resistance.
- Separate the regulated 5 V analog supply from the 6 V pump supply, joining their negatives to common ground. Keep pump current out of the analog ground path and Nano board.

## Example components

| Reference | Selection | Function |
|---|---|---|
| U1 | Existing Arduino Nano ESP32, USB powered | pH conversion, dose sequencing, logging |
| Probe | PH-100ATC, course kit | Glass electrode in the vessel |
| U2 | Original SEN0161, course kit | Supplied high-impedance pH conditioner; 5.00 V supply |
| R1 / R2 | 10 kohm / 10 kohm, 1%, 0.25 W | Analog output attenuator, ratio 0.5 |
| C1 | 100 nF ceramic | ADC input filtering |
| C2 / C3 | 100 nF ceramic / 10 uF >=10 V | SEN0161 supply bypass |
| U3 / U4 | Two TC4420 non-inverting drivers, PDIP-8 | 3.3 V GPIO -> approximately 6 V MOSFET gate drive |
| R3 / R6 | 100 kohm each | Driver-input pull-downs |
| R4 / R7 | 100 ohm each | Gate series resistors |
| R5 / R8 | 100 kohm each | Gate-to-source pull-downs |
| Q1 / Q2 | Two IRLB8748 N-channel MOSFETs | Independent acid/alkali low-side switches |
| D1 / D2 | Two 1N5822 Schottky diodes, 3 A / 40 V | Pump flyback protection |
| Pumps | Two course 6 V, 1 A peristaltic pumps | Acid and alkali dosing |
| C4 / C5 | 100 nF / 1 uF >=16 V | Local U3 +6 V bypass |
| C6 / C7 | 100 nF / 1 uF >=16 V | Local U4 +6 V bypass |
| C8 / C9 | 470 uF >=16 V / 100 nF | Pump-rail bulk and high-frequency bypass |
| Analog supply | Regulated 5.00 V, example >=0.2 A capability | SEN0161 supply, isolated from pump switching noise by wiring/layout |
| Pump supply | Regulated 6 V, example >=3 A capability | Pumps and gate drivers; verify startup/stall current |

The drivers and Schottky diode types are additional example parts, not confirmed kit contents. Branch protection must be selected using the actual source fault current, wiring rating and measured pump startup/stall behaviour. The 1 A pump label is not a verified worst-case current. A 3 A supply is an illustrative capacity, not a proof that every startup is supported. If heater and pumps share a rail, include the heater demand as well; the drawn supply capacity excludes it.

## Exact connections

All GND symbols refer to the same electrical return. Named +6 V pump nodes are the same net. The regulated +5.00 V analog rail is a separate positive net from +6 V and Nano VBUS.

1. Probe BNC -> SEN0161 BNC input. SEN0161 + -> regulated +5.00 V; SEN0161 - -> common GND. Identify the connector labels from the actual board; do not assume cable colours or a V2 pinout.
2. SEN0161 A output -> R1 -> divider midpoint -> Nano A1. R2 and C1 connect midpoint to GND. Place the filter near A1. C2 and C3 connect across SEN0161 supply locally.
3. Nano D6 -> U3 input pin 2. R3 connects that input to GND. Nano D9 -> U4 input pin 2, with R6 to GND.
4. On **each TC4420 PDIP-8**, pins 1 and 8 -> +6 V; pins 4 and 5 -> GND; pin 3 NC; tie pins 6 and 7 together as that driver's output. U3 output -> R4 -> Q1 gate; U4 output -> R7 -> Q2 gate. R5 and R8 connect the respective gate to source.
5. Acid pump + -> +6 V; acid pump - -> Q1 drain; Q1 source -> pump-supply negative. Alkali pump + -> +6 V; alkali pump - -> Q2 drain; Q2 source -> pump-supply negative.
6. D1/D2 cathode (band) -> respective pump +6 V terminal; anode -> corresponding MOSFET drain/pump return. Place flyback paths close to the relevant pump/driver wiring.
7. Place C4/C5 across U3 supply, C6/C7 across U4 supply, and C8/C9 across the pump rail near the supply entry. Electrolytic positive terminal goes to the positive supply.
8. Connect Nano GND to the common return. Route each pump's switched-current return separately from the SEN0161 and ADC return. Do not connect the 6 V rail to Nano VBUS or GPIO. Do not backfeed USB by joining an external 5 V supply to VBUS.

The example pins A1, D6 and D9 do not duplicate the heating A0/D5 or stirring D2/D10 pins. They are board labels, not raw ESP32 GPIO numbers. All subsystem drawings represent the same Nano controller; check the team's other peripheral and communications assignments.

## Analog scaling and calibration

`Vadc = VA * R2 / (R1 + R2) = 0.5 * VA`

`VA = 2 * Vadc` for nominal equal resistors.

Thus a 5.00 V conditioner output would produce 2.50 V at A1. At nominal values the divider draws 0.25 mA at 5 V. The source resistance at A1 is about 5 kohm; with C1 = 100 nF the nominal time constant is 0.5 ms. Confirm that the actual module tolerates the divider loading, and calibrate with this divider connected. Configure suitable Nano ESP32 ADC attenuation and use calibrated voltage acquisition rather than an Uno's 5 V / 1024 equation. Check noise while pumps and stirring are active, not only with the rest of the rig off.

Use known pH buffers and the **actual divided ADC voltage** to calibrate the complete signal chain. For example, measure V4 in a pH 4.00 buffer and V7 in a pH 7.00 buffer:

`pH = 4 + (Vadc - V4) * (7 - 4) / (V7 - V4)`

This expression accommodates either calibration slope. It does not invent a universal pH-to-voltage relationship. Reject invalid calibration, such as equal/near-equal buffer voltages, rather than dividing by a near-zero number. For targets near pH 3, verify performance at an additional known point in that region. Respect buffer-temperature values and probe temperature response. The PH-100ATC name alone does not prove that the complete signal chain performs automatic temperature compensation.

The original SEN0161 and SEN0161-V2 are different products. V2 documentation describes a different supply/output arrangement and library; confirm the actual board before adopting it. The original SEN0161 manufacturer quotes a response time up to one minute, so do not expect the liquid/probe reading to react instantly after dosing.

## Dosing control

Illustrative target: **pH 5.0**. Illustrative decision band: **4.9-5.1**, not a course-required accuracy or measured performance.

| Measured condition | Next action |
|---|---|
| pH below 4.9 | Give one calibrated, limited alkali dose |
| pH above 5.1 | Give one calibrated, limited acid dose |
| Within 4.9-5.1 | Both pumps off |
| Mixing/settling after any dose | Both pumps off; wait and re-measure |
| Invalid/stale pH, no stirring, dose/time limit exceeded | Stop both pumps; report fault |

Implement a non-blocking state machine: IDLE -> RAMP/DOSE_ONE_PUMP -> MIX/SETTLE -> MEASURE -> DECIDE. Always switch both outputs off before changing dosing direction. Ramp startup as instructed by the course, and do not assume a very short drive pulse dispenses a repeatable volume. Prime and calibrate each pump under its real tubing, head and liquid conditions.

An illustrative measured flow of 30 mL/min would correspond to 0.5 mL/s during established flow. It is **not the kit pump's verified flow**, and 1 second of command time need not equal 0.5 mL because startup, ramp and tubing effects matter. Measure delivered volume for the actual pulse profile. Acid/base concentration, buffering and vessel volume determine how that dose changes pH; pH is logarithmic, so identical doses do not imply identical pH changes.

Start with a suitably small calibrated dose and allow mixing and probe settling before deciding to dose again. A trial wait in the order of 30-60 seconds may be a starting experiment, but determine the actual delay from recorded response and the lab's approved procedure. Enforce maximum single-dose time, cumulative dose limits and a timeout for failed response; numerical limits depend on the real chemistry and flow calibration.

The two channels are electrically independent: **if firmware drives both inputs high, both pumps run**. The drawing does not claim a hardware mutual-exclusion interlock. If independent prevention is required, add and validate a hardware interlock. Pull-downs reduce floating-input risk, but do not protect against every software fault or a shorted MOSFET.

## Evaluation

- Calibrate sensing against known buffers; record repeatability, settling and drift.
- Calibrate pump dose volume versus the actual command/ramp profile.
- Use approved solutions to test correction from above and below target, including overshoot and time to settle.
- Verify that invalid readings, stopping the stirrer and exceeding a dosing limit stop both pumps.
- Log measured pH, target, sensor validity, pump commands, dose totals and timestamps. Keep measured data outside the normal target range visible rather than clipping it to 3-7.

This circuit establishes the sensing and actuation path; it does not establish closed-loop accuracy without those measurements.

## Sources

- Course kit and pump ratings: https://moodle.ucl.ac.uk/mod/page/view.php?id=9105524
- Course motor/pump and probe-handling note: https://moodle.ucl.ac.uk/mod/page/view.php?id=9105565
- Original SEN0161 specifications: https://wiki.dfrobot.com/sen0161/
- Manufacturer calibration/sample guidance: https://wiki.dfrobot.com/sen0161/docs/19898
- Nano ESP32 GPIO/VBUS: https://docs.arduino.cc/tutorials/nano-esp32/cheat-sheet/
- TC4420 datasheet: https://ww1.microchip.com/downloads/en/DeviceDoc/21419D.pdf
- IRLB8748 datasheet: https://www.infineon.com/assets/row/public/documents/24/49/infineon-irlb8748-datasheet-en.pdf
- 1N5822 datasheet: https://www.vishay.com/docs/88526/1n5820.pdf
