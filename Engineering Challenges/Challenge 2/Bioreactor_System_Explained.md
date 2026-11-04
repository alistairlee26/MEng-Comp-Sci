**Your bioreactor project, explained from the beginning**

This guide assumes you are comfortable programming but unfamiliar with the project's electronics and communication protocols. It explains a proposed implementation, not an already verified team design. Your supplied slides disagree about the boards being used, so the choices to confirm with your team are identified explicitly.

Read this before the more detailed `Connectivity_and_UI_Plan.md`. This guide establishes what the pieces are and how they fit together; that plan contains the fuller reliability and testing requirements. Prepared on 2 November 2026.

The MQTT design explained here is a recommendation, not an explicit course requirement. For a simpler direct-HTTP alternative, its local-network limitations, and the finished editable proposal slides, see `Connectivity_Presentation_Notes.md` and `Connectivity_Proposal_Slides.pptx`.

**Start with the physical system.**

Your testbed is a container of liquid with equipment that measures and changes three properties: temperature, stirring speed and pH. The wider context is bioreactor operation and vaccine manufacturing, but your practical engineering task is to build and demonstrate the monitoring and control system described in the brief. That context does not mean your team is expected to manufacture a vaccine with this testbed.

There are two kinds of physical components:

- A **sensor** reports something about the liquid or machinery.
- An **actuator** changes something about it.

| Subsystem | What measures it? | What changes it? |
|---|---|---|
| Heating | Thermistor: a component whose resistance changes with temperature | Heating element |
| Stirring | Speed sensor: produces electrical pulses as a shaft rotates | Motor and stirrer |
| pH | pH probe and its interface electronics | Pumps adding acid or alkali |

A microcontroller is a small computer with pins for interacting with these components. Your team writes a program, usually called **firmware**, and uploads it to the board. It then runs on the board, rather than on the laptop that uploaded it. The board still needs power, but it does not normally need the Arduino IDE to remain open.

Sensors do not necessarily produce convenient numbers such as `29.8 degrees`. For example, the thermistor produces a resistance change; circuitry turns that into a voltage, an analogue-to-digital converter measures the voltage, and software converts the result to temperature using a calibration. The EEE and control-software work produces a usable measurement for your communications code.

Similarly, a microcontroller's output pin does not directly power the heater or pump. It controls a driver circuit, such as a MOSFET switch, which controls power to the actuator. A PWM signal rapidly switches an output on and off; changing its duty cycle changes the average drive applied. Your UI generally should not choose individual switching pulses.

Your boundary can therefore be expressed as two software operations:

```text
get latest measurements and operating state
request a new target value
```

The team must agree exactly where those operations are implemented and how they are exposed to you.

**What is a control loop, and what does the operator actually change?**

A **setpoint** is a desired value. If the operator chooses 30 °C, the control software repeatedly measures temperature, compares it with 30 °C and adjusts the heater. That repeated measure–compare–adjust process is a feedback control loop.

An intentionally simplified illustration is:

```text
repeat at the agreed control interval:
    temperature = read_calibrated_temperature()
    heater_output = temperature_controller(temperature, temperature_target)
    apply_heater_output(heater_output)
```

The stirring and pH subsystems have their own equivalent calculations. The actual algorithms and timing are for the control team to design and tune. They may use hysteresis, PI or PID control, depending on the subsystem.

Changing `temperature_target` from 30 to 32 changes the goal of the loop. It does not instantly make the liquid 32 °C. Keep these three things separate:

| Item | Example | Meaning |
|---|---|---|
| Measured value | 29.8 °C | What the sensor currently reports |
| Accepted setpoint | 30.0 °C | What the controller is currently trying to achieve |
| Requested setpoint | 32.0 °C | What the user has asked it to achieve next |

The course specifies temperature targets of 25–35 °C with ±0.5 °C control accuracy, stirring targets of 500–1500 RPM with ±20 RPM accuracy, and pH targets of 3–7. The provided specification does not give a numerical pH tolerance. Those are from page 4 of `3_Bioreactor Design Specification v4_notes.pdf`.

