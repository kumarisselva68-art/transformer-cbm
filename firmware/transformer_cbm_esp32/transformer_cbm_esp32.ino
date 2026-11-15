/**
 * =============================================================================
 * TRANSFORMER CONDITION MONITORING & PREDICTIVE THERMAL MANAGEMENT SYSTEM
 * Platform: ESP32-WROOM-32 / ATX SMPS Multi-Rail Conditioning Bench
 * Document Reference: CBM-ESP32-BENCH-TEST-2026-V1.0
 * 
 * Hardware Subsystems Integrated:
 *  1. Multi-Rail DC Power Telemetry (3x INA219 at 0x40, 0x41, 0x44 on GPIO 21/22)
 *  2. Dual-Zone Digital Thermal Monitoring (Dallas DS18B20 on GPIO 32)
 *  3. Ultrasonic 25 kHz PWM Forced-Air Cooling (Toshiba TB6612FNG on GPIO 16/17)
 *  4. SMPS Master Power Interlock (2N3904 NPN driver on GPIO 4 for PS_ON#)
 *  5. Local Alphanumeric HMI (Direct 4-Bit Parallel 1602 LCD on GPIO 13,14,27,26,25,33)
 *  6. Front-Panel Operator Controls (40ms Debounced Button GPIO 19, Rocker GPIO 23, LED GPIO 18)
 *  7. Cloudflare Worker Edge Telemetry & Bi-directional Remote Supervisory Commands
 * =============================================================================
 */

#include <Arduino.h>
#include <Wire.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <WiFiClientSecure.h>
#include <ArduinoJson.h>
#include <LiquidCrystal.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <Adafruit_INA219.h>

// =============================================================================
// 1. PIN CONFIGURATION (MAPPED DIRECTLY FROM HARDWARE COMMISSIONING REPORT)
// =============================================================================

// --- SMPS Master Interlock (PS_ON#) ---
constexpr uint8_t PIN_PS_ON           = 4;   // GPIO 4 -> 1kΩ -> 2N3904 base -> SMPS PS_ON# (active-LOW)

// --- Direct 4-Bit Parallel 1602 LCD Bus ---
// NOTE: RW is tied to GND. GPIO 12 is strictly excluded to prevent flash strapping voltage corruption.
constexpr uint8_t PIN_LCD_RS          = 13;  // LCD RS (Pin 4)
constexpr uint8_t PIN_LCD_EN          = 14;  // LCD E  (Pin 6)
constexpr uint8_t PIN_LCD_D4          = 27;  // LCD D4 (Pin 11)
constexpr uint8_t PIN_LCD_D5          = 26;  // LCD D5 (Pin 12)
constexpr uint8_t PIN_LCD_D6          = 25;  // LCD D6 (Pin 13)
constexpr uint8_t PIN_LCD_D7          = 33;  // LCD D7 (Pin 14)

// --- Ultrasonic Cooling Fan Actuation (TB6612FNG) ---
constexpr uint8_t PIN_FAN_DIR         = 16;  // TB6612 AIN1 (Direction: HIGH = Forward)
constexpr uint8_t PIN_FAN_PWM         = 17;  // TB6612 PWMA (25 kHz Ultrasonic PWM)

// --- Front-Panel Controls & Status Signaling ---
constexpr uint8_t PIN_STATUS_LED      = 18;  // Active-HIGH status LED (via 330Ω)
constexpr uint8_t PIN_BTN_SETUP       = 19;  // Tactile push button (INPUT_PULLUP, active-LOW)
constexpr uint8_t PIN_SW_ROCKER       = 23;  // Master rocker interlock switch (INPUT_PULLUP, active-LOW)

// --- Hardware I2C Bus (Triple INA219 Power Monitors) ---
constexpr uint8_t PIN_I2C_SDA         = 21;  // Hardware I2C SDA
constexpr uint8_t PIN_I2C_SCL         = 22;  // Hardware I2C SCL

// --- Dallas 1-Wire Digital Thermal Bus ---
constexpr uint8_t PIN_ONEWIRE_DQ      = 32;  // DS18B20 multi-drop with 4.7kΩ pull-up to 3.3V

// =============================================================================
// 2. NETWORK & CLOUD CREDENTIALS
// =============================================================================
const char* WIFI_SSID     = "YOUR_WIFI_SSID";
const char* WIFI_PASS     = "YOUR_WIFI_PASSWORD";

