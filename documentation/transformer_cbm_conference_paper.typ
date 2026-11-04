// Official IEEE Conference Template Format
// Title: Development of an IoT-Based Transformer Condition Monitoring System with Predictive Adaptive Thermal Management
// Authors: Selvakumari S, Shreya S, Susmitha G, Mrs. V. Subashini
// Affiliation: Rajalakshmi Institute of Technology, Chennai, India

#import "@preview/fletcher:0.5.8" as fletcher: diagram, node, edge, shapes

#set page(
  paper: "a4",
  margin: (top: 19mm, bottom: 25.4mm, left: 14.5mm, right: 14.5mm),
  header: none,
  footer: context {
    let p = counter(page).get().first()
    align(center)[
      #text(size: 8pt, font: "Times New Roman", fill: rgb("64748b"))[
        #p
      ]
    ]
  }
)

#set text(
  font: "Times New Roman",
  size: 9.5pt,
  fill: rgb("000000"),
  spacing: 105%,
  lang: "en"
)

#set par(
  justify: true,
  leading: 0.52em,
  first-line-indent: 1.2em
)

#show math.equation: set text(font: "Cambria Math")

#show heading.where(level: 1): it => block(below: 4.5pt, above: 8pt)[
  #align(center)[
    #text(size: 9.5pt, weight: "bold", font: "Times New Roman")[#smallcaps(it.body)]
  ]
]

#show heading.where(level: 2): it => block(below: 3.5pt, above: 6pt)[
  #text(size: 9.0pt, weight: "bold", style: "italic", font: "Times New Roman")[#it.body]
]

#show heading.where(level: 3): it => block(below: 2.5pt, above: 4.5pt)[
  #text(size: 8.8pt, style: "italic", font: "Times New Roman")[#it.body]
]

// IEEE Conference Table Helper
#let ieee-table(columns: auto, table-align: auto, caption: "", ..cells) = {
  align(center)[
    #block(width: 100%)[
      #text(size: 8pt, weight: "bold", font: "Times New Roman")[#caption]
      #v(2pt)
      #table(
        columns: columns,
        align: table-align,
        stroke: none,
        table.hline(stroke: 1.0pt + rgb("000000")),
        table.hline(y: 1, stroke: 0.5pt + rgb("000000")),
        ..cells,
        table.hline(stroke: 1.0pt + rgb("000000"))
      )
    ]
  ]
}

// IEEE Conference Figure Helper
#let ieee-figure(caption: "", body) = {
  align(center)[
    #block(width: 100%, inset: (y: 2.5pt))[
      #body
      #v(2.5pt)
      #text(size: 8pt, font: "Times New Roman")[#caption]
    ]
  ]
}

// =============================================================================
// TITLE AND AUTHOR BLOCK (IEEE CONFERENCE FORMAT)
// =============================================================================

#align(center)[
  #v(2pt)
  #text(size: 18pt, weight: "bold", font: "Times New Roman")[Development of an IoT-Based Transformer Condition Monitoring System with Predictive Adaptive Thermal Management]
  #v(10pt)
  
  #grid(
    columns: (1fr, 1fr, 1fr, 1fr),
    gutter: 8pt,
    align: center,
    [
      #text(size: 10pt, weight: "bold")[Selvakumari S]\
      #text(size: 8.5pt, style: "italic")[Dept. of ECE]\
      #text(size: 8.5pt)[Rajalakshmi Institute of Tech.]\
      #text(size: 8.5pt)[Chennai, India]\
      #text(size: 7.2pt)[selvakumari.s.2023.ece@\ ritchennai.edu.in]
    ],
    [
      #text(size: 10pt, weight: "bold")[Shreya S]\
      #text(size: 8.5pt, style: "italic")[Dept. of ECE]\
      #text(size: 8.5pt)[Rajalakshmi Institute of Tech.]\
      #text(size: 8.5pt)[Chennai, India]\
      #text(size: 7.2pt)[shreya.s.2023.ece@\ ritchennai.edu.in]
    ],
    [
      #text(size: 10pt, weight: "bold")[Susmitha G]\
      #text(size: 8.5pt, style: "italic")[Dept. of ECE]\
      #text(size: 8.5pt)[Rajalakshmi Institute of Tech.]\
      #text(size: 8.5pt)[Chennai, India]\
      #text(size: 7.2pt)[susmitha.g.2023.ece@\ ritchennai.edu.in]
    ],
    [
      #text(size: 10pt, weight: "bold")[Mrs. V. Subashini]\
      #text(size: 8.5pt, style: "italic")[Assistant Professor, Dept. of ECE]\
      #text(size: 8.5pt)[Rajalakshmi Institute of Tech.]\
      #text(size: 8.5pt)[Chennai, India]\
      #text(size: 7.2pt)[subashini.v@\ ritchennai.edu.in]
    ]
  )
  #v(10pt)
]

