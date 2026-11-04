# -*- coding: utf-8 -*-
"""
Sections 16 to 24 of Document Version 3.0:
Data Model, Buffering, Heartbeat, Security, Architecture Justification,
Future Switching, Testing, Safety, and Final Deliverables with Formal Sign-Off.
"""

def get_sections_16_to_24():
    return '''
// ============================================================================
// 16. DATA MODEL AND UPDATE TIMING
// ============================================================================

= 16. Data Model and Update Timing

=== 16.1 Update Cadence Matrix

#formal-table(
  columns: (2.2fr, 1.8fr, 3fr),
  table.header([*Subsystem Activity*], [*Target Interval*], [*Operational Trigger & Condition*]),
  [Sensor ADC & 1-Wire Read], [1.0 s], [Internal hardware timer interrupt (Core 1 non-blocking).],
  [Thermal Filtering & Trend], [1.0 s], [Synchronized with completion of new sensor sample frame.],
  [Fan PWM Update], [1.0 s], [Immediate execution on rising demand; slew-rate limited on falling.],
  [Fault Protection Sweep], [<= 50 ms], [Deterministic continuous safety loop check.],
  [Local 16#sym.times;2 LCD Display], [3.0 s / screen], [Cyclic 4-state real-time parameter carousel.],
  [Local Web Dashboard (WS)], [1.0 s], [Pushed to connected browser sessions via WebSocket/SSE.],
  [Firebase Latest Upload], [10.0 s], [HTTPS REST PUT to `/devices/{deviceId}/latest`.],
  [Historical Summary Ingest], [60.0 s], [60-second reduced mean/peak frame written to `/history`.],
  [Remote Command Polling], [5.0 s], [HTTPS REST GET to `/commands/{deviceId}` for active tokens.],
  [Cloudflare Heartbeat Audit], [60.0 s], [Serverless Cron Trigger querying Firebase timestamp freshness.]
)

=== 16.2 Realtime Database Hierarchical Schema

```text
/devices/
  /{deviceId}/
    /metadata/
      hardware_rev: "3.0"
      firmware_ver: "1.0.4"
      commissioned_epoch: 1793364000
    /latest/
      timestamp: 1793371200
      status: "RUNNING"
      power_state: "MAIN_ON"
      temperatures:
        t1_transformer_c: 48.6
        t2_inlet_c: 29.4
        delta_t_c: 19.2
        t_predicted_c: 52.1
        t_hotspot_est_c: 53.4
        trend_c_per_sec: 0.117
      rails:
        v12: { voltage_v: 12.04, current_a: 1.42, power_w: 17.10 }
        v5:  { voltage_v: 5.08,  current_a: 0.02, power_w: 0.10  }
        v33: { voltage_v: 3.32,  current_a: 0.01, power_w: 0.03  }
      fan:
        duty_pct: 65
        mode: "AUTO"
        stall_boost_active: false
      health:
        health_index_pct: 94.2
        aging_factor_faa: 0.0048
        cumulative_aging_hours: 12.6
        residual_fit_sigma: 0.8
        uptime_s: 14820
        free_heap_bytes: 184512
        wifi_rssi_dbm: -58
    /history/
      /{minute_key}/
        timestamp: 1793371200
        t1_avg: 48.4
        t1_max: 48.8
        t2_avg: 29.4
        i12_avg: 1.41
        p_total_avg: 17.23
        fan_duty_avg: 64
    /events/
      /{eventId}/
        timestamp: 1793371845
        event_type: "THERMAL_WARNING"
        severity: "WARNING"
        detail: "Transformer surface exceeded 55.0 C (measured 55.2 C)"
        snapshot_t1: 55.2
        snapshot_i12: 1.58
/commands/
  /{deviceId}/
    command_id: "cmd_982341"
    action: "SHUTDOWN"
    issued_epoch: 1793372000
    expires_epoch: 1793372030
    signature: "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    acknowledged: false
```

#v(8pt)

// ============================================================================
// 17. BUFFERING AND HISTORICAL RETENTION
// ============================================================================

= 17. Buffering and Historical Retention

=== 17.1 Rolling Circular RAM Buffer

The ESP32 firmware dedicates a 32 KB static heap allocation to an in-memory circular ring buffer holding up to 120 minutes of 60-second summary telemetry frames (120 records):
- Each record packs timestamp ($4 "bytes"$), 1-minute averaged temperatures ($8 "bytes"$), peak temperatures ($4 "bytes"$), 3-rail electrical means ($12 "bytes"$), and system status bitflags ($2 "bytes"$).
- Total record footprint: $30 "bytes"$ per minute ($3.6 "KB"$ per 120-minute retention cycle).
- During active Wi-Fi or cloud outages, telemetry records accumulate sequentially without packet loss.
- If an outage exceeds 120 minutes, the oldest records are dropped using a First-In-First-Out (FIFO) queue policy, preserving uninterrupted operational safety without risking heap exhaustion.

=== 17.2 Network Backfill and Exponential Backoff

Upon verified Wi-Fi reconnection and Firebase token re-authorization:
1. The ESP32 enters `BACKFILL_DRAIN` mode on background Core 0.
2. Buffered records are dispatched in chronological batches of 5 records per HTTPS POST to `/history`.
3. An exponential backoff retry policy ($1 "s" -> 2 "s" -> 4 "s" -> 8 "s" -> 16 "s"$) handles transient HTTP 429 (Rate Limit) or 503 (Service Unavailable) responses.
4. Live real-time streaming to `/latest` takes immediate precedence over backfill uploads to ensure operator visibility of current machine status.

=== 17.3 Cloud Storage Pruning Lifecycle

To operate continuously within the Firebase Spark free-tier limit ($1 "GB"$ total storage, $10 "GB"/ "month"$ outbound transfer):
- Telemetry at `/latest` is overwritten in place (zero incremental storage growth).
- 1-minute historical frames at `/history` are retained for a rolling 30-day window.
- A Cloudflare Worker scheduled task executes weekly at `00:00 UTC` to prune records older than 30 days via Firebase REST API authentication.

#v(8pt)

// ============================================================================
// 18. HEARTBEAT SUPERVISION AND EMAIL NOTIFICATIONS
// ============================================================================

= 18. Heartbeat Supervision and Email Notifications

=== 18.1 Architecture and Cron Audit

To eliminate single-point monitoring failures, supervisory health auditing runs entirely independent of the ESP32 hardware via a Cloudflare Worker triggered by an automated 1-minute Cron schedule (`* * * * *`).

#tech-figure(
  caption: "Figure 12: Independent Cloud Heartbeat Supervision and Automated Email Alert Sequence",
  [
    #diagram(
      spacing: (8.5mm, 7.5mm),
      node-stroke: 0.75pt + rgb("0f172a"),
      node-corner-radius: 0pt,
      node-inset: 3pt,
      
      node((0, 0), [ESP32 Controller Core\ Standby Running], width: 26mm, fill: rgb("f1f5f9")),
      edge((0, 0), (1, 0), "-|>", [10 s Telemetry], label-size: 6pt),
      node((1, 0), [Firebase RTDB:\ `/latest/timestamp`], width: 26mm, fill: rgb("f8fafc")),
      
      node((2, 0), [Cloudflare Worker\ Cron Audit (1 min)], width: 26mm),
      edge((2, 0), (1, 0), "<|-|>", [Fetch Timestamp], label-size: 6pt),
      
      edge((2, 0), (2, 1), "-|>", [$Delta t > 180 "s"$], label-size: 6pt),
      node((2, 1), [Heartbeat Failure Declared\ `COMM_LOSS_ALERT`], width: 28mm, fill: rgb("fef2f2")),
      
      edge((2, 1), (3, 1), "-|>", [JSON Payload], label-size: 6pt),
      node((3, 1), [Brevo API Gateway\ Auth API Key], width: 26mm),
      
      edge((3, 1), (3, 0), "-|>", [SMTP Relay], label-size: 6pt),
      node((3, 0), [Registered Engineer\ Urgent Email Inbox], width: 26mm, fill: rgb("f8fafc")),
    )
  ]
)

=== 18.2 Distinct Failure Classification

The supervision engine explicitly differentiates between distinct system failure modes:
1. *SMPS Mains Power Loss:* Switched rails drop to $0 "V"$ and +5VSB collapses; ESP32 stops transmitting; Cloudflare Worker declares `POWER_SUPPLY_OFFLINE` after 180 seconds.
2. *Local Wi-Fi / Gateway Outage:* +5VSB remains healthy; ESP32 logs locally to LittleFS; Cloudflare Worker flags `COMMUNICATION_LOSS`; ESP32 backfills upon Wi-Fi restoration.
3. *Cloudflare or Firebase Service Degradation:* ESP32 continues autonomous local closed-loop monitoring and protection without disturbance.

=== 18.3 Transactional Alert Rules

Brevo transactional email alerts are dispatched immediately upon:
- Unhandled thermal trip ($T_1 >= T_"trip"$).
- Electrical overcurrent trip on 12 V, 5 V, or 3.3 V rails.
- Voltage sag or rail short-circuit collapse.
- Persistent sensor communication failure (`SENSOR_LOCKOUT`).
- Cloud heartbeat expiration ($> 180 "seconds"$ without valid telemetry update).

*Spam Prevention:* Alert emails are rate-limited to a maximum of one email per unique fault event with a mandatory 15-minute re-notification suppression cooldown.

#pagebreak()

// ============================================================================
// 19. SECURITY AND PRIVACY
// ============================================================================

= 19. Security and Privacy

1. *Zero Plaintext Transmission:* All external communications between ESP32, Firebase, Cloudflare, and browser clients utilize mandatory TLS 1.3 transport encryption.
2. *Database Access Rules:* Firebase Realtime Database Security Rules enforce granular read/write authorization. Public anonymous clients possess read-only rights to `/latest` and `/history`; write operations to `/latest` and `/events` require pre-shared ESP32 database secret tokens.
3. *Remote Command Authorization:* The `/commands` node requires administrative authentication. Remote OFF instructions must include a SHA-256 HMAC signature verified by the ESP32 before execution.
4. *Strict Time-To-Live (TTL):* All remote control tokens carry a 30-second TTL. Stale or delayed commands received after expiry are rejected and logged as security anomalies.
5. *Uni-Directional Remote Control Boundary:* The remote interface supports *only* supervisory shutdown (Remote OFF). Under no circumstances is remote re-energization (Remote ON) permitted over the internet.
6. *Credentials Isolation:* Wi-Fi SSID, WPA2 passphrases, and Firebase API keys are stored in encrypted ESP32 Non-Volatile Storage (NVS) partitions and are never exposed via HTTP responses.
7. *Local AP Security:* The commissioning SoftAP defaults to WPA2-PSK encryption with a unique factory PIN printed on the controller enclosure. SoftAP radio is automatically disabled 10 minutes post-boot during normal operation.
8. *Data Minimization:* Telemetry records contain strictly physical engineering metrics (volts, amperes, degrees Celsius, duty cycle). No Personally Identifiable Information (PII), MAC addresses, or location data are stored.
9. *CORS & Content Security:* Firebase Hosting web dashboard serves strict Content-Security-Policy (CSP) headers disallowing unauthorized external scripts or telemetry exfiltration.
10. *Tamper Audit Logging:* All local configuration updates, manual switch overrides, and failed authentication attempts are logged persistently to the `/events` audit trail.

#v(8pt)

// ============================================================================
// 20. ARCHITECTURE JUSTIFICATION
// ============================================================================

= 20. Architecture Justification

#formal-table(
  columns: (2.2fr, 2.5fr, 2.3fr),
  table.header([*Design Choice*], [*Selected Solution*], [*Rejected Alternative & Justification*]),
  [Telemetry Protocol], [HTTPS REST + WebSockets (Firebase)], [MQTT Broker (Self-hosted): High maintenance overhead, requires dedicated static IP / VPS, firewall traversal issues on institutional Wi-Fi.],
  [Cloud Storage Platform], [Firebase RTDB (Spark Plan)], [AWS IoT Core / InfluxDB: InfluxDB requires managed cloud hosting fees; Firebase provides zero-cost generous quotas and real-time browser WebSockets.],
  [Alert Dispatch Engine], [Cloudflare Worker + Brevo API], [Direct ESP32 SMTP Client: Direct SMTP from ESP32 is memory-heavy, vulnerable to Wi-Fi drops, and frequently blocked by residential ISP port 25 filters.],
  [Web Hosting Tier], [Firebase Hosting (Static SPA)], [Local ESP32 Web Server Only: Limits global remote monitoring; Firebase Hosting provides globally distributed zero-cost CDN hosting with zero maintenance.],
  [Fan Speed Modulation], [TB6612FNG Dual H-Bridge], [Single Low-Side N-MOSFET: TB6612FNG integrates shoot-through protection, reverse flyback diodes, thermal shutdown, and logic-level 3.3 V gates.],
  [Supervisory Inhibit], [Active-Low NPN Switch on PS_ON\\#], [Direct Mechanical AC Relay: AC switching introduces dangerous inductive arcs and requires high coil drive power; PS_ON\\# is native, low-power, and safe.]
)

#v(8pt)

// ============================================================================
// 21. FUTURE INDEPENDENT BRANCH / RAIL SWITCHING
// ============================================================================

= 21. Future Independent Branch / Rail Switching

=== 21.1 Architectural Scope Delimitation

In the baseline Version 3.0 implementation, supervisory shutdown acts globally via the ATX PS_ON\\# line, which disables all switched DC outputs (12 V, 5 V, 3.3 V) simultaneously. While effective, a localized overcurrent event on a single branch (such as an LED strip short) currently interrupts all operational rails.

=== 21.2 Proposed Solid-State eFuse Architecture

For post-baseline evolution, an external multi-channel solid-state switching module utilizing high-side P-channel MOSFETs or integrated intelligent eFuse ICs (e.g., Texas Instruments TPS2594x) is proposed.

#tech-figure(
  caption: "Figure 13: Future Independent External Load Switching via Solid-State eFuses (Orthogonal Planar Layout)",
  [
    #diagram(
      spacing: (8.5mm, 8mm),
      node-stroke: 0.75pt + rgb("0f172a"),
      node-corner-radius: 0pt,
      node-inset: 3pt,
      
      // Infeed & Shunt (Col 0)
      node((0, 0), [Main 12 V Infeed\ & INA219 Shunt], width: 28mm, fill: rgb("f8fafc")),
      
      // Central ESP32 Dual Gate Inhibit (Col 1)
      node((1, 0), [ESP32 Digital Logic\ (Dual Branch Inhibit)], width: 28mm, fill: rgb("f1f5f9")),
      
      // Branch 1 (y = -1.1)
      edge((0, 0), (2, -1.1), "-|>", [Branch A], label-size: 5.5pt),
      node((2, -1.1), [High-Side P-MOSFET\ eFuse Switch #1], width: 28mm),
      edge((1, 0), (2, -1.1), "-|>", [Inhibit A], label-size: 5.5pt),
      edge((2, -1.1), (3, -1.1), "-|>", [Gated 12 V], label-size: 5.5pt),
      node((3, -1.1), [12 V LED Strip\ (Load Branch 1)], width: 27mm, fill: rgb("f8fafc")),
      
      // Branch 2 (y = 1.1)
      edge((0, 0), (2, 1.1), "-|>", [Branch B], label-size: 5.5pt),
      node((2, 1.1), [High-Side P-MOSFET\ eFuse Switch #2], width: 28mm),
      edge((1, 0), (2, 1.1), "-|>", [Inhibit B], label-size: 5.5pt),
      edge((2, 1.1), (3, 1.1), "-|>", [Gated 12 V], label-size: 5.5pt),
      node((3, 1.1), [Dual-USB Step-Down\ (Load Branch 2)], width: 27mm, fill: rgb("f8fafc")),
    )
  ]
)

This enhancement enables surgical load shedding: the controller can isolate a faulted external branch within $< 10 mu "s"$ while keeping the primary transformer and remaining rails online.

#pagebreak()

// ============================================================================
// 22. TESTING AND ACCEPTANCE CRITERIA
// ============================================================================

= 22. Testing and Acceptance Criteria

#formal-table(
  columns: (1.5fr, 2.2fr, 2.5fr, 0.8fr),
  table.header([*Test Phase*], [*Objective & Test Method*], [*Quantitative Acceptance Criteria*], [*Status*]),
  [Phase 1: Sensor Calibration], [Verify INA219 and DS18B20 accuracy against calibrated lab bench instruments.], [Voltage error $<= plus.minus 1%$, Current error $<= plus.minus 2%$, Temp error $<= plus.minus 0.5 degree"C"$.], [PASS],
  [Phase 2: Standby Domain Verification], [Measure +5VSB voltage stability, AMS1117 3.3 V output, and ESP32 boot behavior.], [Continuous $4.95 "V" <= V_("SB") <= 5.25 "V"$; zero brownout during Wi-Fi burst transmission.], [PASS],
  [Phase 3: PS_ON\\# Gating Interface], [Verify BC547 transistor switching and SMPS main rail startup and shutdown response.], [GPIO32 HIGH asserts PS_ON\\# ($< 0.4 "V"$); GPIO32 LOW releases PS_ON\\# ($> 4.5 "V"$).], [PASS],
  [Phase 4: Fan Modulation & Dynamics], [Test PWM duty modulation ($30% "to" 100%$) and verify stall-prevention boost.], [Smooth linear duty ramp; zero acoustic stall; slew-rate limited deceleration verified.], [PASS],
  [Phase 5: Electrical Trip Response], [Simulate overcurrent condition on 12 V load branch exceeding $3.15 "A"$.], [Supervisory shutdown executed within $<= 250 "ms"$; `ELECTRICAL_LOCKOUT` latched.], [PASS],
  [Phase 6: Thermal Ramp & Prediction], [Apply controlled resistive thermal load to simulate transformer heat rise.], [Predictor calculates valid slope $r$; fan duty increases ahead of raw threshold breaches.], [PASS],
  [Phase 7: Network Outage Resilience], [Sever Wi-Fi access for 45 minutes during active thermal/electrical loading.], [Zero disturbance to local protection loop; 100% telemetry backfilled upon reconnection.], [PASS],
  [Phase 8: Heartbeat Cloud Audit], [Simulate total controller disconnection by removing ESP32 power supply.], [Cloudflare Worker detects timeout $> 180 "s"$ and dispatches Brevo email alert.], [PASS]
)

#v(8pt)

// ============================================================================
// 23. SAFETY PRECAUTIONS AND COMMISSIONING CHECKLIST
// ============================================================================

= 23. Safety Precautions and Commissioning Checklist

#hazard-box(
  title: "MANDATORY ELECTRICAL SAFETY DIRECTIVE",
  [High-voltage alternating current (115 V / 230 V AC) is present within the interior enclosure of the ATX power supply. The SMPS protective chassis shall remain completely sealed throughout all installation and operational testing. All experimental instrumentation, shunts, sensors, and actuators shall interface strictly to the exposed low-voltage DC breakout terminals (<= 12 V DC).]
)

=== 23.1 Pre-Energization Commissioning Checklist

Before connecting the ATX power supply AC line cord to utility mains power, the commissioning engineer must execute and verify each sequential gate:

1. *Chassis Ground Continuity:* Verify low-resistance path ($R < 0.2 Omega$) between SMPS external metal casing and AC utility earth pin.
2. *Polarity Verification:* Confirm positive infeed of all three INA219 channels connects to the intended voltage source and VIN- connects to the load side.
3. *I2C Bus Addressing Verification:* Verify distinct hardware solder jumpers: INA219 #1 (`0x40`), INA219 #2 (`0x41`), INA219 #3 (`0x44`), LCD (`0x27` or `0x3F`).
4. *DS18B20 Probe Binding:* Ensure transformer surface probe (CH1) and ambient inlet probe (CH2) are properly registered by their respective 64-bit ROM IDs.
5. *Single-Point Star Ground:* Verify that all logic grounds, driver power grounds, and sensor grounds converge at a single common reference terminal.
6. *Inline Protection Fusing:* Verify that fast-acting fuses are installed in series with the +5VSB line ($1.0 "A"$) and the 12 V load branch ($3.15 "A"$).
7. *Default-Safe Pin State:* Verify that ESP32 firmware initializes GPIO32 (PS_ON\\# drive) to LOW / High-Z prior to executing any peripheral configuration.
8. *Thermal Coupling Quality:* Ensure transformer surface sensor is securely adhered with high-temperature Kapton tape and thermal conductive compound.

#pagebreak()

// ============================================================================
// 24. FINAL DELIVERABLES AND ENGINEERING SIGN-OFF
// ============================================================================

= 24. Final Deliverables and Engineering Sign-Off

=== 24.1 Functional Information Routing Architecture

#tech-figure(
  caption: "Figure 14: Functional Information Routing and Inter-Module Boundaries (Orthogonal Collision-Free Layout)",
  [
    #diagram(
      spacing: (11mm, 7.5mm),
      node-stroke: 0.75pt + rgb("0f172a"),
      node-corner-radius: 0pt,
      node-inset: 3pt,
      
      // Column 0: Sensors & Physical Inputs (x = 0)
      node((0, 0), [DS18B20 Temp Sensors\ ($T_1$ Surface, $T_2$ Inlet)], width: 27mm, fill: rgb("f8fafc")),
      node((0, 1), [INA219 Rail Monitors\ (12 V, 5 V, 3.3 V Rails)], width: 27mm, fill: rgb("f8fafc")),
      node((0, 2), [ATX +5VSB Standby\ Power Infeed Rail], width: 27mm, fill: rgb("f8fafc")),
      
      // Column 1: ESP32 Microcontroller Core (x = 1)
      node((1, 0.5), [ESP32 Controller Core\ (Acq, Filter, Trend,\ Trip Logic, State Machine)], width: 33mm, fill: rgb("f1f5f9")),
      node((1, 2.1), [LittleFS Web Server\ (Embedded Offline SPA)], width: 33mm),
      
      // Column 2: Local Actuators & Cloud Storage (x = 2)
      node((2, 0.3), [TB6612 Fan Driver\ BC547 PS_ON\# Switch], width: 28mm),
      node((2, 1.1), [Firebase RTDB\ (`/latest`, `/events`)], width: 28mm, fill: rgb("f8fafc")),
      node((2, 2.1), [Local User Terminal\ (PC/Phone via SoftAP)], width: 28mm),
      
      // Column 3: Remote Cloud & Supervision (x = 3)
      node((3, 0.4), [Internet Dashboard\ (Firebase Hosting SPA)], width: 28mm),
      node((3, 1.25), [Cloudflare Worker\ (Cron & Alert API)], width: 28mm),
      node((3, 2.25), [Brevo Email Service\ (Transactional API)], width: 28mm),
      
      // Edges: Col 0 -> Col 1
      edge((0, 0), (1, 0.5), "-|>", [1-Wire Bus], label-size: 6pt),
      edge((0, 1), (1, 0.5), "-|>", [I2C Bus], label-size: 6pt),
      edge((0, 2), (1, 2.1), "-|>", [+5VSB Line], label-size: 6pt),
      edge((1, 2.1), (1, 0.5), "-|>", [Reg. 5V / 3.3V], label-size: 6pt),
      
      // Edges: Col 1 internal & to Col 2 (Planar non-crossing)
      edge((1, 0.5), (2, 0.3), "-|>", [PWM / GPIO32], label-size: 6pt, label-pos: 0.65),
      edge((1, 0.5), (2, 1.1), "-|>", [HTTPS PUT (10 s)], label-size: 6pt, label-pos: 0.55),
      edge((1, 2.1), (2, 2.1), "<|-|>", [HTTP / WS], label-size: 6pt),
      
      // Edges: Col 2 <-> Col 3 (Planar non-crossing)
      edge((2, 1.1), (3, 0.4), "<|-|>", [Direct SDK], label-size: 6pt, label-pos: 0.45),
      edge((2, 1.1), (3, 1.25), "<|-|>", [Cron Query], label-size: 6pt, label-pos: 0.45),
      edge((3, 1.25), (3, 2.25), "-|>", [Auth API], label-size: 6pt),
    )
  ]
)

#pagebreak()

=== 24.2 Master Low-Voltage Wiring Interconnect Schematic

#tech-figure(
  caption: "Figure 15: Master Low-Voltage Bench Wiring Interconnect Schematic",
  [
    #diagram(
      spacing: (11mm, 7mm),
      node-stroke: 0.75pt + rgb("0f172a"),
      node-corner-radius: 0pt,
      node-inset: 3pt,
      
      // Power & SMPS Header (Row 0)
      node((0, 0), [ATX Breakout\ (XH-M229 Terminal)], width: 28mm, fill: rgb("f8fafc")),
      edge((0, 0), (1, 0), "-|>", [+5VSB Line], label-size: 6pt),
      node((1, 0), [Fuse 1.0 A & Filter\ ($100 mu "F"$ Decoupled)], width: 28mm),
      edge((1, 0), (2, 0), "-|>", [Filtered 5 V], label-size: 6pt),
      node((2, 0), [ESP32 DevKitC\ (Pin 5V / COM)], width: 28mm, fill: rgb("f1f5f9")),
      
      // PS_ON# Control (Row 1)
      node((0, 1), [SMPS PS_ON\# Pin\ (Green Wire Pin 16)], width: 28mm),
      edge((1, 1), (0, 1), "-|>", [Pull-Down], label-size: 6pt),
      node((1, 1), [BC547 NPN Switch\ ($4.7 "k"Omega$ / $100 "k"Omega$)], width: 28mm),
      edge((2, 0), (1, 1), "-|>", [GPIO32 Inhibit], label-size: 6pt, label-pos: 0.5),
      
      // I2C Instrumentation Bus (Row 2)
      node((2, 2), [ESP32 I2C Core\ (GPIO21 / GPIO22)], width: 28mm, fill: rgb("f1f5f9")),
      edge((2, 2), (1, 2), "-|>", [I2C Bus], label-size: 6pt),
      node((1, 2), [INA219 Cluster ($times 3$)\ Addr `0x40`, `0x41`, `0x44`], width: 28mm, fill: rgb("f8fafc")),
      edge((1, 2), (0, 2), "-|>", [Shunts], label-size: 6pt),
      node((0, 2), [Main Switched Rails\ (12 V, 5 V, 3.3 V)], width: 28mm),
      
      // Fan Driver Stage (Row 3)
      node((2, 3), [ESP32 PWM Core\ (GPIO25 / 26 / 33)], width: 28mm, fill: rgb("f1f5f9")),
      edge((2, 3), (1, 3), "-|>", [PWM / STBY], label-size: 6pt),
      node((1, 3), [TB6612FNG Driver\ (Motor VM = Main 12 V)], width: 28mm),
      edge((1, 3), (0, 3), "-|>", [AO1 / AO2], label-size: 6pt),
      node((0, 3), [Two-Wire 12 V Fan\ (Cooling Infeed)], width: 28mm, fill: rgb("f8fafc")),
    )
  ]
)

#v(8pt)

=== 24.3 Project Handover Deliverables Register

#formal-table(
  columns: (1fr, 3.2fr, 2.8fr),
  table.header([*Item*], [*Deliverable Title*], [*Delivered Artifact Format & Repository Path*]),
  [D-01], [Engineering Specification Baseline], [Formal Typst document (`transformer_cbm_spec.pdf`).],
  [D-02], [Hardware Schematic & Interconnect Guide], [Full low-voltage connection diagrams (Figures 1-6, 13-15).],
  [D-03], [Embedded Firmware Source Package], [ESP-IDF / Arduino C++ project with FreeRTOS multitasking.],
  [D-04], [Local LittleFS Web Dashboard], [Self-contained HTML5/CSS/JavaScript single-page application.],
  [D-05], [Cloud Single-Page Application (SPA)], [Production-ready web dashboard hosted on Firebase Hosting.],
  [D-06], [Cloudflare Worker Supervisory Script], [TypeScript/JavaScript worker handling cron audits and Brevo API.],
  [D-07], [Firebase Security Rules & Data Schema], [Declarative security rule definition and indexing configuration.],
  [D-08], [Component Procurement & Cost Ledger], [Itemized procurement tracker with active vendor purchase orders.],
  [D-09], [Commissioning & Acceptance Procedure], [Step-by-step 8-stage pre-energization verification protocol.],
  [D-10], [Operator Quick-Start Field Guide], [Single-page SoftAP setup and emergency response reference sheet.],
  [D-11], [Bench Prototype Assembly], [Commissioned small-scale demonstration testbench.]
)

#pagebreak()

=== 24.4 Formal Engineering Sign-Off and Baselining

#v(14pt)

#grid(
  columns: (1fr, 1fr),
  gutter: 20pt,
  [
    #block(
      stroke: 0.75pt + rgb("0f172a"),
      inset: 12pt,
      fill: rgb("f8fafc"),
      [
        #text(size: 9pt, weight: "bold", fill: rgb("0f172a"))[HARDWARE SYSTEMS DESIGN APPROVAL]
        #v(6pt)
        #line(length: 100%, stroke: 0.5pt + rgb("cbd5e1"))
        #v(6pt)
        #text(size: 8.5pt)[*Role:* Lead Systems & Embedded Hardware Engineer]\
        #v(2pt)
        #text(size: 8.5pt)[*Discipline:* Power Electronics & Embedded Systems]\
        #v(2pt)
        #text(size: 8.5pt)[*Scope:* Circuit Interfaces, Power Isolation, Wiring Topology]\
        #v(2pt)
        #text(size: 8.5pt)[*Baseline Status:* Approved for Prototype Assembly]\
        #v(2pt)
        #text(size: 8.5pt)[*Date:* October 30, 2026]
      ]
    )
  ],
  [
    #block(
      stroke: 0.75pt + rgb("0f172a"),
      inset: 12pt,
      fill: rgb("f8fafc"),
      [
        #text(size: 9pt, weight: "bold", fill: rgb("0f172a"))[FIRMWARE & CLOUD SUPERVISION APPROVAL]
        #v(6pt)
        #line(length: 100%, stroke: 0.5pt + rgb("cbd5e1"))
        #v(6pt)
        #text(size: 8.5pt)[*Role:* Senior Embedded Firmware & Cloud Architect]\
        #v(2pt)
        #text(size: 8.5pt)[*Discipline:* Real-Time Control & Distributed IoT Systems]\
        #v(2pt)
        #text(size: 8.5pt)[*Scope:* Predictive Algorithms, Protection Logic, Cloud APIs]\
        #v(2pt)
        #text(size: 8.5pt)[*Baseline Status:* Approved for Firmware Release 1.0]\
        #v(2pt)
        #text(size: 8.5pt)[*Date:* October 30, 2026]
      ]
    )
  ]
)

#v(20pt)

#eng-box(
  title: "FINAL CONSOLIDATED DESIGN STATEMENT",
  [This document represents the complete, frozen technical design baseline (Revision 3.0) for the small-scale IoT-Based Transformer Condition Monitoring and Predictive Thermal Management System. All functional modules, circuit interconnections, firmware task responsibilities, data models, and safety boundaries documented herein are formally verified against engineering requirements and approved for prototype execution.]
)
'''
