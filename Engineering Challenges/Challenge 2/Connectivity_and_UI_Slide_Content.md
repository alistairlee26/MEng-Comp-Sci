**Slide content for CSEEE-21: connectivity and user interface**

These are proposed design choices and targets, not completed implementation results. The existing deck is eight pages, with an empty connectivity/UI slide at page 7. Put this material after the overall system diagram and before Data Analysis. Aim for two slides if your team's presentation allocation permits; no presentation length was specified in the supplied files.

**Core slide 1 — Connectivity: from the reactor to the operator**

Use the existing simple white background, dark text and rounded boxes. Give most of the space to this diagram:

```text
CONTROL BOARD  <── UART ──>  ESP32 GATEWAY  <── Wi-Fi / MQTT ──>  MQTT BROKER
  local loops                                                       ↕ MQTT
                                                             DASHBOARD APPLICATION
                                                               ↕          ↓
                                                            Browser   Persistent log
```

Label the upper data path **Measurements, accepted targets and faults →** and the return path **← Target requests and controller confirmations**. Show the anomaly detector as another subscriber if space permits.

Paste-ready bullets:

- **UART:** carries measurements and target commands between the control board and gateway.
- **Wi-Fi + MQTT:** connects the gateway to the dashboard and data-analysis subsystem.
- **Confirmed commands:** the interface shows a change as applied only after the controller acknowledges it.
- **Local control:** feedback loops continue during a network outage; the interface flags stale data.

Small footer: **Proposed stack: PicoMQTT client • Node-RED + FlowFuse Dashboard • CSV experiment logs**.

Speaker notes, approximately 45–60 seconds:

“Our subsystem connects the physical reactor to its operator. The control board runs the temperature, stirring and pH feedback loops. It sends measured values and its accepted targets to an ESP32 gateway over UART. The gateway publishes those readings through an MQTT broker, so the dashboard and the data-analysis subsystem can both receive them. Target changes travel in the reverse direction. We will show a change as pending until the controller confirms it, which avoids presenting a message that was merely sent as a successful control action. If connectivity is lost, the local controller follows its agreed operating policy and the dashboard marks its readings stale.”

Justification to give if asked: UART is a simple fit for the proposed pair of boards; MQTT supports multiple consumers and matches the course examples; Node-RED keeps effort available for integration and testing. Confirm the exact board names before putting them on the final diagram.

**Core slide 2 — User interface: monitor, adjust and verify**

Insert `Connectivity_UI_Wireframe.svg` as the principal visual. It is a static design sketch, and all readings are illustrative. Crop the subtitle only if you keep an explicit “Proposed interface — example values” label elsewhere.

Paste-ready bullets alongside or below it:

- **Monitor:** live temperature, RPM and pH, confirmed targets, trend plots and alerts.
- **Adjust:** validated inputs — 25–35 °C, 500–1500 RPM and pH 3–7.
- **Record:** timestamped readings, accepted targets, command results and faults; export CSV.
- **Verify:** target 1 Hz reporting, command confirmation within 2 s for 95% of trials, stale warning within 5 s.

Small footer: **Communication timings are proposed targets; temperature and RPM tolerances come from the brief.**

Speaker notes, approximately 45–60 seconds:

“The screen will show the measured value separately from the target that the controller has accepted. The operator edits a requested target and presses Apply, with range checks both here and on the controller. Time plots will show the response to target changes, while an alert panel will display faults and the analysis team's anomaly warnings. Logging will continue while the application is running even if the browser is closed, and exported records will support our final report. We will test normal communication, invalid inputs, frozen readings and disconnect recovery. The timing figures shown are our proposed communication targets; they are separate from the time needed for the physical reactor to settle.”

**Optional backup slide — Integration plan and proof of performance**

Use a short timeline:

- **Week 5 / reading week:** agree board interfaces; demonstrate simulated readings and command round trip.
- **Week 6–7:** connect real boards; integrate all three subsystems and logging.
- **Week 8:** test loss of connection, command rejection and alerts.
- **Week 9:** measure performance and rehearse the complete demonstration.

Alongside, show three tests:

| Test | Pass evidence |
|---|---|
| Change a valid target | Matching controller confirmation and updated accepted target |
| Submit an invalid target | Visible rejection and unchanged controller state |
| Disconnect the controller link | Stale warning, disabled commands and an explicit log gap |

Keep the fuller acceptance matrix in the implementation plan for questions.

**If you have only one slide**

Retain the title “Connectivity and User Interface”. Put the simplified communication chain in the top third, a reduced three-panel wireframe in the middle, and these three bullets at the bottom:

- Live readings and trend plots for temperature, stirring speed and pH.
- Validated target changes with confirmation from the controller.
- Timestamped logs, anomaly alerts and visible connection-loss status.

Add a small target strip: **1 Hz reporting | ≤2 s confirmation for 95% of trials | stale after 5 s**. Explain that these are proposed targets. Speak the technology justification and test plan rather than filling the slide with prose.

**Questions to be ready to answer**

- **Where is the server?** The broker is a reachable messaging service; initially the dashboard application and logs run on the operator laptop. Confirm the course broker's access details in the lab. The ESP32 and laptop both connect to it.
- **What if Wi-Fi fails?** The controller retains local responsibility. The UI marks readings stale and stops accepting new requests; logs show a gap. The precise local fault policy is agreed with the controls team.
- **How do you know a target changed?** A matching command ID returns from the controller with its accepted value; telemetry also reports the active target.
- **How will you demonstrate success?** Show a real measurement, one confirmed target change, a rejected invalid input, a disconnect/reconnect and an exported run.
- **Does an MQTT broker store the experiment?** We will implement a separate persistent logger; message routing is not sufficient for historical analysis.
- **How does this support Data Analysis?** The detector subscribes to the same defined telemetry, and its alerts are displayed and logged by the dashboard.
- **Why two boards if the Nano ESP32 has Wi-Fi?** This follows the teaching architecture and separates network work from local control. We will verify the actual kit and team topology before implementation.

**Useful edits elsewhere in the team deck**

- Make Uno/Nano/Nano ESP32 naming consistent across pages 3–6.
- Update the stirrer sensor in page 6 after checking the current kit; the equipment list differs from the older diagram.
- Change “Comments from server” on page 3 to “Setpoint commands”.
- Split “Cloud Server / User Interface” into the broker and application/logging functions, or explain the grouping explicitly.
- On the Data Analysis slide, show a telemetry input and an alert output so the interface between your work and theirs is visible.

Use the source page references in `Connectivity_and_UI_Plan.md` in speaker notes or a references slide. Do not present mock data, proposed targets or diagrams as measured results.