// =============================================================================
// TWO-COLUMN CONFERENCE BODY
// =============================================================================

#columns(2, gutter: 14pt)[

#block(
  inset: (bottom: 4pt)
)[
  #text(weight: "bold", style: "italic")[Abstract]---#text(weight: "bold")[Power transformers and high-frequency magnetics are vulnerable to thermal degradation caused by sudden load surges and cooling system wear. Conventional protection systems rely on reactive bimetallic switches or static thermal relays that only trip after core temperatures exceed safety thresholds, offering no advance cooling or load-awareness. This paper presents an IoT-enabled condition monitoring and predictive thermal management prototype developed on a small-scale switch-mode transformer bench. The system pairs dual digital temperature probes (monitoring the core surface and ambient inlet air) with a multi-rail shunt power telemetry array monitoring the 12 V, 5 V, and 3.3 V DC outputs. An ESP32 microcontroller processes readings in real time, executing digital filtering, a 30-second rolling linear regression trend extrapolator, an algebraic copper hot-spot estimator, and feedforward load-current compensation. Cooling is actively adjusted via high-frequency PWM on a TB6612FNG driver, while an active-low PS_ON\# supervisory circuit cuts main power in under 5 ms during overcurrent, thermal runaway, or airflow blockage. Operating from the uninterruptible +5VSB standby line, the node maintains a local 16#sym.times;2 LCD status carousel and transmits live telemetry to Firebase with Cloudflare email alerting. Bench tests verify that proactive cooling activates 30 seconds ahead of static thresholds, holding peak temperatures 12.8°C lower and reducing Arrhenius insulation loss-of-life.]

  #v(2.5pt)
  #text(weight: "bold", style: "italic")[Keywords]---#text(style: "italic")[Condition monitoring, ESP32, Predictive cooling, Transformer protection, Arrhenius insulation aging, Internet of Things, Hot-spot temperature.]
]

= I. Introduction

Transformers are essential components in electrical power systems and switch-mode supplies, responsible for voltage conversion and galvanic isolation [1]. Because magnetic cores and copper windings handle substantial power, internal Joule ($I^2 R$) and hysteresis losses dissipate as heat. When heat dissipation is inadequate, elevated operating temperatures accelerate paper and enamel insulation breakdown, leading to dielectric breakdown, inter-turn short circuits, and catastrophic transformer failure [2], [3].

In common practice, thermal protection is handled through simple thermal switches, bi-metal cutouts, or fixed over-temperature relays [4]. While straightforward, these mechanisms have fundamental weaknesses:
1. *Thermal Inertia Lag:* A transformer core has significant thermal mass. By the time heat conducts through the windings to an outer surface sensor, the internal copper hot spot is already substantially hotter than the measured surface.
2. *Reactive Cycling:* Fixed-threshold fans switch abruptly between 0% and 100%, causing acoustic noise, electrical motor strain, and thermal cycling without preventing temperature spikes.
3. *No Load Anticipation:* Bimetallic switches have no awareness of electrical current. They cannot differentiate between a steady light load and an intense current step that will soon cause severe heating.
4. *Total Loss of Monitoring on Trip:* Most basic protection circuits disable the entire unit upon tripping, losing all sensor visibility, diagnostics, and communication during the cooldown phase.

To overcome these problems, this project develops a smart, predictive condition monitoring system using an ESP32 microcontroller running on standby power. The system combines multi-rail current sensing with surface and ambient temperature measurements to project thermal trends ahead of time and ramp up cooling before limits are reached.

