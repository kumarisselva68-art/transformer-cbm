# -*- coding: utf-8 -*-
"""
Diagram 4 Generator: Hardware Operational State Machine Flowchart (Rev 2 - Zero Wire Crossings)
Covers all 10 states from Specification Section 7:
1. STANDBY_OFF
2. STARTING (Inrush blanking)
3. RUNNING (Normal operation)
4. MANUAL_OFF
5. ELEC_LOCKOUT
6. BUS_LOCKOUT
7. THERMAL_COOL (Qualified auto-recovery cooldown)
8. RECOVERY_TEST (Supervised restart window)
9. THERMAL_LOCK (Permanent thermal lockout)
10. CONTROL_PATH_FAILURE
"""

import os
import subprocess

def generate_diagram_4():
    w = 2400
    h = 1500

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <defs>
    <pattern id="grid" width="25" height="25" patternUnits="userSpaceOnUse">
      <path d="M 25 0 L 0 0 0 25" fill="none" stroke="#e2e8f0" stroke-width="0.75"/>
    </pattern>
    <filter id="shadow" x="-3%" y="-3%" width="108%" height="110%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="2" dy="4" stdDeviation="5" flood-color="#0f172a" flood-opacity="0.08"/>
    </filter>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#0f172a"/>
    </marker>
    <marker id="arrow-green" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#059669"/>
    </marker>
    <marker id="arrow-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#0284c7"/>
    </marker>
    <marker id="arrow-red" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#dc2626"/>
    </marker>
    <marker id="arrow-orange" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#ea580c"/>
    </marker>
    <marker id="arrow-purple" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#9333ea"/>
    </marker>
  </defs>

  <style>
    text {{
      font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, 'Inter', Roboto, sans-serif;
      user-select: none;
    }}
    .wire {{
      fill: none;
      stroke-linecap: round;
      stroke-linejoin: round;
    }}
  </style>

  <!-- Background Surface -->
  <rect width="{w}" height="{h}" fill="#f8fafc"/>
  <rect width="{w}" height="{h}" fill="url(#grid)"/>

  <!-- ==================== HEADER ==================== -->
  <g transform="translate(60, 48)">
    <text font-size="32" font-weight="900" fill="#0f172a" letter-spacing="-0.5px">IoT Transformer Condition Monitoring System — Hardware Operational Flowchart</text>
    <text font-size="17" font-weight="700" fill="#64748b" y="28">10-State Supervisory Transition Engine, Inrush Blanking, Multi-Tier Fault Cutoffs &amp; Qualified Auto-Recovery</text>
  </g>

  <!-- ==================== COLUMN 1: NORMAL OPERATIONAL SPINE (x = 80 to 520, center = 300) ==================== -->

  <!-- STATE 0: STANDBY_OFF -->
  <g transform="translate(80, 110)" filter="url(#shadow)">
    <rect width="440" height="155" rx="10" fill="#ffffff" stroke="#059669" stroke-width="2.5"/>
    <rect width="440" height="34" rx="10" fill="#059669"/>
    <rect x="0" y="24" width="440" height="10" fill="#059669"/>
    <text x="16" y="24" font-size="16" font-weight="900" fill="#ffffff">STATE 0: STANDBY_OFF (IDLE SUPERVISION)</text>
    <text x="16" y="56" font-size="13.5" font-weight="700" fill="#065f46">• Standby +5VSB active: ESP32, 16x2 LCD &amp; sensors fully powered</text>
    <text x="16" y="78" font-size="13.5" font-weight="600" fill="#334155">• ATX main rails (12V, 5V, 3.3V) DE-ENERGIZED; Dummy Load OFF</text>
    <text x="16" y="100" font-size="13.5" font-weight="600" fill="#334155">• PS_ON# pulled HIGH (2N3904 Q1 base LOW via 10k pull-down)</text>
    <text x="16" y="122" font-size="13.5" font-weight="600" fill="#334155">• LCD displays "SYSTEM: STANDBY" • Sensors polled at 1 Hz</text>
    <text x="16" y="142" font-size="12.5" font-weight="700" fill="#0284c7">Awaiting operator run switch closure OR cloud start command</text>
  </g>

  <!-- Arrow State 0 -> Decision 1 -->
  <path class="wire" stroke="#0f172a" stroke-width="3" marker-end="url(#arrow)" d="M 300 265 L 300 310"/>

  <!-- DECISION 1: START REQUEST & PRE-FLIGHT CHECK -->
  <g transform="translate(140, 310)" filter="url(#shadow)">
    <polygon points="160,0 320,50 160,100 0,50" fill="#eff6ff" stroke="#2563eb" stroke-width="2"/>
    <text x="160" y="42" font-size="14" font-weight="900" fill="#1e40af" text-anchor="middle">START REQUEST?</text>
    <text x="160" y="62" font-size="11.5" font-weight="700" fill="#3b82f6" text-anchor="middle">GPIO 18 ON &amp; T_core &lt; 50°C</text>
  </g>

  <!-- Decision 1 NO loopback to State 0 -->
  <path class="wire" stroke="#64748b" stroke-width="2.5" marker-end="url(#arrow)" d="M 140 360 L 50 360 L 50 185 L 80 185"/>
  <rect x="58" y="345" width="30" height="20" rx="3" fill="#ffffff" stroke="#94a3b8" stroke-width="1"/>
  <text x="73" y="359" font-size="11" font-weight="800" fill="#64748b" text-anchor="middle">NO</text>

  <!-- Decision 1 YES to State 1 -->
  <path class="wire" stroke="#059669" stroke-width="3" marker-end="url(#arrow-green)" d="M 300 410 L 300 455"/>
  <rect x="306" y="420" width="32" height="20" rx="3" fill="#ffffff" stroke="#059669" stroke-width="1"/>
  <text x="322" y="434" font-size="11" font-weight="800" fill="#059669" text-anchor="middle">YES</text>

  <!-- STATE 1: STARTING (INRUSH BLANKING) -->
  <g transform="translate(80, 455)" filter="url(#shadow)">
    <rect width="440" height="150" rx="10" fill="#ffffff" stroke="#0284c7" stroke-width="2.5"/>
    <rect width="440" height="34" rx="10" fill="#0284c7"/>
    <rect x="0" y="24" width="440" height="10" fill="#0284c7"/>
    <text x="16" y="24" font-size="16" font-weight="900" fill="#ffffff">STATE 1: STARTING (INRUSH BLANKING)</text>
    <text x="16" y="56" font-size="13.5" font-weight="700" fill="#0369a1">• Assert GPIO 32 HIGH: 2N3904 saturates, pulling PS_ON# to GND</text>
    <text x="16" y="78" font-size="13.5" font-weight="600" fill="#334155">• ATX main inverter ignites; +12V, +5V, +3.3V power rails spin up</text>
    <text x="16" y="100" font-size="13.5" font-weight="700" fill="#ea580c">• 500 ms Inrush Blanking Window: Current spikes suppressed</text>
    <text x="16" y="122" font-size="13.5" font-weight="600" fill="#334155">• INA219 high-speed bus voltage qualification check</text>
    <text x="16" y="140" font-size="12" font-weight="600" fill="#475569">If rails fail to reach nominal threshold within 500 ms -> trip fault</text>
  </g>

  <!-- Arrow State 1 -> Decision 2 -->
  <path class="wire" stroke="#0f172a" stroke-width="3" marker-end="url(#arrow)" d="M 300 605 L 300 650"/>

  <!-- DECISION 2: RAILS NOMINAL AFTER 500ms? -->
  <g transform="translate(130, 650)" filter="url(#shadow)">
    <polygon points="170,0 340,50 170,100 0,50" fill="#f0fdf4" stroke="#16a34a" stroke-width="2"/>
    <text x="170" y="42" font-size="14" font-weight="900" fill="#15803d" text-anchor="middle">RAILS NOMINAL?</text>
    <text x="170" y="62" font-size="11.5" font-weight="700" fill="#16a34a" text-anchor="middle">12V &gt; 11.2V | 5V &gt; 4.65V | 3.3V &gt; 3.05V</text>
  </g>

  <!-- Decision 2 NO to State 9 (Control Path Failure) -->
  <path class="wire" stroke="#dc2626" stroke-width="3" marker-end="url(#arrow-red)" d="M 470 700 L 610 700"/>
  <rect x="520" y="688" width="32" height="22" rx="3" fill="#ffffff" stroke="#dc2626" stroke-width="1"/>
  <text x="536" y="703" font-size="11" font-weight="800" fill="#dc2626" text-anchor="middle">NO</text>

  <!-- Decision 2 YES to State 2 -->
  <path class="wire" stroke="#059669" stroke-width="3" marker-end="url(#arrow-green)" d="M 300 750 L 300 795"/>
  <rect x="306" y="760" width="32" height="20" rx="3" fill="#ffffff" stroke="#059669" stroke-width="1"/>
  <text x="322" y="774" font-size="11" font-weight="800" fill="#059669" text-anchor="middle">YES</text>

  <!-- STATE 2: RUNNING (NORMAL CLOSED-LOOP OPERATION) -->
  <g transform="translate(80, 795)" filter="url(#shadow)">
    <rect width="440" height="200" rx="10" fill="#ffffff" stroke="#059669" stroke-width="3"/>
    <rect width="440" height="36" rx="10" fill="#059669"/>
    <rect x="0" y="26" width="440" height="10" fill="#059669"/>
    <text x="16" y="25" font-size="16.5" font-weight="900" fill="#ffffff">STATE 2: RUNNING (CLOSED-LOOP REGULATION)</text>
    <text x="16" y="58" font-size="13.5" font-weight="700" fill="#065f46">• 12V 50W Dummy Load Energized: 12.0V • 1.20A (14.4W loading)</text>
    <text x="16" y="80" font-size="13.5" font-weight="600" fill="#334155">• Continuous 1.00s Real-Time Polling: 3x INA219 + 2x DS18B20</text>
    <text x="16" y="102" font-size="13.5" font-weight="700" fill="#2563eb">• Predictive Fan PWM: Dual demand max(g(T_f), g(T_p)) to TB6612</text>
    <text x="16" y="124" font-size="13.5" font-weight="600" fill="#334155">• 10s HTTPS Telemetry Sync: Pushes metrics to Firebase RTDB</text>
    <text x="16" y="146" font-size="13.5" font-weight="600" fill="#334155">• 16x2 LCD Cycler: Screen 1 (Temperatures) &lt;--&gt; Screen 2 (Status)</text>
    <text x="16" y="168" font-size="13.5" font-weight="700" fill="#059669">• Cloud Watchdog Heartbeat: Refreshed every 10 seconds</text>
    <text x="16" y="188" font-size="12" font-weight="600" fill="#475569">Safety invariants evaluate electrical &amp; thermal criteria every tick</text>
  </g>

  <!-- Arrow State 2 -> Decision 3 (Operator Stop) -->
  <path class="wire" stroke="#0f172a" stroke-width="3" marker-end="url(#arrow)" d="M 300 995 L 300 1045"/>

  <!-- DECISION 3: OPERATOR STOP REQUEST? -->
  <g transform="translate(150, 1045)" filter="url(#shadow)">
    <polygon points="150,0 300,45 150,90 0,45" fill="#f8fafc" stroke="#64748b" stroke-width="2"/>
    <text x="150" y="38" font-size="13.5" font-weight="900" fill="#1e293b" text-anchor="middle">STOP REQUEST?</text>
    <text x="150" y="58" font-size="11.5" font-weight="700" fill="#64748b" text-anchor="middle">GPIO 18 OFF OR Cloud Stop</text>
  </g>

  <!-- Decision 3 YES to State 3 (Manual Off) -->
  <path class="wire" stroke="#059669" stroke-width="3" marker-end="url(#arrow-green)" d="M 300 1135 L 300 1180"/>
  <rect x="306" y="1145" width="32" height="20" rx="3" fill="#ffffff" stroke="#059669" stroke-width="1"/>
  <text x="322" y="1159" font-size="11" font-weight="800" fill="#059669" text-anchor="middle">YES</text>

  <!-- STATE 3: MANUAL_OFF (GRACEFUL SHUTDOWN) -->
  <g transform="translate(80, 1180)" filter="url(#shadow)">
    <rect width="440" height="150" rx="10" fill="#ffffff" stroke="#475569" stroke-width="2.5"/>
    <rect width="440" height="34" rx="10" fill="#475569"/>
    <rect x="0" y="24" width="440" height="10" fill="#475569"/>
    <text x="16" y="24" font-size="16" font-weight="900" fill="#ffffff">STATE 3: MANUAL_OFF (GRACEFUL DE-ENERGIZATION)</text>
    <text x="16" y="56" font-size="13.5" font-weight="700" fill="#1e293b">• Controlled shutdown initiated by operator switch or authorized cloud stop</text>
    <text x="16" y="78" font-size="13.5" font-weight="600" fill="#334155">• Fast Cutoff: GPIO 32 driven LOW (&lt; 5 ms); PS_ON# releases to 5V</text>
    <text x="16" y="100" font-size="13.5" font-weight="600" fill="#334155">• ATX main power rails drop to 0V; dummy load de-energized safely</text>
    <text x="16" y="122" font-size="13.5" font-weight="600" fill="#334155">• Graceful event logged to NVS &amp; published to Firebase RTDB</text>
    <text x="16" y="140" font-size="12" font-weight="700" fill="#059669">Returns cleanly to STATE 0: STANDBY_OFF</text>
  </g>

  <!-- Loopback from State 3 to State 0 via left corridor (x=35) -->
  <path class="wire" stroke="#475569" stroke-width="2.5" marker-end="url(#arrow)"
        d="M 80 1255 L 35 1255 L 35 140 L 80 140"/>
  <rect x="18" y="680" width="34" height="22" rx="3" fill="#ffffff" stroke="#475569" stroke-width="1"/>
  <text x="35" y="695" font-size="10.5" font-weight="800" fill="#475569" text-anchor="middle">LOOP</text>


  <!-- ==================== SUPERVISORY SAFETY BUS OUT OF RUNNING ==================== -->
  <path class="wire" stroke="#dc2626" stroke-width="3" d="M 520 895 L 610 895"/>
  <rect x="525" y="878" width="75" height="20" rx="3" fill="#fef2f2" stroke="#dc2626" stroke-width="1"/>
  <text x="562" y="892" font-size="10.5" font-weight="900" fill="#dc2626" text-anchor="middle">FAULT DETECT</text>


  <!-- ==================== COLUMN 2: HARDWARE FAULTS & LOCKOUT (center = 810) ==================== -->

  <!-- STATE 9: CONTROL_PATH_FAILURE (Compact: y = 570 to 710, height 140) -->
  <g transform="translate(610, 570)" filter="url(#shadow)">
    <rect width="400" height="140" rx="10" fill="#ffffff" stroke="#dc2626" stroke-width="2.5"/>
    <rect width="400" height="32" rx="10" fill="#dc2626"/>
    <rect x="0" y="22" width="400" height="10" fill="#dc2626"/>
    <text x="16" y="22" font-size="15.5" font-weight="900" fill="#ffffff">STATE 9: CONTROL_PATH_FAILURE</text>
    <text x="16" y="52" font-size="13" font-weight="700" fill="#b91c1c">• Rails failed to rise despite GPIO 32 HIGH (or stuck rail detected)</text>
    <text x="16" y="72" font-size="13" font-weight="600" fill="#334155">• Incongruence between MCU command pin &amp; physical ATX rail reality</text>
    <text x="16" y="92" font-size="13" font-weight="700" fill="#dc2626">• Immediate failsafe: GPIO 32 forced LOW; LCD: "CTRL PATH FAIL"</text>
    <text x="16" y="112" font-size="13" font-weight="600" fill="#334155">• Dispatches critical hardware incident to Firebase &amp; Brevo API</text>
    <text x="16" y="130" font-size="11.5" font-weight="700" fill="#b91c1c">Permanent hardware lockout: Requires AC mains inspection</text>
  </g>

  <!-- FAULT GATE 1: OVERCURRENT DECISION -->
  <g transform="translate(640, 855)" filter="url(#shadow)">
    <polygon points="170,0 340,40 170,80 0,40" fill="#fef2f2" stroke="#dc2626" stroke-width="2"/>
    <text x="170" y="34" font-size="13.5" font-weight="900" fill="#991b1b" text-anchor="middle">OVERCURRENT TRIP?</text>
    <text x="170" y="54" font-size="11.5" font-weight="700" fill="#dc2626" text-anchor="middle">12V &gt; 3.15A | 5V &gt; 1A | 3.3V &gt; 1A</text>
  </g>

  <!-- Bus line to Overcurrent Decision -->
  <path class="wire" stroke="#dc2626" stroke-width="3" marker-end="url(#arrow-red)" d="M 610 895 L 640 895"/>

  <!-- Decision Overcurrent YES -> State 4 -->
  <path class="wire" stroke="#dc2626" stroke-width="3" marker-end="url(#arrow-red)" d="M 810 935 L 810 995"/>
  <rect x="816" y="955" width="32" height="20" rx="3" fill="#ffffff" stroke="#dc2626" stroke-width="1"/>
  <text x="832" y="969" font-size="11" font-weight="800" fill="#dc2626" text-anchor="middle">YES</text>

  <!-- STATE 4: ELEC_LOCKOUT (PERMANENT ELECTRICAL TRIP) -->
  <g transform="translate(610, 995)" filter="url(#shadow)">
    <rect width="400" height="175" rx="10" fill="#ffffff" stroke="#b91c1c" stroke-width="2.5"/>
    <rect width="400" height="34" rx="10" fill="#b91c1c"/>
    <rect x="0" y="24" width="400" height="10" fill="#b91c1c"/>
    <text x="16" y="24" font-size="15.5" font-weight="900" fill="#ffffff">STATE 4: ELEC_LOCKOUT (PERMANENT)</text>
    <text x="16" y="56" font-size="13" font-weight="700" fill="#991b1b">• Hard limit exceeded: Instant cutoff in &lt; 5 ms (GPIO 32 LOW)</text>
    <text x="16" y="78" font-size="13" font-weight="600" fill="#334155">• ATX main rails collapse immediately; removes all power from fault</text>
    <text x="16" y="100" font-size="13" font-weight="700" fill="#dc2626">• Fault snapshot latched to ESP32 NVS non-volatile flash</text>
    <text x="16" y="122" font-size="13" font-weight="600" fill="#334155">• LCD displays "FAULT: OVERCURRENT" • Cloud email alert sent</text>
    <text x="16" y="142" font-size="13" font-weight="700" fill="#7f1d1d">• Automatic restart STRICTLY FORBIDDEN by firmware invariant</text>
    <text x="16" y="162" font-size="12" font-weight="700" fill="#b91c1c">Requires physical switch reset OR authenticated cloud unlock</text>
  </g>


  <!-- ==================== COLUMN 3: SENSOR BUS & COMMUNICATIONS (center = 1260) ==================== -->

  <!-- Overcurrent NO -> Pass to Sensor Bus Decision -->
  <path class="wire" stroke="#64748b" stroke-width="3" marker-end="url(#arrow)" d="M 980 895 L 1090 895"/>
  <rect x="1005" y="883" width="28" height="20" rx="3" fill="#ffffff" stroke="#94a3b8" stroke-width="1"/>
  <text x="1019" y="897" font-size="11" font-weight="800" fill="#64748b" text-anchor="middle">NO</text>

  <!-- FAULT GATE 2: SENSOR BUS DECISION -->
  <g transform="translate(1090, 855)" filter="url(#shadow)">
    <polygon points="170,0 340,40 170,80 0,40" fill="#fffbeb" stroke="#d97706" stroke-width="2"/>
    <text x="170" y="34" font-size="13.5" font-weight="900" fill="#92400e" text-anchor="middle">SENSOR BUS FAULT?</text>
    <text x="170" y="54" font-size="11.5" font-weight="700" fill="#b45309" text-anchor="middle">I2C Timeout &gt; 500ms | CRC Fail &gt; 3x</text>
  </g>

  <!-- Sensor Bus YES -> State 5 -->
  <path class="wire" stroke="#d97706" stroke-width="3" marker-end="url(#arrow-orange)" d="M 1260 935 L 1260 995"/>
  <rect x="1266" y="955" width="32" height="20" rx="3" fill="#ffffff" stroke="#d97706" stroke-width="1"/>
  <text x="1282" y="969" font-size="11" font-weight="800" fill="#d97706" text-anchor="middle">YES</text>

  <!-- STATE 5: BUS_LOCKOUT (SENSOR INTEGRITY FAIL) -->
  <g transform="translate(1060, 995)" filter="url(#shadow)">
    <rect width="400" height="175" rx="10" fill="#ffffff" stroke="#d97706" stroke-width="2.5"/>
    <rect width="400" height="34" rx="10" fill="#d97706"/>
    <rect x="0" y="24" width="400" height="10" fill="#d97706"/>
    <text x="16" y="24" font-size="15.5" font-weight="900" fill="#ffffff">STATE 5: BUS_LOCKOUT (COMM FAULT)</text>
    <text x="16" y="56" font-size="13" font-weight="700" fill="#b45309">• Blind-spot prevention: Cutoff asserted if telemetry is unverified</text>
    <text x="16" y="78" font-size="13.5" font-weight="600" fill="#334155">• I2C SDA/SCL bus hanging or DS18B20 1-Wire CRC check failed</text>
    <text x="16" y="100" font-size="13.5" font-weight="700" fill="#d97706">• GPIO 32 driven LOW; ATX main rails de-energized safely</text>
    <text x="16" y="122" font-size="13.5" font-weight="600" fill="#334155">• LCD displays "FAULT: SENSOR COMM" • Telemetry pushes alert</text>
    <text x="16" y="142" font-size="13.5" font-weight="600" fill="#334155">• Bus recovery attempt: Generates 9 I2C clock pulses on GPIO 22</text>
    <text x="16" y="162" font-size="12" font-weight="700" fill="#92400e">Auto-clears only if sensor communication restores cleanly</text>
  </g>


  <!-- ==================== COLUMN 4: THERMAL SUPERVISION & AUTO-RECOVERY (center = 1720) ==================== -->

  <!-- Sensor Bus NO -> Pass to Thermal Gate -->
  <path class="wire" stroke="#64748b" stroke-width="3" marker-end="url(#arrow)" d="M 1430 895 L 1540 895"/>
  <rect x="1455" y="883" width="28" height="20" rx="3" fill="#ffffff" stroke="#94a3b8" stroke-width="1"/>
  <text x="1469" y="897" font-size="11" font-weight="800" fill="#64748b" text-anchor="middle">NO</text>

  <!-- FAULT GATE 3: THERMAL OVERTEMP DECISION -->
  <g transform="translate(1540, 850)" filter="url(#shadow)">
    <polygon points="180,0 360,45 180,90 0,45" fill="#fef2f2" stroke="#ea580c" stroke-width="2"/>
    <text x="180" y="38" font-size="13.5" font-weight="900" fill="#9a3412" text-anchor="middle">THERMAL OVERTEMP TRIP?</text>
    <text x="180" y="58" font-size="11.5" font-weight="700" fill="#ea580c" text-anchor="middle">T_core ≥ 65°C OR T_p ≥ 70°C</text>
  </g>

  <!-- Thermal Gate NO -> Loop back to RUNNING via completely open horizontal floor at y=760 (Below State 9 which ends at 710) -->
  <path class="wire" stroke="#059669" stroke-width="2.5" marker-end="url(#arrow-green)"
        d="M 1720 850 L 1720 760 L 400 760 L 400 795"/>
  <rect x="1726" y="805" width="28" height="20" rx="3" fill="#ffffff" stroke="#059669" stroke-width="1"/>
  <text x="1740" y="819" font-size="11" font-weight="800" fill="#059669" text-anchor="middle">NO</text>
  <g transform="translate(1060, 760)">
    <rect x="-140" y="-12" width="280" height="24" rx="4" fill="#ecfdf5" stroke="#059669" stroke-width="1.5"/>
    <text x="0" y="4" font-size="11.5" font-weight="800" fill="#065f46" text-anchor="middle">ALL SENSORS NORMAL: REPEAT 1 Hz CLOSED LOOP</text>
  </g>

  <!-- Thermal Gate YES -> State 6 (Thermal Cooldown) -->
  <path class="wire" stroke="#ea580c" stroke-width="3" marker-end="url(#arrow-orange)" d="M 1720 940 L 1720 995"/>
  <rect x="1726" y="955" width="32" height="20" rx="3" fill="#ffffff" stroke="#ea580c" stroke-width="1"/>
  <text x="1742" y="969" font-size="11" font-weight="800" fill="#ea580c" text-anchor="middle">YES</text>

  <!-- STATE 6: THERMAL_COOL (QUALIFIED AUTO-RECOVERY COOLDOWN, height 185) -->
  <g transform="translate(1510, 995)" filter="url(#shadow)">
    <rect width="420" height="185" rx="10" fill="#ffffff" stroke="#ea580c" stroke-width="2.5"/>
    <rect width="420" height="34" rx="10" fill="#ea580c"/>
    <rect x="0" y="24" width="420" height="10" fill="#ea580c"/>
    <text x="16" y="24" font-size="15.5" font-weight="900" fill="#ffffff">STATE 6: THERMAL_COOL (QUALIFIED COOLDOWN)</text>
    <text x="16" y="56" font-size="13" font-weight="700" fill="#9a3412">• Immediate trip: GPIO 32 driven LOW; 12V dummy load disconnected</text>
    <text x="16" y="78" font-size="13" font-weight="600" fill="#334155">• Removes thermal generation source (I²R losses drop to 0W)</text>
    <text x="16" y="100" font-size="13" font-weight="700" fill="#ea580c">• Core temperature T_core actively monitored via Standby +5VSB</text>
    <text x="16" y="122" font-size="13" font-weight="600" fill="#334155">• LCD displays "FAULT: OVERTEMP - COOLING" • Push alert to RTDB</text>
    <text x="16" y="144" font-size="13" font-weight="600" fill="#334155">• Cooldown target: Core must drop ≤ 45°C sustained for ≥ 60 seconds</text>
    <text x="16" y="168" font-size="12" font-weight="700" fill="#0369a1">Evaluates automatic restart qualification vs permanent lockout</text>
  </g>

  <!-- Arrow State 6 -> Decision 4 (Auto-Recovery Qualification) -->
  <path class="wire" stroke="#0f172a" stroke-width="3" marker-end="url(#arrow)" d="M 1720 1180 L 1720 1225"/>

  <!-- DECISION 4: AUTO-RECOVERY ELIGIBILITY CHECK -->
  <g transform="translate(1530, 1225)" filter="url(#shadow)">
    <polygon points="190,0 380,45 190,90 0,45" fill="#f5f3ff" stroke="#7e22ce" stroke-width="2"/>
    <text x="190" y="38" font-size="13.5" font-weight="900" fill="#581c87" text-anchor="middle">QUALIFIED FOR AUTO-RECOVERY?</text>
    <text x="190" y="58" font-size="11.5" font-weight="700" fill="#7e22ce" text-anchor="middle">Trip Count k &lt; 3 (1-Hr Window) &amp; T_core ≤ 45°C</text>
  </g>

  <!-- Decision 4 YES -> State 7 (Recovery Test) via Right Corridor (x = 2280) -->
  <path class="wire" stroke="#9333ea" stroke-width="3" marker-end="url(#arrow-purple)"
        d="M 1910 1270 L 2280 1270 L 2280 185 L 1930 185"/>
  <rect x="2210" y="700" width="34" height="22" rx="3" fill="#ffffff" stroke="#9333ea" stroke-width="1"/>
  <text x="2227" y="715" font-size="11" font-weight="800" fill="#9333ea" text-anchor="middle">YES</text>
  <text x="2265" y="750" font-size="11.5" font-weight="800" fill="#7e22ce" transform="rotate(90 2265 750)">QUALIFIED: TRY AUTO-RESTART (k &lt; 3)</text>

  <!-- Decision 4 NO -> State 8 (Thermal Lockout) -->
  <path class="wire" stroke="#dc2626" stroke-width="3" marker-end="url(#arrow-red)" d="M 1720 1315 L 1720 1355"/>
  <rect x="1726" y="1325" width="32" height="20" rx="3" fill="#ffffff" stroke="#dc2626" stroke-width="1"/>
  <text x="1742" y="1339" font-size="11" font-weight="800" fill="#dc2626" text-anchor="middle">NO</text>

  <!-- STATE 8: THERMAL_LOCK (PERMANENT THERMAL LOCKOUT) -->
  <g transform="translate(1510, 1355)" filter="url(#shadow)">
    <rect width="420" height="135" rx="10" fill="#ffffff" stroke="#dc2626" stroke-width="2.5"/>
    <rect width="420" height="32" rx="10" fill="#dc2626"/>
    <rect x="0" y="22" width="420" height="10" fill="#dc2626"/>
    <text x="16" y="22" font-size="15.5" font-weight="900" fill="#ffffff">STATE 8: THERMAL_LOCK (PERMANENT LOCKOUT)</text>
    <text x="16" y="52" font-size="13" font-weight="700" fill="#b91c1c">• Persistent over-temperature detected: Auto-recovery exhausted (k ≥ 3)</text>
    <text x="16" y="72" font-size="13" font-weight="600" fill="#334155">• GPIO 32 latched LOW permanently; LCD displays "LOCKOUT: THERMAL"</text>
    <text x="16" y="92" font-size="13" font-weight="700" fill="#dc2626">• Brevo Critical Push Email dispatched: On-site inspection mandated</text>
    <text x="16" y="112" font-size="12" font-weight="700" fill="#7f1d1d">Clearable ONLY via physical power-cycle OR authorized cloud reset</text>
  </g>

  <!-- STATE 7: RECOVERY_TEST (SUPERVISED RESTART ATTEMPT) -->
  <g transform="translate(1510, 110)" filter="url(#shadow)">
    <rect width="420" height="150" rx="10" fill="#ffffff" stroke="#9333ea" stroke-width="2.5"/>
    <rect width="420" height="34" rx="10" fill="#9333ea"/>
    <rect x="0" y="24" width="420" height="10" fill="#9333ea"/>
    <text x="16" y="24" font-size="15.5" font-weight="900" fill="#ffffff">STATE 7: RECOVERY_TEST (SUPERVISED ATTEMPT)</text>
    <text x="16" y="56" font-size="13" font-weight="700" fill="#6b21a8">• Increment restart counter k = k + 1 (Window expires after 3600s)</text>
    <text x="16" y="78" font-size="13" font-weight="600" fill="#334155">• Re-assert GPIO 32 HIGH: 500 ms inrush blanking active</text>
    <text x="16" y="100" font-size="13" font-weight="700" fill="#0284c7">• 120-Second Qualification Timer: Must operate stably under load</text>
    <text x="16" y="122" font-size="13" font-weight="600" fill="#334155">• If temperature re-trips within 120s -> immediate trip to STATE 8</text>
    <text x="16" y="140" font-size="12" font-weight="700" fill="#059669">If stable for 120s -> Qualified success: Returns to STATE 2: RUNNING</text>
  </g>

  <!-- Arrow State 7 Success -> Back to State 2: RUNNING via Open Alley between Col 1 and Col 2 at x=565 -->
  <!-- Col 1 ends at 520, State 9 starts at 610. Center is x=565 (Completely empty corridor!) -->
  <path class="wire" stroke="#059669" stroke-width="3" marker-end="url(#arrow-green)"
        d="M 1510 185 L 565 185 L 565 825 L 520 825"/>
  <g transform="translate(1000, 185)">
    <rect x="-70" y="-12" width="140" height="24" rx="4" fill="#ecfdf5" stroke="#059669" stroke-width="1.5"/>
    <text x="0" y="4" font-size="11" font-weight="800" fill="#065f46" text-anchor="middle">120s STABLE -> RUN</text>
  </g>

</svg>'''

    out_svg = os.path.join("documentation", "diagram_4_hardware_state_flowchart.svg")
    with open(out_svg, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Generated {out_svg}")

    # Compile to high-res PNG via typst
    typ_path = os.path.join("documentation", "render_diag4.typ")
    png_path = os.path.join("documentation", "diagram_4_hardware_state_flowchart.png")
    typst_exe = os.path.join("documentation", "bin", "typst.exe")
    with open(typ_path, "w", encoding="utf-8") as f:
        f.write('#set page(width: 2400pt, height: 1500pt, margin: 0pt)\n#image("diagram_4_hardware_state_flowchart.svg", width: 100%)\n')
    subprocess.run([typst_exe, "compile", "--format", "png", "--ppi", "150", typ_path, png_path], check=True)
    if os.path.exists(typ_path):
        os.remove(typ_path)
    print(f"Compiled {png_path}")

if __name__ == "__main__":
    generate_diagram_4()
