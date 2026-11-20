# Heating whiteboard redraw

Source: `WhatsApp Image 2026-11-18 at 11.37.47.jpeg` in the project root.

The SVG is editable; PDF and PNG are provided for documents and presentations.

## Transcription

- A fixed upper resistor and a lower 10 kΩ thermistor form a divider powered from the MCU 3.3 V rail. Node A feeds A0.
- D1 controls the gate of an unspecified N-channel MOSFET. The source returns to ground; the drain connects to the heater.
- The heater label reads 3 Ω, 30 W. The board annotates 12 V and 48 W, with a PWM duty annotation read as 62.5%.
- The fixed resistor value is blurry. It may read 1 kΩ, but the redraw deliberately leaves its value unspecified.
- MCU model, MOSFET part number and thermistor resistance reference temperature are not specified in the photograph.

## Drawing choices

- R1, TH1, H1 and Q1 are added reference designators for clarity.
- The separate ground indications are drawn as an explicit common return.
- The MOSFET is redrawn using a conventional symbol; no extra driver, protection components or filtering have been added.
- This reproduces the lecturer's concept; it is not an independently validated construction design. Whether Q1 operates properly at 3.3 V depends on the actual device. The arithmetic average of PWM power alone does not establish that a heater rated at 30 W may safely be pulsed at 48 W.
