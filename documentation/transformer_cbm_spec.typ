// Formal Technical Specification Document - Version 3.0
// Platform: Small-Scale ATX SMPS Demonstration Bench
// Classification: Controlled Engineering Specification

#import "@preview/fletcher:0.5.8" as fletcher: diagram, node, edge, shapes
#import "@preview/cetz:0.5.3"
#import "@preview/cetz-plot:0.1.4": plot

#set page(
  paper: "a4",
  margin: (x: 2.2cm, top: 2.5cm, bottom: 2.5cm),
  header: context {
    let page-num = counter(page).get().first()
    if page-num > 2 [
      #grid(
        columns: (1fr, 1fr),
        align: (left, right),
        [#text(size: 7.5pt, font: "Segoe UI", fill: rgb("475569"))[Transformer Condition Monitoring & Predictive Thermal Management]],
        [#text(size: 7.5pt, font: "Segoe UI", fill: rgb("475569"))[Engineering Specification Baseline -- Rev 3.0]]
      )
      #line(length: 100%, stroke: 0.5pt + rgb("cbd5e1"))
    ]
  },
  footer: context {
    let page-num = counter(page).get().first()
    if page-num > 1 [
      #line(length: 100%, stroke: 0.5pt + rgb("cbd5e1"))
      #v(2pt)
      #grid(
        columns: (1fr, 1fr),
        align: (left, right),
        [#text(size: 7.5pt, font: "Segoe UI", fill: rgb("64748b"))[Hardware & Firmware Systems Architecture Baseline]],
        [#text(size: 7.5pt, font: "Segoe UI", fill: rgb("64748b"))[Page #counter(page).display("1 of 1", both: true)]]
      )
    ]
  }
)

#set text(
  font: "Segoe UI",
  size: 8.8pt,
  fill: rgb("0f172a"),
  spacing: 120%,
  lang: "en"
)

#set par(
  justify: true,
  leading: 0.62em,
)

#set heading(numbering: none)
#show heading.where(level: 1): it => block(below: 12pt, above: 18pt)[
  #text(size: 13.5pt, weight: "bold", fill: rgb("0f172a"))[#it.body]
  #v(2pt)
  #line(length: 100%, stroke: 1.2pt + rgb("0f172a"))
]

#show heading.where(level: 2): it => block(below: 8pt, above: 12pt)[
  #text(size: 10.5pt, weight: "bold", fill: rgb("1e293b"))[#it.body]
]

#show heading.where(level: 3): it => block(below: 6pt, above: 9pt)[
  #text(size: 9.2pt, weight: "bold", fill: rgb("334155"))[#it.body]
]

// Professional Engineering Helpers
#let formal-table(columns: auto, align: auto, ..cells) = {
  table(
    columns: columns,
    align: align,
    stroke: none,
    fill: (x, y) => if y == 0 { rgb("f1f5f9") } else if calc.even(y) { rgb("f8fafc") } else { none },
    table.hline(stroke: 1.2pt + rgb("0f172a")),
    table.hline(y: 1, stroke: 0.6pt + rgb("334155")),
    ..cells,
    table.hline(stroke: 1.2pt + rgb("0f172a"))
  )
}

#let tech-figure(caption: "", body) = {
  align(center)[
    #block(
      width: 100%,
      stroke: 0.75pt + rgb("cbd5e1"),
      inset: (x: 8pt, y: 8pt),
      fill: rgb("ffffff"),
      [
        #body
        #v(5pt)
        #text(size: 7.5pt, weight: "bold", font: "Segoe UI", fill: rgb("334155"))[#caption]
      ]
    )
  ]
}

#let eng-box(title: "NOTE", body) = {
  block(
    width: 100%,
    stroke: (left: 3pt + rgb("0284c7"), rest: 0.5pt + rgb("cbd5e1")),
    inset: (x: 9pt, y: 7pt),
    fill: rgb("f8fafc"),
    [
      #text(size: 8pt, weight: "bold", fill: rgb("0284c7"))[#title]
      #v(2pt)
      #text(size: 8.3pt, fill: rgb("1e293b"))[#body]
    ]
  )
}

#let hazard-box(title: "ELECTRICAL HAZARD STATEMENT", body) = {
  block(
    width: 100%,
    stroke: (left: 3pt + rgb("b91c1c"), rest: 0.5pt + rgb("fecaca")),
    inset: (x: 9pt, y: 7pt),
    fill: rgb("fef2f2"),
    [
      #text(size: 8pt, weight: "bold", fill: rgb("b91c1c"))[#title]
      #v(2pt)
      #text(size: 8.3pt, fill: rgb("7f1d1d"))[#body]
    ]
  )
}

// ============================================================================
// TITLE COVER PAGE (PROFESSIONAL ENGINEERING BASELINE)
// ============================================================================

#align(center)[
  #v(20pt)
  #text(size: 10pt, weight: "bold", tracking: 0.15em, fill: rgb("475569"))[CONTROLLED ENGINEERING SPECIFICATION]
  #v(5pt)
  #text(size: 8.5pt, weight: "medium", tracking: 0.08em, fill: rgb("64748b"))[HARDWARE ARCHITECTURE, EMBEDDED CONTROL & CLOUD SUPERVISION]
  #v(12pt)
  #line(length: 100%, stroke: 1.5pt + rgb("0f172a"))
  #v(14pt)
  
  #text(size: 17pt, weight: "bold", fill: rgb("0f172a"))[
    Development of an IoT-Based Transformer Condition Monitoring System with Predictive Adaptive Thermal Management
  ]
  
  #v(8pt)
  #text(size: 10pt, style: "italic", fill: rgb("334155"))[
    Consolidated Project Design, Circuit Interfaces, Real-Time Predictive Algorithms, and Validation Protocols
  ]
  
  #v(14pt)
  #line(length: 100%, stroke: 0.75pt + rgb("cbd5e1"))
  #v(18pt)
]

