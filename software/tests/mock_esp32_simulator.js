/**
 * Interactive ESP32 Hardware Simulator
 * Simulates FreeRTOS 10-Second Telemetry Ingestion, Thermal Dynamics, and Remote Control Execution
 *
 * Usage:
 *   node tests/mock_esp32_simulator.js [http://localhost:8787]
 */

const TARGET_URL = process.argv[2] || process.env.API_URL || 'http://localhost:8787';
const DEVICE_KEY = process.env.DEVICE_KEY || 'cbm_esp32_sec_key_2026';
const DEVICE_ID = 'TRANSFORMER_01';

console.log('====================================================');
console.log('🤖 ESP32 HARDWARE SIMULATOR (FreeRTOS Core Emulation)');
console.log(`Target Cloudflare Worker: ${TARGET_URL}`);
console.log(`Device Identifier:        ${DEVICE_ID}`);
console.log(`X-Device-Key:             ${DEVICE_KEY}`);
console.log('====================================================\n');

// Simulated Hardware Physical State
let psonActive = 1; // 1 = Main rails energized, 0 = Tripped/Off
let tCore = 36.5;
let tInlet = 28.2;
let tFiltered = 36.5;
let rateOfRise = 0.02;
let cycleCount = 0;

async function runSimulationCycle() {
  cycleCount++;

  // 1. Simulate Thermal Physics & Dynamic Heating
  if (psonActive) {
    // Slight heating under load
    tCore += (Math.random() * 0.3 - 0.1);
  } else {
    // Natural cooldown when main output is de-energized
    if (tCore > tInlet + 2.0) {
      tCore -= 0.4;
    }
  }

  // EMA Filter & Extrapolation Horizon (+30s)
  const alpha = 0.2;
  const prevFiltered = tFiltered;
  tFiltered = (alpha * tCore) + ((1.0 - alpha) * prevFiltered);
  rateOfRise = tFiltered - prevFiltered;
  const tPredicted = tFiltered + (30.0 * Math.max(0, rateOfRise));

  // Local Autonomous Hardware Trip Check (Absolute >= 65°C or Predicted >= 70°C)
  let faultCode = 0;
  if (tCore >= 65.0) {
    faultCode = 1; // Core Overtemp
    psonActive = 0;
    console.log('🚨 [LOCAL HARDWARE TRIP] Core Temp >= 65.0°C! GPIO32 de-energized (PS_ON# CUT)!');
  } else if (tPredicted >= 70.0) {
    faultCode = 2; // Predictive Horizon Trip
    psonActive = 0;
    console.log('🚨 [LOCAL HARDWARE TRIP] Predictive Temp >= 70.0°C! GPIO32 de-energized (PS_ON# CUT)!');
  }

  // 2. Prepare JSON Telemetry Payload
  const payload = {
    device_id: DEVICE_ID,
    t_core: parseFloat(tCore.toFixed(2)),
    t_inlet: parseFloat(tInlet.toFixed(2)),
    t_predicted: parseFloat(tPredicted.toFixed(2)),
    rate_of_rise: parseFloat(rateOfRise.toFixed(3)),
    v_12v: psonActive ? parseFloat((12.02 + (Math.random() * 0.08 - 0.04)).toFixed(2)) : 0.0,
    i_12v: psonActive ? parseFloat((2.85 + (Math.random() * 0.3 - 0.15)).toFixed(2)) : 0.0,
    v_5v: 5.01,
    i_5v: 0.85,
    v_3v3: 3.31,
    i_3v3: 0.42,
    pson_active: psonActive,
    fault_code: faultCode
  };

  console.log(`[CYCLE #${cycleCount}] T_core: ${payload.t_core}°C | T_inlet: ${payload.t_inlet}°C | T_pred: ${payload.t_predicted}°C | 12V: ${payload.v_12v}V (${payload.i_12v}A) | Main: ${psonActive ? 'ON' : 'OFF'}`);

  // 3. Transmit via HTTPS POST to Cloudflare Worker
  try {
    const res = await fetch(`${TARGET_URL}/api/telemetry`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Device-Key': DEVICE_KEY
      },
      body: JSON.stringify(payload)
    });

    if (!res.ok) {
      console.error(`❌ [SERVER ERROR] HTTP ${res.status}: ${await res.text()}`);
      return;
    }

    const data = await res.json();

    // 4. Check for Piggybacked Remote Commands
    if (data.pending_command && data.pending_command !== 'NONE') {
      console.log(`\n⚡ [COMMAND RECEIVED] Inbound Remote Command: ${data.pending_command}`);

      if (data.pending_command === 'POWER_ON') {
        if (faultCode > 0 || tCore >= 65.0) {
          console.warn('⛔ [REJECTED BY SAFETY INTERLOCK] Cannot Turn ON: Unit currently in thermal overtemp!');
        } else {
          psonActive = 1;
          console.log('✅ [EXECUTED] GPIO 32 pulled HIGH -> ATX Main Rails Energized (ON)!\n');
        }
      } else if (data.pending_command === 'POWER_OFF') {
        psonActive = 0;
        console.log('✅ [EXECUTED] GPIO 32 released LOW -> ATX Main Rails De-energized (OFF)!\n');
      } else if (data.pending_command === 'RESET_FAULT') {
        faultCode = 0;
        console.log('✅ [EXECUTED] Supervisory fault latch reset.\n');
      }
    }
  } catch (err) {
    console.error(`⚠️ [COMMUNICATION ERROR] Could not reach ${TARGET_URL}: ${err.message}`);
  }
}

// Run immediately then repeat every 5 seconds
runSimulationCycle();
setInterval(runSimulationCycle, 5000);