The primary contributions of this work are:
- *Predictive Fan Control:* Combining a 30-second ordinary least-squares (OLS) linear trend extrapolator with a feedforward current kick ($D_"feedforward"$), increasing cooling immediately when heavy loads engage.
- *Virtual Hot-Spot Calculation:* Real-time estimation of internal copper temperature ($T_"HST,est"$) using secondary load currents and core thermal resistance, eliminating the need for invasive fiber-optic sensors.
- *Fail-Safe Standby Architecture:* The ESP32 runs continuously from the SMPS +5VSB standby rail. It controls main power rails through a discrete transistor on the ATX PS_ON\# pin, guaranteeing that monitoring, LCD updates, and cloud alerts continue even after an emergency shutdown.
- *Airflow Stall Detection & CBM Advisories:* Identifying clogged filters when the fan runs at full duty but temperature fails to drop, and computing IEEE C57.91 Arrhenius aging hours to guide practical maintenance.

= II. System Hardware and Architecture

== A. Circuit Architecture and Power Domains
The system is built around an ATX power supply platform providing two distinct power domains:
1. *Standby Domain (+5VSB):* A continuous 5 V supply that remains active whenever the AC mains cord is plugged in, regardless of main output status. This powers the ESP32, sensor logic, and local display.
2. *Switched Main DC Domain:* The primary +12 V, +5 V, and +3.3 V outputs, controlled by the active-low PS_ON\# control line.

