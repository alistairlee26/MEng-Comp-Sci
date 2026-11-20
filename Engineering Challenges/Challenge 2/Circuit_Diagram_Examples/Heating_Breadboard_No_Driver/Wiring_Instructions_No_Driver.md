# Heating breadboard without a driver IC

This replaces the earlier TC4420 version for your available IRLB8748. Use the two-page **Heating_No_Driver_Guide.pdf** and this connection list together.

## What the TC4420 was doing

It is a gate driver: it takes the Nano's 3.3 V PWM signal and drives the MOSFET gate at a higher voltage. It does not measure temperature or supply the heater current. It was an added design precaution, not a part shown on the lecturer's whiteboard.

The IRLB8748 data sheet gives guaranteed on-resistance at gate voltages of 4.5 V and 10 V. Its typical curves show operation at lower gate voltages, but typical curves do not guarantee every individual part. Direct 3.3 V drive is therefore a **bench-verified option for this 6 V, approximately 2 A load**, not a guaranteed replacement for the driver across arbitrary loads, devices or temperatures.

## Parts and operating conditions

- Nano ESP32, USB powered; confirmed IRLB8748 TO-220.
- R1: 10 kΩ, 1%, ≥0.25 W (selected for this design because the whiteboard value was unclear).
- R2: 1 kΩ, ≥0.25 W, in series between D5 and the gate. This limits the initial GPIO charging current to about 3.3 mA. Slow thermal switching avoids a need for fast gate edges.
- R3: 100 kΩ, ≥0.25 W, gate-to-source pull-down **at the MOSFET connector**. This holds the device off if the controller or gate lead is disconnected.
- Kit 10 kΩ NTC and 3 Ω, 30 W-rated heater.
- Regulated **6 V**, ≥3 A continuous supply capability. The heater operates at approximately 2 A and 12 W when fully on. Do not select 12 V for this layout.
- Manual heater enable switch rated ≥5 A DC, 3 A DC fuse/holder near supply positive, and insulated heater wiring/terminals rated ≥5 A. Check the actual fuse characteristics and supply fault behaviour when assembling.
- Standard 400-point breadboard, or numbered strips 1–30 of an 830-point board. Rails unused. All +6 V heater-power wiring remains off the breadboard.

## Exact connections

On the board, holes A–E of one number connect together, and F–J of that number connect together separately. The two groups do not join across the centre gap. Wire crossings in the picture do not connect.

| Connection / part | From | To |
|---|---|---|
| Nano 3V3 | Nano 3V3 | B3 |
| R1, 10 kΩ | E3 | E9 |
| NTC probe | D9 | D6 (either probe lead orientation) |
| Nano analogue input | Nano A0 | B9 |
| Nano ground | Nano GND | A6 |
| Ground jumper | B6 | G26 |
| PWM control | Nano D5 | B16 |
| R2, 1 kΩ | C16 | C22 |
| Gate lead | B22 | MOSFET G, left leg 1 |
| Common reference | H26 | Supply-negative star terminal |
| R3, 100 kΩ | MOSFET G | MOSFET S, physically at Q1 connector |

The Nano is placed beside the breadboard and connected by female-to-male jumpers; the drawing's board labels refer specifically to the Nano ESP32. Use `D5` and `A0` constants in code. D5 replaces the whiteboard's D1 so TX remains available for UART. Do not map these names directly to numeric ESP32 GPIO numbers.

## Heater power wiring — outside the breadboard

Printed MOSFET face towards you, metal tab behind, legs down: **left gate (1), middle drain (2), right source (3)**. The metal tab is drain. Use secured, insulated terminals or a soldered adapter; do not simply twist bare leads together.

1. Regulated +6 V → 3 A fuse → manual enable switch → heater positive.
2. Heater negative → MOSFET drain, middle leg 2.
3. MOSFET source, right leg 3 → supply negative with a separate power lead. This wire carries heater current; it does not go through the Nano, USB or breadboard.
4. H26 → that same supply-negative terminal via a separate low-current ground lead.
5. B22 → gate, left leg 1. R3 bridges G to S at the MOSFET connector. Keep the gate/control-return wiring short, preferably about 10 cm or less, and away from heater-current wiring.

## Checks before sustained heating

1. Disconnect all power while wiring. Keep the heater-enable switch open. Check that the 3.3 V sensor circuit has no connection to heater positive.
2. Load code that sets D5 LOW immediately at startup. Leave the switch open; power the Nano over USB and verify the sensor. At 25°C with a 10 kΩ thermistor, A0 should be approximately 1.65 V. Warming an NTC should lower that voltage.
3. Set the regulated supply to 6.0 V and verify it with a meter. With the heater isolated, verify gate-to-source voltage is near zero when D5 is LOW and approximately 3.3 V when D5 is HIGH (slightly lower due to R2/R3). Return LOW. **Never connect the gate directly to 6 V while it is also connected to the Nano.**
4. Switch off before connecting the heater. Immerse it correctly, secure the connections and attach voltmeter probes across MOSFET drain and source (red to leg 2, black to leg 3) while power is off. Do not allow a probe to bridge adjacent legs. Use the meter's DC-voltage mode, not its current mode across these pins.
5. With the element immersed, perform a brief supervised full-on test at 6 V. The circuit should draw close to 2 A. **Use less than 0.1 V D–S drop at approximately 2 A as an initial design criterion**, giving less than about 0.2 W MOSFET conduction loss. This is a practical screening target, not a manufacturer specification or a complete thermal certification. Measure real current using the supply display or a properly connected current measurement.
6. If the drop is high, or increases as the device warms, switch off rather than continuing. Recheck pinout and gate voltage. If direct 3.3 V drive is inadequate, use a MOSFET with on-resistance specified at 2.5/3.3 V or add a suitable driver. Do not solve it by connecting Nano GPIO to a higher supply.
7. After the initial check passes, extend the test gradually under supervision and monitor MOSFET temperature using an appropriate instrument and D–S drop, including at the warmest intended operating conditions. Do not rely on touching the MOSFET to judge temperature. Keep a manual heater disconnect available.

Use slow thermal control, for example a one-second on/off control period (time proportioning), rather than an unexamined high-frequency PWM setting. This is a circuit/drive check, not a complete feedback controller: sensor-fault detection and overtemperature handling remain required in the control code. No physical build or temperature-control performance test has been carried out here.

## References

- [Infineon IRLB8748 data sheet](https://www.infineon.com/assets/row/public/documents/24/49/infineon-irlb8748-datasheet-en.pdf): pinout and specified/typical gate-drive behaviour.
- [Arduino Nano ESP32 pinout](https://docs.arduino.cc/resources/pinouts/ABX00083-full-pinout.pdf): board-label positions.

The generator checked hole occupancy, row connectivity, separate sensor and gate nets, the gate series resistor, and shared controller/source ground. A physical load and thermal check is still necessary for this direct-drive arrangement.
