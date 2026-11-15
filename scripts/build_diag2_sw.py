# -*- coding: utf-8 -*-
"""
Diagram 2 Generator: Software & Cloud Architecture Block Diagram (Rev 2 - Zero Wire Crossings)
"""

import os
import subprocess

def generate_diagram_2():
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
    <text font-size="32" font-weight="900" fill="#0f172a" letter-spacing="-0.5px">IoT Transformer Condition Monitoring System — Software &amp; Cloud Architecture</text>
    <text font-size="18" font-weight="700" fill="#64748b" y="32">Firmware Subsystem Pipelines, Mathematical Prediction Engine &amp; Firebase Cloud Ecosystem</text>
  </g>

  <!-- ==================== COLUMN 1: ESP32 FIRMWARE SUBSYSTEMS (LEFT) ==================== -->
  
  <g transform="translate(60, 120)" filter="url(#shadow)">
    <rect width="1020" height="1220" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="2"/>
    <rect width="1020" height="52" rx="12" fill="#0f172a"/>
    <rect x="0" y="42" width="1020" height="10" fill="#0f172a"/>
    <text x="24" y="34" font-size="22" font-weight="900" fill="#f8fafc">ESP32 EMBEDDED FIRMWARE ARCHITECTURE (LOCAL FREERTOS CORE)</text>
    <text x="24" y="80" font-size="15" font-weight="700" fill="#64748b">Non-Blocking Real-Time Multi-Task Scheduling • Autonomous 24/7 Standby Operation</text>

    <!-- Sub-Block 1: Hardware Abstraction & Sensor Acquisition -->
    <g transform="translate(24, 98)">
      <rect width="972" height="240" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
      <rect width="972" height="38" rx="8" fill="#1e3a8a"/>
      <rect x="0" y="30" width="972" height="8" fill="#1e3a8a"/>
      <text x="18" y="25" font-size="17" font-weight="900" fill="#f8fafc">1. HARDWARE DRIVERS &amp; SENSOR ACQUISITION SUBSYSTEM</text>

      <g transform="translate(20, 52)" font-size="14" font-weight="600" fill="#334155">
        <text x="0" y="24" font-weight="800" fill="#1e40af">• DS18B20 1-Wire Driver:</text>
        <text x="200" y="24">Non-blocking 12-bit async conversion (750 ms). Reads T_core and T_inlet</text>

        <text x="0" y="52" font-weight="800" fill="#1e40af">• INA219 I2C Poller:</text>
        <text x="200" y="52">Fast-Mode 400 kHz multi-device poller (12V @ 0x40, 5V @ 0x41, 3.3V @ 0x44)</text>

        <text x="0" y="80" font-weight="800" fill="#1e40af">• TB6612 LEDC PWM:</text>
        <text x="200" y="80">25 kHz ultrasonic PWM generation with smooth hardware duty updates</text>

        <text x="0" y="108" font-weight="800" fill="#1e40af">• LCD Display Driver:</text>
        <text x="200" y="108">I2C 16x2 backpack driver (0x27) with non-blocking dual-screen carousel</text>

        <text x="0" y="136" font-weight="800" fill="#1e40af">• Switch Debounce:</text>
        <text x="200" y="136">50 ms software debouncing for Main Output Enable (18) &amp; Setup (23) toggles</text>

        <text x="0" y="164" font-weight="800" fill="#1e40af">• PS_ON# Gate Driver:</text>
        <text x="200" y="164">GPIO 32 discrete drive (HIGH = Energize ATX, LOW = Immediate Cutoff &lt; 5 ms)</text>
      </g>
    </g>

    <!-- Sub-Block 2: Real-Time Mathematics & Predictive Thermal Engine -->
    <g transform="translate(24, 355)">
      <rect width="972" height="295" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
      <rect width="972" height="38" rx="8" fill="#4338ca"/>
      <rect x="0" y="30" width="972" height="8" fill="#4338ca"/>
      <text x="18" y="25" font-size="17" font-weight="900" fill="#f8fafc">2. REAL-TIME MATHEMATICS &amp; PREDICTIVE THERMAL ENGINE</text>

      <g transform="translate(20, 52)" font-size="14" font-weight="600" fill="#334155">
        <text x="0" y="24" font-weight="800" fill="#4338ca">• Quality &amp; CRC Gate:</text>
        <text x="220" y="24">Discards corrupted scratchpad readings; prevents false outlier excursions</text>

        <text x="0" y="52" font-weight="800" fill="#4338ca">• Digital Noise Filter:</text>
        <text x="220" y="52" font-weight="700" fill="#0f172a">Exponential Moving Average: T_f(k) = 0.20 · T(k) + 0.80 · T_f(k-1)</text>

        <text x="0" y="80" font-weight="800" fill="#4338ca">• Rolling Regression Buffer:</text>
        <text x="220" y="80">Circular 30-sample rolling FIFO array (N = 30 valid samples across 30 seconds)</text>

        <text x="0" y="108" font-weight="800" fill="#4338ca">• Least-Squares Slope (r):</text>
        <text x="220" y="108" font-weight="700" fill="#0f172a">r = Σ[(t_i - t_avg)(T_fi - T_favg)] / Σ(t_i - t_avg)² (rate of rise in °C/sec)</text>

        <text x="0" y="136" font-weight="800" fill="#4338ca">• Forward Projection (T_p):</text>
        <text x="220" y="136" font-weight="700" fill="#2563eb">T_p = T_f + 30.0 · max(0, r) [30-second predictive forward horizon]</text>

        <text x="0" y="164" font-weight="800" fill="#4338ca">• Dual-Demand Mapping:</text>
        <text x="220" y="164" font-weight="700" fill="#059669">D_auto = max(g(T_f), g(T_p)) [Piecewise duty curve with anti-stall 30% floor]</text>

        <text x="0" y="192" font-weight="800" fill="#4338ca">• Slew-Rate Limiter:</text>
        <text x="220" y="192" font-weight="700" fill="#d97706">Instant acceleration on rise; rate-limited descent (≤ 1%/sec) prevents acoustic hunting</text>

        <text x="0" y="220" font-weight="800" fill="#4338ca">• Thermal Rise Delta:</text>
        <text x="220" y="220">ΔT = T_core - T_inlet (Dynamic thermal resistance metric for ambient normalization)</text>
      </g>
    </g>

    <!-- Sub-Block 3: Supervisory Protection & 10-State Machine -->
    <g transform="translate(24, 668)">
      <rect width="972" height="260" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
      <rect width="972" height="38" rx="8" fill="#991b1b"/>
      <rect x="0" y="30" width="972" height="8" fill="#991b1b"/>
      <text x="18" y="25" font-size="17" font-weight="900" fill="#f8fafc">3. SUPERVISORY PROTECTION ENGINE &amp; 10-STATE MACHINE</text>

      <g transform="translate(20, 52)" font-size="14" font-weight="600" fill="#334155">
        <text x="0" y="24" font-weight="800" fill="#991b1b">• Multi-Rail Trip Evaluator:</text>
        <text x="220" y="24" font-weight="700" fill="#dc2626">Overcurrent: 12V &gt; 3.15 A, 5V &gt; 1.0 A, 3.3V &gt; 1.0 A | Voltage Window: ±10%</text>

        <text x="0" y="52" font-weight="800" fill="#991b1b">• Thermal Trip Evaluator:</text>
        <text x="220" y="52" font-weight="700" fill="#dc2626">Absolute Core Trip: T_core ≥ 65.0°C | Predictive Horizon Trip: T_p ≥ 70.0°C</text>

        <text x="0" y="80" font-weight="800" fill="#991b1b">• Inrush Blanking Window:</text>
        <text x="220" y="80">500 ms blanking on startup ignores decoupling capacitor inrush transients</text>

        <text x="0" y="108" font-weight="800" fill="#991b1b">• Voltage Collapse Gate:</text>
        <text x="220" y="108">Confirms rail collapse (&lt; 1.0V) within 500 ms post-trip; flags failure if stuck</text>

        <text x="0" y="136" font-weight="800" fill="#991b1b">• 10-State Power Machine:</text>
        <text x="220" y="136">STANDBY_OFF, STARTING, RUNNING, MANUAL_OFF, ELEC_LOCKOUT, THERMAL_COOL, etc.</text>

        <text x="0" y="164" font-weight="800" fill="#991b1b">• Recovery Strategy:</text>
        <text x="220" y="164" font-weight="700" fill="#059669">Thermal: Qualified auto-restart after cooldown | Electrical: Latched permanently</text>

        <text x="0" y="192" font-weight="800" fill="#991b1b">• Persistent NVS Store:</text>
        <text x="220" y="192">Commits trip code, timestamp, and sensor snapshot to Non-Volatile Flash Memory</text>
      </g>
    </g>

    <!-- Sub-Block 4: Local Connectivity & Web Server -->
    <g transform="translate(24, 945)">
      <rect width="972" height="250" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
      <rect width="972" height="38" rx="8" fill="#065f46"/>
      <rect x="0" y="30" width="972" height="8" fill="#065f46"/>
      <text x="18" y="25" font-size="17" font-weight="900" fill="#f8fafc">4. LOCAL CONNECTIVITY &amp; EMBEDDED LITTLEFS SERVER</text>

      <g transform="translate(20, 52)" font-size="14" font-weight="600" fill="#334155">
        <text x="0" y="24" font-weight="800" fill="#065f46">• Embedded LittleFS Server:</text>
        <text x="220" y="24">Serves complete zero-dependency dashboard (HTML, CSS, JS) from internal flash</text>

        <text x="0" y="52" font-weight="800" fill="#065f46">• SoftAP Provisioning Mode:</text>
        <text x="220" y="52">SSID "ESP32-TMS-SETUP" @ 192.168.4.1 for entering home/lab router Wi-Fi credentials</text>

        <text x="0" y="80" font-weight="800" fill="#065f46">• Non-Blocking Wi-Fi:</text>
        <text x="220" y="80">Asynchronous station reconnection never delays or stalls the safety protection loop</text>

        <text x="0" y="108" font-weight="800" fill="#065f46">• Circular Outage Buffer:</text>
        <text x="220" y="108">120-minute RAM queue buffers telemetry frames during network drops for backfill</text>

        <text x="0" y="136" font-weight="800" fill="#065f46">• Firebase REST Client:</text>
        <text x="220" y="136" font-weight="700" fill="#2563eb">Pushes JSON telemetry frames every 10s via authenticated HTTPS PUT / PATCH</text>

        <text x="0" y="164" font-weight="800" fill="#065f46">• Remote Command Poller:</text>
        <text x="220" y="164">Polls /devices/&#123;id&#125;/commands every ≤ 5s for authorized remote emergency stop</text>
      </g>
    </g>
  </g>


  <!-- ==================== COLUMN 2: CLOUD & SERVERLESS WATCHDOG (CENTER-RIGHT) ==================== -->
  
  <g transform="translate(1110, 120)" filter="url(#shadow)">
    <rect width="600" height="1220" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="2"/>
    <rect width="600" height="52" rx="12" fill="#d97706"/>
    <rect x="0" y="42" width="600" height="10" fill="#d97706"/>
    <text x="24" y="34" font-size="22" font-weight="900" fill="#f8fafc">CLOUD &amp; SERVERLESS ECOSYSTEM</text>
    <text x="24" y="80" font-size="15" font-weight="700" fill="#64748b">Unified Firebase Stack + Cloudflare Watchdog &amp; Brevo Email Alerts</text>

    <!-- Cloud Card 1: Firebase Realtime Database -->
    <g transform="translate(24, 98)">
      <rect width="552" height="260" rx="8" fill="#fffbeb" stroke="#fde68a" stroke-width="2"/>
      <rect width="552" height="38" rx="8" fill="#d97706"/>
      <rect x="0" y="30" width="552" height="8" fill="#d97706"/>
      <text x="18" y="25" font-size="17" font-weight="900" fill="#ffffff">FIREBASE REALTIME DATABASE (RTDB)</text>
      
      <g transform="translate(18, 52)" font-size="14" font-weight="600" fill="#92400e">
        <text x="0" y="22" font-weight="800">• /devices/&#123;id&#125;/latest:</text>
        <text x="20" y="42">Real-time state, voltages, currents, power, temperatures (T1, T2, dT, Tp), fan PWM</text>

        <text x="0" y="70" font-weight="800">• /devices/&#123;id&#125;/history:</text>
        <text x="20" y="90">Persistent rolling hourly summaries, thermal trends, and fault incident records</text>

        <text x="0" y="118" font-weight="800">• /devices/&#123;id&#125;/commands:</text>
        <text x="20" y="138">Remote emergency power OFF, fault lockout reset, and configuration parameter queue</text>

        <text x="0" y="166" font-weight="800">• WebSocket Push Sync:</text>
        <text x="20" y="186" font-weight="700" fill="#b45309">Sub-second bidirectional updates to web dashboard via real-time WebSocket listeners</text>
      </g>
    </g>

    <!-- Native Inter-Firebase Arrow (RTDB to Hosting) -->
    <g transform="translate(300, 360)">
      <path class="wire" stroke="#0284c7" stroke-width="3.5" marker-end="url(#arrow-cyan)" d="M 0 0 L 0 15"/>
    </g>

    <!-- Cloud Card 2: Firebase Hosting (Unified SPA Web App) -->
    <g transform="translate(24, 380)">
      <rect width="552" height="255" rx="8" fill="#f0f9ff" stroke="#bae6fd" stroke-width="2"/>
      <rect width="552" height="38" rx="8" fill="#0284c7"/>
      <rect x="0" y="30" width="552" height="8" fill="#0284c7"/>
      <text x="18" y="25" font-size="17" font-weight="900" fill="#ffffff">FIREBASE HOSTING (INTERNET DASHBOARD)</text>
      
      <g transform="translate(18, 52)" font-size="14" font-weight="600" fill="#0369a1">
        <text x="0" y="22" font-weight="800">• Direct Computer Deployment:</text>
        <text x="20" y="42" font-weight="700" fill="#0284c7">Deployed directly via "firebase deploy" CLI — No GitHub Pages or Vercel required</text>

        <text x="0" y="70" font-weight="800">• Private Code Repository:</text>
        <text x="20" y="90">Source code stays private on GitHub; GitHub acts strictly as code backup</text>

        <text x="0" y="118" font-weight="800">• Unified Firebase Auth &amp; RTDB:</text>
        <text x="20" y="138">Native integration with Firebase Authentication login &amp; RTDB streaming</text>

        <text x="0" y="166" font-weight="800">• Global CDN &amp; Automated SSL:</text>
        <text x="20" y="186">Fast global single-page application delivery with automated SSL certificates</text>
      </g>
    </g>

    <!-- Cloud Card 3: Cloudflare Worker Watchdog -->
    <g transform="translate(24, 652)">
      <rect width="552" height="260" rx="8" fill="#faf5ff" stroke="#e9d5ff" stroke-width="2"/>
      <rect width="552" height="38" rx="8" fill="#7e22ce"/>
      <rect x="0" y="30" width="552" height="8" fill="#7e22ce"/>
      <text x="18" y="25" font-size="17" font-weight="900" fill="#ffffff">CLOUDFLARE WORKER (SERVERLESS WATCHDOG)</text>
      
      <g transform="translate(18, 52)" font-size="14" font-weight="600" fill="#6b21a8">
        <text x="0" y="22" font-weight="800">• Scheduled Cron Trigger:</text>
        <text x="20" y="42">Fires every 60 seconds to audit /latest/timestamp for communication loss</text>

        <text x="0" y="70" font-weight="800">• Heartbeat Watchdog Alert:</text>
        <text x="20" y="90" font-weight="700" fill="#9333ea">If ESP32 is silent &gt; 120s, declares COMM_LOSS and dispatches urgent email</text>

        <text x="0" y="118" font-weight="800">• Incident Webhook Consumer:</text>
        <text x="20" y="138">Receives critical trip payloads from Firebase and prepares diagnostic report</text>

        <text x="0" y="166" font-weight="800">• Lightweight Edge Execution:</text>
        <text x="20" y="186">Executes within 5 ms globally with zero server maintenance or hosting overhead</text>
      </g>
    </g>

    <!-- Direct Trigger Arrow (Worker to Brevo) -->
    <g transform="translate(300, 915)">
      <path class="wire" stroke="#dc2626" stroke-width="3.5" marker-end="url(#arrow-red)" d="M 0 0 L 0 15"/>
    </g>

    <!-- Cloud Card 4: Brevo Email Service -->
    <g transform="translate(24, 935)">
      <rect width="552" height="260" rx="8" fill="#fef2f2" stroke="#fecaca" stroke-width="2"/>
      <rect width="552" height="38" rx="8" fill="#dc2626"/>
      <rect x="0" y="30" width="552" height="8" fill="#dc2626"/>
      <text x="18" y="25" font-size="17" font-weight="900" fill="#ffffff">BREVO TRANSACTIONAL EMAIL SERVICE</text>
      
      <g transform="translate(18, 52)" font-size="14" font-weight="600" fill="#991b1b">
        <text x="0" y="22" font-weight="800">• Authenticated REST API:</text>
        <text x="20" y="42">Invoked securely by Cloudflare Worker over HTTPS using secret API credentials</text>

        <text x="0" y="70" font-weight="800">• Urgent Trip Notifications:</text>
        <text x="20" y="90" font-weight="700" fill="#dc2626">Delivers instantaneous transactional emails on over-temperature or electrical trips</text>

        <text x="0" y="118" font-weight="800">• Structured Diagnostic Payload:</text>
        <text x="20" y="138">Includes fault code, measured temperatures, rail currents, and maintenance advisory</text>

        <text x="0" y="166" font-weight="800">• Reliable Delivery SLA:</text>
        <text x="20" y="186">High deliverability directly to maintenance engineer inboxes and SMS gateways</text>
      </g>
    </g>
  </g>


  <!-- ==================== COLUMN 3: OPERATOR ACCESS & CLIENTS (RIGHT) ==================== -->
  
  <g transform="translate(1740, 120)" filter="url(#shadow)">
    <rect width="400" height="1220" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="2"/>
    <rect width="400" height="52" rx="12" fill="#334155"/>
    <rect x="0" y="42" width="400" height="10" fill="#334155"/>
    <text x="24" y="34" font-size="20" font-weight="900" fill="#f8fafc">OPERATOR ACCESS TIERS</text>
    <text x="24" y="80" font-size="15" font-weight="700" fill="#64748b">Local Offline &amp; Global Internet Access</text>

    <!-- Client Card 1: Offline Local Dashboard -->
    <g transform="translate(20, 98)">
      <rect width="360" height="340" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
      <rect width="360" height="36" rx="8" fill="#065f46"/>
      <rect x="0" y="28" width="360" height="8" fill="#065f46"/>
      <text x="16" y="24" font-size="16" font-weight="900" fill="#ffffff">OFFLINE LOCAL DASHBOARD</text>

      <g transform="translate(16, 52)" font-size="14" font-weight="600" fill="#334155">
        <text x="0" y="20" font-weight="800" fill="#065f46">Hosted directly on ESP32 LittleFS</text>
        <text x="0" y="48">• Connect via SoftAP or Local LAN</text>
        <text x="0" y="74">• Access via http://192.168.4.1</text>
        <text x="0" y="100">• 100% Zero Internet Dependency</text>
        <text x="0" y="126">• Live SVG gauges &amp; thermal trend</text>
        <text x="0" y="152">• Manual fan override &amp; trip reset</text>
        <text x="0" y="178">• Wi-Fi setup &amp; NVS configuration</text>
        <text x="0" y="210" font-weight="700" fill="#059669">Remains fully operational during total cloud or internet outages</text>
      </g>
    </g>

    <!-- Client Card 2: Internet Web Dashboard (Firebase Hosting) -->
    <g transform="translate(20, 460)">
      <rect width="360" height="375" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
      <rect width="360" height="36" rx="8" fill="#0284c7"/>
      <rect x="0" y="28" width="360" height="8" fill="#0284c7"/>
      <text x="16" y="24" font-size="16" font-weight="900" fill="#ffffff">INTERNET DASHBOARD (FIREBASE)</text>

      <g transform="translate(16, 52)" font-size="14" font-weight="600" fill="#334155">
        <text x="0" y="20" font-weight="800" fill="#0284c7">Hosted on Firebase Hosting</text>
        <text x="0" y="48">• Global access on smartphone/PC</text>
        <text x="0" y="74">• Secure Firebase Auth login</text>
        <text x="0" y="100">• Real-time WebSocket live sync</text>
        <text x="0" y="126">• Interactive multi-day charts</text>
        <text x="0" y="152">• Explainable maintenance advice</text>
        <text x="0" y="178">• Flashing red trip alert modal</text>
        <text x="0" y="204">• Authorized remote emergency stop</text>
        <text x="0" y="238" font-weight="700" fill="#0284c7">Deploys directly from computer</text>
        <text x="0" y="256" font-weight="700" fill="#0284c7">Private GitHub repository code backup</text>
      </g>
    </g>

    <!-- Client Card 3: Engineer Alert Inbox -->
    <g transform="translate(20, 855)">
      <rect width="360" height="340" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
      <rect width="360" height="36" rx="8" fill="#dc2626"/>
      <rect x="0" y="28" width="360" height="8" fill="#dc2626"/>
      <text x="16" y="24" font-size="16" font-weight="900" fill="#ffffff">ENGINEER ALERT INBOX</text>

      <g transform="translate(16, 52)" font-size="14" font-weight="600" fill="#334155">
        <text x="0" y="20" font-weight="800" fill="#dc2626">Urgent Push Email Delivery</text>
        <text x="0" y="48">• Immediate notification on trips</text>
        <text x="0" y="74">• Instant Heartbeat loss warning</text>
        <text x="0" y="100">• Contains trip snapshot data:</text>
        <text x="15" y="124" font-family="'JetBrains Mono', monospace" font-size="13" fill="#dc2626">T_Core: 66.2°C [TRIP]</text>
        <text x="15" y="146" font-family="'JetBrains Mono', monospace" font-size="13" fill="#dc2626">12V_I:  3.28A [TRIP]</text>
        <text x="15" y="168" font-family="'JetBrains Mono', monospace" font-size="13" fill="#0f172a">Action: PS_ON# Cut</text>
        <text x="0" y="204" font-weight="700" fill="#991b1b">Directly alerts on-call maintenance engineer without checking dashboard</text>
      </g>
    </g>
  </g>


  <!-- ==================== 100% COLLISION-FREE DATA FLOW INTERCONNECTS ==================== -->
  
  <!-- Path 1: ESP32 to Firebase RTDB (HTTPS PUT) -->
  <path class="wire" stroke="#d97706" stroke-width="4" marker-end="url(#arrow-orange)"
        d="M 1080 1080 L 1098 1080 L 1098 240 L 1130 240"/>
  <text x="1098" y="222" font-size="13" font-weight="800" fill="#d97706" text-anchor="middle">HTTPS 10s</text>

  <!-- Path 2: Firebase RTDB to Cloudflare Worker (Watchdog / Webhook) via Vertical Open Channel -->
  <path class="wire" stroke="#7e22ce" stroke-width="3.5" marker-end="url(#arrow-purple)"
        d="M 1665 240 L 1690 240 L 1690 770 L 1665 770"/>
  <text x="1705" y="500" font-size="13" font-weight="800" fill="#7e22ce" text-anchor="middle" transform="rotate(90 1705 500)">Cron Audit 60s</text>

  <!-- Path 3: Firebase Hosting to Internet Dashboard (WebSocket Live Sync) -->
  <path class="wire" stroke="#0284c7" stroke-width="4" marker-end="url(#arrow-cyan)"
        d="M 1665 510 L 1760 510"/>
  <text x="1712" y="498" font-size="13" font-weight="800" fill="#0284c7" text-anchor="middle">Live Sync</text>

  <!-- Path 4: Brevo to Engineer Alert Inbox -->
  <path class="wire" stroke="#dc2626" stroke-width="4" marker-end="url(#arrow-red)"
        d="M 1665 1060 L 1760 1060"/>
  <text x="1712" y="1048" font-size="13" font-weight="800" fill="#dc2626" text-anchor="middle">Email</text>

  <!-- Path 5: ESP32 to Offline Local Dashboard (Local Wi-Fi / SoftAP via Clean Open Floor) -->
  <path class="wire" stroke="#065f46" stroke-width="4" marker-end="url(#arrow-green)"
        d="M 1080 1195 L 1095 1195 L 1095 1360 L 1725 1360 L 1725 260 L 1760 260"/>
  <text x="1410" y="1378" font-size="15" font-weight="800" fill="#065f46" text-anchor="middle">Local Wi-Fi SoftAP / HTTP 192.168.4.1 (Zero Cloud Dependency)</text>

</svg>'''

    out_svg = os.path.join("documentation", "diagram_2_software_cloud_block.svg")
    with open(out_svg, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Generated {out_svg}")

    # Compile to high-res PNG via typst
    typ_path = os.path.join("documentation", "render_diag2.typ")
    png_path = os.path.join("documentation", "diagram_2_software_cloud_block.png")
    typst_exe = os.path.join("documentation", "bin", "typst.exe")
    with open(typ_path, "w", encoding="utf-8") as f:
        f.write('#set page(width: 2200pt, height: 1400pt, margin: 0pt)\n#image("diagram_2_software_cloud_block.svg", width: 100%)\n')
    subprocess.run([typst_exe, "compile", "--format", "png", "--ppi", "150", typ_path, png_path], check=True)
    if os.path.exists(typ_path):
        os.remove(typ_path)
    print(f"Compiled {png_path}")

if __name__ == "__main__":
    generate_diagram_2()