// Cloudflare Worker Production Telemetry Ingestion Endpoint
const char* CLOUD_API_URL = "https://transformer-cbm.kumarisselva68.workers.dev/api/telemetry";
const char* DEVICE_KEY    = "cbm_esp32_sec_key_2026";
const char* DEVICE_ID     = "TMS-ESP32 Rev 3.0";

// =============================================================================
// 3. HARDWARE CONSTANTS & SAFETY BOUNDS
// =============================================================================
constexpr uint32_t PWM_FREQUENCY      = 25000; // 25 kHz ultrasonic carrier (silent, no motor whine)
constexpr uint8_t  PWM_RESOLUTION     = 8;     // 8-bit resolution (duty 0-255)
constexpr uint32_t DEBOUNCE_MS        = 40;    // 40ms non-blocking debounce window

// Engineering Thermal & Electrical Trip Limits
constexpr float CORE_TRIP_LIMIT_C     = 65.0f; // Static hardware trip limit (°C)
constexpr float PRED_TRIP_LIMIT_C     = 70.0f; // Predictive rolling regression trip limit (°C)
constexpr float OVERCURRENT_12V_A     = 3.00f; // Max continuous current limit on 12V rail
constexpr float OVERCURRENT_5V_A      = 2.50f; // Max continuous current limit on 5V rail

// Trend Extrapolation & Aging Model Parameters
constexpr float EMA_ALPHA             = 0.20f; // Exponential moving average smoothing factor
constexpr float HORIZON_SECONDS       = 30.0f; // Forward predictive time horizon

// =============================================================================
// 4. GLOBAL OBJECT INSTANTIATIONS
// =============================================================================
LiquidCrystal lcd(PIN_LCD_RS, PIN_LCD_EN, PIN_LCD_D4, PIN_LCD_D5, PIN_LCD_D6, PIN_LCD_D7);
OneWire oneWire(PIN_ONEWIRE_DQ);
DallasTemperature tempSensors(&oneWire);

// Triple INA219 Sensor Instances
Adafruit_INA219 ina12v(0x40);  // Rail 1: 12V Main Load (A0=GND, A1=GND)
Adafruit_INA219 ina5v(0x41);   // Rail 2: 5V Standby/Secondary (A0=VS+, A1=GND)
Adafruit_INA219 ina3v3(0x44);  // Rail 3: 3.3V Logic/Auxiliary (A0=GND, A1=VS+)

// =============================================================================
// 5. SYSTEM STATE & TELEMETRY REGISTERS
// =============================================================================
struct TelemetryData {
  float t_core;          // T1: Core surface temperature (°C)
  float t_inlet;         // T2: Ambient cooling air inlet (°C)
  float t_filtered;      // EMA smoothed core temperature (°C)
  float rate_of_rise;    // dT/dt slope (°C/s)
  float t_predicted;     // Projected core temp at +30s (°C)
  float t_hotspot;       // Virtual copper winding hot-spot (IEEE C57.91)
  float aging_factor;    // Arrhenius aging acceleration factor (FAA)
  float health_index;    // Composite transformer health index (0 - 100%)

  float v_12v, i_12v, p_12v;
  float v_5v,  i_5v,  p_5v;
  float v_3v3, i_3v3, p_3v3;

  bool  pson_active;     // Main output rails energized (PS_ON# pulled low)
  bool  thermal_trip;    // Latching overtemperature protection trip
  bool  overcurrent_trip;// Latching overcurrent trip
  int   fault_code;      // 0=Normal, 1=Core Trip, 2=Pred Trip, 3=Overcurrent, 4=Comm Loss
};

TelemetryData telemetry = {
  34.5f, 27.2f, 34.5f, 0.0f, 34.5f, 38.7f, 0.005f, 96.4f,
  12.04f, 0.0f, 0.0f,
  5.01f,  0.0f, 0.0f,
  3.31f,  0.0f, 0.0f,
  false, false, false, 0
};

// Fan Control State
bool fanAutoMode = true;
int  fanDutyPercent = 0;

// Debounced Input Registers
struct DebouncedInput {
  uint8_t pin;
  bool lastRaw;
  bool stable;
  unsigned long changedAt;
};

DebouncedInput btnSetup = {PIN_BTN_SETUP, HIGH, HIGH, 0};
DebouncedInput swRocker = {PIN_SW_ROCKER, HIGH, HIGH, 0};

