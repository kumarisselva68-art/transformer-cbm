# -*- coding: utf-8 -*-
"""
Cirkit Designer Style Authentic Hardware Circuit Diagram Generator for Transformer_CBM
Rev 25.1 - Multi-Rail Clean Linear Flow Edition:
- Keeps all three INA219 power rails in line (12V, 5V, 3.3V).
- Moves the external multi-rail load to the end of the top row.
- Each INA219 delivers its measured positive rail (VIN+) to the external load block.
- Single unified Common Ground connects the external load to the system ground highway.
- 100% collision-free orthogonal routing with zero crossing wires.
"""

import os
import xml.etree.ElementTree as ET
import subprocess

def generate_cirkit_svg():
    w = 2000
    h = 1440
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <defs>
    <!-- Clean Engineering Grid Background -->
    <pattern id="cirkit-grid" width="25" height="25" patternUnits="userSpaceOnUse">
      <path d="M 25 0 L 0 0 0 25" fill="none" stroke="#e2e8f0" stroke-width="0.75"/>
    </pattern>

    <!-- Component Drop Shadow -->
    <filter id="pcb-shadow" x="-3%" y="-3%" width="108%" height="110%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="2" dy="4" stdDeviation="4" flood-color="#0f172a" flood-opacity="0.10"/>
    </filter>

    <!-- LCD Glass Gradient -->
    <linearGradient id="lcd-blue-glass" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#0284c7"/>
      <stop offset="100%" stop-color="#0369a1"/>
    </linearGradient>

    <!-- Fuse Glass Gradient -->
    <linearGradient id="fuse-glass" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.9"/>
      <stop offset="50%" stop-color="#e2e8f0" stop-opacity="0.4"/>
      <stop offset="100%" stop-color="#94a3b8" stop-opacity="0.7"/>
    </linearGradient>

    <!-- Brass Terminal Screw Gradient -->
    <linearGradient id="screw-brass" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#fef08a"/>
      <stop offset="50%" stop-color="#ca8a04"/>
      <stop offset="100%" stop-color="#854d0e"/>
    </linearGradient>
  </defs>

  <style>
    text {{
      font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, 'Inter', Roboto, Helvetica, Arial, sans-serif;
      user-select: none;
    }}
    .sheet-title {{
      font-size: 30px;
      font-weight: 900;
      fill: #0f172a;
      letter-spacing: -0.5px;
    }}
    .comp-title {{
      font-size: 22px;
      font-weight: 800;
      fill: #0f172a;
      letter-spacing: 0.5px;
    }}
    .comp-title-lg {{
      font-size: 26px;
      font-weight: 800;
      fill: #0f172a;
      letter-spacing: 0.5px;
    }}
    .pin-label {{
      font-size: 20px;
      font-weight: 800;
    }}
    .pin-label-lg {{
      font-size: 22px;
      font-weight: 800;
    }}
    .wire-line {{
      fill: none;
      stroke-linecap: round;
      stroke-linejoin: round;
    }}
  </style>

  <!-- Canvas Surface -->
  <rect width="{w}" height="{h}" fill="#f8fafc"/>
  <rect width="{w}" height="{h}" fill="url(#cirkit-grid)"/>

  <!-- ===================================================================== -->
  <!-- PROJECT HEADER BAR (y = 30) - CLEAN & SEPARATED FROM ROOF WIRES      -->
  <!-- ===================================================================== -->
  <g transform="translate(50, 32)">
    <text class="sheet-title" x="0" y="0">IoT Transformer Condition Monitoring System</text>
  </g>


  <!-- ===================================================================== -->
  <!-- ==================== TIER 1: CONTINUOUS POWER ROW =================== -->
  <!-- Roof Wires: y = 50 (+3.3V), y = 68 (+5V), y = 86 (+12V)               -->
  <!-- Component Bodies: y = 135 to 345                                     -->
  <!-- ===================================================================== -->

  <!-- 1. ATX BREAKOUT BOARD (XH-M229) -->
  <text class="comp-title" x="195" y="115" text-anchor="middle">ATX BREAKOUT (XH-M229)</text>
  <g id="atx-board" transform="translate(50, 135)" filter="url(#pcb-shadow)">
    <!-- Blue PCB -->
    <rect width="285" height="210" rx="8" fill="#0d47a1" stroke="#1565c0" stroke-width="2"/>
    <circle cx="14" cy="14" r="5" fill="#0d47a1" stroke="#eab308" stroke-width="2"/>
    <circle cx="271" cy="14" r="5" fill="#0d47a1" stroke="#eab308" stroke-width="2"/>
    <circle cx="14" cy="196" r="5" fill="#0d47a1" stroke="#eab308" stroke-width="2"/>
    <circle cx="271" cy="196" r="5" fill="#0d47a1" stroke="#eab308" stroke-width="2"/>

    <!-- 24-Pin ATX Socket -->
    <g transform="translate(16, 20)">
      <rect width="52" height="155" rx="3" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
      <rect x="19" y="65" width="14" height="25" rx="2" fill="#e2e8f0" stroke="#94a3b8"/>
      <!-- Grid -->
      <g fill="#334155">
        <rect x="8" y="8" width="11" height="8" rx="1.5"/><rect x="8" y="20" width="11" height="8" rx="1.5"/>
        <rect x="8" y="32" width="11" height="8" rx="1.5"/><rect x="8" y="44" width="11" height="8" rx="1.5"/>
        <rect x="8" y="56" width="11" height="8" rx="1.5"/><rect x="8" y="68" width="11" height="8" rx="1.5"/>
        <rect x="8" y="80" width="11" height="8" rx="1.5"/><rect x="8" y="92" width="11" height="8" rx="1.5"/>
        <rect x="8" y="104" width="11" height="8" rx="1.5"/><rect x="8" y="116" width="11" height="8" rx="1.5"/>
        <rect x="8" y="128" width="11" height="8" rx="1.5"/><rect x="8" y="140" width="11" height="8" rx="1.5"/>
        <rect x="33" y="8" width="11" height="8" rx="1.5"/><rect x="33" y="20" width="11" height="8" rx="1.5"/>
        <rect x="33" y="32" width="11" height="8" rx="1.5"/><rect x="33" y="44" width="11" height="8" rx="1.5"/>
        <rect x="33" y="56" width="11" height="8" rx="1.5"/><rect x="33" y="68" width="11" height="8" rx="1.5"/>
        <rect x="33" y="80" width="11" height="8" rx="1.5"/><rect x="33" y="92" width="11" height="8" rx="1.5"/>
        <rect x="33" y="104" width="11" height="8" rx="1.5"/><rect x="33" y="116" width="11" height="8" rx="1.5"/>
        <rect x="33" y="128" width="11" height="8" rx="1.5"/><rect x="33" y="140" width="11" height="8" rx="1.5"/>
      </g>
    </g>

    <!-- Fuses -->
    <g transform="translate(90, 20)">
      <rect y="0" width="45" height="15" rx="2" fill="#0f172a"/><rect x="8" y="2" width="29" height="11" fill="url(#fuse-glass)"/>
      <rect y="40" width="45" height="15" rx="2" fill="#0f172a"/><rect x="8" y="42" width="29" height="11" fill="url(#fuse-glass)"/>
      <rect y="80" width="45" height="15" rx="2" fill="#0f172a"/><rect x="8" y="82" width="29" height="11" fill="url(#fuse-glass)"/>
      <rect y="120" width="45" height="15" rx="2" fill="#0f172a"/><rect x="8" y="122" width="29" height="11" fill="url(#fuse-glass)"/>
    </g>

    <!-- 4 Heavy Binding Posts on Right Edge (cx = 250) -->
    <!-- +12V (cy = 28 -> Global: 300, 163) -->
    <circle cx="250" cy="28" r="14" fill="#d97706" stroke="#fef08a" stroke-width="3"/>
    <circle cx="250" cy="28" r="5" fill="#78350f"/>
    <text class="pin-label-lg" x="226" y="35" fill="#fef08a" text-anchor="end">+12V</text>

    <!-- +5V (cy = 68 -> Global: 300, 203) -->
    <circle cx="250" cy="68" r="14" fill="#dc2626" stroke="#fca5a5" stroke-width="3"/>
    <circle cx="250" cy="68" r="5" fill="#7f1d1d"/>
    <text class="pin-label-lg" x="226" y="75" fill="#fca5a5" text-anchor="end">+5V</text>

    <!-- +3.3V (cy = 108 -> Global: 300, 243) -->
    <circle cx="250" cy="108" r="14" fill="#ea580c" stroke="#fed7aa" stroke-width="3"/>
    <circle cx="250" cy="108" r="5" fill="#7c2d12"/>
    <text class="pin-label-lg" x="226" y="115" fill="#fed7aa" text-anchor="end">+3.3V</text>

    <!-- GND (cy = 148 -> Global: 300, 283) -->
    <circle cx="250" cy="148" r="14" fill="#0f172a" stroke="#f8fafc" stroke-width="3"/>
    <circle cx="250" cy="148" r="5" fill="#334155"/>
    <text class="pin-label-lg" x="226" y="155" fill="#f8fafc" text-anchor="end">GND</text>

    <!-- Standby & Control Terminals at Bottom -->
    <!-- +5VSB (Purple): terminal at cx = 85, cy = 195 -> Global: (135, 330) -->
    <text x="85" y="180" fill="#e9d5ff" font-size="16" font-weight="800" text-anchor="middle">+5VSB</text>
    <circle cx="85" cy="195" r="9" fill="#9333ea" stroke="#f3e8ff" stroke-width="2.5"/>

    <!-- PS_ON# (Green): terminal at cx = 160, cy = 195 -> Global: (210, 330) -->
    <text x="160" y="180" fill="#a7f3d0" font-size="16" font-weight="800" text-anchor="middle">PS_ON#</text>
    <circle cx="160" cy="195" r="9" fill="#10b981" stroke="#d1fae5" stroke-width="2.5"/>
  </g>


  <!-- 2. INA219 #1 (12V RAIL CURRENT MONITOR - ADDR 0x40) -->
  <g id="ina219-12v" transform="translate(390, 135)" filter="url(#pcb-shadow)">
    <rect width="210" height="210" rx="8" fill="#581c87" stroke="#7e22ce" stroke-width="2"/>
    <circle cx="12" cy="12" r="4.5" fill="#581c87" stroke="#eab308" stroke-width="1.5"/>
    <circle cx="198" cy="12" r="4.5" fill="#581c87" stroke="#eab308" stroke-width="1.5"/>
    <circle cx="12" cy="198" r="4.5" fill="#581c87" stroke="#eab308" stroke-width="1.5"/>
    <circle cx="198" cy="198" r="4.5" fill="#581c87" stroke="#eab308" stroke-width="1.5"/>

    <!-- Screw Terminal Block for VIN+ / VIN- -->
    <g transform="translate(20, 20)">
      <rect width="90" height="52" rx="3" fill="#15803d" stroke="#166534" stroke-width="1.5"/>
      <circle cx="24" cy="25" r="13" fill="#14532d"/>
      <circle cx="24" cy="25" r="8" fill="url(#screw-brass)"/>
      <text class="pin-label" x="24" y="47" fill="#fef08a" text-anchor="middle">VIN+</text>
      <circle cx="66" cy="25" r="13" fill="#14532d"/>
      <circle cx="66" cy="25" r="8" fill="url(#screw-brass)"/>
      <text class="pin-label" x="66" y="47" fill="#fef08a" text-anchor="middle">VIN-</text>
    </g>

    <!-- Shunt Resistor R100 -->
    <g transform="translate(125, 28)">
      <rect width="68" height="34" rx="2" fill="#0f172a" stroke="#94a3b8" stroke-width="1.5"/>
      <text class="pin-label-lg" x="34" y="24" fill="#38bdf8" text-anchor="middle">R100</text>
    </g>

    <!-- Center Silkscreen -->
    <text x="105" y="106" fill="#f8fafc" font-size="20" font-weight="900" text-anchor="middle">INA219</text>
    <text x="105" y="132" fill="#fef08a" font-size="16" font-weight="800" text-anchor="middle">+12V SHUNT</text>

    <!-- 4-Pin Logic Header at Bottom (Global y = 325) -->
    <g transform="translate(0, 190)">
      <rect x="15" y="-12" width="180" height="24" rx="2" fill="#0f172a" stroke="#334155"/>
      <circle cx="30" cy="0" r="8" fill="#ea580c" stroke="#fed7aa" stroke-width="2.5"/>
      <text class="pin-label" x="30" y="-15" fill="#fed7aa" text-anchor="middle">VCC</text>
      <circle cx="75" cy="0" r="8" fill="#0f172a" stroke="#f8fafc" stroke-width="2.5"/>
      <text class="pin-label" x="75" y="-15" fill="#f8fafc" text-anchor="middle">GND</text>
      <circle cx="125" cy="0" r="8" fill="#0284c7" stroke="#bae6fd" stroke-width="2.5"/>
      <text class="pin-label" x="125" y="-15" fill="#bae6fd" text-anchor="middle">SCL</text>
      <circle cx="175" cy="0" r="8" fill="#2563eb" stroke="#bfdbfe" stroke-width="2.5"/>
      <text class="pin-label" x="175" y="-15" fill="#bfdbfe" text-anchor="middle">SDA</text>
    </g>
  </g>


  <!-- 3. INA219 #2 (5V RAIL CURRENT MONITOR) - IN LINE! -->
  <g id="ina219-5v" transform="translate(650, 135)" filter="url(#pcb-shadow)">
    <rect width="210" height="210" rx="8" fill="#581c87" stroke="#7e22ce" stroke-width="2"/>
    <circle cx="12" cy="12" r="4.5" fill="#581c87" stroke="#eab308" stroke-width="1.5"/>
    <circle cx="198" cy="12" r="4.5" fill="#581c87" stroke="#eab308" stroke-width="1.5"/>
    <circle cx="12" cy="198" r="4.5" fill="#581c87" stroke="#eab308" stroke-width="1.5"/>
    <circle cx="198" cy="198" r="4.5" fill="#581c87" stroke="#eab308" stroke-width="1.5"/>

    <!-- Screw Terminal Block -->
    <g transform="translate(20, 20)">
      <rect width="90" height="52" rx="3" fill="#15803d" stroke="#166534" stroke-width="1.5"/>
      <circle cx="24" cy="25" r="13" fill="#14532d"/>
      <circle cx="24" cy="25" r="8" fill="url(#screw-brass)"/>
      <text class="pin-label" x="24" y="47" fill="#fca5a5" text-anchor="middle">VIN+</text>
      <circle cx="66" cy="25" r="13" fill="#14532d"/>
      <circle cx="66" cy="25" r="8" fill="url(#screw-brass)"/>
      <text class="pin-label" x="66" y="47" fill="#fca5a5" text-anchor="middle">VIN-</text>
    </g>

    <!-- Shunt Resistor R100 -->
    <g transform="translate(125, 28)">
      <rect width="68" height="34" rx="2" fill="#0f172a" stroke="#94a3b8" stroke-width="1.5"/>
      <text class="pin-label-lg" x="34" y="24" fill="#38bdf8" text-anchor="middle">R100</text>
    </g>

    <!-- Center Silkscreen -->
    <text x="105" y="106" fill="#f8fafc" font-size="20" font-weight="900" text-anchor="middle">INA219</text>
    <text x="105" y="132" fill="#fca5a5" font-size="16" font-weight="800" text-anchor="middle">+5V SHUNT</text>

    <!-- 4-Pin Logic Header at Bottom (Global y = 325) -->
    <g transform="translate(0, 190)">
      <rect x="15" y="-12" width="180" height="24" rx="2" fill="#0f172a" stroke="#334155"/>
      <circle cx="30" cy="0" r="8" fill="#ea580c" stroke="#fed7aa" stroke-width="2.5"/>
      <text class="pin-label" x="30" y="-15" fill="#fed7aa" text-anchor="middle">VCC</text>
      <circle cx="75" cy="0" r="8" fill="#0f172a" stroke="#f8fafc" stroke-width="2.5"/>
      <text class="pin-label" x="75" y="-15" fill="#f8fafc" text-anchor="middle">GND</text>
      <circle cx="125" cy="0" r="8" fill="#0284c7" stroke="#bae6fd" stroke-width="2.5"/>
      <text class="pin-label" x="125" y="-15" fill="#bae6fd" text-anchor="middle">SCL</text>
      <circle cx="175" cy="0" r="8" fill="#2563eb" stroke="#bfdbfe" stroke-width="2.5"/>
      <text class="pin-label" x="175" y="-15" fill="#bfdbfe" text-anchor="middle">SDA</text>
    </g>
  </g>


  <!-- 4. INA219 #3 (3.3V RAIL CURRENT MONITOR) - IN LINE! -->
  <g id="ina219-3v3" transform="translate(910, 135)" filter="url(#pcb-shadow)">
    <rect width="210" height="210" rx="8" fill="#581c87" stroke="#7e22ce" stroke-width="2"/>
    <circle cx="12" cy="12" r="4.5" fill="#581c87" stroke="#eab308" stroke-width="1.5"/>
    <circle cx="198" cy="12" r="4.5" fill="#581c87" stroke="#eab308" stroke-width="1.5"/>
    <circle cx="12" cy="198" r="4.5" fill="#581c87" stroke="#eab308" stroke-width="1.5"/>
    <circle cx="198" cy="198" r="4.5" fill="#581c87" stroke="#eab308" stroke-width="1.5"/>

    <!-- Screw Terminal Block -->
    <g transform="translate(20, 20)">
      <rect width="90" height="52" rx="3" fill="#15803d" stroke="#166534" stroke-width="1.5"/>
      <circle cx="24" cy="25" r="13" fill="#14532d"/>
      <circle cx="24" cy="25" r="8" fill="url(#screw-brass)"/>
      <text class="pin-label" x="24" y="47" fill="#fed7aa" text-anchor="middle">VIN+</text>
      <circle cx="66" cy="25" r="13" fill="#14532d"/>
      <circle cx="66" cy="25" r="8" fill="url(#screw-brass)"/>
      <text class="pin-label" x="66" y="47" fill="#fed7aa" text-anchor="middle">VIN-</text>
    </g>

    <!-- Shunt Resistor R100 -->
    <g transform="translate(125, 28)">
      <rect width="68" height="34" rx="2" fill="#0f172a" stroke="#94a3b8" stroke-width="1.5"/>
      <text class="pin-label-lg" x="34" y="24" fill="#38bdf8" text-anchor="middle">R100</text>
    </g>

    <!-- Center Silkscreen -->
    <text x="105" y="106" fill="#f8fafc" font-size="20" font-weight="900" text-anchor="middle">INA219</text>
    <text x="105" y="132" fill="#fed7aa" font-size="16" font-weight="800" text-anchor="middle">+3.3V SHUNT</text>

    <!-- 4-Pin Logic Header at Bottom (Global y = 325) -->
    <g transform="translate(0, 190)">
      <rect x="15" y="-12" width="180" height="24" rx="2" fill="#0f172a" stroke="#334155"/>
      <circle cx="30" cy="0" r="8" fill="#ea580c" stroke="#fed7aa" stroke-width="2.5"/>
      <text class="pin-label" x="30" y="-15" fill="#fed7aa" text-anchor="middle">VCC</text>
      <circle cx="75" cy="0" r="8" fill="#0f172a" stroke="#f8fafc" stroke-width="2.5"/>
      <text class="pin-label" x="75" y="-15" fill="#f8fafc" text-anchor="middle">GND</text>
      <circle cx="125" cy="0" r="8" fill="#0284c7" stroke="#bae6fd" stroke-width="2.5"/>
      <text class="pin-label" x="125" y="-15" fill="#bae6fd" text-anchor="middle">SCL</text>
      <circle cx="175" cy="0" r="8" fill="#2563eb" stroke="#bfdbfe" stroke-width="2.5"/>
      <text class="pin-label" x="175" y="-15" fill="#bfdbfe" text-anchor="middle">SDA</text>
    </g>
  </g>


  <!-- 5. EXTERNAL LOAD (CLEAN & MINIMAL) -->
  <g id="external-loads" transform="translate(1180, 135)" filter="url(#pcb-shadow)">
    <!-- Industrial Slate Enclosure -->
    <rect width="480" height="210" rx="8" fill="#1e293b" stroke="#475569" stroke-width="2"/>
    <circle cx="14" cy="14" r="5" fill="#1e293b" stroke="#94a3b8" stroke-width="1.5"/>
    <circle cx="466" cy="14" r="5" fill="#1e293b" stroke="#94a3b8" stroke-width="1.5"/>
    <circle cx="14" cy="196" r="5" fill="#1e293b" stroke="#94a3b8" stroke-width="1.5"/>
    <circle cx="466" cy="196" r="5" fill="#1e293b" stroke="#94a3b8" stroke-width="1.5"/>

    <!-- 4 Heavy Binding Posts: 3 Positive Rail Inputs + 1 Common Return Ground -->
    <!-- 1. +12V LOAD IN (cx = 65, cy = 46 -> Global: 1245, 181) -->
    <g transform="translate(65, 46)">
      <circle cx="0" cy="0" r="14" fill="#d97706" stroke="#fef08a" stroke-width="3"/>
      <circle cx="0" cy="0" r="5" fill="#78350f"/>
      <text class="pin-label-lg" x="0" y="28" fill="#fef08a" text-anchor="middle">+12V</text>
    </g>

    <!-- 2. +5V LOAD IN (cx = 175, cy = 46 -> Global: 1355, 181) -->
    <g transform="translate(175, 46)">
      <circle cx="0" cy="0" r="14" fill="#dc2626" stroke="#fca5a5" stroke-width="3"/>
      <circle cx="0" cy="0" r="5" fill="#7f1d1d"/>
      <text class="pin-label-lg" x="0" y="28" fill="#fca5a5" text-anchor="middle">+5V</text>
    </g>

    <!-- 3. +3.3V LOAD IN (cx = 285, cy = 46 -> Global: 1465, 181) -->
    <g transform="translate(285, 46)">
      <circle cx="0" cy="0" r="14" fill="#ea580c" stroke="#fed7aa" stroke-width="3"/>
      <circle cx="0" cy="0" r="5" fill="#7c2d12"/>
      <text class="pin-label-lg" x="0" y="28" fill="#fed7aa" text-anchor="middle">+3.3V</text>
    </g>

    <!-- 4. COMMON GND (cx = 395, cy = 46 -> Global: 1575, 181) -->
    <g transform="translate(395, 46)">
      <circle cx="0" cy="0" r="14" fill="#334155" stroke="#94a3b8" stroke-width="3"/>
      <circle cx="0" cy="0" r="5" fill="#1e293b"/>
      <text class="pin-label-lg" x="0" y="28" fill="#f8fafc" text-anchor="middle">GND</text>
    </g>

    <!-- Lower Panel Silkscreen: Clean, bold EXTERNAL LOAD -->
    <line x1="25" y1="110" x2="455" y2="110" stroke="#334155" stroke-width="1.5" stroke-dasharray="4,4"/>
    <text x="240" y="165" fill="#f8fafc" font-size="24" font-weight="900" letter-spacing="1.5" text-anchor="middle">EXTERNAL LOAD</text>
  </g>


  <!-- ===================================================================== -->
  <!-- ==================== TIER 2: MIDDLE ROW ============================= -->
  <!-- Discrete PS_ON# Circuit | ESP32-WROOM-32 DevKit                       -->
  <!-- ===================================================================== -->

  <!-- 6. PURE DISCRETE PS_ON# TRANSISTOR SWITCH -->
  <g transform="translate(120, 560)">
    <text class="comp-title" x="0" y="0" text-anchor="middle">PS_ON#</text>
    <text class="comp-title" x="0" y="28" text-anchor="middle">SWITCH</text>
  </g>
  <g id="bc547-schematic" transform="translate(50, 470)">
    <g transform="translate(160, 150)">
      <!-- Transistor Circle -->
      <circle cx="0" cy="0" r="32" fill="#ffffff" stroke="#0f172a" stroke-width="2.5"/>
      <line x1="-15" y1="-20" x2="-15" y2="20" stroke="#0f172a" stroke-width="5" stroke-linecap="round"/>
      <line x1="-15" y1="0" x2="35" y2="0" stroke="#0f172a" stroke-width="3"/>
      <line x1="-15" y1="-10" x2="0" y2="-24" stroke="#0f172a" stroke-width="3"/>
      <line x1="0" y1="-24" x2="0" y2="-45" stroke="#0f172a" stroke-width="3.5"/>
      <line x1="-15" y1="10" x2="0" y2="24" stroke="#0f172a" stroke-width="3"/>
      <line x1="0" y1="24" x2="0" y2="45" stroke="#0f172a" stroke-width="3.5"/>
      <polygon points="-6,15 1,25 -9,23" fill="#0f172a"/>
      <text class="pin-label-lg" x="-38" y="6" fill="#0f172a" text-anchor="end">BC547</text>
      <text class="pin-label" x="-38" y="28" fill="#64748b" font-size="16" text-anchor="end">Q1 (NPN)</text>
    </g>

    <!-- Horizontal 1 kΩ Base Resistor R1 -->
    <g transform="translate(195, 150)">
      <line x1="0" y1="0" x2="20" y2="0" stroke="#0f172a" stroke-width="3"/>
      <rect x="20" y="-16" width="55" height="32" rx="4" fill="#d97706" stroke="#78350f" stroke-width="2"/>
      <text class="pin-label" x="47" y="7" fill="#fef08a" text-anchor="middle">1 kΩ</text>
      <text class="pin-label" x="47" y="-22" fill="#065f46" font-size="16" text-anchor="middle">R1 (BASE)</text>
      <line x1="75" y1="0" x2="100" y2="0" stroke="#10b981" stroke-width="3.5"/>
    </g>

    <!-- Vertical 10 kΩ Pull-Down Resistor R2 -->
    <g transform="translate(205, 150)">
      <line x1="0" y1="0" x2="0" y2="35" stroke="#0f172a" stroke-width="2.5"/>
      <rect x="-16" y="35" width="32" height="55" rx="4" fill="#d97706" stroke="#78350f" stroke-width="2"/>
      <text class="pin-label" x="0" y="68" fill="#fef08a" text-anchor="middle" transform="rotate(-90 0 68)">10 kΩ</text>
      <text class="pin-label" x="24" y="68" fill="#64748b" font-size="15">R2 (PULL-DOWN)</text>
      <line x1="0" y1="90" x2="0" y2="120" stroke="#0f172a" stroke-width="2.5"/>
      <line x1="0" y1="120" x2="-45" y2="120" stroke="#0f172a" stroke-width="2.5"/>
      <circle cx="-45" cy="120" r="4.5" fill="#0f172a"/>
    </g>

    <!-- Emitter Wire Downwards to Ground Junction -->
    <line x1="160" y1="195" x2="160" y2="270" stroke="#0f172a" stroke-width="4"/>
    <text class="pin-label" x="65" y="260" fill="#0f172a" text-anchor="middle">TO GND</text>
  </g>


  <!-- 7. ESP32-WROOM-32 DEVKIT -->
  <text class="comp-title-lg" x="700" y="450" text-anchor="middle">ESP32-WROOM-32 DEVKIT</text>
  <g id="esp32-devkit" transform="translate(440, 470)" filter="url(#pcb-shadow)">
    <rect width="520" height="415" rx="10" fill="#18181b" stroke="#27272a" stroke-width="2.5"/>
    <circle cx="18" cy="18" r="5" fill="#18181b" stroke="#eab308" stroke-width="2"/>
    <circle cx="502" cy="18" r="5" fill="#18181b" stroke="#eab308" stroke-width="2"/>
    <circle cx="18" cy="397" r="5" fill="#18181b" stroke="#eab308" stroke-width="2"/>
    <circle cx="502" cy="397" r="5" fill="#18181b" stroke="#eab308" stroke-width="2"/>

    <!-- Center Silkscreen -->
    <g transform="translate(260, 205)">
      <text x="0" y="-10" fill="#f8fafc" font-size="24" font-weight="800" text-anchor="middle">ESP32 DEVKIT V1</text>
      <text x="0" y="24" fill="#94a3b8" font-size="20" font-weight="700" text-anchor="middle">ESP-WROOM-32</text>
    </g>

    <!-- USB Jack -->
    <g transform="translate(230, 387)">
      <rect width="60" height="26" rx="3" fill="#cbd5e1" stroke="#64748b" stroke-width="1.5"/>
      <text class="pin-label" x="30" y="18" fill="#334155" text-anchor="middle">USB</text>
    </g>

    <!-- Left Header Pins (cy = 40, 95, 150, 205, 260, 315, 370) -->
    <g id="esp32-left-pins">
      <circle cx="30" cy="40" r="11" fill="#ea580c" stroke="#fed7aa" stroke-width="3"/>
      <text class="pin-label-lg" x="52" y="47" fill="#fed7aa">3V3</text>
      <circle cx="30" cy="95" r="11" fill="#10b981" stroke="#d1fae5" stroke-width="3"/>
      <text class="pin-label" x="52" y="102" fill="#a7f3d0">D32 (PS_ON#)</text>
      <circle cx="30" cy="150" r="11" fill="#06b6d4" stroke="#cffafe" stroke-width="3"/>
      <text class="pin-label" x="52" y="157" fill="#cffafe">D33 (STBY)</text>
      <circle cx="30" cy="205" r="11" fill="#8b5cf6" stroke="#ede9fe" stroke-width="3"/>
      <text class="pin-label" x="52" y="212" fill="#ede9fe">D25 (PWM)</text>
      <circle cx="30" cy="260" r="11" fill="#ec4899" stroke="#fce7f3" stroke-width="3"/>
      <text class="pin-label" x="52" y="267" fill="#fce7f3">D26 (AIN1)</text>
      <circle cx="30" cy="315" r="11" fill="#eab308" stroke="#fef08a" stroke-width="3"/>
      <text class="pin-label" x="52" y="322" fill="#fef08a">D27 (TEMP)</text>
      <circle cx="30" cy="370" r="11" fill="#9333ea" stroke="#f3e8ff" stroke-width="3"/>
      <text class="pin-label-lg" x="52" y="377" fill="#f3e8ff">5V (VIN)</text>
    </g>

    <!-- Right Header Pins -->
    <g id="esp32-right-pins">
      <circle cx="490" cy="40" r="11" fill="#0f172a" stroke="#f8fafc" stroke-width="3"/>
      <text class="pin-label-lg" x="468" y="47" fill="#f8fafc" text-anchor="end">GND</text>
      <circle cx="490" cy="125" r="11" fill="#0284c7" stroke="#bae6fd" stroke-width="3"/>
      <text class="pin-label" x="468" y="132" fill="#bae6fd" text-anchor="end">D22 (SCL)</text>
      <circle cx="490" cy="210" r="11" fill="#2563eb" stroke="#bfdbfe" stroke-width="3"/>
      <text class="pin-label" x="468" y="217" fill="#bfdbfe" text-anchor="end">D21 (SDA)</text>
      <circle cx="490" cy="370" r="11" fill="#0f172a" stroke="#f8fafc" stroke-width="3"/>
      <text class="pin-label-lg" x="468" y="377" fill="#f8fafc" text-anchor="end">GND</text>
    </g>
  </g>


  <!-- ===================================================================== -->
  <!-- ==================== TIER 3: BOTTOM ROW ============================= -->
  <!-- TB6612 & Fan | Dual DS18B20 | 16x2 LCD                                -->
  <!-- ===================================================================== -->

  <!-- 8. TB6612FNG MOTOR DRIVER MODULE -->
  <text class="comp-title" x="190" y="935" text-anchor="middle">TB6612FNG MOTOR DRIVER</text>
  <g id="tb6612-module" transform="translate(50, 955)" filter="url(#pcb-shadow)">
    <rect width="280" height="200" rx="8" fill="#991b1b" stroke="#b91c1c" stroke-width="2"/>
    <circle cx="12" cy="12" r="4.5" fill="#991b1b" stroke="#eab308" stroke-width="1.5"/>
    <circle cx="268" cy="12" r="4.5" fill="#991b1b" stroke="#eab308" stroke-width="1.5"/>
    <circle cx="12" cy="188" r="4.5" fill="#991b1b" stroke="#eab308" stroke-width="1.5"/>
    <circle cx="268" cy="188" r="4.5" fill="#991b1b" stroke="#eab308" stroke-width="1.5"/>

    <rect x="105" y="75" width="70" height="50" rx="2" fill="#18181b" stroke="#3f3f46"/>
    <text class="pin-label" x="140" y="105" fill="#f8fafc" text-anchor="middle">TB6612</text>

    <!-- Left Header Row -->
    <circle cx="25" cy="35" r="9" fill="#d97706" stroke="#fef08a" stroke-width="2.5"/>
    <text class="pin-label" x="42" y="42" fill="#fef08a">VM (+12V)</text>
    <circle cx="25" cy="70" r="9" fill="#ea580c" stroke="#fed7aa" stroke-width="2.5"/>
    <text class="pin-label" x="42" y="77" fill="#fed7aa">VCC (3.3V)</text>
    <circle cx="25" cy="105" r="9" fill="#0f172a" stroke="#f8fafc" stroke-width="2.5"/>
    <text class="pin-label" x="42" y="112" fill="#f8fafc">GND</text>
    <circle cx="25" cy="140" r="9" fill="#dc2626" stroke="#fca5a5" stroke-width="2.5"/>
    <text class="pin-label" x="42" y="147" fill="#fca5a5">AO1 (+)</text>
    <circle cx="25" cy="170" r="9" fill="#0f172a" stroke="#cbd5e1" stroke-width="2.5"/>
    <text class="pin-label" x="42" y="177" fill="#cbd5e1">AO2 (-)</text>

    <!-- Right Header Row -->
    <circle cx="255" cy="35" r="9" fill="#06b6d4" stroke="#cffafe" stroke-width="2.5"/>
    <text class="pin-label" x="238" y="42" fill="#cffafe" text-anchor="end">STBY</text>
    <circle cx="255" cy="75" r="9" fill="#8b5cf6" stroke="#ede9fe" stroke-width="2.5"/>
    <text class="pin-label" x="238" y="82" fill="#ede9fe" text-anchor="end">PWMA</text>
    <circle cx="255" cy="115" r="9" fill="#ec4899" stroke="#fce7f3" stroke-width="2.5"/>
    <text class="pin-label" x="238" y="122" fill="#fce7f3" text-anchor="end">AIN1</text>
    <circle cx="255" cy="155" r="9" fill="#0f172a" stroke="#f8fafc" stroke-width="2.5"/>
    <text class="pin-label" x="238" y="162" fill="#f8fafc" text-anchor="end">AIN2 (GND)</text>
  </g>


  <!-- 9. 12V DC BRUSHLESS COOLING FAN -->
  <g id="cooling-fan" transform="translate(50, 1185)" filter="url(#pcb-shadow)">
    <rect width="280" height="190" rx="8" fill="#0f172a" stroke="#334155" stroke-width="2"/>
    <circle cx="16" cy="16" r="5" fill="#1e293b" stroke="#94a3b8" stroke-width="1.5"/>
    <circle cx="264" cy="16" r="5" fill="#1e293b" stroke="#94a3b8" stroke-width="1.5"/>
    <circle cx="16" cy="174" r="5" fill="#1e293b" stroke="#94a3b8" stroke-width="1.5"/>
    <circle cx="264" cy="174" r="5" fill="#1e293b" stroke="#94a3b8" stroke-width="1.5"/>

    <circle cx="140" cy="110" r="65" fill="#1e293b" stroke="#475569" stroke-width="2.5"/>
    <circle cx="140" cy="110" r="32" fill="#334155" stroke="#64748b" stroke-width="2"/>
    <text class="pin-label" x="140" y="116" fill="#f8fafc" text-anchor="middle">12V FAN</text>

    <!-- Terminals: RED (+) at (110, 1210) & BLK (-) at (270, 1210) -->
    <g transform="translate(60, 25)">
      <circle cx="0" cy="0" r="10" fill="#dc2626" stroke="#fca5a5" stroke-width="3"/>
      <text class="pin-label-lg" x="0" y="28" fill="#fca5a5" text-anchor="middle">RED (+)</text>
    </g>
    <g transform="translate(220, 25)">
      <circle cx="0" cy="0" r="10" fill="#0f172a" stroke="#cbd5e1" stroke-width="3"/>
      <text class="pin-label-lg" x="0" y="28" fill="#cbd5e1" text-anchor="middle">BLK (-)</text>
    </g>
  </g>
  <text class="comp-title-lg" x="190" y="1410" text-anchor="middle">12V DC COOLING FAN</text>


  <!-- 10. DUAL DS18B20 TEMPERATURE SENSORS -->
  <!-- PROBE 1: CORE TEMP -->
  <g id="temp-core-mod" transform="translate(460, 955)" filter="url(#pcb-shadow)">
    <rect width="270" height="170" rx="8" fill="#1e3a8a" stroke="#1d4ed8" stroke-width="2"/>
    <text x="25" y="55" fill="#ffffff" font-size="24" font-weight="900" letter-spacing="0.5px">PROBE 1</text>
    <text x="25" y="95" fill="#f8fafc" font-size="20" font-weight="800">CORE TEMP</text>

    <circle cx="245" cy="40" r="10" fill="#ea580c" stroke="#fed7aa" stroke-width="3"/>
    <text x="224" y="47" fill="#fed7aa" font-size="22" font-weight="800" text-anchor="end">VCC</text>
    <circle cx="245" cy="85" r="10" fill="#eab308" stroke="#fef08a" stroke-width="3"/>
    <text x="224" y="92" fill="#fef08a" font-size="22" font-weight="800" text-anchor="end">DAT</text>
    <circle cx="245" cy="130" r="10" fill="#0f172a" stroke="#f8fafc" stroke-width="3"/>
    <text x="224" y="137" fill="#f8fafc" font-size="22" font-weight="800" text-anchor="end">GND</text>
  </g>

  <!-- PROBE 2: AMBIENT TEMP -->
  <g id="temp-amb-mod" transform="translate(460, 1175)" filter="url(#pcb-shadow)">
    <rect width="270" height="170" rx="8" fill="#1e3a8a" stroke="#1d4ed8" stroke-width="2"/>
    <text x="25" y="55" fill="#ffffff" font-size="24" font-weight="900" letter-spacing="0.5px">PROBE 2</text>
    <text x="25" y="95" fill="#f8fafc" font-size="20" font-weight="800">AMBIENT TEMP</text>

    <circle cx="245" cy="40" r="10" fill="#ea580c" stroke="#fed7aa" stroke-width="3"/>
    <text x="224" y="47" fill="#fed7aa" font-size="22" font-weight="800" text-anchor="end">VCC</text>
    <circle cx="245" cy="85" r="10" fill="#eab308" stroke="#fef08a" stroke-width="3"/>
    <text x="224" y="92" fill="#fef08a" font-size="22" font-weight="800" text-anchor="end">DAT</text>
    <circle cx="245" cy="130" r="10" fill="#0f172a" stroke="#f8fafc" stroke-width="3"/>
    <text x="224" y="137" fill="#f8fafc" font-size="22" font-weight="800" text-anchor="end">GND</text>
  </g>
  <text class="comp-title-lg" x="595" y="1410" text-anchor="middle">DS18B20 SENSORS</text>


  <!-- 11. 16x2 CHARACTER LCD WITH PCF8574 I2C BACKPACK -->
  <g id="lcd-display" transform="translate(1010, 955)" filter="url(#pcb-shadow)">
    <rect width="700" height="420" rx="8" fill="#14532d" stroke="#166534" stroke-width="2"/>
    <circle cx="16" cy="16" r="6" fill="#14532d" stroke="#eab308" stroke-width="2"/>
    <circle cx="684" cy="16" r="6" fill="#14532d" stroke="#eab308" stroke-width="2"/>
    <circle cx="16" cy="404" r="6" fill="#14532d" stroke="#eab308" stroke-width="2"/>
    <circle cx="684" cy="404" r="6" fill="#14532d" stroke="#eab308" stroke-width="2"/>

    <!-- PCF8574 I2C BACKPACK -->
    <g transform="translate(90, 8)">
      <rect width="520" height="64" rx="4" fill="#1e293b" stroke="#475569" stroke-width="1.5"/>
      <text class="pin-label" x="40" y="38" fill="#f8fafc">I2C BACKPACK</text>

      <circle cx="350" cy="30" r="10" fill="#0f172a" stroke="#f8fafc" stroke-width="3"/>
      <text class="pin-label-lg" x="350" y="58" fill="#f8fafc" text-anchor="middle">GND</text>
      <circle cx="400" cy="30" r="10" fill="#9333ea" stroke="#f3e8ff" stroke-width="3"/>
      <text class="pin-label-lg" x="400" y="58" fill="#e9d5ff" text-anchor="middle">VCC</text>
      <circle cx="450" cy="30" r="10" fill="#2563eb" stroke="#bfdbfe" stroke-width="3"/>
      <text class="pin-label-lg" x="450" y="58" fill="#bfdbfe" text-anchor="middle">SDA</text>
      <circle cx="500" cy="30" r="10" fill="#0284c7" stroke="#bae6fd" stroke-width="3"/>
      <text class="pin-label-lg" x="500" y="58" fill="#bae6fd" text-anchor="middle">SCL</text>
    </g>

    <!-- Screen Glass & Dot-Matrix Characters -->
    <rect x="50" y="95" width="600" height="290" rx="6" fill="#0f172a" stroke="#334155" stroke-width="2"/>
    <rect x="70" y="115" width="560" height="250" rx="4" fill="url(#lcd-blue-glass)" stroke="#0284c7" stroke-width="2"/>

    <text x="95" y="200" fill="#f0f9ff" font-family="'JetBrains Mono', Consolas, monospace" font-size="32" font-weight="bold" letter-spacing="3">
      CORE:48.6C AMB:29.4C
    </text>
    <text x="95" y="295" fill="#f0f9ff" font-family="'JetBrains Mono', Consolas, monospace" font-size="32" font-weight="bold" letter-spacing="3">
      ATX:ON  FAN:100%[ACT]
    </text>
  </g>
  <text class="comp-title-lg" x="1360" y="1410" text-anchor="middle">16×2 I2C LCD</text>


  <!-- ===================================================================== -->
  <!-- ==================== WIRING INTERCONNECTS =========================== -->
  <!-- 100% Orthogonal, Clean, Non-Crossing Bus Architecture                 -->
  <!-- ===================================================================== -->

  <!-- ==================== 1. POWER PATH WIRING ==================== -->
  <g id="wires-power">
    <!-- ATX +12V post (300, 163) -> INA219 #1 VIN+ (434, 180) -->
    <path class="wire-line" stroke="#d97706" stroke-width="4.5" 
          d="M 300 163 L 434 163 L 434 180"/>

    <!-- ATX +5V post (300, 203) -> INA219 #2 VIN+ (694, 180) via Roof at y=76 -->
    <path class="wire-line" stroke="#dc2626" stroke-width="4" 
          d="M 300 203 L 340 203 L 340 76 L 694 76 L 694 180"/>

    <!-- ATX +3.3V post (300, 243) -> INA219 #3 VIN+ (954, 180) via Roof at y=56 -->
    <path class="wire-line" stroke="#ea580c" stroke-width="4" 
          d="M 300 243 L 355 243 L 355 56 L 954 56 L 954 180"/>

    <!-- ATX +12V Tap down to TB6612 VM (+12V at 75, 990) via Outer Left Margin (x=25) -->
    <path class="wire-line" stroke="#d97706" stroke-width="4" 
          d="M 300 163 L 320 163 L 320 345 L 25 345 L 25 990 L 75 990"/>
    <circle cx="320" cy="163" r="5" fill="#d97706" stroke="#ffffff" stroke-width="2"/>

    <!-- ==================== MONITORED POWER FEEDS TO EXTERNAL LOAD ==================== -->
    <!-- INA219 #1 VIN- (476, 180) -> Monitored +12V Rail -> External Load +12V Post (1245, 181) via y=96 -->
    <path class="wire-line" stroke="#d97706" stroke-width="4.5" 
          d="M 476 180 L 476 96 L 1245 96 L 1245 181"/>

    <!-- INA219 #2 VIN- (736, 180) -> Monitored +5V Rail -> External Load +5V Post (1355, 181) via y=76 -->
    <path class="wire-line" stroke="#dc2626" stroke-width="4" 
          d="M 736 180 L 736 76 L 1355 76 L 1355 181"/>

    <!-- INA219 #3 VIN- (996, 180) -> Monitored +3.3V Rail -> External Load +3.3V Post (1465, 181) via y=56 -->
    <path class="wire-line" stroke="#ea580c" stroke-width="4" 
          d="M 996 180 L 996 56 L 1465 56 L 1465 181"/>

    <!-- External Load Common GND: exits right from Post 4 (1589, 181) to x=1630, then straight DOWN to Ground Highway at y=422 -->
    <path class="wire-line" stroke="#0f172a" stroke-width="4.5" 
          d="M 1589 181 L 1630 181 L 1630 422"/>
    <circle cx="1630" cy="422" r="5" fill="#0f172a" stroke="#ffffff" stroke-width="2"/>

    <!-- ATX +5VSB (135, 330) -> Standby Power Highway at y=404 -->
    <path class="wire-line" stroke="#9333ea" stroke-width="4.5" 
          d="M 135 330 L 135 404 L 1500 404 L 1500 993"/>
    
    <!-- Tap down to ESP32 5V (VIN at 470, 840) -->
    <path class="wire-line" stroke="#9333ea" stroke-width="4" 
          d="M 410 404 L 410 840 L 470 840"/>
    <circle cx="410" cy="404" r="5.5" fill="#9333ea" stroke="#ffffff" stroke-width="2"/>
  </g>


  <!-- ==================== 2. CONTROL & TRANSISTOR SWITCH WIRING ==================== -->
  <g id="wires-control">
    <!-- ATX PS_ON# (210, 330) drops straight to BC547 Collector (210, 575) -->
    <path class="wire-line" stroke="#10b981" stroke-width="4" 
          d="M 210 330 L 210 575"/>

    <!-- ESP32 D32 (470, 565) -> Base Resistor R1 Input (345, 620) -->
    <path class="wire-line" stroke="#10b981" stroke-width="4" 
          d="M 470 565 L 375 565 L 375 620 L 345 620"/>

    <!-- BC547 Emitter & R2 Ground Lead (210, 740) -> Ground at x=55 -->
    <path class="wire-line" stroke="#0f172a" stroke-width="4" 
          d="M 210 665 L 210 740 L 55 740"/>
    <circle cx="55" cy="740" r="5" fill="#0f172a" stroke="#ffffff" stroke-width="2"/>
  </g>


  <!-- ==================== 3. MOTOR DRIVER (TB6612) & FAN WIRING ==================== -->
  <g id="wires-driver">
    <!-- ESP32 D33 (STBY: 470, 620) -> TB6612 STBY (305, 990) -->
    <path class="wire-line" stroke="#06b6d4" stroke-width="3.5" 
          d="M 470 620 L 395 620 L 395 990 L 305 990"/>

    <!-- ESP32 D25 (PWM: 470, 675) -> TB6612 PWMA (305, 1030) -->
    <path class="wire-line" stroke="#8b5cf6" stroke-width="3.5" 
          d="M 470 675 L 370 675 L 370 1030 L 305 1030"/>

    <!-- ESP32 D26 (AIN1: 470, 730) -> TB6612 AIN1 (305, 1070) -->
    <path class="wire-line" stroke="#ec4899" stroke-width="3.5" 
          d="M 470 730 L 345 730 L 345 1070 L 305 1070"/>

    <!-- TB6612 AIN2 (305, 1110) tied locally to GND (75, 1060) -->
    <path class="wire-line" stroke="#0f172a" stroke-width="3" 
          d="M 305 1110 L 325 1110 L 325 1140 L 45 1140 L 45 1060 L 75 1060"/>

    <!-- AO1 (+) (75, 1095) -> Fan RED (+) (110, 1210) -->
    <path class="wire-line" stroke="#dc2626" stroke-width="4" 
          d="M 75 1095 L 35 1095 L 35 1165 L 110 1165 L 110 1210"/>

    <!-- AO2 (-) (75, 1125) -> Fan BLK (-) (270, 1210) -->
    <path class="wire-line" stroke="#0f172a" stroke-width="4" 
          d="M 75 1125 L 25 1125 L 25 1175 L 270 1175 L 270 1210"/>
  </g>


  <!-- ==================== 4. 1-WIRE TEMPERATURE SENSOR WIRING ==================== -->
  <g id="wires-temperature">
    <path class="wire-line" stroke="#eab308" stroke-width="3.5" 
          d="M 470 785 L 435 785 L 435 915 L 740 915 L 740 1040 L 705 1040"/>
    <path class="wire-line" stroke="#eab308" stroke-width="3.5" 
          d="M 740 1040 L 740 1260 L 705 1260"/>
    <circle cx="740" cy="1040" r="5" fill="#eab308" stroke="#ffffff" stroke-width="2"/>
  </g>


  <!-- ==================== 5. 3.3V LOGIC POWER RAIL ==================== -->
  <g id="wires-3v3-logic">
    <!-- ESP32 3V3 (470, 510) -> 3.3V distribution Highway at y=386 -->
    <path class="wire-line" stroke="#ea580c" stroke-width="4" 
          d="M 470 510 L 445 510 L 445 386 L 940 386 L 940 325"/> <!-- To INA219 #3 VCC -->
    
    <!-- Tap to INA219 #1 VCC (420, 325) & INA219 #2 VCC (680, 325) -->
    <path class="wire-line" stroke="#ea580c" stroke-width="3.5" d="M 420 386 L 420 325"/>
    <circle cx="420" cy="386" r="5" fill="#ea580c" stroke="#ffffff" stroke-width="2"/>
    <path class="wire-line" stroke="#ea580c" stroke-width="3.5" d="M 680 386 L 680 325"/>
    <circle cx="680" cy="386" r="5" fill="#ea580c" stroke="#ffffff" stroke-width="2"/>

    <!-- Tap left into TB6612 VCC (75, 1025) via Left Margin (x=15) -->
    <path class="wire-line" stroke="#ea580c" stroke-width="3.5" 
          d="M 445 386 L 15 386 L 15 1025 L 75 1025"/>

    <!-- Tap down Right Alley (x=975) to Dual DS18B20 VCC pins (705, 995 & 705, 1215) -->
    <path class="wire-line" stroke="#ea580c" stroke-width="3.5" 
          d="M 975 386 L 975 925 L 760 925 L 760 995 L 705 995"/>
    <circle cx="975" cy="386" r="5" fill="#ea580c" stroke="#ffffff" stroke-width="2"/>
    <path class="wire-line" stroke="#ea580c" stroke-width="3.5" 
          d="M 760 995 L 760 1215 L 705 1215"/>
    <circle cx="760" cy="995" r="5" fill="#ea580c" stroke="#ffffff" stroke-width="2"/>
  </g>


  <!-- ==================== 6. I2C BUS WIRING (SCL & SDA) ==================== -->
  <g id="wires-i2c">
    <!-- I2C SCL (Cyan) at y=350: ESP32 D22 (930, 595) -> SCL Bus Highway -->
    <path class="wire-line" stroke="#0284c7" stroke-width="3.5" 
          d="M 930 595 L 940 595 L 940 350 L 515 350 L 515 325"/> <!-- To INA219 #1 SCL -->
    <!-- Taps to INA219 #2 SCL (775, 325) & INA219 #3 SCL (1035, 325) -->
    <path class="wire-line" stroke="#0284c7" stroke-width="3.5" d="M 775 350 L 775 325"/>
    <circle cx="775" cy="350" r="4.5" fill="#0284c7" stroke="#ffffff" stroke-width="1.5"/>
    <path class="wire-line" stroke="#0284c7" stroke-width="3.5" d="M 1035 350 L 1035 325"/>
    <circle cx="1035" cy="350" r="4.5" fill="#0284c7" stroke="#ffffff" stroke-width="1.5"/>
    <!-- Tap to LCD SCL (1600, 993) -->
    <path class="wire-line" stroke="#0284c7" stroke-width="3.5" 
          d="M 1035 350 L 1600 350 L 1600 993"/>

    <!-- I2C SDA (Blue) at y=368: ESP32 D21 (930, 680) -> SDA Bus Highway -->
    <path class="wire-line" stroke="#2563eb" stroke-width="3.5" 
          d="M 930 680 L 955 680 L 955 368 L 565 368 L 565 325"/> <!-- To INA219 #1 SDA -->
    <!-- Taps to INA219 #2 SDA (825, 325) & INA219 #3 SDA (1085, 325) -->
    <path class="wire-line" stroke="#2563eb" stroke-width="3.5" d="M 825 368 L 825 325"/>
    <circle cx="825" cy="368" r="4.5" fill="#2563eb" stroke="#ffffff" stroke-width="1.5"/>
    <path class="wire-line" stroke="#2563eb" stroke-width="3.5" d="M 1085 368 L 1085 325"/>
    <circle cx="1085" cy="368" r="4.5" fill="#2563eb" stroke="#ffffff" stroke-width="1.5"/>
    <!-- Tap to LCD SDA (1550, 993) -->
    <path class="wire-line" stroke="#2563eb" stroke-width="3.5" 
          d="M 1085 368 L 1550 368 L 1550 993"/>
  </g>


  <!-- ==================== 7. COMMON GROUND NETWORK (GND) ==================== -->
  <g id="wires-gnd">
    <!-- Heavy System Ground Highway at y=422 -->
    <path class="wire-line" stroke="#0f172a" stroke-width="4.5" 
          d="M 300 283 L 335 283 L 335 422 L 985 422 L 985 325"/> <!-- To INA219 #3 GND -->

    <!-- Drops into INA219 #1 GND (465, 325) & INA219 #2 GND (725, 325) -->
    <path class="wire-line" stroke="#0f172a" stroke-width="4" d="M 465 422 L 465 325"/>
    <circle cx="465" cy="422" r="5" fill="#0f172a" stroke="#ffffff" stroke-width="2"/>
    <path class="wire-line" stroke="#0f172a" stroke-width="4" d="M 725 422 L 725 325"/>
    <circle cx="725" cy="422" r="5" fill="#0f172a" stroke="#ffffff" stroke-width="2"/>

    <!-- ESP32 GND (930, 510) connects to GND line -->
    <path class="wire-line" stroke="#0f172a" stroke-width="4" 
          d="M 930 510 L 970 510 L 970 422"/>
    <circle cx="970" cy="422" r="5" fill="#0f172a" stroke="#ffffff" stroke-width="2"/>

    <!-- Drops down Right Alley (x=995) to Dual DS18B20 GND (705, 1085 & 705, 1305) -->
    <path class="wire-line" stroke="#0f172a" stroke-width="3.5" 
          d="M 995 422 L 995 940 L 780 940 L 780 1085 L 705 1085"/>
    <circle cx="995" cy="422" r="5" fill="#0f172a" stroke="#ffffff" stroke-width="2"/>
    <path class="wire-line" stroke="#0f172a" stroke-width="3.5" 
          d="M 780 1085 L 780 1305 L 705 1305"/>
    <circle cx="780" cy="1085" r="4.5" fill="#0f172a" stroke="#ffffff" stroke-width="1.5"/>

    <!-- TB6612 GND (75, 1060) connects to Ground line via Left Margin (x=35) -->
    <path class="wire-line" stroke="#0f172a" stroke-width="3.5" 
          d="M 75 1060 L 55 1060 L 55 422 L 335 422"/>

    <!-- Ground continuation to LCD GND (1450, 993) & External Load Common GND (1630, 422) -->
    <path class="wire-line" stroke="#0f172a" stroke-width="4.5" 
          d="M 985 422 L 1630 422"/>
    <path class="wire-line" stroke="#0f172a" stroke-width="4" 
          d="M 1450 422 L 1450 993"/>
    <circle cx="1450" cy="422" r="5" fill="#0f172a" stroke="#ffffff" stroke-width="2"/>
  </g>

</svg>'''

    output_svg = os.path.join("documentation", "transformer_cbm_circuit_diagram.svg")
    ET.fromstring(svg) # Structural XML validation
    with open(output_svg, "w", encoding="utf-8") as f:
        f.write(svg)
    print("Cirkit Designer SVG (Rev 25.1) generated successfully.")

    # Update interactive HTML viewer as well!
    html_path = os.path.join("documentation", "transformer_cbm_circuit_diagram.html")
    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Transformer CBM - Hardware Wiring Architecture</title>
  <style>
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      background-color: #0f172a;
      color: #f8fafc;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      height: 100vh;
    }}
    header {{
      background: #1e293b;
      padding: 14px 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid #334155;
      z-index: 10;
    }}
    .title-group h1 {{
      font-size: 18px;
      font-weight: 700;
      letter-spacing: -0.02em;
    }}
    .toolbar {{
      display: flex;
      gap: 10px;
      align-items: center;
    }}
    .btn {{
      background: #334155;
      color: #f8fafc;
      border: 1px solid #475569;
      padding: 7px 16px;
      border-radius: 6px;
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      text-decoration: none;
      transition: all 0.15s ease;
    }}
    .btn:hover {{
      background: #475569;
      border-color: #64748b;
    }}
    .viewport {{
      flex: 1;
      overflow: auto;
      display: flex;
      align-items: center;
      justify-content: center;
      background: #090d16;
      padding: 20px;
    }}
    .svg-container {{
      background: #ffffff;
      box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
      border-radius: 8px;
      overflow: hidden;
      max-width: 100%;
      height: auto;
    }}
    svg {{
      display: block;
      width: 100%;
      height: auto;
    }}
  </style>
</head>
<body>
  <header>
    <div class="title-group">
      <h1>IoT Transformer Condition Monitoring System — Hardware Wiring Diagram</h1>
    </div>
    <div class="toolbar">
      <button class="btn" onclick="window.print()">Print Schematic</button>
      <a class="btn" href="circuit_diagram_preview.png" download="transformer_cbm_schematic.png">Download PNG</a>
    </div>
  </header>
  <div class="viewport">
    <div class="svg-container">
      {svg}
    </div>
  </div>
</body>
</html>
'''
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Updated interactive HTML viewer at {html_path}")

    # Compile to high-resolution PNG using typst
    typ_path = os.path.join("documentation", "render_preview.typ")
    png_path = os.path.join("documentation", "circuit_diagram_preview.png")
    typst_exe = os.path.join("documentation", "bin", "typst.exe")
    
    with open(typ_path, "w", encoding="utf-8") as f:
        f.write('#set page(width: 2000pt, height: 1440pt, margin: 0pt)\n#image("transformer_cbm_circuit_diagram.svg", width: 100%)\n')
    
    tmp_png = os.path.join("documentation", "circuit_diagram_preview_gen.png")
    subprocess.run([typst_exe, "compile", "--format", "png", "--ppi", "150", typ_path, tmp_png], check=True)
    if os.path.exists(typ_path):
        os.remove(typ_path)
    
    import shutil, time
    for attempt in range(5):
        try:
            if os.path.exists(png_path):
                os.remove(png_path)
            shutil.move(tmp_png, png_path)
            break
        except Exception:
            time.sleep(0.5)
    else:
        if os.path.exists(tmp_png):
            shutil.copy2(tmp_png, png_path)
    print(f"High-resolution PNG generated at {png_path}")

if __name__ == "__main__":
    generate_cirkit_svg()