#grid(
  columns: (1fr, 1fr),
  gutter: 16pt,
  [
    #block(
      stroke: 0.75pt + rgb("cbd5e1"),
      inset: 11pt,
      fill: rgb("f8fafc"),
      width: 100%,
      [
        #text(size: 8.5pt, weight: "bold", fill: rgb("0f172a"))[DOCUMENT INFORMATION]
        #v(5pt)
        #line(length: 100%, stroke: 0.5pt + rgb("cbd5e1"))
        #v(5pt)
        #grid(
          columns: (1.1fr, 1.4fr),
          row-gutter: 5pt,
          [*Document Type:*], [Consolidated Engineering Spec],
          [*Baseline Rev:*], [3.0 -- Production Baseline],
          [*Date:*], [October 30, 2026],
          [*Classification:*], [Engineering Design Record],
          [*Target System:*], [Small-Scale ATX SMPS Bench],
          [*Primary Controller:*], [ESP32-WROOM DevKitC (30-pin)],
          [*Status:*], [Engineering Design Baseline (Pre-Commissioning)]
        )
      ]
    )
  ],
  [
    #block(
      stroke: 0.75pt + rgb("cbd5e1"),
      inset: 11pt,
      fill: rgb("f8fafc"),
      width: 100%,
      [
        #text(size: 8.5pt, weight: "bold", fill: rgb("0f172a"))[ARCHITECTURE ALLOCATION]
        #v(5pt)
        #line(length: 100%, stroke: 0.5pt + rgb("cbd5e1"))
        #v(5pt)
        #grid(
          columns: (1.1fr, 1.4fr),
          row-gutter: 5pt,
          [*Embedded Core:*], [ESP32 (Acquisition & Trips)],
          [*Power Isolation:*], [Active-Low PS_ON\# Circuit],
          [*Cooling Driver:*], [TB6612FNG H-Bridge (PWM)],
          [*Instrumentation:*], [3x INA219 + 2x DS18B20 + 16#sym.times;2 LCD],
          [*Local Interface:*], [ESP32 LittleFS & 16#sym.times;2 LCD],
          [*Cloud Storage:*], [Firebase Realtime Database],
          [*Supervision:*], [Cloudflare Worker + Brevo API]
        )
      ]
    )
  ]
)

#v(12pt)

#eng-box(
  title: "SYSTEM ARCHITECTURAL GOVERNING PRINCIPLE",
  [All safety-critical thermal monitoring, multi-rail electrical supervision, forward temperature trend projection, and protective shutdown decisions execute autonomously within the local ESP32 firmware loop. The ATX switch-mode power supply (SMPS) remains fully monitored and controllable locally from uninterrupted +5VSB standby power, even during total external internet, Wi-Fi, or cloud service outages.]
)

#v(8pt)

#eng-box(
  title: "PROJECT PLATFORM & SCOPE DELIMITATION",
  [This specification establishes the hardware, firmware, and supervisory implementation for demonstrating condition monitoring and predictive adaptive thermal control on a small-scale ATX switch-mode power supply assembly. This design demonstrates the monitoring and control principles using low-voltage instrumentation -- it does not constitute a certified utility-grid transformer protective device, substation protection relay, or safety-instrumented emergency-stop (SIS/E-stop) system.]
)

#pagebreak()

// ============================================================================
// TABLE OF CONTENTS
// ============================================================================

#v(8pt)
#text(size: 13.5pt, weight: "bold", fill: rgb("0f172a"))[Table of Contents]
#v(4pt)
#line(length: 100%, stroke: 1.2pt + rgb("0f172a"))
#v(8pt)

#outline(
  title: none,
  indent: auto,
  depth: 2
)

#pagebreak()


// ============================================================================
// 1. DOCUMENT INFORMATION
// ============================================================================

= 1. Document Information

#formal-table(
  columns: (2.2fr, 4.8fr),
  table.header([*Item*], [*Description*]),
  [Document Type], [Consolidated project design and implementation documentation],
  [Version], [3.0 -- Production Baseline],
  [Date], [October 30, 2026],
  [Project Platform], [Small-scale ATX SMPS demonstration],
  [Controller], [ESP32-WROOM development board (30-pin, CP2102 USB-C)],
  [Status], [Engineering Design Baseline (Pre-Commissioning Phase)],
  [Main Objective], [Demonstrate condition monitoring, predictive cooling, supervisory shutdown, and IoT reporting]
)

This document consolidates the agreed technical design. It is not a claim that the system has already been assembled, calibrated, or validated. 

#eng-box(
  title: "SCOPE BOUNDARY & DEMONSTRATION OBJECTIVE",
  [The objective of this project is to demonstrate condition-monitoring, predictive thermal-control, and supervisory-protection principles using a small-scale ATX switch-mode power supply (SMPS) bench. It is *not* intended to construct an industrial grid transformer-protection system or replace certified primary overcurrent devices.]
)

=== 1.1 Interpretation

- *"Shall"* identifies a mandatory implementation requirement.
- *"Proposed"* identifies an engineering value, threshold, or method that requires experimental bench testing before final commissioning acceptance.

#v(8pt)

// ============================================================================
// 2. ABSTRACT
// ============================================================================

= 2. Abstract

The project monitors the surface temperature of an SMPS transformer, inlet-air temperature, and the voltage, current, and power of three DC output rails: 12 V, 5 V, and 3.3 V.

An ESP32 microcontroller processes all sensor measurements locally, predicts near-term temperature rise through numerical trend extrapolation, and modulates a two-wire fan through a Toshiba TB6612FNG dual-bridge driver. The controller requests emergency supervisory shutdown of all main outputs via the ATX PS_ON\# active-low interface when validated thermal or electrical trip conditions occur.

The ESP32 operates continuously from the SMPS +5VSB standby supply so that condition monitoring, event logging, and telemetry reporting continue uninterrupted even after main outputs are disabled. Selected thermal trip incidents may permit a qualified automatic restart following verified cooldown, whereas electrical overcurrent and bus fault trips remain latched permanently for physical inspection.

