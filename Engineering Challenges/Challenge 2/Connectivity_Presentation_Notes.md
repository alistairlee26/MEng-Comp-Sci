**Your connectivity slide: requirements, choice of connection, and what to say**

The editable PowerPoint contains two alternative versions of the same main slide and one optional backup slide. Present ONE main version. The MQTT version is the default because it fits the supplied campus-network guidance. The HTTP version is a simpler local-network proposal, conditional on staff accepting that scope and the use of the ESP32 access point. All displayed values are examples; the timings are proposed test targets.

**What the teaching slides actually specify**

`3_Bioreactor Design Specification v4_notes.pdf`, page 18, asks for block diagrams and structure charts for the overall system and subsystems, flowcharts explaining functionality, and wireframes of display screens. Page 2 also lists requirements. Page 17 asks you to explain how the UI connects and where data is stored. Page 4 requires logging, monitoring and adjustable setpoints. Pages 14–16 emphasise proving performance through results.

These are project modelling deliverables. I found no rule in the supplied material saying that your individual connectivity slide must contain all of them or prescribing a particular slide layout, duration or count. The main slide therefore combines a block diagram with a simple screen wireframe; the optional backup provides a command flowchart and software structure chart. Requirements and tests remain in the accompanying plan. Check any separate proposal rubric on Moodle if one exists; it was not in the supplied files.

**Is MQTT compulsory?**

I found no explicit requirement to use MQTT in the supplied material. The connectivity lecture teaches it and suggests supporting libraries and brokers, but the specification requires the capabilities: two-way connectivity, monitoring, target adjustment and logging. This is different from claiming staff have already approved every possible alternative.

Standard MQTT uses a broker. If you use HTTP instead, you do not need an MQTT broker. Moving a broker onto the ESP32 would change its location, rather than eliminate its role.

There is one separate dependency: the supplied anomaly-detection simulator streams its data over MQTT. Even if your physical rig uses HTTP, your analysis teammate may still need MQTT to receive that teaching stream. Their detector can consume your real measurements through a backend interface or exported files, but that handoff must be agreed.

**A simpler direct connection: laptop backend calls an ESP32 HTTP API**

```text
Sensors / actuators
       ↕
Control board
       ↕ UART
ESP32 gateway: Wi-Fi access point + small HTTP API
       ↕ direct Wi-Fi connection; JSON over HTTP
Laptop backend: polls state, sends commands, records CSV, serves UI
       ↕ localhost web connection
Browser dashboard
```

The ESP32 creates a password-protected Wi-Fi network. Your laptop joins it. The gateway exposes a few HTTP endpoints; the dashboard application and logger still run on the laptop. This is supported by the ESP32's access-point mode and HTTP server libraries. [Espressif Wi-Fi documentation](https://docs.espressif.com/projects/arduino-esp32/en/latest/api/wifi.html), [official Arduino-ESP32 HTTP server example](https://github.com/espressif/arduino-esp32/blob/master/libraries/WebServer/examples/HelloServer/HelloServer.ino).

A minimal proposed API is:

| Request from laptop backend | Meaning |
|---|---|
| `GET /api/state` | Return latest controller measurement, source sample ID/age, accepted targets and fault flags |
| `POST /api/commands` | Submit a target request carrying a unique command ID; return a pending receipt |
| `GET /api/commands/{id}` | Return pending, applied or rejected, based on the actual controller's result |

Your backend polls state approximately once per second, saves each newly observed sample once, and updates the browser. It forwards user requests to the gateway, which forwards them over UART to the control board. A successful HTTP receipt is not proof the controller applied a command. Show pending until the controller confirms it; use command IDs, validation, timeouts and duplicate handling.

Have the backend make the ESP32 HTTP calls. The browser only calls the backend on the same laptop, keeping the frontend arrangement simple. Logging must run in the backend independently of whether the browser is open. Do not infer a fresh measurement merely from a successful HTTP response: the gateway may be serving cached data after the controller link fails.

Polling just the latest state can miss intermediate samples; use source sequence IDs and record gaps. A buffered range endpoint is an optional later improvement if complete sample capture is required. For an initial prototype, be honest about those gaps rather than claiming lossless collection.

The practical limitations are important:

- This access-point arrangement provides local wireless access, not internet-wide access.
- A laptop with one Wi-Fi adapter will normally leave eduroam when joining the ESP32's network. Do not depend on simultaneous access to the teaching MQTT stream or online assets without another network connection. Store dashboard assets locally and use recorded simulator data when appropriate.
- The specification's pages 12–13 describe sending data to an internet server. Confirm whether a local wireless operator station meets the expected demonstration scope, and whether operating the access point is permitted in the lab.
- The connectivity lecture, page 18, warns against running a server on eduroam. Do not assume placing both devices on eduroam makes this HTTP API reachable.

Another possible architecture is ESP32 HTTP requests to an internet-hosted backend, which avoids a broker and can meet internet access needs. It adds hosting and a command-delivery mechanism, so it is not necessarily simpler than using the provided course broker. USB serial is simpler for initial debugging but does not by itself demonstrate the proposed remote network connection. WebSockets are another option, but one-second HTTP polling is enough for the initial display concept and easier to explain.

**Which main slide should you use?**

