# -*- coding: utf-8 -*-
"""
Diagram 5: Predictive Thermal Algorithm Flowchart
Textbook Academic Engineering Style (Matching User Reference Images 4 & 5):
- Unified, non-AI color palette:
  * Algorithm steps / processes: Soft Sky Blue (#e0f2fe fill, #0284c7 stroke, #0369a1 text)
  * Decision diamonds: Soft Sky Blue (#e0f2fe fill, #0284c7 stroke, #0369a1 text)
  * Emergency trip branch: Soft Coral (#fee2e2 fill, #ef4444 stroke, #991b1b text)
  * Terminator start/stop: Soft Peach (#ffedd5 fill, #f97316 stroke, #c2410c text)
- Strictly NO sentences: concise action titles (2-3 words, large legible font)
- Strictly NO text over arrows except clean 'Yes' and 'No' markers
- Single, beautiful closed-loop vertical flow
"""

import os
import subprocess

def generate():
    w = 1200
    h = 1600

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <defs>
    <filter id="shadow" x="-4%" y="-4%" width="108%" height="110%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="1" dy="2" stdDeviation="2" flood-color="#0f172a" flood-opacity="0.08"/>
    </filter>
    <marker id="arrow" viewBox="0 0 12 12" refX="10" refY="6" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M 1 2 L 11 6 L 1 10 z" fill="#334155"/>
    </marker>
    <marker id="arrow-red" viewBox="0 0 12 12" refX="10" refY="6" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M 1 2 L 11 6 L 1 10 z" fill="#ef4444"/>
    </marker>
  </defs>

  <style>
    text {{
      font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
      text-anchor: middle;
      dominant-baseline: central;
    }}
    .wire {{
      fill: none;
      stroke: #334155;
      stroke-width: 2.5;
      stroke-linecap: round;
      stroke-linejoin: round;
    }}
    .wire-red {{
      fill: none;
      stroke: #ef4444;
      stroke-width: 2.5;
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
    .node-title {{
      font-size: 19px;
      font-weight: 700;
    }}
    .lbl-yes {{
      font-size: 14px;
      font-weight: 700;
      fill: #15803d;
      text-anchor: start;
    }}
    .lbl-no {{
      font-size: 14px;
      font-weight: 700;
      fill: #dc2626;
      text-anchor: start;
    }}
  </style>

  <!-- Background -->
  <rect width="{w}" height="{h}" fill="#ffffff"/>

  <!-- Main Header -->
  <text x="{w/2}" y="40" class="title-main">PREDICTIVE THERMAL ALGORITHM FLOWCHART</text>
  <text x="{w/2}" y="70" class="title-sub">1.00 Hz Real-Time Execution Loop &amp; Closed-Loop Regulation</text>

  <!-- Node 0: START (Oval) at (450, 110) -->
  <g transform="translate(420, 110)" filter="url(#shadow)">
    <rect width="260" height="55" rx="27.5" fill="#ffedd5" stroke="#f97316" stroke-width="2"/>
    <text x="130" y="27.5" class="node-title" fill="#c2410c">Start Execution (1 Hz)</text>
  </g>
  <path class="wire" marker-end="url(#arrow)" d="M 550 165 L 550 205"/>

  <!-- Node 1: Read Sensor Probes (Parallelogram) -->
  <g transform="translate(410, 205)" filter="url(#shadow)">
    <polygon points="30,0 280,0 250,65 0,65" fill="#e0f2fe" stroke="#0284c7" stroke-width="2"/>
    <text x="140" y="32.5" class="node-title" fill="#0369a1">Read Sensor Probes</text>
  </g>
  <path class="wire" marker-end="url(#arrow)" d="M 550 270 L 550 310"/>

  <!-- Node 2: Filter Temperature (Rectangle) -->
  <g transform="translate(410, 310)" filter="url(#shadow)">
    <rect width="280" height="65" rx="10" fill="#e0f2fe" stroke="#0284c7" stroke-width="2"/>
    <text x="140" y="32.5" class="node-title" fill="#0369a1">Compute EMA Filter</text>
  </g>
  <path class="wire" marker-end="url(#arrow)" d="M 550 375 L 550 415"/>

  <!-- Node 3: Calculate Slope (Rectangle) -->
  <g transform="translate(410, 415)" filter="url(#shadow)">
    <rect width="280" height="65" rx="10" fill="#e0f2fe" stroke="#0284c7" stroke-width="2"/>
    <text x="140" y="32.5" class="node-title" fill="#0369a1">Calculate Thermal Rate</text>
  </g>
  <path class="wire" marker-end="url(#arrow)" d="M 550 480 L 550 520"/>

  <!-- Node 4: Predict Ahead (Rectangle) -->
  <g transform="translate(410, 520)" filter="url(#shadow)">
    <rect width="280" height="65" rx="10" fill="#e0f2fe" stroke="#0284c7" stroke-width="2"/>
    <text x="140" y="32.5" class="node-title" fill="#0369a1">Project 30s Temperature</text>
  </g>
  <path class="wire" marker-end="url(#arrow)" d="M 550 585 L 550 625"/>

  <!-- Decision 1: Thermal Breach? (Diamond) at (550, 675) -->
  <g transform="translate(425, 625)" filter="url(#shadow)">
    <polygon points="125,0 250,50 125,100 0,50" fill="#e0f2fe" stroke="#0284c7" stroke-width="2"/>
    <text x="125" y="50" class="node-title" fill="#0369a1">Thermal Breach?</text>
  </g>
  <!-- Decision 1: Yes -> Emergency Trip Branch -->
  <path class="wire-red" marker-end="url(#arrow-red)" d="M 675 675 L 780 675"/>
  <text x="715" y="663" class="lbl-yes">Yes</text>

  <!-- Emergency Cutoff (Rectangle) -->
  <g transform="translate(780, 642.5)" filter="url(#shadow)">
    <rect width="260" height="65" rx="10" fill="#fee2e2" stroke="#ef4444" stroke-width="2"/>
    <text x="130" y="32.5" class="node-title" fill="#991b1b">Cut Power Supply</text>
  </g>
  <path class="wire-red" marker-end="url(#arrow-red)" d="M 910 707.5 L 910 750"/>

  <!-- Alert Dispatch (Parallelogram) -->
  <g transform="translate(770, 750)" filter="url(#shadow)">
    <polygon points="30,0 280,0 250,65 0,65" fill="#fee2e2" stroke="#ef4444" stroke-width="2"/>
    <text x="140" y="32.5" class="node-title" fill="#991b1b">Trigger Alert Email</text>
  </g>

  <!-- Decision 1: No -> Compute Fan Speed -->
  <path class="wire" marker-end="url(#arrow)" d="M 550 725 L 550 765"/>
  <text x="560" y="745" class="lbl-no">No</text>

  <!-- Node 5: Compute Fan Speed (Rectangle) -->
  <g transform="translate(410, 765)" filter="url(#shadow)">
    <rect width="280" height="65" rx="10" fill="#e0f2fe" stroke="#0284c7" stroke-width="2"/>
    <text x="140" y="32.5" class="node-title" fill="#0369a1">Compute Fan Demand</text>
  </g>
  <path class="wire" marker-end="url(#arrow)" d="M 550 830 L 550 870"/>

  <!-- Node 6: Apply Rate Limiter (Rectangle) -->
  <g transform="translate(410, 870)" filter="url(#shadow)">
    <rect width="280" height="65" rx="10" fill="#e0f2fe" stroke="#0284c7" stroke-width="2"/>
    <text x="140" y="32.5" class="node-title" fill="#0369a1">Apply Slew Limiter</text>
  </g>
  <path class="wire" marker-end="url(#arrow)" d="M 550 935 L 550 975"/>

  <!-- Node 7: Update Fan PWM (Rectangle) -->
  <g transform="translate(410, 975)" filter="url(#shadow)">
    <rect width="280" height="65" rx="10" fill="#e0f2fe" stroke="#0284c7" stroke-width="2"/>
    <text x="140" y="32.5" class="node-title" fill="#0369a1">Update Fan PWM</text>
  </g>
  <path class="wire" marker-end="url(#arrow)" d="M 550 1040 L 550 1080"/>

  <!-- Node 8: Update LCD Display (Parallelogram) -->
  <g transform="translate(410, 1080)" filter="url(#shadow)">
    <polygon points="30,0 280,0 250,65 0,65" fill="#e0f2fe" stroke="#0284c7" stroke-width="2"/>
    <text x="140" y="32.5" class="node-title" fill="#0369a1">Display on LCD</text>
  </g>
  <path class="wire" marker-end="url(#arrow)" d="M 550 1145 L 550 1185"/>

  <!-- Decision 2: 10s Timer? (Diamond) at (550, 1235) -->
  <g transform="translate(425, 1185)" filter="url(#shadow)">
    <polygon points="125,0 250,50 125,100 0,50" fill="#e0f2fe" stroke="#0284c7" stroke-width="2"/>
    <text x="125" y="50" class="node-title" fill="#0369a1">10s Cloud Timer?</text>
  </g>
  <!-- Decision 2: Yes -> Publish Telemetry -->
  <path class="wire" marker-end="url(#arrow)" d="M 675 1235 L 780 1235"/>
  <text x="715" y="1223" class="lbl-yes">Yes</text>

  <!-- Upload Telemetry (Parallelogram) -->
  <g transform="translate(770, 1202.5)" filter="url(#shadow)">
    <polygon points="30,0 280,0 250,65 0,65" fill="#e0f2fe" stroke="#0284c7" stroke-width="2"/>
    <text x="140" y="32.5" class="node-title" fill="#0369a1">Publish to Cloud</text>
  </g>
  <!-- Wire from Publish to Wait loop -->
  <path class="wire" d="M 910 1267.5 L 910 1372.5 L 690 1372.5"/>

  <!-- Decision 2: No -> Wait Interval -->
  <path class="wire" marker-end="url(#arrow)" d="M 550 1285 L 550 1340"/>
  <text x="560" y="1305" class="lbl-no">No</text>

  <!-- Node 9: Wait Interval (Rectangle) -->
  <g transform="translate(410, 1340)" filter="url(#shadow)">
    <rect width="280" height="65" rx="10" fill="#e0f2fe" stroke="#0284c7" stroke-width="2"/>
    <text x="140" y="32.5" class="node-title" fill="#0369a1">Wait 1.00s Interval</text>
  </g>

  <!-- Loop back to Read Sensor Probes: Exit left, up to y=237.5, enter Read Sensor Probes left -->
  <path class="wire" marker-end="url(#arrow)"
        d="M 410 1372.5 L 220 1372.5 L 220 237.5 L 415 237.5"/>

  <path class="wire" marker-end="url(#arrow)" d="M 550 1405 L 550 1465"/>

  <!-- Node 10: END (Oval) -->
  <g transform="translate(420, 1465)" filter="url(#shadow)">
    <rect width="260" height="55" rx="27.5" fill="#ffedd5" stroke="#f97316" stroke-width="2"/>
    <text x="130" y="27.5" class="node-title" fill="#c2410c">Stop Execution</text>
  </g>

</svg>'''

    svg_path = os.path.join("documentation", "diagram_5_predictive_thermal_flowchart.svg")
    png_path = os.path.join("documentation", "diagram_5_predictive_thermal_flowchart.png")
    typ_path = os.path.join("documentation", "render_diag5.typ")
    typst_exe = os.path.join("documentation", "bin", "typst.exe")

    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Wrote {svg_path}")

    with open(typ_path, "w", encoding="utf-8") as f:
        f.write(f'#set page(width: {w}pt, height: {h}pt, margin: 0pt)\n#image("diagram_5_predictive_thermal_flowchart.svg", width: 100%)\n')

    subprocess.run([typst_exe, "compile", "--format", "png", "--ppi", "150", typ_path, png_path], check=True)
    if os.path.exists(typ_path):
        os.remove(typ_path)
    print(f"Compiled {png_path}")

if __name__ == "__main__":
    generate()
