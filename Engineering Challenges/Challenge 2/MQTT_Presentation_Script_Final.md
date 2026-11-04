**Updated MQTT presentation script**

125 words; approximately 52–56 seconds at 135–145 words per minute. This version uses an application server, database storage and CSV export, and allows the broker and application to share a machine. It replaces the earlier laptop-hosted script.

Starting on the left, the control board runs the physical control loops and exchanges readings and target commands with the ESP32 gateway over UART.

The gateway connects over Wi-Fi to an MQTT broker, which forwards messages to our application server. The broker and application can run on the same machine.

The application server hosts the dashboard and database, while the operator accesses the interface through a browser.

The example interface displays temperature, stirring speed and pH, alongside confirmed targets and trend graphs. Users can request new targets within the specified ranges. We validate each request and show it as confirmed once the control board accepts it.

Finally, we store timestamped measurements and provide CSV export, supporting the team's data analysis and evaluation of reactor performance.
