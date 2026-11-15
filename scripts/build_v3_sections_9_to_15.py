# -*- coding: utf-8 -*-
"""
Sections 9 to 15 of Document Version 3.0:
Firmware Architecture, Predictive Thermal Algorithm, Protection Logic,
Recovery & Power-State Control, Maintenance Advisories, Local Dashboard,
and Internet Deployment.
"""

def get_sections_9_to_15():
    return '''
// ============================================================================
// 9. FIRMWARE ARCHITECTURE
// ============================================================================

= 9. Firmware Architecture

#formal-table(
  columns: (2fr, 5fr),
  table.header([*Firmware Subsystem*], [*Functional Architectural Responsibility*]),
  [Sensor Manager], [Coordinates non-blocking periodic conversions and binds hardware ROM/I2C addresses.],
  [Quality Manager], [Enforces data validity flags, timestamp freshness, CRC verification, and bus timeouts.],
  [Measurement Processor], [Calculates numerical moving averages, rate-of-change, and multi-sample statistical reductions.],
  [Thermal Predictor], [Executes rolling 30-second linear regression slope and projects forward horizon temperature.],
  [Fan Controller], [Translates thermal demand into rate-limited PWM duty cycles with stall-prevention boost.],
  [Protection Supervisor], [Executes deterministic, non-preemptible threshold checks for thermal and electrical trips.],
  [Power Manager], [Coordinates state machine transitions, inrush blanking timers, and PS_ON\\# gating.],
  [Local Web Server], [Serves embedded LittleFS dashboard assets and handles authenticated SoftAP endpoints.],
  [Network Manager], [Maintains Wi-Fi link, performs non-blocking reconnects, and caches IP configuration.],
  [Firebase Transport], [Executes authenticated REST PUT/POST uploads and reads remote command queues.],
  [Buffer Manager], [Maintains 120-minute circular RAM outage queue for reliable network backfill.],
  [Event/Advisory Manager], [Evaluates persistent trend deviations and formats structured incident telemetry frames.],
  [Configuration Store], [Manages persistent Non-Volatile Storage (NVS) for calibration offsets and lockout flags.]
)

#eng-box(
  title: "NON-BLOCKING REAL-TIME ARCHITECTURAL PRINCIPLE",
  [Safety-critical acquisition, fan modulation, and supervisory fault evaluation tasks execute with strict real-time priority. Protection routines shall *never* wait on Wi-Fi connection attempts, HTTP transactions, Firebase database round-trips, or Cloudflare Worker invocations.]
)

#v(8pt)

// ============================================================================
// 10. PREDICTIVE THERMAL-MANAGEMENT ALGORITHM
// ============================================================================

= 10. Predictive Thermal-Management Algorithm

=== 10.1 Acquisition

- Proposed temperature sampling interval: $Delta t = 1.0 "second"$.
- DS18B20 12-bit conversion is initiated asynchronously ($750 "ms"$ max). The scratchpad register is read only after conversion completion.
- Each sample record contains the float temperature value, validity boolean, monotonic timestamp, and CRC error status.
- Corrupted or invalid samples are discarded and never enter the trend estimation buffer.

=== 10.2 Digital Filtering

Raw sensor noise is filtered using an Exponential Moving Average (EMA):

$ T_f (k) = alpha T(k) + (1 - alpha) T_f (k - 1) $

- Proposed baseline filter coefficient: $alpha = 0.2$.
- The filter is initialized directly from the first verified valid measurement.
- *Protection Invariant:* Filtered temperature $T_f$ is used strictly for trend projection and fan demand modulation. Unfiltered raw readings $T(k)$ are supervised concurrently by the protection loop to guarantee zero trip latency during sudden thermal excursions.

=== 10.3 Trend Estimation

The temperature-rise rate $r$ (in $degree"C" / "second"$) is estimated over a rolling 30-second window ($N = 30$ valid samples) using an unweighted least-squares linear regression:

$ r = frac(sum_(i=1)^N (t_i - macron(t)) (T_(f,i) - macron(T)_f), sum_(i=1)^N (t_i - macron(t))^2) $

Where $macron(t)$ is the mean timestamp and $macron(T)_f$ is the mean filtered temperature across the active trend window.

=== 10.4 Forward Temperature Projection

The algorithm projects the estimated transformer surface temperature forward across a fixed predictive horizon $H$:

$ T_p = T_f + H dot max(0, r) $

- Proposed predictive horizon: $H = 30 "seconds"$.
- If the trend slope is negative or zero ($r <= 0$), cooling demand relies directly on $T_f$ without downward projection bias.
- During initial boot warm-up (buffer samples $< 30$), forward prediction is marked invalid and fan modulation defaults strictly to $T_f$.

=== 10.5 Fan-Demand Calculation

A piecewise continuous mapping $g(T)$ defines requested fan command duty ($0 "to" 100%$):
- For $T < T_"ramp,start"$: Maintain minimum reliable duty $D_"min"$ ($approx 30%$ to prevent acoustic motor stall).
- For $T_"ramp,start" <= T <= T_"full"$: Linearly ramp duty from $D_"min"$ to $100%$.
- For $T > T_"full"$: Request full $100%$ cooling command.

The automatic cooling duty demand is evaluated as the maximum of current and projected thermal demands:

$ D_"auto" = max(g(T_f), g(T_p)) $

*Actuation Dynamic:* Increases in cooling demand execute immediately without lag. Decreases in cooling demand are slew-rate limited ($<= 1% / "second"$) to prevent rapid thermal cycling and acoustic hunting.

=== 10.6 Ambient Inlet-Air Reference

$ Delta T = T_"surface" - T_"inlet" $

Temperature rise above inlet air ($Delta T$) is computed continuously to provide comparative thermal resistance metrics under varying laboratory ambient temperatures. Primary supervisory trip boundaries remain anchored to absolute surface temperature.

=== 10.7 Virtual Internal Winding Hot-Spot Estimation

Direct measurement via the external surface DS18B20 probe ($T_"surface"$) inherently underestimates internal copper winding temperatures due to the thermal resistance of core insulation and boundary layers. To bridge this gap without physical fiber-optic sensor penetration, a real-time virtual hot-spot estimator calculates:

$ T_"HST,est" = T_f + R_"th,int" dot P_"copper" $

Where $P_"copper"$ is the aggregate instantaneous Joule heating across all three secondary rails:

$ P_"copper" = I_(12V)^2 R_(12V) + I_(5V)^2 R_(5V) + I_(3.3V)^2 R_(3.3V) $

And $R_"th,int"$ is the calibrated internal core-to-surface thermal resistance ($approx 0.85 degree"C"/W$). This estimated hot-spot value is logged to telemetry and supervised as a secondary early-warning boundary.

=== 10.8 Feedforward Load Current Anticipation

To counteract thermal mass latency during sudden heavy step-loads, the fan duty calculation incorporates feedforward current injection:

$ D_"feedforward" = K_"load" dot (I_(12V) + I_(5V) + I_(3.3V)) $

The aggregate fan request is evaluated as the maximum across filtered, projected, and feedforward demands:

$ D_"auto" = max(g(T_f), g(T_p), D_"feedforward") $

This immediately steps up fan cooling when loads engage, preventing temperature spikes before thermal inertia causes core temperatures to rise.

=== 10.9 Algorithm Scope and Delimitations

The prediction algorithm couples a 30-second empirical OLS trend extrapolator with algebraic Joule-loss hot-spot estimation. It provides operational predictive cooling without requiring high-complexity multi-layer CFD or high-overhead neural networks on the edge microcontroller.

#tech-figure(
  caption: "Figure 7: Predictive Thermal-Management Closed-Loop Execution Pipeline",
  [
    #diagram(
      spacing: (10mm, 6.5mm),
      node-stroke: 0.75pt + rgb("0f172a"),
      node-corner-radius: 0pt,
      node-inset: 3pt,
      
      // Top row: Forward processing (Row 0)
      node((0, 0), [Raw Temp $T_1(k)$\ (1 s Rate)], width: 26mm, fill: rgb("f8fafc")),
      edge((0, 0), (1, 0), "-|>", [Async Read], label-size: 6pt),
      node((1, 0), [EMA Filter\ ($alpha = 0.2$)], width: 26mm),
      edge((1, 0), (2, 0), "-|>", [Filtered $T_f$], label-size: 6pt),
      node((2, 0), [Rolling 30 s Buffer\ Least-Squares $r$], width: 28mm),
      edge((2, 0), (3, 0), "-|>", [Rate $r$], label-size: 6pt),
      node((3, 0), [Forward Projection\ $T_p = T_f + H r$], width: 28mm, fill: rgb("f1f5f9")),
      
      // Bottom row: Actuation loop (Row 1)
      edge((3, 0), (3, 1), "-|>", [Projected $T_p$], label-size: 6pt),
      node((3, 1), [Demand Function\ $D = max(g_f, g_p)$], width: 28mm),
      edge((3, 1), (2, 1), "-|>", [Slew Limit], label-size: 6pt),
      node((2, 1), [Rate-Limited PWM\ $25 "kHz"$ Modulation], width: 28mm),
      edge((2, 1), (1, 1), "-|>", [Bridge Drive], label-size: 6pt),
      node((1, 1), [TB6612FNG Bridge\ Two-Wire Cooling Fan], width: 26mm, fill: rgb("f8fafc")),
    )
  ]
)

#pagebreak()

// ============================================================================
// 11. PROTECTION LOGIC
// ============================================================================

= 11. Protection Logic

=== 11.1 Thermal Supervision Progression

#tech-figure(
  caption: "Figure 8: Supervisory Thermal Protection and Escalation Sequence",
  [
    #diagram(
      spacing: (10mm, 6.5mm),
      node-stroke: 0.75pt + rgb("0f172a"),
      node-corner-radius: 0pt,
      node-inset: 3pt,
      
      node((0, 0), [Normal State\ ($T < T_"warn"$)], width: 26mm, fill: rgb("f8fafc")),
      edge((0, 0), (1, 0), "-|>", [$T >= T_"warn"$], label-size: 6pt),
      node((1, 0), [Thermal Warning\ (Log Event & Pre-Cool)], width: 28mm),
      edge((1, 0), (2, 0), "-|>", [$T >= T_"full"$], label-size: 6pt),
      node((2, 0), [Full-Cooling Stage\ ($100%$ Duty Boost)], width: 28mm),
      edge((2, 0), (3, 0), "-|>", [$T >= T_"trip"$], label-size: 6pt),
      node((3, 0), [Confirmed Trip\ (De-assert PS_ON\#)], width: 28mm, fill: rgb("fef2f2")),
    )
  ]
)

Trip thresholds and persistence confirmation windows shall be determined through experimental bench loading rather than copied from arbitrary defaults.

=== 11.2 Electrical Supervision Matrix

#formal-table(
  columns: (1.5fr, 1.8fr, 1.8fr, 1.9fr),
  table.header([*Monitored Rail*], [*Warning Current*], [*Trip Current ($I_"trip"$)*], [*Voltage Trip Window*]),
  [12 V External Rail], [2.5 A (Proposed)], [3.15 A (Fast Trip)], [$10.8 "V" "to" 13.2 "V" (plus.minus 10%)$],
  [Native 5 V Rail], [0.5 A (Unloaded)], [1.0 A (Overcurrent)], [$4.50 "V" "to" 5.50 "V" (plus.minus 10%)$],
  [Native 3.3 V Rail], [0.5 A (Unloaded)], [1.0 A (Overcurrent)], [$2.97 "V" "to" 3.63 "V" (plus.minus 10%)$]
)

- *Overcurrent Action:* If measured current exceeds $I_"trip"$ for $>= 250 "ms"$, GPIO32 is immediately pulled LOW ($< 5 "ms"$), de-asserting PS_ON\\# and latching `ELECTRICAL_LOCKOUT`.
- *Voltage Boundary Anomaly:* If rail voltage leaves the permissible window following startup, an electrical fault is declared.
- *I2C Bus Communication Loss:* Telemetry timeout $> 500 "ms"$ triggers immediate supervisory shutdown (`SENSOR_LOCKOUT`).

=== 11.3 State-Aware Supervision and Inrush Blanking

- During intentional OFF (`STANDBY_OFF`), low voltage on main switched rails is expected and must not generate nuisance undervoltage faults.
- Upon assertion of PS_ON\\# (startup), an inrush blanking window ($500 "ms"$) inhibits false undervoltage/overcurrent trips while output decoupling capacitors charge. Gross short circuits ($I > 200% I_"trip"$) remain actionable immediately.

=== 11.4 Shutdown Verification Gate

When a supervisory trip occurs:
1. De-assert GPIO32 (releasing PS_ON\\# to pull high).
2. Record shutdown timestamp, active fault flag, and all sensor readings.
3. Observe all monitored rail voltages decay below configured threshold ($< 1.0 "V"$) within $500 "ms"$.
4. If rail voltage fails to collapse, declare a `CONTROL_PATH_FAILURE` and alert the operator.

=== 11.5 Convective Airflow Stall & Heat Trap Supervisory Protection

Operating a fan at maximum duty inside a choked or recirculating enclosure can paradoxically increase equipment temperature due to fan motor coil heat dissipation and convective stagnation. 
The supervisor continuously audits cooling effectiveness:
- *Condition:* Fan commanded duty $D_"fan" = 100%$ AND temperature trend slope $r >= 0$ ($T_"surface"$ failing to decrease).
- *Persistence Gate:* Condition sustained continuously for $t_"stall" >= 120 "seconds"$.
- *Action:* Declare `AIRFLOW_STALL_WARNING`, log diagnostic code `ERR_CONVECTIVE_STALL` to Firebase Events, and illuminate the amber status LED. This flags clogged air intakes or physical duct obstruction before the primary 85°C hardware trip ceiling is breached.

#v(8pt)

// ============================================================================
// 12. RECOVERY AND POWER-STATE CONTROL
// ============================================================================

= 12. Recovery and Power-State Control

=== 12.1 Operational State Machine

#tech-figure(
  caption: "Figure 9: Main-Output Operational and Protective State Machine (Planar Orthogonal Layout)",
  [
    #diagram(
      spacing: (11mm, 10mm),
      node-stroke: 0.75pt + rgb("0f172a"),
      node-corner-radius: 0pt,
      node-inset: 3pt,
      
      // Operational Spine (Row 0)
      node((0, 0), [*STANDBY_OFF*\ PS_ON\# Rel.], width: 27mm, fill: rgb("f8fafc")),
      node((1, 0), [*STARTING*\ Inrush Blank], width: 27mm),
      node((2, 0), [*RUNNING*\ Normal Op], width: 27mm, fill: rgb("f1f5f9")),
      
      // Right branches (Faults & Manual Off)
      node((3, -0.7), [*MANUAL_OFF*\ Switch/Remote], width: 28mm),
      node((3, 0.2), [*ELEC_LOCKOUT*\ Latched O/C], width: 28mm, fill: rgb("fef2f2")),
      node((3, 1.1), [*BUS_LOCKOUT*\ Bus Timeout], width: 28mm, fill: rgb("fef2f2")),
      
      // Bottom loop (Thermal management, Row 1.8)
      node((2, 1.8), [*THERMAL_COOL*\ Passive Cooldown], width: 28mm),
      node((1, 1.8), [*RECOVERY_TEST*\ Supervised Run], width: 28mm),
      node((0, 1.8), [*THERMAL_LOCK*\ Max Retries], width: 28mm, fill: rgb("fef2f2")),
      
      // Transitions Row 0
      edge((0, 0), (1, 0), "-|>", [START Req], label-size: 6pt),
      edge((1, 0), (2, 0), "-|>", [Rails OK], label-size: 6pt),
      
      // Transitions to Right Branches
      edge((2, 0), (3, -0.7), "-|>", [OFF Cmd], label-size: 6pt),
      edge((2, 0), (3, 0.2), "-|>", [$I > I_"trip"$], label-size: 6pt),
      edge((2, 0), (3, 1.1), "-|>", [Bus Fail], label-size: 6pt),
      
      // Transitions to Thermal Loop
      edge((2, 0), (2, 1.8), "-|>", [$T >= T_"trip"$], label-size: 6pt),
      edge((2, 1.8), (1, 1.8), "-|>", [Cooled], label-size: 6pt),
      edge((1, 1.8), (2, 0), "-|>", [Stable], label-size: 6pt),
      edge((1, 1.8), (0, 1.8), "-|>", [Retrip], label-size: 6pt),
      edge((0, 1.8), (0, 0), "-|>", [Manual Reset], label-size: 6pt),
    )
  ]
)

=== 12.2 Qualified Thermal Automatic Recovery Rules

Automatic re-energization after a thermal shutdown is strictly conditional and permitted only when:
1. Connected loads are verified safe for unattended re-energization.
2. The initial trip was caused exclusively by a recoverable thermal event (not electrical overcurrent).
3. All temperature and rail sensors report valid, fresh measurements.
4. Transformer surface temperature has dropped below a separate restart threshold: $T <= T_"restart"$.
5. Measured temperature is stable or decreasing over a verified observation period ($>= 300 "seconds"$).
6. Minimum cooling dwell time ($>= 600 "seconds"$) has fully elapsed.
7. No manual OFF switch assertion or remote emergency stop inhibit is active.
8. Remaining automatic retry allowance is available ($N_"retry" > 0$). Default policy: 1 retry per incident.

=== 12.3 Mandatory Restart Restrictions

- Electrical trips *never* restart automatically. Manual bench inspection is mandatory.
- An authorized remote OFF command immediately cancels any pending automatic thermal recovery.
- Network reconnection or cloud sync events never trigger an automatic startup sequence.
- A maintained physical ON switch position does not bypass fault lockouts.
- Controller MCU resets always default main outputs to disabled (`STANDBY_OFF`).

#pagebreak()

// ============================================================================
// 13. MAINTENANCE-ADVISORY FUNCTION
// ============================================================================

= 13. Maintenance-Advisory Function

=== 13.1 Incipient Thermal Fault Detection via Residual Analysis

Rather than relying solely on static over-temperature trip ceilings, the supervisor continuously monitors thermal model residuals to detect incipient cooling degradation (e.g., heatsink paste dry-out, radiator dust fouling, or bearing friction):

$ e(t) = Delta T_"measured"(t) - Delta T_"expected"(I, D_"fan") $

Where the expected steady-state temperature rise is modeled from baseline commissioning data:

$ Delta T_"expected" = K_"thermal" dot I_"total"^2 dot (1.0 - 0.75 dot D_"fan") $

#formal-table(
  columns: (1.8fr, 1.8fr, 3.4fr),
  table.header([*Residual Threshold*], [*Confidence Level*], [*Supervisory Action*]),
  [$e(t) > 1 sigma$ ($+2.0 degree"C"$)], [Baseline variance], [Normal operational drift; no alert.],
  [$e(t) > 2 sigma$ ($+3.5 degree"C"$)], [95.4% confidence], [Log incipient thermal drift advisory to `/history`.],
  [$e(t) > 3 sigma$ ($+5.0 degree"C"$)], [99.7% confidence], [Raise `INCIPIENT_COOLING_DEGRADATION` warning event.],
  [$e(t) > 4 sigma$ ($+7.0 degree"C"$)], [Critical anomaly], [Initiate proactive pre-cooling; dispatch maintenance email.]
)

=== 13.2 Cumulative Arrhenius Insulation Degradation Accounting

To monitor cumulative insulation wear over operational life without complex offline laboratory sampling, the system implements the IEEE Standard C57.91 Arrhenius Aging Acceleration Factor ($F_"AA"$):

$ F_"AA"(t) = exp(frac(15000, 383) - frac(15000, T_"HST,est"(t) + 273.15)) $

- At reference temperature ($110 degree"C"$): $F_"AA" = 1.0$ (1 operating hour consumes exactly 1 hour of normal insulation life).
- At standard operating temperature ($approx 50 degree"C"$): $F_"AA" approx 0.005$ (negligible consumption).
- At elevated thermal excursion ($85 degree"C"$): $F_"AA" approx 0.18$ (accelerating thermal wear).

The system integrates equivalent aging hours into non-volatile storage:

$ "Loss of Life (Equivalent Hours)" = sum_(k) F_"AA"(k) dot frac(Delta t, 3600) $

=== 13.3 Explainable Maintenance Advisory Matrix

#formal-table(
  columns: (2.5fr, 4.5fr),
  table.header([*Condition Indicator*], [*Explainable Maintenance Advisory*]),
  [Incipient residual $e(t) > 3 sigma$ under steady current], [Cooling efficiency degraded; inspect fan filter, clear chassis vents, re-apply thermal grease to transformer core.],
  [Convective stall ($D = 100%$, $r >= 0$ for $>120 "s"$)], [Airflow blocked or recirculating; verify enclosure inlet/outlet clearance and check fan tachometer RPM.],
  [Cumulative $F_"AA"$ acceleration $> 5.0 times$ nominal baseline], [Sustained thermal overload operating history; schedule insulation resistance test and audit downstream rail loading.],
  [Repeated overcurrent or voltage sag anomalies on 12 V rail], [Inspect 12 V downstream wiring harness, check USB converter efficiency, test LED strip for partial shorts.],
  [Insufficient operating history or missing calibration], [Baseline unavailable; collect 8 hours of stable run history before relying on advisory flags.]
)

#eng-box(
  title: "COMPOSITE TRANSFORMER HEALTH INDEX (HI)",
  [A real-time Health Index ($0 "to" 100%$) is synthesized for dashboard display:
  $ "Health Index (HI)" = 100 - "Penalty"_"thermal" - "Penalty"_"overcurrent" - "Penalty"_"aging" - "Penalty"_"residual" $
  - *90--100%:* Nominal / Excellent condition (Green).
  - *70--89%:* Moderate load / Normal aging (Yellow).
  - *50--69%:* Incipient cooling degradation / Inspection recommended (Amber).
  - *< 50%:* Critical condition / Immediate intervention required (Red).]
)

#v(8pt)

// ============================================================================
// 14. LOCAL DASHBOARD AND SETUP
// ============================================================================

= 14. Local Dashboard and Setup

=== 14.1 Local Setup Flow

#tech-figure(
  caption: "Figure 10: First-Time User Commissioning and SoftAP Provisioning Flowchart",
  [
    #diagram(
      spacing: (11mm, 6.5mm),
      node-stroke: 0.75pt + rgb("0f172a"),
      node-corner-radius: 0pt,
      node-inset: 3.5pt,
      
      node((0, 0), [Apply AC Mains Power], width: 40mm, fill: rgb("f8fafc")),
      edge((0, 0), (0, 1), "-|>"),
      node((0, 1), [ESP32 Starts Cold from +5VSB\ (PS_ON\# High / Outputs Disabled)], width: 48mm),
      edge((0, 1), (0, 2), "-|>"),
      node((0, 2), [Launch Setup SoftAP\ (SSID: `ESP32-TMS-SETUP` | IP: `192.168.4.1`)], width: 52mm, fill: rgb("f1f5f9")),
      edge((0, 2), (0, 3), "-|>"),
      node((0, 3), [User Enters Local Router Credentials\ & Selects Telemetry Mode], width: 50mm),
      edge((0, 3), (0, 4), "-|>"),
      node((0, 4), [Execute Wi-Fi Association Test], width: 44mm),
      
      edge((0, 4), (-1, 4), "-|>", [Failed], label-size: 6.5pt),
      node((-1, 4), [Revert to Setup AP;\ Display Diagnostic], width: 32mm, fill: rgb("fef2f2")),
      
      edge((0, 4), (1, 4), "-|>", [Success], label-size: 6.5pt),
      node((1, 4), [Commit to NVS;\ Resume Monitoring], width: 32mm, fill: rgb("f8fafc")),
    )
  ]
)

=== 14.2 Local Embedded Dashboard Features

- *Hardware Independence:* All HTML, CSS, JavaScript, and charting assets are stored in ESP32 internal flash via LittleFS. The offline dashboard functions without internet access or external CDN scripts.
- *Real-Time Telemetry:* Renders live temperatures ($T_1, T_2, Delta T$), rail voltages, currents, power, projected temperature ($T_p$), fan PWM duty ($0 "to" 100%$), operational state, and active trip flags.
- *Local Diagnostics:* Displays Wi-Fi RSSI signal strength, NVS error registers, and direct hardware restart controls.

#v(8pt)

// ============================================================================
// 15. INTERNET DEPLOYMENT AND FULL DATA FLOW
// ============================================================================

= 15. Internet Deployment and Full Data Flow

=== 15.1 Cloud Deployment Roles

#formal-table(
  columns: (2.2fr, 4.8fr),
  table.header([*Cloud Subsystem*], [*Architectural Role & Service Allocation*]),
  [Firebase Hosting], [Static asset hosting for the internet Single-Page Application (SPA) dashboard.],
  [Firebase RTDB], [Authenticated real-time cloud data storage, historical arrays, and remote command queues.],
  [Cloudflare Worker], [Serverless execution engine for asynchronous alert dispatch and scheduled heartbeat auditing.],
  [Brevo Service], [Authenticated transactional email API for urgent operator fault notifications.]
)

#tech-figure(
  caption: "Figure 11: End-to-End Internet Telemetry, Alert Notification, and Remote Command Pipelines",
  [
    #diagram(
      spacing: (9mm, 6.5mm),
      node-stroke: 0.75pt + rgb("0f172a"),
      node-corner-radius: 0pt,
      node-inset: 3pt,
      
      // Flow 1: Telemetry Ingestion (Row 0)
      node((0, 0), [ESP32 Controller\ Shared RAM Snapshot], width: 30mm, fill: rgb("f1f5f9")),
      edge((0, 0), (1, 0), "-|>", [HTTPS PUT], label-size: 6pt),
      node((1, 0), [Firebase RTDB:\ `/devices/{id}/latest`], width: 32mm, fill: rgb("f8fafc")),
      edge((1, 0), (2, 0), "-|>", [WebSocket Sync], label-size: 6pt),
      node((2, 0), [Operator Browser\ SPA (Firebase Hosting)], width: 30mm),
      
      // Flow 2: Urgent Fault Alerts (Row 1)
      node((0, 1), [Declared Fault Trip\ (Hardware Latch OFF)], width: 30mm, fill: rgb("fef2f2")),
      edge((0, 1), (1, 1), "-|>", [Async Commit], label-size: 6pt),
      node((1, 1), [Firebase Events:\ `/devices/{id}/events`], width: 32mm),
      edge((1, 1), (2, 1), "-|>", [HTTPS Trigger], label-size: 6pt),
      node((2, 1), [Cloudflare Worker\ Invokes Brevo API], width: 30mm),
      
      // Flow 3: Remote Emergency OFF (Row 2)
      node((0, 2), [Authorized User\ Confirms OFF in UI], width: 30mm),
      edge((0, 2), (1, 2), "-|>", [Signed Token (30 s)], label-size: 6pt),
      node((1, 2), [Firebase Queue:\ `/commands/{id}`], width: 32mm),
      edge((1, 2), (2, 2), "-|>", [Poll <= 5 s], label-size: 6pt),
      node((2, 2), [ESP32 Ingestion:\ Releases PS_ON\#], width: 30mm, fill: rgb("fef2f2")),
    )
  ]
)

=== 15.2 Telemetry Ingestion (Flow 1)

Every 10 seconds, the ESP32 pushes a lightweight authenticated JSON telemetry payload to Firebase Realtime Database at `/devices/{deviceId}/latest`. Connected operator browsers synchronize instantly via WebSockets. Firebase Hosting serves static files only and is never an intermediary in sensor telemetry transfer.

=== 15.3 Alert Notification Pipeline (Flow 2)

Upon confirming an overcurrent or thermal trip, the ESP32 records an event in `/devices/{deviceId}/events` and notifies the Cloudflare Worker via authenticated HTTPS. The Worker verifies the event record in Firebase and issues an authorized API call to Brevo to dispatch transactional emails to registered maintenance personnel.

=== 15.4 Time-Bounded Remote Emergency OFF (Flow 3)

The internet dashboard supports a cryptographically authorized remote emergency shutdown command:
1. Operator confirms shutdown in the web UI. A signed command is published to `/commands/{deviceId}` with a strict 30-second Time-To-Live (TTL).
2. The ESP32 polls the command queue every 5 seconds.
3. Upon ingestion, the controller verifies command ID uniqueness and expiry, de-asserts GPIO32, releases PS_ON\\#, confirms rail voltage decay, and writes an execution acknowledgment record.
4. *Safety Delimitation:* Remote re-energization (Remote ON) is explicitly prohibited within this baseline design.
'''