Keep these loops on the control board. Network latency, a closed browser or a laptop going to sleep should not determine when the next heater-control calculation occurs.

**Why are there multiple controllers?**

The word “controller” is overloaded. A temperature controller can mean an algorithm. A microcontroller means a physical chip or board. An I²C controller means whichever device initiates a particular bus transaction. These are different uses of the same word.

For the proposed project architecture, think of two physical boards:

| Board role | Main job | Program running on it |
|---|---|---|
| Board A: control board | Read sensors and operate the heater, stirrer and pumps | Control firmware, plus a small communications interface |
| Board B: gateway | Exchange data with Board A and the network | Gateway firmware: serial messages, Wi-Fi, MQTT |

“Gateway” just means a program/device that transfers information between two communication systems. Here it transfers between a wired board-to-board link and network messages.

The older specification describes an Arduino Uno, which needs additional hardware for Wi-Fi. A separate ESP32 supplies that network connection. Your newer equipment list names a Nano ESP32, which already has Wi-Fi. A single suitably programmed ESP32 could in principle perform both roles, subject to pins, resources and timing. The course connectivity lecture nevertheless describes using at least two boards, and your current overall diagram also shows two.

My recommendation is to work with that two-board structure unless your team and teaching staff establish a different intended arrangement. It divides the work and reduces the interaction between networking and local control, but adds a communication interface that you must implement. The second board is not automatically required because the first is called “Arduino”. [Arduino's Nano ESP32 documentation](https://docs.arduino.cc/hardware/nano-esp32/) confirms its Wi-Fi capability.

Also, three physical subsystems do not automatically imply three control boards. One board can run three control algorithms. Your current overall diagram appears to propose one shared control board. Ask whether that is actually the agreed integration plan. If teammates prototype on separate boards, decide how their code will eventually be combined and who owns the combined firmware.

**What connects to what, and where does each program run?**

This is the proposed first working arrangement:

```text
AT THE REACTOR

  Temperature / pH / speed sensors
                 |
                 | electrical sensor signals
                 v
      Board A: control firmware ---- driver circuits ---- heater / motor / pumps
                 ^
                 | UART wires: messages in both directions
                 v
      Board B: ESP32 gateway firmware
                 ^
                 | Wi-Fi -> access point -> network
                 | MQTT connection
                 v
  MQTT BROKER ON A REACHABLE SERVER
                 ^
                 | another MQTT connection
                 v
ON YOUR LAPTOP

      Dashboard application / backend ---- CSV files or database
                 ^
                 | HTTP and live browser updates
                 v
          Browser showing the dashboard
```

There are two independent network connections to the broker: one from the gateway, one from the laptop application. The broker forwards messages between them over those existing connections. The ESP32 does not need to discover your laptop's IP address in this arrangement.

| Connection | What travels over it? | What it is for |
|---|---|---|
| Sensors → Board A | Voltages or digital signals/pulses | Acquire physical measurements |
| Board A → driver circuits | Control signals | Drive actuators |
| Board A ↔ Board B | Framed byte messages over UART, or an agreed I²C alternative | Transfer measurements, requests and results |
| Board B ↔ broker | MQTT messages over a network connection using Wi-Fi | Connect the rig to network applications |
| Laptop backend ↔ broker | MQTT messages | Receive telemetry and send requests |
| Browser ↔ laptop backend | Web requests and live updates | Let a human use the system |
| Backend → disk | CSV rows or database records | Preserve experiment history |

USB cables used for uploading firmware, debugging or powering boards are separate from this proposed runtime data path. You can use USB serial in early experiments, but do not accidentally demonstrate only a USB-connected laptop when the required feature is remote network monitoring.

**UART: a stream of bytes between two boards.**

For a programmer, UART is similar to having a very simple bidirectional byte stream connecting two devices. You write bytes on one side, and read arriving bytes on the other. There is no IP address, broker or web server involved.

The usual wiring is:

```text
Board A TX  -----------------> Board B RX
Board A RX  <----------------- Board B TX
Board A GND ------------------ Board B GND
```

TX means transmit and RX means receive. The common ground provides a shared voltage reference. This wiring diagram describes signals, not how to power the boards.

Both ends agree a speed and format, for example **115200 baud, 8N1**. For ordinary UART that means 115200 bits per second on the wire, with eight data bits, no parity bit and one stop bit per frame. Hardware handles the individual bits; you use the serial library. You do not need to implement electrical timing in C++.

However, UART only transports bytes. It does not know where your JSON messages end. You define an application format, for example one compact JSON object per line:

```text
{"type":"telemetry","seq":42,"temperature_C":29.8}\n
{"type":"telemetry","seq":43,"temperature_C":29.9}\n
```

Here `\n` means an actual newline byte. A read may contain part of a line or several lines. Accumulate bytes until a newline, then parse the complete record. Set a maximum record length and discard an oversized record through its next newline so the parser can recover. Debugging text should use a different serial channel.

An illustrative ESP32 API fragment is:

```cpp
// Fragment only: agree and define these pins for the actual board first.
HardwareSerial reactorLink(1);

// In setup(): RX comes before TX in this API.
reactorLink.begin(115200, SERIAL_8N1, REACTOR_RX_PIN, REACTOR_TX_PIN);

// Sending a complete record, terminated with a newline:
reactorLink.println("{\"type\":\"ping\",\"id\":1}");

// In loop(): feed arriving bytes into your bounded line parser.
while (reactorLink.available() > 0) {
    feedLineParser(reactorLink.read());
}
```

`feedLineParser` is your own function, not an Arduino library function. Start by exchanging a ping and response, then add JSON messages. Avoid waiting indefinitely for input, because the rest of the firmware must keep running. The API fragment follows [Espressif's HardwareSerial documentation](https://docs.espressif.com/projects/arduino-esp32/en/latest/api/serial.html); it is not a complete sketch or a verified pin assignment.

Ask an EEE teammate to verify voltage compatibility and pin availability. “Arduino Nano” is not enough information: a classic Nano and Nano ESP32 differ. A 5 V output must not simply be attached to a 3.3 V-only input. The supplied kit's board labels and pin mapping matter more than an arbitrary wiring example online.

**I²C: an alternative for the board-to-board link.**

I²C uses a shared data line, SDA, and clock line, SCL, plus a common ground. Devices have bus addresses. A device acting as bus controller initiates reads/writes to an addressed peripheral. The lines need suitable pull-up resistors and compatible voltage levels.

For example, the gateway could initiate a write carrying a target request to the control board at an agreed address, then later initiate a read of its latest measurements. Those transaction roles do not decide which board runs the reactor's control algorithms.

In Arduino's `Wire` API, the initiating side uses `beginTransmission`, `write`, `endTransmission` and `requestFrom`. The responding side registers receive/request callbacks and prepares response data. Keep transactions within the implementation's buffer limits and callbacks brief. See [Espressif's I²C documentation and examples](https://docs.espressif.com/projects/arduino-esp32/en/latest/api/i2c.html).

You do not need both UART and I²C between the same pair of boards for this proposed design. Use UART if the link has not been decided; keep I²C if your team already has a suitable working implementation. Both still require agreement about the meaning of the transferred bytes. The project's `Connectivity.pdf`, pages 5–14, explains both options.

**Wi-Fi, MQTT, topics and brokers are different pieces.**

Wi-Fi gets the gateway onto a network. MQTT specifies how applications exchange named messages over network connections. A **broker** is the running server program that accepts MQTT client connections and routes messages. A **client** is a connected program, such as your gateway firmware or dashboard backend.

A client can both publish and subscribe:

- **Publish:** send a payload with a topic name.
- **Subscribe:** ask to receive messages matching a topic.
- **Topic:** a routing label, such as `cseee21/rig01/telemetry`.
- **Payload:** the message content, such as a JSON object.

A topic resembles a path but is not a web page or disk folder. The broker generally routes the payload without knowing what temperature or pH mean. This is an event-distribution pattern: your application defines the event meanings. [MQTT 3.1.1 specification](https://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html).

For this project, define these topics together:

| Topic | Who publishes? | Who subscribes? |
|---|---|---|
| `cseee21/rig01/telemetry` | Gateway | Dashboard backend and analysis program |
| `cseee21/rig01/command` | Dashboard backend | Gateway |
| `cseee21/rig01/ack` | Gateway, forwarding the control board's result | Dashboard backend |
| `cseee21/rig01/status` | Gateway | Dashboard backend |
| `cseee21/rig01/alerts` | Analysis program | Dashboard backend/logger |

All participants must use the same broker and matching topic names. Connecting successfully to different brokers will not join them into one system. Give concurrently connected clients distinct client IDs.

You do not write a broker yourself. You connect to an existing one, or run an existing broker program if local hosting is chosen. Your gateway does need your own firmware to translate between UART and MQTT; installing a library does not automatically bridge those links.

The gateway's logic can be expressed as:

```text
when a valid telemetry record arrives over UART:
    publish it to the telemetry topic

when a command arrives from MQTT:
    validate its structure and destination
    queue a corresponding UART request to the control board

when a control-board result arrives over UART:
    publish it to the acknowledgement topic
```

Keep message types explicit so forwarding does not accidentally create an echo loop. A broker delivery acknowledgement is not proof that the control board accepted a target; your `ack` payload provides that application-level result.

**How you implement the gateway in practice.**

Use the Arduino IDE or your team's agreed embedded build environment. Select the exact board and install the course-recommended PicoMQTT library. Its client API offers `subscribe`, `publish`, `begin` and a regularly serviced `loop`; the documentation provides an ESP32 example. [PicoMQTT documentation](https://github.com/mlesniew/PicoMQTT).

Work through these layers separately:

1. Upload a program and see its debugging output.
2. Use the supplied `eduroam.ino` to establish Wi-Fi in the lab. It also has a normal-network option. Wi-Fi success alone does not establish broker connectivity.
3. Configure the confirmed broker hostname, port, credentials and encryption settings; publish one synthetic reading.
4. Subscribe to your command topic and print a test request to debugging output.
5. Add the UART message parser and forwarding logic.

The supplied `eduroam.ino` connects during setup and has an empty main loop. MQTT, reconnection behaviour and UART forwarding remain to be added. Do not place personal Wi-Fi credentials in shared slides or committed source files.

The gateway's ongoing work should resemble this pseudocode:

```text
repeat:
    service Wi-Fi connection state / scheduled reconnect attempt
    service MQTT
    consume a bounded amount of UART input
    forward complete validated messages
    send queued requests when possible
    update link freshness / pending-request timeouts
```

This is a small event-processing program. Avoid long blocking waits in callbacks or the main loop. A gateway restart must not require restarting the physical control program.

**Where is the web application hosted?**

“Hosted” simply means “running somewhere that serves the application”. For your first version, I recommend your own laptop. There is no separate website hosting service required to open a local web application in your browser.

With the earlier Node-RED recommendation:

- Node-RED runs as a process on your laptop. It is the backend/runtime.
- FlowFuse Dashboard adds the operator web interface to that process.
- Your browser loads that interface from the laptop.
- Node-RED connects to the MQTT broker and writes experiment files on the laptop.
- The broker runs wherever the chosen broker service is hosted, which may be a different machine.

The broker is not automatically the website host. A “cloud” box in a diagram does not specify a service that already exists.

The Node-RED editor is normally reached at `http://localhost:1880`. The dashboard has its own configured route, for example `/dashboard`. `localhost` means the machine making the connection: on your laptop it means your laptop; on an ESP32 it would mean the ESP32, not your laptop. Use the broker's actual reachable hostname in the gateway. [Node-RED local setup](https://nodered.org/docs/getting-started/local), [FlowFuse Dashboard setup](https://dashboard.flowfuse.com/getting-started.html).

You can close the browser and leave the backend logging, provided the backend is running and you have implemented logging there. If you stop the backend or the laptop sleeps, that version's dashboard service and logger stop. The reactor controller should still follow its local operating policy.

There are three deployment arrangements worth distinguishing:

| Arrangement | Broker location | App location | Implication |
|---|---|---|---|
| Recommended first lab setup | Reachable course broker | Your laptop | No incoming connection to the laptop is needed from the ESP32 |
| Private-network demonstration | Laptop or another local machine | Your laptop | ESP32 must reach the broker's LAN address; routing and firewall rules must permit it |
| Internet-accessible dashboard | Suitable reachable server/service | Hosted server | Requires deployment and access control; neither is provided automatically by MQTT |

The course lecture lists `engf0001.cs.ucl.ac.uk` and says it is visible only inside UCL. It also says not to run a server on eduroam. Treat these as constraints in the provided material and verify current lab instructions. I have not tested the broker's current availability, credentials or ports. A laptop backend accessed only by its own browser can still connect out to that broker without requiring the ESP32 to reach a server on the laptop.

The gateway and backend do not inherently need to be on the same Wi-Fi network; both need network access to the chosen broker. A UCL-only broker restricts where that is possible. Likewise, a locally hosted dashboard is not automatically accessible to someone on another laptop. Ask staff whether “remote” means a networked operator station or a website accessible from other machines: the local operator-station setup demonstrates network connectivity, but wider browser access is a separate deployment decision.

**Do you have to use Node-RED?**

No. The provided lecture allows a choice of interface technology. Node-RED is a practical option, not a requirement, and your programming experience may make a custom application equally reasonable.

If you prefer a familiar backend framework, the same architecture becomes:

```text
Browser UI
    ↕ HTTP plus WebSocket/SSE, or polling for updates
Your JavaScript/Python backend
    ↕ MQTT client library
MQTT broker
```

The backend owns the MQTT connection, validation, command tracking and logging. The frontend owns display and user input. This keeps the protocol plumbing in one persistent process. A browser can alternatively use MQTT over WebSockets if the broker supports it, but you do not need that additional arrangement for the proposed backend design.

Choose the stack you can debug reliably. My earlier Node-RED recommendation was intended to reduce application-building work, not to suggest that your interface must be low-code.

To try the Node-RED route on Windows, install a supported Node.js version, install Node-RED with `npm install -g node-red`, and start it with `node-red`. These are suggested future setup steps; nothing has been installed for this guide. The [official local instructions](https://nodered.org/docs/getting-started/local) describe this process.

Install `@flowfuse/node-red-dashboard` through Manage Palette. Its forms, charts and display widgets can then be connected to flows. [FlowFuse installation guide](https://dashboard.flowfuse.com/getting-started.html).

Start with this flow, using generated data:

```text
MQTT In -> JSON parsing -> schema validation -> extract values -> display/chart
                                           -> append timestamped record to file

UI form -> range validation -> assign command ID -> MQTT Out

MQTT In for ack -> match pending command -> update confirmed target/status
```

Node-RED's MQTT In/Out nodes share a broker configuration. [Official MQTT connection example](https://cookbook.nodered.org/mqtt/connect-to-broker). You still implement the validation, acknowledgement tracking and logging semantics yourself.

**Follow a reading and a command all the way through.**

Imagine the temperature is 29.8 °C and the accepted target is 30 °C.

1. The thermistor and measurement circuit produce a reading on Board A.
2. Board A converts it into 29.8 °C and runs its heating-control calculation locally.
3. Board A sends a telemetry record over UART to Board B.
4. Board B publishes that record on `cseee21/rig01/telemetry`.
5. The broker forwards it to subscribed clients, including your application and the analysis program.
6. Your backend records the sample and updates the browser display.

Now the operator requests 32 °C:

1. The user enters 32 and presses Apply.
2. The backend checks the allowed range, assigns a command ID and publishes a command. The UI shows pending.
3. The broker forwards the command to the gateway subscription.
4. The gateway sends the request over UART to Board A.
5. Board A validates it again and updates its temperature target to 32.
6. Board A returns a result with the same command ID and accepted value.
7. The gateway publishes that result on the acknowledgement topic; the broker forwards it to your backend.
8. The UI shows the confirmed target as 32. The measured temperature may still be 29.8.
9. Subsequent telemetry shows the liquid approaching the new target as the local loop operates.

If no result returns, show “unconfirmed” or “timed out”; do not assume success. A lost acknowledgement can also mean the change happened but the confirmation was lost, so recover the actual accepted target from fresh controller state.

**The small shared contract your team needs.**

Treat the controller firmware as another service in a distributed application. Before implementation, agree its API, even though the transport is a wire.

An illustrative telemetry message is:

```json
{
  "type": "telemetry",
  "schema": 1,
  "device": "rig01",
  "boot_id": "boot8",
  "seq": 42,
  "sample_ms": 42000,
  "temperature_C": 29.8,
  "rpm": 998,
  "pH": 5.02,
  "setpoints": {"temperature_C": 30.0, "rpm": 1000, "pH": 5.0},
  "valid": {"temperature_C": true, "rpm": true, "pH": true}
}
```

These fields are a proposal. `seq` identifies a new sample; `sample_ms` is time since that controller boot, not calendar time; `boot_id` changes when it restarts. The backend adds its own receipt timestamp for logging. Do not manufacture a new sample number on the gateway when the controller has stopped producing data.

Agree at least:

- Names, units and types, including whether a missing value is `null` plus a validity flag.
- Framing and maximum message size; UART newline JSON is only one option.
- A reporting rate, initially around one report per second. Control-loop timing is a separate decision.
- How requests identify the parameter, desired value, device and command ID.
- Applied/rejected results, including the matching command ID and reason for rejection.
- How old and duplicate requests are rejected or handled consistently.
- How freshness, reboot and disconnection are represented.

Use absolute requests such as “set temperature to 32”, rather than “increase it by 2”. Repeating an absolute request is easier to handle safely. For the physical system, disable retained/obsolete queued commands, make requests expire or tie them to recent controller state, and deduplicate IDs. The earlier plan gives more detail; these are incremental reliability features after the first round trip works, not prerequisites to understanding the architecture.

**What to communicate to your team, in order.**

Use this as the agenda for a short integration meeting. Write the answers down and name an owner for each shared component.

| Ask or agree | Why it matters | Proposed starting answer |
|---|---|---|
| What exact boards do we physically have? | Uno, classic Nano and Nano ESP32 have different capabilities and electrical details | Inspect the boards; update every diagram consistently |
| One control board for all subsystems, or separate boards? | Determines both the wiring and firmware integration | One shared control board plus one gateway, if consistent with the kit/course |
| Who combines the three control programs? | Separate sketches cannot simply all be flashed to one board and run independently | Name a firmware integrator; agree module interfaces |
| Has UART or I²C already been chosen or implemented? | Avoid duplicating or replacing working team decisions | UART if undecided; keep a suitable working I²C link |
| Which pins, voltages and serial channels are free? | Prevent wiring mistakes and conflicts with sensors/debugging | EEE member and firmware integrator verify together |
| What calibrated values can you provide, and how often? | You need values in usable units, plus validity | Temperature °C, actual stirrer RPM, pH, accepted targets and faults |
| How does my request reach each control loop? | The network callback must lead to a real state change | Shared request parser and per-parameter setpoint update functions |
| Who generates applied/rejected results? | Only the controller knows whether it accepted a request | Board A, forwarded unchanged in meaning by the gateway |
| What happens if Wi-Fi drops or a sensor fails? | The UI and physical behaviour must agree | Network-only loss keeps local control; separate sensor-fault rules agreed by subsystem owners |
| Which broker and network will we use? | Connectivity must work in the actual lab | Verify course broker details and an allowed fallback |
| Where will the dashboard run, and who must access it? | Determines hosting scope | Laptop backend and local browser first; confirm remote-access expectation |
| What does Data Analysis consume and produce? | Your code must connect cleanly to theirs | Shared telemetry schema in; timestamped alert events out |
| When is our first integration test? | Prevent everyone finishing isolated subsystems too late | One fake reading and one confirmed command before full hardware completion |

There are two source inconsistencies to raise without needing to solve them yourself. Your slides alternate Uno/Nano while the equipment list specifies Nano ESP32. Also, the older diagram shows an optical speed sensor, while the recent equipment list specifies a Hall sensor with 70 pulses per revolution and 10:1 gearing. Ask the stirring owner to establish what shaft the pulse count refers to and to give you correctly calculated stirrer RPM.

Here is wording you can adapt and send yourself:

> I am defining the connectivity and UI interface so we can integrate early. Can we confirm the exact control/gateway boards, whether all three loops will run on one board, and who owns combining that firmware? I propose UART between the control board and gateway unless we already have I²C working. I need calibrated temperature, stirrer RPM, pH, accepted targets and fault flags in an agreed message format. The dashboard will send target requests, and the controller should return applied/rejected results with matching command IDs. I suggest a laptop-hosted dashboard connected through the course MQTT broker, subject to checking lab access. Let's agree the pins, message format, broker settings and a date for one simulated reading and one command round trip.

**Build a sequence of small experiments.**

You do not need to implement the entire system to understand it. Each experiment should prove one connection, then give you a known-good component for the next experiment.

1. **Dashboard without hardware:** generate fake temperature/RPM/pH values, display them and save a file. Confirm you can reopen that file. This can start before the team meeting.
2. **MQTT without hardware:** use two test clients or Node-RED publish/subscribe flows on the same broker. Send a JSON message to a private team topic and observe it arriving. This proves topics and broker connectivity.
3. **ESP32 without the reactor:** connect Wi-Fi, publish a fake value, and receive a command that only changes a dummy variable. Confirm it in the dashboard.
4. **UART without actuator outputs:** make Board A send fake telemetry to Board B; send a target back and return an acknowledgement. Record the expected result on both sides.
5. **Connect the whole fake path:** browser → backend → broker → gateway → control board → result back. This proves your distributed application before physical behaviour complicates debugging.
6. **Replace one fake sensor with a real one:** integrate temperature or whichever subsystem is ready first, with its owner present.
7. **Integrate all three and test failures:** malformed request, invalid target, stopped controller messages, Wi-Fi loss and restart. Collect evidence for your report.

Only use public unauthenticated test brokers for harmless synthetic experiments. Before connecting commands to physical actuators, agree how access to command publishing is controlled. A hard-to-guess topic prevents some accidental collisions; it is not authentication.

**Recognise the common failures.**

| Symptom | First things to inspect |
|---|---|
| UART characters are garbled | Matching baud/configuration, voltage levels, correct pins, ground |
| UART receives nothing | TX-to-RX crossing, correct hardware serial instance, sender actually running |
| JSON parsing fails intermittently | Partial lines, overflow, mixed debugging output, inconsistent schema |
| Wi-Fi connects but MQTT does not | Broker hostname/port, network reachability, credentials, TLS configuration |
| MQTT connects but nothing is displayed | Same broker, exact topic, subscription, client IDs, payload fields |
| UI reports success but controller target is unchanged | UI may be treating publish success as controller confirmation |
| Values look live after Board A freezes | Gateway is repeating cached data; freshness must follow controller samples |
| Teammate cannot open your `localhost` link | Their localhost is their computer; shared access needs a reachable app host |
| Logging stops when browser closes | Logging was implemented in the frontend rather than the persistent backend |

You need enough protocol understanding to reason about these failures. You do not need to implement UART bit timing, MQTT packet encoding or a broker from scratch. The productive work is defining the contracts, using libraries correctly, testing each boundary, and making the UI accurately reflect the physical controller's state.

The next concrete action is to confirm the physical boards and firmware integration owner, while you independently build a dashboard with simulated data. That allows the hardware and application work to progress together.

The supplied materials most relevant to this explanation are `Connectivity.pdf` (wired links, MQTT and network constraints), `3_Bioreactor Design Specification v4_notes.pdf` (requirements and overall structure), `List of bioreactor testbed elements.txt` (current equipment), `eduroam.ino` (initial Wi-Fi example), and pages 3–8 of `Engineering Challenges Presentation.pdf` (your team's proposed integration). The external documentation links above support the practical API/setup details. No hardware or broker connection was tested while preparing this guide.
