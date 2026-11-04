# -*- coding: utf-8 -*-
"""
Diagram 4: Hardware Operational Flowchart (10-State Supervisory Engine)
Textbook Academic Engineering Style (Matching User Reference Images 4 & 5):
- Unified, non-AI color palette:
  * Normal states / processes: Soft Sky Blue (#e0f2fe fill, #0284c7 stroke, #0369a1 text)
  * Decision diamonds: Soft Sky Blue (#e0f2fe fill, #0284c7 stroke, #0369a1 text)
  * Fault / Lockout states: Soft Coral (#fee2e2 fill, #ef4444 stroke, #991b1b text)
  * Terminator start/stop: Soft Peach (#ffedd5 fill, #f97316 stroke, #c2410c text)
- Strictly NO sentences: exactly 1-2 lines per node (2-3 words max, large legible font)
- Strictly NO text over arrows except clean 'Yes' and 'No' branch markers
- Clear return corridors with zero line overlaps
"""

import os
import subprocess

def generate():
    w = 1400
    h = 1650

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
    .node-sub {{
      font-size: 14px;
      font-weight: 500;
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
  <text x="{w/2}" y="40" class="title-main">HARDWARE OPERATIONAL FLOWCHART</text>
  <text x="{w/2}" y="70" class="title-sub">10-State Supervisory Engine &amp; Multi-Tier Protection</text>

  <!-- Node 0: START (Oval) at (500, 100) -->
  <g transform="translate(420, 100)" filter="url(#shadow)">
    <rect width="260" height="60" rx="30" fill="#ffedd5" stroke="#f97316" stroke-width="2"/>
    <text x="130" y="30" class="node-title" fill="#c2410c">AC Mains Connected</text>
  </g>
  <path class="wire" marker-end="url(#arrow)" d="M 550 160 L 550 200"/>

  <!-- Node 1: STANDBY_OFF (State 0) at (410, 200) -->
  <g transform="translate(410, 200)" filter="url(#shadow)">
    <rect width="280" height="75" rx="10" fill="#e0f2fe" stroke="#0284c7" stroke-width="2"/>
    <text x="140" y="27" class="node-title" fill="#0369a1">STANDBY_OFF</text>
    <text x="140" y="52" class="node-sub" fill="#0284c7">State 0 • Standby Rail</text>
  </g>
  <path class="wire" marker-end="url(#arrow)" d="M 550 275 L 550 315"/>

  <!-- Node 2: Read Run Switch (Parallelogram) -->
  <g transform="translate(410, 315)" filter="url(#shadow)">
    <polygon points="30,0 280,0 250,65 0,65" fill="#e0f2fe" stroke="#0284c7" stroke-width="2"/>
    <text x="140" y="32.5" class="node-title" fill="#0369a1">Read Run Switch</text>
  </g>
  <path class="wire" marker-end="url(#arrow)" d="M 550 380 L 550 420"/>

  <!-- Decision 1: Run Active? (Diamond) at (550, 470) -->
  <g transform="translate(425, 420)" filter="url(#shadow)">
    <polygon points="125,0 250,50 125,100 0,50" fill="#e0f2fe" stroke="#0284c7" stroke-width="2"/>
    <text x="125" y="50" class="node-title" fill="#0369a1">Run Active?</text>
  </g>
  <!-- Decision 1: No -> Loop back to STANDBY_OFF -->
  <path class="wire" marker-end="url(#arrow)" d="M 425 470 L 330 470 L 330 237.5 L 410 237.5"/>
  <text x="380" y="458" class="lbl-no">No</text>
  <!-- Decision 1: Yes -> STARTING -->
  <path class="wire" marker-end="url(#arrow)" d="M 550 520 L 550 560"/>
  <text x="560" y="540" class="lbl-yes">Yes</text>

  <!-- Node 3: STARTING (State 1) -->
  <g transform="translate(410, 560)" filter="url(#shadow)">
    <rect width="280" height="75" rx="10" fill="#e0f2fe" stroke="#0284c7" stroke-width="2"/>
    <text x="140" y="27" class="node-title" fill="#0369a1">STARTING</text>
    <text x="140" y="52" class="node-sub" fill="#0284c7">State 1 • Inrush Blanking</text>
  </g>
  <path class="wire" marker-end="url(#arrow)" d="M 550 635 L 550 675"/>

  <!-- Decision 2: Rails OK? (Diamond) at (550, 725) -->
  <g transform="translate(425, 675)" filter="url(#shadow)">
    <polygon points="125,0 250,50 125,100 0,50" fill="#e0f2fe" stroke="#0284c7" stroke-width="2"/>
    <text x="125" y="50" class="node-title" fill="#0369a1">Rails OK?</text>
  </g>
  <!-- Decision 2: No -> CONTROL_FAIL -->
  <path class="wire-red" marker-end="url(#arrow-red)" d="M 675 725 L 820 725"/>
  <text x="735" y="713" class="lbl-no">No</text>
  <!-- Fault 1: CONTROL_FAIL (State 9) -->
  <g transform="translate(820, 690)" filter="url(#shadow)">
    <rect width="260" height="70" rx="10" fill="#fee2e2" stroke="#ef4444" stroke-width="2"/>
    <text x="130" y="25" class="node-title" fill="#991b1b">CONTROL_FAIL</text>
    <text x="130" y="50" class="node-sub" fill="#ef4444">State 9 • Power Fault</text>
  </g>

  <!-- Decision 2: Yes -> RUNNING -->
  <path class="wire" marker-end="url(#arrow)" d="M 550 775 L 550 815"/>
  <text x="560" y="795" class="lbl-yes">Yes</text>

  <!-- Node 4: RUNNING (State 2) -->
  <g transform="translate(410, 815)" filter="url(#shadow)">
    <rect width="280" height="75" rx="10" fill="#bbf7d0" stroke="#16a34a" stroke-width="2.5"/>
    <text x="140" y="27" class="node-title" fill="#14532d">RUNNING</text>
    <text x="140" y="52" class="node-sub" fill="#15803d">State 2 • Active Monitoring</text>
  </g>
  <path class="wire" marker-end="url(#arrow)" d="M 550 890 L 550 930"/>

  <!-- Decision 3: Overcurrent? (Diamond) at (550, 980) -->
  <g transform="translate(425, 930)" filter="url(#shadow)">
    <polygon points="125,0 250,50 125,100 0,50" fill="#e0f2fe" stroke="#0284c7" stroke-width="2"/>
    <text x="125" y="50" class="node-title" fill="#0369a1">Overcurrent?</text>
  </g>
  <!-- Decision 3: Yes -> ELEC_LOCKOUT -->
  <path class="wire-red" marker-end="url(#arrow-red)" d="M 675 980 L 820 980"/>
  <text x="735" y="968" class="lbl-yes">Yes</text>
  <!-- Fault 2: ELEC_LOCKOUT (State 4) -->
  <g transform="translate(820, 945)" filter="url(#shadow)">
    <rect width="260" height="70" rx="10" fill="#fee2e2" stroke="#ef4444" stroke-width="2"/>
    <text x="130" y="25" class="node-title" fill="#991b1b">ELEC_LOCKOUT</text>
    <text x="130" y="50" class="node-sub" fill="#ef4444">State 4 • Instant Trip</text>
  </g>

  <!-- Decision 3: No -> Next Decision -->
  <path class="wire" marker-end="url(#arrow)" d="M 550 1030 L 550 1070"/>
  <text x="560" y="1050" class="lbl-no">No</text>

  <!-- Decision 4: Bus Fault? (Diamond) at (550, 1120) -->
  <g transform="translate(425, 1070)" filter="url(#shadow)">
    <polygon points="125,0 250,50 125,100 0,50" fill="#e0f2fe" stroke="#0284c7" stroke-width="2"/>
    <text x="125" y="50" class="node-title" fill="#0369a1">Bus Fault?</text>
  </g>
  <!-- Decision 4: Yes -> BUS_LOCKOUT -->
  <path class="wire-red" marker-end="url(#arrow-red)" d="M 675 1120 L 820 1120"/>
  <text x="735" y="1108" class="lbl-yes">Yes</text>
  <!-- Fault 3: BUS_LOCKOUT (State 5) -->
  <g transform="translate(820, 1085)" filter="url(#shadow)">
    <rect width="260" height="70" rx="10" fill="#fee2e2" stroke="#ef4444" stroke-width="2"/>
    <text x="130" y="25" class="node-title" fill="#991b1b">BUS_LOCKOUT</text>
    <text x="130" y="50" class="node-sub" fill="#ef4444">State 5 • Sensor Timeout</text>
  </g>

  <!-- Decision 4: No -> Next Decision -->
  <path class="wire" marker-end="url(#arrow)" d="M 550 1170 L 550 1210"/>
  <text x="560" y="1190" class="lbl-no">No</text>

  <!-- Decision 5: Thermal Trip? (Diamond) at (550, 1260) -->
  <g transform="translate(425, 1210)" filter="url(#shadow)">
    <polygon points="125,0 250,50 125,100 0,50" fill="#e0f2fe" stroke="#0284c7" stroke-width="2"/>
    <text x="125" y="50" class="node-title" fill="#0369a1">Thermal Trip?</text>
  </g>
  <!-- Decision 5: Yes -> THERMAL_COOL -->
  <path class="wire-red" marker-end="url(#arrow-red)" d="M 675 1260 L 820 1260"/>
  <text x="735" y="1248" class="lbl-yes">Yes</text>
  <!-- Recovery Subsystem: THERMAL_COOL (State 6) -->
  <g transform="translate(820, 1225)" filter="url(#shadow)">
    <rect width="260" height="70" rx="10" fill="#e0f2fe" stroke="#0284c7" stroke-width="2"/>
    <text x="130" y="25" class="node-title" fill="#0369a1">THERMAL_COOL</text>
    <text x="130" y="50" class="node-sub" fill="#0284c7">State 6 • Fan Cooldown</text>
  </g>
  <path class="wire" marker-end="url(#arrow)" d="M 950 1295 L 950 1335"/>

  <!-- Decision Cooldown: Cooled? (Diamond) at (950, 1385) -->
  <g transform="translate(825, 1335)" filter="url(#shadow)">
    <polygon points="125,0 250,50 125,100 0,50" fill="#e0f2fe" stroke="#0284c7" stroke-width="2"/>
    <text x="125" y="50" class="node-title" fill="#0369a1">Cooled Down?</text>
  </g>
  <!-- Cooled No -> THERMAL_LOCK -->
  <path class="wire-red" marker-end="url(#arrow-red)" d="M 950 1435 L 950 1485"/>
  <text x="960" y="1455" class="lbl-no">No</text>
  <g transform="translate(820, 1485)" filter="url(#shadow)">
    <rect width="260" height="70" rx="10" fill="#fee2e2" stroke="#ef4444" stroke-width="2"/>
    <text x="130" y="25" class="node-title" fill="#991b1b">THERMAL_LOCK</text>
    <text x="130" y="50" class="node-sub" fill="#ef4444">State 8 • Lockout</text>
  </g>
  <!-- Cooled Yes -> RECOVERY_TEST -->
  <path class="wire" marker-end="url(#arrow)" d="M 1075 1385 L 1150 1385"/>
  <text x="1090" y="1373" class="lbl-yes">Yes</text>
  <g transform="translate(1150, 1350)" filter="url(#shadow)">
    <rect width="200" height="70" rx="10" fill="#e0f2fe" stroke="#0284c7" stroke-width="2"/>
    <text x="100" y="25" class="node-title" fill="#0369a1">RECOVERY</text>
    <text x="100" y="50" class="node-sub" fill="#0284c7">State 7 • Test Run</text>
  </g>
  <!-- Recovery loop back to RUNNING -->
  <path class="wire" marker-end="url(#arrow)"
        d="M 1250 1350 L 1250 852.5 L 690 852.5"/>

  <!-- Decision 5: No -> Stop Request? -->
  <path class="wire" marker-end="url(#arrow)" d="M 550 1310 L 550 1350"/>
  <text x="560" y="1330" class="lbl-no">No</text>

  <!-- Decision 6: Stop Request? (Diamond) at (550, 1400) -->
  <g transform="translate(425, 1350)" filter="url(#shadow)">
    <polygon points="125,0 250,50 125,100 0,50" fill="#e0f2fe" stroke="#0284c7" stroke-width="2"/>
    <text x="125" y="50" class="node-title" fill="#0369a1">Stop Pressed?</text>
  </g>
  <!-- Decision 6: No -> Loop back to RUNNING -->
  <path class="wire" marker-end="url(#arrow)"
        d="M 425 1400 L 250 1400 L 250 852.5 L 410 852.5"/>
  <text x="360" y="1388" class="lbl-no">No</text>

  <!-- Decision 6: Yes -> MANUAL_OFF -->
  <path class="wire" marker-end="url(#arrow)" d="M 550 1450 L 550 1490"/>
  <text x="560" y="1470" class="lbl-yes">Yes</text>

  <!-- Node 5: MANUAL_OFF (State 3) -->
  <g transform="translate(410, 1490)" filter="url(#shadow)">
    <rect width="280" height="65" rx="10" fill="#e0f2fe" stroke="#0284c7" stroke-width="2"/>
    <text x="140" y="23" class="node-title" fill="#0369a1">MANUAL_OFF</text>
    <text x="140" y="45" class="node-sub" fill="#0284c7">State 3 • Graceful Stop</text>
  </g>
  <path class="wire" marker-end="url(#arrow)" d="M 550 1555 L 550 1590"/>

  <!-- Terminator: STOP (Oval) -->
  <g transform="translate(420, 1590)" filter="url(#shadow)">
    <rect width="260" height="50" rx="25" fill="#ffedd5" stroke="#f97316" stroke-width="2"/>
    <text x="130" y="25" class="node-title" fill="#c2410c">AC Mains Removed</text>
  </g>

</svg>'''

    svg_path = os.path.join("documentation", "diagram_4_hardware_state_flowchart.svg")
    png_path = os.path.join("documentation", "diagram_4_hardware_state_flowchart.png")
    typ_path = os.path.join("documentation", "render_diag4.typ")
    typst_exe = os.path.join("documentation", "bin", "typst.exe")

    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Wrote {svg_path}")

    with open(typ_path, "w", encoding="utf-8") as f:
        f.write(f'#set page(width: {w}pt, height: {h}pt, margin: 0pt)\n#image("diagram_4_hardware_state_flowchart.svg", width: 100%)\n')

    subprocess.run([typst_exe, "compile", "--format", "png", "--ppi", "150", typ_path, png_path], check=True)
    if os.path.exists(typ_path):
        os.remove(typ_path)
    print(f"Compiled {png_path}")

if __name__ == "__main__":
    generate()