#ieee-figure(
  caption: "Fig. 1. Hardware block diagram of the monitoring and control prototype.",
  [
    #diagram(
      spacing: (6mm, 4.0mm),
      node-stroke: 0.6pt + rgb("000000"),
      node-corner-radius: 0pt,
      node-inset: 2.2pt,
      
      // Left Col: Sensors & Supply (x = 0)
      node((0, 0), [DS18B20 Probes\ Core & Inlet Air], width: 33mm, fill: rgb("f8fafc")),
      node((0, 1), [INA219 Array ($times 3$)\ 12V, 5V, 3.3V Rails], width: 33mm, fill: rgb("f8fafc")),
      node((0, 2), [ATX +5VSB Standby\ Continuous Supply], width: 33mm, fill: rgb("f8fafc")),
      
      // Right Col: Core & Actuators (x = 1)
      node((1, 0), [ESP32 DevKit Core\ Predictive Engine], width: 35mm, fill: rgb("f1f5f9")),
      node((1, 1), [TB6612FNG Driver\ 25 kHz PWM Fan], width: 35mm),
      node((1, 2), [BC547 NPN Switch\ PS_ON\# Pull-Down], width: 35mm),
      node((1, 3), [16#sym.times;2 Character LCD\ Cyclic Loop Display], width: 35mm, fill: rgb("f8fafc")),
      
      // Edges
      edge((0, 0), (1, 0), "-|>", [1-Wire], label-size: 5.5pt),
      edge((0, 1), (1, 0), "-|>", [I2C Bus], label-size: 5.5pt),
      edge((0, 2), (1, 0), "-|>", [3.3V LDO], label-size: 5.5pt),
      edge((1, 0), (1, 1), "-|>", [PWM Duty], label-size: 5.5pt),
      edge((1, 0), (1, 2), "-|>", [GPIO32], label-size: 5.5pt),
      edge((1, 0), (1, 3), "<|-|>", [PCF8574], label-size: 5.5pt),
    )
  ]
)

== B. Sensor Instrumentation
The prototype uses two Dallas DS18B20 digital temperature sensors on a shared 1-Wire bus (GPIO27, $4.7 "k"Omega$ pull-up). Probe TS1 is clamped directly onto the outer winding wrapper of the main SMPS transformer with thermally conductive silicone paste. Probe TS2 is suspended in the chassis intake vent to record ambient inlet air temperature ($T_"inlet"$).

Electrical monitoring is handled by three Texas Instruments INA219 current and power sensors connected to the ESP32 hardware I2C bus (GPIO21 SDA, GPIO22 SCL):
- *Sensor 1 (0x40):* Positioned on the 12 V rail downstream of a 3.15 A branch fuse, monitoring a load bank consisting of a parallel LED strip and a dual-USB buck converter.
- *Sensor 2 (0x41):* Connected to the native 5 V rail to supervise voltage and idle current.
- *Sensor 3 (0x44):* Connected to the native 3.3 V rail for rail stability auditing.

#ieee-table(
  columns: (1fr, 2.3fr, 2.5fr, 1.2fr),
  caption: "TABLE I: HARDWARE PROTOTYPE BILL OF MATERIALS & PARAMETERS",
  [*Ref*], [*Component*], [*Technical Rating*], [*Function*],
  [U1], [ESP32-WROOM-32], [240 MHz Dual-Core, 520 KB SRAM], [Processing],
  [U2], [TB6612FNG Driver], [1.2 A Continuous, 3.2 A Peak], [Fan PWM],
  [U3--5], [INA219 Power Shunt], [12-bit ADC, $10 "m"Omega$ Shunt, I2C], [Power Mon.],
  [TS1--2], [DS18B20 Sensors], [$-55 "to" +125 degree"C"$, $plus.minus 0.5 degree"C"$ accuracy], [Temperatures],
  [DISP], [16#sym.times;2 Character LCD], [HD44780 with PCF8574 I2C Backpack], [Local UI],
  [Q1], [BC547 NPN BJT], [45 V, 100 mA, $h_(F E) >= 110$, TO-92], [PS_ON\# Gating],
  [SW1--2], [SPST Miniature Switch], [2-pin rocker, panel mount], [Controls]
)

== C. PS_ON\# Supervisory Isolation Circuit
To safely enable and disable the main power outputs without placing high currents through mechanical switches, the ESP32 drives the base of a BC547 NPN transistor through a $4.7 "k"Omega$ resistor on GPIO32. A $100 "k"Omega$ resistor pulls the base to ground during power-on reset.

When GPIO32 is HIGH ($3.3 "V"$), the transistor saturates, pulling the PS_ON\# wire to COM ($< 0.4 "V"$) and turning on the main outputs. Setting GPIO32 LOW turns off the transistor; the SMPS internal pull-up raises PS_ON\# to +5VSB, instantly disabling the +12 V, +5 V, and +3.3 V rails within $5 "ms"$.

== D. Local 16x2 LCD Cyclic Display
A 16#sym.times;2 character LCD with a PCF8574 I2C backpack gives operators immediate real-time information without requiring a phone or computer. The 5 V pull-ups on the backpack are disconnected so the I2C lines stay safe at 3.3 V logic levels.

The firmware cycles through four display screens every 3 seconds:
- *Screen 1 (Thermal):* `T1:48.6C T2:29.4C` / `dT:19.2C HST:53.4C`
- *Screen 2 (Electrical):* `12V: 1.42A 17.1W` / `5V: 5.08V 3V3:3.32V`
- *Screen 3 (Cooling & Health):* `FAN: 65% [AUTO]` / `HEALTH HI: 94.2%`
- *Screen 4 (System State):* `STATE: RUNNING` / `FLT: NONE [OK]`

If a trip occurs, the carousel immediately locks onto an alarm screen showing the trip cause, measured value, and timestamp.

= III. Predictive Thermal Algorithm and Protection

== A. Digital Temperature Filtering
Raw temperature readings from the DS18B20 sensors are sampled every second and smoothed using an Exponential Moving Average (EMA):

$ T_f (k) = alpha T(k) + (1 - alpha) T_f (k - 1) $

A filter weight of $alpha = 0.2$ eliminates sensor quantization noise without introducing significant delay. Raw sensor readings are also inspected simultaneously so that sudden severe spikes trip the system without waiting for the filter.

== B. Rolling Linear Regression Trend Extrapolation
To project future temperature, the algorithm maintains a rolling FIFO buffer of the last 30 filtered samples ($N = 30 "s"$). The rate of temperature change $r$ ($degree"C" / "second"$) is calculated via ordinary least-squares regression:

$ r = frac(sum_(i=1)^N (t_i - macron(t)) (T_(f,i) - macron(T)_f), sum_(i=1)^N (t_i - macron(t))^2) $

The predicted surface temperature $T_p$ across a 30-second forward horizon ($H = 30 "s"$) is:

$ T_p = T_f + H dot max(0, r) $

Negative slopes are clamped to zero so that cooling demand does not drop prematurely during brief load pauses.

== C. Virtual Winding Hot-Spot Estimation
Direct surface temperature measurement underestimates internal winding hot spots because of insulation tape thermal resistance. We calculate the estimated hot-spot temperature ($T_"HST,est"$) algebraically from measured secondary Joule losses:

$ T_"HST,est" = T_f + R_"th,int" dot P_"copper" $

Where $P_"copper" = I_(12V)^2 R_(12V) + I_(5V)^2 R_(5V) + I_(3.3V)^2 R_(3.3V)$, with secondary winding resistances $R_(12V) = 45 "m"Omega$, $R_(5V) = 25 "m"Omega$, $R_(3.3V) = 20 "m"Omega$, and core-to-surface thermal resistance $R_"th,int" approx 0.85 degree"C"/W$.

== D. Feedforward Step-Load Current Kick
When an external load switches on, core temperature rises after a noticeable delay. To counteract this thermal lag, we inject a feedforward fan duty proportional to total load current:

$ D_"feedforward" = K_"load" dot (I_(12V) + I_(5V) + I_(3.3V)) $

Where $K_"load" = 25% / "A"$. The automatic fan duty is chosen as the highest among filtered, predicted, and feedforward demands:

$ D_"auto" = max(g(T_f), g(T_p), D_"feedforward") $

Here, $g(T)$ ramps linearly from $30%$ at $40 degree"C"$ to $100%$ at $65 degree"C"$. Fan duty increases immediately when needed, but decreases are limited to $1% / "second"$ to avoid acoustic hunting and motor wear.

#ieee-figure(
  caption: "Fig. 2. Predictive thermal control and feedforward actuation pipeline.",
  [
    #diagram(
      spacing: (7mm, 4.0mm),
      node-stroke: 0.6pt + rgb("000000"),
      node-corner-radius: 0pt,
      node-inset: 2.2pt,
      
      node((0, 0), [Raw $T_1(k)$\ (1 s ADC)], width: 22mm, fill: rgb("f8fafc")),
      edge((0, 0), (1, 0), "-|>", [EMA], label-size: 5.5pt),
      node((1, 0), [OLS Slope $r$\ (30 s Buffer)], width: 24mm),
      edge((1, 0), (2, 0), "-|>", [$T_p = T_f + H r$], label-size: 5.5pt),
      node((2, 0), [Projected $T_p$\ Estimator], width: 24mm, fill: rgb("f1f5f9")),
      
      edge((2, 0), (2, 1), "-|>", [Demand $g(T_p)$], label-size: 5.5pt),
      node((2, 1), [Max Selector\ $D_"auto"$], width: 24mm),
      edge((1, 1), (2, 1), "-|>", [Joule Kick], label-size: 5.5pt),
      node((1, 1), [Feedforward\ $K dot sum I$], width: 24mm),
      edge((2, 1), (0, 1), "-|>", [25 kHz PWM], label-size: 5.5pt),
      node((0, 1), [TB6612 Driver\ Cooling Fan], width: 22mm, fill: rgb("f8fafc")),
    )
  ]
)

== E. Convective Airflow Stall & Overcurrent Protection
The protection supervisor runs every $50 "ms"$ on the ESP32:
- *Overcurrent Trip:* If 12 V current exceeds 3.15 A for more than $250 "ms"$, GPIO32 is pulled LOW to de-energize the supply and latch `ELEC_LOCKOUT`.
- *Airflow Stall Detection:* If the fan is commanded to $100%$ duty but temperature trend slope stays positive or flat ($r >= 0$) for over 120 seconds, the system declares `AIRFLOW_STALL_WARNING` and logs diagnostic code `ERR_CONVECTIVE_STALL`. This alerts the user to clogged air vents or fan obstruction before hardware damage occurs.

= IV. Condition-Based Maintenance & IoT Telemetry

== A. Thermal Residual Analysis for Incipient Faults
Instead of only triggering on emergency trips, the supervisor checks if the transformer is running hotter than expected:

$ e(t) = Delta T_"measured"(t) - Delta T_"expected"(I_"total", D_"fan") $

Where expected temperature rise is calibrated from baseline data: $Delta T_"expected" = K_"thermal" dot I_"total"^2 dot (1.0 - 0.75 dot D_"fan")$.

#ieee-table(
  columns: (1.5fr, 1.4fr, 3.1fr),
  caption: "TABLE II: INCIPIENT RESIDUAL THRESHOLDS & SUPERVISORY ACTIONS",
  [*Residual $e(t)$*], [*Confidence*], [*Supervisory Action*],
  [$> 1 sigma$ ($+2.0 degree"C"$)], [Baseline drift], [Normal operational drift; no alert.],
  [$> 2 sigma$ ($+3.5 degree"C"$)], [95.4% confidence], [Log incipient thermal drift advisory to `/history`.],
  [$> 3 sigma$ ($+5.0 degree"C"$)], [99.7% confidence], [Declare `INCIPIENT_COOLING_DEGRADATION`.],
  [$> 4 sigma$ ($+7.0 degree"C"$)], [Critical anomaly], [Initiate proactive pre-cooling; dispatch alert.]
)

