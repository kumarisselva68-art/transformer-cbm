# -*- coding: utf-8 -*-
"""
High-Legibility Professional Vector SVG Schematic Generator:
documentation/transformer_cbm_circuit_diagram.svg
Enlarged fonts, high-contrast badge callouts, and spacious pin layouts.
"""

import os
import xml.etree.ElementTree as ET

def build_svg():
    svg_content = r'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2400 1600" width="2400" height="1600">
  <defs>
    <!-- Background Blueprint Grid Pattern -->
    <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
      <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#e2e8f0" stroke-width="0.75"/>
    </pattern>
    <pattern id="major-grid" width="100" height="100" patternUnits="userSpaceOnUse">
      <rect width="100" height="100" fill="url(#grid)"/>
      <path d="M 100 0 L 0 0 0 100" fill="none" stroke="#cbd5e1" stroke-width="1.2"/>
    </pattern>

    <!-- Component Drop Shadow -->
    <filter id="shadow" x="-5%" y="-5%" width="112%" height="118%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="4" dy="6" stdDeviation="6" flood-color="#0f172a" flood-opacity="0.25"/>
    </filter>

    <!-- Badge Drop Shadow for Wire Callouts -->
    <filter id="badge-shadow" x="-10%" y="-15%" width="120%" height="130%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="1" dy="2" stdDeviation="2" flood-color="#0f172a" flood-opacity="0.2"/>
    </filter>

    <!-- Metallic Gradient for ESP32 Can and Probes -->
    <linearGradient id="metal-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffffff" />
      <stop offset="35%" stop-color="#e2e8f0" />
      <stop offset="70%" stop-color="#94a3b8" />
      <stop offset="100%" stop-color="#64748b" />
    </linearGradient>

    <!-- Gold Plating Gradient -->
    <linearGradient id="gold-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#fef08a" />
      <stop offset="50%" stop-color="#eab308" />
      <stop offset="100%" stop-color="#ca8a04" />
    </linearGradient>

    <!-- Glass Fuse Tube Gradient -->
    <linearGradient id="glass-grad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.9"/>
      <stop offset="40%" stop-color="#e2e8f0" stop-opacity="0.3"/>
      <stop offset="70%" stop-color="#cbd5e1" stop-opacity="0.2"/>
      <stop offset="100%" stop-color="#64748b" stop-opacity="0.7"/>
    </linearGradient>

    <!-- LCD Matrix Display Gradient -->
    <linearGradient id="lcd-grad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#0284c7"/>
      <stop offset="100%" stop-color="#0369a1"/>
    </linearGradient>
  </defs>

  <style>
    .title-large { font-family: 'Segoe UI', Arial, sans-serif; font-size: 19px; font-weight: bold; }
    .subtitle { font-family: 'Segoe UI', Arial, sans-serif; font-size: 13px; font-weight: 600; }
    .pin-label { font-family: 'SF Mono', Consolas, 'Courier New', monospace; font-size: 13px; font-weight: bold; }
    .pin-label-lg { font-family: 'SF Mono', Consolas, 'Courier New', monospace; font-size: 15px; font-weight: bold; }
    .badge-text { font-family: 'Segoe UI', Arial, sans-serif; font-size: 13px; font-weight: bold; }
    .wire { fill: none; stroke-linecap: round; stroke-linejoin: round; }
    .wire-glow:hover { stroke-width: 7 !important; cursor: pointer; filter: drop-shadow(0 0 6px rgba(255,255,255,0.95)); }
    .bus-junction { stroke: #ffffff; stroke-width: 2; }
  </style>

  <!-- ===================================================================== -->
  <!-- DRAWING BORDER AND BACKGROUND                                         -->
  <!-- ===================================================================== -->
  <rect width="2400" height="1600" fill="#f8fafc"/>
  <rect x="25" y="25" width="2350" height="1550" fill="url(#major-grid)" stroke="#0f172a" stroke-width="3"/>
  <rect x="38" y="38" width="2324" height="1524" fill="none" stroke="#475569" stroke-width="1.5"/>

  <!-- Border Engineering Coordinate Zones -->
  <g fill="#475569" font-family="'Segoe UI', sans-serif" font-size="15" font-weight="bold" text-anchor="middle">
    <text x="250" y="22">1</text><text x="600" y="22">2</text><text x="950" y="22">3</text>
    <text x="1300" y="22">4</text><text x="1650" y="22">5</text><text x="2000" y="22">6</text>
    <text x="250" y="1590">1</text><text x="600" y="1590">2</text><text x="950" y="1590">3</text>
    <text x="1300" y="1590">4</text><text x="1650" y="1590">5</text><text x="2000" y="1590">6</text>
    <text x="18" y="250">A</text><text x="18" y="550">B</text><text x="18" y="850">C</text>
    <text x="18" y="1150">D</text><text x="18" y="1450">E</text>
    <text x="2382" y="250">A</text><text x="2382" y="550">B</text><text x="2382" y="850">C</text>
    <text x="2382" y="1150">D</text><text x="2382" y="1450">E</text>
  </g>


  <!-- ===================================================================== -->
  <!-- 1. ATX BENCH BREAKOUT BOARD (XH=M229)                                 -->
  <!-- ===================================================================== -->
  <g id="comp-atx" transform="translate(70, 70)" filter="url(#shadow)">
    <!-- Board FR4 Body -->
    <rect width="440" height="320" rx="12" fill="#14532d" stroke="#166534" stroke-width="2.5"/>
    <!-- Gold Mount Holes -->
    <circle cx="20" cy="20" r="9" fill="#14532d" stroke="url(#gold-grad)" stroke-width="3"/>
    <circle cx="420" cy="20" r="9" fill="#14532d" stroke="url(#gold-grad)" stroke-width="3"/>
    <circle cx="20" cy="300" r="9" fill="#14532d" stroke="url(#gold-grad)" stroke-width="3"/>
    <circle cx="420" cy="300" r="9" fill="#14532d" stroke="url(#gold-grad)" stroke-width="3"/>

    <!-- Silkscreen Titles -->
    <text class="title-large" x="220" y="34" fill="#f0fdf4" text-anchor="middle">ATX BENCH BREAKOUT (XH-M229)</text>
    <text class="subtitle" x="220" y="54" fill="#86efac" text-anchor="middle">Inbuilt Cartridge Protection Fuses &amp; Bench Power Rails</text>

    <!-- 24=Pin ATX Socket -->
    <rect x="25" y="75" width="115" height="215" rx="5" fill="#f8fafc" stroke="#94a3b8" stroke-width="2"/>
    <text x="82" y="185" fill="#475569" font-size="13" font-weight="bold" text-anchor="middle" transform="rotate(-90 82 185)" font-family="'Segoe UI', sans-serif">24-PIN ATX INFEED</text>
    <!-- Socket pins -->
    <g fill="#1e293b">
      <rect x="35" y="85" width="12" height="12" rx="1"/><rect x="52" y="85" width="12" height="12" rx="1"/>
      <rect x="69" y="85" width="12" height="12" rx="1"/><rect x="86" y="85" width="12" height="12" rx="1"/>
      <rect x="103" y="85" width="12" height="12" rx="1"/><rect x="120" y="85" width="12" height="12" rx="1"/>
      <rect x="35" y="115" width="12" height="12" rx="1"/><rect x="120" y="115" width="12" height="12" rx="1"/>
      <rect x="35" y="145" width="12" height="12" rx="1"/><rect x="120" y="145" width="12" height="12" rx="1"/>
      <rect x="35" y="175" width="12" height="12" rx="1"/><rect x="120" y="175" width="12" height="12" rx="1"/>
      <rect x="35" y="205" width="12" height="12" rx="1"/><rect x="120" y="205" width="12" height="12" rx="1"/>
      <rect x="35" y="235" width="12" height="12" rx="1"/><rect x="120" y="235" width="12" height="12" rx="1"/>
      <rect x="35" y="265" width="12" height="12" rx="1"/><rect x="120" y="265" width="12" height="12" rx="1"/>
    </g>

    <!-- 4 Cartridge Fuses -->
    <g transform="translate(170, 80)">
      <rect x="0" y="0" width="55" height="20" rx="3" fill="url(#glass-grad)" stroke="#475569" stroke-width="1.2"/>
      <rect x="0" y="0" width="10" height="20" fill="url(#metal-grad)"/><rect x="45" y="0" width="10" height="20" fill="url(#metal-grad)"/>
      <line x1="10" y1="10" x2="45" y2="10" stroke="#ca8a04" stroke-width="1.5"/>
      <text x="27" y="15" fill="#0f172a" font-size="10" font-weight="bold" text-anchor="middle">F1:12V</text>

      <rect x="0" y="38" width="55" height="20" rx="3" fill="url(#glass-grad)" stroke="#475569" stroke-width="1.2"/>
      <rect x="0" y="38" width="10" height="20" fill="url(#metal-grad)"/><rect x="45" y="38" width="10" height="20" fill="url(#metal-grad)"/>
      <line x1="10" y1="48" x2="45" y2="48" stroke="#ca8a04" stroke-width="1.5"/>
      <text x="27" y="53" fill="#0f172a" font-size="10" font-weight="bold" text-anchor="middle">F2:-12V</text>

      <rect x="0" y="76" width="55" height="20" rx="3" fill="url(#glass-grad)" stroke="#475569" stroke-width="1.2"/>
      <rect x="0" y="76" width="10" height="20" fill="url(#metal-grad)"/><rect x="45" y="76" width="10" height="20" fill="url(#metal-grad)"/>
      <line x1="10" y1="86" x2="45" y2="86" stroke="#ca8a04" stroke-width="1.5"/>
      <text x="27" y="91" fill="#0f172a" font-size="10" font-weight="bold" text-anchor="middle">F3:5V</text>

      <rect x="0" y="114" width="55" height="20" rx="3" fill="url(#glass-grad)" stroke="#475569" stroke-width="1.2"/>
      <rect x="0" y="114" width="10" height="20" fill="url(#metal-grad)"/><rect x="45" y="114" width="10" height="20" fill="url(#metal-grad)"/>
      <line x1="10" y1="124" x2="45" y2="124" stroke="#ca8a04" stroke-width="1.5"/>
      <text x="27" y="129" fill="#0f172a" font-size="10" font-weight="bold" text-anchor="middle">F4:3.3V</text>
    </g>

    <!-- Screw Terminal Binding Posts -->
    <!-- +12V Terminal -->
    <circle cx="360" cy="85" r="18" fill="#ca8a04" stroke="#fef08a" stroke-width="3.5"/>
    <circle cx="360" cy="85" r="7" fill="#713f12"/>
    <text class="pin-label-lg" x="305" y="91" fill="#fef08a">+12V</text>

    <!-- =12V Terminal -->
    <circle cx="360" cy="135" r="18" fill="#1d4ed8" stroke="#bfdbfe" stroke-width="3.5"/>
    <circle cx="360" cy="135" r="7" fill="#1e3a8a"/>
    <text class="pin-label-lg" x="305" y="141" fill="#bfdbfe">-12V</text>

    <!-- +5V Terminal -->
    <circle cx="360" cy="185" r="18" fill="#dc2626" stroke="#fca5a5" stroke-width="3.5"/>
    <circle cx="360" cy="185" r="7" fill="#7f1d1d"/>
    <text class="pin-label-lg" x="315" y="191" fill="#fca5a5">+5V</text>

    <!-- +3.3V Terminal -->
    <circle cx="360" cy="235" r="18" fill="#ea580c" stroke="#fed7aa" stroke-width="3.5"/>
    <circle cx="360" cy="235" r="7" fill="#7c2d12"/>
    <text class="pin-label-lg" x="300" y="241" fill="#fed7aa">+3.3V</text>

    <!-- COM / GND Terminal -->
    <circle cx="360" cy="285" r="18" fill="#0f172a" stroke="#f8fafc" stroke-width="3.5"/>
    <circle cx="360" cy="285" r="7" fill="#334155"/>
    <text class="pin-label-lg" x="305" y="291" fill="#f8fafc">GND</text>

    <!-- Auxiliary Header: +5VSB & PS_ON# -->
    <rect x="160" y="240" width="110" height="50" rx="4" fill="#0f172a" stroke="#475569" stroke-width="2"/>
    
    <circle cx="185" cy="265" r="8" fill="#a855f7" stroke="#e9d5ff" stroke-width="2.5"/>
    <text class="pin-label-lg" x="185" y="306" fill="#e9d5ff" text-anchor="middle">+5VSB</text>

    <circle cx="245" cy="265" r="8" fill="#10b981" stroke="#a7f3d0" stroke-width="2.5"/>
    <text class="pin-label-lg" x="245" y="306" fill="#a7f3d0" text-anchor="middle">PS_ON#</text>
  </g>


  <!-- ===================================================================== -->
  <!-- 2. CENTRAL CONTROLLER: ESP32=WROOM=32 DEVKITC (30=PIN)                -->
  <!-- ===================================================================== -->
  <g id="comp-esp32" transform="translate(800, 260)" filter="url(#shadow)">
    <!-- Main PCB Body -->
    <rect width="360" height="650" rx="12" fill="#18181b" stroke="#3f3f46" stroke-width="3"/>
    
    <circle cx="20" cy="20" r="7" fill="#18181b" stroke="url(#gold-grad)" stroke-width="2"/>
    <circle cx="340" cy="20" r="7" fill="#18181b" stroke="url(#gold-grad)" stroke-width="2"/>
    <circle cx="20" cy="630" r="7" fill="#18181b" stroke="url(#gold-grad)" stroke-width="2"/>
    <circle cx="340" cy="630" r="7" fill="#18181b" stroke="url(#gold-grad)" stroke-width="2"/>

    <!-- RF Shield Can -->
    <rect x="80" y="55" width="200" height="175" rx="6" fill="url(#metal-grad)" stroke="#475569" stroke-width="2"/>
    <path d="M 110 70 L 125 70 L 125 90 L 140 90 L 140 70 L 155 70 L 155 90 L 170 90 L 170 70 L 185 70 L 185 90 L 200 90 L 200 70 L 245 70" 
          fill="none" stroke="url(#gold-grad)" stroke-width="4.5" stroke-linecap="round"/>
    
    <text x="180" y="135" fill="#0f172a" font-size="18" font-weight="bold" text-anchor="middle" font-family="'Segoe UI', sans-serif">ESPRESSIF</text>
    <text x="180" y="160" fill="#1e293b" font-size="14" font-weight="bold" text-anchor="middle" font-family="'Segoe UI', sans-serif">ESP-WROOM-32</text>
    <text x="180" y="182" fill="#334155" font-size="11" text-anchor="middle">FCC ID: 2AC7Z-ESPWROOM32</text>
    <text x="180" y="200" fill="#475569" font-size="10" text-anchor="middle">2.4 GHz Dual-Core Wi-Fi + BLE</text>

    <!-- CP2102 IC -->
    <rect x="150" y="300" width="60" height="60" rx="3" fill="#27272a" stroke="#52525b" stroke-width="1.5"/>
    <circle cx="160" cy="310" r="3" fill="#71717a"/>
    <text x="180" y="335" fill="#e4e4e7" font-size="11" font-weight="bold" text-anchor="middle">CP2102</text>

    <!-- LDO Regulator -->
    <rect x="145" y="420" width="70" height="40" rx="2" fill="#27272a" stroke="#52525b" stroke-width="1.5"/>
    <rect x="160" y="412" width="40" height="10" fill="url(#metal-grad)"/>
    <text x="180" y="445" fill="#e4e4e7" font-size="10" font-weight="bold" text-anchor="middle">AMS1117</text>

    <!-- Pushbuttons -->
    <rect x="65" y="580" width="30" height="30" rx="3" fill="#3f3f46" stroke="#71717a"/>
    <circle cx="80" cy="595" r="8" fill="#d4d4d8"/>
    <text x="80" y="626" fill="#a1a1aa" font-size="11" font-weight="bold" text-anchor="middle">EN</text>

    <rect x="265" y="580" width="30" height="30" rx="3" fill="#3f3f46" stroke="#71717a"/>
    <circle cx="280" cy="595" r="8" fill="#d4d4d8"/>
    <text x="280" y="626" fill="#a1a1aa" font-size="11" font-weight="bold" text-anchor="middle">BOOT</text>

    <!-- USB Socket -->
    <rect x="145" y="615" width="70" height="35" rx="4" fill="url(#metal-grad)" stroke="#475569" stroke-width="2"/>

    <!-- ================= ESP32 LEFT HEADER (15 PINS) ================= -->
    <g id="esp-left-pins">
      <!-- 3V3 (y = 90) -->
      <circle cx="22" cy="90" r="8" fill="#ea580c" stroke="#fed7aa" stroke-width="2.5"/>
      <text class="pin-label-lg" x="38" y="95" fill="#fed7aa">3V3 [LOGIC OUT]</text>

      <circle cx="22" cy="126" r="6" fill="#27272a" stroke="#71717a"/><text class="pin-label" x="38" y="130" fill="#a1a1aa">EN</text>
      <circle cx="22" cy="162" r="6" fill="#27272a" stroke="#71717a"/><text class="pin-label" x="38" y="166" fill="#a1a1aa">VP (GPIO36)</text>
      <circle cx="22" cy="198" r="6" fill="#27272a" stroke="#71717a"/><text class="pin-label" x="38" y="202" fill="#a1a1aa">VN (GPIO39)</text>
      <circle cx="22" cy="234" r="6" fill="#27272a" stroke="#71717a"/><text class="pin-label" x="38" y="238" fill="#a1a1aa">D34</text>
      <circle cx="22" cy="270" r="6" fill="#27272a" stroke="#71717a"/><text class="pin-label" x="38" y="274" fill="#a1a1aa">D35</text>

      <!-- GPIO 32 (y = 306) => PS_ON# Control -->
      <circle cx="22" cy="306" r="8" fill="#10b981" stroke="#a7f3d0" stroke-width="2.5"/>
      <text class="pin-label-lg" x="38" y="311" fill="#a7f3d0">D32 [PS_ON# TRIP]</text>

      <!-- GPIO 33 (y = 342) => TB6612 STBY -->
      <circle cx="22" cy="342" r="8" fill="#38bdf8" stroke="#bae6fd" stroke-width="2.5"/>
      <text class="pin-label-lg" x="38" y="347" fill="#bae6fd">D33 [TB6612 STBY]</text>

      <!-- GPIO 25 (y = 378) => TB6612 PWMA -->
      <circle cx="22" cy="378" r="8" fill="#a855f7" stroke="#e9d5ff" stroke-width="2.5"/>
      <text class="pin-label-lg" x="38" y="383" fill="#e9d5ff">D25 [PWM SPEED]</text>

      <!-- GPIO 26 (y = 414) => TB6612 AIN1 -->
      <circle cx="22" cy="414" r="8" fill="#ec4899" stroke="#fbcfe8" stroke-width="2.5"/>
      <text class="pin-label-lg" x="38" y="419" fill="#fbcfe8">D26 [FAN DIR]</text>

      <!-- GPIO 27 (y = 450) => DS18B20 1=Wire DQ -->
      <circle cx="22" cy="450" r="8" fill="#eab308" stroke="#fef08a" stroke-width="2.5"/>
      <text class="pin-label-lg" x="38" y="455" fill="#fef08a">D27 [1-WIRE DQ]</text>

      <circle cx="22" cy="486" r="6" fill="#27272a" stroke="#71717a"/><text class="pin-label" x="38" y="490" fill="#a1a1aa">D14</text>
      <circle cx="22" cy="522" r="6" fill="#27272a" stroke="#71717a"/><text class="pin-label" x="38" y="526" fill="#a1a1aa">D12</text>

      <!-- GND Left (y = 558) -->
      <circle cx="22" cy="558" r="8" fill="#0f172a" stroke="#f8fafc" stroke-width="2.5"/>
      <text class="pin-label-lg" x="38" y="563" fill="#f8fafc">GND [COM]</text>

      <circle cx="22" cy="594" r="6" fill="#27272a" stroke="#71717a"/><text class="pin-label" x="38" y="598" fill="#a1a1aa">D13</text>
    </g>

    <!-- ================= ESP32 RIGHT HEADER (15 PINS) ================= -->
    <g id="esp-right-pins">
      <!-- GPIO 23 (y = 90) => SW2 Setup AP -->
      <circle cx="338" cy="90" r="8" fill="#f43f5e" stroke="#fecdd3" stroke-width="2.5"/>
      <text class="pin-label-lg" x="200" y="95" fill="#fecdd3">D23 [SW2 SETUP]</text>

      <!-- GPIO 22 (y = 126) => I2C SCL -->
      <circle cx="338" cy="126" r="8" fill="#2563eb" stroke="#93c5fd" stroke-width="2.5"/>
      <text class="pin-label-lg" x="220" y="131" fill="#93c5fd">D22 [I2C SCL]</text>

      <circle cx="338" cy="162" r="6" fill="#27272a" stroke="#71717a"/><text class="pin-label" x="290" y="166" fill="#a1a1aa">TX0</text>
      <circle cx="338" cy="198" r="6" fill="#27272a" stroke="#71717a"/><text class="pin-label" x="290" y="202" fill="#a1a1aa">RX0</text>

      <!-- GPIO 21 (y = 234) => I2C SDA -->
      <circle cx="338" cy="234" r="8" fill="#16a34a" stroke="#86efac" stroke-width="2.5"/>
      <text class="pin-label-lg" x="220" y="239" fill="#86efac">D21 [I2C SDA]</text>

      <circle cx="338" cy="270" r="6" fill="#27272a" stroke="#71717a"/><text class="pin-label" x="295" y="274" fill="#a1a1aa">D19</text>

      <!-- GPIO 18 (y = 306) => SW1 Main Enable -->
      <circle cx="338" cy="306" r="8" fill="#d946ef" stroke="#f5d0fe" stroke-width="2.5"/>
      <text class="pin-label-lg" x="200" y="311" fill="#f5d0fe">D18 [SW1 MAIN]</text>

      <circle cx="338" cy="342" r="6" fill="#27272a" stroke="#71717a"/><text class="pin-label" x="300" y="346" fill="#a1a1aa">D5</text>
      <circle cx="338" cy="378" r="6" fill="#27272a" stroke="#71717a"/><text class="pin-label" x="295" y="382" fill="#a1a1aa">D17</text>
      <circle cx="338" cy="414" r="6" fill="#27272a" stroke="#71717a"/><text class="pin-label" x="295" y="418" fill="#a1a1aa">D16</text>
      <circle cx="338" cy="450" r="6" fill="#27272a" stroke="#71717a"/><text class="pin-label" x="300" y="454" fill="#a1a1aa">D4</text>
      <circle cx="338" cy="486" r="6" fill="#27272a" stroke="#71717a"/><text class="pin-label" x="300" y="490" fill="#a1a1aa">D0</text>
      <circle cx="338" cy="522" r="6" fill="#27272a" stroke="#71717a"/><text class="pin-label" x="300" y="526" fill="#a1a1aa">D2</text>
      <circle cx="338" cy="558" r="6" fill="#27272a" stroke="#71717a"/><text class="pin-label" x="295" y="562" fill="#a1a1aa">D15</text>

      <!-- 5V / VIN (y = 594) => +5VSB Infeed -->
      <circle cx="338" cy="594" r="8" fill="#dc2626" stroke="#fca5a5" stroke-width="2.5"/>
      <text class="pin-label-lg" x="210" y="599" fill="#fca5a5">5V [VIN INFEED]</text>
    </g>
  </g>


  <!-- ===================================================================== -->
  <!-- 3. THREE INA219 DC POWER MONITORS (PURPLE BOARDS)                     -->
  <!-- ===================================================================== -->
  <!-- INA219 #1: 12V LOAD RAIL (Address 0x40) -->
  <g id="comp-ina1" transform="translate(1620, 70)" filter="url(#shadow)">
    <rect width="320" height="200" rx="10" fill="#581c87" stroke="#7e22ce" stroke-width="2.5"/>
    <text class="title-large" x="160" y="28" fill="#f3e8ff" text-anchor="middle">INA219 #1 (ADDR: 0x40)</text>
    <text class="subtitle" x="160" y="46" fill="#d8b4fe" text-anchor="middle">12V Monitored Load Rail (A0=Open, A1=Open)</text>
    
    <!-- Shunt Resistor R100 -->
    <rect x="135" y="65" width="50" height="26" rx="2" fill="#0f172a" stroke="#94a3b8" stroke-width="1.5"/>
    <text x="160" y="82" fill="#38bdf8" font-size="12" font-weight="bold" text-anchor="middle">R100</text>

    <!-- INA219 IC -->
    <rect x="140" y="100" width="40" height="28" rx="2" fill="#18181b" stroke="#52525b"/>
    <text x="160" y="118" fill="#a1a1aa" font-size="9" font-weight="bold" text-anchor="middle">INA219</text>

    <!-- 2=Pin Screw Terminal Block -->
    <rect x="25" y="65" width="75" height="50" rx="4" fill="#15803d" stroke="#166534" stroke-width="2"/>
    <circle cx="45" cy="90" r="10" fill="#ca8a04" stroke="#fef08a" stroke-width="2.5"/>
    <text class="pin-label-lg" x="45" y="112" fill="#fef08a" text-anchor="middle">VIN+</text>
    <circle cx="78" cy="90" r="10" fill="#ca8a04" stroke="#fef08a" stroke-width="2.5"/>
    <text class="pin-label-lg" x="78" y="112" fill="#fef08a" text-anchor="middle">VIN-</text>

    <!-- Logic Pins: VCC, GND, SCL, SDA -->
    <g transform="translate(25, 145)">
      <circle cx="20" cy="20" r="8" fill="#ea580c" stroke="#fed7aa" stroke-width="2"/>
      <text class="pin-label-lg" x="20" y="42" fill="#fed7aa" text-anchor="middle">VCC</text>

      <circle cx="70" cy="20" r="8" fill="#0f172a" stroke="#f8fafc" stroke-width="2"/>
      <text class="pin-label-lg" x="70" y="42" fill="#f8fafc" text-anchor="middle">GND</text>

      <circle cx="120" cy="20" r="8" fill="#2563eb" stroke="#93c5fd" stroke-width="2"/>
      <text class="pin-label-lg" x="120" y="42" fill="#93c5fd" text-anchor="middle">SCL</text>

      <circle cx="170" cy="20" r="8" fill="#16a34a" stroke="#86efac" stroke-width="2"/>
      <text class="pin-label-lg" x="170" y="42" fill="#86efac" text-anchor="middle">SDA</text>
    </g>
  </g>

  <!-- INA219 #2: 5V NATIVE RAIL (Address 0x41) -->
  <g id="comp-ina2" transform="translate(2000, 70)" filter="url(#shadow)">
    <rect width="320" height="200" rx="10" fill="#581c87" stroke="#7e22ce" stroke-width="2.5"/>
    <text class="title-large" x="160" y="28" fill="#f3e8ff" text-anchor="middle">INA219 #2 (ADDR: 0x41)</text>
    <text class="subtitle" x="160" y="46" fill="#d8b4fe" text-anchor="middle">Native 5V Bus Monitor (A0=VCC)</text>
    
    <rect x="135" y="65" width="50" height="26" rx="2" fill="#0f172a" stroke="#94a3b8" stroke-width="1.5"/>
    <text x="160" y="82" fill="#38bdf8" font-size="12" font-weight="bold" text-anchor="middle">R100</text>
    <rect x="140" y="100" width="40" height="28" rx="2" fill="#18181b" stroke="#52525b"/>
    <text x="160" y="118" fill="#a1a1aa" font-size="9" font-weight="bold" text-anchor="middle">INA219</text>

    <rect x="25" y="65" width="75" height="50" rx="4" fill="#15803d" stroke="#166534" stroke-width="2"/>
    <circle cx="45" cy="90" r="10" fill="#dc2626" stroke="#fca5a5" stroke-width="2.5"/>
    <text class="pin-label-lg" x="45" y="112" fill="#fca5a5" text-anchor="middle">VIN+</text>
    <circle cx="78" cy="90" r="8" fill="#475569"/>
    <text class="pin-label" x="78" y="112" fill="#cbd5e1" text-anchor="middle">(Open)</text>

    <g transform="translate(25, 145)">
      <circle cx="20" cy="20" r="8" fill="#ea580c" stroke="#fed7aa" stroke-width="2"/>
      <text class="pin-label-lg" x="20" y="42" fill="#fed7aa" text-anchor="middle">VCC</text>
      <circle cx="70" cy="20" r="8" fill="#0f172a" stroke="#f8fafc" stroke-width="2"/>
      <text class="pin-label-lg" x="70" y="42" fill="#f8fafc" text-anchor="middle">GND</text>
      <circle cx="120" cy="20" r="8" fill="#2563eb" stroke="#93c5fd" stroke-width="2"/>
      <text class="pin-label-lg" x="120" y="42" fill="#93c5fd" text-anchor="middle">SCL</text>
      <circle cx="170" cy="20" r="8" fill="#16a34a" stroke="#86efac" stroke-width="2"/>
      <text class="pin-label-lg" x="170" y="42" fill="#86efac" text-anchor="middle">SDA</text>
    </g>
  </g>

  <!-- INA219 #3: 3.3V NATIVE RAIL (Address 0x44) -->
  <g id="comp-ina3" transform="translate(1620, 310)" filter="url(#shadow)">
    <rect width="320" height="200" rx="10" fill="#581c87" stroke="#7e22ce" stroke-width="2.5"/>
    <text class="title-large" x="160" y="28" fill="#f3e8ff" text-anchor="middle">INA219 #3 (ADDR: 0x44)</text>
    <text class="subtitle" x="160" y="46" fill="#d8b4fe" text-anchor="middle">Native 3.3V Bus Monitor (A1=VCC)</text>
    
    <rect x="135" y="65" width="50" height="26" rx="2" fill="#0f172a" stroke="#94a3b8" stroke-width="1.5"/>
    <text x="160" y="82" fill="#38bdf8" font-size="12" font-weight="bold" text-anchor="middle">R100</text>
    <rect x="140" y="100" width="40" height="28" rx="2" fill="#18181b" stroke="#52525b"/>
    <text x="160" y="118" fill="#a1a1aa" font-size="9" font-weight="bold" text-anchor="middle">INA219</text>

    <rect x="25" y="65" width="75" height="50" rx="4" fill="#15803d" stroke="#166534" stroke-width="2"/>
    <circle cx="45" cy="90" r="10" fill="#ea580c" stroke="#fed7aa" stroke-width="2.5"/>
    <text class="pin-label-lg" x="45" y="112" fill="#fed7aa" text-anchor="middle">VIN+</text>
    <circle cx="78" cy="90" r="8" fill="#475569"/>
    <text class="pin-label" x="78" y="112" fill="#cbd5e1" text-anchor="middle">(Open)</text>

    <g transform="translate(25, 145)">
      <circle cx="20" cy="20" r="8" fill="#ea580c" stroke="#fed7aa" stroke-width="2"/>
      <text class="pin-label-lg" x="20" y="42" fill="#fed7aa" text-anchor="middle">VCC</text>
      <circle cx="70" cy="20" r="8" fill="#0f172a" stroke="#f8fafc" stroke-width="2"/>
      <text class="pin-label-lg" x="70" y="42" fill="#f8fafc" text-anchor="middle">GND</text>
      <circle cx="120" cy="20" r="8" fill="#2563eb" stroke="#93c5fd" stroke-width="2"/>
      <text class="pin-label-lg" x="120" y="42" fill="#93c5fd" text-anchor="middle">SCL</text>
      <circle cx="170" cy="20" r="8" fill="#16a34a" stroke="#86efac" stroke-width="2"/>
      <text class="pin-label-lg" x="170" y="42" fill="#86efac" text-anchor="middle">SDA</text>
    </g>
  </g>


  <!-- ===================================================================== -->
  <!-- 4. TB6612FNG MOTOR DRIVER (RED BOARD)                                 -->
  <!-- ===================================================================== -->
  <g id="comp-tb6612" transform="translate(70, 440)" filter="url(#shadow)">
    <rect width="320" height="320" rx="10" fill="#991b1b" stroke="#b91c1c" stroke-width="2.5"/>
    <text class="title-large" x="160" y="30" fill="#fee2e2" text-anchor="middle">TB6612FNG MOTOR DRIVER</text>
    <text class="subtitle" x="160" y="50" fill="#fca5a5" text-anchor="middle">12V Cooling Fan PWM Speed Controller</text>

    <!-- Toshiba Chip -->
    <rect x="110" y="105" width="100" height="60" rx="3" fill="#1e293b" stroke="#475569" stroke-width="2"/>
    <circle cx="122" cy="117" r="3" fill="#64748b"/>
    <text x="160" y="136" fill="#f8fafc" font-size="12" font-weight="bold" text-anchor="middle">TOSHIBA</text>
    <text x="160" y="153" fill="#94a3b8" font-size="10" font-weight="bold" text-anchor="middle">TB6612FNG</text>

    <!-- Power & Motor Drive Pins (Left Header) -->
    <g transform="translate(25, 75)">
      <circle cx="12" cy="25" r="8" fill="#ca8a04" stroke="#fef08a" stroke-width="2.5"/>
      <text class="pin-label-lg" x="28" y="30" fill="#fef08a">VM (+12V)</text>

      <circle cx="12" cy="65" r="8" fill="#ea580c" stroke="#fed7aa" stroke-width="2.5"/>
      <text class="pin-label-lg" x="28" y="70" fill="#fed7aa">VCC (3.3V)</text>

      <circle cx="12" cy="105" r="8" fill="#0f172a" stroke="#f8fafc" stroke-width="2.5"/>
      <text class="pin-label-lg" x="28" y="110" fill="#f8fafc">GND [COM]</text>

      <circle cx="12" cy="155" r="8" fill="#dc2626" stroke="#fca5a5" stroke-width="2.5"/>
      <text class="pin-label-lg" x="28" y="160" fill="#fca5a5">AO1 [FAN +]</text>

      <circle cx="12" cy="195" r="8" fill="#1e293b" stroke="#94a3b8" stroke-width="2.5"/>
      <text class="pin-label-lg" x="28" y="200" fill="#cbd5e1">AO2 [FAN -]</text>
    </g>

    <!-- Logic Control Pins (Right Header) -->
    <g transform="translate(190, 75)">
      <circle cx="105" cy="25" r="8" fill="#a855f7" stroke="#e9d5ff" stroke-width="2.5"/>
      <text class="pin-label-lg" x="88" y="30" fill="#e9d5ff" text-anchor="end">PWMA</text>

      <circle cx="105" cy="65" r="8" fill="#ec4899" stroke="#fbcfe8" stroke-width="2.5"/>
      <text class="pin-label-lg" x="88" y="70" fill="#fbcfe8" text-anchor="end">AIN1</text>

      <circle cx="105" cy="105" r="8" fill="#0f172a" stroke="#f8fafc" stroke-width="2.5"/>
      <text class="pin-label-lg" x="88" y="110" fill="#f8fafc" text-anchor="end">AIN2 [GND]</text>

      <circle cx="105" cy="155" r="8" fill="#38bdf8" stroke="#bae6fd" stroke-width="2.5"/>
      <text class="pin-label-lg" x="88" y="160" fill="#bae6fd" text-anchor="end">STBY</text>
    </g>
  </g>


  <!-- ===================================================================== -->
  <!-- 5. 12V DC COOLING FAN                                                 -->
  <!-- ===================================================================== -->
  <g id="comp-fan" transform="translate(70, 810)" filter="url(#shadow)">
    <rect width="250" height="250" rx="16" fill="#0f172a" stroke="#334155" stroke-width="3"/>
    <circle cx="125" cy="125" r="105" fill="#1e293b" stroke="#475569" stroke-width="2"/>

    <g transform="translate(125, 125)">
      <circle cx="0" cy="0" r="38" fill="#0f172a" stroke="#64748b" stroke-width="2"/>
      <path d="M 0 0 Q 50 -40 90 -25" stroke="#475569" stroke-width="20" fill="none" stroke-linecap="round"/>
      <path d="M 0 0 Q 50 50 70 80" stroke="#475569" stroke-width="20" fill="none" stroke-linecap="round"/>
      <path d="M 0 0 Q -25 60 -20 100" stroke="#475569" stroke-width="20" fill="none" stroke-linecap="round"/>
      <path d="M 0 0 Q -60 40 -90 45" stroke="#475569" stroke-width="20" fill="none" stroke-linecap="round"/>
      <path d="M 0 0 Q -60 -40 -75 -75" stroke="#475569" stroke-width="20" fill="none" stroke-linecap="round"/>
      <path d="M 0 0 Q 15 -60 20 -100" stroke="#475569" stroke-width="20" fill="none" stroke-linecap="round"/>
      
      <circle cx="0" cy="0" r="22" fill="#334155"/>
      <text x="0" y="5" fill="#f8fafc" font-size="11" font-weight="bold" text-anchor="middle">12V FAN</text>
    </g>

    <!-- Lead Wire Junctions -->
    <circle cx="195" cy="20" r="7" fill="#dc2626" stroke="#fca5a5" stroke-width="2"/>
    <text class="pin-label-lg" x="195" y="44" fill="#fca5a5" text-anchor="middle">RED (+)</text>

    <circle cx="225" cy="20" r="7" fill="#0f172a" stroke="#f8fafc" stroke-width="2"/>
    <text class="pin-label-lg" x="225" y="44" fill="#f8fafc" text-anchor="middle">BLK (-)</text>
  </g>


  <!-- ===================================================================== -->
  <!-- 6. DUAL DS18B20 TEMPERATURE PROBES & 4.7K PULL=UP                     -->
  <!-- ===================================================================== -->
  <g id="comp-ds18b20" transform="translate(70, 1120)" filter="url(#shadow)">
    <!-- Probe 1 -->
    <g transform="translate(0, 0)">
      <rect width="140" height="42" rx="8" fill="url(#metal-grad)" stroke="#475569" stroke-width="2"/>
      <text class="pin-label-lg" x="70" y="26" fill="#0f172a" text-anchor="middle">DS18B20 #1</text>
      <text class="subtitle" x="70" y="60" fill="#334155" text-anchor="middle">Core Surface Sensor</text>

      <rect x="140" y="10" width="30" height="22" rx="4" fill="#0f172a"/>
      <!-- Leads -->
      <circle cx="185" cy="12" r="6" fill="#ea580c"/>
      <text class="pin-label" x="200" y="16" fill="#ea580c">VDD (Red)</text>
      <circle cx="185" cy="26" r="6" fill="#eab308"/>
      <text class="pin-label" x="200" y="30" fill="#ca8a04">DQ (Yellow)</text>
      <circle cx="185" cy="40" r="6" fill="#0f172a" stroke="#64748b"/>
      <text class="pin-label" x="200" y="44" fill="#334155">GND (Black)</text>
    </g>

    <!-- Probe 2 -->
    <g transform="translate(0, 110)">
      <rect width="140" height="42" rx="8" fill="url(#metal-grad)" stroke="#475569" stroke-width="2"/>
      <text class="pin-label-lg" x="70" y="26" fill="#0f172a" text-anchor="middle">DS18B20 #2</text>
      <text class="subtitle" x="70" y="60" fill="#334155" text-anchor="middle">Inlet Air Ambient Sensor</text>

      <rect x="140" y="10" width="30" height="22" rx="4" fill="#0f172a"/>
      <circle cx="185" cy="12" r="6" fill="#ea580c"/>
      <circle cx="185" cy="26" r="6" fill="#eab308"/>
      <circle cx="185" cy="40" r="6" fill="#0f172a" stroke="#64748b"/>
    </g>

    <!-- 4.7k Resistor -->
    <g transform="translate(300, 50)">
      <line x1="-20" y1="16" x2="80" y2="16" stroke="#94a3b8" stroke-width="2.5"/>
      <rect x="0" y="0" width="60" height="32" rx="8" fill="#d97706" stroke="#b45309" stroke-width="2"/>
      <rect x="12" y="0" width="6" height="32" fill="#facc15"/>
      <rect x="22" y="0" width="6" height="32" fill="#7c3aed"/>
      <rect x="32" y="0" width="6" height="32" fill="#dc2626"/>
      <rect x="46" y="0" width="5" height="32" fill="#ca8a04"/>
      <text class="pin-label-lg" x="30" y="52" fill="#78350f" text-anchor="middle">4.7 kΩ</text>
      <text class="subtitle" x="30" y="68" fill="#92400e" text-anchor="middle">Bus Pull-Up</text>
    </g>
  </g>


  <!-- ===================================================================== -->
  <!-- 7. 2N3904 NPN TRANSISTOR SWITCH CIRCUIT                                -->
  <!-- ===================================================================== -->
  <g id="comp-transistor" transform="translate(480, 520)" filter="url(#shadow)">
    <rect width="210" height="190" rx="10" fill="#f1f5f9" stroke="#94a3b8" stroke-width="2" stroke-dasharray="5"/>
    <text class="title-large" x="105" y="28" fill="#0f172a" text-anchor="middle">PS_ON# NPN DRIVER</text>
    <text class="subtitle" x="105" y="46" fill="#64748b" text-anchor="middle">Active-Low Main Power Relay</text>

    <!-- Transistor Package -->
    <g transform="translate(105, 95)">
      <path d="M -18 20 C -18 -12 18 -12 18 20 Z" fill="#18181b" stroke="#3f3f46" stroke-width="2"/>
      <rect x="-18" y="20" width="36" height="8" fill="#18181b"/>
      <text x="0" y="12" fill="#f8fafc" font-size="9" font-weight="bold" text-anchor="middle">2N3904</text>

      <!-- Pins -->
      <circle cx="0" cy="-30" r="7" fill="#10b981" stroke="#a7f3d0" stroke-width="2"/>
      <text class="pin-label-lg" x="16" y="-25" fill="#065f46">C [PS_ON#]</text>

      <circle cx="-42" cy="22" r="7" fill="#38bdf8" stroke="#bae6fd" stroke-width="2"/>
      <text class="pin-label-lg" x="-58" y="26" fill="#0369a1" text-anchor="end">B</text>

      <circle cx="0" cy="55" r="7" fill="#0f172a" stroke="#f8fafc" stroke-width="2"/>
      <text class="pin-label-lg" x="16" y="60" fill="#0f172a">E [GND]</text>
    </g>

    <!-- Resistors -->
    <rect x="25" y="105" width="32" height="16" rx="3" fill="#d97706" stroke="#b45309"/>
    <text class="pin-label" x="41" y="135" fill="#92400e" text-anchor="middle">4.7k Base</text>

    <rect x="45" y="150" width="32" height="14" rx="3" fill="#d97706" stroke="#b45309"/>
    <text class="pin-label" x="61" y="176" fill="#92400e" text-anchor="middle">100k Pulldown</text>
  </g>


  <!-- ===================================================================== -->
  <!-- 8. 16x2 CHARACTER LCD WITH PCF8574 I2C BACKPACK                       -->
  <!-- ===================================================================== -->
  <g id="comp-lcd" transform="translate(1500, 560)" filter="url(#shadow)">
    <rect width="560" height="260" rx="12" fill="#14532d" stroke="#166534" stroke-width="3"/>
    <circle cx="20" cy="20" r="7" fill="#14532d" stroke="url(#gold-grad)" stroke-width="2"/>
    <circle cx="540" cy="20" r="7" fill="#14532d" stroke="url(#gold-grad)" stroke-width="2"/>
    <circle cx="20" cy="240" r="7" fill="#14532d" stroke="url(#gold-grad)" stroke-width="2"/>
    <circle cx="540" cy="240" r="7" fill="#14532d" stroke="url(#gold-grad)" stroke-width="2"/>

    <!-- Black Bezel -->
    <rect x="45" y="30" width="470" height="160" rx="6" fill="#0f172a" stroke="#334155" stroke-width="2.5"/>

    <!-- Blue Display Matrix Screen -->
    <rect x="65" y="45" width="430" height="130" rx="5" fill="url(#lcd-grad)" stroke="#0284c7" stroke-width="2"/>

    <!-- Large Telemetry Text Matrix -->
    <text x="85" y="95" fill="#f0f9ff" font-family="'SF Mono', Consolas, monospace" font-size="24" font-weight="bold" letter-spacing="2">
      T1:48.6C  T2:29.4C
    </text>
    <text x="85" y="145" fill="#f0f9ff" font-family="'SF Mono', Consolas, monospace" font-size="24" font-weight="bold" letter-spacing="2">
      Main:ACT [NORMAL]
    </text>

    <!-- PCF8574 Backpack Header -->
    <g transform="translate(140, 205)">
      <rect width="280" height="44" rx="5" fill="#0f172a" stroke="#475569" stroke-width="2"/>
      <text x="140" y="15" fill="#94a3b8" font-size="10" font-weight="bold" text-anchor="middle">PCF8574 I2C BACKPACK</text>

      <circle cx="35" cy="28" r="8" fill="#0f172a" stroke="#f8fafc" stroke-width="2.5"/>
      <text class="pin-label-lg" x="35" y="52" fill="#f8fafc" text-anchor="middle">GND</text>

      <circle cx="95" cy="28" r="8" fill="#dc2626" stroke="#fca5a5" stroke-width="2.5"/>
      <text class="pin-label-lg" x="95" y="52" fill="#fca5a5" text-anchor="middle">VCC (5V)</text>

      <circle cx="155" cy="28" r="8" fill="#16a34a" stroke="#86efac" stroke-width="2.5"/>
      <text class="pin-label-lg" x="155" y="52" fill="#86efac" text-anchor="middle">SDA</text>

      <circle cx="215" cy="28" r="8" fill="#2563eb" stroke="#93c5fd" stroke-width="2.5"/>
      <text class="pin-label-lg" x="215" y="52" fill="#93c5fd" text-anchor="middle">SCL</text>
    </g>

    <!-- Contrast Trimpot -->
    <rect x="445" y="210" width="30" height="30" rx="3" fill="#2563eb" stroke="#1d4ed8"/>
    <circle cx="460" cy="225" r="9" fill="#f8fafc"/>
    <line x1="453" y1="225" x2="467" y2="225" stroke="#64748b" stroke-width="2.5"/>
    <text x="460" y="252" fill="#bae6fd" font-size="9" font-weight="bold" text-anchor="middle">CONTRAST</text>
  </g>


  <!-- ===================================================================== -->
  <!-- 9. MANUAL CONTROL SWITCHES (SW1 & SW2)                                -->
  <!-- ===================================================================== -->
  <g id="comp-switches" transform="translate(1500, 870)" filter="url(#shadow)">
    <!-- SW1: Main Enable -->
    <g transform="translate(0, 0)">
      <rect width="210" height="110" rx="8" fill="#1e293b" stroke="#475569" stroke-width="2.5"/>
      <rect x="25" y="25" width="55" height="60" rx="4" fill="#dc2626" stroke="#b91c1c" stroke-width="2.5"/>
      <text x="52" y="52" fill="#ffffff" font-size="14" font-weight="bold" text-anchor="middle">I</text>
      <text x="52" y="74" fill="#ffffff" font-size="14" font-weight="bold" text-anchor="middle">O</text>

      <text class="title-large" x="145" y="42" fill="#f8fafc">SW1: MAIN</text>
      <text class="subtitle" x="145" y="62" fill="#94a3b8">Output Enable</text>
      <text class="pin-label-lg" x="145" y="82" fill="#f5d0fe">GPIO 18</text>
      <circle cx="110" cy="95" r="6" fill="#d946ef" stroke="#f5d0fe"/>
    </g>

    <!-- SW2: Setup AP -->
    <g transform="translate(260, 0)">
      <rect width="210" height="110" rx="8" fill="#1e293b" stroke="#475569" stroke-width="2.5"/>
      <rect x="25" y="25" width="55" height="60" rx="4" fill="#2563eb" stroke="#1d4ed8" stroke-width="2.5"/>
      <text x="52" y="52" fill="#ffffff" font-size="14" font-weight="bold" text-anchor="middle">I</text>
      <text x="52" y="74" fill="#ffffff" font-size="14" font-weight="bold" text-anchor="middle">O</text>

      <text class="title-large" x="145" y="42" fill="#f8fafc">SW2: SETUP</text>
      <text class="subtitle" x="145" y="62" fill="#94a3b8">SoftAP Mode</text>
      <text class="pin-label-lg" x="145" y="82" fill="#fecdd3">GPIO 23</text>
      <circle cx="110" cy="95" r="6" fill="#f43f5e" stroke="#fecdd3"/>
    </g>
  </g>


  <!-- ===================================================================== -->
  <!-- 10. SYSTEM TITLE BLOCK & REVISION METADATA                            -->
  <!-- ===================================================================== -->
  <g id="title-block" transform="translate(1450, 1220)">
    <rect width="880" height="300" rx="6" fill="#ffffff" stroke="#0f172a" stroke-width="2.5"/>
    
    <line x1="0" y1="75" x2="880" y2="75" stroke="#0f172a" stroke-width="2"/>
    <line x1="0" y1="150" x2="880" y2="150" stroke="#0f172a" stroke-width="2"/>
    <line x1="0" y1="225" x2="880" y2="225" stroke="#0f172a" stroke-width="2"/>
    
    <line x1="560" y1="0" x2="560" y2="225" stroke="#0f172a" stroke-width="2"/>
    <line x1="720" y1="0" x2="720" y2="225" stroke="#0f172a" stroke-width="2"/>

    <!-- Box 1 -->
    <text x="280" y="32" fill="#64748b" font-size="12" font-weight="bold" text-anchor="middle">RAJALAKSHMI INSTITUTE OF TECHNOLOGY, CHENNAI</text>
    <text x="280" y="58" fill="#0f172a" font-size="16" font-weight="bold" text-anchor="middle">TRANSFORMER CONDITION MONITORING SYSTEM</text>

    <!-- Box 2 -->
    <text x="25" y="100" fill="#64748b" font-size="11" font-weight="bold">DRAWING TITLE:</text>
    <text x="25" y="128" fill="#0369a1" font-size="18" font-weight="bold">Hardware Interconnect &amp; Full Circuit Wiring Schematic</text>

    <!-- Box 3 -->
    <text x="25" y="175" fill="#64748b" font-size="11" font-weight="bold">SYSTEM ARCHITECTURE BASELINE:</text>
    <text x="25" y="202" fill="#0f172a" font-size="15" font-weight="bold">Revision 3.0 Production Baseline (Controlled Engineering Record)</text>

    <!-- Control Table -->
    <text x="640" y="30" fill="#64748b" font-size="11" font-weight="bold" text-anchor="middle">DOC NUMBER</text>
    <text x="640" y="56" fill="#0f172a" font-size="13" font-weight="bold" text-anchor="middle">TMS-ESP32-SCHEM</text>

    <text x="800" y="30" fill="#64748b" font-size="11" font-weight="bold" text-anchor="middle">REVISION</text>
    <text x="800" y="56" fill="#dc2626" font-size="17" font-weight="bold" text-anchor="middle">REV 3.0</text>

    <text x="640" y="105" fill="#64748b" font-size="11" font-weight="bold" text-anchor="middle">DATE</text>
    <text x="640" y="132" fill="#0f172a" font-size="14" font-weight="bold" text-anchor="middle">OCTOBER 2026</text>

    <text x="800" y="105" fill="#64748b" font-size="11" font-weight="bold" text-anchor="middle">SHEET</text>
    <text x="800" y="132" fill="#0f172a" font-size="14" font-weight="bold" text-anchor="middle">1 OF 1</text>

    <text x="640" y="180" fill="#64748b" font-size="11" font-weight="bold" text-anchor="middle">STATUS</text>
    <text x="640" y="207" fill="#15803d" font-size="14" font-weight="bold" text-anchor="middle">APPROVED</text>

    <text x="800" y="180" fill="#64748b" font-size="11" font-weight="bold" text-anchor="middle">PLATFORM</text>
    <text x="800" y="207" fill="#0f172a" font-size="14" font-weight="bold" text-anchor="middle">ESP32 / ATX</text>

    <!-- Governing Principle -->
    <text x="440" y="256" fill="#0f172a" font-size="12" font-weight="bold" text-anchor="middle">
      CENTRAL GOVERNING PRINCIPLE: ZERO TRIP LATENCY AUTONOMOUS SAFETY CONTROLLER
    </text>
    <text x="440" y="280" fill="#64748b" font-size="10.5" text-anchor="middle">
      All safety-critical thermal monitoring, predictive cooling, and PS_ON# tripping execute locally from uninterrupted +5VSB.
    </text>
  </g>


  <!-- ===================================================================== -->
  <!-- 11. WIRING CONNECTIONS (ORTHOGONAL, WITH HIGH=CONTRAST BADGES)        -->
  <!-- ===================================================================== -->
  <g id="wires" stroke-width="4">

    <!-- ================================================================= -->
    <!-- 1. +5VSB STANDBY POWER (PURPLE)                                   -->
    <!-- ================================================================= -->
    <path class="wire wire-glow" stroke="#a855f7"
          d="M 255 335 L 255 365 L 720 365 L 720 854 L 1138 854"/>
    <!-- Wire Badge -->
    <g transform="translate(420, 350)" filter="url(#badge-shadow)">
      <rect x="0" y="0" width="220" height="28" rx="6" fill="#ffffff" stroke="#a855f7" stroke-width="2"/>
      <text class="badge-text" x="110" y="19" fill="#7e22ce" text-anchor="middle">+5VSB (Standby Power Infeed)</text>
    </g>

    <!-- ================================================================= -->
    <!-- 2. COMMON GROUND (BLACK WITH WHITE JAW)                           -->
    <!-- ================================================================= -->
    <path class="wire wire-glow" stroke="#0f172a" stroke-width="5"
          d="M 430 355 L 670 355 L 670 818 L 822 818"/>
    <g transform="translate(450, 390)" filter="url(#badge-shadow)">
      <rect x="0" y="0" width="210" height="28" rx="6" fill="#ffffff" stroke="#0f172a" stroke-width="2"/>
      <text class="badge-text" x="105" y="19" fill="#0f172a" text-anchor="middle">COMMON GROUND [COM]</text>
    </g>

    <!-- ================================================================= -->
    <!-- 3. PS_ON# LINE (EMERALD GREEN)                                    -->
    <!-- ================================================================= -->
    <path class="wire wire-glow" stroke="#10b981"
          d="M 315 335 L 315 470 L 585 470 L 585 585"/>
    <g transform="translate(340, 455)" filter="url(#badge-shadow)">
      <rect x="0" y="0" width="190" height="28" rx="6" fill="#ffffff" stroke="#10b981" stroke-width="2"/>
      <text class="badge-text" x="95" y="19" fill="#047857" text-anchor="middle">PS_ON# Supervisory Line</text>
    </g>

    <!-- GPIO 32 => 2N3904 Base -->
    <path class="wire wire-glow" stroke="#059669"
          d="M 822 566 L 710 566 L 710 635 L 515 635"/>
    <g transform="translate(685, 595)" filter="url(#badge-shadow)">
      <rect x="0" y="0" width="115" height="26" rx="5" fill="#ffffff" stroke="#059669" stroke-width="1.8"/>
      <text class="badge-text" x="57" y="18" fill="#047857" text-anchor="middle">GPIO 32 Trip</text>
    </g>

    <!-- 2N3904 Emitter => GND -->
    <path class="wire wire-glow" stroke="#0f172a"
          d="M 585 670 L 585 730 L 670 730"/>

    <!-- ================================================================= -->
    <!-- 4. I2C BUS (SDA = GREEN, SCL = BLUE)                              -->
    <!-- ================================================================= -->
    <!-- I2C SDA (GPIO 21): ESP32 (1138, 494) => LCD SDA & INA219 SDA -->
    <path class="wire wire-glow" stroke="#16a34a"
          d="M 1138 494 L 1320 494 L 1320 235 L 1790 235"/>
    <path class="wire wire-glow" stroke="#16a34a"
          d="M 1790 235 L 2170 235"/>
    <path class="wire wire-glow" stroke="#16a34a"
          d="M 1320 475 L 1790 475"/>
    <path class="wire wire-glow" stroke="#16a34a"
          d="M 1320 494 L 1320 815 L 1655 815 L 1655 793"/>
    <circle cx="1320" cy="494" r="5.5" fill="#16a34a" class="bus-junction"/>
    <circle cx="1320" cy="235" r="5.5" fill="#16a34a" class="bus-junction"/>
    <circle cx="1320" cy="475" r="5.5" fill="#16a34a" class="bus-junction"/>

    <g transform="translate(1340, 220)" filter="url(#badge-shadow)">
      <rect x="0" y="0" width="160" height="28" rx="6" fill="#ffffff" stroke="#16a34a" stroke-width="2"/>
      <text class="badge-text" x="80" y="19" fill="#15803d" text-anchor="middle">I2C SDA (GPIO 21)</text>
    </g>

    <!-- I2C SCL (GPIO 22): ESP32 (1138, 386) => LCD SCL & INA219 SCL -->
    <path class="wire wire-glow" stroke="#2563eb"
          d="M 1138 386 L 1360 386 L 1360 190 L 1740 190 L 1740 215"/>
    <path class="wire wire-glow" stroke="#2563eb"
          d="M 1740 190 L 2120 190 L 2120 215"/>
    <path class="wire wire-glow" stroke="#2563eb"
          d="M 1360 435 L 1740 435 L 1740 455"/>
    <path class="wire wire-glow" stroke="#2563eb"
          d="M 1360 386 L 1360 840 L 1715 840 L 1715 793"/>
    <circle cx="1360" cy="386" r="5.5" fill="#2563eb" class="bus-junction"/>
    <circle cx="1360" cy="190" r="5.5" fill="#2563eb" class="bus-junction"/>
    <circle cx="1360" cy="435" r="5.5" fill="#2563eb" class="bus-junction"/>

    <g transform="translate(1380, 175)" filter="url(#badge-shadow)">
      <rect x="0" y="0" width="160" height="28" rx="6" fill="#ffffff" stroke="#2563eb" stroke-width="2"/>
      <text class="badge-text" x="80" y="19" fill="#1d4ed8" text-anchor="middle">I2C SCL (GPIO 22)</text>
    </g>

    <!-- LCD 5V Power from 5V line -->
    <path class="wire wire-glow" stroke="#dc2626"
          d="M 1138 854 L 1440 854 L 1440 820 L 1595 820 L 1595 793"/>
    <circle cx="1440" cy="854" r="5.5" fill="#dc2626" class="bus-junction"/>

    <!-- LCD GND from ground line -->
    <path class="wire wire-glow" stroke="#0f172a"
          d="M 1138 818 L 1460 818 L 1460 835 L 1535 835 L 1535 793"/>

    <!-- ================================================================= -->
    <!-- 5. MAIN DC RAILS (+12V, +5V, +3.3V)                               -->
    <!-- ================================================================= -->
    <!-- +12V Main => INA219 #1 VIN+ -->
    <path class="wire wire-glow" stroke="#ca8a04" stroke-width="4.5"
          d="M 430 155 L 1560 155 L 1560 160 L 1665 160"/>
    <g transform="translate(720, 140)" filter="url(#badge-shadow)">
      <rect x="0" y="0" width="180" height="28" rx="6" fill="#ffffff" stroke="#ca8a04" stroke-width="2"/>
      <text class="badge-text" x="90" y="19" fill="#854d0e" text-anchor="middle">+12V Main DC Infeed</text>
    </g>

    <!-- +12V Main => TB6612 VM Pin -->
    <path class="wire wire-glow" stroke="#ca8a04" stroke-width="3.5"
          d="M 430 155 L 460 155 L 460 420 L 40 420 L 40 540 L 95 540"/>

    <!-- +5V Main => INA219 #2 VIN+ -->
    <path class="wire wire-glow" stroke="#dc2626" stroke-width="3.5"
          d="M 430 255 L 1540 255 L 1540 60 L 2045 60 L 2045 160"/>
    <g transform="translate(680, 240)" filter="url(#badge-shadow)">
      <rect x="0" y="0" width="160" height="28" rx="6" fill="#ffffff" stroke="#dc2626" stroke-width="2"/>
      <text class="badge-text" x="80" y="19" fill="#991b1b" text-anchor="middle">+5V Main DC Rail</text>
    </g>

    <!-- +3.3V Main => INA219 #3 VIN+ -->
    <path class="wire wire-glow" stroke="#ea580c" stroke-width="3.5"
          d="M 430 305 L 1520 305 L 1520 400 L 1665 400"/>
    <g transform="translate(640, 290)" filter="url(#badge-shadow)">
      <rect x="0" y="0" width="170" height="28" rx="6" fill="#ffffff" stroke="#ea580c" stroke-width="2"/>
      <text class="badge-text" x="85" y="19" fill="#9a3412" text-anchor="middle">+3.3V Main DC Rail</text>
    </g>

    <!-- ================================================================= -->
    <!-- 6. TB6612 FAN DRIVER CONTROL SIGNALS                              -->
    <!-- ================================================================= -->
    <!-- PWMA (GPIO 25) -->
    <path class="wire wire-glow" stroke="#a855f7"
          d="M 822 638 L 440 638 L 440 540 L 365 540"/>
    <g transform="translate(450, 620)" filter="url(#badge-shadow)">
      <rect x="0" y="0" width="160" height="26" rx="5" fill="#ffffff" stroke="#a855f7" stroke-width="1.8"/>
      <text class="badge-text" x="80" y="18" fill="#7e22ce" text-anchor="middle">GPIO 25 (PWM Fan)</text>
    </g>

    <!-- AIN1 (GPIO 26) -->
    <path class="wire wire-glow" stroke="#ec4899"
          d="M 822 674 L 410 674 L 410 580 L 365 580"/>
    <g transform="translate(450, 660)" filter="url(#badge-shadow)">
      <rect x="0" y="0" width="150" height="26" rx="5" fill="#ffffff" stroke="#ec4899" stroke-width="1.8"/>
      <text class="badge-text" x="75" y="18" fill="#be185d" text-anchor="middle">GPIO 26 (Fan Dir)</text>
    </g>

    <!-- STBY (GPIO 33) -->
    <path class="wire wire-glow" stroke="#38bdf8"
          d="M 822 602 L 390 602 L 390 670 L 365 670"/>
    <g transform="translate(450, 590)" filter="url(#badge-shadow)">
      <rect x="0" y="0" width="140" height="26" rx="5" fill="#ffffff" stroke="#38bdf8" stroke-width="1.8"/>
      <text class="badge-text" x="70" y="18" fill="#0284c7" text-anchor="middle">GPIO 33 (STBY)</text>
    </g>

    <!-- TB6612 AO1 & AO2 to Fan -->
    <path class="wire wire-glow" stroke="#dc2626"
          d="M 95 670 L 50 670 L 50 780 L 265 780 L 265 830"/>
    <path class="wire wire-glow" stroke="#0f172a"
          d="M 95 710 L 35 710 L 35 795 L 295 795 L 295 830"/>

    <!-- ================================================================= -->
    <!-- 7. DS18B20 1=WIRE TEMPERATURE BUS                                 -->
    <!-- ================================================================= -->
    <!-- GPIO 27 => Both DS18B20 DQ Lines -->
    <path class="wire wire-glow" stroke="#eab308"
          d="M 822 710 L 470 710 L 470 1100 L 255 1100 L 255 1146"/>
    <path class="wire wire-glow" stroke="#eab308"
          d="M 255 1146 L 255 1256"/>
    <g transform="translate(480, 780)" filter="url(#badge-shadow)">
      <rect x="0" y="0" width="180" height="28" rx="6" fill="#ffffff" stroke="#eab308" stroke-width="2"/>
      <text class="badge-text" x="90" y="19" fill="#a16207" text-anchor="middle">1-Wire DQ (GPIO 27)</text>
    </g>

    <!-- 3.3V Logic Supply => DS18B20 VDD & Pull=Up -->
    <path class="wire wire-glow" stroke="#ea580c"
          d="M 822 350 L 740 350 L 740 1080 L 225 1080 L 225 1132"/>
    <path class="wire wire-glow" stroke="#ea580c"
          d="M 225 1132 L 225 1242"/>
    <g transform="translate(540, 1065)" filter="url(#badge-shadow)">
      <rect x="0" y="0" width="170" height="28" rx="6" fill="#ffffff" stroke="#ea580c" stroke-width="2"/>
      <text class="badge-text" x="85" y="19" fill="#c2410c" text-anchor="middle">3.3V Logic Rail</text>
    </g>

    <!-- ================================================================= -->
    <!-- 8. SWITCHES SW1 & SW2                                             -->
    <!-- ================================================================= -->
    <!-- SW1: GPIO 18 -->
    <path class="wire wire-glow" stroke="#d946ef"
          d="M 1138 566 L 1400 566 L 1400 965 L 1610 965"/>
    <g transform="translate(1410, 600)" filter="url(#badge-shadow)">
      <rect x="0" y="0" width="140" height="26" rx="5" fill="#ffffff" stroke="#d946ef" stroke-width="1.8"/>
      <text class="badge-text" x="70" y="18" fill="#a21caf" text-anchor="middle">GPIO 18 (SW1)</text>
    </g>

    <!-- SW2: GPIO 23 -->
    <path class="wire wire-glow" stroke="#f43f5e"
          d="M 1138 350 L 1420 350 L 1420 965 L 1870 965"/>
    <g transform="translate(1430, 365)" filter="url(#badge-shadow)">
      <rect x="0" y="0" width="140" height="26" rx="5" fill="#ffffff" stroke="#f43f5e" stroke-width="1.8"/>
      <text class="badge-text" x="70" y="18" fill="#be123c" text-anchor="middle">GPIO 23 (SW2)</text>
    </g>

  </g>


  <!-- ===================================================================== -->
  <!-- 12. DRAWING SIGNAL LEGEND & WIRE COLOR CODE                           -->
  <!-- ===================================================================== -->
  <g id="drawing-legend" transform="translate(800, 960)" filter="url(#shadow)">
    <rect width="640" height="220" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="2"/>
    <rect width="640" height="38" rx="8" fill="#f1f5f9"/>
    <text class="title-large" x="320" y="26" fill="#0f172a" text-anchor="middle">SIGNAL BUS LEGEND &amp; WIRE COLOR CODING</text>
    
    <g transform="translate(30, 55)" font-family="'Segoe UI', sans-serif" font-size="13" font-weight="bold">
      <!-- Col 1 -->
      <line x1="0" y1="15" x2="45" y2="15" stroke="#a855f7" stroke-width="5"/>
      <text x="58" y="20" fill="#6b21a8">+5VSB Standby Power Infeed</text>

      <line x1="0" y1="45" x2="45" y2="45" stroke="#0f172a" stroke-width="5"/>
      <text x="58" y="50" fill="#0f172a">Common Ground [COM]</text>

      <line x1="0" y1="75" x2="45" y2="75" stroke="#ca8a04" stroke-width="5"/>
      <text x="58" y="80" fill="#854d0e">+12V Main DC Power Rail</text>

      <line x1="0" y1="105" x2="45" y2="105" stroke="#dc2626" stroke-width="5"/>
      <text x="58" y="110" fill="#991b1b">+5V Main &amp; LCD VCC Supply</text>

      <line x1="0" y1="135" x2="45" y2="135" stroke="#ea580c" stroke-width="5"/>
      <text x="58" y="140" fill="#9a3412">+3.3V Logic &amp; Sensor Rail</text>

      <!-- Col 2 -->
      <g transform="translate(300, 0)">
        <line x1="0" y1="15" x2="45" y2="15" stroke="#16a34a" stroke-width="5"/>
        <text x="58" y="20" fill="#166534">I2C SDA (Data Bus - GPIO 21)</text>

        <line x1="0" y1="45" x2="45" y2="45" stroke="#2563eb" stroke-width="5"/>
        <text x="58" y="50" fill="#1e40af">I2C SCL (Clock Bus - GPIO 22)</text>

        <line x1="0" y1="75" x2="45" y2="75" stroke="#eab308" stroke-width="5"/>
        <text x="58" y="80" fill="#854d0e">1-Wire DQ Bus (GPIO 27)</text>

        <line x1="0" y1="105" x2="45" y2="105" stroke="#10b981" stroke-width="5"/>
        <text x="58" y="110" fill="#065f46">PS_ON# Supervisory Trip Line</text>

        <line x1="0" y1="135" x2="45" y2="135" stroke="#a855f7" stroke-width="5"/>
        <text x="58" y="140" fill="#581c87">TB6612 Fan PWM (GPIO 25)</text>
      </g>
    </g>
  </g>

</svg>'''

    output_path = os.path.join("documentation", "transformer_cbm_circuit_diagram.svg")
    
    # Validate XML parsing
    try:
        ET.fromstring(svg_content)
        print("XML Syntax Validation Passed: Well-formed SVG.")
    except ET.ParseError as e:
        print(f"XML Parsing Error: {e}")
        return False
        
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
        
    print(f"Successfully generated {output_path} ({len(svg_content)} bytes).")
    return True

if __name__ == "__main__":
    build_svg()
