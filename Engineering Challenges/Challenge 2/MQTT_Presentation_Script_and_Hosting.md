**One-minute script for the simplified MQTT slide**

129 words. Approximately 53–57 seconds at 135–145 words per minute; rehearse once to account for pauses.

Our subsystem connects the bioreactor to the operator. Starting on the left, the control board runs the physical control loops and exchanges readings and target commands with the ESP32 gateway over UART.

The gateway connects over Wi-Fi to an MQTT broker, which passes messages between the reactor and our laptop application.

The laptop hosts the web interface and logger, and the operator accesses the dashboard through a browser.

The example interface shows temperature, stirring speed and pH, alongside confirmed targets and trend graphs. Users can enter new targets within the specified ranges. We will validate each request and display it as confirmed once the control board accepts it.

Finally, we will log timestamped measurements and export them as CSV, supporting the team's data analysis and evaluation of reactor performance.

Point across the upper diagram during the first three paragraphs, then at the example interface. The readings and graph shapes on the slide are illustrative.

**Likely audience questions and suggested answers**

| Question | Suggested answer |
|---|---|
| Why did you choose MQTT? | It provides lightweight two-way messaging suited to the ESP32. The dashboard and analysis program can subscribe to the same measurements, and it matches the teaching examples. |
| What does the broker do? | It receives messages on named topics and forwards them to subscribed clients. It does not calculate the physical control outputs. |
| Where will the broker run? | We can use the course broker, or host our own broker on an existing rented server. We will test access from the lab before finalising that choice. Do not describe the rented-server option as already deployed. |
| Where are the website and data hosted? | In the design shown, the backend and logger run on the laptop, with a browser displaying the interface. The broker can be on a different server. |
| Why UART between the boards? | It provides a straightforward two-way byte stream between nearby boards. We agree pins, voltage levels, baud rate and message format. |
| Why two boards if the Nano ESP32 has Wi-Fi? | We propose separating local control from networking, following the teaching architecture. It is a design choice; one sufficiently capable board could perform both roles. Confirm the actual boards with the team. |
| How do you know a target change succeeded? | The controller returns a result carrying the request's ID and accepted value. Until that arrives, the UI shows pending. The fluid reaching the target is a separate, slower process. |
| How do you stop invalid inputs? | Validate targets in the application and again on the controller: 25–35 °C, 500–1500 RPM and pH 3–7. Measurements outside those ranges are still displayed and logged. |
| How will you prove it works? | Demonstrate a sensor reading, a confirmed target change, rejection of invalid input and an exported log. Compare physical performance with the required tolerances using suitable measurements. |
| What happens if the network or laptop stops? | The control board follows its locally agreed operating policy. Remote monitoring and laptop logging are interrupted. We should not claim continuous logs unless buffering has actually been implemented. |
| How will Data Analysis get the readings? | It can subscribe to the same telemetry topic, or consume the logged records. Agree the schema with that teammate. |
| Are those readings real? | No. The slide shows an example interface for the proposal; measured results will come from integration testing. |

**What the teaching slides say about MQTT and hosting**

The supplied `Connectivity.pdf` explains publish/subscribe messaging on pages 16–17. Page 18 recommends the PicoMQTT library and discusses an ESP32-hosted broker, then explicitly warns that eduroam will not allow you to run a server on it. It says that such a broker would need to be on another network.

Page 19 lists public test brokers, `broker.hivemq.com` and `test.mosquitto.org`, and a course broker, `engf0001.cs.ucl.ac.uk`. It says the course broker is visible only within UCL. This documents the teaching material, not a current availability or firewall test.

The design specification's pages 12–13 describe two-way communication with a server on the internet. An internet-hosted broker fits that connectivity description. A broker alone does not provide the storage and display functions: the proposed laptop backend and logger supply them. If staff expect storage and the UI themselves to run on an internet server, clarify that hosting detail; they can be moved to your server later.

The slides recommend tools but do not explicitly require MQTT or a particular website framework.

**How MQTT works in your project**

