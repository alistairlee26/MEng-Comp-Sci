**Slide 1: Connectivity and User Interface**

Our subsystem connects the reactor to the operator. The control board exchanges measurements and target requests with the ESP32 over UART. The ESP32 and laptop application connect to an MQTT broker, which forwards their messages.

The web application and logger run on the laptop. The interface displays temperature, stirring speed and pH, with their current targets and trends. The operator can request new targets, which we validate and confirm with the control board. We also save timestamped readings for data analysis and export them as CSV.

The interface values shown are examples. Confirm the actual board models and course broker access with the team. Sources: Design Specification pp. 4, 13, 17–18; Connectivity pp. 18–19.

**Slide 2: Connectivity and User Interface**

This alternative uses a direct local Wi-Fi connection. The control board exchanges measurements and target requests with the ESP32 over UART. The ESP32 creates a Wi-Fi network and exposes an HTTP API. The laptop joins that network, requests readings and sends target requests.

The web application and logger run on the laptop. The operator can monitor temperature, stirring speed and pH, adjust their targets, and export timestamped measurements as CSV. A change is confirmed by the control board before the interface reports it as applied.

The interface values shown are examples. This is local wireless access, not internet-wide access. Confirm the local scope and access-point use with staff. The separate teaching simulator still uses MQTT. Reference: Connectivity_Presentation_Notes.md.

**Slide 3: Backup: command flow and software structure**

The top diagram is the command flow: operator request → UI validation → transport to control board → controller validation → accepted/rejected result → update the UI. It separates application acknowledgement from physical settling time. The lower chart breaks your software into gateway firmware and laptop application modules. Use this slide only if asked about logic or responsibilities, or if the team has room for it.

Validation failures stay on the laptop; controller-side validation also remains mandatory. Controller rejection and missing confirmation must be visible. Neither network transport runs the physical feedback algorithms.