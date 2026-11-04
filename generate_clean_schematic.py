# -*- coding: utf-8 -*-
"""
Clean, Professional, Human-Engineered Schematic Generator
Cirkit Designer / Fritzing Style with Common Ground & Power Bus Trunks
"""

import os
import xml.etree.ElementTree as ET

def generate_clean_schematic():
    svg = r'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2000 1300" width="2000" height="1300">
  <defs>
    <!-- Clean drafting grid paper -->
    <pattern id="grid-pattern" width="20" height="20" patternUnits="userSpaceOnUse">
      <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#f1f5f9" stroke-width="1"/>
    </pattern>
    <pattern id="grid-dots" width="20" height="20" patternUnits="userSpaceOnUse">
      <circle cx="10" cy="10" r="0.75" fill="#cbd5e1"/>
    </pattern>

    <!-- Drop shadow for realistic modules -->
    <filter id="module-shadow" x="-4%" y="-4%" width="108%" height="110%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="2" dy="4" stdDeviation="4" flood-color="#0f172a" flood-opacity="0.12"/>
    </filter>

    <!-- Metallic IC gradient -->
    <linearGradient id="shield-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="50%" stop-color="#e2e8f0"/>
      <stop offset="100%" stop-color="#94a3b8"/>
    </linearGradient>

    <!-- Gold connector gradient -->
    <linearGradient id="gold-pin" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#fef08a"/>
      <stop offset="100%" stop-color="#ca8a04"/>
    </linearGradient>
  </defs>

  <style>
    text { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }
    .board-title { font-size: 13px; font-weight: 700; fill: #ffffff; letter-spacing: 0.5px; }
    .board-subtitle { font-size: 9px; font-weight: 600; fill: #94a3b8; }
    .pin-text { font-family: 'SF Mono', Consolas, monospace; font-size: 10px; font-weight: 700; }
    .wire { fill: none; stroke-linecap: round; stroke-linejoin: round; }
    .wire-gnd { stroke: #047857; stroke-width: 3.5; }
    .wire-3v3 { stroke: #ea580c; stroke-width: 3.5; }
    .wire-5v { stroke: #dc2626; stroke-width: 3.5; }
    .wire-12v { stroke: #ca8a04; stroke-width: 3.5; }
    .wire-sda { stroke: #2563eb; stroke-width: 3; }
    .wire-scl { stroke: #0284c7; stroke-width: 3; }
    .wire-sig { stroke-width: 3; }
    .junction { stroke: #ffffff; stroke-width: 1.5; }
  </style>

  <!-- Background Canvas -->
  <rect width="2000" height="1300" fill="#ffffff"/>
  <rect width="2000" height="1300" fill="url(#grid-dots)"/>

  <!-- ===================================================================== -->
  <!-- 1. ATX BENCH BREAKOUT BOARD (Top Left)                                -->
  <!-- ===================================================================== -->
  <g id="mod-atx" transform="translate(60, 60)" filter="url(#module-shadow)">
    <!-- PCB -->
    <rect width="320" height="230" rx="8" fill="#15803d" stroke="#166534" stroke-width="2"/>
    <circle cx="15" cy="15" r="5" fill="#15803d" stroke="url(#gold-pin)" stroke-width="2"/>
    <circle cx="305" cy="15" r="5" fill="#15803d" stroke="url(#gold-pin)" stroke-width="2"/>
    <circle cx="15" cy="215" r="5" fill="#15803d" stroke="url(#gold-pin)" stroke-width="2"/>
    <circle cx="305" cy="215" r="5" fill="#15803d" stroke="url(#gold-pin)" stroke-width="2"/>

    <text class="board-title" x="160" y="24" text-anchor="middle">ATX BREAKOUT (XH-M229)</text>
    <text x="160" y="38" fill="#bbf7d0" font-size="8.5" font-weight="600" text-anchor="middle">Inbuilt Rail Fuses F1-F4</text>

    <!-- 24-Pin ATX Socket -->
    <rect x="20" y="55" width="85" height="155" rx="3" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.5"/>
    <text x="62" y="135" fill="#64748b" font-size="10" font-weight="bold" text-anchor="middle" transform="rotate(-90 62 135)">24-PIN ATX</text>

    <!-- Fuses -->
    <g transform="translate(125, 60)">
      <rect x="0" y="0" width="36" height="14" rx="2" fill="#e2e8f0" stroke="#475569"/><text x="18" y="10" font-size="7" font-weight="bold" text-anchor="middle" fill="#0f172a">F1:12V</text>
      <rect x="0" y="26" width="36" height="14" rx="2" fill="#e2e8f0" stroke="#475569"/><text x="18" y="36" font-size="7" font-weight="bold" text-anchor="middle" fill="#0f172a">F2:-12V</text>
      <rect x="0" y="52" width="36" height="14" rx="2" fill="#e2e8f0" stroke="#475569"/><text x="18" y="62" font-size="7" font-weight="bold" text-anchor="middle" fill="#0f172a">F3:5V</text>
      <rect x="0" y="78" width="36" height="14" rx="2" fill="#e2e8f0" stroke="#475569"/><text x="18" y="88" font-size="7" font-weight="bold" text-anchor="middle" fill="#0f172a">F4:3.3V</text>
    </g>

    <!-- Terminal Posts (Right edge) -->
    <!-- +12V -->
    <circle cx="275" cy="65" r="14" fill="#ca8a04" stroke="#fef08a" stroke-width="2.5"/>
    <circle cx="275" cy="65" r="5" fill="#713f12"/>
    <text class="pin-text" x="235" y="69" fill="#fef08a">+12V</text>

    <!-- +5V -->
    <circle cx="275" cy="110" r="14" fill="#dc2626" stroke="#fca5a5" stroke-width="2.5"/>
    <circle cx="275" cy="110" r="5" fill="#7f1d1d"/>
    <text class="pin-text" x="240" y="114" fill="#fca5a5">+5V</text>

    <!-- +3.3V -->
    <circle cx="275" cy="155" r="14" fill="#ea580c" stroke="#fed7aa" stroke-width="2.5"/>
    <circle cx="275" cy="155" r="5" fill="#7c2d12"/>
    <text class="pin-text" x="230" y="159" fill="#fed7aa">+3.3V</text>

    <!-- GND -->
    <circle cx="275" cy="200" r="14" fill="#0f172a" stroke="#f8fafc" stroke-width="2.5"/>
    <circle cx="275" cy="200" r="5" fill="#334155"/>
    <text class="pin-text" x="235" y="204" fill="#f8fafc">GND</text>

    <!-- Header for +5VSB and PS_ON# -->
    <rect x="120" y="175" width="80" height="35" rx="3" fill="#0f172a" stroke="#475569"/>
    <circle cx="140" cy="192" r="6" fill="#a855f7" stroke="#e9d5ff" stroke-width="1.5"/>
    <text class="pin-text" x="140" y="170" fill="#e9d5ff" text-anchor="middle">+5VSB</text>

    <circle cx="180" cy="192" r="6" fill="#10b981" stroke="#a7f3d0" stroke-width="1.5"/>
    <text class="pin-text" x="180" y="170" fill="#a7f3d0" text-anchor="middle">PS_ON#</text>
  </g>


  <!-- ===================================================================== -->
  <!-- 2. ESP32-WROOM-32 DEVKITC (Center-Left)                               -->
  <!-- ===================================================================== -->
  <g id="mod-esp32" transform="translate(560, 260)" filter="url(#module-shadow)">
    <!-- Matte black board -->
    <rect width="250" height="580" rx="8" fill="#18181b" stroke="#3f3f46" stroke-width="2"/>
    
    <!-- Metal Shield -->
    <rect x="45" y="45" width="160" height="145" rx="5" fill="url(#shield-grad)" stroke="#64748b" stroke-width="1.5"/>
    <!-- Gold PCB Antenna -->
    <path d="M 70 58 L 85 58 L 85 75 L 100 75 L 100 58 L 115 58 L 115 75 L 130 75 L 130 58 L 145 58 L 145 75 L 160 75 L 160 58 L 180 58" 
          fill="none" stroke="url(#gold-pin)" stroke-width="3" stroke-linecap="round"/>
    <text x="125" y="115" fill="#0f172a" font-size="14" font-weight="bold" text-anchor="middle">ESPRESSIF</text>
    <text x="125" y="135" fill="#1e293b" font-size="11" font-weight="bold" text-anchor="middle">ESP-WROOM-32</text>
    <text x="125" y="155" fill="#475569" font-size="8.5" text-anchor="middle">Wi-Fi &amp; Bluetooth MCU</text>

    <!-- CP2102 USB Bridge -->
    <rect x="100" y="260" width="50" height="50" rx="2" fill="#27272a" stroke="#52525b"/>
    <text x="125" y="290" fill="#a1a1aa" font-size="8" font-weight="bold" text-anchor="middle">CP2102</text>

    <!-- USB Port & Buttons -->
    <rect x="100" y="550" width="50" height="25" rx="3" fill="#cbd5e1" stroke="#64748b"/>
    <circle cx="45" cy="530" r="7" fill="#52525b"/><text x="45" y="550" fill="#a1a1aa" font-size="8" text-anchor="middle">EN</text>
    <circle cx="205" cy="530" r="7" fill="#52525b"/><text x="205" y="550" fill="#a1a1aa" font-size="8" text-anchor="middle">BOOT</text>

    <!-- Left Header Pins (15 Pins, Pitch: 32px) -->
    <!-- y = 80 + i*32 -->
    <!-- 3V3 (y=80) -->
    <circle cx="16" cy="80" r="6" fill="#ea580c" stroke="#fed7aa" stroke-width="1.5"/>
    <text class="pin-text" x="28" y="84" fill="#fed7aa">3V3</text>

    <circle cx="16" cy="112" r="5" fill="#27272a" stroke="#71717a"/><text class="pin-text" x="28" y="116" fill="#71717a">EN</text>
    <circle cx="16" cy="144" r="5" fill="#27272a" stroke="#71717a"/><text class="pin-text" x="28" y="148" fill="#71717a">VP</text>
    <circle cx="16" cy="176" r="5" fill="#27272a" stroke="#71717a"/><text class="pin-text" x="28" y="180" fill="#71717a">VN</text>
    <circle cx="16" cy="208" r="5" fill="#27272a" stroke="#71717a"/><text class="pin-text" x="28" y="212" fill="#71717a">D34</text>
    <circle cx="16" cy="240" r="5" fill="#27272a" stroke="#71717a"/><text class="pin-text" x="28" y="244" fill="#71717a">D35</text>

    <!-- D32 (y=272) -> PS_ON# -->
    <circle cx="16" cy="272" r="6" fill="#10b981" stroke="#a7f3d0" stroke-width="1.5"/>
    <text class="pin-text" x="28" y="276" fill="#a7f3d0">D32 [PS_ON]</text>

    <!-- D33 (y=304) -> STBY -->
    <circle cx="16" cy="304" r="6" fill="#38bdf8" stroke="#bae6fd" stroke-width="1.5"/>
    <text class="pin-text" x="28" y="308" fill="#bae6fd">D33 [STBY]</text>

    <!-- D25 (y=336) -> PWMA -->
    <circle cx="16" cy="336" r="6" fill="#a855f7" stroke="#e9d5ff" stroke-width="1.5"/>
    <text class="pin-text" x="28" y="340" fill="#e9d5ff">D25 [PWM]</text>

    <!-- D26 (y=368) -> AIN1 -->
    <circle cx="16" cy="368" r="6" fill="#ec4899" stroke="#fbcfe8" stroke-width="1.5"/>
    <text class="pin-text" x="28" y="372" fill="#fbcfe8">D26 [DIR]</text>

    <!-- D27 (y=400) -> 1-Wire DQ -->
    <circle cx="16" cy="400" r="6" fill="#eab308" stroke="#fef08a" stroke-width="1.5"/>
    <text class="pin-text" x="28" y="404" fill="#fef08a">D27 [1-WIRE]</text>

    <circle cx="16" cy="432" r="5" fill="#27272a" stroke="#71717a"/><text class="pin-text" x="28" y="436" fill="#71717a">D14</text>
    <circle cx="16" cy="464" r="5" fill="#27272a" stroke="#71717a"/><text class="pin-text" x="28" y="468" fill="#71717a">D12</text>

    <!-- GND (y=496) -->
    <circle cx="16" cy="496" r="6" fill="#0f172a" stroke="#f8fafc" stroke-width="1.5"/>
    <text class="pin-text" x="28" y="500" fill="#f8fafc">GND</text>

    <circle cx="16" cy="528" r="5" fill="#27272a" stroke="#71717a"/><text class="pin-text" x="28" y="532" fill="#71717a">D13</text>


    <!-- Right Header Pins (15 Pins) -->
    <!-- D23 (y=80) -->
    <circle cx="234" cy="80" r="6" fill="#f43f5e" stroke="#fecdd3" stroke-width="1.5"/>
    <text class="pin-text" x="160" y="84" fill="#fecdd3">D23 [SW2]</text>

    <!-- D22 (y=112) -> SCL -->
    <circle cx="234" cy="112" r="6" fill="#0284c7" stroke="#bae6fd" stroke-width="1.5"/>
    <text class="pin-text" x="165" y="116" fill="#bae6fd">D22 [SCL]</text>

    <circle cx="234" cy="144" r="5" fill="#27272a" stroke="#71717a"/><text class="pin-text" x="195" y="148" fill="#71717a">TX0</text>
    <circle cx="234" cy="176" r="5" fill="#27272a" stroke="#71717a"/><text class="pin-text" x="195" y="180" fill="#71717a">RX0</text>

    <!-- D21 (y=208) -> SDA -->
    <circle cx="234" cy="208" r="6" fill="#2563eb" stroke="#93c5fd" stroke-width="1.5"/>
    <text class="pin-text" x="165" y="212" fill="#93c5fd">D21 [SDA]</text>

    <circle cx="234" cy="240" r="5" fill="#27272a" stroke="#71717a"/><text class="pin-text" x="195" y="244" fill="#71717a">D19</text>

    <!-- D18 (y=272) -> SW1 -->
    <circle cx="234" cy="272" r="6" fill="#d946ef" stroke="#f5d0fe" stroke-width="1.5"/>
    <text class="pin-text" x="160" y="276" fill="#f5d0fe">D18 [SW1]</text>

    <circle cx="234" cy="304" r="5" fill="#27272a" stroke="#71717a"/><text class="pin-text" x="200" y="308" fill="#71717a">D5</text>
    <circle cx="234" cy="336" r="5" fill="#27272a" stroke="#71717a"/><text class="pin-text" x="195" y="340" fill="#71717a">D17</text>
    <circle cx="234" cy="368" r="5" fill="#27272a" stroke="#71717a"/><text class="pin-text" x="195" y="372" fill="#71717a">D16</text>
    <circle cx="234" cy="400" r="5" fill="#27272a" stroke="#71717a"/><text class="pin-text" x="200" y="404" fill="#71717a">D4</text>
    <circle cx="234" cy="432" r="5" fill="#27272a" stroke="#71717a"/><text class="pin-text" x="200" y="436" fill="#71717a">D0</text>
    <circle cx="234" cy="464" r="5" fill="#27272a" stroke="#71717a"/><text class="pin-text" x="200" y="468" fill="#71717a">D2</text>
    <circle cx="234" cy="496" r="5" fill="#27272a" stroke="#71717a"/><text class="pin-text" x="195" y="500" fill="#71717a">D15</text>

    <!-- 5V / VIN (y=528) -->
    <circle cx="234" cy="528" r="6" fill="#dc2626" stroke="#fca5a5" stroke-width="1.5"/>
    <text class="pin-text" x="175" y="532" fill="#fca5a5">5V [VIN]</text>
  </g>


  <!-- ===================================================================== -->
  <!-- 3. THREE INA219 CURRENT/VOLTAGE SENSORS (Right Column)                -->
  <!-- ===================================================================== -->
  <!-- INA219 #1: 12V Rail (0x40) -->
  <g id="mod-ina1" transform="translate(1420, 60)" filter="url(#module-shadow)">
    <rect width="260" height="150" rx="8" fill="#581c87" stroke="#7e22ce" stroke-width="2"/>
    <text class="board-title" x="130" y="24" text-anchor="middle">INA219 #1 (ADDR: 0x40)</text>
    <text x="130" y="38" fill="#d8b4fe" font-size="9" font-weight="600" text-anchor="middle">12V Monitored Load Rail</text>
    
    <!-- Screw Terminal for Sensing -->
    <rect x="20" y="55" width="60" height="38" rx="3" fill="#15803d" stroke="#166534"/>
    <circle cx="35" cy="74" r="7" fill="#ca8a04" stroke="#fef08a" stroke-width="1.5"/>
    <text class="pin-text" x="35" y="88" fill="#fef08a" text-anchor="middle">VIN+</text>
    <circle cx="65" cy="74" r="7" fill="#ca8a04" stroke="#fef08a" stroke-width="1.5"/>
    <text class="pin-text" x="65" y="88" fill="#fef08a" text-anchor="middle">VIN-</text>

    <!-- Shunt & IC -->
    <rect x="100" y="60" width="35" height="18" fill="#0f172a" stroke="#94a3b8"/><text x="117" y="73" fill="#38bdf8" font-size="8" font-weight="bold" text-anchor="middle">R100</text>

    <!-- Logic Pins: VCC, GND, SCL, SDA -->
    <g transform="translate(20, 110)">
      <circle cx="15" cy="15" r="5.5" fill="#ea580c" stroke="#fed7aa" stroke-width="1.5"/><text class="pin-text" x="15" y="32" fill="#fed7aa" text-anchor="middle">VCC</text>
      <circle cx="55" cy="15" r="5.5" fill="#047857" stroke="#a7f3d0" stroke-width="1.5"/><text class="pin-text" x="55" y="32" fill="#a7f3d0" text-anchor="middle">GND</text>
      <circle cx="95" cy="15" r="5.5" fill="#0284c7" stroke="#bae6fd" stroke-width="1.5"/><text class="pin-text" x="95" y="32" fill="#bae6fd" text-anchor="middle">SCL</text>
      <circle cx="135" cy="15" r="5.5" fill="#2563eb" stroke="#93c5fd" stroke-width="1.5"/><text class="pin-text" x="135" y="32" fill="#93c5fd" text-anchor="middle">SDA</text>
    </g>
  </g>

  <!-- INA219 #2: 5V Rail (0x41) -->
  <g id="mod-ina2" transform="translate(1420, 240)" filter="url(#module-shadow)">
    <rect width="260" height="150" rx="8" fill="#581c87" stroke="#7e22ce" stroke-width="2"/>
    <text class="board-title" x="130" y="24" text-anchor="middle">INA219 #2 (ADDR: 0x41)</text>
    <text x="130" y="38" fill="#d8b4fe" font-size="9" font-weight="600" text-anchor="middle">Native 5V Rail Monitor</text>
    
    <rect x="20" y="55" width="60" height="38" rx="3" fill="#15803d" stroke="#166534"/>
    <circle cx="35" cy="74" r="7" fill="#dc2626" stroke="#fca5a5" stroke-width="1.5"/>
    <text class="pin-text" x="35" y="88" fill="#fca5a5" text-anchor="middle">VIN+</text>
    <circle cx="65" cy="74" r="5" fill="#475569"/><text x="65" y="88" fill="#cbd5e1" font-size="7" text-anchor="middle">(Open)</text>

    <rect x="100" y="60" width="35" height="18" fill="#0f172a" stroke="#94a3b8"/><text x="117" y="73" fill="#38bdf8" font-size="8" font-weight="bold" text-anchor="middle">R100</text>

    <g transform="translate(20, 110)">
      <circle cx="15" cy="15" r="5.5" fill="#ea580c" stroke="#fed7aa" stroke-width="1.5"/><text class="pin-text" x="15" y="32" fill="#fed7aa" text-anchor="middle">VCC</text>
      <circle cx="55" cy="15" r="5.5" fill="#047857" stroke="#a7f3d0" stroke-width="1.5"/><text class="pin-text" x="55" y="32" fill="#a7f3d0" text-anchor="middle">GND</text>
      <circle cx="95" cy="15" r="5.5" fill="#0284c7" stroke="#bae6fd" stroke-width="1.5"/><text class="pin-text" x="95" y="32" fill="#bae6fd" text-anchor="middle">SCL</text>
      <circle cx="135" cy="15" r="5.5" fill="#2563eb" stroke="#93c5fd" stroke-width="1.5"/><text class="pin-text" x="135" y="32" fill="#93c5fd" text-anchor="middle">SDA</text>
    </g>
  </g>

  <!-- INA219 #3: 3.3V Rail (0x44) -->
  <g id="mod-ina3" transform="translate(1420, 420)" filter="url(#module-shadow)">
    <rect width="260" height="150" rx="8" fill="#581c87" stroke="#7e22ce" stroke-width="2"/>
    <text class="board-title" x="130" y="24" text-anchor="middle">INA219 #3 (ADDR: 0x44)</text>
    <text x="130" y="38" fill="#d8b4fe" font-size="9" font-weight="600" text-anchor="middle">Native 3.3V Rail Monitor</text>
    
    <rect x="20" y="55" width="60" height="38" rx="3" fill="#15803d" stroke="#166534"/>
    <circle cx="35" cy="74" r="7" fill="#ea580c" stroke="#fed7aa" stroke-width="1.5"/>
    <text class="pin-text" x="35" y="88" fill="#fed7aa" text-anchor="middle">VIN+</text>
    <circle cx="65" cy="74" r="5" fill="#475569"/><text x="65" y="88" fill="#cbd5e1" font-size="7" text-anchor="middle">(Open)</text>

    <rect x="100" y="60" width="35" height="18" fill="#0f172a" stroke="#94a3b8"/><text x="117" y="73" fill="#38bdf8" font-size="8" font-weight="bold" text-anchor="middle">R100</text>

    <g transform="translate(20, 110)">
      <circle cx="15" cy="15" r="5.5" fill="#ea580c" stroke="#fed7aa" stroke-width="1.5"/><text class="pin-text" x="15" y="32" fill="#fed7aa" text-anchor="middle">VCC</text>
      <circle cx="55" cy="15" r="5.5" fill="#047857" stroke="#a7f3d0" stroke-width="1.5"/><text class="pin-text" x="55" y="32" fill="#a7f3d0" text-anchor="middle">GND</text>
      <circle cx="95" cy="15" r="5.5" fill="#0284c7" stroke="#bae6fd" stroke-width="1.5"/><text class="pin-text" x="95" y="32" fill="#bae6fd" text-anchor="middle">SCL</text>
      <circle cx="135" cy="15" r="5.5" fill="#2563eb" stroke="#93c5fd" stroke-width="1.5"/><text class="pin-text" x="135" y="32" fill="#93c5fd" text-anchor="middle">SDA</text>
    </g>
  </g>


  <!-- ===================================================================== -->
  <!-- 4. 16x2 LCD DISPLAY WITH I2C BACKPACK (Bottom Right)                  -->
  <!-- ===================================================================== -->
  <g id="mod-lcd" transform="translate(1360, 620)" filter="url(#module-shadow)">
    <rect width="380" height="200" rx="8" fill="#14532d" stroke="#166534" stroke-width="2"/>
    <rect x="30" y="25" width="320" height="110" rx="4" fill="#0284c7" stroke="#0369a1" stroke-width="2"/>
    
    <!-- LCD Text -->
    <text x="50" y="65" fill="#f0f9ff" font-family="'SF Mono', Consolas, monospace" font-size="16" font-weight="bold" letter-spacing="1">
      T1:48.6C  T2:29.4C
    </text>
    <text x="50" y="105" fill="#f0f9ff" font-family="'SF Mono', Consolas, monospace" font-size="16" font-weight="bold" letter-spacing="1">
      Main:ACT [NORMAL]
    </text>

    <!-- I2C Backpack on rear (4 Pins) -->
    <g transform="translate(100, 150)">
      <rect width="180" height="35" rx="3" fill="#0f172a" stroke="#475569"/>
      
      <circle cx="25" cy="18" r="6" fill="#047857" stroke="#a7f3d0" stroke-width="1.5"/>
      <text class="pin-text" x="25" y="32" fill="#a7f3d0" text-anchor="middle">GND</text>

      <circle cx="65" cy="18" r="6" fill="#dc2626" stroke="#fca5a5" stroke-width="1.5"/>
      <text class="pin-text" x="65" y="32" fill="#fca5a5" text-anchor="middle">VCC</text>

      <circle cx="110" cy="18" r="6" fill="#2563eb" stroke="#93c5fd" stroke-width="1.5"/>
      <text class="pin-text" x="110" y="32" fill="#93c5fd" text-anchor="middle">SDA</text>

      <circle cx="155" cy="18" r="6" fill="#0284c7" stroke="#bae6fd" stroke-width="1.5"/>
      <text class="pin-text" x="155" y="32" fill="#bae6fd" text-anchor="middle">SCL</text>
    </g>
  </g>


  <!-- ===================================================================== -->
  <!-- 5. TB6612FNG MOTOR DRIVER & 12V FAN (Bottom Left)                     -->
  <!-- ===================================================================== -->
  <g id="mod-tb6612" transform="translate(60, 360)" filter="url(#module-shadow)">
    <rect width="250" height="230" rx="8" fill="#991b1b" stroke="#b91c1c" stroke-width="2"/>
    <text class="board-title" x="125" y="24" text-anchor="middle">TB6612FNG DRIVER</text>
    <text x="125" y="38" fill="#fca5a5" font-size="8.5" font-weight="600" text-anchor="middle">12V Fan PWM Modulation</text>

    <rect x="85" y="70" width="80" height="45" rx="2" fill="#1e293b" stroke="#475569"/>
    <text x="125" y="96" fill="#f8fafc" font-size="9" font-weight="bold" text-anchor="middle">TB6612</text>

    <!-- Left Pins (Power & Output) -->
    <g transform="translate(15, 55)">
      <circle cx="10" cy="15" r="5.5" fill="#ca8a04" stroke="#fef08a" stroke-width="1.5"/><text class="pin-text" x="22" y="19" fill="#fef08a">VM (12V)</text>
      <circle cx="10" cy="45" r="5.5" fill="#ea580c" stroke="#fed7aa" stroke-width="1.5"/><text class="pin-text" x="22" y="49" fill="#fed7aa">VCC (3.3V)</text>
      <circle cx="10" cy="75" r="5.5" fill="#047857" stroke="#a7f3d0" stroke-width="1.5"/><text class="pin-text" x="22" y="79" fill="#a7f3d0">GND</text>
      <circle cx="10" cy="115" r="5.5" fill="#dc2626" stroke="#fca5a5" stroke-width="1.5"/><text class="pin-text" x="22" y="119" fill="#fca5a5">AO1 [FAN+]</text>
      <circle cx="10" cy="145" r="5.5" fill="#0f172a" stroke="#cbd5e1" stroke-width="1.5"/><text class="pin-text" x="22" y="149" fill="#cbd5e1">AO2 [FAN-]</text>
    </g>

    <!-- Right Pins (Control) -->
    <g transform="translate(160, 55)">
      <circle cx="75" cy="15" r="5.5" fill="#a855f7" stroke="#e9d5ff" stroke-width="1.5"/><text class="pin-text" x="62" y="19" fill="#e9d5ff" text-anchor="end">PWMA</text>
      <circle cx="75" cy="45" r="5.5" fill="#ec4899" stroke="#fbcfe8" stroke-width="1.5"/><text class="pin-text" x="62" y="49" fill="#fbcfe8" text-anchor="end">AIN1</text>
      <circle cx="75" cy="75" r="5.5" fill="#047857" stroke="#a7f3d0" stroke-width="1.5"/><text class="pin-text" x="62" y="79" fill="#a7f3d0" text-anchor="end">AIN2 [GND]</text>
      <circle cx="75" cy="115" r="5.5" fill="#38bdf8" stroke="#bae6fd" stroke-width="1.5"/><text class="pin-text" x="62" y="119" fill="#bae6fd" text-anchor="end">STBY</text>
    </g>
  </g>

  <!-- 12V Cooling Fan -->
  <g id="mod-fan" transform="translate(60, 650)" filter="url(#module-shadow)">
    <rect width="180" height="180" rx="10" fill="#0f172a" stroke="#334155" stroke-width="2"/>
    <circle cx="90" cy="90" r="75" fill="#1e293b"/>
    <circle cx="90" cy="90" r="25" fill="#334155"/>
    <text x="90" y="94" fill="#f8fafc" font-size="9" font-weight="bold" text-anchor="middle">12V DC FAN</text>
    <!-- Leads -->
    <circle cx="145" cy="15" r="6" fill="#dc2626" stroke="#fca5a5" stroke-width="1.5"/>
    <text class="pin-text" x="145" y="35" fill="#fca5a5" text-anchor="middle">RED</text>
    <circle cx="165" cy="15" r="6" fill="#0f172a" stroke="#cbd5e1" stroke-width="1.5"/>
    <text class="pin-text" x="165" y="35" fill="#cbd5e1" text-anchor="middle">BLK</text>
  </g>


  <!-- ===================================================================== -->
  <!-- 6. DUAL DS18B20 PROBES (Bottom Center)                                -->
  <!-- ===================================================================== -->
  <g id="mod-probes" transform="translate(560, 920)" filter="url(#module-shadow)">
    <rect width="320" height="140" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
    <text x="160" y="22" fill="#0f172a" font-size="11" font-weight="bold" text-anchor="middle">DS18B20 1-WIRE TEMPERATURE PROBES</text>

    <!-- Probe 1 Capsule -->
    <g transform="translate(20, 35)">
      <rect width="80" height="26" rx="4" fill="url(#shield-grad)" stroke="#64748b"/>
      <text x="40" y="16" fill="#0f172a" font-size="8" font-weight="bold" text-anchor="middle">PROBE 1 (CORE)</text>
      <!-- 3 Pins -->
      <circle cx="95" cy="8" r="4.5" fill="#ea580c"/>
      <circle cx="95" cy="15" r="4.5" fill="#eab308"/>
      <circle cx="95" cy="22" r="4.5" fill="#047857"/>
    </g>

    <!-- Probe 2 Capsule -->
    <g transform="translate(20, 75)">
      <rect width="80" height="26" rx="4" fill="url(#shield-grad)" stroke="#64748b"/>
      <text x="40" y="16" fill="#0f172a" font-size="8" font-weight="bold" text-anchor="middle">PROBE 2 (INLET)</text>
      <circle cx="95" cy="8" r="4.5" fill="#ea580c"/>
      <circle cx="95" cy="15" r="4.5" fill="#eab308"/>
      <circle cx="95" cy="22" r="4.5" fill="#047857"/>
    </g>

    <!-- 4.7k Pullup Resistor -->
    <g transform="translate(190, 48)">
      <rect width="45" height="20" rx="4" fill="#d97706" stroke="#b45309"/>
      <rect x="8" y="0" width="4" height="20" fill="#facc15"/>
      <rect x="15" y="0" width="4" height="20" fill="#7c3aed"/>
      <rect x="22" y="0" width="4" height="20" fill="#dc2626"/>
      <rect x="32" y="0" width="3" height="20" fill="#ca8a04"/>
      <text x="22" y="34" fill="#78350f" font-size="9" font-weight="bold" text-anchor="middle">4.7 kΩ</text>
    </g>

    <text class="pin-text" x="145" y="125" fill="#ea580c">VDD</text>
    <text class="pin-text" x="195" y="125" fill="#ca8a04">DQ (Data)</text>
    <text class="pin-text" x="260" y="125" fill="#047857">GND</text>
  </g>


  <!-- ===================================================================== -->
  <!-- 7. BC547 TRANSISTOR SWITCH (Between ATX and ESP32)                    -->
  <!-- ===================================================================== -->
  <g id="mod-bc547" transform="translate(390, 310)" filter="url(#module-shadow)">
    <rect width="130" height="130" rx="6" fill="#ffffff" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="3"/>
    <text x="65" y="18" fill="#0f172a" font-size="9" font-weight="bold" text-anchor="middle">BC547 SWITCH</text>

    <!-- Transistor Shape -->
    <path d="M 50 65 C 50 45 80 45 80 65 Z" fill="#18181b"/>
    <rect x="50" y="65" width="30" height="5" fill="#18181b"/>
    <text x="65" y="58" fill="#f8fafc" font-size="7" font-weight="bold" text-anchor="middle">BC547</text>

    <!-- Pins -->
    <circle cx="65" cy="35" r="5" fill="#10b981"/><text class="pin-text" x="75" y="38" fill="#047857">C</text>
    <circle cx="35" cy="65" r="5" fill="#38bdf8"/><text class="pin-text" x="25" y="68" fill="#0284c7">B</text>
    <circle cx="65" cy="95" r="5" fill="#047857"/><text class="pin-text" x="75" y="98" fill="#047857">E</text>
  </g>


  <!-- ===================================================================== -->
  <!-- 8. HUMAN-ENGINEERED BUS WIRING SYSTEM                                 -->
  <!-- Clean orthogonal corridors with Common Ground & Power Rails           -->
  <!-- ===================================================================== -->

  <!-- ==================== BUS 1: COMMON GROUND (GREEN #047857) ==================== -->
  <!-- Main Ground Trunk corridor: x = 500, with horizontal branches -->
  <g id="wires-gnd">
    <!-- ATX GND (335, 260) -> Main Ground Bus -->
    <path class="wire wire-gnd" d="M 335 260 L 500 260 L 500 120 L 1380 120 L 1380 170 L 1475 170"/>
    <circle cx="500" cy="260" r="4.5" fill="#047857" class="junction"/>

    <!-- Tap to BC547 Emitter (455, 405) -->
    <path class="wire wire-gnd" d="M 455 405 L 500 405"/>
    <circle cx="500" cy="405" r="4" fill="#047857" class="junction"/>

    <!-- Tap to ESP32 GND (576, 756) -->
    <path class="wire wire-gnd" d="M 500 756 L 576 756"/>
    <circle cx="500" cy="756" r="4.5" fill="#047857" class="junction"/>

    <!-- Tap to TB6612 GND (85, 435) & AIN2 (250, 435) -->
    <path class="wire wire-gnd" d="M 500 490 L 50 490 L 50 435 L 85 435"/>
    <path class="wire wire-gnd" d="M 50 490 L 250 490 L 250 435"/>
    <circle cx="500" cy="490" r="4" fill="#047857" class="junction"/>

    <!-- Tap to DS18B20 GND (840, 942) -->
    <path class="wire wire-gnd" d="M 500 756 L 500 1100 L 840 1100 L 840 942"/>
    <circle cx="500" cy="1100" r="4" fill="#047857" class="junction"/>

    <!-- Right Side Ground Bus running vertically along x = 1380 to INA #2, #3, LCD -->
    <path class="wire wire-gnd" d="M 1380 170 L 1380 350 L 1475 350"/>
    <circle cx="1380" cy="170" r="4" fill="#047857" class="junction"/>
    <path class="wire wire-gnd" d="M 1380 350 L 1380 530 L 1475 530"/>
    <circle cx="1380" cy="350" r="4" fill="#047857" class="junction"/>
    <path class="wire wire-gnd" d="M 1380 530 L 1380 770 L 1485 770"/>
    <circle cx="1380" cy="530" r="4" fill="#047857" class="junction"/>
  </g>

  <!-- ==================== BUS 2: 3.3V LOGIC POWER (ORANGE #ea580c) ==================== -->
  <g id="wires-3v3">
    <!-- ESP32 3V3 (576, 340) -> Logic Bus -->
    <path class="wire wire-3v3" d="M 576 340 L 530 340 L 530 200 L 1340 200 L 1340 170 L 1435 170"/>

    <!-- Tap to TB6612 VCC (85, 405) -->
    <path class="wire wire-3v3" d="M 530 340 L 530 405 L 85 405"/>
    <circle cx="530" cy="340" r="4" fill="#ea580c" class="junction"/>

    <!-- Tap to DS18B20 VDD & 4.7k Pullup (655, 942) -->
    <path class="wire wire-3v3" d="M 530 405 L 530 1080 L 760 1080 L 760 968"/>
    <circle cx="530" cy="405" r="4" fill="#ea580c" class="junction"/>

    <!-- Right Side 3.3V Bus running down x = 1340 to INA #2, #3 -->
    <path class="wire wire-3v3" d="M 1340 200 L 1340 350 L 1435 350"/>
    <circle cx="1340" cy="200" r="4" fill="#ea580c" class="junction"/>
    <path class="wire wire-3v3" d="M 1340 350 L 1340 530 L 1435 530"/>
    <circle cx="1340" cy="350" r="4" fill="#ea580c" class="junction"/>
  </g>

  <!-- ==================== BUS 3: I2C COMMUNICATION (SDA = BLUE, SCL = CYAN) ==================== -->
  <!-- SDA: GPIO 21 (794, 468) | SCL: GPIO 22 (794, 372) -->
  <g id="wires-i2c">
    <!-- I2C SDA (GPIO 21) -->
    <path class="wire wire-sda" d="M 794 468 L 1260 468 L 1260 170 L 1555 170"/>
    <path class="wire wire-sda" d="M 1260 350 L 1555 350"/>
    <circle cx="1260" cy="350" r="4" fill="#2563eb" class="junction"/>
    <path class="wire wire-sda" d="M 1260 468 L 1260 530 L 1555 530"/>
    <circle cx="1260" cy="468" r="4" fill="#2563eb" class="junction"/>
    <path class="wire wire-sda" d="M 1260 530 L 1260 770 L 1570 770"/>
    <circle cx="1260" cy="530" r="4" fill="#2563eb" class="junction"/>

    <!-- I2C SCL (GPIO 22) -->
    <path class="wire wire-scl" d="M 794 372 L 1220 372 L 1220 170 L 1515 170"/>
    <path class="wire wire-scl" d="M 1220 350 L 1515 350"/>
    <circle cx="1220" cy="350" r="4" fill="#0284c7" class="junction"/>
    <path class="wire wire-scl" d="M 1220 372 L 1220 530 L 1515 530"/>
    <circle cx="1220" cy="372" r="4" fill="#0284c7" class="junction"/>
    <path class="wire wire-scl" d="M 1220 530 L 1220 770 L 1615 770"/>
    <circle cx="1220" cy="530" r="4" fill="#0284c7" class="junction"/>
  </g>

  <!-- ==================== BUS 4: STANDBY POWER & CONTROL ==================== -->
  <g id="wires-control">
    <!-- ATX +5VSB (200, 252) -> ESP32 5V/VIN (794, 788) -->
    <path class="wire" stroke="#a855f7" stroke-width="3.5"
          d="M 200 252 L 200 280 L 350 280 L 350 820 L 820 820 L 820 788 L 794 788"/>

    <!-- LCD 5V Power (Taps off 5V Infeed line to LCD VCC) -->
    <path class="wire wire-5v" d="M 820 820 L 1525 820 L 1525 770"/>
    <circle cx="820" cy="820" r="4" fill="#dc2626" class="junction"/>

    <!-- ATX PS_ON# (240, 252) -> BC547 Collector (455, 345) -->
    <path class="wire" stroke="#10b981" stroke-width="3.5"
          d="M 240 252 L 240 345 L 455 345"/>

    <!-- ESP32 GPIO 32 (576, 532) -> BC547 Base (425, 375) -->
    <path class="wire" stroke="#059669" stroke-width="3"
          d="M 576 532 L 425 532 L 425 375"/>
  </g>

  <!-- ==================== BUS 5: HIGH-CURRENT DC RAILS ==================== -->
  <g id="wires-dc-rails">
    <!-- ATX +12V (335, 125) -> INA219 #1 VIN+ (1455, 134) -->
    <path class="wire wire-12v" d="M 335 125 L 1400 125 L 1400 134 L 1455 134"/>

    <!-- ATX +12V Branch -> TB6612 VM Pin (85, 375) -->
    <path class="wire wire-12v" d="M 350 125 L 350 375 L 85 375"/>
    <circle cx="350" cy="125" r="4" fill="#ca8a04" class="junction"/>

    <!-- ATX +5V (335, 170) -> INA219 #2 VIN+ (1455, 314) -->
    <path class="wire wire-5v" d="M 335 170 L 370 170 L 370 230 L 1400 230 L 1400 314 L 1455 314"/>

    <!-- ATX +3.3V (335, 215) -> INA219 #3 VIN+ (1455, 494) -->
    <path class="wire wire-3v3" d="M 335 215 L 360 215 L 360 410 L 1400 410 L 1400 494 L 1455 494"/>
  </g>

  <!-- ==================== BUS 6: FAN & TEMPERATURE SENSORS ==================== -->
  <g id="wires-peripherals">
    <!-- TB6612 Control from ESP32: -->
    <!-- PWMA: GPIO 25 (576, 596) -> TB6612 PWMA (245, 375) -->
    <path class="wire" stroke="#a855f7" stroke-width="3"
          d="M 576 596 L 280 596 L 280 375 L 245 375"/>

    <!-- AIN1: GPIO 26 (576, 628) -> TB6612 AIN1 (245, 405) -->
    <path class="wire" stroke="#ec4899" stroke-width="3"
          d="M 576 628 L 295 628 L 295 405 L 245 405"/>

    <!-- STBY: GPIO 33 (576, 564) -> TB6612 STBY (245, 475) -->
    <path class="wire" stroke="#38bdf8" stroke-width="3"
          d="M 576 564 L 310 564 L 310 475 L 245 475"/>

    <!-- Fan Drive: AO1 & AO2 to Fan Red & Black -->
    <path class="wire wire-5v" d="M 85 475 L 40 475 L 40 665 L 205 665"/>
    <path class="wire" stroke="#0f172a" stroke-width="3" d="M 85 505 L 30 505 L 30 680 L 225 680"/>

    <!-- DS18B20 1-Wire DQ: GPIO 27 (576, 660) -> Probes DQ (655, 957) -->
    <path class="wire" stroke="#eab308" stroke-width="3.5"
          d="M 576 660 L 510 660 L 510 990 L 755 990 L 755 957"/>
  </g>


  <!-- ===================================================================== -->
  <!-- 9. CLEAN ENGINEERING LEGEND (Bottom Center)                           -->
  <!-- ===================================================================== -->
  <g id="legend" transform="translate(950, 940)" filter="url(#module-shadow)">
    <rect width="780" height="150" rx="6" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
    <rect width="780" height="28" rx="6" fill="#f8fafc"/>
    <text x="390" y="19" fill="#0f172a" font-size="11" font-weight="700" text-anchor="middle">
      CIRCUIT SCHEMATIC BUS LEGEND (HUMAN-ENGINEERED TRUNK ROUTING)
    </text>

    <g transform="translate(25, 45)" font-size="11" font-weight="700">
      <!-- Col 1 -->
      <line x1="0" y1="12" x2="35" y2="12" stroke="#047857" stroke-width="4"/>
      <text x="45" y="16" fill="#047857">Common Ground Bus (GND / COM)</text>

      <line x1="0" y1="38" x2="35" y2="38" stroke="#ea580c" stroke-width="4"/>
      <text x="45" y="42" fill="#ea580c">3.3V Logic Bus (ESP32 3V3)</text>

      <line x1="0" y1="64" x2="35" y2="64" stroke="#a855f7" stroke-width="4"/>
      <text x="45" y="68" fill="#7e22ce">+5VSB Standby Uninterrupted Infeed</text>

      <line x1="0" y1="90" x2="35" y2="90" stroke="#ca8a04" stroke-width="4"/>
      <text x="45" y="94" fill="#854d0e">+12V Main DC Power Rail</text>

      <!-- Col 2 -->
      <g transform="translate(380, 0)">
        <line x1="0" y1="12" x2="35" y2="12" stroke="#2563eb" stroke-width="4"/>
        <text x="45" y="16" fill="#1d4ed8">I2C SDA Serial Data (GPIO 21)</text>

        <line x1="0" y1="38" x2="35" y2="38" stroke="#0284c7" stroke-width="4"/>
        <text x="45" y="42" fill="#0284c7">I2C SCL Serial Clock (GPIO 22)</text>

        <line x1="0" y1="64" x2="35" y2="64" stroke="#10b981" stroke-width="4"/>
        <text x="45" y="68" fill="#047857">PS_ON# Supervisory Trip Line</text>

        <line x1="0" y1="90" x2="35" y2="90" stroke="#eab308" stroke-width="4"/>
        <text x="45" y="94" fill="#a16207">1-Wire DQ Temperature Bus (GPIO 27)</text>
      </g>
    </g>
  </g>

</svg>'''

    output_path = os.path.join("documentation", "transformer_cbm_circuit_diagram.svg")
    ET.fromstring(svg) # validate XML
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print("Clean schematic written successfully.")

if __name__ == "__main__":
    generate_clean_schematic()