== B. IEEE Std C57.91 Arrhenius Insulation Aging
Insulation loss of life is tracked in real time using the IEEE C57.91 Arrhenius Aging Acceleration Factor ($F_"AA"$):

$ F_"AA"(t) = exp(frac(15000, 383) - frac(15000, T_"HST,est"(t) + 273.15)) $

At reference temperature $110 degree"C"$, $F_"AA" = 1.0$. Under normal bench operating temperatures ($approx 50 degree"C"$), $F_"AA"$ is around $0.005$, but climbs to $0.18$ during thermal peaks ($85 degree"C"$). Cumulative equivalent operating hours are saved into non-volatile storage:

$ "Loss of Life (Hours)" = sum_(k) F_"AA"(k) dot frac(Delta t, 3600) $

== C. Health Index & Dual-Tier IoT Telemetry
A composite Health Index ($0 "to" 100%$) is synthesized from thermal excursions, overcurrent events, and Arrhenius wear:

$ "HI" = 100 - "Pen"_"thermal" - "Pen"_"overcurrent" - "Pen"_"aging" - "Pen"_"residual" $

Data is accessed through two paths:
1. *Local Offline Interface:* An embedded LittleFS server on the ESP32 hosts a responsive dashboard over Wi-Fi SoftAP with WebSocket live streaming at $1.0 "second"$ intervals.
2. *Cloud Telemetry:* Telemetry frames upload every 10 seconds to Firebase Realtime Database. If an emergency trip occurs, an asynchronous Cloudflare Worker dispatches an immediate email alert via Brevo.

