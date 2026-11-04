# -*- coding: utf-8 -*-
"""
Generate unified interactive HTML gallery viewer for all system architecture diagrams & flowcharts
"""

import os

def generate_gallery():
    diagrams = [
        {
            "id": "diag1",
            "title": "Diagram 1: Hardware Circuit Block Diagram",
            "subtitle": "Power Distribution, ATX SMPS, Multi-Rail INA219 Sensing, Dual DS18B20 & TB6612 Fan Actuation",
            "svg_file": "diagram_1_hardware_block.svg",
            "png_file": "diagram_1_hardware_block.png",
            "desc": "Illustrates the complete physical hardware topology: ATX breakout (XH-M229), +12V/5V/3.3V switched rails, standby +5VSB 24/7 logic supply, 3x INA219 current/voltage monitors, dual DS18B20 probes, 12V 50W dummy load, TB6612FNG MOSFET driver, and BC547 PS_ON# hardware failsafe interlock switch."
        },
        {
            "id": "diag2",
            "title": "Diagram 2: Software & Cloud Architecture Block Diagram",
            "subtitle": "ESP32 FreeRTOS Firmware, Firebase Hosting, RTDB, Firebase Auth, Cloudflare Watchdog & Brevo API",
            "svg_file": "diagram_2_software_cloud_block.svg",
            "png_file": "diagram_2_software_cloud_block.png",
            "desc": "Details the firmware execution pipelines (Sensor HAL, Mathematical Predictor, Supervisory Engine, Cloud Dispatcher) and serverless cloud topology: Firebase Hosting (deployed via Firebase CLI), Firebase RTDB (/latest, /history, /commands), Cloudflare Worker (60s cron watchdog), and Brevo Transactional Email delivery."
        },
        {
            "id": "diag3",
            "title": "Diagram 3: Combined Hardware & Software System Architecture",
            "subtitle": "Unified 4-Tier Cross-Domain Architecture: Cloud Tier, Local UI, Embedded Firmware & Physical Hardware",
            "svg_file": "diagram_3_combined_architecture_block.svg",
            "png_file": "diagram_3_combined_architecture_block.png",
            "desc": "A unified cross-domain architectural view stacking all 4 tiers: Tier 1 (Cloud & Remote Supervision), Tier 2 (Local Operator Interface & Access Boundary), Tier 3 (Embedded FreeRTOS Firmware Engine), and Tier 4 (Physical Hardware, Sensors & Power Actuation Layer) with 100% collision-free orthogonal routing."
        },
        {
            "id": "diag4",
            "title": "Diagram 4: Hardware Operational State Machine Flowchart",
            "subtitle": "10-State Supervisory Engine, 500 ms Inrush Blanking, Multi-Tier Cutoffs & Qualified Auto-Recovery",
            "svg_file": "diagram_4_hardware_state_flowchart.svg",
            "png_file": "diagram_4_hardware_state_flowchart.png",
            "desc": "Complete state machine modeling all 10 states from the engineering specification: STANDBY_OFF, STARTING (with 500 ms inrush blanking), RUNNING, MANUAL_OFF, ELEC_LOCKOUT, BUS_LOCKOUT, THERMAL_COOL, RECOVERY_TEST (120s qualification timer), THERMAL_LOCK (permanent lockout), and CONTROL_PATH_FAILURE."
        },
        {
            "id": "diag5",
            "title": "Diagram 5: Software & Predictive Thermal Control Flowchart",
            "subtitle": "1.00 Hz Real-Time Tick, Digital EMA Filter, 30s Regression Slope, Forward Projection & Dual-Demand PWM",
            "svg_file": "diagram_5_predictive_thermal_flowchart.svg",
            "png_file": "diagram_5_predictive_thermal_flowchart.png",
            "desc": "Step-by-step mathematical algorithm flowchart: 1.00s tick -> 1-Wire & I2C async read -> CRC-8 check -> EMA filter (alpha=0.20) -> Rolling 30s FIFO -> Least-squares regression slope -> 30s forward projection (Tp) -> Dual demand piecewise curve -> Asymmetric slew limiter (instant rise, <=1%/s descent) -> 25 kHz ultrasonic LEDC PWM actuation."
        },
        {
            "id": "diag6",
            "title": "Diagram 6: Combined System Supervisory End-to-End Flowchart",
            "subtitle": "Sensor Acquisition -> Health Evaluation -> Normal Dynamic Cooling vs Critical Hardware Trip & Cloud Push",
            "svg_file": "diagram_6_combined_supervisory_flowchart.svg",
            "png_file": "diagram_6_combined_supervisory_flowchart.png",
            "desc": "End-to-end supervisory flowchart linking physical hardware, firmware trip decisions, instant hardware cutoff (< 5 ms GPIO 32 LOW -> PS_ON# released -> ATX rails collapsed), NVS flash fault latching, standby-powered 16x2 LCD alert, Firebase RTDB emergency push, Cloudflare Worker trigger, and Brevo email delivery."
        },
        {
            "id": "schematic",
            "title": "Master Hardware Schematic: Cirkit Designer Wiring Diagram",
            "subtitle": "Complete Breadboard & Component Wiring: ESP32, ATX Breakout, INA219 x3, DS18B20 x2, TB6612, LCD & BC547",
            "svg_file": "transformer_cbm_circuit_diagram.svg",
            "png_file": "circuit_diagram_preview.png",
            "desc": "Publication-grade wiring schematic with custom styled component chips, pin labels, color-coded power buses (+12V, +5V, +3.3V, +5VSB, GND), dedicated BC547 NPN transistor switch circuit, 16x2 I2C LCD, and 3-pin DS18B20 digital temperature sensor modules."
        }
    ]

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>IoT Transformer Condition Monitoring System — Architectural Diagrams &amp; Flowcharts Gallery</title>
  <style>
    :root {{
      --primary: #2563eb;
      --primary-dark: #1d4ed8;
      --bg: #0f172a;
      --surface: #1e293b;
      --surface-light: #334155;
      --text: #f8fafc;
      --text-muted: #94a3b8;
      --accent: #059669;
      --warning: #d97706;
      --danger: #dc2626;
      --border: #334155;
    }}
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Inter", sans-serif;
      background: var(--bg);
      color: var(--text);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }}
    header {{
      background: var(--surface);
      border-bottom: 1px solid var(--border);
      padding: 20px 32px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 16px;
    }}
    .title-group h1 {{
      font-size: 22px;
      font-weight: 800;
      color: #ffffff;
      letter-spacing: -0.5px;
    }}
    .title-group p {{
      font-size: 13.5px;
      color: var(--text-muted);
      margin-top: 4px;
    }}
    .nav-tabs {{
      display: flex;
      background: #090d16;
      border-bottom: 1px solid var(--border);
      padding: 8px 32px 0;
      overflow-x: auto;
      gap: 6px;
    }}
    .tab-btn {{
      background: transparent;
      border: 1px solid transparent;
      border-bottom: none;
      color: var(--text-muted);
      font-size: 13.5px;
      font-weight: 700;
      padding: 12px 18px;
      cursor: pointer;
      border-radius: 8px 8px 0 0;
      transition: all 0.15s ease;
      white-space: nowrap;
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .tab-btn:hover {{
      color: #ffffff;
      background: rgba(255, 255, 255, 0.04);
    }}
    .tab-btn.active {{
      color: #ffffff;
      background: var(--surface);
      border-color: var(--border);
      border-top: 3px solid #38bdf8;
    }}
    .tab-btn .badge {{
      font-size: 11px;
      padding: 2px 7px;
      border-radius: 999px;
      background: rgba(255, 255, 255, 0.1);
    }}
    .tab-btn.active .badge {{
      background: #0284c7;
      color: #ffffff;
    }}
    .main-content {{
      flex: 1;
      padding: 24px 32px;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }}
    .card-meta {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 18px 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 16px;
    }}
    .meta-text h2 {{
      font-size: 18px;
      font-weight: 800;
      color: #ffffff;
    }}
    .meta-text p {{
      font-size: 13px;
      color: #cbd5e1;
      margin-top: 4px;
      max-width: 1000px;
      line-height: 1.5;
    }}
    .action-group {{
      display: flex;
      gap: 10px;
      align-items: center;
    }}
    .btn {{
      background: var(--surface-light);
      border: 1px solid #475569;
      color: #ffffff;
      font-size: 13px;
      font-weight: 700;
      padding: 9px 16px;
      border-radius: 6px;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      text-decoration: none;
      transition: all 0.15s ease;
    }}
    .btn:hover {{
      background: #475569;
      border-color: #64748b;
    }}
    .btn-primary {{
      background: var(--primary);
      border-color: var(--primary-dark);
    }}
    .btn-primary:hover {{
      background: var(--primary-dark);
    }}
    .viewer-container {{
      flex: 1;
      background: #0b0f19;
      border: 1px solid var(--border);
      border-radius: 12px;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      position: relative;
      min-height: 720px;
      box-shadow: inset 0 2px 10px rgba(0, 0, 0, 0.4);
    }}
    .viewer-toolbar {{
      background: rgba(15, 23, 42, 0.85);
      backdrop-filter: blur(8px);
      border-bottom: 1px solid var(--border);
      padding: 8px 16px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      z-index: 10;
    }}
    .zoom-controls {{
      display: flex;
      gap: 6px;
    }}
    .tool-btn {{
      background: var(--surface);
      border: 1px solid var(--border);
      color: #f1f5f9;
      padding: 6px 12px;
      border-radius: 5px;
      font-size: 12.5px;
      font-weight: 700;
      cursor: pointer;
    }}
    .tool-btn:hover {{
      background: var(--surface-light);
    }}
    .viewport {{
      flex: 1;
      overflow: auto;
      display: flex;
      justify-content: center;
      align-items: center;
      padding: 24px;
      position: relative;
    }}
    .diagram-panel {{
      display: none;
      width: 100%;
      height: 100%;
    }}
    .diagram-panel.active {{
      display: flex;
      justify-content: center;
      align-items: center;
    }}
    .diagram-panel img {{
      max-width: 100%;
      max-height: 100%;
      object-fit: contain;
      border-radius: 8px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.5);
      transition: transform 0.2s ease;
      transform-origin: center center;
    }}
  </style>
