# -*- coding: utf-8 -*-
"""
Diagram 1 Generator: Hardware Circuit Block Diagram
"""

import os
import subprocess

def generate_diagram_1():
    w = 2200
    h = 1400

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <defs>
    <pattern id="grid" width="25" height="25" patternUnits="userSpaceOnUse">
      <path d="M 25 0 L 0 0 0 25" fill="none" stroke="#e2e8f0" stroke-width="0.75"/>
    </pattern>
    <filter id="shadow" x="-3%" y="-3%" width="108%" height="110%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="2" dy="4" stdDeviation="5" flood-color="#0f172a" flood-opacity="0.08"/>
    </filter>
    <!-- Arrow Markers -->
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#0f172a"/>
    </marker>
    <marker id="arrow-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#2563eb"/>
    </marker>
    <marker id="arrow-green" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#059669"/>
    </marker>
    <marker id="arrow-orange" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#d97706"/>
    </marker>
    <marker id="arrow-purple" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#9333ea"/>
    </marker>
    <marker id="arrow-red" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#dc2626"/>
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
  <g transform="translate(60, 52)">
    <text font-size="32" font-weight="900" fill="#0f172a" letter-spacing="-0.5px">IoT Transformer Condition Monitoring System — Hardware Block Diagram</text>
    <text font-size="18" font-weight="700" fill="#64748b" y="32">Physical Hardware Modules, Power Domains, Multi-Rail Instrumentation &amp; Control Buses</text>
  </g>

  <!-- ==================== ZONE 1: PRIMARY POWER & SWITCHING (LEFT) ==================== -->
  
  <!-- 1. ATX SMPS Power Supply Box -->
  <g transform="translate(60, 130)" filter="url(#shadow)">
    <rect width="450" height="490" rx="10" fill="#ffffff" stroke="#cbd5e1" stroke-width="2"/>
    <rect width="450" height="52" rx="10" fill="#1e293b"/>
    <rect x="0" y="42" width="450" height="10" fill="#1e293b"/>
    <text x="24" y="34" font-size="20" font-weight="900" fill="#f8fafc">ATX SMPS POWER SUPPLY (XH-M229)</text>
    <text x="24" y="78" font-size="15" font-weight="700" fill="#64748b">Primary 230V AC Input • Switched DC Rails &amp; Standby</text>

    <!-- Rail Outlets -->
    <!-- +12V -->
    <g transform="translate(24, 100)">
      <rect width="402" height="60" rx="6" fill="#fffbeb" stroke="#fde68a" stroke-width="1.5"/>
      <circle cx="30" cy="30" r="14" fill="#d97706"/>
      <text x="56" y="27" font-size="18" font-weight="800" fill="#92400e">+12V DC Main Switched Rail</text>
      <text x="56" y="48" font-size="14" font-weight="600" fill="#b45309">Powers 12V 50W Dummy Load &amp; Cooling Fan Driver</text>
    </g>

    <!-- +5V -->
    <g transform="translate(24, 172)">
      <rect width="402" height="60" rx="6" fill="#fef2f2" stroke="#fecaca" stroke-width="1.5"/>
      <circle cx="30" cy="30" r="14" fill="#dc2626"/>
      <text x="56" y="27" font-size="18" font-weight="800" fill="#991b1b">+5V DC Native Switched Rail</text>
      <text x="56" y="48" font-size="14" font-weight="600" fill="#b91c1c">Switched secondary rail monitored via INA219 #2</text>
    </g>

    <!-- +3.3V -->
    <g transform="translate(24, 244)">
      <rect width="402" height="60" rx="6" fill="#fff7ed" stroke="#fed7aa" stroke-width="1.5"/>
      <circle cx="30" cy="30" r="14" fill="#ea580c"/>
      <text x="56" y="27" font-size="18" font-weight="800" fill="#9a3412">+3.3V DC Native Switched Rail</text>
      <text x="56" y="48" font-size="14" font-weight="600" fill="#c2410c">Switched secondary rail monitored via INA219 #3</text>
    </g>

    <!-- +5VSB Standby -->
    <g transform="translate(24, 316)">
      <rect width="402" height="74" rx="6" fill="#faf5ff" stroke="#e9d5ff" stroke-width="2"/>
      <circle cx="30" cy="37" r="14" fill="#9333ea"/>
      <text x="56" y="30" font-size="18" font-weight="800" fill="#6b21a8">+5VSB Standby Power (Continuous)</text>
      <text x="56" y="52" font-size="14" font-weight="700" fill="#7e22ce">24/7 Uninterrupted Supply → ESP32 VIN &amp; LCD VCC</text>
      <text x="56" y="68" font-size="12" font-weight="600" fill="#9333ea">Maintains monitoring &amp; display even when ATX is OFF</text>
    </g>

    <!-- PS_ON# Terminal -->
    <g transform="translate(24, 402)">
      <rect width="402" height="66" rx="6" fill="#f0fdf4" stroke="#bbf7d0" stroke-width="2"/>
      <circle cx="30" cy="33" r="14" fill="#059669"/>
      <text x="56" y="28" font-size="18" font-weight="800" fill="#065f46">PS_ON# Control Terminal (Pin 16)</text>
      <text x="56" y="50" font-size="14" font-weight="600" fill="#047857">Active-Low: Pull to GND to energize main rails</text>
    </g>
  </g>

  <!-- 2. Discrete PS_ON# Switch Box -->
  <g transform="translate(60, 645)" filter="url(#shadow)">
    <rect width="450" height="320" rx="10" fill="#ffffff" stroke="#cbd5e1" stroke-width="2"/>
    <rect width="450" height="48" rx="10" fill="#065f46"/>
    <rect x="0" y="38" width="450" height="10" fill="#065f46"/>
    <text x="24" y="32" font-size="20" font-weight="900" fill="#f8fafc">PS_ON# HARDWARE INTERLOCK SWITCH</text>
    <text x="24" y="75" font-size="15" font-weight="700" fill="#64748b">Discrete NPN Transistor Inverter Stage</text>

    <!-- Sub-elements -->
    <g transform="translate(24, 92)">
      <rect width="402" height="56" rx="6" fill="#f8fafc" stroke="#e2e8f0" stroke-width="1.5"/>
      <text x="20" y="26" font-size="17" font-weight="800" fill="#0f172a">2N3904 NPN Transistor (Q1)</text>
      <text x="20" y="46" font-size="14" font-weight="600" fill="#475569">Collector (Pin 3) pulls PS_ON# to GND; Emitter (Pin 1) to Star GND</text>
    </g>

    <g transform="translate(24, 160)">
      <rect width="402" height="66" rx="6" fill="#f8fafc" stroke="#e2e8f0" stroke-width="1.5"/>
      <text x="20" y="26" font-size="17" font-weight="800" fill="#0f172a">1 kΩ Base Resistor (R1)</text>
      <text x="20" y="48" font-size="14" font-weight="600" fill="#475569">Driven by ESP32 GPIO 32 (HIGH = Energize, LOW = Cut)</text>
    </g>

    <g transform="translate(24, 238)">
      <rect width="402" height="66" rx="6" fill="#f8fafc" stroke="#e2e8f0" stroke-width="1.5"/>
      <text x="20" y="26" font-size="17" font-weight="800" fill="#0f172a">10 kΩ Pull-Down Resistor (R2)</text>
      <text x="20" y="48" font-size="14" font-weight="600" fill="#475569">Keeps transistor OFF during ESP32 boot/reset</text>
    </g>
  </g>

  <!-- 3. Physical Operator Switches -->
  <g transform="translate(60, 990)" filter="url(#shadow)">
    <rect width="450" height="340" rx="10" fill="#ffffff" stroke="#cbd5e1" stroke-width="2"/>
    <rect width="450" height="48" rx="10" fill="#334155"/>
    <rect x="0" y="38" width="450" height="10" fill="#334155"/>
    <text x="24" y="32" font-size="20" font-weight="900" fill="#f8fafc">PHYSICAL OPERATOR SWITCHES</text>
    <text x="24" y="75" font-size="15" font-weight="700" fill="#64748b">SPST Rocker Switches with Hardware Debounce</text>

    <g transform="translate(24, 95)">
      <rect width="402" height="95" rx="6" fill="#f8fafc" stroke="#e2e8f0" stroke-width="1.5"/>
      <text x="20" y="28" font-size="18" font-weight="800" fill="#0f172a">Main Output Enable Switch (GPIO 18)</text>
      <text x="20" y="52" font-size="14" font-weight="600" fill="#475569">Closed to GND = Authorized Startup Request</text>
      <text x="20" y="72" font-size="13" font-weight="700" fill="#059669">Safety: Maintained ON never bypasses software trips</text>
    </g>

    <g transform="translate(24, 205)">
      <rect width="402" height="95" rx="6" fill="#f8fafc" stroke="#e2e8f0" stroke-width="1.5"/>
      <text x="20" y="28" font-size="18" font-weight="800" fill="#0f172a">SoftAP Setup Switch (GPIO 23)</text>
      <text x="20" y="52" font-size="14" font-weight="600" fill="#475569">Closed to GND = Launch ESP32-TMS-SETUP Mode</text>
      <text x="20" y="72" font-size="13" font-weight="700" fill="#2563eb">Enables local Wi-Fi router credential provisioning</text>
    </g>
  </g>


  <!-- ==================== ZONE 2: INSTRUMENTATION & SENSING (CENTER-TOP) ==================== -->
  
  <!-- 4. 3x INA219 Current & Voltage Monitors -->
  <g transform="translate(560, 130)" filter="url(#shadow)">
    <rect width="930" height="340" rx="10" fill="#ffffff" stroke="#cbd5e1" stroke-width="2"/>
    <rect width="930" height="52" rx="10" fill="#4c1d95"/>
    <rect x="0" y="42" width="930" height="10" fill="#4c1d95"/>
    <text x="24" y="34" font-size="20" font-weight="900" fill="#f8fafc">MULTI-RAIL CURRENT &amp; VOLTAGE INSTRUMENTATION (3x INA219)</text>
    <text x="24" y="78" font-size="15" font-weight="700" fill="#64748b">12-bit High-Side Shunt &amp; Bus Voltage Monitors • Shared I2C Highway (GPIO 21 SDA / GPIO 22 SCL)</text>

    <!-- INA219 #1 (12V) -->
    <g transform="translate(24, 95)">
      <rect width="280" height="215" rx="8" fill="#581c87" stroke="#7e22ce" stroke-width="2"/>
      <text x="20" y="34" font-size="20" font-weight="900" fill="#f8fafc">INA219 #1 (12V)</text>
      <text x="20" y="58" font-size="15" font-weight="700" fill="#e9d5ff">I2C Address: 0x40</text>
      <rect x="20" y="72" width="240" height="1" fill="#7e22ce"/>
      <text x="20" y="98" font-size="14" font-weight="600" fill="#fed7aa">Shunt: 0.1 Ω (R100)</text>
      <text x="20" y="122" font-size="14" font-weight="600" fill="#fed7aa">Monitors: +12V Rail</text>
      <text x="20" y="146" font-size="14" font-weight="600" fill="#fed7aa">Warning: &gt; 2.50 A</text>
      <text x="20" y="170" font-size="14" font-weight="800" fill="#fca5a5">Fast Trip: &gt; 3.15 A</text>
      <text x="20" y="194" font-size="13" font-weight="700" fill="#fde68a">Voltage Window: 10.8 - 13.2V</text>
    </g>

    <!-- INA219 #2 (5V) -->
    <g transform="translate(324, 95)">
      <rect width="280" height="215" rx="8" fill="#581c87" stroke="#7e22ce" stroke-width="2"/>
      <text x="20" y="34" font-size="20" font-weight="900" fill="#f8fafc">INA219 #2 (5V)</text>
      <text x="20" y="58" font-size="15" font-weight="700" fill="#e9d5ff">I2C Address: 0x41 [A0]</text>
      <rect x="20" y="72" width="240" height="1" fill="#7e22ce"/>
      <text x="20" y="98" font-size="14" font-weight="600" fill="#fed7aa">Shunt: 0.1 Ω (R100)</text>
      <text x="20" y="122" font-size="14" font-weight="600" fill="#fed7aa">Monitors: +5V Rail</text>
      <text x="20" y="146" font-size="14" font-weight="600" fill="#fed7aa">Warning: &gt; 0.50 A</text>
      <text x="20" y="170" font-size="14" font-weight="800" fill="#fca5a5">Overcurrent: &gt; 1.00 A</text>
      <text x="20" y="194" font-size="13" font-weight="700" fill="#fde68a">Voltage Window: 4.50 - 5.50V</text>
    </g>

    <!-- INA219 #3 (3.3V) -->
    <g transform="translate(624, 95)">
      <rect width="280" height="215" rx="8" fill="#581c87" stroke="#7e22ce" stroke-width="2"/>
      <text x="20" y="34" font-size="20" font-weight="900" fill="#f8fafc">INA219 #3 (3.3V)</text>
      <text x="20" y="58" font-size="15" font-weight="700" fill="#e9d5ff">I2C Address: 0x44 [A1]</text>
      <rect x="20" y="72" width="240" height="1" fill="#7e22ce"/>
      <text x="20" y="98" font-size="14" font-weight="600" fill="#fed7aa">Shunt: 0.1 Ω (R100)</text>
      <text x="20" y="122" font-size="14" font-weight="600" fill="#fed7aa">Monitors: +3.3V Rail</text>
      <text x="20" y="146" font-size="14" font-weight="600" fill="#fed7aa">Warning: &gt; 0.50 A</text>
      <text x="20" y="170" font-size="14" font-weight="800" fill="#fca5a5">Overcurrent: &gt; 1.00 A</text>
      <text x="20" y="194" font-size="13" font-weight="700" fill="#fde68a">Voltage Window: 2.97 - 3.63V</text>
    </g>
  </g>

  <!-- 5. Dual DS18B20 Digital Temperature Probes -->
  <g transform="translate(560, 495)" filter="url(#shadow)">
    <rect width="930" height="210" rx="10" fill="#ffffff" stroke="#cbd5e1" stroke-width="2"/>
    <rect width="930" height="48" rx="10" fill="#1e3a8a"/>
    <rect x="0" y="38" width="930" height="10" fill="#1e3a8a"/>
    <text x="24" y="32" font-size="20" font-weight="900" fill="#f8fafc">DUAL DS18B20 DIGITAL TEMPERATURE SENSORS (1-WIRE DQ BUS)</text>
    <text x="24" y="75" font-size="15" font-weight="700" fill="#64748b">12-bit Digital Precision (0.0625°C Res) • GPIO 27 1-Wire Bus with 4.7 kΩ Pull-up to 3.3V</text>

    <!-- Probe 1 -->
    <g transform="translate(24, 92)">
      <rect width="425" height="98" rx="8" fill="#1e3a8a" stroke="#1d4ed8" stroke-width="2"/>
      <text x="20" y="32" font-size="20" font-weight="900" fill="#ffffff">PROBE 1: TRANSFORMER CORE</text>
      <text x="20" y="56" font-size="15" font-weight="700" fill="#f8fafc">Monitors Transformer Surface Hot-Spot Temp (T_core)</text>
      <text x="20" y="80" font-size="14" font-weight="700" fill="#fef08a">Trip: T_core ≥ 65.0°C or Projected T_p ≥ 70.0°C</text>
    </g>

    <!-- Probe 2 -->
    <g transform="translate(480, 92)">
      <rect width="425" height="98" rx="8" fill="#1e3a8a" stroke="#1d4ed8" stroke-width="2"/>
      <text x="20" y="32" font-size="20" font-weight="900" fill="#ffffff">PROBE 2: AMBIENT AIR INLET</text>
      <text x="20" y="56" font-size="15" font-weight="700" fill="#f8fafc">Monitors Intake Reference Air Temp (T_inlet)</text>
      <text x="20" y="80" font-size="14" font-weight="700" fill="#a7f3d0">Computes Continuous Thermal Rise: ΔT = T_core - T_inlet</text>
    </g>
  </g>


  <!-- ==================== ZONE 3: EMBEDDED CONTROLLER CORE (CENTER-BOTTOM) ==================== -->
  
  <!-- 6. ESP32-WROOM-32 DevKit Core -->
  <g transform="translate(560, 730)" filter="url(#shadow)">
    <rect width="930" height="600" rx="10" fill="#ffffff" stroke="#cbd5e1" stroke-width="2"/>
    <rect width="930" height="52" rx="10" fill="#0f172a"/>
    <rect x="0" y="42" width="930" height="10" fill="#0f172a"/>
    <text x="24" y="34" font-size="22" font-weight="900" fill="#f8fafc">ESP32-WROOM-32 DEVKIT CORE CONTROLLER</text>
    <text x="24" y="78" font-size="15" font-weight="700" fill="#64748b">240 MHz Dual-Core Tensilica LX6 • Powered 24/7 via VIN from +5VSB Standby Rail</text>

    <!-- Internal Firmware Subsystems (Cards) -->
    <!-- Card A: Acquisition & Math -->
    <g transform="translate(24, 98)">
      <rect width="425" height="230" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
      <text x="20" y="30" font-size="18" font-weight="900" fill="#1e3a8a">1. ACQUISITION &amp; MATH ENGINE</text>
      <text x="20" y="58" font-size="14" font-weight="600" fill="#334155">• Non-blocking 1-Wire &amp; I2C Drivers</text>
      <text x="20" y="82" font-size="14" font-weight="600" fill="#334155">• EMA Noise Filtering (α = 0.20)</text>
      <text x="20" y="106" font-size="14" font-weight="600" fill="#334155">• Rolling 30-Second Regression Window (N=30)</text>
      <text x="20" y="130" font-size="14" font-weight="600" fill="#334155">• Linear Regression Rate of Rise (r = dT/dt)</text>
      <text x="20" y="154" font-size="14" font-weight="700" fill="#2563eb">• Forward Horizon Projection: T_p = T_f + 30r</text>
      <text x="20" y="178" font-size="14" font-weight="600" fill="#334155">• Dual Demand: D_auto = max(g(T_f), g(T_p))</text>
      <text x="20" y="202" font-size="14" font-weight="700" fill="#d97706">• Slew Limiter: Instant rise, ≤1%/s descent</text>
    </g>

    <!-- Card B: Supervisory Protection -->
    <g transform="translate(480, 98)">
      <rect width="425" height="230" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
      <text x="20" y="30" font-size="18" font-weight="900" fill="#991b1b">2. SUPERVISORY PROTECTION ENGINE</text>
      <text x="20" y="58" font-size="14" font-weight="600" fill="#334155">• Deterministic Non-Preemptible Evaluation</text>
      <text x="20" y="82" font-size="14" font-weight="700" fill="#dc2626">• 12V Overcurrent Fast Trip: &gt; 3.15 A (&lt; 5 ms)</text>
      <text x="20" y="106" font-size="14" font-weight="700" fill="#dc2626">• Thermal Over-temp Trip: T ≥ 65°C | T_p ≥ 70°C</text>
      <text x="20" y="130" font-size="14" font-weight="600" fill="#334155">• Rail Voltage Boundary Supervision (±10%)</text>
      <text x="20" y="154" font-size="14" font-weight="600" fill="#334155">• 500 ms Inrush Blanking Window on startup</text>
      <text x="20" y="178" font-size="14" font-weight="600" fill="#334155">• 10-State Power State Machine</text>
      <text x="20" y="202" font-size="14" font-weight="700" fill="#059669">• Qualified Auto-Recovery vs Permanent Lockout</text>
    </g>

    <!-- Card C: Hardware Pin Allocation Matrix -->
    <g transform="translate(24, 345)">
      <rect width="882" height="230" rx="8" fill="#0f172a"/>
      <text x="20" y="30" font-size="18" font-weight="900" fill="#f8fafc">HARDWARE PIN ASSIGNMENTS &amp; INTERFACE BUSES</text>

      <!-- Pin Table Grid -->
      <g transform="translate(20, 50)" font-size="15" font-weight="700">
        <!-- Col 1 -->
        <text x="0" y="24" fill="#60a5fa">GPIO 21 (SDA):</text><text x="130" y="24" fill="#f8fafc">I2C Data Bus (3x INA219 + 16x2 LCD)</text>
        <text x="0" y="52" fill="#38bdf8">GPIO 22 (SCL):</text><text x="130" y="52" fill="#f8fafc">I2C Clock Bus (400 kHz Fast-Mode)</text>
        <text x="0" y="80" fill="#facc15">GPIO 27 (TEMP):</text><text x="130" y="80" fill="#f8fafc">1-Wire DQ Bus (Dual DS18B20 Probes)</text>
        <text x="0" y="108" fill="#4ade80">GPIO 32 (PS_ON#):</text><text x="130" y="108" fill="#f8fafc">Active-Low Driver → 2N3904 NPN Switch</text>

        <!-- Col 2 -->
        <text x="460" y="24" fill="#c084fc">GPIO 25 (PWM):</text><text x="590" y="24" fill="#f8fafc">25 kHz Fan PWM → TB6612 PWMA</text>
        <text x="460" y="52" fill="#f472b6">GPIO 26 (AIN1):</text><text x="590" y="52" fill="#f8fafc">Fan Motor Direction 1 → TB6612 AIN1</text>
        <text x="460" y="80" fill="#67e8f9">GPIO 33 (STBY):</text><text x="590" y="80" fill="#f8fafc">Driver Bridge Enable → TB6612 STBY</text>
        <text x="460" y="108" fill="#fed7aa">GPIO 18 / 23:</text><text x="590" y="108" fill="#f8fafc">Main Power SW (18) | SoftAP Setup SW (23)</text>
        <text x="460" y="136" fill="#f3e8ff">VIN Pin (5V):</text><text x="590" y="136" fill="#f8fafc">Fed from +5VSB Standby (Continuous)</text>
      </g>
    </g>
  </g>


  <!-- ==================== ZONE 4: ACTUATION, LOAD & DISPLAY (RIGHT) ==================== -->
  
  <!-- 7. 12V 50W Dummy Load Resistor -->
  <g transform="translate(1530, 130)" filter="url(#shadow)">
    <rect width="610" height="340" rx="10" fill="#ffffff" stroke="#cbd5e1" stroke-width="2"/>
    <rect width="610" height="52" rx="10" fill="#1e293b"/>
    <rect x="0" y="42" width="610" height="10" fill="#1e293b"/>
    <text x="24" y="34" font-size="20" font-weight="900" fill="#f8fafc">12V DUMMY LOAD RESISTOR (TEST BENCH LOAD)</text>
    <text x="24" y="78" font-size="15" font-weight="700" fill="#64748b">External Electrical Load for Demonstrating Secondary Loading</text>

    <g transform="translate(24, 100)">
      <rect width="562" height="210" rx="8" fill="#0f172a"/>
      <rect x="25" y="25" width="220" height="160" rx="6" fill="#d97706" stroke="#b45309" stroke-width="2"/>
      <text x="135" y="90" font-size="28" font-weight="900" fill="#fef08a" text-anchor="middle">10 Ω, 50 W</text>
      <text x="135" y="125" font-size="18" font-weight="800" fill="#ffffff" text-anchor="middle">ALUMINUM HOUSED</text>

      <g transform="translate(270, 35)">
        <text x="0" y="25" font-size="18" font-weight="800" fill="#f8fafc">Nominal Load Specs:</text>
        <text x="0" y="55" font-size="16" font-weight="700" fill="#fed7aa">• Operating Voltage: 12.0 V DC</text>
        <text x="0" y="80" font-size="16" font-weight="700" fill="#fed7aa">• Measured Current: 1.20 A</text>
        <text x="0" y="105" font-size="16" font-weight="700" fill="#fed7aa">• Dissipated Power: 14.4 W</text>
        <text x="0" y="132" font-size="13" font-weight="600" fill="#94a3b8">Fed through INA219 #1 shunt to evaluate</text>
        <text x="0" y="150" font-size="13" font-weight="600" fill="#94a3b8">real-time secondary load dynamics</text>
      </g>
    </g>
  </g>

  <!-- 8. TB6612FNG Driver & 12V Cooling Fan -->
  <g transform="translate(1530, 495)" filter="url(#shadow)">
    <rect width="610" height="400" rx="10" fill="#ffffff" stroke="#cbd5e1" stroke-width="2"/>
    <rect width="610" height="52" rx="10" fill="#991b1b"/>
    <rect x="0" y="42" width="610" height="10" fill="#991b1b"/>
    <text x="24" y="34" font-size="20" font-weight="900" fill="#f8fafc">TB6612FNG DRIVER &amp; 12V COOLING FAN</text>
    <text x="24" y="78" font-size="15" font-weight="700" fill="#64748b">Dual MOSFET H-Bridge • Ultrasonic 25 kHz PWM Speed Modulation</text>

    <!-- Sub-elements -->
    <g transform="translate(24, 95)">
      <rect width="265" height="280" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
      <text x="18" y="30" font-size="18" font-weight="900" fill="#991b1b">TB6612FNG DRIVER</text>
      <text x="18" y="58" font-size="14" font-weight="600" fill="#334155">• VM: +12V Switched Rail</text>
      <text x="18" y="82" font-size="14" font-weight="600" fill="#334155">• VCC: 3.3V Logic Supply</text>
      <text x="18" y="106" font-size="14" font-weight="600" fill="#334155">• STBY: GPIO 33 (Active-High)</text>
      <text x="18" y="130" font-size="14" font-weight="600" fill="#334155">• PWMA: GPIO 25 (25 kHz)</text>
      <text x="18" y="154" font-size="14" font-weight="600" fill="#334155">• AIN1: GPIO 26 (Forward)</text>
      <text x="18" y="178" font-size="14" font-weight="600" fill="#334155">• AIN2: Tied locally to GND</text>
      <text x="18" y="210" font-size="13" font-weight="700" fill="#059669">Continuous: 1.2 A / Peak: 3.2 A</text>
      <text x="18" y="235" font-size="13" font-weight="600" fill="#475569">Low R_DS(on) Power MOSFETs</text>
    </g>

    <g transform="translate(310, 95)">
      <rect width="275" height="280" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
      <text x="18" y="30" font-size="18" font-weight="900" fill="#0f172a">12V DC COOLING FAN</text>
      <circle cx="137" cy="115" r="50" fill="#0f172a" stroke="#334155" stroke-width="3"/>
      <circle cx="137" cy="115" r="16" fill="#38bdf8"/>
      <text x="137" y="180" font-size="15" font-weight="800" fill="#0f172a" text-anchor="middle">BRUSHLESS 12V DC</text>
      <text x="18" y="215" font-size="14" font-weight="600" fill="#334155">• Slew-rate limited deceleration</text>
      <text x="18" y="238" font-size="14" font-weight="600" fill="#334155">• Minimum duty: 30% (anti-stall)</text>
      <text x="18" y="260" font-size="14" font-weight="700" fill="#2563eb">• Boost to 100% on high load/temp</text>
    </g>
  </g>

  <!-- 9. 16x2 Character LCD (Standby 5V) -->
  <g transform="translate(1530, 920)" filter="url(#shadow)">
    <rect width="610" height="410" rx="10" fill="#ffffff" stroke="#cbd5e1" stroke-width="2"/>
    <rect width="610" height="52" rx="10" fill="#14532d"/>
    <rect x="0" y="42" width="610" height="10" fill="#14532d"/>
    <text x="24" y="34" font-size="20" font-weight="900" fill="#f8fafc">16x2 CHARACTER LCD (STANDBY POWERED)</text>
    <text x="24" y="78" font-size="15" font-weight="700" fill="#64748b">PCF8574 I2C Backpack (0x27) • Powered 24/7 from +5VSB</text>

    <!-- LCD Glass -->
    <g transform="translate(24, 98)">
      <rect width="562" height="190" rx="6" fill="#0f172a" stroke="#166534" stroke-width="2"/>
      <rect x="15" y="15" width="532" height="160" rx="4" fill="#0284c7" stroke="#0369a1" stroke-width="1.5"/>

      <!-- 16x2 Characters in JetBrains Mono -->
      <text x="35" y="65" font-family="'JetBrains Mono', Consolas, monospace" font-size="22" font-weight="bold" fill="#f0f9ff" letter-spacing="2">
        T1:48.6C  T2:29.4C
      </text>
      <text x="35" y="105" font-family="'JetBrains Mono', Consolas, monospace" font-size="22" font-weight="bold" fill="#f0f9ff" letter-spacing="2">
        dT:19.2C  Tp:51.3C
      </text>
      <text x="35" y="145" font-family="'JetBrains Mono', Consolas, monospace" font-size="20" font-weight="bold" fill="#fef08a" letter-spacing="2">
        Main: ON  FAN: 65%
      </text>
    </g>

    <g transform="translate(24, 305)">
      <text x="0" y="25" font-size="15" font-weight="700" fill="#0f172a">Continuous Operation Architectural Benefit:</text>
      <text x="0" y="50" font-size="14" font-weight="600" fill="#334155">Because the LCD is powered from +5VSB, the screen remains fully illuminated</text>
      <text x="0" y="72" font-size="14" font-weight="600" fill="#334155">and displays "Main: DE-ENERGIZED" or "FAULT: OVERTEMP" even when ATX is tripped.</text>
    </g>
  </g>


  <!-- ==================== INTERCONNECTING BUS LINES & LABELS ==================== -->
  
  <!-- Standby Power Rail (+5VSB: Purple) -->
  <path class="wire" stroke="#9333ea" stroke-width="4.5" stroke-dasharray="8,4"
        d="M 474 485 L 520 485 L 520 710 L 560 710"/>
  <!-- Tap down to ESP32 VIN -->
  <path class="wire" stroke="#9333ea" stroke-width="4.5" stroke-dasharray="8,4"
        d="M 520 710 L 520 1200 L 560 1200"/>
  <!-- Tap right across to LCD Display -->
  <path class="wire" stroke="#9333ea" stroke-width="4" stroke-dasharray="8,4"
        d="M 520 710 L 520 720 L 1500 720 L 1500 1150 L 1530 1150"/>
  
  <!-- Switched +12V Rail (Gold/Amber) -->
  <path class="wire" stroke="#d97706" stroke-width="5"
        d="M 474 260 L 560 260"/>
  <!-- +12V through INA219 #1 to Dummy Load -->
  <path class="wire" stroke="#d97706" stroke-width="5"
        d="M 864 260 L 1530 260"/>
  <!-- Tap down from +12V to TB6612 VM -->
  <path class="wire" stroke="#d97706" stroke-width="4"
        d="M 1510 260 L 1510 650 L 1530 650"/>
  <circle cx="1510" cy="260" r="5.5" fill="#d97706"/>

  <!-- Switched +5V & +3.3V Rails to INA219 #2 and #3 -->
  <path class="wire" stroke="#dc2626" stroke-width="4" d="M 474 330 L 540 330 L 540 350 L 884 350"/>
  <path class="wire" stroke="#ea580c" stroke-width="4" d="M 474 400 L 530 400 L 530 420 L 1184 420"/>

  <!-- I2C Bus Highway (Cyan/Blue) from ESP32 up to INA219s and right to LCD -->
  <path class="wire" stroke="#0284c7" stroke-width="3.5"
        d="M 1490 850 L 1515 850 L 1515 410 L 1490 410"/>
  <path class="wire" stroke="#0284c7" stroke-width="3.5"
        d="M 1515 850 L 1515 1050 L 1530 1050"/>

  <!-- 1-Wire Bus from ESP32 to DS18B20s -->
  <path class="wire" stroke="#eab308" stroke-width="4"
        d="M 1025 730 L 1025 705"/>

  <!-- Control Line: ESP32 GPIO 32 to 2N3904 Base -->
  <path class="wire" stroke="#059669" stroke-width="4"
        d="M 560 810 L 510 810"/>

  <!-- Switch Lines from Operator Switches to ESP32 -->
  <path class="wire" stroke="#64748b" stroke-width="3.5"
        d="M 510 1080 L 535 1080 L 535 1100 L 560 1100"/>
  <path class="wire" stroke="#64748b" stroke-width="3.5"
        d="M 510 1200 L 545 1200 L 545 1140 L 560 1140"/>

  <!-- Fan PWM & Control Lines from ESP32 to TB6612 -->
  <path class="wire" stroke="#c084fc" stroke-width="3.5"
        d="M 1490 920 L 1520 920 L 1520 780 L 1530 780"/>

</svg>'''

    out_svg = os.path.join("documentation", "diagram_1_hardware_block.svg")
    with open(out_svg, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Generated {out_svg}")

    # Compile to high-res PNG via typst
    typ_path = os.path.join("documentation", "render_diag1.typ")
    png_path = os.path.join("documentation", "diagram_1_hardware_block.png")
    typst_exe = os.path.join("documentation", "bin", "typst.exe")
    with open(typ_path, "w", encoding="utf-8") as f:
        f.write('#set page(width: 2200pt, height: 1400pt, margin: 0pt)\n#image("diagram_1_hardware_block.svg", width: 100%)\n')
    subprocess.run([typst_exe, "compile", "--format", "png", "--ppi", "150", typ_path, png_path], check=True)
    if os.path.exists(typ_path):
        os.remove(typ_path)
    print(f"Compiled {png_path}")

if __name__ == "__main__":
    generate_diagram_1()
