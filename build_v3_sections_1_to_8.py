# -*- coding: utf-8 -*-
"""
Sections 1 to 8 of Document Version 3.0:
Document Information, Abstract, Objectives, System Architecture,
Hardware & Procurement Status, Measurement & Load Arrangement,
Power Domains, and Proposed Circuit Connections.
"""

def get_sections_1_to_8():
    return '''
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

An ESP32 microcontroller processes all sensor measurements locally, predicts near-term temperature rise through numerical trend extrapolation, and modulates a two-wire fan through a Toshiba TB6612FNG dual-bridge driver. The controller requests emergency supervisory shutdown of all main outputs via the ATX PS_ON\\# active-low interface when validated thermal or electrical trip conditions occur.

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
- Individual branch load disconnection (all main outputs are interrupted together via PS_ON\\#).
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
      node((2, 0.8), [BC547 NPN Switch\ #sym.arrow.r PS_ON\\# Pull-Down], width: 28mm),
      node((2, 1.8), [Firebase RTDB\ `/latest`, `/events`], width: 28mm, fill: rgb("f8fafc")),
      
      // Col 3: Cloud Dashboards & Alerts (x = 3)
      node((3, 1.3), [Firebase Hosting\ SPA Dashboard], width: 28mm),
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
  [Q1], [BC547 NPN BJT], [TO-92, 45 V, 100 mA, $h_(F E) >= 110$], [1], [PS_ON\# Interface],
  [SW1--SW2], [Miniature SPST Rockers], [2-pin panel mount, contact rated 250V/3A], [2], [Manual UI Controls],
  [F1--F4], [Fast-Acting Cartridge Fuses], [5x20 mm glass, 1.0 A (+5VSB), 3.15 A (12V)], [4], [Circuit Protection],
  [PASS], [Passive Components Assortment], [Metal film resistors (4.7k, 10k, 100k), caps], [1 set], [Signal / Filter]
)

=== 5.2 Component Technical Allocations

1. *Core Microcontroller (ESP32-WROOM-32):* Operates as the central embedded controller executing real-time digital filtering, least-squares thermal trend estimation, multi-rail protection supervision, and local web serving.
2. *Thermal Sensors (DS18B20):* TS1 is mechanically coupled to the SMPS main transformer core wrapper with thermally conductive paste and Kapton insulation; TS2 is suspended in the chassis intake duct for ambient reference.
3. *Power Telemetry (INA219):* Three shunt sensors monitor rail voltages and currents over a shared I2C bus with hardware jumper-selected addresses (`0x40`, `0x41`, `0x44`).
4. *Thermal Actuator (TB6612FNG):* Provides high-frequency ($25 "kHz"$) PWM speed control for the 12 V cooling fan without audible switching noise or electrical motor stalling.
5. *Supervisory Inhibit Switch (BC547):* Sinks the ATX PS_ON\\# wire to COM ground during active operation; de-energizing its base immediately trips all main DC rails to high-Z.

=== 5.3 Prototyping Substrate and Interconnect Standards

- *Prototyping Substrate:* High-grade single-sided copper prototyping Vero-boards ($90 times 150 "mm"$) with dedicated common bus power distribution.
- *Interconnect Cabling:* 18 AWG stranded copper wire for all primary DC rails and high-current fan/load loops; 24 AWG ribbon wire for 1-Wire, I2C, and logic control signals.
- *Insulation & Mechanical Mounting:* Polyolefin flame-retardant heat-shrink sleeving across all exposed high-voltage and DC terminal junctions; thermal adhesive / silicone mounting for DS18B20 core surface coupling.
- *Bench Supply Integration:* Standard desktop SMPS with verified continuous +5VSB rating ($>= 1.5 "A"$) and active-low PS_ON\\# wire. The internal fan is audited prior to connection to ensure inrush and operating current remain safely within the TB6612FNG $1.2 "A"$ rating.

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

The ATX standby rail (+5VSB) remains energized continuously whenever the power supply AC mains line cord is connected, irrespective of whether the main outputs are enabled or disabled via PS_ON\\#.

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

Main 12 V, 5 V, and 3.3 V rails are enabled or disabled simultaneously via the PS_ON\\# line. When disabled:
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
  [GPIO32], [PS_ON\\# Transistor Base Control -- BC547 NPN Switch], [3.3 V Active-HIGH ($100 "k"Omega$ Pull-down)],
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

=== 8.6 PS_ON\\# Active-Low Transistor Interface

#tech-figure(
  caption: "Figure 5: Discrete NPN Transistor Pull-Down Interface for ATX PS_ON# Control",
  [
    #diagram(
      spacing: (12mm, 7mm),
      node-stroke: 0.75pt + rgb("0f172a"),
      node-corner-radius: 0pt,
      node-inset: 4pt,
      
      node((0, 0), [ESP32 GPIO32\ (Output Pin)], width: 26mm),
      edge((0, 0), (1, 0), "-|>", [$4.7 "k"Omega$], label-size: 6.5pt, label-side: left),
      node((1, 0), [BC547 NPN Base\ (TO-92 Package)], width: 30mm),
      
      node((1, 1), [$100 "k"Omega$ Bleed\ to COM Ground], width: 28mm),
      edge((1, 0), (1, 1), "-"),
      
      node((2, -0.6), [Collector Pin #sym.arrow.r\ SMPS PS_ON\# Wire], width: 32mm),
      edge((1, 0), (2, -0.6), "-"),
      
      node((2, 0.6), [Emitter Pin #sym.arrow.r\ SMPS Common (COM)], width: 32mm),
      edge((1, 0), (2, 0.6), "-"),
    )
  ]
)

#formal-table(
  columns: (1.8fr, 5.2fr),
  table.header([*GPIO32 State*], [*Hardware Electrical Result*]),
  [LOW / High-Z], [Transistor cutoff; PS_ON\\# pulled high to +5VSB; *main DC outputs are disabled (OFF)*.],
  [HIGH ($3.3 "V"$)], [Transistor saturated; PS_ON\\# pulled low to $< 0.4 "V"$; *main DC outputs are energized (ON)*.]
)

#hazard-box(
  title: "ELECTRICAL HAZARD STATEMENT",
  [PS_ON\\# is an active-low supervisory inhibit. Releasing PS_ON\\# disables the switched DC outputs (+12 V, +5 V, +3.3 V) but does *not* isolate AC utility line voltage or de-energize the +5VSB standby rail. The SMPS chassis must never be opened or touched without completely removing the AC mains power cord.]
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
  table.header([*Screen \\#*], [*Display State*], [*Rendered Alphanumeric Format (16#sym.times;2 Characters)*]),
  [Screen 1], [Thermal & Hotspot Status], [
    `T1:48.6C T2:29.4C`\
    `dT:19.2C HST:53.4C`
  ],
  [Screen 2], [Multi-Rail DC Metrics], [
    `12V: 1.42A 17.1W`\
    `5V: 5.08V 3V3:3.32V`
  ],
  [Screen 3], [Cooling & Health Index], [
    `FAN: 65% [AUTO] `\
    `HEALTH HI: 94.2% `
  ],
  [Screen 4], [System State & Faults], [
    `STATE: RUNNING `\
    `FLT: NONE [OK] `
  ]
)

- *Priority Emergency Override:* If a supervisory fault trip (`THERMAL_TRIP`, `ELEC_LOCKOUT`, `AIRFLOW_STALL`) or emergency shutdown occurs, the cyclic loop is immediately preempted. The LCD locks into a persistent high-contrast alarm screen displaying the latched fault code, trip metric value, and timestamp until acknowledged or manually reset.
- *Non-Blocking Rendering:* LCD string formatting and I2C transmission occur via a periodic FreeRTOS software timer task, ensuring zero blocking or jitter in the $50 "ms"$ protective supervision loop.

=== 8.9 Wiring and Decoupling Best Practices

1. All high-current connections ($>= 2 "A"$) use 18 AWG copper conductors; low-current logic uses 24 AWG ribbon wire.
2. Local $10 mu "F"$ electrolytic bulk decoupling and $0.1 mu "F"$ high-frequency ceramic capacitors are placed adjacent to the TB6612FNG driver and INA219 logic pins.
3. Star grounding topology connects all logic and sensor grounds to a single physical terminal on the SMPS secondary side. Never route high-current motor or LED return currents through sensor breadboard jumpers.
'''
