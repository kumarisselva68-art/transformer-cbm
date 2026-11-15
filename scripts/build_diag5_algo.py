# -*- coding: utf-8 -*-
"""
Diagram 5 Generator: Software Execution & Predictive Thermal Algorithm Closed-Loop Flowchart
Covers:
- Strict 1.00 Hz Real-Time Tick
- 1-Wire & I2C Async Sensor Acquisition + CRC-8 Gate
- Differential Temperature Calculation
- Exponential Moving Average (EMA) Digital Filter (alpha = 0.20)
- Rolling 30-Sample FIFO Buffer & Least-Squares Regression Slope
- 30-Second Forward Predictive Horizon (Tp = Tf + 30*max(0, r))
- Dual-Demand Piecewise Transfer Function (D_auto = max(g(Tf), g(Tp)))
- Asymmetric Slew-Rate Limiter (Instant Rise, <=1%/s Fall) & 30% Anti-Stall Floor
- 25 kHz Ultrasonic LEDC PWM Actuation to TB6612 Driver
- Multi-Task Dispatch: LCD Refresh, Circular RAM Buffer, 10s Firebase RTDB Push
"""

import os
import subprocess

def generate_diagram_5():
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
  <g transform="translate(60, 50)">
    <text font-size="32" font-weight="900" fill="#0f172a" letter-spacing="-0.5px">IoT Transformer Condition Monitoring System — Software &amp; Predictive Algorithm Flowchart</text>
    <text font-size="17" font-weight="700" fill="#64748b" y="28">1.00 Hz Real-Time Tick, Digital EMA Filter, 30s Regression Slope, Forward Projection &amp; Dual-Demand PWM Modulation</text>
  </g>

  <!-- ==================== COLUMN 1: SENSOR ACQUISITION & INTEGRITY (x = 80, center = 340) ==================== -->

  <!-- STEP 1: 1.00 Hz TICK TRIGGER -->
  <g transform="translate(80, 110)" filter="url(#shadow)">
    <rect width="520" height="110" rx="10" fill="#ffffff" stroke="#1e3a8a" stroke-width="2.5"/>
    <rect width="520" height="32" rx="10" fill="#1e3a8a"/>
    <rect x="0" y="22" width="520" height="10" fill="#1e3a8a"/>
    <text x="16" y="22" font-size="15.5" font-weight="900" fill="#ffffff">STEP 1: 1.00 Hz REAL-TIME TICK (FREERTOS TIMER)</text>
    <text x="16" y="54" font-size="13.5" font-weight="700" fill="#1e3a8a">• FreeRTOS Task: vTaskDelayUntil(&amp;xLastWakeTime, pdMS_TO_TICKS(1000))</text>
    <text x="16" y="76" font-size="13.5" font-weight="600" fill="#334155">• Jitter-Free Sampling Interval: Δt = 1.000s exact temporal reference</text>
    <text x="16" y="96" font-size="12.5" font-weight="700" fill="#059669">Strict deterministic priority: Never yields to network stack operations</text>
  </g>

  <!-- Arrow Step 1 -> Step 2 -->
  <path class="wire" stroke="#0f172a" stroke-width="3" marker-end="url(#arrow)" d="M 340 220 L 340 265"/>

  <!-- STEP 2: MULTI-BUS SENSOR HAL ACQUISITION -->
  <g transform="translate(80, 265)" filter="url(#shadow)">
    <rect width="520" height="165" rx="10" fill="#ffffff" stroke="#0284c7" stroke-width="2.5"/>
    <rect width="520" height="32" rx="10" fill="#0284c7"/>
    <rect x="0" y="22" width="520" height="10" fill="#0284c7"/>
    <text x="16" y="22" font-size="15.5" font-weight="900" fill="#ffffff">STEP 2: MULTI-BUS SENSOR ACQUISITION (HAL)</text>
    <text x="16" y="54" font-size="13.5" font-weight="700" fill="#0369a1">• Non-blocking 1-Wire Read (GPIO 27): 12-bit DS18B20 core (T1) &amp; inlet (T2)</text>
    <text x="16" y="76" font-size="13.5" font-weight="600" fill="#334155">• I2C 400 kHz Fast-Mode Poller (GPIO 21/22): 3x INA219 power monitors</text>
    <text x="16" y="98" font-size="13.5" font-weight="600" fill="#334155">• Acquired metrics: V_12V, I_12V, P_12V, V_5V, I_5V, V_3.3V, I_3.3V</text>
    <text x="16" y="120" font-size="13.5" font-weight="700" fill="#0284c7">• Temperature Differential: ΔT = T_core - T_inlet</text>
    <text x="16" y="142" font-size="12" font-weight="600" fill="#475569">Acquisition completes in &lt; 25 ms across both serial bus channels</text>
  </g>

  <!-- Arrow Step 2 -> Step 3 -->
  <path class="wire" stroke="#0f172a" stroke-width="3" marker-end="url(#arrow)" d="M 340 430 L 340 475"/>

  <!-- STEP 3: DATA INTEGRITY & BUS MONITOR -->
  <g transform="translate(80, 475)" filter="url(#shadow)">
    <rect width="520" height="145" rx="10" fill="#ffffff" stroke="#ea580c" stroke-width="2.5"/>
    <rect width="520" height="32" rx="10" fill="#ea580c"/>
    <rect x="0" y="22" width="520" height="10" fill="#ea580c"/>
    <text x="16" y="22" font-size="15.5" font-weight="900" fill="#ffffff">STEP 3: INTEGRITY &amp; TIMEOUT VALIDATION</text>
    <text x="16" y="54" font-size="13.5" font-weight="700" fill="#9a3412">• 1-Wire Scratchpad CRC-8 Check: Polynomial X^8 + X^5 + X^4 + 1</text>
    <text x="16" y="76" font-size="13.5" font-weight="600" fill="#334155">• I2C Bus Hang Watchdog: Hardware timeout flag (&gt; 500 ms = Trip)</text>
    <text x="16" y="98" font-size="13.5" font-weight="600" fill="#334155">• INA219 Math Overflow &amp; Shunt Range Boundary Verification</text>
    <text x="16" y="120" font-size="12.5" font-weight="700" fill="#ea580c">Corrupt samples flagged and isolated before reaching algorithm</text>
  </g>

  <!-- Arrow Step 3 -> Decision Gate 1 -->
  <path class="wire" stroke="#0f172a" stroke-width="3" marker-end="url(#arrow)" d="M 340 620 L 340 665"/>

  <!-- DECISION GATE 1: SENSOR DATA INTEGRITY VALID? -->
  <g transform="translate(160, 665)" filter="url(#shadow)">
    <polygon points="180,0 360,45 180,90 0,45" fill="#f8fafc" stroke="#64748b" stroke-width="2"/>
    <text x="180" y="38" font-size="13.5" font-weight="900" fill="#1e293b" text-anchor="middle">SENSOR CRC &amp; BUS OK?</text>
    <text x="180" y="58" font-size="11.5" font-weight="700" fill="#64748b" text-anchor="middle">CRC-8 Valid &amp; Timeout &lt; 500ms</text>
  </g>

  <!-- Decision 1 NO -> BUS FAULT CUTOFF -->
  <path class="wire" stroke="#dc2626" stroke-width="3" marker-end="url(#arrow-red)" d="M 160 710 L 50 710 L 50 820"/>
  <rect x="75" y="698" width="30" height="20" rx="3" fill="#ffffff" stroke="#dc2626" stroke-width="1"/>
  <text x="90" y="712" font-size="11" font-weight="800" fill="#dc2626" text-anchor="middle">NO</text>

  <!-- BUS FAULT ACTION BOX -->
  <g transform="translate(10, 820)" filter="url(#shadow)">
    <rect width="240" height="110" rx="8" fill="#fef2f2" stroke="#dc2626" stroke-width="2"/>
    <text x="12" y="24" font-size="13" font-weight="900" fill="#991b1b">SENSOR BUS FAULT</text>
    <text x="12" y="46" font-size="11.5" font-weight="700" fill="#dc2626">• Pull GPIO 32 LOW (&lt; 5 ms)</text>
    <text x="12" y="66" font-size="11" font-weight="600" fill="#334155">• De-energize ATX power rails</text>
    <text x="12" y="86" font-size="11" font-weight="700" fill="#991b1b">• LCD: "FAULT: SENSOR COMM"</text>
  </g>

  <!-- Decision 1 YES -> Decision Gate 2 (Electrical Limits) -->
  <path class="wire" stroke="#059669" stroke-width="3" marker-end="url(#arrow-green)" d="M 340 755 L 340 805"/>
  <rect x="346" y="768" width="32" height="20" rx="3" fill="#ffffff" stroke="#059669" stroke-width="1"/>
  <text x="362" y="782" font-size="11" font-weight="800" fill="#059669" text-anchor="middle">YES</text>

  <!-- DECISION GATE 2: ELECTRICAL OVERCURRENT SUPERVISION -->
  <g transform="translate(150, 805)" filter="url(#shadow)">
    <polygon points="190,0 380,45 190,90 0,45" fill="#fef2f2" stroke="#dc2626" stroke-width="2"/>
    <text x="190" y="38" font-size="13.5" font-weight="900" fill="#991b1b" text-anchor="middle">ELECTRICAL LIMITS EXCEEDED?</text>
    <text x="190" y="58" font-size="11.5" font-weight="700" fill="#dc2626" text-anchor="middle">12V &gt; 3.15A | 5V &gt; 1A | 3.3V &gt; 1A</text>
  </g>

  <!-- Decision 2 YES -> Instant Cutoff (State 4) -->
  <path class="wire" stroke="#dc2626" stroke-width="3" marker-end="url(#arrow-red)" d="M 340 895 L 340 945"/>
  <rect x="346" y="908" width="32" height="20" rx="3" fill="#ffffff" stroke="#dc2626" stroke-width="1"/>
  <text x="362" y="922" font-size="11" font-weight="800" fill="#dc2626" text-anchor="middle">YES</text>

  <!-- CRITICAL OVERCURRENT TRIP BOX -->
  <g transform="translate(80, 945)" filter="url(#shadow)">
    <rect width="520" height="135" rx="10" fill="#ffffff" stroke="#dc2626" stroke-width="2.5"/>
    <rect width="520" height="32" rx="10" fill="#dc2626"/>
    <rect x="0" y="22" width="520" height="10" fill="#dc2626"/>
    <text x="16" y="22" font-size="15" font-weight="900" fill="#ffffff">HARDWARE CUTOFF: STATE 4 (ELEC_LOCKOUT)</text>
    <text x="16" y="54" font-size="13" font-weight="700" fill="#991b1b">• Fast Cutoff: GPIO 32 pulled LOW in &lt; 5 ms; PS_ON# releases to 5V</text>
    <text x="16" y="74" font-size="13" font-weight="600" fill="#334155">• ATX power rails collapse to 0V; dummy load de-energized immediately</text>
    <text x="16" y="94" font-size="13" font-weight="700" fill="#dc2626">• Fault code latched into ESP32 NVS flash • LCD displays "FAULT: OVERCURRENT"</text>
    <text x="16" y="114" font-size="12" font-weight="700" fill="#7f1d1d">Dispatches critical push alert to Firebase RTDB &amp; Brevo API; auto-restart FORBIDDEN</text>
  </g>

  <!-- Decision 2 NO -> Enter Predictive Algorithm Spine (Rightward Corridor to Col 2) -->
  <path class="wire" stroke="#059669" stroke-width="3" marker-end="url(#arrow-green)"
        d="M 530 850 L 680 850 L 680 180 L 730 180"/>
  <rect x="580" y="838" width="30" height="20" rx="3" fill="#ffffff" stroke="#059669" stroke-width="1"/>
  <text x="595" y="852" font-size="11" font-weight="800" fill="#059669" text-anchor="middle">NO</text>
  <text x="695" y="480" font-size="12" font-weight="800" fill="#059669" transform="rotate(-90 695 480)">PASS TO PREDICTIVE ENGINE</text>


  <!-- ==================== COLUMN 2: MATHEMATICAL PREDICTIVE ENGINE (x = 730, center = 1010) ==================== -->

  <!-- STEP 4: DIGITAL EXPONENTIAL MOVING AVERAGE (EMA) FILTER -->
  <g transform="translate(730, 110)" filter="url(#shadow)">
    <rect width="560" height="155" rx="10" fill="#ffffff" stroke="#4338ca" stroke-width="2.5"/>
    <rect width="560" height="32" rx="10" fill="#4338ca"/>
    <rect x="0" y="22" width="560" height="10" fill="#4338ca"/>
    <text x="16" y="22" font-size="15.5" font-weight="900" fill="#ffffff">STEP 4: EXPONENTIAL MOVING AVERAGE (EMA) FILTER</text>
    <text x="16" y="56" font-size="14.5" font-weight="900" fill="#1e1b4b">• Filter Formula: T_f(k) = 0.20 · T_core(k) + 0.80 · T_f(k-1)</text>
    <text x="16" y="80" font-size="13.5" font-weight="600" fill="#334155">• Alpha = 0.20 (Suppresses DS18B20 ±0.0625°C quantization steps)</text>
    <text x="16" y="102" font-size="13.5" font-weight="600" fill="#334155">• Group Delay: 4.0 seconds • Rejects sensor thermal noise &amp; turbulent air spikes</text>
    <text x="16" y="124" font-size="13.5" font-weight="700" fill="#4338ca">• Ambient Inlet Temp Filtered Similarly: T_amb_f(k) = 0.10·T_amb + 0.90·T_amb_f</text>
    <text x="16" y="142" font-size="12" font-weight="600" fill="#475569">Smooth continuous temperature curve ready for numerical differentiation</text>
  </g>

  <!-- Arrow Step 4 -> Step 5 -->
  <path class="wire" stroke="#0f172a" stroke-width="3" marker-end="url(#arrow)" d="M 1010 265 L 1010 310"/>

  <!-- STEP 5: ROLLING 30s FIFO BUFFER & LEAST-SQUARES SLOPE -->
  <g transform="translate(730, 310)" filter="url(#shadow)">
    <rect width="560" height="175" rx="10" fill="#ffffff" stroke="#2563eb" stroke-width="2.5"/>
    <rect width="560" height="32" rx="10" fill="#2563eb"/>
    <rect x="0" y="22" width="560" height="10" fill="#2563eb"/>
    <text x="16" y="22" font-size="15.5" font-weight="900" fill="#ffffff">STEP 5: ROLLING 30s FIFO BUFFER &amp; REGRESSION SLOPE</text>
    <text x="16" y="56" font-size="13.5" font-weight="700" fill="#1e40af">• Rolling Circular Buffer: N = 30 samples (stores last 30s of filtered data)</text>
    <text x="16" y="78" font-size="13.5" font-weight="900" fill="#0f172a">• Least-Squares Linear Regression Slope (dT/dt):</text>
    <text x="36" y="100" font-size="13.5" font-weight="800" fill="#2563eb">r = [ N·Σ(i·T_i) - Σi·ΣT_i ] / [ N·Σi² - (Σi)² ]   [°C/second]</text>
    <text x="16" y="124" font-size="13.5" font-weight="600" fill="#334155">• Exact closed-form denominator precomputed as constant: D_reg = 224750</text>
    <text x="16" y="146" font-size="13.5" font-weight="600" fill="#334155">• Quantifies instantaneous thermal acceleration before temperature peaks</text>
    <text x="16" y="164" font-size="12" font-weight="700" fill="#059669">Detects runaway conditions up to 45 seconds earlier than static thresholds</text>
  </g>

  <!-- Arrow Step 5 -> Step 6 -->
  <path class="wire" stroke="#0f172a" stroke-width="3" marker-end="url(#arrow)" d="M 1010 485 L 1010 530"/>

  <!-- STEP 6: 30-SECOND FORWARD PREDICTIVE PROJECTION -->
  <g transform="translate(730, 530)" filter="url(#shadow)">
    <rect width="560" height="155" rx="10" fill="#ffffff" stroke="#0284c7" stroke-width="2.5"/>
    <rect width="560" height="32" rx="10" fill="#0284c7"/>
    <rect x="0" y="22" width="560" height="10" fill="#0284c7"/>
    <text x="16" y="22" font-size="15.5" font-weight="900" fill="#ffffff">STEP 6: 30-SECOND FORWARD THERMAL PROJECTION</text>
    <text x="16" y="56" font-size="14.5" font-weight="900" fill="#0369a1">• Forward Projection Formula: T_p = T_f + 30.0 · max(0, r)</text>
    <text x="16" y="80" font-size="13.5" font-weight="700" fill="#ea580c">• Asymmetric Rate Clamp: Negative cooling slope clamped to 0.0</text>
    <text x="16" y="102" font-size="13.5" font-weight="600" fill="#334155">• Prevents thermal cooling inertia from masking current high core temp</text>
    <text x="16" y="124" font-size="13.5" font-weight="600" fill="#334155">• Predicts transformer temperature 30 seconds into the future</text>
    <text x="16" y="142" font-size="12" font-weight="700" fill="#0284c7">Proactively alerts cooling subsystem before safety trip boundaries are hit</text>
  </g>

  <!-- Arrow Step 6 -> Decision Gate 3 (Thermal Trip Check) -->
  <path class="wire" stroke="#0f172a" stroke-width="3" marker-end="url(#arrow)" d="M 1010 685 L 1010 730"/>

  <!-- DECISION GATE 3: THERMAL SAFETY BOUNDARY CHECK -->
  <g transform="translate(820, 730)" filter="url(#shadow)">
    <polygon points="190,0 380,45 190,90 0,45" fill="#fef2f2" stroke="#ea580c" stroke-width="2"/>
    <text x="190" y="38" font-size="13.5" font-weight="900" fill="#9a3412" text-anchor="middle">THERMAL SAFETY LIMIT BREACHED?</text>
    <text x="190" y="58" font-size="11.5" font-weight="700" fill="#ea580c" text-anchor="middle">T_core ≥ 65°C OR T_p ≥ 70°C</text>
  </g>

  <!-- Decision 3 YES -> Thermal Cooldown State 6 (Left to Overcurrent/Trip area) -->
  <path class="wire" stroke="#dc2626" stroke-width="3" marker-end="url(#arrow-red)"
        d="M 820 775 L 750 775 L 750 945"/>
  <rect x="765" y="763" width="32" height="20" rx="3" fill="#ffffff" stroke="#dc2626" stroke-width="1"/>
  <text x="781" y="777" font-size="11" font-weight="800" fill="#dc2626" text-anchor="middle">YES</text>

  <!-- Decision 3 NO -> Proceed to Dual-Demand Cooling (Col 3) -->
  <path class="wire" stroke="#059669" stroke-width="3" marker-end="url(#arrow-green)"
        d="M 1200 775 L 1330 775 L 1330 180 L 1380 180"/>
  <rect x="1230" y="763" width="30" height="20" rx="3" fill="#ffffff" stroke="#059669" stroke-width="1"/>
  <text x="1245" y="777" font-size="11" font-weight="800" fill="#059669" text-anchor="middle">NO</text>
  <text x="1345" y="480" font-size="12" font-weight="800" fill="#059669" transform="rotate(-90 1345 480)">NORMAL: COMPUTE PWM COOLING</text>


  <!-- ==================== COLUMN 3: DUAL-DEMAND & PWM MODULATION (x = 1380, center = 1660) ==================== -->

  <!-- STEP 7: DUAL-DEMAND PIECEWISE MODULATION ENGINE -->
  <g transform="translate(1380, 110)" filter="url(#shadow)">
    <rect width="560" height="195" rx="10" fill="#ffffff" stroke="#059669" stroke-width="2.5"/>
    <rect width="560" height="32" rx="10" fill="#059669"/>
    <rect x="0" y="22" width="560" height="10" fill="#059669"/>
    <text x="16" y="22" font-size="15.5" font-weight="900" fill="#ffffff">STEP 7: DUAL-DEMAND PIECEWISE MODULATION</text>
    <text x="16" y="56" font-size="13.5" font-weight="700" fill="#065f46">• Piecewise Transfer Curve g(T):</text>
    <text x="36" y="76" font-size="13" font-weight="600" fill="#334155">g(T) = 0% for T ≤ 35°C (Silent passive cooling mode)</text>
    <text x="36" y="96" font-size="13" font-weight="700" fill="#065f46">g(T) = 30% + [(T - 35)/(60 - 35)] · 70% for 35°C &lt; T &lt; 60°C</text>
    <text x="36" y="116" font-size="13" font-weight="600" fill="#334155">g(T) = 100% for T ≥ 60°C (Full emergency airflow)</text>
    <text x="16" y="142" font-size="14.5" font-weight="900" fill="#0f172a">• Dual Demand Selection: D_auto = max( g(T_f), g(T_p) )</text>
    <text x="16" y="166" font-size="13.5" font-weight="600" fill="#334155">• Current temp demands what is needed now; projected temp demands pre-cooling</text>
    <text x="16" y="184" font-size="12" font-weight="700" fill="#059669">Pre-cools heat sink before thermal mass absorbs rising heat load</text>
  </g>

  <!-- Arrow Step 7 -> Step 8 -->
  <path class="wire" stroke="#0f172a" stroke-width="3" marker-end="url(#arrow)" d="M 1660 305 L 1660 350"/>

  <!-- STEP 8: ASYMMETRIC SLEW-RATE LIMITER & ANTI-STALL FLOOR -->
  <g transform="translate(1380, 350)" filter="url(#shadow)">
    <rect width="560" height="175" rx="10" fill="#ffffff" stroke="#d97706" stroke-width="2.5"/>
    <rect width="560" height="32" rx="10" fill="#d97706"/>
    <rect x="0" y="22" width="560" height="10" fill="#d97706"/>
    <text x="16" y="22" font-size="15.5" font-weight="900" fill="#ffffff">STEP 8: ASYMMETRIC SLEW-RATE LIMITER</text>
    <text x="16" y="56" font-size="13.5" font-weight="700" fill="#92400e">• Asymmetric Dynamics Invariant:</text>
    <text x="36" y="78" font-size="13.5" font-weight="800" fill="#dc2626">Rising Thermal Slew: Uncapped (Instant rise to 100% in 1 tick)</text>
    <text x="36" y="100" font-size="13.5" font-weight="800" fill="#059669">Falling Thermal Slew: Limited to ≤ 1.0% duty descent per second</text>
    <text x="16" y="126" font-size="13.5" font-weight="700" fill="#b45309">• Anti-Stall Clamp: Floor = 30% duty when commanded ON</text>
    <text x="16" y="148" font-size="13.5" font-weight="600" fill="#334155">• Prevents motor buzzing, acoustic hunting &amp; inductive winding flutter</text>
    <text x="16" y="166" font-size="12" font-weight="600" fill="#475569">Delivers smooth acoustic profile and maximizes brushless blower bearing life</text>
  </g>

  <!-- Arrow Step 8 -> Step 9 -->
  <path class="wire" stroke="#0f172a" stroke-width="3" marker-end="url(#arrow)" d="M 1660 525 L 1660 570"/>

  <!-- STEP 9: 25 kHz ULTRASONIC PWM HARDWARE ACTUATION -->
  <g transform="translate(1380, 570)" filter="url(#shadow)">
    <rect width="560" height="155" rx="10" fill="#ffffff" stroke="#9333ea" stroke-width="2.5"/>
    <rect width="560" height="32" rx="10" fill="#9333ea"/>
    <rect x="0" y="22" width="560" height="10" fill="#9333ea"/>
    <text x="16" y="22" font-size="15.5" font-weight="900" fill="#ffffff">STEP 9: 25 kHz ULTRASONIC LEDC PWM ACTUATION</text>
    <text x="16" y="56" font-size="13.5" font-weight="700" fill="#6b21a8">• ESP32 Hardware LEDC Peripheral: Configured at 25.0 kHz carrier</text>
    <text x="16" y="78" font-size="13.5" font-weight="600" fill="#334155">• Above Human Hearing Threshold (&gt; 20 kHz) = Zero audible coil whine</text>
    <text x="16" y="100" font-size="13.5" font-weight="700" fill="#0f172a">• Output Pin GPIO 25 (PWMA) drives TB6612FNG Dual MOSFET H-Bridge</text>
    <text x="16" y="122" font-size="13.5" font-weight="600" fill="#334155">• Motor Supply (VM): Switched +12V DC rail | Logic VCC: 3.3V DC rail</text>
    <text x="16" y="142" font-size="12" font-weight="700" fill="#059669">Hardware PWM generation runs autonomously via hardware timers</text>
  </g>

  <!-- Arrow Step 9 -> Rightward Corridor to Multi-Task Dispatch (Col 4) -->
  <path class="wire" stroke="#059669" stroke-width="3" marker-end="url(#arrow-green)"
        d="M 1940 645 L 2000 645 L 2000 180 L 2030 180"/>
  <text x="2015" y="420" font-size="12" font-weight="800" fill="#059669" transform="rotate(-90 2015 420)">DISPATCH TELEMETRY &amp; UI</text>


  <!-- ==================== COLUMN 4: MULTI-TASK DISPATCH & CLOUD SYNC (x = 2030, center = 2200) ==================== -->

  <!-- STEP 10A: 16x2 I2C LCD SCREEN CYCLER -->
  <g transform="translate(2030, 110)" filter="url(#shadow)">
    <rect width="330" height="150" rx="10" fill="#ffffff" stroke="#0284c7" stroke-width="2"/>
    <rect width="330" height="30" rx="10" fill="#0284c7"/>
    <rect x="0" y="20" width="330" height="10" fill="#0284c7"/>
    <text x="14" y="20" font-size="14" font-weight="900" fill="#ffffff">16x2 I2C LCD SCREEN CYCLER</text>
    <text x="14" y="48" font-size="12" font-weight="700" fill="#0369a1">• Cycles every 2.0s via Standby +5VSB</text>
    <text x="14" y="68" font-size="11.5" font-weight="600" fill="#334155">• Screen 1: T1, T2, ΔT, Projected Tp</text>
    <text x="14" y="88" font-size="11.5" font-weight="600" fill="#334155">• Screen 2: Rail Volts, Currents, Fan %</text>
    <text x="14" y="108" font-size="11.5" font-weight="700" fill="#059669">• Stays active during ATX shutdown</text>
    <text x="14" y="128" font-size="11" font-weight="600" fill="#475569">I2C PCF8574 backpack @ 0x27</text>
  </g>

  <!-- STEP 10B: CIRCULAR RAM BUFFER -->
  <g transform="translate(2030, 290)" filter="url(#shadow)">
    <rect width="330" height="150" rx="10" fill="#ffffff" stroke="#4338ca" stroke-width="2"/>
    <rect width="330" height="30" rx="10" fill="#4338ca"/>
    <rect x="0" y="20" width="330" height="10" fill="#4338ca"/>
    <text x="14" y="20" font-size="14" font-weight="900" fill="#ffffff">120-MIN CIRCULAR RAM BUFFER</text>
    <text x="14" y="48" font-size="12" font-weight="700" fill="#312e81">• 7,200 telemetry points in SRAM</text>
    <text x="14" y="68" font-size="11.5" font-weight="600" fill="#334155">• Preserves data through Wi-Fi drops</text>
    <text x="14" y="88" font-size="11.5" font-weight="600" fill="#334155">• Automatic backfill upon reconnect</text>
    <text x="14" y="108" font-size="11.5" font-weight="700" fill="#4338ca">• Zero data loss during outages</text>
    <text x="14" y="128" font-size="11" font-weight="600" fill="#475569">Memory-optimized struct packing</text>
  </g>

  <!-- STEP 10C: 10s HTTPS FIREBASE RTDB PUSH -->
  <g transform="translate(2030, 470)" filter="url(#shadow)">
    <rect width="330" height="165" rx="10" fill="#ffffff" stroke="#ea580c" stroke-width="2"/>
    <rect width="330" height="30" rx="10" fill="#ea580c"/>
    <rect x="0" y="20" width="330" height="10" fill="#ea580c"/>
    <text x="14" y="20" font-size="14" font-weight="900" fill="#ffffff">10s FIREBASE RTDB SYNC</text>
    <text x="14" y="48" font-size="12" font-weight="700" fill="#9a3412">• 10s Timer: Push JSON payload</text>
    <text x="14" y="68" font-size="11.5" font-weight="600" fill="#334155">• /devices/&#123;id&#125;/latest: Live metrics</text>
    <text x="14" y="88" font-size="11.5" font-weight="600" fill="#334155">• Updates Cloudflare Watchdog</text>
    <text x="14" y="108" font-size="11.5" font-weight="700" fill="#059669">• Web dashboard real-time stream</text>
    <text x="14" y="128" font-size="11.5" font-weight="600" fill="#334155">• Polls /commands queue (cutoff/reset)</text>
    <text x="14" y="146" font-size="11" font-weight="600" fill="#475569">Non-blocking background HTTPS task</text>
  </g>

  <!-- Loopback Arrow from Step 10C back to 1.00 Hz Tick via Clean Open Channel (Right Margin x=2380 & Top Corridor y=88) -->
  <path class="wire" stroke="#059669" stroke-width="3" marker-end="url(#arrow-green)"
        d="M 2195 635 L 2195 660 L 2380 660 L 2380 88 L 340 88 L 340 110"/>
  <g transform="translate(1200, 88)">
    <rect x="-95" y="-12" width="190" height="24" rx="4" fill="#ecfdf5" stroke="#059669" stroke-width="1.5"/>
    <text x="0" y="4" font-size="11.5" font-weight="800" fill="#065f46" text-anchor="middle">NEXT 1.00s SAMPLE CYCLE</text>
  </g>

</svg>'''

    out_svg = os.path.join("documentation", "diagram_5_predictive_thermal_flowchart.svg")
    with open(out_svg, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Generated {out_svg}")

    # Compile to high-res PNG via typst
    typ_path = os.path.join("documentation", "render_diag5.typ")
    png_path = os.path.join("documentation", "diagram_5_predictive_thermal_flowchart.png")
    typst_exe = os.path.join("documentation", "bin", "typst.exe")
    with open(typ_path, "w", encoding="utf-8") as f:
        f.write('#set page(width: 2400pt, height: 1500pt, margin: 0pt)\n#image("diagram_5_predictive_thermal_flowchart.svg", width: 100%)\n')
    subprocess.run([typst_exe, "compile", "--format", "png", "--ppi", "150", typ_path, png_path], check=True)
    if os.path.exists(typ_path):
        os.remove(typ_path)
    print(f"Compiled {png_path}")

if __name__ == "__main__":
    generate_diagram_5()
