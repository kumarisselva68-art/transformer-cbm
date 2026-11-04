# -*- coding: utf-8 -*-
"""
Diagram 6 Generator: Combined System Supervisory End-to-End Flowchart
Unifies:
1. Physical Hardware & Sensor Domain
2. Embedded FreeRTOS Processing & Predictive Thermal Engine
3. Multi-Tier Supervisory Gate: Normal Operation vs Critical Emergency Cutoff
4. Instant Hardware Failsafe Interlock (< 5 ms GPIO 32 Low -> PS_ON# Cutoff -> ATX Rail Collapse)
5. NVS Flash Fault Latching & Standby-Powered LCD Alert
6. Cloud Alert Propagation: Firebase RTDB -> Firebase Hosting Dashboard Alert + Cloudflare Worker -> Brevo Email API
"""

import os
import subprocess

def generate_diagram_6():
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
    <!-- Arrow Markers -->
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
    <text font-size="32" font-weight="900" fill="#0f172a" letter-spacing="-0.5px">IoT Transformer Condition Monitoring System — End-to-End Supervisory Flowchart</text>
    <text font-size="17" font-weight="700" fill="#64748b" y="28">Unified System Integration: Sensor Acquisition, Mathematical Prediction, Hardware Cutoff &amp; Multi-Tier Cloud Alert Dispatch</text>
  </g>

  <!-- ==================== STAGE 1: PHYSICAL SENSING & HARDWARE ACQUISITION (TOP ROW) ==================== -->
  
  <!-- Block 1A: Physical Hardware Domain -->
  <g transform="translate(60, 105)" filter="url(#shadow)">
    <rect width="680" height="155" rx="10" fill="#ffffff" stroke="#1e293b" stroke-width="2.5"/>
    <rect width="680" height="34" rx="10" fill="#1e293b"/>
    <rect x="0" y="24" width="680" height="10" fill="#1e293b"/>
    <text x="18" y="24" font-size="16" font-weight="900" fill="#ffffff">PHASE 1: PHYSICAL HARDWARE SENSING &amp; POWER MONITORING</text>
    <text x="18" y="56" font-size="13.5" font-weight="700" fill="#0f172a">• ATX Breakout (XH-M229): Switched +12V, +5V, +3.3V Rails &amp; Standby +5VSB (24/7)</text>
    <text x="18" y="78" font-size="13.5" font-weight="600" fill="#334155">• Dual DS18B20 1-Wire Digital Probes: Core Temp (T1) on winding + Inlet Temp (T2)</text>
    <text x="18" y="100" font-size="13.5" font-weight="600" fill="#334155">• 3x INA219 High-Side Power Monitors: Continuous bus voltage, load current, power</text>
    <text x="18" y="122" font-size="13.5" font-weight="700" fill="#059669">• Electrical Loading: 12V 50W Aluminum Housed Dummy Load (12.0V • 1.20A = 14.4W)</text>
    <text x="18" y="142" font-size="12" font-weight="600" fill="#64748b">Primary 230V AC mains converted via switched-mode topology with star-ground reference</text>
  </g>

  <!-- Arrow Phase 1 -> Phase 2 -->
  <path class="wire" stroke="#0284c7" stroke-width="3.5" marker-end="url(#arrow-cyan)" d="M 740 182 L 830 182"/>
  <rect x="752" y="170" width="65" height="24" rx="4" fill="#f0f9ff" stroke="#38bdf8" stroke-width="1.5"/>
  <text x="784" y="186" font-size="11" font-weight="800" fill="#0284c7" text-anchor="middle">1 Hz TICK</text>

  <!-- Block 1B: Embedded FreeRTOS Processing Engine -->
  <g transform="translate(830, 105)" filter="url(#shadow)">
    <rect width="700" height="155" rx="10" fill="#ffffff" stroke="#1e3a8a" stroke-width="2.5"/>
    <rect width="700" height="34" rx="10" fill="#1e3a8a"/>
    <rect x="0" y="24" width="700" height="10" fill="#1e3a8a"/>
    <text x="18" y="24" font-size="16" font-weight="900" fill="#ffffff">PHASE 2: EMBEDDED FREERTOS PROCESSING &amp; PREDICTIVE ENGINE</text>
    <text x="18" y="56" font-size="13.5" font-weight="700" fill="#1e3a8a">• Acquisition HAL: Async DS18B20 read (750 ms) + Fast 400 kHz I2C bus poll (25 ms)</text>
    <text x="18" y="78" font-size="13.5" font-weight="600" fill="#334155">• Data Gate: Scratchpad CRC-8 validation + Bus hang watchdog (&gt; 500 ms timeout)</text>
    <text x="18" y="100" font-size="13.5" font-weight="700" fill="#0f172a">• EMA Digital Filter (α = 0.20): T_f(k) = 0.20·T(k) + 0.80·T_f(k-1) [Attenuates noise]</text>
    <text x="18" y="122" font-size="13.5" font-weight="700" fill="#2563eb">• Forward Projection (30s): T_p = T_f + 30.0·max(0, r) [r = Least-Squares Slope]</text>
    <text x="18" y="142" font-size="12" font-weight="700" fill="#059669">Strict deterministic priority: Execution never yields to network or Wi-Fi operations</text>
  </g>

  <!-- Arrow Phase 2 -> Central Decision Gate -->
  <path class="wire" stroke="#0f172a" stroke-width="3.5" marker-end="url(#arrow)" d="M 1530 182 L 1630 182"/>


  <!-- ==================== PHASE 3: MULTI-TIER SUPERVISORY HEALTH EVALUATION (TOP-RIGHT) ==================== -->
  
  <g transform="translate(1630, 110)" filter="url(#shadow)">
    <polygon points="200,0 400,72 200,144 0,72" fill="#fffbeb" stroke="#d97706" stroke-width="3"/>
    <text x="200" y="56" font-size="16" font-weight="900" fill="#92400e" text-anchor="middle">SYSTEM HEALTH EVALUATION</text>
    <text x="200" y="80" font-size="12" font-weight="700" fill="#b45309" text-anchor="middle">T_core &lt; 65°C &amp; T_p &lt; 70°C &amp; I_12V &lt; 3.15A</text>
    <text x="200" y="100" font-size="11.5" font-weight="800" fill="#78350f" text-anchor="middle">&amp; I_5V/3.3V &lt; 1A &amp; Sensor Bus Healthy</text>
  </g>


  <!-- ==================== BRANCH A: NORMAL CLOSED-LOOP REGULATION (LEFT-MIDDLE TIER) ==================== -->
  
  <!-- Green Arrow pointing DOWN from Health Decision to Branch A -->
  <path class="wire" stroke="#059669" stroke-width="4" marker-end="url(#arrow-green)"
        d="M 1720 254 L 1720 320 L 750 320 L 750 365"/>
  <rect x="1180" y="308" width="160" height="24" rx="4" fill="#ecfdf5" stroke="#059669" stroke-width="1.5"/>
  <text x="1260" y="324" font-size="12" font-weight="900" fill="#065f46" text-anchor="middle">ALL CRITERIA NOMINAL (PASS)</text>

  <!-- Card A1: Active Thermal Regulation & Local Dispatch -->
  <g transform="translate(60, 365)" filter="url(#shadow)">
    <rect width="680" height="235" rx="10" fill="#ffffff" stroke="#059669" stroke-width="2.5"/>
    <rect width="680" height="34" rx="10" fill="#059669"/>
    <rect x="0" y="24" width="680" height="10" fill="#059669"/>
    <text x="18" y="24" font-size="16" font-weight="900" fill="#ffffff">BRANCH A1: PREDICTIVE PWM COOLING &amp; LOCAL UI DISPATCH</text>
    <text x="18" y="58" font-size="13.5" font-weight="700" fill="#065f46">• Dual-Demand PWM Demand: D_auto = max(g(T_f), g(T_p)) [Proactive pre-cooling]</text>
    <text x="18" y="80" font-size="13.5" font-weight="700" fill="#d97706">• Asymmetric Slew Limiter: Instant acceleration on rise; rate-limited descent ≤ 1%/s</text>
    <text x="18" y="102" font-size="13.5" font-weight="600" fill="#334155">• Anti-Stall Clamp: Minimum 30% duty floor when active suppresses inductive hum</text>
    <text x="18" y="124" font-size="13.5" font-weight="700" fill="#6b21a8">• 25.0 kHz Ultrasonic LEDC PWM: GPIO 25 drives TB6612FNG H-Bridge (Silent drive)</text>
    <text x="18" y="146" font-size="13.5" font-weight="600" fill="#334155">• 16x2 I2C LCD Cycler (Standby +5VSB): Alternates Screen 1 &amp; Screen 2 every 2.0s</text>
    <text x="18" y="168" font-size="13.5" font-weight="600" fill="#334155">• 120-Minute Circular SRAM History: 7,200 records backfilled upon Wi-Fi reconnect</text>
    <text x="18" y="190" font-size="13.5" font-weight="700" fill="#0284c7">• Embedded LittleFS Server: Full local dashboard on SoftAP (192.168.4.1) or LAN</text>
    <text x="18" y="212" font-size="12" font-weight="700" fill="#059669">Maintains transformer hot-spot temperature safely below 50°C continuous</text>
  </g>

  <!-- Arrow A1 -> A2 -->
  <path class="wire" stroke="#059669" stroke-width="3.5" marker-end="url(#arrow-green)" d="M 740 482 L 830 482"/>
  <rect x="752" y="470" width="65" height="24" rx="4" fill="#ecfdf5" stroke="#059669" stroke-width="1.5"/>
  <text x="784" y="486" font-size="11" font-weight="800" fill="#059669" text-anchor="middle">10s TIMER</text>

  <!-- Card A2: Cloud Synchronization & Supervision Tier -->
  <g transform="translate(830, 365)" filter="url(#shadow)">
    <rect width="700" height="235" rx="10" fill="#ffffff" stroke="#0284c7" stroke-width="2.5"/>
    <rect width="700" height="34" rx="10" fill="#0284c7"/>
    <rect x="0" y="24" width="700" height="10" fill="#0284c7"/>
    <text x="18" y="24" font-size="16" font-weight="900" fill="#ffffff">BRANCH A2: CLOUD SYNCHRONIZATION &amp; REMOTE SUPERVISION</text>
    <text x="18" y="58" font-size="13.5" font-weight="700" fill="#0369a1">• Firebase Realtime Database (RTDB): Non-blocking HTTPS PUT to /devices/&#123;id&#125;/latest</text>
    <text x="18" y="80" font-size="13.5" font-weight="600" fill="#334155">• Telemetry Record: T1, T2, ΔT, Tp, 12V/5V/3.3V Volts &amp; Amps, Fan PWM, Uptime</text>
    <text x="18" y="102" font-size="13.5" font-weight="700" fill="#059669">• Firebase Hosting Web Dashboard: Single-Page App streams metrics via WebSocket</text>
    <text x="18" y="124" font-size="13.5" font-weight="600" fill="#334155">• Firebase Authentication: Role-based engineer login, historical trends &amp; command queue</text>
    <text x="18" y="146" font-size="13.5" font-weight="700" fill="#7e22ce">• Cloudflare Serverless Worker: 60s scheduled cron watchdog verifies live heartbeat</text>
    <text x="18" y="168" font-size="13.5" font-weight="600" fill="#334155">• Remote Command Queue: Polls /commands for authorized remote shutdown/reset</text>
    <text x="18" y="190" font-size="13.5" font-weight="700" fill="#0284c7">• Direct CLI Deploy: firebase deploy (GitHub repository remains 100% private)</text>
    <text x="18" y="212" font-size="12" font-weight="700" fill="#0369a1">Sub-second cloud propagation delivers live operational visibility worldwide</text>
  </g>

  <!-- Loopback from Normal Path back to Stage 1 at top -->
  <path class="wire" stroke="#059669" stroke-width="2.5" marker-end="url(#arrow-green)"
        d="M 1180 600 L 1180 645 L 35 645 L 35 182 L 60 182"/>
  <rect x="520" y="633" width="180" height="24" rx="4" fill="#ecfdf5" stroke="#059669" stroke-width="1.5"/>
  <text x="610" y="649" font-size="11.5" font-weight="800" fill="#065f46" text-anchor="middle">NORMAL LOOP: TICK 1.00s</text>


  <!-- ==================== BRANCH B: CRITICAL EMERGENCY HARDWARE TRIP (RIGHT & BOTTOM TIER) ==================== -->

  <!-- Red Arrow pointing DOWN from Health Decision to Branch B -->
  <path class="wire" stroke="#dc2626" stroke-width="4" marker-end="url(#arrow-red)"
        d="M 1940 254 L 1940 365"/>
  <rect x="1860" y="295" width="160" height="24" rx="4" fill="#fef2f2" stroke="#dc2626" stroke-width="1.5"/>
  <text x="1940" y="311" font-size="12" font-weight="900" fill="#dc2626" text-anchor="middle">SAFETY LIMIT BREACHED</text>

  <!-- Card B1: Instant Hardware Cutoff & Failsafe Interlock -->
  <g transform="translate(1600, 365)" filter="url(#shadow)">
    <rect width="740" height="235" rx="10" fill="#ffffff" stroke="#dc2626" stroke-width="3"/>
    <rect width="740" height="34" rx="10" fill="#dc2626"/>
    <rect x="0" y="24" width="740" height="10" fill="#dc2626"/>
    <text x="18" y="24" font-size="16" font-weight="900" fill="#ffffff">BRANCH B1: INSTANT HARDWARE CUTOFF &amp; POWER DE-ENERGIZATION</text>
    <text x="18" y="58" font-size="14" font-weight="900" fill="#b91c1c">• Fast Cutoff (&lt; 5 ms): ESP32 GPIO 32 pulled LOW instantaneously</text>
    <text x="18" y="80" font-size="13.5" font-weight="700" fill="#0f172a">• PS_ON# Interlock Releases: BC547 Q1 turns OFF; ATX PS_ON# pulled to +5V</text>
    <text x="18" y="102" font-size="13.5" font-weight="900" fill="#dc2626">• ATX Main Power Rails Collapse: +12V, +5V, +3.3V fall to 0V within milliseconds</text>
    <text x="18" y="124" font-size="13.5" font-weight="700" fill="#b91c1c">• Load Disconnected: Removes power from 12V 50W Dummy Load (Stops I²R losses)</text>
    <text x="18" y="146" font-size="13.5" font-weight="600" fill="#334155">• 500 ms Rail Collapse Check: INA219 confirms V_12V &lt; 2.0V (detects stuck relay)</text>
    <text x="18" y="168" font-size="13.5" font-weight="700" fill="#059669">• Standby +5VSB Remains 100% Active: Powers ESP32, 16x2 LCD &amp; telemetry chip</text>
    <text x="18" y="190" font-size="13.5" font-weight="600" fill="#334155">• Hardware Failsafe Invariant: Transistor defaults open during MCU reset/brownout</text>
    <text x="18" y="212" font-size="12" font-weight="700" fill="#7f1d1d">Catastrophic transformer failure prevented at the physical silicon layer</text>
  </g>

  <!-- Arrow B1 -> B2 (Down to Bottom Row) -->
  <path class="wire" stroke="#dc2626" stroke-width="4" marker-end="url(#arrow-red)" d="M 1970 600 L 1970 700"/>
  <rect x="1880" y="640" width="180" height="24" rx="4" fill="#fef2f2" stroke="#dc2626" stroke-width="1.5"/>
  <text x="1970" y="656" font-size="11.5" font-weight="900" fill="#dc2626" text-anchor="middle">LATCH &amp; ALERT PROPAGATION</text>


  <!-- ==================== BOTTOM ROW: EMERGENCY LATCHING & MULTI-CHANNEL CLOUD ALERTS ==================== -->

  <!-- Card B2: Local Latching & Standby LCD Alert -->
  <g transform="translate(60, 700)" filter="url(#shadow)">
    <rect width="680" height="250" rx="10" fill="#ffffff" stroke="#b91c1c" stroke-width="2.5"/>
    <rect width="680" height="34" rx="10" fill="#b91c1c"/>
    <rect x="0" y="24" width="680" height="10" fill="#b91c1c"/>
    <text x="18" y="24" font-size="16" font-weight="900" fill="#ffffff">BRANCH B2: LOCAL FAULT LATCHING &amp; STANDBY LCD ALERT</text>
    <text x="18" y="58" font-size="13.5" font-weight="700" fill="#991b1b">• Immutable NVS Log: Fault code, trip timestamp, peak temp &amp; rail currents latched</text>
    <text x="18" y="80" font-size="13.5" font-weight="600" fill="#334155">• Non-Volatile Flash Persistence: Survives complete AC mains power disconnection</text>
    <text x="18" y="102" font-size="13.5" font-weight="900" fill="#dc2626">• 16x2 I2C LCD Blinks Red Alert via +5VSB: "FAULT: OVERTEMP" or "FAULT: OVERCURRENT"</text>
    <text x="18" y="124" font-size="13.5" font-weight="600" fill="#334155">• Screen Line 2: Displays exact trip values (e.g., "T_CORE: 65.4°C I: 3.28A")</text>
    <text x="18" y="146" font-size="13.5" font-weight="700" fill="#0f172a">• On-Site Operator Guidance: Audio piezo alarm / visual status alert</text>
    <text x="18" y="168" font-size="13.5" font-weight="700" fill="#b91c1c">• Auto-Restart Counter (k): Evaluates qualified auto-recovery vs permanent lockout</text>
    <text x="18" y="190" font-size="13.5" font-weight="600" fill="#334155">• State Transition: Enters STATE 6 (THERMAL_COOL) OR STATE 4 (ELEC_LOCKOUT)</text>
    <text x="18" y="214" font-size="12" font-weight="700" fill="#7f1d1d">Standby rail guarantees operator visibility even with ATX main inverter offline</text>
  </g>

  <!-- Arrow B2 -> B3 -->
  <path class="wire" stroke="#ea580c" stroke-width="3.5" marker-end="url(#arrow-orange)" d="M 740 825 L 830 825"/>
  <rect x="752" y="813" width="65" height="24" rx="4" fill="#fff7ed" stroke="#fb923c" stroke-width="1.5"/>
  <text x="784" y="829" font-size="11" font-weight="800" fill="#c2410c" text-anchor="middle">RTDB PUSH</text>

  <!-- Card B3: Firebase Realtime Database & Web Dashboard Banner -->
  <g transform="translate(830, 700)" filter="url(#shadow)">
    <rect width="700" height="250" rx="10" fill="#ffffff" stroke="#ea580c" stroke-width="2.5"/>
    <rect width="700" height="34" rx="10" fill="#ea580c"/>
    <rect x="0" y="24" width="700" height="10" fill="#ea580c"/>
    <text x="18" y="24" font-size="16" font-weight="900" fill="#ffffff">BRANCH B3: FIREBASE RTDB PUSH &amp; DASHBOARD RED ALERT BANNER</text>
    <text x="18" y="58" font-size="13.5" font-weight="700" fill="#9a3412">• Immediate Emergency Push: Dispatched via HTTPS to /devices/&#123;id&#125;/latest</text>
    <text x="18" y="80" font-size="13.5" font-weight="600" fill="#334155">• Payload: trip_active: true, fault_code: "E_OVERTEMP", trip_timestamp, trip_metrics</text>
    <text x="18" y="102" font-size="13.5" font-weight="600" fill="#334155">• Persistent Incident Logged: Written to /devices/&#123;id&#125;/history/trips/&#123;timestamp&#125;</text>
    <text x="18" y="124" font-size="13.5" font-weight="900" fill="#dc2626">• Firebase Hosting Web Dashboard: WebSocket pushes incident to all active browsers</text>
    <text x="18" y="146" font-size="13.5" font-weight="700" fill="#b91c1c">• Top Red Alert Emergency Banner: Displays fault code, trip values &amp; lockout status</text>
    <text x="18" y="168" font-size="13.5" font-weight="600" fill="#334155">• UI Invariant: Output power controls disabled; manual remote re-arm requires Auth</text>
    <text x="18" y="190" font-size="13.5" font-weight="700" fill="#0284c7">• Cloudflare Worker Webhook: RTDB update automatically triggers serverless alert worker</text>
    <text x="18" y="214" font-size="12" font-weight="700" fill="#9a3412">Remote operations center alerted within &lt; 1 second of physical trip event</text>
  </g>

  <!-- Arrow B3 -> B4 -->
  <path class="wire" stroke="#7e22ce" stroke-width="3.5" marker-end="url(#arrow-purple)" d="M 1530 825 L 1600 825"/>
  <rect x="1540" y="813" width="50" height="24" rx="4" fill="#faf5ff" stroke="#c084fc" stroke-width="1.5"/>
  <text x="1565" y="829" font-size="11" font-weight="800" fill="#7e22ce" text-anchor="middle">WEBHOOK</text>

  <!-- Card B4: Cloudflare Worker & Brevo Transactional Email Alert -->
  <g transform="translate(1600, 700)" filter="url(#shadow)">
    <rect width="740" height="250" rx="10" fill="#ffffff" stroke="#7e22ce" stroke-width="2.5"/>
    <rect width="740" height="34" rx="10" fill="#7e22ce"/>
    <rect x="0" y="24" width="740" height="10" fill="#7e22ce"/>
    <text x="18" y="24" font-size="16" font-weight="900" fill="#ffffff">BRANCH B4: CLOUDFLARE WORKER &amp; BREVO TRANSACTIONAL EMAIL DISPATCH</text>
    <text x="18" y="58" font-size="13.5" font-weight="700" fill="#6b21a8">• Serverless Edge Execution: Cloudflare Worker receives RTDB emergency event</text>
    <text x="18" y="80" font-size="13.5" font-weight="600" fill="#334155">• Heartbeat Watchdog Integration: Flags COMM_LOSS if telemetry silent &gt; 120 seconds</text>
    <text x="18" y="102" font-size="13.5" font-weight="700" fill="#0f172a">• Brevo Transactional Email API: Dispatches high-priority diagnostic alert email</text>
    <text x="18" y="124" font-size="13.5" font-weight="600" fill="#334155">• Structured HTML Notification: Unit ID, exact timestamp, trip reason &amp; sensor metrics</text>
    <text x="18" y="146" font-size="13.5" font-weight="700" fill="#dc2626">• Direct Maintenance Action Items: Immediate transformer inspection checklist</text>
    <text x="18" y="168" font-size="13.5" font-weight="600" fill="#334155">• Sub-Minute Delivery: Engineers receive inbox push alerts on mobile devices</text>
    <text x="18" y="190" font-size="13.5" font-weight="700" fill="#059669">• Lockout Awaits Resolution: System holds in safe de-energized state until reset</text>
    <text x="18" y="214" font-size="12" font-weight="700" fill="#581c87">Guarantees zero silent failures even during off-hours unmanned operation</text>
  </g>


  <!-- ==================== RECOVERY & RESET CORRIDOR (BOTTOM FLOOR) ==================== -->
  
  <g transform="translate(60, 1010)" filter="url(#shadow)">
    <rect width="2280" height="110" rx="10" fill="#f8fafc" stroke="#64748b" stroke-width="2"/>
    <text x="24" y="32" font-size="16" font-weight="900" fill="#0f172a">RESTORATION &amp; RE-ENERGIZATION PATHWAYS (CLEARING LOCKOUT)</text>
    
    <g transform="translate(24, 48)" font-size="13.5" font-weight="600" fill="#334155">
      <text x="0" y="20" font-weight="800" fill="#059669">1. Qualified Thermal Auto-Recovery:</text>
      <text x="290" y="20">If trip count k &lt; 3 within 1 hour AND core cools to ≤ 45°C for ≥ 60s -> Re-energizes under 120s supervised qualification test</text>

      <text x="0" y="44" font-weight="800" fill="#dc2626">2. Permanent Thermal / Overcurrent Lockout:</text>
      <text x="290" y="44">Auto-restart FORBIDDEN (k ≥ 3 or electrical short). Requires physical ON/OFF switch toggle OR authorized cloud reset via Firebase Auth</text>
    </g>
  </g>

</svg>'''

    out_svg = os.path.join("documentation", "diagram_6_combined_supervisory_flowchart.svg")
    with open(out_svg, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Generated {out_svg}")

    # Compile to high-res PNG via typst
    typ_path = os.path.join("documentation", "render_diag6.typ")
    png_path = os.path.join("documentation", "diagram_6_combined_supervisory_flowchart.png")
    typst_exe = os.path.join("documentation", "bin", "typst.exe")
    with open(typ_path, "w", encoding="utf-8") as f:
        f.write('#set page(width: 2400pt, height: 1500pt, margin: 0pt)\n#image("diagram_6_combined_supervisory_flowchart.svg", width: 100%)\n')
    subprocess.run([typst_exe, "compile", "--format", "png", "--ppi", "150", typ_path, png_path], check=True)
    if os.path.exists(typ_path):
        os.remove(typ_path)
    print(f"Compiled {png_path}")

if __name__ == "__main__":
    generate_diagram_6()
