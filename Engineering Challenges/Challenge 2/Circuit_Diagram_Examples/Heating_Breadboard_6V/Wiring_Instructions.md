# Heating breadboard guide — Nano ESP32 and IRLB8748

Use **Heating_Breadboard_Guide.pdf** for all three illustrated sheets. PNG and editable SVG versions are also included.

## What this design assumes

- Controller: **Arduino Nano ESP32** from your course kit list. If your board is an Uno, an AVR Nano or a different ESP32 board, the drawn physical pin positions do not apply.
- Confirmed MOSFET: **IRLB8748**, TO-220. Printed face toward you, legs down: **G, D, S** from left to right; metal tab is drain.
- **Regulated 6.0 V**, at least **3 A continuous** supply capacity. At 3 Ω the heater takes about 2 A and produces 12 W at 100% duty. This layout deliberately uses the 6 V setting, not the whiteboard's 12 V / 48 W pulse example. Heating will be slower than a 30 W operating point; the temperature performance must be measured.
- Standard solderless breadboard with numbered strips and A–J holes: 400-point board or strips 1–30 of an 830-point board. The diagram is a placement guide, not to physical scale. Keep the driver, MOSFET and their short control leads close together.
- Nano stays beside the breadboard and is USB powered. Use female-to-male jumper wires on its headers. The power rails of the breadboard are unused, avoiding split-rail ambiguity.

## Parts to have before copying

| Part | Quantity / specification |
|---|---|
| Arduino Nano ESP32 | 1, with headers; USB powered |
| IRLB8748 | Your confirmed MOSFET |
| TC4420 | **1 additional non-inverting driver, PDIP-8 package** (e.g. TC4420CPA). Not TC4429 and not a TO-220/SOIC package |
| R1 | 10 kΩ, 1%, ≥0.25 W |
| R2 | 100 kΩ, ≥0.25 W, driver-input pull-down |
| R3 | 100 Ω, ≥0.25 W, gate series resistor |
| R4 | 100 kΩ, ≥0.25 W, gate-to-source pull-down at the MOSFET connector |
| C1 | 1 µF **ceramic/non-polar**, ≥16 V; use the shown A15/A18 positions with suitably formed leads |
| TH1 | Kit 10 kΩ NTC thermistor |
| H1 | Kit 3 Ω, 30 W-rated immersed heater |
| F1 / F2 | 3 A and 250 mA fast fuses, DC rated above the supply voltage, in insulated holders |
| SW1 | Manual heater-enable switch, ≥5 A DC at ≥6 V |
| Power connections | Secured, insulated terminals/adapter and cable rated ≥5 A DC for the heater loop |

TC4420 accepts the Nano's 3.3 V logic and supplies approximately 6 V gate drive. The IRLB8748 data sheet guarantees low on-resistance at 4.5 V and 10 V gate drive, not 3.3 V. R2 holds the driver input low if the Nano pin floats; R4 is physically at Q1 so an unplugged gate lead does not leave the gate floating. C1 provides the local driver supply bypass recommended by its data sheet. Do not remove the driver and connect D5 straight to the MOSFET in this layout.

## Breadboard connections

A–E of any one number are joined internally. F–J of that number are joined separately. A16 and F16 are **not** connected unless you add a jumper. Crossing insulated wires in the picture do not connect.

| Component | First hole | Second hole | Value |
|---|---|---|---|
| R1 | E3 | E9 | 10 kΩ, 1% |
| R2 | H16 | H22 | 100 kΩ |
| R3 | C17 | C23 | 100 Ω |
| C1 | A15 | A18 | 1 µF ceramic, ≥16 V |
| TH1 probe leads | D9 | D6 | 10 kΩ NTC; either way round |

Place U2 across the centre gap with its **notch to the left**, towards strip 15. The corner next to the notch on the F side is pin 1.

| TC4420 pin | Hole | Function |
|---|---|---|
| 1 | F15 | +6 V |
| 2 | F16 | Input |
| 3 | F17 | NC — leave unconnected |
| 4 | F18 | Ground |
| 5 | E18 | Ground |
| 6 | E17 | Output |
| 7 | E16 | Output |
| 8 | E15 | +6 V |

| Jumper | From | To | Purpose |
|---|---|---|---|
| J1 | B6 | B18 | Ground: sensor section to driver |
| J2 | C6 | G22 | Ground for input pull-down |
| J3 | C12 | C15 | +6 V to driver pin 8 |
| J4 | D15 | G15 | Join driver VDD pins 1 and 8 |
| J5 | D18 | G18 | Join driver GND pins 4 and 5 |
| J6 | D16 | D17 | Join driver output pins 7 and 6 |
| J7 | J18 | J29 | Driver ground to external ground lead |

| External lead | Connection | Breadboard hole |
|---|---|---|
| N1 | Nano 3V3 | B3 |
| N2 | Nano A0 | B9 |
| N3 | Nano GND | A6 |
| N4 | Nano D5 | I16 |
| P1 | Fused +6 V driver branch (page 2) | A12 |
| P2 | Supply-negative star point (page 2) | H29 |
| P3 | MOSFET gate (page 2) | B23 |
| T1 | One thermistor lead | D9 |
| T2 | Other thermistor lead | D6 |