MQTT is a messaging protocol. Your ESP32 firmware and laptop backend each use an MQTT client library. Each client establishes a connection to the same broker and can publish and subscribe. This model supports two-way device/cloud communication. [MQTT overview](https://mqtt.org/).

A topic is a routing name, such as `cseee21/rig01/telemetry`. The payload is the actual content, for example:

```json
{"temperature_C":29.8,"rpm":998,"pH":5.02}
```

This is a simplified illustrative payload. The implemented version should also identify the sample and accepted targets.

For measurements:

1. The control board sends a reading to the gateway over UART.
2. The gateway publishes it to the telemetry topic.
3. The broker forwards it to subscribed clients.
4. The laptop application displays and records it. The analysis program may receive the same message through its own subscription.

For commands:

1. The laptop application publishes a target request on a command topic.
2. The subscribed gateway receives it and forwards it over UART.
3. The controller validates and applies or rejects it.
4. The gateway forwards the controller's result on an acknowledgement topic.
5. The laptop updates its displayed command status.

Both directions use client connections that are already established. A remote command does not require the broker to open a new inbound connection to the ESP32.

**What is the broker?**

The broker is a server program, rather than special physical hardware. Eclipse Mosquitto is one broker implementation you could install on your rented server. PicoMQTT is the client library recommended for your board; it is not a hosted service that gives you a server account.

A rented server provides the computer on which the broker program runs. The same machine may also run a website, database or other applications, but those remain separate software services.

The broker routes messages. Retained messages or broker persistence do not replace an experimental time-series logger.

**How your rented server could be useful**

If it is a VPS or similar server that lets you install a persistent service or container and configure network access, it is a suitable candidate for a private broker. Restricted website-only hosting may not provide those capabilities.

For the first implementation, keep the current slide's layout:

```text
ESP32 on eduroam ── MQTT connection ──┐
                                    │
                        Broker on your rented server
                                    │
Laptop application ─ MQTT connection┘
       ↕
Browser dashboard
       |
Backend records CSV on laptop
```

Both the ESP32 and laptop initiate connections out to your server. The eduroam warning in the lecture concerns hosting a server on that network; it does not establish that clients cannot reach a broker elsewhere. However, actual outbound access to your chosen server and port still needs testing from the lab.

Your server's broker must be reachable on its configured listener. MQTT over TLS commonly uses TCP port 8883, but configuring that port alone does not enable encryption: the broker needs certificates and the clients must verify them. [Mosquitto configuration documentation](https://mosquitto.org/man/mosquitto-conf-5.html).

A practical setup would involve:

1. Install a Mosquitto broker service or container on the existing server.
2. Configure a reachable hostname, TLS listener and the necessary server/provider firewall rule.
3. Disable anonymous access, create client credentials and restrict who can publish commands through topic permissions.
4. Configure the ESP32 and laptop MQTT clients with the hostname, port and their credentials; verify the server certificate.
5. Test harmless telemetry and a dummy target round trip from the lab before attaching requests to real outputs.

Mosquitto supports password-based authentication and topic access control. Its documentation recommends encryption when sending credentials. [Mosquitto authentication guide](https://mosquitto.org/documentation/authentication-methods/), [configuration reference](https://mosquitto.org/man/mosquitto-conf-5.html).

PicoMQTT supports a custom secure network client for TLS connections; use the version and example appropriate to your board. [PicoMQTT documentation](https://github.com/mlesniew/PicoMQTT).

No server access, installation, firewall change or deployment was performed while preparing this guide.

**Should you also put the dashboard on your server?**

You can later host the backend, logger and dashboard on the same rented server. That would let logging continue when your laptop is off, as long as the server and reactor connection remain operational. The browser would then access the server-hosted website, and the diagram's “Laptop backend” box would need changing to “Cloud backend”.

For the first version, hosting only the broker there keeps the implementation consistent with the current slide. You retain the option to use the course broker if your own server setup proves inconvenient.

If asked about hosting during the proposal, a precise answer is:

“We plan to connect both the ESP32 and laptop to an external MQTT broker. We can use the course broker or host a private broker on an existing rented server. The dashboard and logger will initially run on the laptop, and we will verify the connection from the lab.”

Choose one broker for the actual rig and point all its clients at it. Your analysis teammate's separate teaching-simulator subscription may still connect to the simulator's public broker.

