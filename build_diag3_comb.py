# -*- coding: utf-8 -*-
"""
Diagram 3 Generator: Combined Hardware + Software System Architecture Diagram (Pristine, 100% Collision-Free)
"""

import os
import subprocess

def generate_diagram_3():
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
    <marker id="arrow-cyan" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#0284c7"/>
    </marker>
    <marker id="arrow-green" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#059669"/>
    </marker>
    <marker id="arrow-orange" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#ea580c"/>
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
  <g transform="translate(60, 48)">
    <text font-size="32" font-weight="900" fill="#0f172a" letter-spacing="-0.5px">IoT Transformer Condition Monitoring System — Unified System Architecture</text>
    <text font-size="17" font-weight="700" fill="#64748b" y="28">End-to-End System Integration: Physical Hardware, Embedded Firmware, Local UI &amp; Cloud Supervision</text>
  </g>

  <!-- ==================== TIER 1: CLOUD & REMOTE SUPERVISION LAYER (TOP) ==================== -->
  <g transform="translate(60, 100)" filter="url(#shadow)">
    <rect width="2080" height="245" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="2"/>
    <rect width="2080" height="40" rx="12" fill="#d97706"/>
    <rect x="0" y="30" width="2080" height="10" fill="#d97706"/>
    <text x="24" y="26" font-size="17" font-weight="900" fill="#ffffff">TIER 1: CLOUD &amp; REMOTE SUPERVISION LAYER (FIREBASE &amp; SERVERLESS EDGE)</text>

    <!-- Cloud Sub-Block 1: Firebase Hosting & Web Dashboard -->
    <g transform="translate(24, 55)">
      <rect width="640" height="175" rx="8" fill="#f0f9ff" stroke="#bae6fd" stroke-width="1.5"/>
      <text x="18" y="26" font-size="17" font-weight="900" fill="#0369a1">FIREBASE HOSTING (INTERNET WEB DASHBOARD)</text>
      <text x="18" y="48" font-size="13.5" font-weight="700" fill="#0284c7">• Single-Page Application (SPA) deployed directly via Firebase CLI</text>
      <text x="18" y="70" font-size="13.5" font-weight="600" fill="#334155">• Private GitHub code repository (GitHub serves solely as code backup)</text>
      <text x="18" y="92" font-size="13.5" font-weight="600" fill="#334155">• Integrated Firebase Authentication: Role-based engineer login &amp; security</text>
      <text x="18" y="114" font-size="13.5" font-weight="600" fill="#334155">• Real-time WebSocket connection streams live gauges &amp; multi-day charts</text>
      <text x="18" y="136" font-size="13.5" font-weight="700" fill="#dc2626">• Red Alert Trip Banner &amp; Remote Authorized Emergency Stop</text>
    </g>

    <!-- Cloud Sub-Block 2: Firebase Realtime Database (RTDB) -->
    <g transform="translate(710, 55)">
      <rect width="660" height="175" rx="8" fill="#fffbeb" stroke="#fde68a" stroke-width="1.5"/>
      <text x="18" y="26" font-size="17" font-weight="900" fill="#92400e">FIREBASE REALTIME DATABASE (RTDB)</text>
      <text x="18" y="48" font-size="13.5" font-weight="700" fill="#b45309">• /devices/&#123;id&#125;/latest: 10s periodic live telemetry frame upload</text>
      <text x="18" y="70" font-size="13.5" font-weight="600" fill="#334155">• Telemetry: T1, T2, dT, Tp, 12V/5V/3.3V Volts, Currents, Power, Fan PWM</text>
      <text x="18" y="92" font-size="13.5" font-weight="600" fill="#334155">• /devices/&#123;id&#125;/history: Persistent hourly rollups &amp; emergency trip snapshots</text>
      <text x="18" y="114" font-size="13.5" font-weight="600" fill="#334155">• /devices/&#123;id&#125;/commands: Remote manual cutoff &amp; fault lockout reset queue</text>
      <text x="18" y="136" font-size="13.5" font-weight="700" fill="#059669">• Bidirectional sub-second data synchronization to web clients</text>
    </g>

    <!-- Cloud Sub-Block 3: Cloudflare Watchdog & Brevo Email -->
    <g transform="translate(1415, 55)">
      <rect width="640" height="175" rx="8" fill="#faf5ff" stroke="#e9d5ff" stroke-width="1.5"/>
      <text x="18" y="26" font-size="17" font-weight="900" fill="#6b21a8">SERVERLESS WATCHDOG &amp; EMAIL ALERT TIER</text>
      <text x="18" y="48" font-size="13.5" font-weight="700" fill="#7e22ce">• Cloudflare Worker: Serverless edge worker with 60s Cron Trigger</text>
      <text x="18" y="70" font-size="13.5" font-weight="600" fill="#334155">• Heartbeat Watchdog: Audits /latest/timestamp (Declares COMM_LOSS if &gt; 120s)</text>
      <text x="18" y="92" font-size="13.5" font-weight="600" fill="#334155">• Incident Webhook: Processes critical over-temperature &amp; electrical trip events</text>
      <text x="18" y="114" font-size="13.5" font-weight="700" fill="#dc2626">• Brevo Transactional Email API: Instant push alert delivery to engineers</text>
      <text x="18" y="136" font-size="13.5" font-weight="600" fill="#334155">• Diagnostic Email Content: Fault code, trip sensor values &amp; maintenance advice</text>
    </g>

    <!-- Clean Horizontal Inter-Cloud Connectors (Inside Card Body Gap) -->
    <path class="wire" stroke="#0284c7" stroke-width="3" marker-end="url(#arrow-cyan)" d="M 710 142 L 668 142"/>
    <rect x="668" y="130" width="40" height="24" rx="4" fill="#e0f2fe" stroke="#38bdf8" stroke-width="1"/>
    <text x="688" y="146" font-size="11" font-weight="800" fill="#0369a1" text-anchor="middle">SYNC</text>

    <path class="wire" stroke="#9333ea" stroke-width="3" marker-end="url(#arrow-purple)" d="M 1370 142 L 1411 142"/>
    <rect x="1372" y="130" width="40" height="24" rx="4" fill="#f3e8ff" stroke="#c084fc" stroke-width="1"/>
    <text x="1392" y="146" font-size="11" font-weight="800" fill="#7e22ce" text-anchor="middle">AUDIT</text>
  </g>


  <!-- ==================== TIER 2: LOCAL OPERATOR INTERFACE & NETWORK BOUNDARY ==================== -->
  <g transform="translate(60, 385)" filter="url(#shadow)">
    <rect width="2080" height="235" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="2"/>
    <rect width="2080" height="40" rx="12" fill="#065f46"/>
    <rect x="0" y="30" width="2080" height="10" fill="#065f46"/>
    <text x="24" y="26" font-size="17" font-weight="900" fill="#ffffff">TIER 2: LOCAL OPERATOR INTERFACE &amp; ACCESS BOUNDARY</text>

    <!-- Sub-Block A: Offline LittleFS Dashboard (w=600, ends at global x=684) -->
    <g transform="translate(24, 55)">
      <rect width="600" height="165" rx="8" fill="#f0fdf4" stroke="#bbf7d0" stroke-width="1.5"/>
      <text x="18" y="26" font-size="17" font-weight="900" fill="#065f46">EMBEDDED LITTLEFS OFFLINE DASHBOARD</text>
      <text x="18" y="48" font-size="13" font-weight="700" fill="#059669">• 100% Zero-Dependency Offline Web Server in ESP32 flash</text>
      <text x="18" y="70" font-size="13" font-weight="600" fill="#334155">• Access via SoftAP (http://192.168.4.1) or local station IP</text>
      <text x="18" y="92" font-size="13" font-weight="600" fill="#334155">• Full live gauges, temperatures, rail metrics, and fan controls</text>
      <text x="18" y="114" font-size="13" font-weight="600" fill="#334155">• Operational during total internet or cloud infrastructure outages</text>
      <text x="18" y="136" font-size="13" font-weight="700" fill="#047857">• Instant local fallback: Zero external CDN assets required</text>
    </g>

    <!-- Sub-Block B: Physical Operator Switches (starts at global x=800, w=620) -->
    <g transform="translate(740, 55)">
      <rect width="620" height="165" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
      <text x="18" y="26" font-size="17" font-weight="900" fill="#0f172a">PHYSICAL TOGGLE SWITCHES (GPIO 18 / 23)</text>
      <text x="18" y="48" font-size="13" font-weight="700" fill="#1e293b">• Main Output Enable Switch (GPIO 18): Closed to GND = Run request</text>
      <text x="18" y="70" font-size="13" font-weight="600" fill="#475569">• Safety Invariant: Maintained ON switch never bypasses software trips</text>
      <text x="18" y="92" font-size="13" font-weight="700" fill="#2563eb">• SoftAP Setup Switch (GPIO 23): Closed to GND = Launch "ESP32-TMS-SETUP"</text>
      <text x="18" y="114" font-size="13" font-weight="600" fill="#475569">• Captive portal for local Wi-Fi router credential provisioning</text>
      <text x="18" y="136" font-size="13" font-weight="700" fill="#0f172a">• Debounced: 50 ms filter in software eliminates mechanical chatter</text>
    </g>

    <!-- Sub-Block C: 16x2 Character LCD (Standby Powered) -->
    <g transform="translate(1415, 55)">
      <rect width="640" height="165" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
      <text x="18" y="26" font-size="17" font-weight="900" fill="#0f172a">16x2 CHARACTER LCD (STANDBY POWERED)</text>
      <text x="18" y="48" font-size="13.5" font-weight="700" fill="#7e22ce">• Powered 24/7 via ATX +5VSB Standby Rail (I2C Backpack @ 0x27)</text>
      <text x="18" y="70" font-size="13.5" font-weight="600" fill="#334155">• Screen 1: Core Temp (T1), Ambient (T2), Delta (dT), Projected Temp (Tp)</text>
      <text x="18" y="92" font-size="13.5" font-weight="600" fill="#334155">• Screen 2: System Status (Main: ON / DE-ENERGIZED), Fan Duty %, Trip Code</text>
      <text x="18" y="114" font-size="13.5" font-weight="700" fill="#059669">• Remains lit and displays "FAULT: OVERTEMP" even after ATX rails collapse</text>
      <text x="18" y="136" font-size="13.5" font-weight="600" fill="#475569">• Non-blocking update task decoupled from sensor acquisition loop</text>
    </g>
  </g>


  <!-- ==================== TIER 3: EMBEDDED FIRMWARE LAYER (ESP32) ==================== -->
  <g transform="translate(60, 660)" filter="url(#shadow)">
    <rect width="2080" height="300" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="2"/>
    <rect width="2080" height="40" rx="12" fill="#1e3a8a"/>
    <rect x="0" y="30" width="2080" height="10" fill="#1e3a8a"/>
    <text x="24" y="26" font-size="17" font-weight="900" fill="#ffffff">TIER 3: EMBEDDED FIRMWARE EXECUTION LAYER (ESP32-WROOM-32 FREERTOS ENGINE)</text>

    <!-- Pipeline 1: Sensor HAL & Acquisition -->
    <g transform="translate(24, 55)">
      <rect width="490" height="225" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
      <text x="18" y="26" font-size="16.5" font-weight="900" fill="#1e3a8a">1. ACQUISITION &amp; SENSOR HAL</text>
      <text x="18" y="50" font-size="13.5" font-weight="600" fill="#334155">• Non-blocking 1-Wire DS18B20 12-bit read</text>
      <text x="18" y="74" font-size="13.5" font-weight="600" fill="#334155">• I2C 400 kHz fast-mode poller for 3x INA219</text>
      <text x="18" y="98" font-size="13.5" font-weight="600" fill="#334155">• Data validity flags &amp; CRC error gate</text>
      <text x="18" y="122" font-size="13.5" font-weight="600" fill="#334155">• Bus timeout monitor (&gt; 500 ms triggers trip)</text>
      <text x="18" y="146" font-size="13.5" font-weight="600" fill="#334155">• Temperature differential: ΔT = T_core - T_inlet</text>
      <text x="18" y="174" font-size="13" font-weight="700" fill="#2563eb">Strict real-time execution priority (1.00s tick)</text>
    </g>

    <!-- Pipeline 2: Mathematical Prediction Engine -->
    <g transform="translate(538, 55)">
      <rect width="490" height="225" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
      <text x="18" y="26" font-size="16.5" font-weight="900" fill="#4338ca">2. MATHEMATICAL PREDICTOR</text>
      <text x="18" y="50" font-size="13.5" font-weight="700" fill="#0f172a">• EMA Filter: T_f(k) = 0.20·T(k) + 0.80·T_f(k-1)</text>
      <text x="18" y="74" font-size="13.5" font-weight="600" fill="#334155">• Rolling 30s FIFO regression buffer (N = 30)</text>
      <text x="18" y="98" font-size="13.5" font-weight="700" fill="#0f172a">• Least-Squares Slope: r = dT/dt (°C/second)</text>
      <text x="18" y="122" font-size="13.5" font-weight="700" fill="#2563eb">• Forward Projection: T_p = T_f + 30.0·max(0, r)</text>
      <text x="18" y="146" font-size="13.5" font-weight="600" fill="#334155">• Dual Demand: D_auto = max(g(T_f), g(T_p))</text>
      <text x="18" y="170" font-size="13.5" font-weight="700" fill="#d97706">• Slew Limiter: Instant rise, ≤1%/s descent</text>
      <text x="18" y="194" font-size="12.5" font-weight="600" fill="#475569">Anti-stall 30% duty floor prevents motor buzz</text>
    </g>

    <!-- Pipeline 3: Supervisory Protection State Machine -->
    <g transform="translate(1052, 55)">
      <rect width="490" height="225" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
      <text x="18" y="26" font-size="16.5" font-weight="900" fill="#991b1b">3. SUPERVISORY PROTECTION</text>
      <text x="18" y="50" font-size="13.5" font-weight="700" fill="#dc2626">• Overcurrent: 12V &gt; 3.15A | 5V &gt; 1A | 3.3V &gt; 1A</text>
      <text x="18" y="74" font-size="13.5" font-weight="700" fill="#dc2626">• Thermal Trip: T_core ≥ 65°C OR T_p ≥ 70°C</text>
      <text x="18" y="98" font-size="13.5" font-weight="600" fill="#334155">• 500 ms inrush blanking suppresses start spikes</text>
      <text x="18" y="122" font-size="13.5" font-weight="600" fill="#334155">• Fast Cutoff: GPIO 32 pulled LOW (&lt; 5 ms)</text>
      <text x="18" y="146" font-size="13.5" font-weight="600" fill="#334155">• 10-State Machine (STANDBY_OFF, RUNNING, etc.)</text>
      <text x="18" y="170" font-size="13.5" font-weight="700" fill="#059669">• Qualified Auto-Recovery vs Permanent Lockout</text>
      <text x="18" y="194" font-size="12.5" font-weight="600" fill="#475569">Persistent fault snapshot logged to ESP32 NVS</text>
    </g>

    <!-- Pipeline 4: Communication & Cloud Dispatch -->
    <g transform="translate(1566, 55)">
      <rect width="490" height="225" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
      <text x="18" y="26" font-size="16.5" font-weight="900" fill="#065f46">4. COMMUNICATIONS &amp; DISPATCH</text>
      <text x="18" y="50" font-size="13.5" font-weight="600" fill="#334155">• 10s HTTPS telemetry publisher to Firebase RTDB</text>
      <text x="18" y="74" font-size="13.5" font-weight="600" fill="#334155">• 120-minute circular RAM buffer for outage backfill</text>
      <text x="18" y="98" font-size="13.5" font-weight="600" fill="#334155">• Non-blocking Wi-Fi station reconnection</text>
      <text x="18" y="122" font-size="13.5" font-weight="600" fill="#334155">• Asynchronous remote command poller (≤ 5s)</text>
      <text x="18" y="146" font-size="13.5" font-weight="600" fill="#334155">• 25 kHz LEDC PWM output to TB6612 driver</text>
      <text x="18" y="170" font-size="13.5" font-weight="600" fill="#334155">• 16x2 I2C LCD dual-screen refresh cycler</text>
      <text x="18" y="194" font-size="12.5" font-weight="700" fill="#059669">Safety invariants never block on network operations</text>
    </g>
  </g>


  <!-- ==================== TIER 4: PHYSICAL HARDWARE & POWER DOMAIN (BOTTOM) ==================== -->
  <g transform="translate(60, 1025)" filter="url(#shadow)">
    <rect width="2080" height="325" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="2"/>
    <rect width="2080" height="40" rx="12" fill="#1e293b"/>
    <rect x="0" y="30" width="2080" height="10" fill="#1e293b"/>
    <text x="24" y="26" font-size="17" font-weight="900" fill="#ffffff">TIER 4: PHYSICAL HARDWARE, SENSORS &amp; POWER ACTUATION LAYER</text>

    <!-- Hardware Box 1: ATX SMPS & PS_ON# Switch -->
    <g transform="translate(24, 55)">
      <rect width="640" height="250" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
      <text x="18" y="26" font-size="17" font-weight="900" fill="#0f172a">ATX POWER SUPPLY &amp; HARDWARE INTERLOCK</text>
      
      <g transform="translate(18, 48)" font-size="13.5" font-weight="600" fill="#334155">
        <text x="0" y="20" font-weight="800" fill="#0f172a">• ATX Breakout (XH-M229):</text>
        <text x="200" y="20">Primary 230V AC input; secondary binding posts</text>

        <text x="0" y="44" font-weight="800" fill="#d97706">• Switched +12V DC Rail:</text>
        <text x="200" y="44">Powers 12V 50W Dummy Load &amp; TB6612 VM motor power</text>

        <text x="0" y="68" font-weight="800" fill="#dc2626">• Switched +5V DC Rail:</text>
        <text x="200" y="68">Secondary ATX power rail monitored via INA219 #2</text>

        <text x="0" y="92" font-weight="800" fill="#ea580c">• Switched +3.3V DC Rail:</text>
        <text x="200" y="92">Secondary ATX power rail monitored via INA219 #3</text>

        <text x="0" y="116" font-weight="800" fill="#9333ea">• Standby +5VSB Rail:</text>
        <text x="200" y="116" font-weight="700" fill="#7e22ce">24/7 continuous supply to ESP32 VIN &amp; LCD VCC</text>

        <text x="0" y="140" font-weight="800" fill="#059669">• PS_ON# Interlock:</text>
        <text x="200" y="140">BC547 NPN + 1k base resistor + 10k pull-down to GND</text>

        <text x="0" y="170" font-weight="700" fill="#059669">Hardware failsafe: Transistor defaults OFF (rails cut) during MCU reboot</text>
      </g>
    </g>

    <!-- Hardware Box 2: Sensors & Probes -->
    <g transform="translate(710, 55)">
      <rect width="660" height="250" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
      <text x="18" y="26" font-size="17" font-weight="900" fill="#0f172a">MULTI-RAIL SENSORS &amp; TEMPERATURE PROBES</text>
      
      <g transform="translate(18, 48)" font-size="13.5" font-weight="600" fill="#334155">
        <text x="0" y="20" font-weight="800" fill="#581c87">• INA219 #1 (12V @ 0x40):</text>
        <text x="210" y="20">0.1 Ω shunt monitors 12V bus voltage, load current, power</text>

        <text x="0" y="44" font-weight="800" fill="#581c87">• INA219 #2 (5V @ 0x41):</text>
        <text x="210" y="44">0.1 Ω shunt monitors native 5V bus voltage &amp; current</text>

        <text x="0" y="68" font-weight="800" fill="#581c87">• INA219 #3 (3.3V @ 0x44):</text>
        <text x="210" y="68">0.1 Ω shunt monitors native 3.3V bus voltage &amp; current</text>

        <text x="0" y="92" font-weight="800" fill="#1e3a8a">• DS18B20 Probe 1 (Core):</text>
        <text x="210" y="92">Surface-mounted probe measures transformer core temp T_core</text>

        <text x="0" y="116" font-weight="800" fill="#1e3a8a">• DS18B20 Probe 2 (Inlet):</text>
        <text x="210" y="116">Intake reference probe measures ambient air inlet temp T_inlet</text>

        <text x="0" y="140" font-weight="800" fill="#0f172a">• Bus Topologies:</text>
        <text x="210" y="140">Shared I2C bus (GPIO 21/22) + 1-Wire DQ bus (GPIO 27)</text>

        <text x="0" y="170" font-weight="700" fill="#0f172a">All sensor returns connect via secondary star-ground topology</text>
      </g>
    </g>

    <!-- Hardware Box 3: Electrical Load & Actuation -->
    <g transform="translate(1415, 55)">
      <rect width="640" height="250" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
      <text x="18" y="26" font-size="17" font-weight="900" fill="#0f172a">ELECTRICAL LOAD &amp; ACTIVE COOLING ACTUATION</text>
      
      <g transform="translate(18, 48)" font-size="13.5" font-weight="600" fill="#334155">
        <text x="0" y="20" font-weight="800" fill="#d97706">• 12V Dummy Load Resistor:</text>
        <text x="220" y="20">10 Ω, 50W aluminum housed wirewound load resistor</text>

        <text x="0" y="44" font-weight="800" fill="#d97706">• Continuous Load Draw:</text>
        <text x="220" y="44">12.0 V DC • 1.20 A (14.4 W) secondary electrical loading</text>

        <text x="0" y="68" font-weight="800" fill="#991b1b">• TB6612FNG Driver:</text>
        <text x="220" y="68">Dual power MOSFET H-bridge (VM from 12V, VCC from 3.3V)</text>

        <text x="0" y="92" font-weight="800" fill="#991b1b">• PWM Speed Modulation:</text>
        <text x="220" y="92">Ultrasonic 25 kHz PWM driven by ESP32 GPIO 25 (PWMA)</text>

        <text x="0" y="116" font-weight="800" fill="#0f172a">• 12V DC Cooling Fan:</text>
        <text x="220" y="116">Brushless DC blower fan modulates airflow across transformer</text>

        <text x="0" y="140" font-weight="800" fill="#0f172a">• Dynamic Response:</text>
        <text x="220" y="140">Instant acceleration on thermal rise; slew-rate descent</text>

        <text x="0" y="170" font-weight="700" fill="#059669">Pre-cools transformer proactively before hot-spot limit is breached</text>
      </g>
    </g>
  </g>


  <!-- ==================== 100% COLLISION-FREE INTER-TIER BUS LINES ==================== -->
  
  <!-- Gap between Tier 3 (y=960) and Tier 4 (y=1025) is 65px! Clean space for badges at y=992 -->

  <!-- Physical to Firmware: Sensors to Acquisition (Blue) -->
  <path class="wire" stroke="#0284c7" stroke-width="4" marker-end="url(#arrow-cyan)"
        d="M 1040 1025 L 1040 960"/>
  <rect x="970" y="980" width="140" height="26" rx="5" fill="#f0f9ff" stroke="#38bdf8" stroke-width="1.5"/>
  <text x="1040" y="998" font-size="12" font-weight="800" fill="#0284c7" text-anchor="middle">I2C / 1-WIRE DATA</text>

  <!-- Firmware to Physical: GPIO 32 to BC547 PS_ON# Cutoff (Green) -->
  <path class="wire" stroke="#059669" stroke-width="4" marker-end="url(#arrow-green)"
        d="M 350 960 L 350 1025"/>
  <rect x="275" y="980" width="150" height="26" rx="5" fill="#ecfdf5" stroke="#34d399" stroke-width="1.5"/>
  <text x="350" y="998" font-size="12" font-weight="800" fill="#059669" text-anchor="middle">GPIO 32 PS_ON# CUTOFF</text>

  <!-- Firmware to Physical: PWM Fan Drive (Purple) -->
  <path class="wire" stroke="#9333ea" stroke-width="4" marker-end="url(#arrow-purple)"
        d="M 1730 960 L 1730 1025"/>
  <rect x="1665" y="980" width="130" height="26" rx="5" fill="#faf5ff" stroke="#c084fc" stroke-width="1.5"/>
  <text x="1730" y="998" font-size="12" font-weight="800" fill="#7e22ce" text-anchor="middle">25 kHz FAN PWM</text>


  <!-- Gap between Tier 2 (y=620) and Tier 3 (y=660) is 40px! Clean space for LCD/Web UI -->
  <path class="wire" stroke="#0284c7" stroke-width="4" marker-end="url(#arrow-cyan)"
        d="M 1730 660 L 1730 620"/>
  <rect x="1650" y="627" width="160" height="26" rx="5" fill="#f0f9ff" stroke="#38bdf8" stroke-width="1.5"/>
  <text x="1730" y="645" font-size="12" font-weight="800" fill="#0369a1" text-anchor="middle">LCD &amp; WEB UI FEED</text>


  <!-- Firmware to Cloud: HTTPS Telemetry via Clean Open Vertical Channel between Sub-Block A (ends at 684) and Sub-Block B (starts at 800) -->
  <!-- Channel centerline is exactly x=742 (116px wide empty corridor) -->
  <path class="wire" stroke="#ea580c" stroke-width="4" marker-end="url(#arrow-orange)"
        d="M 742 660 L 742 215 L 770 215"/>
  <!-- Telemetry Badge positioned neatly inside the open gap between Tier 2 cards -->
  <g transform="translate(742, 500)">
    <rect x="-52" y="-14" width="104" height="28" rx="6" fill="#fff7ed" stroke="#fb923c" stroke-width="1.5"/>
    <text x="0" y="5" font-size="11" font-weight="900" fill="#c2410c" text-anchor="middle">10s TELEMETRY</text>
  </g>

</svg>'''

    out_svg = os.path.join("documentation", "diagram_3_combined_architecture_block.svg")
    with open(out_svg, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Generated {out_svg}")

    # Compile to high-res PNG via typst
    typ_path = os.path.join("documentation", "render_diag3.typ")
    png_path = os.path.join("documentation", "diagram_3_combined_architecture_block.png")
    typst_exe = os.path.join("documentation", "bin", "typst.exe")
    with open(typ_path, "w", encoding="utf-8") as f:
        f.write('#set page(width: 2200pt, height: 1400pt, margin: 0pt)\n#image("diagram_3_combined_architecture_block.svg", width: 100%)\n')
    subprocess.run([typst_exe, "compile", "--format", "png", "--ppi", "150", typ_path, png_path], check=True)
    if os.path.exists(typ_path):
        os.remove(typ_path)
    print(f"Compiled {png_path}")

if __name__ == "__main__":
    generate_diagram_3()
