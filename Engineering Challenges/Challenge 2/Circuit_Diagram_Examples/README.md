# Circuit diagrams extracted from Moodle teaching materials

These are figures from the course materials, not newly designed subsystem circuits.

## Breadboard design added later

The current option for the user's available IRLB8748, without the unavailable TC4420, is in `Heating_Breadboard_No_Driver/`. Read its PDF and wiring instructions together, including the required direct-drive load check. `Heating_Breadboard_6V/` preserves the earlier TC4420-based option.

## Images

- `01_MOSFET_Switch_Heating_Reference_Transistors_Slide_06.png`: cropped circuit figure from **Introduction_to_Transistors.pdf**, slide 6. Generic low-side MOSFET switch, suitable as a starting point for the heater power stage. It does not include thermistor sensing or a complete heating subsystem.
- `02_Stirring_Circuit_MotorHallSensorInstructions_Slide_03.jpeg`: original embedded circuit image from **MotorHallSensorInstructions.pptx**, slide 3. Shows the motor, speed sensor, MOSFET, flyback diode, 470 uF capacitor and microcontroller connections.
- `Context/Transistors_Slide_06_Full.png`: the complete transistor slide, including its explanation.

## pH

No complete pH subsystem circuit picture was found in the slides checked. **Bioreactor Tips.pdf**, slide 8, gives text instructions for connecting the pH breakout board to 5 V, ground and an analogue input. The generic MOSFET switching circuit above is a starting point for each pump power stage; pump circuits also need appropriate flyback protection. It is not a complete pH circuit.

## Moodle sources

- Introduction to Transistors: https://moodle.ucl.ac.uk/mod/resource/view.php?id=9105526
- Motor subsystem instructions folder: https://moodle.ucl.ac.uk/mod/folder/view.php?id=9105547
- Tips for Completing the Bioreactor: https://moodle.ucl.ac.uk/mod/resource/view.php?id=9105559

The source examples include 5 V Uno/Nano hardware. Check voltage and component compatibility before adapting them for Nano ESP32 hardware with 3.3 V I/O.