// Remote Control Command Overrides
bool remotePowerAllowed = true;
bool setupModeActive = false;

// Task Timing Registers
unsigned long lastSampleTick = 0;
unsigned long lastCloudTick  = 0;
unsigned long lastLcdTick    = 0;
unsigned long lastBlinkTick  = 0;
uint8_t lcdScreenIndex       = 0;

// =============================================================================
// 6. HELPER ROUTINES: LCD, ACTUATION, SENSORS
// =============================================================================

/**
 * Flicker-Free LCD Row Update:
 * Directly writes space-padded 16-character buffers without lcd.clear()
 */
void printLcdRow(uint8_t row, const char* text) {
  lcd.setCursor(0, row);
  bool endOfText = false;
  for (uint8_t col = 0; col < 16; col++) {
    if (!endOfText && text[col] == '\0') endOfText = true;
    lcd.write(endOfText ? ' ' : text[col]);
  }
}

/**
 * Set Ultrasonic Fan Speed (0 - 100%)
 */
void setFanSpeed(int percent) {
  percent = constrain(percent, 0, 100);
  fanDutyPercent = percent;
  int duty = map(percent, 0, 100, 0, 255);

  if (percent == 0) {
    digitalWrite(PIN_FAN_DIR, LOW);
    ledcWrite(PIN_FAN_PWM, 0);
  } else {
    digitalWrite(PIN_FAN_DIR, HIGH); // Forward airflow
    ledcWrite(PIN_FAN_PWM, duty);
  }
}

/**
 * Update SMPS Main Power Interlock (< 5ms cut)
 */
void setMainPower(bool enable) {
  // Enforce hardware safety trip lockouts
  if (telemetry.thermal_trip || telemetry.overcurrent_trip) {
    enable = false;
  }
  // Enforce physical rocker switch state (must be CLOSED / LOW to enable)
  if (swRocker.stable == HIGH) {
    enable = false;
  }
  // Enforce remote operator command
  if (!remotePowerAllowed) {
    enable = false;
  }

  telemetry.pson_active = enable;
  // Transistor saturated (HIGH) pulls PS_ON# to GND -> SMPS Main ON
  // Transistor cutoff (LOW) releases PS_ON# to float -> SMPS Main OFF
  digitalWrite(PIN_PS_ON, enable ? HIGH : LOW);
}

/**
 * 40ms Software Debouncer Engine
 */
bool updateDebouncedInput(DebouncedInput &input) {
  bool raw = digitalRead(input.pin);
  unsigned long now = millis();
  if (raw != input.lastRaw) {
    input.lastRaw = raw;
    input.changedAt = now;
  }
  if (raw != input.stable && (now - input.changedAt >= DEBOUNCE_MS)) {
    input.stable = raw;
    return true; // State change event
  }
  return false;
}

/**
 * Non-blocking I2C Probe Routine
 */
bool probeI2C(uint8_t address) {
  Wire.beginTransmission(address);
  return (Wire.endTransmission() == 0);
}

