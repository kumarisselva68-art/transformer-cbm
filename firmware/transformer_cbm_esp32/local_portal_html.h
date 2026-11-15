#ifndef LOCAL_PORTAL_HTML_H
#define LOCAL_PORTAL_HTML_H

#include <Arduino.h>

/**
 * Embedded Zero-CDN Local Web Portal for Transformer CBM
 * Served directly from ESP32 PROGMEM in SoftAP / Local Mode.
 * Designed with an Apple/Linear obsidian industrial aesthetic.
 * Fully responsive for mobile and desktop displays.
 * Strictly zero emojis and zero external internet dependencies.
 */
const char LOCAL_PORTAL_HTML[] PROGMEM = R"rawliteral(<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>TRANSFORMER CBM &mdash; Local Console</title>
<style>
:root {
  --bg-primary: #070a12;
  --bg-card: #0f172a;
  --bg-card-hover: #1e293b;
  --border: #1e293b;
  --border-light: #334155;
  --text-main: #f8fafc;
  --text-muted: #94a3b8;
  --text-dim: #64748b;
  --accent-cyan: #38bdf8;
  --accent-green: #10b981;
  --accent-amber: #f59e0b;
  --accent-crimson: #ef4444;
  --font-stack: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  --radius: 12px;
}
* { box-sizing: border-box; margin: 0; padding: 0; -webkit-tap-highlight-color: transparent; }
body {
  background-color: var(--bg-primary);
  color: var(--text-main);
  font-family: var(--font-stack);
  font-size: 14px;
  line-height: 1.5;
  padding: 16px;
  min-height: 100vh;
}
.container { max-width: 1040px; margin: 0 auto; }
header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  margin-bottom: 16px;
  flex-wrap: wrap;
  gap: 12px;
}
.header-title { font-size: 16px; font-weight: 800; letter-spacing: 0.5px; color: var(--text-main); }
.header-subtitle { font-size: 12px; color: var(--text-muted); font-weight: 500; }
.header-status {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  padding: 6px 12px;
  background: rgba(16, 185, 129, 0.1);
  border: 1px solid rgba(16, 185, 129, 0.25);
  border-radius: 9999px;
  color: var(--accent-green);
}
.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--accent-green);
  box-shadow: 0 0 8px var(--accent-green);
  animation: pulse 2s infinite ease-in-out;
}
@keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.4; } }
.trip-active {
  background: rgba(239, 68, 68, 0.15) !important;
  border-color: rgba(239, 68, 68, 0.3) !important;
  color: var(--accent-crimson) !important;
}
.trip-active .status-dot {
  background: var(--accent-crimson) !important;
  box-shadow: 0 0 8px var(--accent-crimson) !important;
}
.grid-main {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 16px;
  margin-bottom: 16px;
}
.card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 18px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  transition: border-color 0.2s;
}
.card:hover { border-color: var(--border-light); }
.card-label {
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.75px;
  color: var(--text-muted);
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}
.card-val-row { display: flex; align-items: baseline; gap: 6px; }
.card-val { font-size: 32px; font-weight: 800; color: var(--text-main); font-feature-settings: "tnum"; }
.card-unit { font-size: 16px; font-weight: 600; color: var(--text-muted); }
.card-sub {
  margin-top: 10px;
  padding-top: 10px;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: var(--text-muted);
}
.badge {
  font-size: 10px;
  padding: 3px 8px;
  border-radius: 4px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
.badge-green { background: rgba(16, 185, 129, 0.15); color: var(--accent-green); }
.badge-amber { background: rgba(245, 158, 11, 0.15); color: var(--accent-amber); }
.badge-crimson { background: rgba(239, 68, 68, 0.15); color: var(--accent-crimson); }
.badge-cyan { background: rgba(56, 189, 248, 0.15); color: var(--accent-cyan); }

/* Control Panel Section */
.controls-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 16px;
  margin-bottom: 16px;
}
.control-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 20px;
}
.section-title {
  font-size: 13px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.75px;
  color: var(--text-main);
  margin-bottom: 14px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.btn-group { display: flex; gap: 10px; margin-top: 12px; }
.btn {
  flex: 1;
  padding: 12px 16px;
  font-size: 13px;
  font-weight: 700;
  border-radius: 8px;
  border: 1px solid transparent;
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: center;
  user-select: none;
}
.btn-primary { background: #2563eb; color: #fff; }
.btn-primary:hover { background: #1d4ed8; }
.btn-danger { background: rgba(239, 68, 68, 0.15); border-color: rgba(239, 68, 68, 0.3); color: var(--accent-crimson); }
.btn-danger:hover { background: var(--accent-crimson); color: #fff; }
.btn-success { background: rgba(16, 185, 129, 0.15); border-color: rgba(16, 185, 129, 0.3); color: var(--accent-green); }
.btn-success:hover { background: var(--accent-green); color: #000; }
.btn-secondary { background: #1e293b; color: var(--text-main); border-color: var(--border-light); }
.btn-secondary:hover { background: #334155; }
.slider-container { margin-top: 14px; }
.slider-labels { display: flex; justify-content: space-between; font-size: 12px; color: var(--text-muted); margin-bottom: 6px; }
input[type=range] {
  width: 100%;
  height: 6px;
  background: #334155;
  border-radius: 3px;
  outline: none;
  -webkit-appearance: none;
}
input[type=range]::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: var(--accent-cyan);
  cursor: pointer;
  box-shadow: 0 0 10px rgba(56, 189, 248, 0.5);
}

/* WiFi Provisioning Section */
.wifi-form { display: flex; flex-direction: column; gap: 12px; margin-top: 10px; }
.form-group { display: flex; flex-direction: column; gap: 6px; }
.form-label { font-size: 11px; font-weight: 700; color: var(--text-muted); text-transform: uppercase; }
.form-input, .form-select {
  background: #090d16;
  border: 1px solid var(--border-light);
  color: var(--text-main);
  padding: 10px 14px;
  border-radius: 8px;
  font-size: 13px;
  outline: none;
  width: 100%;
  font-family: inherit;
}
.form-input:focus, .form-select:focus { border-color: var(--accent-cyan); }
.toast {
  position: fixed;
  bottom: 24px;
  right: 24px;
  padding: 12px 20px;
  background: #1e293b;
  border: 1px solid var(--border-light);
  border-radius: 8px;
  font-weight: 600;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
  opacity: 0;
  transform: translateY(10px);
  transition: all 0.25s ease;
  pointer-events: none;
  z-index: 1000;
}
.toast.show { opacity: 1; transform: translateY(0); }
footer {
  text-align: center;
  font-size: 11px;
  color: var(--text-dim);
  padding: 24px 0 12px;
  border-top: 1px solid var(--border);
  margin-top: 24px;
}
</style>
</head>
<body>
<div class="container">
  <header>
    <div>
      <div class="header-title">TRANSFORMER CBM &bull; LOCAL CONSOLE</div>
      <div class="header-subtitle" id="deviceMeta">TMS-ESP32 Rev 3.0 &bull; Dual-Core Embedded Node</div>
    </div>
    <div class="header-status" id="statusBadge">
      <span class="status-dot"></span>
      <span id="statusText">SYSTEM NOMINAL</span>
    </div>
  </header>

  <!-- Real-Time Thermal & Prognostics Grid -->
  <div class="grid-main">
    <div class="card">
      <div class="card-label">
        <span>Core Hotspot (T1)</span>
        <span class="badge badge-green" id="tCoreBadge">NOMINAL</span>
      </div>
      <div class="card-val-row">
        <span class="card-val" id="valTcore">--.-</span>
        <span class="card-unit">&deg;C</span>
      </div>
      <div class="card-sub">
        <span>Trip Limit</span>
        <span>65.0 &deg;C</span>
      </div>
    </div>

    <div class="card">
      <div class="card-label">
        <span>Inlet Airflow (T2)</span>
        <span class="badge badge-cyan">AMBIENT</span>
      </div>
      <div class="card-val-row">
        <span class="card-val" id="valTinlet">--.-</span>
        <span class="card-unit">&deg;C</span>
      </div>
      <div class="card-sub">
        <span>Thermal Rise (&Delta;T)</span>
        <span id="valDeltaT">--.- &deg;C</span>
      </div>
    </div>

    <div class="card">
      <div class="card-label">
        <span>Predicted Horizon</span>
        <span class="badge badge-amber">+30s OLS</span>
      </div>
      <div class="card-val-row">
        <span class="card-val" id="valTpred">--.-</span>
        <span class="card-unit">&deg;C</span>
      </div>
      <div class="card-sub">
        <span>Rate of Rise</span>
        <span id="valRateOfRise">--.- &deg;C/s</span>
      </div>
    </div>

    <div class="card">
      <div class="card-label">
        <span>Transformer Health Index</span>
        <span class="badge badge-green" id="hiBadge">HEALTHY</span>
      </div>
      <div class="card-val-row">
        <span class="card-val" id="valHI">100.0</span>
        <span class="card-unit">%</span>
      </div>
      <div class="card-sub">
        <span>Virtual Hotspot (THST)</span>
        <span id="valThst">--.- &deg;C</span>
      </div>
    </div>
  </div>

  <!-- Multi-Rail DC Power Diagnostics Grid -->
  <div class="grid-main">
    <div class="card">
      <div class="card-label">
        <span>+12V Main Load Rail</span>
        <span class="badge badge-cyan">INA219 0x40</span>
      </div>
      <div class="card-val-row">
        <span class="card-val" id="valV12">--.-</span>
        <span class="card-unit">V</span>
      </div>
      <div class="card-sub">
        <span id="valI12">-- A</span>
        <span id="valP12">-- W</span>
      </div>
    </div>

    <div class="card">
      <div class="card-label">
        <span>+5V Standby Rail</span>
        <span class="badge badge-cyan">INA219 0x41</span>
      </div>
      <div class="card-val-row">
        <span class="card-val" id="valV5">--.-</span>
        <span class="card-unit">V</span>
      </div>
      <div class="card-sub">
        <span id="valI5">-- A</span>
        <span id="valP5">-- W</span>
      </div>
    </div>

    <div class="card">
      <div class="card-label">
        <span>+3.3V Logic Bus</span>
        <span class="badge badge-cyan">INA219 0x44</span>
      </div>
      <div class="card-val-row">
        <span class="card-val" id="valV33">--.-</span>
        <span class="card-unit">V</span>
      </div>
      <div class="card-sub">
        <span id="valI33">-- A</span>
        <span id="valP33">-- W</span>
      </div>
    </div>

    <div class="card">
      <div class="card-label">
        <span>Ultrasonic Fan Actuation</span>
        <span class="badge badge-green" id="fanModeBadge">AUTO-PID</span>
      </div>
      <div class="card-val-row">
        <span class="card-val" id="valFanSpeed">--</span>
        <span class="card-unit">% PWM</span>
      </div>
      <div class="card-sub">
        <span>Carrier Frequency</span>
        <span>25 kHz Silent</span>
      </div>
    </div>
  </div>

  <!-- Supervisory Controls and Wi-Fi Configuration Section -->
  <div class="controls-grid">
    <!-- Local Actuator Controls -->
    <div class="control-card">
      <div class="section-title">
        <span>Main Power Supervisory Interlock</span>
        <span class="badge badge-green" id="powerStatusBadge">ENERGIZED</span>
      </div>
      <p style="color:var(--text-muted);font-size:12px;margin-bottom:12px;">
        Direct active-low hardware isolation via 2N3904 transistor on PS_ON#. Latches off upon trip.
      </p>
      <div class="btn-group">
        <button class="btn btn-danger" onclick="sendControl('power', 0)">EMERGENCY CUTOFF</button>
        <button class="btn btn-success" onclick="sendControl('power', 1)">ENERGIZE RAILS</button>
      </div>

      <div class="section-title" style="margin-top:24px;">
        <span>Active Cooling Modulation</span>
      </div>
      <div class="slider-container">
        <div class="slider-labels">
          <span>Manual Duty Override</span>
          <span id="sliderDutyLabel">50%</span>
        </div>
        <input type="range" id="fanDutySlider" min="0" max="100" value="50" oninput="updateFanSliderLabel(this.value)" onchange="sendFanControl('MANUAL', this.value)">
      </div>
      <div class="btn-group">
        <button class="btn btn-secondary" onclick="sendFanControl('AUTO', 0)">RESTORE AUTO-PID</button>
        <button class="btn btn-secondary" onclick="sendControl('reset_fault', 1)">CLEAR FAULT TRIP</button>
      </div>
    </div>

    <!-- Wi-Fi Provisioning Configuration -->
    <div class="control-card">
      <div class="section-title">
        <span>Wi-Fi Network Provisioning</span>
        <span class="badge badge-cyan" id="netStateBadge">STANDALONE AP</span>
      </div>
      <p style="color:var(--text-muted);font-size:12px;margin-bottom:8px;">
        Configure station credentials to establish uplink with Cloudflare Edge.
      </p>
      <form class="wifi-form" onsubmit="saveWifiConfig(event)">
        <div class="form-group">
          <label class="form-label">Available 2.4 GHz Access Points</label>
          <div style="display:flex;gap:8px;">
            <select class="form-select" id="wifiSelect" onchange="selectNetwork(this.value)">
              <option value="">-- Tap 'Scan' to discover --</option>
            </select>
            <button type="button" class="btn btn-secondary" style="flex:0 0 80px;" onclick="scanNetworks()">SCAN</button>
          </div>
        </div>
        <div class="form-group">
          <label class="form-label">Network SSID</label>
          <input type="text" class="form-input" id="wifiSsid" placeholder="Target Wi-Fi SSID" required>
        </div>
        <div class="form-group">
          <label class="form-label">WPA2/WPA3 Pre-Shared Key</label>
          <input type="password" class="form-input" id="wifiPass" placeholder="Wi-Fi Password">
        </div>
        <button type="submit" class="btn btn-primary" style="margin-top:4px;">SAVE &amp; CONNECT TO NETWORK</button>
      </form>
    </div>
  </div>

  <footer>
    TRANSFORMER CONDITION MONITORING SYSTEM &bull; EMBEDDED FREERTOS FIRMWARE REV 3.0<br>
    Rajalakshmi Institute of Technology &bull; Department of Electronics and Communication Engineering
  </footer>
</div>

<div class="toast" id="toastBox">Action dispatched</div>

<script>
let lastFaultCode = 0;

function showToast(msg) {
  const t = document.getElementById('toastBox');
  t.innerText = msg;
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 3000);
}

function updateFanSliderLabel(val) {
  document.getElementById('sliderDutyLabel').innerText = val + '%';
}

function pollTelemetry() {
  fetch('/api/telemetry')
    .then(r => r.json())
    .then(data => {
      document.getElementById('valTcore').innerText = data.t_core.toFixed(1);
      document.getElementById('valTinlet').innerText = data.t_inlet.toFixed(1);
      document.getElementById('valDeltaT').innerText = (data.t_core - data.t_inlet).toFixed(1) + ' \u00B0C';
      document.getElementById('valTpred').innerText = data.t_predicted.toFixed(1);
      document.getElementById('valRateOfRise').innerText = (data.rate_of_rise >= 0 ? '+' : '') + data.rate_of_rise.toFixed(2) + ' \u00B0C/s';
      document.getElementById('valHI').innerText = data.health_index.toFixed(1);
      document.getElementById('valThst').innerText = data.t_hotspot.toFixed(1) + ' \u00B0C';

      // Power Rails
      document.getElementById('valV12').innerText = data.v_12v.toFixed(2);
      document.getElementById('valI12').innerText = data.i_12v.toFixed(2) + ' A';
      document.getElementById('valP12').innerText = data.p_12v.toFixed(2) + ' W';

      document.getElementById('valV5').innerText = data.v_5v.toFixed(2);
      document.getElementById('valI5').innerText = data.i_5v.toFixed(2) + ' A';
      document.getElementById('valP5').innerText = data.p_5v.toFixed(2) + ' W';

      document.getElementById('valV33').innerText = data.v_3v3.toFixed(2);
      document.getElementById('valI33').innerText = data.i_3v3.toFixed(2) + ' A';
      document.getElementById('valP33').innerText = data.p_3v3.toFixed(2) + ' W';

      // Fan
      document.getElementById('valFanSpeed').innerText = data.fan_speed;
      document.getElementById('fanModeBadge').innerText = data.fan_auto ? 'AUTO-PID' : 'MANUAL';

      // Badges & States
      const tBadge = document.getElementById('tCoreBadge');
      if (data.t_core >= 65.0) {
        tBadge.className = 'badge badge-crimson';
        tBadge.innerText = 'TRIP BREACH';
      } else if (data.t_core >= 50.0) {
        tBadge.className = 'badge badge-amber';
        tBadge.innerText = 'ELEVATED';
      } else {
        tBadge.className = 'badge badge-green';
        tBadge.innerText = 'NOMINAL';
      }

      // Master Rail State
      const pwrBadge = document.getElementById('powerStatusBadge');
      if (data.pson_active) {
        pwrBadge.className = 'badge badge-green';
        pwrBadge.innerText = 'ENERGIZED';
      } else {
        pwrBadge.className = 'badge badge-crimson';
        pwrBadge.innerText = 'ISOLATED';
      }

      // Overall System Status
      const statusBadge = document.getElementById('statusBadge');
      const statusText = document.getElementById('statusText');
      if (data.fault_code > 0) {
        statusBadge.classList.add('trip-active');
        if (data.fault_code === 1) statusText.innerText = 'TRIP: CORE OVERTEMP';
        else if (data.fault_code === 2) statusText.innerText = 'TRIP: PREDICTIVE RATE';
        else if (data.fault_code === 3) statusText.innerText = 'TRIP: OVERCURRENT';
        else statusText.innerText = 'TRIP: SAFETY CUTOFF';
      } else {
        statusBadge.classList.remove('trip-active');
        statusText.innerText = data.pson_active ? 'SYSTEM NOMINAL' : 'MAIN RAILS OFF';
      }

      // Network State
      const netBadge = document.getElementById('netStateBadge');
      if (data.wifi_connected) {
        netBadge.className = 'badge badge-green';
        netBadge.innerText = 'ONLINE (' + data.ip_addr + ')';
      } else if (data.ap_active) {
        netBadge.className = 'badge badge-cyan';
        netBadge.innerText = 'LOCAL AP (192.168.4.1)';
      } else {
        netBadge.className = 'badge badge-amber';
        netBadge.innerText = 'STANDALONE';
      }
    })
    .catch(() => {});
}

function sendControl(action, value) {
  fetch('/api/control', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ action: action, value: value })
  })
  .then(r => r.json())
  .then(res => {
    showToast(res.message || 'Command executed');
    pollTelemetry();
  })
  .catch(() => showToast('Error communicating with ESP32'));
}

function sendFanControl(mode, speed) {
  fetch('/api/control', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ action: 'fan', mode: mode, speed: parseInt(speed) })
  })
  .then(r => r.json())
  .then(res => {
    showToast(res.message || 'Fan setting updated');
    pollTelemetry();
  })
  .catch(() => showToast('Error setting fan'));
}