</head>
<body>

  <header>
    <div class="title-group">
      <h1>IoT Transformer Condition Monitoring System (CBM)</h1>
      <p>System Architecture Diagrams, Predictive Thermal Algorithms &amp; Supervisory State Flowcharts</p>
    </div>
    <div class="action-group">
      <a href="transformer_cbm_spec.pdf" target="_blank" class="btn btn-primary">
        <span>📄 Open Complete Specification PDF</span>
      </a>
    </div>
  </header>

  <nav class="nav-tabs" id="navTabs">
'''

    for i, d in enumerate(diagrams):
        active_cls = " active" if i == 0 else ""
        badge_txt = f"0{i+1}" if i < 6 else "SCHEMATIC"
        short_title = d["title"].split(":")[1].strip() if ":" in d["title"] else d["title"]
        html += f'''    <button class="tab-btn{active_cls}" onclick="switchTab('{d["id"]}')">
      <span class="badge">{badge_txt}</span>
      <span>{short_title}</span>
    </button>\n'''

    html += '''  </nav>

  <main class="main-content">
'''

    for i, d in enumerate(diagrams):
        active_cls = " active" if i == 0 else ""
        html += f'''    <!-- {d["title"]} -->
    <div id="{d["id"]}-card" class="diagram-panel{active_cls}">
      <div style="width: 100%; display: flex; flex-direction: column; gap: 14px;">
        <div class="card-meta">
          <div class="meta-text">
            <h2>{d["title"]}</h2>
            <p><strong>Architecture Overview:</strong> {d["desc"]}</p>
          </div>
          <div class="action-group">
            <a href="{d["svg_file"]}" target="_blank" class="btn">
              <span>🔍 Open Vector SVG</span>
            </a>
            <a href="{d["png_file"]}" download class="btn">
              <span>📥 Download High-Res PNG (150 PPI)</span>
            </a>
          </div>
        </div>

        <div class="viewer-container">
          <div class="viewer-toolbar">
            <span style="font-size: 12.5px; color: var(--text-muted);">Interactive View: Click and drag or use controls</span>
            <div class="zoom-controls">
              <button class="tool-btn" onclick="zoomDiagram('{d["id"]}', 0.15)">Zoom In (+)</button>
              <button class="tool-btn" onclick="zoomDiagram('{d["id"]}', -0.15)">Zoom Out (-)</button>
              <button class="tool-btn" onclick="resetZoom('{d["id"]}')">Reset</button>
              <button class="tool-btn" onclick="toggleFullscreen('{d["id"]}')">Full Window</button>
            </div>
          </div>
          <div class="viewport" id="{d["id"]}-viewport">
            <img id="{d["id"]}-img" src="{d["png_file"]}" alt="{d["title"]}" data-zoom="1.0">
          </div>
        </div>
      </div>
    </div>\n'''

    html += '''  </main>

  <script>
    function switchTab(id) {
      document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
      document.querySelectorAll('.diagram-panel').forEach(panel => panel.classList.remove('active'));

      const btns = document.querySelectorAll('.tab-btn');
      const tabs = ['diag1', 'diag2', 'diag3', 'diag4', 'diag5', 'diag6', 'schematic'];
      const idx = tabs.indexOf(id);
      if (idx !== -1 && btns[idx]) {
        btns[idx].classList.add('active');
      }

      const activeCard = document.getElementById(id + '-card');
      if (activeCard) {
        activeCard.classList.add('active');
      }
    }

    function zoomDiagram(id, delta) {
      const img = document.getElementById(id + '-img');
      if (!img) return;
      let cur = parseFloat(img.getAttribute('data-zoom') || '1.0');
      cur = Math.max(0.5, Math.min(3.0, cur + delta));
      img.setAttribute('data-zoom', cur.toFixed(2));
      img.style.transform = `scale(${cur})`;
    }

    function resetZoom(id) {
      const img = document.getElementById(id + '-img');
      if (!img) return;
      img.setAttribute('data-zoom', '1.0');
      img.style.transform = 'scale(1.0)';
    }

    function toggleFullscreen(id) {
      const vp = document.getElementById(id + '-viewport');
      if (!vp) return;
      if (!document.fullscreenElement) {
        vp.requestFullscreen().catch(err => {
          alert(`Error entering fullscreen: ${err.message}`);
        });
      } else {
        document.exitFullscreen();
      }
    }
  </script>
</body>
</html>'''

    out_file = os.path.join("documentation", "system_diagrams_gallery.html")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Generated {out_file}")

if __name__ == "__main__":
    generate_gallery()