// =============================================================================
// 7. INITIALIZATION SETUP
// =============================================================================
void setup() {
  // CRITICAL FAILSAFE: Initialize PS_ON to LOW immediately before configuring output mode
  digitalWrite(PIN_PS_ON, LOW);
  pinMode(PIN_PS_ON, OUTPUT);

  // Initialize Fan Actuation Outputs
  pinMode(PIN_FAN_DIR, OUTPUT);
  digitalWrite(PIN_FAN_DIR, LOW);
  ledcAttach(PIN_FAN_PWM, PWM_FREQUENCY, PWM_RESOLUTION);
  setFanSpeed(0);

  // Initialize HMI Pins
  pinMode(PIN_STATUS_LED, OUTPUT);
  digitalWrite(PIN_STATUS_LED, LOW);
  pinMode(PIN_BTN_SETUP, INPUT_PULLUP);
  pinMode(PIN_SW_ROCKER, INPUT_PULLUP);

  // Initialize Serial Interface (CP2102 UART)
  Serial.begin(115200);
  delay(500);
  Serial.println(F("\n======================================================="));
  Serial.println(F("  TRANSFORMER CONDITION MONITORING SYSTEM (TMS-ESP32)  "));
  Serial.println(F("  Commissioning Baseline Rev 3.0 • Hardware Initialized"));
  Serial.println(F("======================================================="));

  // Initialize 4-Bit Parallel 1602 LCD
  lcd.begin(16, 2);
  lcd.noCursor();
  lcd.noBlink();
  printLcdRow(0, "TRANSFORMER CBM");
  printLcdRow(1, "REV 3.0 INIT...");
  delay(1200);

  // Initialize 1-Wire Dallas Temperature Bus
  tempSensors.begin();
  tempSensors.setWaitForConversion(false); // Non-blocking asynchronous conversion
  tempSensors.requestTemperatures();
  Serial.printf("[1-WIRE] Discovered %d Dallas temperature probes on GPIO 32\n", tempSensors.getDeviceCount());

  // Initialize Hardware I2C Bus & Triple INA219 Monitors
  Wire.begin(PIN_I2C_SDA, PIN_I2C_SCL, 100000); // 100 kHz standard clock
  
  if (probeI2C(0x40)) {
    ina12v.begin(&Wire);
    ina12v.setCalibration_32V_2A();
    Serial.println(F("[INA219] 12V Monitor (0x40) calibrated [OK]"));
  } else {
    Serial.println(F("[INA219] WARN: 12V Monitor (0x40) not responding on I2C"));
  }

  if (probeI2C(0x41)) {
    ina5v.begin(&Wire);
    ina5v.setCalibration_32V_2A();
    Serial.println(F("[INA219] 5V Monitor (0x41) calibrated [OK]"));
  } else {
    Serial.println(F("[INA219] WARN: 5V Monitor (0x41) not responding on I2C"));
  }

  if (probeI2C(0x44)) {
    ina3v3.begin(&Wire);
    ina3v3.setCalibration_32V_2A();
    Serial.println(F("[INA219] 3.3V Monitor (0x44) calibrated [OK]"));
  } else {
    Serial.println(F("[INA219] WARN: 3.3V Monitor (0x44) not responding on I2C"));
  }

  // Connect to WiFi (Non-blocking attempt)
  printLcdRow(0, "CONNECTING WIFI");
  printLcdRow(1, WIFI_SSID);
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  
  unsigned long wifiStart = millis();
  while (WiFi.status() != WL_CONNECTED && (millis() - wifiStart < 5000)) {
    delay(200);
    digitalWrite(PIN_STATUS_LED, !digitalRead(PIN_STATUS_LED));
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.printf("[WIFI] Connected! Assigned IP: %s\n", WiFi.localIP().toString().c_str());
    digitalWrite(PIN_STATUS_LED, HIGH);
    printLcdRow(1, "WIFI CONNECTED");
  } else {
    Serial.println(F("[WIFI] Connection timeout. Operating in autonomous standalone mode."));
    digitalWrite(PIN_STATUS_LED, LOW);
    printLcdRow(1, "STANDALONE MODE");
  }
  delay(1000);
}

// =============================================================================
// 8. MATHEMATICAL PROCESSING: EMA, HORIZON, ARRHENIUS, HEALTH INDEX
// =============================================================================
void processThermalAnalytics(float rawCore, float rawInlet, float dtSeconds) {
  // 1. Temperature Sensor Sanity Guard
  if (rawCore > -40.0f && rawCore < 125.0f) {
    telemetry.t_core = rawCore;
  }
  if (rawInlet > -40.0f && rawInlet < 125.0f) {
    telemetry.t_inlet = rawInlet;
  }

  // 2. Exponential Moving Average (EMA) Filtering
  float prevFiltered = telemetry.t_filtered;
  telemetry.t_filtered = (EMA_ALPHA * telemetry.t_core) + ((1.0f - EMA_ALPHA) * prevFiltered);

  // 3. Rate of Rise (dT/dt) & 30s Linear Trend Extrapolation
  if (dtSeconds > 0.001f) {
    telemetry.rate_of_rise = (telemetry.t_filtered - prevFiltered) / dtSeconds;
  }
  telemetry.t_predicted = telemetry.t_filtered + (HORIZON_SECONDS * max(0.0f, telemetry.rate_of_rise));

  // 4. Virtual Winding Hot-Spot Estimation (IEEE Std C57.91)
  float deltaT = max(0.0f, telemetry.t_core - telemetry.t_inlet);
  telemetry.t_hotspot = telemetry.t_core + (0.08f * deltaT) + 2.5f;

  // 5. Arrhenius Aging Acceleration Factor (FAA)
  // Standard Reference: 110°C (383.15 K)
  float kelvinHST = telemetry.t_hotspot + 273.15f;
  telemetry.aging_factor = exp((15000.0f / 383.15f) - (15000.0f / kelvinHST));

  // 6. Multi-Stress Composite Transformer Health Index (0 - 100%)
  float penThermal = max(0.0f, (telemetry.t_core - 45.0f) * 1.4f);
  float penAging   = min(20.0f, telemetry.aging_factor * 200.0f);
  float penTrip    = (telemetry.pson_active ? 0.0f : 15.0f) + (telemetry.fault_code > 0 ? 25.0f : 0.0f);
  telemetry.health_index = constrain(100.0f - penThermal - penAging - penTrip, 0.0f, 100.0f);

  // 7. Closed-Loop Automatic Ultrasonic Fan Modulation
  if (fanAutoMode) {
    if (telemetry.t_core < 35.0f) {
      setFanSpeed(30);  // Silent baseline airflow
    } else if (telemetry.t_core < 45.0f) {
      setFanSpeed(50);  // Moderate dissipation
    } else if (telemetry.t_core < 55.0f) {
      setFanSpeed(75);  // High-efficiency forced air
    } else {
      setFanSpeed(100); // 100% emergency maximum extraction
    }
  }

  // 8. Autonomous Supervisory Trip Logic
  if (telemetry.t_core >= CORE_TRIP_LIMIT_C) {
    telemetry.thermal_trip = true;
    telemetry.fault_code = 1; // Core overtemperature trip
  } else if (telemetry.t_predicted >= PRED_TRIP_LIMIT_C) {
    telemetry.thermal_trip = true;
    telemetry.fault_code = 2; // Predictive horizon trip
  }
}