## External heater wiring

1. Set the regulated output to **6 V** with the heater disconnected. Connect supply positive to two separate branches: heater branch through **F1 (3 A)** and **SW1** to heater positive; driver branch through **F2 (250 mA)** to **A12**. Fit the holders near the supply.
2. Heater negative → **IRLB8748 drain, middle leg (2)**. The tab is also drain: keep it insulated from ground and other wiring.
3. **IRLB8748 source, right leg (3)** → supply negative using a separate power lead. This is the approximately 2 A return; it never passes through breadboard contacts, Nano pins or the USB cable.
4. **H29** → the same supply-negative terminal with a separate low-current wire. This joins Nano, sensor and driver ground to the power circuit.
5. **B23** → IRLB8748 gate, left leg (1), keeping the connection short. Fit **R4 = 100 kΩ between gate and source at the MOSFET connector**, rather than at the far end of a detachable gate lead.
6. Use an insulated soldered adapter or suitably rated terminal arrangement for Q1. The drawing does not call for bare wires wrapped around its legs. Use individual secured connections; do not mount the high-current drain/source loop on the solderless board.

The two fuse values assume the listed cable/terminal ratings and regulated source. Verify the actual fuse time/current characteristics and supply fault behaviour when assembling. The small driver branch does not carry heater current. Keep all 6 V wiring away from Nano 3V3, VBUS, VIN and signal pins. Heater power is controlled by the external circuit, while the Nano is powered only by USB.

## Assembly and checks

1. Disconnect USB and the heater supply. Fit U2, R1–R3, C1 and every jumper using the tables. Verify the IC notch; inspect for adjacent shorts. R4 is at the external MOSFET connector.
2. With power disconnected, check continuity: upper strip 15 to lower strip 15; upper strip 18 to lower strip 18; upper 16 to upper 17; Nano GND to the supply-negative star. Confirm lower strip 17 (U2 NC) is not wired. Capacitors may briefly change an ohmmeter reading; a reading through a resistor is not the same as a short.
3. Leave the heater isolated with SW1 open. Connect USB only. Verify about 3.3 V at B3 and the divider voltage at B9. For a 10 kΩ thermistor at 25°C, the ideal divider gives about 1.65 V. Warming the NTC should lower the voltage. Do not assume the same ADC reading as an Uno.
4. Load code that makes **D5 LOW immediately at startup**. Check 6.0 V on the supply before connecting it. Apply the driver branch with heater still disconnected. Verify pins 1 and 8 of U2 are about +6 V relative to source; with D5 LOW, gate-to-source voltage should be near zero.
5. With the heater disconnected, briefly set D5 HIGH and verify about +6 V gate-to-source, then restore LOW. If either state is wrong, disconnect power and correct the wiring before connecting the heater.
6. Switch off and disconnect power. Connect the heater power loop, place the heater and thermistor correctly in the liquid, then repeat the LOW/off check before closing SW1. Start with a short, supervised heating test; monitor liquid temperature and power connections. Do not energise the heater dry.

## Changes from the lecturer's sketch

- Added the TC4420, local bypass capacitor, input pull-down, gate resistor and gate-to-source pull-down for the confirmed IRLB8748 and 3.3 V Nano.
- Chose a definite **10 kΩ** fixed divider resistor, because its whiteboard value was unclear. Calibrate using this actual resistor.
- Used **D5**, not D1/TX, to leave the UART transmit connection available. In code use `D5` and `A0` board-label constants; do not substitute the numeric GPIO pin names.
- Selected **6 V**, giving up to about 12 W. The whiteboard's 62.5% duty annotation is not this design's required operating duty. At 6 V, 62.5% would average about 7.5 W. Feedback must determine the required duty.

## Sources and verification

- [Arduino Nano ESP32 official pinout](https://docs.arduino.cc/resources/pinouts/ABX00083-full-pinout.pdf)
- [Arduino Nano ESP32 manual](https://docs.arduino.cc/resources/datasheets/ABX00083-datasheet.pdf)
- [Infineon IRLB8748 data sheet](https://www.infineon.com/assets/row/public/documents/24/49/infineon-irlb8748-datasheet-en.pdf)
- [Microchip TC4420/TC4429 data sheet](https://ww1.microchip.com/downloads/en/DeviceDoc/21419D.pdf)
- [BusBoard BB830 specification](https://www.busboard.com/BB830): an example quality solderless board is rated at 2 A. This design keeps heater current entirely off the board rather than relying on an unknown board's contact rating.

The generator checked occupied-hole conflicts, row-strip connectivity, separate 3.3 V / 6 V / ground / signal nets, the two connected driver supplies, both grounds, both outputs, and the unused NC pin. `Connectivity_Check.json` records the result. This is a drawing and connection check; no physical prototype, supply transient measurement, calibration or thermal performance test has been performed.