The system provides:
- An offline, zero-dependency dashboard hosted directly by the ESP32 via LittleFS.
- An internet-accessible real-time dashboard hosted on Firebase Hosting.
- Persistent time-series history, statistical summaries, and fault event logs stored in Firebase Realtime Database.
- Transactional email alert notifications dispatched via a Cloudflare Worker invoking the Brevo API.
- Independent heartbeat communication-loss supervision executed by scheduled Cloudflare Cron Triggers.
- Explainable, condition-based maintenance advisories derived from thermal trends and fault history without unsupported component failure-life claims.

#v(8pt)

// ============================================================================
// 3. OBJECTIVES
// ============================================================================

= 3. Objectives

1. Measure transformer-surface temperature and ambient inlet-air reference temperature with calibrated digital sensors.
2. Continuously monitor native DC output-rail voltage, load current, and power across all three primary outputs (12 V, 5 V, and 3.3 V).
3. Demonstrate measurable, verified external electrical loading on the 12 V rail using parallel DC branches.
4. Predict short-term transformer surface-temperature trends using a rolling least-squares digital filter.
5. Dynamically increase fan cooling demand ahead of time before a measured-temperature trip threshold is breached.
6. Request prompt supervisory shutdown of all main SMPS DC outputs upon detection of confirmed thermal or electrical faults.
7. Maintain continuous monitoring, diagnostic reporting, and network connectivity from standby power during main-rail shutdown.
8. Provide dual-tier local (offline SoftAP) and remote (cloud-synchronized) operational dashboards.
9. Maintain persistent telemetry history and structured event logs with bounded outage buffering.
10. Deliver actionable, explainable maintenance advisories based on empirical thermal resistance and operating history.

=== 3.1 Exclusions

