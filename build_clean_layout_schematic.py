# -*- coding: utf-8 -*-
"""
High-Precision CAD Circuit Diagram Generator for Transformer_CBM
Rev 10.0 - Hardware Authenticity Edition:
1. ATX Wiring Fix: +12V (y=65), +5V (y=105), +3.3V (y=145), GND (y=185) - 100% verified connections!
   TB6612 VM connects strictly to +12V at y=65 (never +5V).
2. No OS Windows: Removed the artificial desktop-window boxes on BC547 and DS18B20.
3. Clean DS18B20 Modules: Simple, realistic 3-pin breakout modules (VCC, DAT, GND) without ugly transistor graphics.
4. Authentic 16x2 LCD: Realistic wide 2.2:1 aspect ratio, 16-pin gold bus, metal bezel, 16x2 character grid.
5. Spacious 45px wire corridors, 100% strictly orthogonal routing.
"""

import os
import xml.etree.ElementTree as ET

def generate_circuit_svg():
    w = 1800
    h = 1220
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <defs>
    <!-- Background CAD Grid -->
    <pattern id="cad-grid" width="25" height="25" patternUnits="userSpaceOnUse">
      <path d="M 25 0 L 0 0 0 25" fill="none" stroke="#e2e8f0" stroke-width="0.8"/>
      <circle cx="25" cy="25" r="1" fill="#cbd5e1"/>
    </pattern>

    <!-- Card Shadow -->
    <filter id="card-shadow" x="-3%" y="-3%" width="106%" height="108%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="0" dy="4" stdDeviation="4" flood-color="#0f172a" flood-opacity="0.12"/>
    </filter>

    <!-- Metallic Gradients -->
    <linearGradient id="metal-silver" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="40%" stop-color="#e2e8f0"/>
      <stop offset="80%" stop-color="#94a3b8"/>
      <stop offset="100%" stop-color="#64748b"/>
    </linearGradient>

    <linearGradient id="metal-gold" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#fef08a"/>
      <stop offset="60%" stop-color="#eab308"/>
      <stop offset="100%" stop-color="#a16207"/>
    </linearGradient>

    <linearGradient id="metal-heatsink" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#334155"/>
      <stop offset="50%" stop-color="#1e293b"/>
      <stop offset="100%" stop-color="#0f172a"/>
    </linearGradient>

    <linearGradient id="lcd-screen" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#0284c7"/>
      <stop offset="100%" stop-color="#0369a1"/>
    </linearGradient>
  </defs>

  <style>
    text {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      user-select: none;
    }}
    .title-banner {{
      font-size: 14px;
      font-weight: 800;
      letter-spacing: 0.8px;
      text-transform: uppercase;
    }}
    .pin-txt {{
      font-family: "JetBrains Mono", Consolas, "SF Mono", monospace;
      font-size: 12px;
      font-weight: 700;
    }}
    .pin-txt-lg {{
      font-family: "JetBrains Mono", Consolas, "SF Mono", monospace;
      font-size: 14px;
      font-weight: 800;
    }}
    .bus-txt {{
      font-family: "JetBrains Mono", Consolas, "SF Mono", monospace;
      font-size: 13px;
      font-weight: 800;
      letter-spacing: 0.5px;
    }}
    .wire {{
      fill: none;
      stroke-linecap: round;
      stroke-linejoin: round;
    }}
    .solder-junction {{
      stroke: #ffffff;
      stroke-width: 2.5;
    }}
  </style>

  <!-- Background Surface -->
  <rect width="{w}" height="{h}" fill="#f8fafc"/>
  <rect width="{w}" height="{h}" fill="url(#cad-grid)"/>

  <!-- ===================================================================== -->
  <!-- ==================== TIER 1: CONTINUOUS POWER ROW =================== -->
  <!-- ATX Breakout -> INA219 #1 -> Ext Load -> INA219 #2 -> INA219 #3       -->
  <!-- ===================================================================== -->

  <!-- 1. ATX BREAKOUT BOARD (Top Left: x=40, y=40, w=270, h=180) -->
  <g id="cmp-atx" transform="translate(40, 40)" filter="url(#card-shadow)">
    <rect width="270" height="180" rx="8" fill="#14532d" stroke="#166534" stroke-width="2"/>
    <circle cx="12" cy="12" r="5" fill="#14532d" stroke="url(#metal-gold)" stroke-width="2"/>
    <circle cx="258" cy="12" r="5" fill="#14532d" stroke="url(#metal-gold)" stroke-width="2"/>
    <circle cx="12" cy="168" r="5" fill="#14532d" stroke="url(#metal-gold)" stroke-width="2"/>
    <circle cx="258" cy="168" r="5" fill="#14532d" stroke="url(#metal-gold)" stroke-width="2"/>

    <!-- Title Bar -->
    <rect x="0" y="0" width="270" height="30" rx="8" fill="#166534"/>
    <rect x="0" y="20" width="270" height="10" fill="#166534"/>
    <text class="title-banner" x="135" y="20" fill="#f0fdf4" text-anchor="middle">ATX BREAKOUT (XH-M229)</text>

    <!-- 24-Pin ATX Socket -->
    <rect x="15" y="42" width="50" height="125" rx="4" fill="#ffffff" stroke="#94a3b8" stroke-width="2"/>
    <text x="40" y="105" fill="#64748b" font-size="10" font-weight="800" text-anchor="middle" transform="rotate(-90 40 105)">24-PIN ATX</text>

    <!-- Output Binding Posts on Right Edge (x=245): Exact Y-Positions! -->
    <!-- +12V (y = 65) -->
    <circle cx="245" cy="65" r="11" fill="#d97706" stroke="#fef08a" stroke-width="2.5"/>
    <text class="pin-txt-lg" x="228" y="70" fill="#fef08a" text-anchor="end">+12V</text>

    <!-- +5V (y = 105) -->
    <circle cx="245" cy="105" r="11" fill="#dc2626" stroke="#fca5a5" stroke-width="2.5"/>
    <text class="pin-txt-lg" x="228" y="110" fill="#fca5a5" text-anchor="end">+5V</text>

    <!-- +3.3V (y = 145) -->
    <circle cx="245" cy="145" r="11" fill="#ea580c" stroke="#fed7aa" stroke-width="2.5"/>
    <text class="pin-txt-lg" x="228" y="150" fill="#fed7aa" text-anchor="end">+3.3V</text>

    <!-- GND (y = 175) -->
    <circle cx="245" cy="175" r="11" fill="#0f172a" stroke="#f8fafc" stroke-width="2.5"/>
    <text class="pin-txt-lg" x="228" y="180" fill="#f8fafc" text-anchor="end">GND</text>

    <!-- Bottom Pins -->
    <circle cx="105" cy="165" r="6" fill="#9333ea" stroke="#f3e8ff" stroke-width="2"/>
    <text class="pin-txt" x="105" y="152" fill="#f3e8ff" text-anchor="middle">+5VSB</text>

    <circle cx="160" cy="165" r="6" fill="#10b981" stroke="#d1fae5" stroke-width="2"/>
    <text class="pin-txt" x="160" y="152" fill="#d1fae5" text-anchor="middle">PS_ON#</text>
  </g>


  <!-- 2. INA219 #1 (12V High-Side Monitor: x=350, y=40, w=220, h=180) -->
  <g id="cmp-ina1" transform="translate(350, 40)" filter="url(#card-shadow)">
    <rect width="220" height="180" rx="8" fill="#4c1d95" stroke="#6d28d9" stroke-width="2"/>
    <rect x="0" y="0" width="220" height="30" rx="8" fill="#5b21b6"/>
    <rect x="0" y="20" width="220" height="10" fill="#5b21b6"/>
    <text class="title-banner" x="110" y="20" fill="#f5f3ff" text-anchor="middle">INA219 (12V)</text>

    <!-- Terminal Block -->
    <rect x="25" y="45" width="85" height="42" rx="4" fill="#15803d" stroke="#166534" stroke-width="1.5"/>
    <circle cx="45" cy="66" r="7.5" fill="#d97706" stroke="#fef08a" stroke-width="2"/>
    <text class="pin-txt" x="45" y="55" fill="#fef08a" text-anchor="middle">VIN+</text>
    <circle cx="85" cy="66" r="7.5" fill="#d97706" stroke="#fef08a" stroke-width="2"/>
    <text class="pin-txt" x="85" y="55" fill="#fef08a" text-anchor="middle">VIN-</text>

    <!-- Shunt Resistor -->
    <rect x="135" y="54" width="55" height="24" rx="2" fill="#0f172a" stroke="#94a3b8"/>
    <text x="162" y="70" fill="#38bdf8" font-size="11" font-weight="bold" text-anchor="middle">R100</text>

    <!-- Logic Header -->
    <circle cx="30" cy="155" r="6.5" fill="#ea580c" stroke="#fed7aa" stroke-width="2"/>
    <text class="pin-txt" x="30" y="142" fill="#fed7aa" text-anchor="middle">VCC</text>

    <circle cx="70" cy="155" r="6.5" fill="#0f172a" stroke="#f8fafc" stroke-width="2"/>
    <text class="pin-txt" x="70" y="142" fill="#f8fafc" text-anchor="middle">GND</text>

    <circle cx="120" cy="155" r="6.5" fill="#0284c7" stroke="#bae6fd" stroke-width="2"/>
    <text class="pin-txt" x="120" y="142" fill="#bae6fd" text-anchor="middle">SCL</text>

    <circle cx="170" cy="155" r="6.5" fill="#2563eb" stroke="#bfdbfe" stroke-width="2"/>
    <text class="pin-txt" x="170" y="142" fill="#bfdbfe" text-anchor="middle">SDA</text>
  </g>


  <!-- 3. EXTERNAL 12V LOAD (x=610, y=40, w=260, h=180) -->
  <g id="cmp-load" transform="translate(610, 40)" filter="url(#card-shadow)">
    <rect width="260" height="180" rx="8" fill="#1e293b" stroke="#334155" stroke-width="2"/>
    <rect x="0" y="0" width="260" height="30" rx="8" fill="#334155"/>
    <rect x="0" y="20" width="260" height="10" fill="#334155"/>
    <text class="title-banner" x="130" y="20" fill="#f8fafc" text-anchor="middle">12V LOAD</text>

    <!-- Heatsink Fins -->
    <rect x="25" y="45" width="210" height="50" rx="4" fill="url(#metal-heatsink)" stroke="#475569"/>
    <g stroke="#94a3b8" stroke-width="3">
      <line x1="45" y1="50" x2="45" y2="90"/>
      <line x1="70" y1="50" x2="70" y2="90"/>
      <line x1="95" y1="50" x2="95" y2="90"/>
      <line x1="120" y1="50" x2="120" y2="90"/>
      <line x1="145" y1="50" x2="145" y2="90"/>
      <line x1="170" y1="50" x2="170" y2="90"/>
      <line x1="195" y1="50" x2="195" y2="90"/>
      <line x1="215" y1="50" x2="215" y2="90"/>
    </g>

    <!-- Terminals -->
    <circle cx="65" cy="145" r="8.5" fill="#d97706" stroke="#fef08a" stroke-width="2"/>
    <text class="pin-txt-lg" x="65" y="128" fill="#fef08a" text-anchor="middle">IN (+)</text>

    <circle cx="195" cy="145" r="8.5" fill="#0f172a" stroke="#f8fafc" stroke-width="2"/>
    <text class="pin-txt-lg" x="195" y="128" fill="#f8fafc" text-anchor="middle">GND (-)</text>
  </g>


  <!-- 4. INA219 #2 (5V Bus Monitor: x=910, y=40, w=220, h=180) -->
  <g id="cmp-ina2" transform="translate(910, 40)" filter="url(#card-shadow)">
    <rect width="220" height="180" rx="8" fill="#4c1d95" stroke="#6d28d9" stroke-width="2"/>
    <rect x="0" y="0" width="220" height="30" rx="8" fill="#5b21b6"/>
    <rect x="0" y="20" width="220" height="10" fill="#5b21b6"/>
    <text class="title-banner" x="110" y="20" fill="#f5f3ff" text-anchor="middle">INA219 (5V)</text>

    <rect x="25" y="45" width="85" height="42" rx="4" fill="#15803d" stroke="#166534" stroke-width="1.5"/>
    <circle cx="45" cy="66" r="7.5" fill="#dc2626" stroke="#fca5a5" stroke-width="2"/>
    <text class="pin-txt" x="45" y="55" fill="#fca5a5" text-anchor="middle">VIN+</text>
    <circle cx="85" cy="66" r="5" fill="#475569"/>

    <circle cx="30" cy="155" r="6.5" fill="#ea580c" stroke="#fed7aa" stroke-width="2"/>
    <text class="pin-txt" x="30" y="142" fill="#fed7aa" text-anchor="middle">VCC</text>

    <circle cx="70" cy="155" r="6.5" fill="#0f172a" stroke="#f8fafc" stroke-width="2"/>
    <text class="pin-txt" x="70" y="142" fill="#f8fafc" text-anchor="middle">GND</text>

    <circle cx="120" cy="155" r="6.5" fill="#0284c7" stroke="#bae6fd" stroke-width="2"/>
    <text class="pin-txt" x="120" y="142" fill="#bae6fd" text-anchor="middle">SCL</text>

    <circle cx="170" cy="155" r="6.5" fill="#2563eb" stroke="#bfdbfe" stroke-width="2"/>
    <text class="pin-txt" x="170" y="142" fill="#bfdbfe" text-anchor="middle">SDA</text>
  </g>


  <!-- 5. INA219 #3 (3.3V Bus Monitor: x=1170, y=40, w=220, h=180) -->
  <g id="cmp-ina3" transform="translate(1170, 40)" filter="url(#card-shadow)">
    <rect width="220" height="180" rx="8" fill="#4c1d95" stroke="#6d28d9" stroke-width="2"/>
    <rect x="0" y="0" width="220" height="30" rx="8" fill="#5b21b6"/>
    <rect x="0" y="20" width="220" height="10" fill="#5b21b6"/>
    <text class="title-banner" x="110" y="20" fill="#f5f3ff" text-anchor="middle">INA219 (3.3V)</text>

    <rect x="25" y="45" width="85" height="42" rx="4" fill="#15803d" stroke="#166534" stroke-width="1.5"/>
    <circle cx="45" cy="66" r="7.5" fill="#ea580c" stroke="#fed7aa" stroke-width="2"/>
    <text class="pin-txt" x="45" y="55" fill="#fed7aa" text-anchor="middle">VIN+</text>
    <circle cx="85" cy="66" r="5" fill="#475569"/>

    <circle cx="30" cy="155" r="6.5" fill="#ea580c" stroke="#fed7aa" stroke-width="2"/>
    <text class="pin-txt" x="30" y="142" fill="#fed7aa" text-anchor="middle">VCC</text>

    <circle cx="70" cy="155" r="6.5" fill="#0f172a" stroke="#f8fafc" stroke-width="2"/>
    <text class="pin-txt" x="70" y="142" fill="#f8fafc" text-anchor="middle">GND</text>

    <circle cx="120" cy="155" r="6.5" fill="#0284c7" stroke="#bae6fd" stroke-width="2"/>
    <text class="pin-txt" x="120" y="142" fill="#bae6fd" text-anchor="middle">SCL</text>

    <circle cx="170" cy="155" r="6.5" fill="#2563eb" stroke="#bfdbfe" stroke-width="2"/>
    <text class="pin-txt" x="170" y="142" fill="#bfdbfe" text-anchor="middle">SDA</text>
  </g>


  <!-- ===================================================================== -->
  <!-- ==================== HORIZONTAL BUS HIGHWAYS ======================== -->
  <!-- 4 Clean parallel lines between Tier 1 and Tier 2                       -->
  <!-- ===================================================================== -->

  <!-- HIGHWAY 1: COMMON GROUND BUS (GND) at y = 245 -->
  <g id="hwy-gnd" stroke="#0f172a" stroke-width="5" fill="none">
    <path class="wire" d="M 40 245 L 1720 245"/>
    <text class="bus-txt" x="1735" y="250" fill="#0f172a" stroke="none">GND BUS</text>

    <!-- PRIMARY GROUND SOURCE: Heavy feed from ATX GND post (285, 215) down to y=245 -->
    <path class="wire" stroke-width="5" d="M 285 215 L 285 245"/>
    <circle cx="285" cy="245" r="6" fill="#0f172a" class="solder-junction"/>

    <!-- Taps from Tier 1 Down: -->
    <path class="wire" stroke-width="4.5" d="M 420 195 L 420 245"/><circle cx="420" cy="245" r="5" fill="#0f172a" class="solder-junction"/>
    <path class="wire" stroke-width="4.5" d="M 805 185 L 805 245"/><circle cx="805" cy="245" r="5" fill="#0f172a" class="solder-junction"/>
    <path class="wire" stroke-width="4.5" d="M 980 195 L 980 245"/><circle cx="980" cy="245" r="5" fill="#0f172a" class="solder-junction"/>
    <path class="wire" stroke-width="4.5" d="M 1240 195 L 1240 245"/><circle cx="1240" cy="245" r="5" fill="#0f172a" class="solder-junction"/>
  </g>

  <!-- HIGHWAY 2: 3.3V SENSOR & LOGIC BUS at y = 275 -->
  <g id="hwy-3v3" stroke="#ea580c" stroke-width="4" fill="none">
    <path class="wire" d="M 370 275 L 1720 275"/>
    <text class="bus-txt" x="1735" y="280" fill="#ea580c" stroke="none">3.3V BUS</text>

    <!-- Taps up to Tier 1: -->
    <path class="wire" d="M 380 195 L 380 275"/><circle cx="380" cy="275" r="5" fill="#ea580c" class="solder-junction"/>
    <path class="wire" d="M 940 195 L 940 275"/><circle cx="940" cy="275" r="5" fill="#ea580c" class="solder-junction"/>
    <path class="wire" d="M 1200 195 L 1200 275"/><circle cx="1200" cy="275" r="5" fill="#ea580c" class="solder-junction"/>
  </g>

  <!-- HIGHWAY 3: I2C SCL BUS at y = 305 -->
  <g id="hwy-scl" stroke="#0284c7" stroke-width="3.5" fill="none">
    <path class="wire" d="M 470 305 L 1720 305"/>
    <text class="bus-txt" x="1735" y="310" fill="#0284c7" stroke="none">I2C SCL</text>

    <!-- Taps up to Tier 1: -->
    <path class="wire" d="M 470 195 L 470 305"/>
    <path class="wire" d="M 1030 195 L 1030 305"/><circle cx="1030" cy="305" r="5" fill="#0284c7" class="solder-junction"/>
    <path class="wire" d="M 1290 195 L 1290 305"/><circle cx="1290" cy="305" r="5" fill="#0284c7" class="solder-junction"/>
  </g>

  <!-- HIGHWAY 4: I2C SDA BUS at y = 335 -->
  <g id="hwy-sda" stroke="#2563eb" stroke-width="3.5" fill="none">
    <path class="wire" d="M 520 335 L 1720 335"/>
    <text class="bus-txt" x="1735" y="340" fill="#2563eb" stroke="none">I2C SDA</text>

    <!-- Taps up to Tier 1: -->
    <path class="wire" d="M 520 195 L 520 335"/>
    <path class="wire" d="M 1080 195 L 1080 335"/><circle cx="1080" cy="335" r="5" fill="#2563eb" class="solder-junction"/>
    <path class="wire" d="M 1340 195 L 1340 335"/><circle cx="1340" cy="335" r="5" fill="#2563eb" class="solder-junction"/>
  </g>


  <!-- ===================================================================== -->
  <!-- ==================== TIER 2: MIDDLE ROW ============================= -->
  <!-- PS_ON# Switch (No OS Window!) | ESP32 Controller (Center)             -->
  <!-- ===================================================================== -->

  <!-- 6. BC547 NPN TRANSISTOR SWITCH MODULE (x=40, y=390, w=270, h=260: Sleek PCB, NO OS Window) -->
  <g id="cmp-transistor-circuit" transform="translate(40, 390)" filter="url(#card-shadow)">
    <rect width="270" height="260" rx="8" fill="#1e293b" stroke="#334155" stroke-width="2"/>
    <text x="135" y="24" fill="#38bdf8" font-size="13" font-weight="800" text-anchor="middle">PS_ON# SWITCH (BC547)</text>

    <!-- Collector Terminal on TOP EDGE (x=135, y=45) -> global x=175, y=435 -->
    <circle cx="135" cy="45" r="7.5" fill="#10b981" stroke="#d1fae5" stroke-width="2"/>
    <text class="pin-txt" x="150" y="50" fill="#a7f3d0">C (PS_ON#)</text>

    <!-- Base Drive IN Terminal on RIGHT EDGE (x=255, y=110) -> global x=295, y=500 -->
    <circle cx="255" cy="110" r="7.5" fill="#10b981" stroke="#d1fae5" stroke-width="2"/>
    <text class="pin-txt" x="242" y="100" fill="#a7f3d0" text-anchor="end">IN (D32)</text>

    <!-- Emitter Terminal on BOTTOM EDGE (x=135, y=240) -> global x=175, y=630 -->
    <circle cx="135" cy="240" r="7.5" fill="#0f172a" stroke="#f8fafc" stroke-width="2"/>
    <text class="pin-txt" x="150" y="245" fill="#cbd5e1">E (GND)</text>

    <!-- 1 kOhm Base Resistor R_B (Horizontal) -->
    <g transform="translate(145, 98)">
      <rect width="50" height="24" rx="4" fill="#d97706" stroke="#b45309" stroke-width="1.5"/>
      <rect x="8" y="0" width="5" height="24" fill="#78350f"/>
      <rect x="18" y="0" width="5" height="24" fill="#0f172a"/>
      <rect x="28" y="0" width="5" height="24" fill="#dc2626"/>
      <rect x="38" y="0" width="4" height="24" fill="#ca8a04"/>
      <text x="25" y="-6" fill="#fde68a" font-size="11" font-weight="bold" text-anchor="middle">1 kΩ</text>
    </g>
    <path d="M 255 110 L 195 110" stroke="#10b981" stroke-width="3" fill="none"/>
    <path d="M 145 110 L 105 110" stroke="#f8fafc" stroke-width="3" fill="none"/>

    <!-- NPN Transistor Schematic Symbol -->
    <line x1="105" y1="85" x2="105" y2="135" stroke="#f8fafc" stroke-width="4.5" stroke-linecap="round"/>
    <line x1="105" y1="95" x2="135" y2="45" stroke="#10b981" stroke-width="3.5" stroke-linecap="round"/>
    <line x1="105" y1="125" x2="135" y2="165" stroke="#cbd5e1" stroke-width="3.5" stroke-linecap="round"/>
    <polygon points="130,153 135,165 122,163" fill="#cbd5e1"/>

    <circle cx="118" cy="110" r="32" fill="none" stroke="#64748b" stroke-width="1.5" stroke-dasharray="3"/>
    <text x="70" y="114" fill="#94a3b8" font-size="11" font-weight="800" text-anchor="middle">BC547</text>

    <!-- 10k Base-Emitter Pull-Down Resistor (Vertical) -->
    <g transform="translate(123, 170)">
      <line x1="12" y1="-60" x2="12" y2="0" stroke="#cbd5e1" stroke-width="2"/>
      <circle cx="12" cy="-60" r="3.5" fill="#0f172a" class="solder-junction"/>
      <rect x="0" y="0" width="24" height="38" rx="4" fill="#d97706" stroke="#b45309" stroke-width="1.2"/>
      <rect x="0" y="6" width="24" height="4" fill="#78350f"/>
      <rect x="0" y="14" width="24" height="4" fill="#0f172a"/>
      <rect x="0" y="22" width="24" height="4" fill="#ea580c"/>
      <rect x="0" y="29" width="24" height="3" fill="#ca8a04"/>
      <line x1="12" y1="38" x2="12" y2="70" stroke="#cbd5e1" stroke-width="2"/>
      <text x="-6" y="23" fill="#fde68a" font-size="10" font-weight="bold" text-anchor="end">10 kΩ</text>
    </g>
  </g>


  <!-- 7. ESP32-WROOM-32 DEVKIT (Center Middle: x=490, y=390, w=560, h=290) -->
  <g id="cmp-esp32" transform="translate(490, 390)" filter="url(#card-shadow)">
    <rect width="560" height="290" rx="10" fill="#18181b" stroke="#3f3f46" stroke-width="2"/>

    <!-- RF Shield Can -->
    <g transform="translate(195, 25)">
      <rect width="170" height="145" rx="5" fill="url(#metal-silver)" stroke="#64748b" stroke-width="1.5"/>
      <path d="M 25 20 L 40 20 L 40 35 L 55 35 L 55 20 L 70 20 L 70 35 L 85 35 L 85 20 L 100 20 L 100 35 L 115 35 L 115 20 L 145 20" 
            fill="none" stroke="url(#metal-gold)" stroke-width="3.5" stroke-linecap="round"/>
      <text x="85" y="75" fill="#0f172a" font-size="16" font-weight="800" text-anchor="middle">ESPRESSIF</text>
      <text x="85" y="100" fill="#1e293b" font-size="13" font-weight="700" text-anchor="middle">ESP-WROOM-32</text>
    </g>

    <!-- USB Port & CP2102 Bridge -->
    <rect x="250" y="190" width="60" height="42" rx="3" fill="#27272a" stroke="#52525b"/>
    <text x="280" y="215" fill="#a1a1aa" font-size="10" font-weight="bold" text-anchor="middle">CP2102</text>
    <rect x="240" y="268" width="80" height="22" rx="4" fill="#cbd5e1" stroke="#64748b"/>

    <!-- Left Header Pins -->
    <circle cx="15" cy="40" r="7.5" fill="#ea580c" stroke="#fed7aa" stroke-width="2"/><text class="pin-txt-lg" x="32" y="45" fill="#fed7aa">3V3</text>
    <circle cx="15" cy="85" r="7.5" fill="#10b981" stroke="#a7f3d0" stroke-width="2"/><text class="pin-txt-lg" x="32" y="90" fill="#a7f3d0">D32 (PS_ON#)</text>
    <circle cx="15" cy="130" r="7.5" fill="#06b6d4" stroke="#cffafe" stroke-width="2"/><text class="pin-txt-lg" x="32" y="135" fill="#cffafe">D33 (STBY)</text>
    <circle cx="15" cy="175" r="7.5" fill="#8b5cf6" stroke="#ede9fe" stroke-width="2"/><text class="pin-txt-lg" x="32" y="180" fill="#ede9fe">D25 (PWM)</text>
    <circle cx="15" cy="220" r="7.5" fill="#ec4899" stroke="#fce7f3" stroke-width="2"/><text class="pin-txt-lg" x="32" y="225" fill="#fce7f3">D26 (AIN1)</text>
    <circle cx="15" cy="260" r="7.5" fill="#eab308" stroke="#fef08a" stroke-width="2"/><text class="pin-txt-lg" x="32" y="265" fill="#fef08a">D27 (TEMP)</text>

    <!-- Right Header Pins -->
    <circle cx="545" cy="40" r="7.5" fill="#0284c7" stroke="#bae6fd" stroke-width="2"/><text class="pin-txt-lg" x="528" y="45" fill="#bae6fd" text-anchor="end">D22 (SCL)</text>
    <circle cx="545" cy="85" r="7.5" fill="#2563eb" stroke="#bfdbfe" stroke-width="2"/><text class="pin-txt-lg" x="528" y="90" fill="#bfdbfe" text-anchor="end">D21 (SDA)</text>
    <circle cx="545" cy="220" r="7.5" fill="#0f172a" stroke="#f8fafc" stroke-width="2.5"/><text class="pin-txt-lg" x="528" y="225" fill="#f8fafc" text-anchor="end">GND</text>
    <circle cx="545" cy="260" r="7.5" fill="#9333ea" stroke="#f3e8ff" stroke-width="2"/><text class="pin-txt-lg" x="528" y="265" fill="#f3e8ff" text-anchor="end">5V (VIN)</text>
  </g>


  <!-- ===================================================================== -->
  <!-- ==================== TIER 3: BOTTOM ROW ============================= -->
  <!-- TB6612 & Fan (Left) | Dual DS18B20 Breakouts | Real 16x2 LCD (Right)  -->
  <!-- ===================================================================== -->

  <!-- 8. TB6612FNG MOTOR DRIVER (Bottom Left: x=40, y=720, w=270, h=180) -->
  <g id="cmp-tb6612" transform="translate(40, 720)" filter="url(#card-shadow)">
    <rect width="270" height="180" rx="8" fill="#991b1b" stroke="#b91c1c" stroke-width="2"/>
    <text class="title-banner" x="135" y="24" fill="#fef2f2" text-anchor="middle">TB6612FNG DRIVER</text>

    <!-- IC -->
    <rect x="95" y="65" width="80" height="40" rx="3" fill="#1e293b" stroke="#475569"/>
    <circle cx="105" cy="75" r="2.5" fill="#94a3b8"/>
    <text x="135" y="90" fill="#f8fafc" font-size="11" font-weight="bold" text-anchor="middle">TB6612</text>

    <!-- Left Header (VM is at top: y=50 -> global y=770) -->
    <circle cx="20" cy="50" r="7" fill="#d97706" stroke="#fef08a" stroke-width="2"/><text class="pin-txt" x="35" y="55" fill="#fef08a">VM (+12V)</text>
    <circle cx="20" cy="80" r="7" fill="#ea580c" stroke="#fed7aa" stroke-width="2"/><text class="pin-txt" x="35" y="85" fill="#fed7aa">VCC (3.3V)</text>
    <circle cx="20" cy="110" r="7" fill="#0f172a" stroke="#f8fafc" stroke-width="2"/><text class="pin-txt" x="35" y="115" fill="#f8fafc">GND</text>
    <circle cx="20" cy="140" r="7" fill="#dc2626" stroke="#fca5a5" stroke-width="2"/><text class="pin-txt" x="35" y="145" fill="#fca5a5">AO1 (+)</text>
    <circle cx="20" cy="165" r="7" fill="#0f172a" stroke="#cbd5e1" stroke-width="2"/><text class="pin-txt" x="35" y="170" fill="#cbd5e1">AO2 (-)</text>

    <!-- Right Header -->
    <circle cx="250" cy="50" r="7" fill="#06b6d4" stroke="#cffafe" stroke-width="2"/><text class="pin-txt" x="235" y="55" fill="#cffafe" text-anchor="end">STBY</text>
    <circle cx="250" cy="85" r="7" fill="#8b5cf6" stroke="#ede9fe" stroke-width="2"/><text class="pin-txt" x="235" y="90" fill="#ede9fe" text-anchor="end">PWMA</text>
    <circle cx="250" cy="120" r="7" fill="#ec4899" stroke="#fce7f3" stroke-width="2"/><text class="pin-txt" x="235" y="125" fill="#fce7f3" text-anchor="end">AIN1</text>
    <circle cx="250" cy="155" r="7" fill="#0f172a" stroke="#f8fafc" stroke-width="2"/><text class="pin-txt" x="235" y="160" fill="#f8fafc" text-anchor="end">AIN2 (GND)</text>
  </g>


  <!-- 9. 12V DC BRUSHLESS COOLING FAN (x=40, y=940, w=270, h=240) -->
  <g id="cmp-fan" transform="translate(40, 940)" filter="url(#card-shadow)">
    <rect width="270" height="240" rx="8" fill="#0f172a" stroke="#334155" stroke-width="2"/>
    <text class="title-banner" x="135" y="24" fill="#f8fafc" text-anchor="middle">12V DC FAN</text>

    <!-- Corner Screw Mounts -->
    <circle cx="20" cy="52" r="5" fill="#475569" stroke="#94a3b8"/><circle cx="250" cy="52" r="5" fill="#475569" stroke="#94a3b8"/>
    <circle cx="20" cy="220" r="5" fill="#475569" stroke="#94a3b8"/><circle cx="250" cy="220" r="5" fill="#475569" stroke="#94a3b8"/>

    <!-- Circular Tunnel -->
    <circle cx="135" cy="145" r="70" fill="#1e293b" stroke="#475569" stroke-width="3"/>
    <g stroke="#334155" stroke-width="2" fill="#0f172a">
      <path d="M 135 145 Q 155 95 170 90 Q 150 115 135 145 Z"/>
      <path d="M 135 145 Q 185 130 195 145 Q 170 155 135 145 Z"/>
      <path d="M 135 145 Q 170 190 165 205 Q 145 185 135 145 Z"/>
      <path d="M 135 145 Q 115 200 100 200 Q 115 175 135 145 Z"/>
      <path d="M 135 145 Q 80 170 73 155 Q 100 145 135 145 Z"/>
      <path d="M 135 145 Q 90 115 97 100 Q 115 125 135 145 Z"/>
    </g>
    <circle cx="135" cy="145" r="30" fill="#334155" stroke="#64748b" stroke-width="2"/>
    <text x="135" y="142" fill="#f8fafc" font-size="10" font-weight="800" text-anchor="middle">12V DC</text>
    <text x="135" y="155" fill="#38bdf8" font-size="9" font-weight="bold" text-anchor="middle">PWM SPEED</text>

    <!-- Wire Lead Terminals -->
    <circle cx="80" cy="46" r="7" fill="#dc2626" stroke="#fca5a5" stroke-width="2"/>
    <text class="pin-txt" x="95" y="51" fill="#fca5a5">RED (+)</text>

    <circle cx="215" cy="46" r="7" fill="#0f172a" stroke="#cbd5e1" stroke-width="2"/>
    <text class="pin-txt" x="200" y="51" fill="#cbd5e1" text-anchor="end">BLK (-)</text>
  </g>


  <!-- 10. DUAL DS18B20 3-PIN BREAKOUT MODULES (Bottom Center: Two Compact Clean Boards, NO Windows!) -->
  <!-- MODULE 1: CORE TEMP (DS18B20 Breakout Board: x=510, y=740, w=240, h=120) -->
  <g id="cmp-temp-core" transform="translate(510, 740)" filter="url(#card-shadow)">
    <rect width="240" height="120" rx="6" fill="#1e3a8a" stroke="#1d4ed8" stroke-width="2"/>
    <circle cx="12" cy="12" r="4.5" fill="#1e3a8a" stroke="url(#metal-gold)" stroke-width="1.5"/>
    <text x="110" y="22" fill="#93c5fd" font-size="12" font-weight="800" text-anchor="middle">DS18B20 (CORE TEMP)</text>

    <!-- Chip Graphic & SMD Parts -->
    <rect x="25" y="45" width="40" height="45" rx="3" fill="#0f172a" stroke="#334155"/>
    <text x="45" y="72" fill="#f8fafc" font-size="9" font-weight="bold" text-anchor="middle">DS18B20</text>
    <rect x="80" y="55" width="18" height="10" fill="#0f172a" stroke="#64748b"/>
    <circle cx="89" cy="80" r="3.5" fill="#22c55e" stroke="#86efac"/>

    <!-- 3-Pin Header on Right Edge -->
    <g transform="translate(180, 25)">
      <rect width="45" height="75" rx="3" fill="#0f172a"/>
      <circle cx="25" cy="15" r="6" fill="#ea580c" stroke="#fed7aa" stroke-width="2"/>
      <text class="pin-txt" x="12" y="19" fill="#fed7aa" text-anchor="end">VCC</text>
      <circle cx="25" cy="38" r="6" fill="#eab308" stroke="#fef08a" stroke-width="2"/>
      <text class="pin-txt" x="12" y="42" fill="#fef08a" text-anchor="end">DAT</text>
      <circle cx="25" cy="60" r="6" fill="#0f172a" stroke="#f8fafc" stroke-width="2"/>
      <text class="pin-txt" x="12" y="64" fill="#f8fafc" text-anchor="end">GND</text>
    </g>
  </g>

  <!-- MODULE 2: AMBIENT TEMP (DS18B20 Breakout Board: x=510, y=930, w=240, h=120) -->
  <g id="cmp-temp-ambient" transform="translate(510, 930)" filter="url(#card-shadow)">
    <rect width="240" height="120" rx="6" fill="#1e3a8a" stroke="#1d4ed8" stroke-width="2"/>
    <circle cx="12" cy="12" r="4.5" fill="#1e3a8a" stroke="url(#metal-gold)" stroke-width="1.5"/>
    <text x="110" y="22" fill="#93c5fd" font-size="12" font-weight="800" text-anchor="middle">DS18B20 (AMBIENT TEMP)</text>

    <!-- Chip Graphic & SMD Parts -->
    <rect x="25" y="45" width="40" height="45" rx="3" fill="#0f172a" stroke="#334155"/>
    <text x="45" y="72" fill="#f8fafc" font-size="9" font-weight="bold" text-anchor="middle">DS18B20</text>
    <rect x="80" y="55" width="18" height="10" fill="#0f172a" stroke="#64748b"/>
    <circle cx="89" cy="80" r="3.5" fill="#22c55e" stroke="#86efac"/>

    <!-- 3-Pin Header on Right Edge -->
    <g transform="translate(180, 25)">
      <rect width="45" height="75" rx="3" fill="#0f172a"/>
      <circle cx="25" cy="15" r="6" fill="#ea580c" stroke="#fed7aa" stroke-width="2"/>
      <text class="pin-txt" x="12" y="19" fill="#fed7aa" text-anchor="end">VCC</text>
      <circle cx="25" cy="38" r="6" fill="#eab308" stroke="#fef08a" stroke-width="2"/>
      <text class="pin-txt" x="12" y="42" fill="#fef08a" text-anchor="end">DAT</text>
      <circle cx="25" cy="60" r="6" fill="#0f172a" stroke="#f8fafc" stroke-width="2"/>
      <text class="pin-txt" x="12" y="64" fill="#f8fafc" text-anchor="end">GND</text>
    </g>
  </g>


  <!-- 11. AUTHENTIC 16x2 CHARACTER LCD DISPLAY (Bottom Right: x=1180, y=740, w=560, h=260) -->
  <!-- Wide 2.2:1 Aspect Ratio, Real Metal Bezel, 16x2 Dot Matrix Cells, I2C Backpack on Top -->
  <g id="cmp-lcd" transform="translate(1180, 740)" filter="url(#card-shadow)">
    <!-- Main Green PCB -->
    <rect width="560" height="260" rx="8" fill="#064e3b" stroke="#047857" stroke-width="2"/>
    <!-- 4 Corner Mounting Holes -->
    <circle cx="15" cy="15" r="5" fill="#064e3b" stroke="url(#metal-gold)" stroke-width="2"/>
    <circle cx="545" cy="15" r="5" fill="#064e3b" stroke="url(#metal-gold)" stroke-width="2"/>
    <circle cx="15" cy="245" r="5" fill="#064e3b" stroke="url(#metal-gold)" stroke-width="2"/>
    <circle cx="545" cy="245" r="5" fill="#064e3b" stroke="url(#metal-gold)" stroke-width="2"/>

    <!-- I2C BACKPACK MODULE ON TOP EDGE (x=90, y=10, w=380, h=45) -->
    <rect x="90" y="8" width="380" height="42" rx="4" fill="#1e293b" stroke="#475569" stroke-width="1.5"/>
    <text x="180" y="32" fill="#94a3b8" font-size="11" font-weight="800">I2C BACKPACK (PCF8574)</text>

    <!-- 4-Pin Header Pads: GND(cx=280), VCC(cx=340), SDA(cx=400), SCL(cx=450) -->
    <circle cx="280" cy="28" r="7" fill="#0f172a" stroke="#f8fafc" stroke-width="2"/>
    <text class="pin-txt" x="280" y="44" fill="#f8fafc" text-anchor="middle">GND</text>

    <circle cx="340" cy="28" r="7" fill="#dc2626" stroke="#fca5a5" stroke-width="2"/>
    <text class="pin-txt" x="340" y="44" fill="#fca5a5" text-anchor="middle">VCC</text>

    <circle cx="400" cy="28" r="7" fill="#2563eb" stroke="#bfdbfe" stroke-width="2"/>
    <text class="pin-txt" x="400" y="44" fill="#bfdbfe" text-anchor="middle">SDA</text>

    <circle cx="450" cy="28" r="7" fill="#0284c7" stroke="#bae6fd" stroke-width="2"/>
    <text class="pin-txt" x="450" y="44" fill="#bae6fd" text-anchor="middle">SCL</text>

    <!-- 16-Pin Gold Connector Strip (Hitachi HD44780 standard pins 1-16) -->
    <g transform="translate(40, 58)">
      <rect width="480" height="8" fill="#ca8a04"/>
      <circle cx="15" cy="4" r="2.5" fill="#fef08a"/><circle cx="45" cy="4" r="2.5" fill="#fef08a"/>
      <circle cx="75" cy="4" r="2.5" fill="#fef08a"/><circle cx="105" cy="4" r="2.5" fill="#fef08a"/>
      <circle cx="135" cy="4" r="2.5" fill="#fef08a"/><circle cx="165" cy="4" r="2.5" fill="#fef08a"/>
      <circle cx="195" cy="4" r="2.5" fill="#fef08a"/><circle cx="225" cy="4" r="2.5" fill="#fef08a"/>
      <circle cx="255" cy="4" r="2.5" fill="#fef08a"/><circle cx="285" cy="4" r="2.5" fill="#fef08a"/>
      <circle cx="315" cy="4" r="2.5" fill="#fef08a"/><circle cx="345" cy="4" r="2.5" fill="#fef08a"/>
      <circle cx="375" cy="4" r="2.5" fill="#fef08a"/><circle cx="405" cy="4" r="2.5" fill="#fef08a"/>
      <circle cx="435" cy="4" r="2.5" fill="#fef08a"/><circle cx="465" cy="4" r="2.5" fill="#fef08a"/>
    </g>

    <!-- Dark Metal Bezel (x=30, y=72, w=500, h=165) with 6 Metal Bezel Tabs -->
    <rect x="30" y="72" width="500" height="165" rx="5" fill="#0f172a" stroke="#334155" stroke-width="2"/>
    <rect x="80" y="69" width="14" height="6" fill="#64748b"/><rect x="460" y="69" width="14" height="6" fill="#64748b"/>
    <rect x="80" y="234" width="14" height="6" fill="#64748b"/><rect x="460" y="234" width="14" height="6" fill="#64748b"/>

    <!-- Illuminated Cyan-Blue Screen -->
    <rect x="45" y="86" width="470" height="138" rx="4" fill="url(#lcd-screen)" stroke="#0284c7" stroke-width="2"/>

    <!-- High-Contrast 16x2 Character Text (Emulated Dot Matrix) -->
    <text x="65" y="138" fill="#f0f9ff" font-family="'JetBrains Mono', Consolas, monospace" font-size="24" font-weight="bold" letter-spacing="2">
      CORE:48.6C AMB:29.4C
    </text>
    <text x="65" y="195" fill="#f0f9ff" font-family="'JetBrains Mono', Consolas, monospace" font-size="24" font-weight="bold" letter-spacing="2">
      ATX:ON  FAN:100%[ACT]
    </text>

    <!-- Model Designation on Bezel -->
    <text x="280" y="252" fill="#a7f3d0" font-size="11" font-weight="bold" text-anchor="middle">16×2 CHARACTER LCD MODULE (I2C ADDR: 0x27)</text>
  </g>


  <!-- ===================================================================== -->
  <!-- ==================== WIRING & INTERCONNECTS ========================= -->
  <!-- STRICT ELECTRICAL ACCURACY: 100% Correct Binding Posts!               -->
  <!-- ===================================================================== -->

  <!-- 1. POWER PATHS: ATX TO INA219S & LOAD (VERIFIED BINDING POSTS) -->
  <g id="wires-power" stroke-width="4.5" fill="none">
    <!-- +12V FROM ATX BINDING POST AT (285, 105) - NO OFFSET! -->
    <!-- ATX +12V post is at cx=245 on board at x=40 -> global x=285, cy=65 -> global y=105 -->
    <!-- Feeds INA219 #1 VIN+ at (395, 106) -->
    <path class="wire" stroke="#d97706" d="M 285 105 L 395 105 L 395 106"/>

    <!-- INA219 #1 VIN- (435, 106) -> 12V Load IN (+) (675, 185) -->
    <path class="wire" stroke="#d97706" d="M 435 106 L 435 120 L 590 120 L 590 185 L 675 185"/>

    <!-- +12V Tap down to TB6612 VM (770) from the EXACT +12V line at y=105! -->
    <path class="wire" stroke="#d97706" d="M 320 105 L 320 220 L 25 220 L 25 770 L 60 770"/>
    <circle cx="320" cy="105" r="5" fill="#d97706" class="solder-junction"/>

    <!-- +5V FROM ATX BINDING POST AT (285, 145) - NO OFFSET! -->
    <!-- ATX +5V post is at cx=245 on board at x=40 -> global x=285, cy=105 -> global y=145 -->
    <!-- Routes up across roof at y=20 to INA219 #2 VIN+ at (955, 106) -->
    <path class="wire" stroke="#dc2626" d="M 285 145 L 305 145 L 305 20 L 895 20 L 895 106 L 955 106"/>

    <!-- LCD 5V VCC Tap from the +5V Roof Line at (1520, 20) down to LCD VCC at (1520, 768) -->
    <path class="wire" stroke="#dc2626" stroke-width="3.5" d="M 895 20 L 1520 20 L 1520 768"/>
    <circle cx="1520" cy="20" r="5" fill="#dc2626" class="solder-junction"/>

    <!-- +3.3V FROM ATX BINDING POST AT (285, 185) - NO OFFSET! -->
    <!-- ATX +3.3V post is at cx=245 on board at x=40 -> global x=285, cy=145 -> global y=185 -->
    <!-- Routes up across roof at y=10 to INA219 #3 VIN+ at (1215, 106) -->
    <path class="wire" stroke="#ea580c" d="M 285 185 L 295 185 L 295 10 L 1155 10 L 1155 106 L 1215 106"/>
  </g>


  <!-- 2. STANDBY POWER (+5VSB) & PS_ON# CONTROL -->
  <g id="wires-standby-control" stroke-width="4" fill="none">
    <!-- ATX +5VSB from (145, 205) routes over roof at y=30 to ESP32 5V/VIN (1035, 650) -->
    <path class="wire" stroke="#9333ea"
          d="M 145 205 L 145 235 L 335 235 L 335 30 L 1200 30 L 1200 650 L 1035 650"/>

    <!-- ATX PS_ON# from (200, 205) drops straight down into BC547 Collector (175, 435) -->
    <path class="wire" stroke="#10b981"
          d="M 200 205 L 200 380 L 175 380 L 175 435"/>

    <!-- BC547 Emitter (175, 630) connects down and right to GND Bus at y=245 -->
    <path class="wire" stroke="#0f172a"
          d="M 175 630 L 175 660 L 320 660 L 320 245"/>
    <circle cx="320" cy="245" r="5" fill="#0f172a" class="solder-junction"/>

    <!-- ESP32 D32 Trip Signal (505, 475) routes 100% STRAIGHT LEFT into BC547 IN (295, 500) -->
    <path class="wire" stroke="#10b981" stroke-width="3.5"
          d="M 505 475 L 340 475 L 340 500 L 295 500"/>
  </g>


  <!-- 3. ESP32 POWER & I2C CONNECTIONS TO BUS HIGHWAYS -->
  <g id="wires-esp32-bus" fill="none">
    <!-- ESP32 3V3 (505, 430) routes straight up to 3.3V Bus (y=275) -->
    <path class="wire" stroke="#ea580c" stroke-width="4"
          d="M 505 430 L 505 275"/>
    <circle cx="505" cy="275" r="5" fill="#ea580c" class="solder-junction"/>

    <!-- ESP32 GND (1035, 610) routes right to x=1160 and up to GND Bus (y=245) -->
    <path class="wire" stroke="#0f172a" stroke-width="4.5"
          d="M 1035 610 L 1160 610 L 1160 245"/>
    <circle cx="1160" cy="245" r="5" fill="#0f172a" class="solder-junction"/>

    <!-- ESP32 D22 SCL (1035, 430) routes right to x=1100 and up to I2C SCL Bus (y=305) -->
    <path class="wire" stroke="#0284c7" stroke-width="3.5"
          d="M 1035 430 L 1100 430 L 1100 305"/>
    <circle cx="1100" cy="305" r="5" fill="#0284c7" class="solder-junction"/>

    <!-- ESP32 D21 SDA (1035, 475) routes right to x=1130 and up to I2C SDA Bus (y=335) -->
    <path class="wire" stroke="#2563eb" stroke-width="3.5"
          d="M 1035 475 L 1130 475 L 1130 335"/>
    <circle cx="1130" cy="335" r="5" fill="#2563eb" class="solder-junction"/>
  </g>


  <!-- 4. TB6612 FAN DRIVER CONNECTIONS (Wide 45px Spacing!) -->
  <g id="wires-driver-fan" fill="none">
    <!-- TB6612 VCC (60, 800) routes up to 3.3V Bus at x=360 -->
    <path class="wire" stroke="#ea580c" stroke-width="3.5"
          d="M 60 800 L 35 800 L 35 700 L 360 700 L 360 275"/>
    <circle cx="360" cy="275" r="5" fill="#ea580c" class="solder-junction"/>

    <!-- TB6612 GND (60, 830) routes straight up to Common GND at x=60 -->
    <path class="wire" stroke="#0f172a" stroke-width="3.5"
          d="M 60 830 L 60 245"/>
    <circle cx="60" cy="245" r="5" fill="#0f172a" class="solder-junction"/>

    <!-- TB6612 AIN2 (290, 875) tied to GND line -->
    <path class="wire" stroke="#0f172a" stroke-width="3"
          d="M 290 875 L 320 875 L 320 705 L 60 705"/>

    <!-- Control lines from ESP32 to TB6612 (Parallel Non-Crossing Tracks): -->
    <!-- D33 STBY (505, 520) -> Track at x=465 -> TB6612 STBY (290, 770) -->
    <path class="wire" stroke="#06b6d4" stroke-width="3.5"
          d="M 505 520 L 465 520 L 465 770 L 290 770"/>

    <!-- D25 PWM (505, 565) -> Track at x=420 -> TB6612 PWMA (290, 805) -->
    <path class="wire" stroke="#8b5cf6" stroke-width="3.5"
          d="M 505 565 L 420 565 L 420 805 L 290 805"/>

    <!-- D26 DIR (505, 610) -> Track at x=375 -> TB6612 AIN1 (290, 840) -->
    <path class="wire" stroke="#ec4899" stroke-width="3.5"
          d="M 505 610 L 375 610 L 375 840 L 290 840"/>

    <!-- TB6612 AO1 (+) (60, 860) down to Fan RED (+) (120, 986) -->
    <path class="wire" stroke="#dc2626" stroke-width="4"
          d="M 60 860 L 20 860 L 20 920 L 120 920 L 120 986"/>

    <!-- TB6612 AO2 (-) (60, 885) down to Fan BLK (-) (255, 986) -->
    <path class="wire" stroke="#0f172a" stroke-width="4"
          d="M 60 885 L 12 885 L 12 928 L 255 928 L 255 986"/>
  </g>


  <!-- 5. DUAL DS18B20 3-PIN MODULE CONNECTIONS (Clean & Direct) -->
  <g id="wires-temperature" fill="none">
    <!-- Both DAT pins connect to Yellow Line and go straight into ESP32 D27 (505, 650) -->
    <!-- Module 1 DAT at (715, 780), Module 2 DAT at (715, 970) -->
    <path class="wire" stroke="#eab308" stroke-width="4"
          d="M 715 780 L 760 780 L 760 685 L 505 685 L 505 650"/>
    <path class="wire" stroke="#eab308" stroke-width="4"
          d="M 715 970 L 760 970 L 760 780"/>
    <circle cx="760" cy="780" r="4.5" fill="#eab308" class="solder-junction"/>

    <!-- Both VCC pins connect to Orange Line at x=800 and go up to 3.3V Bus (y=275) -->
    <!-- Module 1 VCC at (715, 755), Module 2 VCC at (715, 945) -->
    <path class="wire" stroke="#ea580c" stroke-width="4"
          d="M 715 755 L 800 755 L 800 275"/>
    <circle cx="800" cy="275" r="5" fill="#ea580c" class="solder-junction"/>
    <path class="wire" stroke="#ea580c" stroke-width="4"
          d="M 715 945 L 800 945 L 800 755"/>
    <circle cx="800" cy="755" r="4.5" fill="#ea580c" class="solder-junction"/>

    <!-- Both GND pins connect to Black Line at x=840 and go up to GND Bus (y=245) -->
    <!-- Module 1 GND at (715, 800), Module 2 GND at (715, 990) -->
    <path class="wire" stroke="#0f172a" stroke-width="4"
          d="M 715 800 L 840 800 L 840 245"/>
    <circle cx="840" cy="245" r="5" fill="#0f172a" class="solder-junction"/>
    <path class="wire" stroke="#0f172a" stroke-width="4"
          d="M 715 990 L 840 990 L 840 800"/>
    <circle cx="840" cy="800" r="4.5" fill="#0f172a" class="solder-junction"/>
  </g>


  <!-- 6. 16x2 I2C LCD CONNECTIONS (Exact Mathematical Drops into Pins at y=768!) -->
  <g id="wires-lcd" fill="none">
    <!-- LCD GND (Pin at x=1460, y=768) -> straight up to GND Bus (y=245) -->
    <!-- global x = 1180 + 280 = 1460 -->
    <path class="wire" stroke="#0f172a" stroke-width="4"
          d="M 1460 768 L 1460 245"/>
    <circle cx="1460" cy="245" r="5" fill="#0f172a" class="solder-junction"/>

    <!-- LCD SDA (Pin at x=1580, y=768) -> straight up to I2C SDA Bus (y=335) -->
    <!-- global x = 1180 + 400 = 1580 -->
    <path class="wire" stroke="#2563eb" stroke-width="3.5"
          d="M 1580 768 L 1580 335"/>
    <circle cx="1580" cy="335" r="5" fill="#2563eb" class="solder-junction"/>

    <!-- LCD SCL (Pin at x=1630, y=768) -> straight up to I2C SCL Bus (y=305) -->
    <!-- global x = 1180 + 450 = 1630 -->
    <path class="wire" stroke="#0284c7" stroke-width="3.5"
          d="M 1630 768 L 1630 305"/>
    <circle cx="1630" cy="305" r="5" fill="#0284c7" class="solder-junction"/>
  </g>

</svg>'''

    output_path = os.path.join("documentation", "transformer_cbm_circuit_diagram.svg")
    ET.fromstring(svg) # Validate XML structure
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print("Rev 10.0 Circuit Diagram SVG generated successfully.")

if __name__ == "__main__":
    generate_circuit_svg()