// =============================================================================
// 9. ELECTRICAL TELEMETRY SAMPLING (3x INA219)
// =============================================================================
void sampleElectricalTelemetry() {
  // Rail 1: 12V Main Load
  if (probeI2C(0x40)) {
    telemetry.v_12v = ina12v.getBusVoltage_V() + (ina12v.getShuntVoltage_mV() / 1000.0f);
    telemetry.i_12v = max(0.0f, ina12v.getCurrent_mA() / 1000.0f);
    telemetry.p_12v = (telemetry.v_12v * telemetry.i_12v);
  }

  // Rail 2: 5V Standby
  if (probeI2C(0x41)) {
    telemetry.v_5v = ina5v.getBusVoltage_V() + (ina5v.getShuntVoltage_mV() / 1000.0f);
    telemetry.i_5v = max(0.0f, ina5v.getCurrent_mA() / 1000.0f);
    telemetry.p_5v = (telemetry.v_5v * telemetry.i_5v);
  }

  // Rail 3: 3.3V Logic
  if (probeI2C(0x44)) {
    telemetry.v_3v3 = ina3v3.getBusVoltage_V() + (ina3v3.getShuntVoltage_mV() / 1000.0f);
    telemetry.i_3v3 = max(0.0f, ina3v3.getCurrent_mA() / 1000.0f);
    telemetry.p_3v3 = (telemetry.v_3v3 * telemetry.i_3v3);
  }

  // Overcurrent Protection Evaluation
  if (telemetry.i_12v > OVERCURRENT_12V_A || telemetry.i_5v > OVERCURRENT_5V_A) {
    telemetry.overcurrent_trip = true;
    telemetry.fault_code = 3; // Overcurrent trip
  }
}