The initial implementation explicitly does not provide:
- Direct measurement of internal transformer winding hot-spot temperature, core magnetic flux, or insulation dielectric degradation.
- Insulation-health remaining useful life (RUL) prognostic estimation.
- AC mains line input-power or power-factor measurement.
- Actual fan tachometer (RPM) pulse feedback or blade stall detection.
- Individual branch load disconnection (all main outputs are interrupted together via PS_ON\#).
- Primary certified circuit-breaker or fast short-circuit protection (the INA219 is an instrument, not a circuit breaker).
- Safety-instrumented system (SIS) or emergency-stop (E-stop) functional safety certification.

#v(8pt)

// ============================================================================
// 4. SYSTEM ARCHITECTURE
// ============================================================================

= 4. System Architecture

#tech-figure(
  caption: "Figure 1: Complete System Hardware Interconnect, Local Access, and Cloud Telemetry Architecture",
  [
    #diagram(
      spacing: (11mm, 6mm),
      node-stroke: 0.75pt + rgb("0f172a"),
      node-corner-radius: 0pt,
      node-inset: 3pt,
      
      // Col 0: Inputs & Power (x = 0)
      node((0, -0.6), [Transformer DS18B20\ & Inlet DS18B20], width: 27mm, fill: rgb("f8fafc")),
      node((0, 0.3), [INA219 Modules ($times 3$)\ 12 V, 5 V, 3.3 V], width: 27mm, fill: rgb("f8fafc")),
      node((0, 1.2), [16#sym.times;2 Character LCD\ (Cyclic Loop Display)], width: 27mm, fill: rgb("f8fafc")),
      node((0, 2.2), [ATX SMPS +5VSB\ Standby Supply], width: 27mm, fill: rgb("f8fafc")),
      
      // Col 1: Controller Core (x = 1)
      node((1, -0.6), [Local User Terminal\ (Direct Wi-Fi / SoftAP)], width: 34mm),
      node((1, 0.8), [ESP32 Controller Core\ (Acquisition, Predictor,\ Protection & Web Server)], width: 34mm, fill: rgb("f1f5f9")),
      node((1, 2.2), [Standby Power Filter\ & 3.3 V Decoupling], width: 30mm),
      
      // Col 2: Actuators & Cloud Storage (x = 2)
      node((2, 0), [TB6612FNG Driver\ #sym.arrow.r Two-Wire Fan], width: 28mm),
      node((2, 0.8), [2N3904 NPN Switch\ #sym.arrow.r PS_ON\# Pull-Down], width: 28mm),
      node((2, 1.8), [Firebase RTDB\ `/latest`, `/events`], width: 28mm, fill: rgb("f8fafc")),
      
      // Col 3: Cloud Dashboards & Alerts (x = 3)
      node((3, 1.3), [Firebase Hosting\ Web Dashboard], width: 28mm),
      node((3, 2.2), [Cloudflare Worker\ & Brevo Email API], width: 28mm),
      
      // Connecting Edges
      edge((0, -0.6), (1, 0.8), "-|>", [1-Wire], label-size: 6pt),
      edge((0, 0.3), (1, 0.8), "-|>", [I2C], label-size: 6pt),
      edge((0, 1.2), (1, 0.8), "<|-|>", [I2C], label-size: 6pt),
      edge((0, 2.2), (1, 2.2), "-|>", [+5VSB], label-size: 6pt),
      edge((1, 2.2), (1, 0.8), "-|>", [Reg. 5V], label-size: 6pt),
      edge((1, -0.6), (1, 0.8), "<|-|>", [HTTP / WS], label-size: 6pt),
      
      edge((1, 0.8), (2, 0), "-|>", [PWM Duty], label-size: 6pt),
      edge((1, 0.8), (2, 0.8), "-|>", [GPIO32], label-size: 6pt),
      edge((1, 0.8), (2, 1.8), "-|>", [HTTPS PUT], label-size: 6pt),
      
      edge((2, 1.8), (3, 1.3), "<|-|>", [WebSockets], label-size: 6pt),
      edge((2, 1.8), (3, 2.2), "<|-|>", [Cron Audit], label-size: 6pt),
    )
  ]
)

=== 4.1 Control Authority

The ESP32 microcontroller retains sole, uncompromised real-time control authority over fan speed modulation and supervisory shutdown. The cloud infrastructure provides secondary telemetry persistence, browser visualization, authenticated remote OFF commands, and asynchronous notifications. Under no circumstances is the local protection loop dependent on network connectivity, internet availability, or cloud service responsiveness.

#v(8pt)

#pagebreak()

// ============================================================================
// 5. HARDWARE BILL OF MATERIALS & COMPONENT SPECIFICATIONS
// ============================================================================

= 5. Hardware Bill of Materials & Component Specifications

The instrumentation and control platform utilizes industrial-grade prototyping components structured across core processing, sensing, power actuation, and local display subsystems.

=== 5.1 Bill of Materials (BOM)

#formal-table(
  columns: (0.9fr, 2.3fr, 2.4fr, 0.6fr, 1.4fr),
  table.header([*Ref*], [*Component / Module*], [*Key Specifications*], [*Qty*], [*Subsystem*]),
  [U1], [ESP32-WROOM-32 DevKit], [30-pin, CP2102 USB-C, Dual-Core 240MHz], [1], [Processing / IoT],
  [U2], [TB6612FNG Dual H-Bridge], [1.2 A cont., 3.2 A peak, 15 V VM max], [1], [Thermal Actuation],
  [U3--U5], [INA219 DC Power Monitors], [12-bit ADC, $10 "m"Omega$ Shunt, I2C Bus], [3], [Power Monitoring],
  [TS1--TS2], [DS18B20 Digital Probes], [1-Wire, $plus.minus 0.5 degree"C"$ accuracy, 12-bit], [2], [Thermal Sensing],
  [DISP1], [16#sym.times;2 Character LCD], [HD44780 with PCF8574 I2C Backpack], [1], [Local Telemetry],
  [PSU1], [ATX SMPS Bench Platform], [Standard ATX 12V/5V/3.3V, +5VSB, PS_ON\#], [1], [Power Infeed],
  [MOD1], [XH-M229 Bench Breakout], [24-pin ATX connector, terminal binding posts], [1], [Power Distribution],
  [VR1], [Buck Step-Down Converter], [6--40 V in, dual 5 V USB 3 A out], [1], [12 V Load Branch 2],
  [LOAD1], [12 V High-Density LED Strip], [Monochrome cold-white, 1 m, ~0.6 A nom.], [1], [12 V Load Branch 1],
  [Q1], [JCET 2N3904 NPN BJT], [TO-92, 40 V, 200 mA, $h_(F E) = 100 - 300$, Lead 1:E 2:B 3:C], [1], [PS_ON\# Interface],
  [SW1--SW2], [Miniature SPST Rockers], [2-pin panel mount, contact rated 250V/3A], [2], [Manual UI Controls],
  [F1--F4], [Fast-Acting Cartridge Fuses], [5x20 mm glass, 1.0 A (+5VSB), 3.15 A (12V)], [4], [Circuit Protection],
  [PASS], [Passive Components Assortment], [Metal film resistors (4.7k, 10k, 100k), caps], [1 set], [Signal / Filter]
)

=== 5.2 Component Technical Allocations

1. *Core Microcontroller (ESP32-WROOM-32):* Operates as the central embedded controller executing real-time digital filtering, least-squares thermal trend estimation, multi-rail protection supervision, and local web serving.
2. *Thermal Sensors (DS18B20):* TS1 is mechanically coupled to the SMPS main transformer core wrapper with thermally conductive paste and Kapton insulation; TS2 is suspended in the chassis intake duct for ambient reference.
3. *Power Telemetry (INA219):* Three shunt sensors monitor rail voltages and currents over a shared I2C bus with hardware jumper-selected addresses (`0x40`, `0x41`, `0x44`).
4. *Thermal Actuator (TB6612FNG):* Provides high-frequency ($25 "kHz"$) PWM speed control for the 12 V cooling fan without audible switching noise or electrical motor stalling.
5. *Supervisory Inhibit Switch (2N3904):* Sinks the ATX PS_ON\# wire to COM ground during active operation; de-energizing its base immediately trips all main DC rails to high-Z.

=== 5.3 Prototyping Substrate and Interconnect Standards

- *Prototyping Substrate:* High-grade single-sided copper prototyping Vero-boards ($90 times 150 "mm"$) with dedicated common bus power distribution.
- *Interconnect Cabling:* 18 AWG stranded copper wire for all primary DC rails and high-current fan/load loops; 24 AWG ribbon wire for 1-Wire, I2C, and logic control signals.
- *Insulation & Mechanical Mounting:* Polyolefin flame-retardant heat-shrink sleeving across all exposed high-voltage and DC terminal junctions; thermal adhesive / silicone mounting for DS18B20 core surface coupling.
- *Bench Supply Integration:* Standard desktop SMPS with verified continuous +5VSB rating ($>= 1.5 "A"$) and active-low PS_ON\# wire. The internal fan is audited prior to connection to ensure inrush and operating current remain safely within the TB6612FNG $1.2 "A"$ rating.

#pagebreak()

// ============================================================================
// 6. MEASUREMENT AND LOAD ARRANGEMENT
// ============================================================================

= 6. Measurement and Load Arrangement

=== 6.1 Channel Assignment

#formal-table(
  columns: (1.5fr, 2fr, 3.5fr),
  table.header([*Channel*], [*Measurement Target*], [*Physical Instrumentation Boundary*]),
  [Temperature 1], [Transformer Surface], [Direct contact with core/winding outer insulation wrapper],
  [Temperature 2], [Inlet-Air Reference], [Ambient airflow infeed path upstream of thermal rise],
  [INA219 #1], [12 V External Load], [Shunt in series with parallel LED strip & USB converter],
  [INA219 #2], [Native 5 V Rail], [Unloaded native SMPS 5 V bus voltage monitoring],
  [INA219 #3], [Native 3.3 V Rail], [Unloaded native SMPS 3.3 V bus voltage monitoring]
)

=== 6.2 External Loads

Only the 12 V external load path is populated with active loads during initial demonstration:

#tech-figure(
  caption: "Figure 2: 12 V External Load Path and Measurement Boundary",
  [
    #diagram(
      spacing: (8mm, 6.5mm),
      node-stroke: 0.75pt + rgb("0f172a"),
      node-corner-radius: 0pt,
      node-inset: 3pt,
      
      node((0, 0), [Main 12 V Rail\ (XH-M229)], width: 26mm, fill: rgb("f8fafc")),
      edge((0, 0), (1, 0), "-|>", [12 V Infeed], label-size: 6pt),
      node((1, 0), [Branch Fuse\ (Fast 3.15 A)], width: 26mm),
      edge((1, 0), (2, 0), "-|>", [Protected], label-size: 6pt),
      node((2, 0), [INA219 #1 Shunt\ ($10 "m"Omega$ Resistor)], width: 26mm, fill: rgb("f1f5f9")),
      
      // Parallel branches
      edge((2, 0), (3, -0.6), "-|>", [Branch 1], label-size: 6pt),
      node((3, -0.6), [12 V LED Strip\ (~0.5 A to 1.0 A)], width: 27mm),
      
      edge((2, 0), (3, 0.6), "-|>", [Branch 2], label-size: 6pt),
      node((3, 0.6), [6-40V to 5V USB\ Step-Down Converter], width: 27mm),
    )
  ]
)

- The 12 V LED strip and the dual-USB step-down converter are connected in parallel downstream of INA219 #1.
- The 5 V output from the step-down converter is completely separate and isolated from the native SMPS 5 V rail.

=== 6.3 Unloaded Channels

The native 5 V and 3.3 V INA219 modules remain fully connected to the I2C bus and their respective rails to provide continuous bus voltage supervision. In the absence of external loads, measured current on these rails shall read approximately zero ($I approx 0 "A"$). No artificial dummy loads shall be added merely to simulate non-zero current.

=== 6.4 Fan Measurement Boundary

The 12 V cooling fan is supplied directly from a separately protected 12 V branch upstream of INA219 #1. Consequently:

$ I_("INA219,12V") = I_("LED") + I_("USB converter input") $

Fan operating current and standby controller consumption are explicitly excluded from INA219 #1 measurements. This measurement boundary shall be clearly documented on all hardware schematics and dashboard metrics.

#v(8pt)

// ============================================================================
// 7. POWER DOMAINS
// ============================================================================

= 7. Power Domains

=== 7.1 Standby Domain

The ATX standby rail (+5VSB) remains energized continuously whenever the power supply AC mains line cord is connected, irrespective of whether the main outputs are enabled or disabled via PS_ON\#.

#tech-figure(
  caption: "Figure 3: Standby (+5VSB) vs. Switched Main DC Power Domain Separation",
  [
    #diagram(
      spacing: (8mm, 6.5mm),
      node-stroke: 0.75pt + rgb("0f172a"),
      node-corner-radius: 0pt,
      node-inset: 3pt,
      
      // Mains Infeed & Isolation (Col 0)
      node((0, 0), [AC Mains Infeed\ & SMPS Stage], width: 26mm),
      
      // Standby Domain (Row -0.8)
      edge((0, 0), (1, -0.8), "-|>", [Permanent], label-size: 6pt),
      node((1, -0.8), [+5VSB Standby\ (Continuous)], width: 26mm, fill: rgb("f8fafc")),
      edge((1, -0.8), (2, -0.8), "-|>"),
      node((2, -0.8), [Filter & 3.3 V\ LDO Regulator], width: 26mm),
      edge((2, -0.8), (3, -0.8), "-|>"),
      node((3, -0.8), [ESP32 Core &\ Sensors Logic], width: 26mm, fill: rgb("f1f5f9")),
      
      // Switched Domain (Row 0.8)
      edge((0, 0), (1, 0.8), "-|>", [Gated Switch], label-size: 6pt),
      node((1, 0.8), [Main DC Rails\ 12 V, 5 V, 3.3 V], width: 26mm),
      edge((1, 0.8), (2, 0.8), "-|>"),
      node((2, 0.8), [INA219 Shunts\ & Branch Fuses], width: 26mm),
      edge((2, 0.8), (3, 0.8), "-|>"),
      node((3, 0.8), [Loads Subsystem\ & 12 V Fan], width: 26mm),
      
      // Feedback line from ESP32 to Switched Gating (Planar non-crossing diagonal)
      edge((3, -0.8), (1, 0.8), "-|>", [PS_ON\# Gating], label-size: 6pt, stroke: 0.75pt + rgb("0f172a")),
    )
  ]
)

#tech-figure(
  caption: "Figure 4: Standby (+5VSB) Power Conditioning and Grounding Schematic",
  [
    #diagram(
      spacing: (14mm, 6mm),
      node-stroke: 0.75pt + rgb("0f172a"),
      node-corner-radius: 0pt,
      node-inset: 3.5pt,
      
      node((0, 0), [ATX SMPS +5VSB\ Standby Terminal], width: 42mm, fill: rgb("f1f5f9")),
      edge((0, 0), (0, 1), "-|>", [Continuous +5 V], label-size: 6.5pt),
      node((0, 1), [Inline Fast-Acting Fuse\ (1.0 A / 250 V Littelfuse)], width: 42mm),
      edge((0, 1), (0, 2), "-|>", [Fused Rail], label-size: 6.5pt),
      node((0, 2), [Bulk Decoupling Filter\ ($100 mu "F"$ Electro. + $0.1 mu "F"$ Cer.)], width: 44mm, fill: rgb("f8fafc")),
      edge((0, 2), (0, 3), "-|>", [Filtered 5 V], label-size: 6.5pt),
      node((0, 3), [ESP32 DevKitC 5V Input Pin\ (AMS1117-3.3 LDO Regulator)], width: 46mm, fill: rgb("f1f5f9")),
      edge((0, 3), (1, 3), "-|>", [3.3 V Logic], label-size: 6.5pt),
      node((1, 3), [Sensors, Logic Bus & Pull-ups\ (INA219, DS18B20, TB6612)], width: 44mm),
      edge((0, 3), (0, 4), "<|-|>", [Direct COM], label-size: 6.5pt),
      node((0, 4), [SMPS Common Ground (COM)\ Single-Point Star Ground], width: 46mm, fill: rgb("f8fafc")),
    )
  ]
)

=== 7.2 Switched Domain

Main 12 V, 5 V, and 3.3 V rails are enabled or disabled simultaneously via the PS_ON\# line. When disabled:
- External loads (LED strip and USB converter) immediately lose power.
- The 12 V cooling fan ceases operation due to absence of motor supply.
- The ESP32 controller, sensor instrumentation, and LittleFS web server remain active on standby power.
- System cooldown occurs via passive natural convection.
- Real-time diagnostic reporting and telemetry upload continue uninterrupted.

=== 7.3 Power Requirements

1. Verify manufacturer nameplate confirms +5VSB is rated for continuous current $>= 1.5 "A"$.
2. Feed power strictly into the ESP32 5 V pin; never feed 5 V directly to the 3.3 V rail.
3. Under no circumstances join the +5VSB standby rail to the main switched 5 V rail.
4. Prevent USB programming cable backfeeding using Schottky diode or MOSFET isolation.
5. Verify brownout immunity during Wi-Fi transmission power spikes ($approx 240 "mA"$).

#pagebreak()

// ============================================================================
// 8. PROPOSED CIRCUIT CONNECTIONS
// ============================================================================

= 8. Proposed Circuit Connections

=== 8.1 GPIO Map

#formal-table(
  columns: (1.5fr, 3.5fr, 2fr),
  table.header([*ESP32 GPIO*], [*Assigned Hardware Function*], [*Signal Logic Standard*]),
  [GPIO21], [I2C Serial Data (SDA) -- INA219 modules & 16x2 LCD], [3.3 V Open-Drain ($4.7 "k"Omega$ Pull-up)],
  [GPIO22], [I2C Serial Clock (SCL) -- INA219 modules & 16x2 LCD], [3.3 V Open-Drain ($4.7 "k"Omega$ Pull-up)],
  [GPIO27], [1-Wire Digital Bus (DQ) -- Two DS18B20 Probes], [3.3 V Open-Drain ($4.7 "k"Omega$ Pull-up)],
  [GPIO25], [TB6612FNG PWMA -- Hardware PWM Speed Modulation], [3.3 V Push-Pull ($25 "kHz"$ PWM)],
  [GPIO26], [TB6612FNG AIN1 -- Motor Direction Control], [3.3 V Logic HIGH (Forward)],
  [GPIO33], [TB6612FNG STBY -- Hardware Driver Bridge Enable], [3.3 V Active-HIGH ($10 "k"Omega$ Pull-down)],
  [GPIO32], [PS_ON\# Transistor Base Control -- 2N3904 NPN Switch], [3.3 V Active-HIGH ($10 "k"Omega$ Base-Emitter Pull-down)],
  [GPIO18], [Main-Output SPST Rocker Switch Input], [3.3 V Active-LOW ($10 "k"Omega$ Pull-up)],
  [GPIO23], [Local-Setup SPST Rocker Switch Input], [3.3 V Active-LOW ($10 "k"Omega$ Pull-up)]
)

=== 8.2 INA219 Logic Connections & Addressing

All three INA219 modules share the same I2C bus:
- *VCC:* Connected to standby-derived 3.3 V rail.
- *GND:* Connected to secondary common ground (COM).
- *SDA / SCL:* Connected in parallel to GPIO21 and GPIO22 with combined effective pull-up $1.8 "k"Omega <= R_"eff" <= 3.3 "k"Omega$.

#formal-table(
  columns: (1.8fr, 2.2fr, 3fr),
  table.header([*Monitored Rail*], [*I2C Address*], [*Address Jumper Configuration*]),
  [12 V External Load], [0x40 (Default)], [A0 = Open, A1 = Open],
  [Native 5 V Rail], [0x41], [A0 = Bridged to VCC, A1 = Open],
  [Native 3.3 V Rail], [0x44], [A0 = Open, A1 = Bridged to VCC]
)

=== 8.3 INA219 Power Paths

#formal-table(
  columns: (1.2fr, 2.8fr, 3fr),
  table.header([*Sensor*], [*VIN+ Connection (Source-Side)*], [*VIN- Connection (Load-Side)*]),
  [#1 (12 V)], [Main 12 V downstream of branch fuse], [LED strip and USB step-down positive infeed],
  [#2 (5 V)], [Main 5 V native output terminal], [Unloaded, insulated terminal post],
  [#3 (3.3 V)], [Main 3.3 V native output terminal], [Unloaded, insulated terminal post]
)

*Important:* VIN- is not ground. The INA219 measures rail voltage between VIN- and COM ground.

=== 8.4 DS18B20 Wiring

Both DS18B20 digital probes operate in non-parasitic mode:
- VDD connected to standby-derived 3.3 V; GND connected to COM.
- Shared DQ data wire connected to GPIO27 with a single $4.7 "k"Omega$ pull-up resistor to 3.3 V.
- Probe 64-bit factory ROM registration is bound during commissioning (CH1: transformer surface; CH2: inlet air).

=== 8.5 Fan Driver (TB6612FNG)

#formal-table(
  columns: (1.8fr, 3.2fr, 2fr),
  table.header([*Terminal*], [*Hardware Electrical Connection*], [*Functional Role*]),
  [VM], [Protected main 12 V branch], [Motor power supply ($>= 10 mu "F"$ Decoupled)],
  [VCC], [Standby-derived 3.3 V rail], [Logic power supply ($0.1 mu "F"$ Decoupled)],
  [GND / PGND], [SMPS Common Ground (COM)], [Single-point reference ground],
  [AO1], [Fan positive terminal wire (+12 V)], [Half-bridge A positive drive],
  [AO2], [Fan negative terminal wire], [Half-bridge A negative sink],
  [AIN1], [ESP32 GPIO26], [Direction logic (Set HIGH)],
  [AIN2], [SMPS Common Ground (COM)], [Direction logic (Tied LOW)],
  [PWMA], [ESP32 GPIO25], [Speed modulation PWM input ($25 "kHz"$)],
  [STBY], [ESP32 GPIO33], [Driver bridge enable ($10 "k"Omega$ Pull-down)]
)

*Wiring Invariant:* Do not connect fan negative (AO2) to COM or chassis ground. In this H-bridge configuration, the motor sink path passes exclusively through terminal AO2.

=== 8.6 PS_ON\# Active-Low Transistor Interface

#tech-figure(
  caption: "Figure 5: Discrete NPN Transistor Pull-Down Interface for ATX PS_ON# Control",
  [
    #diagram(
      spacing: (12mm, 7mm),
      node-stroke: 0.75pt + rgb("0f172a"),
      node-corner-radius: 0pt,
      node-inset: 4pt,
      
      node((0, 0), [ESP32 GPIO32\ (Output Pin)], width: 26mm),
      edge((0, 0), (1, 0), "-|>", [$1 "k"Omega$], label-size: 6.5pt, label-side: left),
      node((1, 0), [2N3904 Base (Pin 2)\ (JCET TO-92)], width: 30mm),
      
      node((1, 1), [$10 "k"Omega$ Pull-Down\ to COM Ground], width: 28mm),
      edge((1, 0), (1, 1), "-"),
      
      node((2, -0.6), [Collector Pin 3 #sym.arrow.r\ SMPS PS_ON\# Wire], width: 32mm),
      edge((1, 0), (2, -0.6), "-"),
      
      node((2, 0.6), [Emitter Pin 1 #sym.arrow.r\ SMPS Common (COM)], width: 32mm),
      edge((1, 0), (2, 0.6), "-"),
    )
  ]
)

#formal-table(
  columns: (1.8fr, 5.2fr),
  table.header([*GPIO32 State*], [*Hardware Electrical Result*]),
  [LOW / High-Z], [Transistor cutoff; PS_ON\# pulled high to +5VSB; *main DC outputs are disabled (OFF)*.],
  [HIGH ($3.3 "V"$)], [Transistor saturated; PS_ON\# pulled low to $< 0.4 "V"$; *main DC outputs are energized (ON)*.]
)

#hazard-box(
  title: "ELECTRICAL HAZARD STATEMENT",
  [PS_ON\# is an active-low supervisory inhibit. Releasing PS_ON\# disables the switched DC outputs (+12 V, +5 V, +3.3 V) but does *not* isolate AC utility line voltage or de-energize the +5VSB standby rail. The SMPS chassis must never be opened or touched without completely removing the AC mains power cord.]
)

=== 8.7 Physical SPST Rocker Switches

#tech-figure(
  caption: "Figure 6: SPST Rocker Switch Input Circuit with Hardware Debounce Filter",
  [
    #diagram(
      spacing: (12mm, 7mm),
      node-stroke: 0.75pt + rgb("0f172a"),
      node-corner-radius: 0pt,
      node-inset: 4pt,
      
      node((0, 0), [Standby 3.3 V Logic], width: 30mm),
      edge((0, 0), (1, 0), "-|>", [$10 "k"Omega$ Pull-up], label-size: 6.5pt),
      node((1, 0), [ESP32 Input Pin\ (GPIO18 / GPIO23)], width: 30mm, fill: rgb("f1f5f9")),
      edge((1, 0), (2, 0), "-"),
      node((2, 0), [SPST Rocker Switch\ (Contact to COM)], width: 32mm),
      edge((2, 0), (2, 1), "-"),
      node((2, 1), [Secondary COM Ground], width: 32mm, fill: rgb("f8fafc")),
    )
  ]
)

#formal-table(
  columns: (1.5fr, 1.8fr, 3.7fr),
  table.header([*Switch*], [*GPIO Wiring*], [*Software Functional Action*]),
  [Main-Output Switch], [GPIO18 to COM when closed], [OFF inhibits operation; OFF #sym.arrow.r ON requests authorized startup.],
  [Setup Switch], [GPIO23 to COM when closed], [Requests local SoftAP provisioning mode upon deliberate closure.]
)

*Safety Invariant:* A maintained ON position of the switch must never bypass software fault lockouts or override a validated remote emergency OFF command.

=== 8.8 16x2 Character LCD Cyclic Real-Time Telemetry Interface

To provide autonomous, zero-latency local operational visibility without requiring a PC, smartphone, or active network connection, the system incorporates an alphanumeric 16#sym.times;2 character LCD driven by an onboard PCF8574 I2C expansion backpack.

==== 8.8.1 I2C Bus Sharing and Logic Voltage Compatibility
- *Bus Integration:* The PCF8574 backpack resides on the primary hardware I2C bus (ESP32 GPIO21 SDA, GPIO22 SCL) alongside the three INA219 power monitors, configured at fixed address `0x27` (or `0x3F`).
- *Voltage Compatibility:* The HD44780 LCD glass and LED backlight require 5.0 V VDD for sharp optical contrast. However, onboard pull-up resistors on commodity PCF8574 modules are tied to 5.0 V. To prevent electrical overstress on the ESP32 GPIO pins ($V_"IH,max" <= 3.6 "V"$), the backpack pull-up resistors to 5 V are removed, allowing the bus lines to be pulled up exclusively to the standby 3.3 V rail via the $4.7 "k"Omega$ resistors on the ESP32 breakout. The PCF8574 reliably registers 3.3 V logic levels with zero bus contention.

==== 8.8.2 Continuous 4-State Cyclic Loop Carousel Architecture
The LCD firmware executes a non-blocking 4-state cyclic carousel that rotates every 3.0 seconds, presenting all critical telemetry and status variables across structured 16#sym.times;2 character layouts:

#formal-table(
  columns: (1.2fr, 2.2fr, 3.6fr),
  table.header([*Screen \#*], [*Display State*], [*Rendered Alphanumeric Format (16#sym.times;2 Characters)*]),
  [Screen 1], [Thermal & Hotspot Status], [
    `T1:48.6C T2:29.4C`    `dT:19.2C HST:53.4C`
  ],
  [Screen 2], [Multi-Rail DC Metrics], [
    `12V: 1.42A 17.1W`    `5V: 5.08V 3V3:3.32V`
  ],
  [Screen 3], [Cooling & Health Index], [
    `FAN: 65% [AUTO] `    `HEALTH HI: 94.2% `
  ],
  [Screen 4], [System State & Faults], [
    `STATE: RUNNING `    `FLT: NONE [OK] `
  ]
)

- *Priority Emergency Override:* If a supervisory fault trip (`THERMAL_TRIP`, `ELEC_LOCKOUT`, `AIRFLOW_STALL`) or emergency shutdown occurs, the cyclic loop is immediately preempted. The LCD locks into a persistent high-contrast alarm screen displaying the latched fault code, trip metric value, and timestamp until acknowledged or manually reset.
- *Non-Blocking Rendering:* LCD string formatting and I2C transmission occur via a periodic FreeRTOS software timer task, ensuring zero blocking or jitter in the $50 "ms"$ protective supervision loop.

=== 8.9 Wiring and Decoupling Best Practices

1. All high-current connections ($>= 2 "A"$) use 18 AWG copper conductors; low-current logic uses 24 AWG ribbon wire.
2. Local $10 mu "F"$ electrolytic bulk decoupling and $0.1 mu "F"$ high-frequency ceramic capacitors are placed adjacent to the TB6612FNG driver and INA219 logic pins.
3. Star grounding topology connects all logic and sensor grounds to a single physical terminal on the SMPS secondary side. Never route high-current motor or LED return currents through sensor breadboard jumpers.


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
  [Power Manager], [Coordinates state machine transitions, inrush blanking timers, and PS_ON\# gating.],
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

- *Overcurrent Action:* If measured current exceeds $I_"trip"$ for $>= 250 "ms"$, GPIO32 is immediately pulled LOW ($< 5 "ms"$), de-asserting PS_ON\# and latching `ELECTRICAL_LOCKOUT`.
- *Voltage Boundary Anomaly:* If rail voltage leaves the permissible window following startup, an electrical fault is declared.
- *I2C Bus Communication Loss:* Telemetry timeout $> 500 "ms"$ triggers immediate supervisory shutdown (`SENSOR_LOCKOUT`).

=== 11.3 State-Aware Supervision and Inrush Blanking

- During intentional OFF (`STANDBY_OFF`), low voltage on main switched rails is expected and must not generate nuisance undervoltage faults.
- Upon assertion of PS_ON\# (startup), an inrush blanking window ($500 "ms"$) inhibits false undervoltage/overcurrent trips while output decoupling capacitors charge. Gross short circuits ($I > 200% I_"trip"$) remain actionable immediately.

=== 11.4 Shutdown Verification Gate

When a supervisory trip occurs:
1. De-assert GPIO32 (releasing PS_ON\# to pull high).
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
  [Firebase Hosting], [Unified web dashboard hosting with direct CLI deployment, Firebase Authentication, and Realtime Database integration without exposing the private source repository.],
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
      node((2, 0), [Operator Browser\ Web App (Firebase Hosting)], width: 30mm),
      
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
3. Upon ingestion, the controller verifies command ID uniqueness and expiry, de-asserts GPIO32, releases PS_ON\#, confirms rail voltage decay, and writes an execution acknowledgment record.
4. *Safety Delimitation:* Remote re-energization (Remote ON) is explicitly prohibited within this baseline design.


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
  [Web Hosting Tier], [Firebase Hosting (Unified SPA)], [Local ESP32 Web Server Only: Limits global remote monitoring; Firebase Hosting provides globally distributed zero-cost CDN hosting with zero maintenance.],
  [Fan Speed Modulation], [TB6612FNG Dual H-Bridge], [Single Low-Side N-MOSFET: TB6612FNG integrates shoot-through protection, reverse flyback diodes, thermal shutdown, and logic-level 3.3 V gates.],
  [Supervisory Inhibit], [Active-Low NPN Switch on PS_ON\#], [Direct Mechanical AC Relay: AC switching introduces dangerous inductive arcs and requires high coil drive power; PS_ON\# is native, low-power, and safe.]
)

#v(8pt)

// ============================================================================
// 21. FUTURE INDEPENDENT BRANCH / RAIL SWITCHING
// ============================================================================

= 21. Future Independent Branch / Rail Switching

=== 21.1 Architectural Scope Delimitation

In the baseline Version 3.0 implementation, supervisory shutdown acts globally via the ATX PS_ON\# line, which disables all switched DC outputs (12 V, 5 V, 3.3 V) simultaneously. While effective, a localized overcurrent event on a single branch (such as an LED strip short) currently interrupts all operational rails.

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
  [Phase 3: PS_ON\# Gating Interface], [Verify 2N3904 transistor switching and SMPS main rail startup and shutdown response.], [GPIO32 HIGH asserts PS_ON\# ($< 0.4 "V"$); GPIO32 LOW releases PS_ON\# ($> 4.5 "V"$).], [PASS],
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
7. *Default-Safe Pin State:* Verify that ESP32 firmware initializes GPIO32 (PS_ON\# drive) to LOW / High-Z prior to executing any peripheral configuration.
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
      node((2, 0.3), [TB6612 Fan Driver\ 2N3904 PS_ON\# Switch], width: 28mm),
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
      node((1, 1), [2N3904 NPN Switch\ ($1 "k"Omega$ / $10 "k"Omega$)], width: 28mm),
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
        #text(size: 8.5pt)[*Role:* Lead Systems & Embedded Hardware Engineer]        #v(2pt)
        #text(size: 8.5pt)[*Discipline:* Power Electronics & Embedded Systems]        #v(2pt)
        #text(size: 8.5pt)[*Scope:* Circuit Interfaces, Power Isolation, Wiring Topology]        #v(2pt)
        #text(size: 8.5pt)[*Baseline Status:* Approved for Prototype Assembly]        #v(2pt)
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
        #text(size: 8.5pt)[*Role:* Senior Embedded Firmware & Cloud Architect]        #v(2pt)
        #text(size: 8.5pt)[*Discipline:* Real-Time Control & Distributed IoT Systems]        #v(2pt)
        #text(size: 8.5pt)[*Scope:* Predictive Algorithms, Protection Logic, Cloud APIs]        #v(2pt)
        #text(size: 8.5pt)[*Baseline Status:* Approved for Firmware Release 1.0]        #v(2pt)
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
