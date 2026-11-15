# -*- coding: utf-8 -*-
"""
Diagram 2: Software & Cloud Architecture Block Diagram
Textbook Academic Engineering Style:
- Strict 2-domain color composition:
  * Firmware domain: Soft Mint Green (#dcfce7 fill, #16a34a stroke, #14532d text)
  * Cloud domain: Soft Sky Blue (#e0f2fe fill, #0284c7 stroke, #0369a1 text)
- Strictly NO text over arrows: clean, unobstructed lines with sharp arrowheads
- Reduced, punchy text: 1-2 lines per card, 2-3 words max, large legible font
- Clean layout with zero wire overlaps
"""

import os
import subprocess

def generate():
    w = 1600
    h = 950

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <defs>
    <filter id="shadow" x="-4%" y="-4%" width="108%" height="110%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="1" dy="2" stdDeviation="2" flood-color="#0f172a" flood-opacity="0.08"/>
    </filter>
    <marker id="arrow-green" viewBox="0 0 12 12" refX="10" refY="6" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M 1 2 L 11 6 L 1 10 z" fill="#15803d"/>
    </marker>
    <marker id="arrow-blue" viewBox="0 0 12 12" refX="10" refY="6" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M 1 2 L 11 6 L 1 10 z" fill="#0284c7"/>
    </marker>
    <marker id="arrow-dark" viewBox="0 0 12 12" refX="10" refY="6" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M 1 2 L 11 6 L 1 10 z" fill="#1e293b"/>
    </marker>
  </defs>

  <style>
    text {{
      font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
      text-anchor: middle;
      dominant-baseline: central;
    }}
    .wire-green {{
      fill: none;
      stroke: #16a34a;
      stroke-width: 2.5;
      stroke-linecap: round;
      stroke-linejoin: round;
    }}
    .wire-blue {{
      fill: none;
      stroke: #0284c7;
      stroke-width: 2.5;
      stroke-linecap: round;
      stroke-linejoin: round;
    }}
    .wire-bridge {{
      fill: none;
      stroke: #0284c7;
      stroke-width: 3;
      stroke-linecap: round;
      stroke-linejoin: round;
    }}
    .title-main {{
      font-size: 28px;
      font-weight: 800;
      fill: #0f172a;
      letter-spacing: 0.5px;
    }}
    .title-sub {{
      font-size: 15px;
      font-weight: 500;
      fill: #64748b;
    }}
    .container-title-green {{
      font-size: 16px;
      font-weight: 800;
      fill: #166534;
      text-anchor: start;
      letter-spacing: 0.5px;
    }}
    .container-title-blue {{
      font-size: 16px;
      font-weight: 800;
      fill: #1e40af;
      text-anchor: start;
      letter-spacing: 0.5px;
    }}
    .card-title-green {{
      font-size: 21px;
      font-weight: 700;
      fill: #14532d;
    }}
    .card-sub-green {{
      font-size: 14.5px;
      font-weight: 500;
      fill: #15803d;
    }}
    .card-title-blue {{
      font-size: 21px;
      font-weight: 700;
      fill: #0369a1;
    }}
    .card-sub-blue {{
      font-size: 14.5px;
      font-weight: 500;
      fill: #0284c7;
    }}
  </style>

  <!-- Background -->
  <rect width="{w}" height="{h}" fill="#ffffff"/>

  <!-- Main Header -->
  <text x="{w/2}" y="45" class="title-main">SOFTWARE &amp; CLOUD ARCHITECTURE BLOCK DIAGRAM</text>
  <text x="{w/2}" y="75" class="title-sub">Embedded FreeRTOS Core, Cloud Pipeline &amp; Edge Supervision</text>


  <!-- ==================== LEFT CONTAINER: EMBEDDED FIRMWARE ==================== -->
  <rect x="60" y="110" width="700" height="780" rx="16" fill="#f0fdf4" stroke="#86efac" stroke-width="1.5"/>
  <text x="90" y="140" class="container-title-green">ESP32 EMBEDDED FIRMWARE (FreeRTOS)</text>

  <!-- FW 1: Sensor Acquisition -->
  <!-- Box: 260 x 100 at (100, 180) -->
  <g transform="translate(100, 180)" filter="url(#shadow)">
    <rect width="260" height="100" rx="12" fill="#dcfce7" stroke="#16a34a" stroke-width="2"/>
    <text x="130" y="38" class="card-title-green">Sensor Acquisition</text>
    <text x="130" y="66" class="card-sub-green">1-Wire &amp; I2C Drivers</text>
  </g>

  <!-- FW 2: Thermal Predictor -->
  <!-- Box: 260 x 100 at (100, 340) -->
  <g transform="translate(100, 340)" filter="url(#shadow)">
    <rect width="260" height="100" rx="12" fill="#dcfce7" stroke="#16a34a" stroke-width="2"/>
    <text x="130" y="38" class="card-title-green">Thermal Model</text>
    <text x="130" y="66" class="card-sub-green">EMA &amp; Projection</text>
  </g>
  <!-- Wire: Acquisition bottom (230, 280) -> Thermal top (230, 340) -->
  <path class="wire-green" marker-end="url(#arrow-green)" d="M 230 280 L 230 340"/>

  <!-- FW 3: Supervisory State Machine -->
  <!-- Box: 260 x 110 at (100, 500) -->
  <g transform="translate(100, 500)" filter="url(#shadow)">
    <rect width="260" height="110" rx="12" fill="#dcfce7" stroke="#16a34a" stroke-width="2.5"/>
    <text x="130" y="42" class="card-title-green">Safety Machine</text>
    <text x="130" y="72" class="card-sub-green">10-State Supervisory</text>
  </g>
  <!-- Wire: Thermal bottom (230, 440) -> Safety top (230, 500) -->
  <path class="wire-green" marker-end="url(#arrow-green)" d="M 230 440 L 230 500"/>

  <!-- FW 4: Fan Control (Col 1, Row 4) -->
  <!-- Box: 260 x 100 at (100, 680) -->
  <g transform="translate(100, 680)" filter="url(#shadow)">
    <rect width="260" height="100" rx="12" fill="#dcfce7" stroke="#16a34a" stroke-width="2"/>
    <text x="130" y="38" class="card-title-green">Fan Control</text>
    <text x="130" y="66" class="card-sub-green">PWM Modulation</text>
  </g>
  <!-- Wire: Safety bottom (230, 610) -> Fan Control top (230, 680) -->
  <path class="wire-green" marker-end="url(#arrow-green)" d="M 230 610 L 230 680"/>

  <!-- FW 5: Local Web UI (Col 2, Row 3) -->
  <!-- Box: 260 x 100 at (460, 505) -->
  <g transform="translate(460, 505)" filter="url(#shadow)">
    <rect width="260" height="100" rx="12" fill="#dcfce7" stroke="#16a34a" stroke-width="2"/>
    <text x="130" y="38" class="card-title-green">Local Web UI</text>
    <text x="130" y="66" class="card-sub-green">LittleFS Dashboard</text>
  </g>
  <!-- Wire: Safety right (360, 555) -> Local Web UI left (460, 555) -->
  <path class="wire-green" marker-end="url(#arrow-green)" d="M 360 555 L 460 555"/>

  <!-- FW 6: Cloud Dispatcher (Col 2, Row 2) -->
  <!-- Box: 260 x 100 at (460, 340) -->
  <g transform="translate(460, 340)" filter="url(#shadow)">
    <rect width="260" height="100" rx="12" fill="#dcfce7" stroke="#16a34a" stroke-width="2"/>
    <text x="130" y="38" class="card-title-green">Cloud Dispatcher</text>
    <text x="130" y="66" class="card-sub-green">HTTPS Client</text>
  </g>
  <!-- Wire: Safety right (360, 530) -> up -> Cloud Dispatcher bottom (590, 440) -->
  <path class="wire-green" marker-end="url(#arrow-green)" d="M 360 530 L 410 530 L 410 470 L 590 470 L 590 440"/>


  <!-- ==================== BRIDGE: FIRMWARE TO CLOUD ==================== -->
  <!-- Wire: Cloud Dispatcher right (720, 390) -> Cloud Database left (880, 390) -->
  <path class="wire-bridge" marker-end="url(#arrow-blue)" d="M 720 390 L 880 390"/>


  <!-- ==================== RIGHT CONTAINER: CLOUD & SUPERVISION ==================== -->
  <rect x="840" y="110" width="700" height="780" rx="16" fill="#f0f7ff" stroke="#93c5fd" stroke-width="1.5"/>
  <text x="870" y="140" class="container-title-blue">FIREBASE CLOUD &amp; SERVERLESS EDGE</text>

  <!-- Cloud 1: Cloud Database (Col 1, Row 2) -->
  <!-- Box: 260 x 110 at (880, 335) -->
  <g transform="translate(880, 335)" filter="url(#shadow)">
    <rect width="260" height="110" rx="12" fill="#e0f2fe" stroke="#0284c7" stroke-width="2.5"/>
    <text x="130" y="42" class="card-title-blue">Cloud Database</text>
    <text x="130" y="72" class="card-sub-blue">Firebase RTDB</text>
  </g>

  <!-- Cloud 2: Web Dashboard (Col 2, Row 2) -->
  <!-- Box: 260 x 100 at (1240, 340) -->
  <g transform="translate(1240, 340)" filter="url(#shadow)">
    <rect width="260" height="100" rx="12" fill="#e0f2fe" stroke="#0284c7" stroke-width="2"/>
    <text x="130" y="38" class="card-title-blue">Web Dashboard</text>
    <text x="130" y="66" class="card-sub-blue">Firebase Hosting</text>
  </g>
  <!-- Wire: Cloud Database right (1140, 390) -> Web Dashboard left (1240, 390) -->
  <path class="wire-blue" marker-end="url(#arrow-blue)" d="M 1140 390 L 1240 390"/>

  <!-- Cloud 3: Watchdog Worker (Col 1, Row 3) -->
  <!-- Box: 260 x 100 at (880, 520) -->
  <g transform="translate(880, 520)" filter="url(#shadow)">
    <rect width="260" height="100" rx="12" fill="#e0f2fe" stroke="#0284c7" stroke-width="2"/>
    <text x="130" y="38" class="card-title-blue">Watchdog Worker</text>
    <text x="130" y="66" class="card-sub-blue">Cloudflare Edge</text>
  </g>
  <!-- Wire: Cloud Database bottom (1010, 445) -> Watchdog top (1010, 520) -->
  <path class="wire-blue" marker-end="url(#arrow-blue)" d="M 1010 445 L 1010 520"/>

  <!-- Cloud 4: Email Service (Col 2, Row 3) -->
  <!-- Box: 260 x 100 at (1240, 520) -->
  <g transform="translate(1240, 520)" filter="url(#shadow)">
    <rect width="260" height="100" rx="12" fill="#e0f2fe" stroke="#0284c7" stroke-width="2"/>
    <text x="130" y="38" class="card-title-blue">Email Service</text>
    <text x="130" y="66" class="card-sub-blue">Brevo REST API</text>
  </g>
  <!-- Wire: Watchdog right (1140, 570) -> Email Service left (1240, 570) -->
  <path class="wire-blue" marker-end="url(#arrow-blue)" d="M 1140 570 L 1240 570"/>

  <!-- Cloud 5: Engineer Alert (Col 2, Row 4) -->
  <!-- Box: 260 x 100 at (1240, 680) -->
  <g transform="translate(1240, 680)" filter="url(#shadow)">
    <rect width="260" height="100" rx="12" fill="#f0f9ff" stroke="#38bdf8" stroke-width="2"/>
    <text x="130" y="38" class="card-title-blue">Engineer Alert</text>
    <text x="130" y="66" class="card-sub-blue">Incident Notification</text>
  </g>
  <!-- Wire: Email Service bottom (1370, 620) -> Engineer Alert top (1370, 680) -->
  <path class="wire-blue" marker-end="url(#arrow-blue)" d="M 1370 620 L 1370 680"/>

</svg>'''

    svg_path = os.path.join("documentation", "diagram_2_software_cloud_block.svg")
    png_path = os.path.join("documentation", "diagram_2_software_cloud_block.png")
    typ_path = os.path.join("documentation", "render_diag2.typ")
    typst_exe = os.path.join("documentation", "bin", "typst.exe")

    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Wrote {svg_path}")

    with open(typ_path, "w", encoding="utf-8") as f:
        f.write(f'#set page(width: {w}pt, height: {h}pt, margin: 0pt)\n#image("diagram_2_software_cloud_block.svg", width: 100%)\n')

    subprocess.run([typst_exe, "compile", "--format", "png", "--ppi", "150", typ_path, png_path], check=True)
    if os.path.exists(typ_path):
        os.remove(typ_path)
    print(f"Compiled {png_path}")

if __name__ == "__main__":
    generate()