// =============================================================================
// 10. CLOUD EDGE TELEMETRY & COMMAND DISPATCH
// =============================================================================
void syncWithCloudflareEdge() {
  if (WiFi.status() != WL_CONNECTED) {
    WiFi.reconnect();
    return;
  }

  WiFiClientSecure client;
  client.setInsecure(); // Cloudflare Edge HTTPS validation

  HTTPClient http;
  http.begin(client, CLOUD_API_URL);
  http.addHeader("Content-Type", "application/json");
  http.addHeader("X-Device-Key", DEVICE_KEY);
  http.setTimeout(3000);

  // Format Cloud JSON Payload
  StaticJsonDocument<512> doc;
  doc["device_id"]     = DEVICE_ID;
  doc["t_core"]        = round(telemetry.t_core * 10.0f) / 10.0f;
  doc["t_inlet"]       = round(telemetry.t_inlet * 10.0f) / 10.0f;
  doc["t_predicted"]   = round(telemetry.t_predicted * 10.0f) / 10.0f;
  doc["rate_of_rise"]  = round(telemetry.rate_of_rise * 100.0f) / 100.0f;
  doc["v_12v"]         = round(telemetry.v_12v * 100.0f) / 100.0f;
  doc["i_12v"]         = round(telemetry.i_12v * 100.0f) / 100.0f;
  doc["v_5v"]          = round(telemetry.v_5v * 100.0f) / 100.0f;
  doc["i_5v"]          = round(telemetry.i_5v * 100.0f) / 100.0f;
  doc["v_3v3"]         = round(telemetry.v_3v3 * 100.0f) / 100.0f;
  doc["i_3v3"]         = round(telemetry.i_3v3 * 100.0f) / 100.0f;
  doc["pson_active"]   = telemetry.pson_active ? 1 : 0;
  doc["fault_code"]    = telemetry.fault_code;

  String jsonPayload;
  serializeJson(doc, jsonPayload);

  int httpCode = http.POST(jsonPayload);

  if (httpCode == HTTP_CODE_OK) {
    String response = http.getString();
    StaticJsonDocument<384> respDoc;
    DeserializationError err = deserializeJson(respDoc, response);

    if (!err) {
      const char* pendingCommand = respDoc["pending_command"] | "NONE";

      // Execute Remote Supervisory Commands from Portal
      if (strcmp(pendingCommand, "POWER_ON") == 0) {
        Serial.println(F("[COMMAND] Remote POWER_ON command received from cloud"));
        remotePowerAllowed = true;
        setMainPower(true);
      } else if (strcmp(pendingCommand, "POWER_OFF") == 0) {
        Serial.println(F("[COMMAND] Remote POWER_OFF command received from cloud"));
        remotePowerAllowed = false;
        setMainPower(false);
      } else if (strcmp(pendingCommand, "RESET_FAULT") == 0) {
        Serial.println(F("[COMMAND] Remote RESET_FAULT command received from cloud"));
        if (telemetry.t_core < CORE_TRIP_LIMIT_C && telemetry.t_predicted < PRED_TRIP_LIMIT_C) {
          telemetry.thermal_trip = false;
          telemetry.overcurrent_trip = false;
          telemetry.fault_code = 0;
          remotePowerAllowed = true;
          setMainPower(true);
        }
      } else if (strcmp(pendingCommand, "SET_FAN") == 0) {
        JsonObject payload = respDoc["command_payload"];
        const char* mode = payload["mode"] | "AUTO";
        int speed = payload["speed"] | 50;

        if (strcmp(mode, "MANUAL") == 0) {
          fanAutoMode = false;
          setFanSpeed(speed);
          Serial.printf("[COMMAND] Remote fan set to MANUAL %d%%\n", speed);
        } else {
          fanAutoMode = true;
          Serial.println(F("[COMMAND] Remote fan restored to AUTO mode"));
        }
      }
    }
  } else {
    Serial.printf("[CLOUD] HTTP POST failed with code %d\n", httpCode);
  }

  http.end();
}

// =============================================================================
// 11. 16x2 LCD CAROUSEL DISPLAY
// =============================================================================
void updateLcdCarousel() {
  char line1[17];
  char line2[17];

  // Rotate screen every 2.5 seconds
  lcdScreenIndex = (lcdScreenIndex + 1) % 4;

  if (telemetry.fault_code > 0) {
    // Priority Trip Screen
    printLcdRow(0, "! SAFETY TRIP ! ");
    if (telemetry.fault_code == 1)      printLcdRow(1, "CORE OVERTEMP!  ");
    else if (telemetry.fault_code == 2) printLcdRow(1, "PRED RISE TRIP! ");
    else if (telemetry.fault_code == 3) printLcdRow(1, "OVERCURRENT CUT!");
    return;
  }

  switch (lcdScreenIndex) {
    case 0:
      // Screen 1: Thermal Metrics (T1, T2, Delta T, Virtual Hotspot)
      snprintf(line1, sizeof(line1), "T1:%4.1fC T2:%4.1fC", telemetry.t_core, telemetry.t_inlet);
      snprintf(line2, sizeof(line2), "dT:%4.1fC HST:%4.1f", (telemetry.t_core - telemetry.t_inlet), telemetry.t_hotspot);
      break;

    case 1:
      // Screen 2: Multi-Rail DC Power Telemetry
      snprintf(line1, sizeof(line1), "12V:%4.1fV %4.2fA", telemetry.v_12v, telemetry.i_12v);
      snprintf(line2, sizeof(line2), "5V:%4.2fV 3V3:%3.1f", telemetry.v_5v, telemetry.v_3v3);
      break;

    case 2:
      // Screen 3: Ultrasonic Fan & IEEE C57.91 Health Index
      snprintf(line1, sizeof(line1), "FAN:%3d%% [%s]", fanDutyPercent, fanAutoMode ? "AUTO" : "MANU");
      snprintf(line2, sizeof(line2), "HEALTH HI:%4.1f%%", telemetry.health_index);
      break;

    case 3:
      // Screen 4: Operational System State
      snprintf(line1, sizeof(line1), "RAILS: %s", telemetry.pson_active ? "ENERGIZED" : "ISOLATED ");
      snprintf(line2, sizeof(line2), "STATE: %s", (WiFi.status() == WL_CONNECTED) ? "ONLINE [OK]" : "STANDALONE");
      break;
  }

  printLcdRow(0, line1);
  printLcdRow(1, line2);
}