function scanNetworks() {
  showToast('Scanning 2.4 GHz spectrum...');
  fetch('/api/wifi/scan')
    .then(r => r.json())
    .then(networks => {
      const select = document.getElementById('wifiSelect');
      select.innerHTML = '<option value="">-- Select Discovered AP --</option>';
      networks.forEach(net => {
        const opt = document.createElement('option');
        opt.value = net.ssid;
        opt.innerText = net.ssid + ' (' + net.rssi + ' dBm)';
        select.appendChild(opt);
      });
      showToast('Found ' + networks.length + ' networks');
    })
    .catch(() => showToast('Scan failed'));
}

function selectNetwork(ssid) {
  if (ssid) {
    document.getElementById('wifiSsid').value = ssid;
  }
}

function saveWifiConfig(e) {
  e.preventDefault();
  const ssid = document.getElementById('wifiSsid').value;
  const pass = document.getElementById('wifiPass').value;

  showToast('Saving credentials and reconnecting...');
  fetch('/api/wifi/save', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ ssid: ssid, pass: pass })
  })
  .then(r => r.json())
  .then(res => {
    showToast(res.message || 'Credentials stored in flash');
  })
  .catch(() => showToast('Failed to save settings'));
}

setInterval(pollTelemetry, 1000);
window.onload = pollTelemetry;
</script>
</body>
</html>
)rawliteral";

#endif // LOCAL_PORTAL_HTML_H