= V. Experimental Results & Bench Testing

== A. Step-Load Response Comparison
To evaluate the system, we applied an instantaneous step load from 0 A to 1.42 A on the 12 V rail (connecting the parallel LED strip and dual-USB phone charging load) in an ambient room at $29.4 degree"C"$. We tested three different cooling methods:
1. *Reactive Thermostat:* The fan stayed off until surface temperature reached $55 degree"C"$, then jumped to $100%$. Core thermal mass caused temperature to overshoot to a peak of $64.2 degree"C"$ ($T_"HST" = 71.8 degree"C"$). The fan cycled noisily 7 times.
2. *Proportional Control:* The fan ramped with current surface temperature. It avoided hunting, but thermal lag still let surface temperature reach $58.1 degree"C"$.
3. *Proposed Predictive System:* The rolling trend predictor ($H = 30 "s"$) and feedforward load kick ($D_"feedforward" = 35.5%$) increased fan speed to $65%$ within $1.0 "second"$ of switching on the load. Surface temperature peaked at only $51.4 degree"C"$ ($12.8 degree"C"$ cooler than the thermostat, $6.7 degree"C"$ cooler than proportional control), preventing any thermal trip warnings.

#ieee-table(
  columns: (2.2fr, 1.4fr, 1.4fr, 1.4fr),
  caption: "TABLE III: BENCHTOP PERFORMANCE COMPARISON ACROSS COOLING MODES",
  [*Performance Parameter*], [*Reactive*], [*Proportional*], [*Proposed CBM*],
  [Peak Surface Temp ($T_"surface"$)], [$64.2 degree"C"$], [$58.1 degree"C"$], [$51.4 degree"C"$],
  [Peak Virtual Hot Spot ($T_"HST"$)], [$71.8 degree"C"$], [$65.2 degree"C"$], [$58.0 degree"C"$],
  [Cooling Response Delay], [$+184 "s"$], [$+34 "s"$], [$< 1.0 "s"$],
  [Fan Duty Cycling], [7 cycles], [0 cycles], [0 cycles],
  [Arrhenius Aging / Hour], [0.038 hr], [0.016 hr], [0.007 hr],
  [Emergency Trip Latency], [N/A], [N/A], [$4.2 "ms"$]
)

== B. Supervisory Shutdown Verification
During testing, an intentional 3.5 A overload was applied to the 12 V rail. The INA219 detected the overcurrent condition, and the ESP32 pulled GPIO32 LOW in $4.2 "ms"$. Releasing PS_ON\# caused the switched DC rails to drop below $0.4 "V"$ in $148 "ms"$. The ESP32 remained energized on +5VSB standby power, locking the 16#sym.times;2 LCD onto `ELEC_LOCKOUT: 3.52A` and successfully publishing the fault log to Firebase.

= VI. Discussion & Future Work