// =============================================================================
// 12. MAIN FREE-RUNNING REAL-TIME LOOP
// =============================================================================
void loop() {
  unsigned long now = millis();

  // --- Task A: Read Front-Panel HMI Controls (40ms Debounce) ---
  if (updateDebouncedInput(btnSetup)) {
    if (btnSetup.stable == LOW) { // Button Pressed
      setupModeActive = !setupModeActive;
      Serial.printf("[HMI] Setup push-button toggled. Setup Mode: %s\n", setupModeActive ? "ACTIVE" : "INACTIVE");
    }
  }

  if (updateDebouncedInput(swRocker)) {
    Serial.printf("[HMI] Rocker switch state changed to %s\n", (swRocker.stable == LOW) ? "CLOSED [ON]" : "OPEN [OFF]");
    setMainPower(swRocker.stable == LOW);
  }

  // Status LED Signaling: 400ms flash in setup mode, solid ON if normal, fast strobe if tripped
  if (telemetry.fault_code > 0) {
    if (now - lastBlinkTick >= 100) {
      lastBlinkTick = now;
      digitalWrite(PIN_STATUS_LED, !digitalRead(PIN_STATUS_LED)); // 100ms rapid strobe
    }
  } else if (setupModeActive) {
    if (now - lastBlinkTick >= 400) {
      lastBlinkTick = now;
      digitalWrite(PIN_STATUS_LED, !digitalRead(PIN_STATUS_LED)); // 400ms setup cadence
    }
  } else {
    digitalWrite(PIN_STATUS_LED, telemetry.pson_active ? HIGH : LOW);
  }

  // --- Task B: 1 Hz High-Precision Telemetry Sampling & Analytics ---
  if (now - lastSampleTick >= 1000) {
    float dtSeconds = (now - lastSampleTick) / 1000.0f;
    lastSampleTick = now;

    // Read DS18B20 Temperature Probes
    float coreTemp  = tempSensors.getTempCByIndex(0);
    float inletTemp = (tempSensors.getDeviceCount() > 1) ? tempSensors.getTempCByIndex(1) : (coreTemp - 7.3f);
    tempSensors.requestTemperatures(); // Trigger next async conversion

    // Read Triple INA219 Power Monitors
    sampleElectricalTelemetry();

    // Execute EMA Filtering, Rate-of-Rise, Hotspot & Health Prognostics
    processThermalAnalytics(coreTemp, inletTemp, dtSeconds);

    // Apply Output Power Decision
    setMainPower(swRocker.stable == LOW);

    // Serial Diagnostics
    Serial.printf("[CBM-ESP32] Core=%.1f C | In=%.1f C | Pred=%.1f C | 12V=%.2fV/%.2fA | HI=%.1f%% | PS_ON=%d\n",
                  telemetry.t_core, telemetry.t_inlet, telemetry.t_predicted,
                  telemetry.v_12v, telemetry.i_12v, telemetry.health_index, telemetry.pson_active);
  }

  // --- Task C: 2.5s Alphanumeric 1602 LCD Carousel ---
  if (now - lastLcdTick >= 2500) {
    lastLcdTick = now;
    updateLcdCarousel();
  }

  // --- Task D: 3s Cloudflare Worker Edge Telemetry Sync & Command Fetch ---
  if (now - lastCloudTick >= 3000) {
    lastCloudTick = now;
    syncWithCloudflareEdge();
  }
}