Use the MQTT main slide if using eduroam and the course broker is the team's likely path. The board and laptop both connect to that broker, avoiding reliance on direct inbound access to either device. The laptop backend hosts the UI and logger; the broker only routes messages.

Use the HTTP main slide if you want to propose the simpler local arrangement. Keep its visible note about local access and staff confirmation. Present it as a proposal with a known constraint, not an already approved or tested design. Agree the architecture with your team so the other slides' generic “cloud server” labels do not contradict it.

In either case, leave the exact control-board model as “Control board” until the Uno/Nano/Nano ESP32 discrepancy in the team deck has been resolved. The diagram assumes one control board runs all three physical loops.

**What to say for the MQTT slide — approximately 70 seconds**

“Our subsystem lets the operator monitor the reactor, change its targets and save experimental data. Starting on the left, the control board runs the temperature, stirring and pH feedback loops. It exchanges readings and target commands with the ESP32 gateway over UART. The gateway and our laptop application both connect to an MQTT broker, which forwards messages between them.

“The web application and logger run on the laptop. The browser shows the current readings, confirmed targets and trend plots. We will validate target changes and show them as pending until the control board confirms they have been applied. We will also save timestamped measurements and events for the final report and data analysis.

“If communication is lost, the screen will flag stale readings while local control follows the agreed operating policy. We will test live updates, command confirmation and disconnect recovery. The figures along the bottom are proposed targets, not results we have already measured.”

While speaking, point left-to-right across the architecture, then to the three parameter cards, then to the verification strip. Do not explain MQTT packet formats or UART electrical timing unless asked.

**What to say for the HTTP slide — approximately 75 seconds**

“We propose a direct local connection between the reactor and an operator laptop. The control board runs the three physical feedback loops and exchanges readings and target requests with the ESP32 gateway over UART. The ESP32 creates a Wi-Fi network and exposes a small HTTP API, which the laptop application calls.

“The web interface and logger run on the laptop. The application requests the latest state approximately once per second, records new samples and updates the browser. When the operator changes a target, the request travels back to the control board. The UI shows it as applied only after that board confirms it.

“This removes the need for a broker and uses familiar HTTP requests. The trade-off is that it provides local access rather than internet-wide access, so we need to confirm that scope and access-point use with the teaching staff. If the course requires the campus-broker route, we have an MQTT alternative. Both designs retain local feedback control and show stale data when communication fails.”

Point to the Wi-Fi/HTTP link when explaining the simplification. Point to the local-network note when acknowledging the constraint. That is a design question for the proposal discussion, not a hidden limitation.

**Optional backup slide**

The top diagram is the command flow: operator request → UI validation → transport to control board → controller validation → accepted/rejected result → update the UI. It separates application acknowledgement from physical settling time. The lower chart breaks your software into gateway firmware and laptop application modules. Use this slide only if asked about logic or responsibilities, or if the team has room for it.

**Questions and concise answers**

- **Why a block diagram?** It identifies the components, connections, data direction and hosting location requested by the design material. The small dashboard drawing is the required type of screen wireframe.
- **Why not put everything on one ESP32?** That is possible in principle, but the teaching architecture and current team diagram separate control and networking. We must confirm the actual board allocation before committing wiring.
- **Where are the UI and logger hosted?** In a backend process on the operator laptop. The browser is the frontend. Closing the browser does not stop backend logging; stopping the backend or sleeping the laptop does.
- **Why retain MQTT as an option?** It matches the teaching examples and allows gateway and laptop to connect out to a reachable broker. It also gives the analysis program its own subscription.
- **Can HTTP meet the functional requirements?** It can support monitoring, target changes and logging. Local access-point scope still needs checking against the brief's internet-server wording and current lab requirements.
- **Does “200 OK” mean the reactor changed its target?** Only if the response explicitly represents a controller-confirmed result. Our proposed API returns pending first and reports the controller's result separately.
- **What happens on a dropped connection?** Display the last reading as stale, disable new requests, record the gap and recover fresh state on reconnection. Local control follows the policy agreed with subsystem owners.
- **What happens to anomaly detection without MQTT on the rig?** It consumes the same real telemetry through an agreed backend interface or files. The separate course simulator can still use MQTT.
- **What are you proving?** A real reading reaches the UI; a valid target is confirmed; invalid input is rejected; failures are visible; and the recorded data can support performance analysis.

The main slide includes a proposed one-second reporting interval and a stale warning after five seconds. These are communication/UI choices, not sensor sampling or feedback-loop rates. Sensor acquisition and physical control may run much faster. The command-confirmation target is a 95th-percentile time of two seconds on the chosen network, which must be measured.

**Using the files**

Copy the selected main slide from `Connectivity_Proposal_Slides.pptx` into position 7 of your team's editable presentation. All main content is editable text, shapes and lines. The PowerPoint includes speaker notes; this document keeps the same scripts accessible separately. The generated PDF and PNGs are previews of the slide layout. The supplied team deck was a PDF, so its editable source was not available; no original file has been overwritten.

The supporting material for these conclusions is `3_Bioreactor Design Specification v4_notes.pdf`, pages 2, 4 and 12–18; `Connectivity.pdf`, pages 18–20; and `Anomaly_detection_slides.pdf`, pages 31–41. No separate proposal marking rubric or live network test was available in this review.