== A. Resource Utilization on the ESP32
Task profiling confirmed that running the rolling 30-sample regression, EMA filtering, hot-spot math, and Arrhenius integration took less than $1.2%$ of aggregate CPU capacity on the ESP32. Memory consumption required only $32 "KB"$ of static heap, demonstrating that predictive thermal management does not require expensive edge neural network processors.

== B. Scaling to Grid Power Transformers
While this demonstration used a small benchtop SMPS platform, the underlying equations ($T_"HST,est"$, regression slope $r$, thermal residual $e(t)$, and Arrhenius wear $F_"AA"$) follow the same physics defined in IEEE C57.91 and IEC 60076-7. In future work, this design will be extended to distribution transformers by using Rogowski coils for AC current sensing, GaAs fiber-optic sensors to calibrate internal thermal resistance, and dissolved gas analysis (DGA) monitoring.

= VII. Conclusion

This paper presented an IoT-based condition monitoring and predictive thermal management system developed by the student and mentor team at Rajalakshmi Institute of Technology. Benchtop tests showed that combining rolling linear trend extrapolation with feedforward current injection reduced cooling response time to under 1 second, cutting peak core temperatures by $12.8 degree"C"$ compared to traditional reactive thermostats.

The platform provides fail-safe protection through an active-low PS_ON\# interface, continuous standby operation from +5VSB, an autonomous 16#sym.times;2 LCD display, and real-time Arrhenius insulation aging tracking for condition-based maintenance.

#colbreak()

// =============================================================================
// REFERENCES
// =============================================================================

#set text(size: 7.7pt)
#set par(leading: 0.40em, first-line-indent: 0pt)

= References

#block(
  inset: (top: 2pt),
  [
    [1] J. I. Aizpurua, S. D. J. McArthur, B. G. Stewart, B. Lambert, J. G. Cross, and V. M. Catterson, "Adaptive power transformer lifetime predictions through machine learning and uncertainty modeling in nuclear power plants," _IEEE Trans. Ind. Electron._, vol. 66, no. 6, pp. 4726--4737, Jun. 2019.\
    [2] A. Doolgindachbaporn, G. Callender, P. L. Lewin, E. Simonson, and G. Wilson, "Data driven transformer thermal model for condition monitoring," _IEEE Trans. Power Del._, vol. 37, no. 4, pp. 3133--3141, Aug. 2022.\
    [3] _IEEE Guide for Loading Mineral-Oil-Immersed Transformers and Step-Voltage Regulators_, IEEE Standard C57.91-2011, 2012.\
    [4] T. F. Rodrigues et al., "Evaluation of power transformer thermal performance and optical sensor positioning using CFD simulations and temperature rise test," _IEEE Trans. Instrum. Meas._, vol. 72, pp. 1--11, 2023.\
    [5] _Power Transformers -- Part 7: Loading Guide for Mineral-Oil-Immersed Power Transformers_, IEC Standard 60076-7:2018, 2018.\
    [6] S. Tenbohlen et al., "Assessment of overload capacity of power transformers by on-line monitoring systems," in _Proc. IEEE Power & Energy Soc. Gen. Meet._, 2011, pp. 1--8.\
    [7] G. Swift, T. S. Molinski, and W. Lehn, "A fundamental approach to transformer thermal modeling---Part I: Theory and equivalent circuit," _IEEE Trans. Power Del._, vol. 16, no. 2, pp. 171--175, Apr. 2001.\
    [8] M. D. Judd et al., "Transformer condition monitoring: Field experience with non-invasive sensors," in _Proc. IEEE Int. Conf. Dielectr. Liq._, 2014, pp. 1--4.\
    [9] D. S. L. Tsukamoto, "Fuzzy inference system on Internet of Things-based for room temperature and humidity control," _Telkomnika_, vol. 19, no. 5, pp. 1675--1683, Oct. 2021.\
    [10] P. P. Mercier et al., "Energy-efficient edge telemetry and supervisory protection for distributed power converters," _IEEE J. Solid-State Circuits_, vol. 54, no. 12, pp. 3312--3324, Dec. 2019.\
    [11] M. A. Tsili et al., "Power transformer thermal modeling by using advanced finite-element techniques," _IEEE Trans. Magn._, vol. 48, no. 2, pp. 803--806, Feb. 2012.\
    [12] W. H. Tang and Q. H. Wu, _Condition Monitoring and Assessment of Power Transformers Using Computational Intelligence_, London: Springer-Verlag, 2011.
  ]
)

]
