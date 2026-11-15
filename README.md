# Transformer CBM — Predictive Adaptive Thermal Management

[![Architecture](https://img.shields.io/badge/Architecture-FreeRTOS%20%7C%20Edge%20Cloud-000000?style=for-the-badge)](https://transformer-cbm.kumarisselva68.workers.dev)
[![Firmware](https://img.shields.io/badge/Firmware-ESP32%20WROOM--32E-f59e0b?style=for-the-badge)](firmware/transformer_cbm_esp32)
[![Cloud](https://img.shields.io/badge/Cloud-Cloudflare%20Workers%20%7C%20D1-f97316?style=for-the-badge)](software)
[![Standards](https://img.shields.io/badge/Compliance-IEEE%20Std%20C57.91-10b981?style=for-the-badge)](documentation)
[![Status](https://img.shields.io/badge/Deployment-Live%20Production-06b6d4?style=for-the-badge)](https://transformer-cbm.kumarisselva68.workers.dev)

A condition-based monitoring (CBM) and autonomous supervisory protection platform for power transformers and switch-mode magnetic components. Combines FreeRTOS dual-core edge telemetry, ordinary least-squares rate-of-rise thermal extrapolation, IEEE Std C57.91 Arrhenius insulation loss-of-life prognostics, and sub-5 millisecond hardware isolation via active-low interlocks.

---

## Live System Deployment

* **Production Edge Dashboard:** [https://transformer-cbm.kumarisselva68.workers.dev](https://transformer-cbm.kumarisselva68.workers.dev)
* **GitHub Repository:** [https://github.com/kumarisselva68-art/transformer-cbm](https://github.com/kumarisselva68-art/transformer-cbm)
* **Target Hardware Platform:** ESP32 WROOM-32E (38-pin DevKit V1)
* **Auxiliary Telemetry:** Continuous +5VSB standby power rail operation

---

## System Architecture

```
                  PHYSICAL HARDWARE TIER
+-------------------------------------------------------------+
| Transformer Core (T1)       Cooling Inlet Airflow (T2)     |
| [DS18B20 1-Wire • GPIO 32]  [DS18B20 1-Wire • GPIO 32]     |
|                                                             |
| +12V Shunt (0x40)    +5V Shunt (0x41)    +3.3V Shunt (0x44) |
| [INA219 Power]       [INA219 Power]      [INA219 Power]     |
|         \                  |                  /             |
|          +----------> I2C Bus [GPIO 21/22] <--+             |
+-------------------------------------------------------------+
                               |
                               v
                     ESP32 FREERTOS CORE
+-------------------------------------------------------------+
| Task_Acquisition (Core 0, 100ms):                           |
|   - 12-Bit Dual DS18B20 1-Wire Acquisition                  |
|   - Triple INA219 Voltage/Current/Power Integration         |
|   - 30-Sample Rolling Ordinary Least Squares Extrapolation  |
|                                                             |
| Task_Supervisory (Core 1, 10ms):                            |
|   - 25 kHz Ultrasonic PWM Dynamic Fan Drive (TB6612FNG)     |
|   - Hardware Safety Interlock Trip (< 5 ms, 2N3904 PS_ON#)  |
|   - Direct 4-Bit Parallel 1602 LCD Telemetry Carousel       |
+-------------------------------------------------------------+
                               |
                 HTTPS / TLS 1.3 Telemetry Stream
                               v
                    CLOUDFLARE EDGE TIER
+-------------------------------------------------------------+
| - Worker Runtime: Serverless REST API                       |
| - Storage: Cloudflare D1 Serverless SQLite Database         |
| - Notifications: Brevo Transactional Email Engine           |
| - Dashboard: Apple / Linear Telemetry SPA & Controls        |
| - Prognostics: IEEE Std C57.91 Arrhenius Life Estimator     |
+-------------------------------------------------------------+
```

---

## Key Engineering Innovations

### 1. Rolling Ordinary Least Squares (OLS) Extrapolation
Rather than reacting solely to static threshold breaches, the local firmware maintains a 30-sample sliding window ($N = 30$, $\Delta t = 1.0\text{ s}$) computing temperature rate-of-rise:

$$\frac{dT}{dt} = \frac{N \sum (t_i T_i) - \sum t_i \sum T_i}{N \sum t_i^2 - (\sum t_i)^2}$$

The 30-second forward projected horizon is derived deterministically:

$$T_{\text{predicted}} = T_{\text{core}} + \left(\frac{dT}{dt}\right) \times 30$$

If $T_{\text{predicted}} \ge 70.0^\circ\text{C}$ or instantaneous $T_{\text{core}} \ge 65.0^\circ\text{C}$, the firmware releases the active-low hardware interlock in under 5 milliseconds.

### 2. IEEE Std C57.91 Arrhenius Insulation Prognostics
Internal winding hot-spot temperature ($T_{\text{HST}}$) is reconstructed using the measured core surface temperature and empirical convective gradient:

$$T_{\text{HST}} = T_{\text{core}} + 0.08 \times \max(0, T_{\text{core}} - T_{\text{inlet}}) + 2.5^\circ\text{C}$$

Relative insulation aging acceleration factor ($F_{\text{AA}}$) is evaluated continuously against the standard 110°C (383.15 K) baseline reference:

$$F_{\text{AA}} = \exp\left( \frac{15000}{383.15} - \frac{15000}{T_{\text{HST}} + 273.15} \right)$$

### 3. Silent 25 kHz Ultrasonic Fan Modulation
Audible motor whine is eliminated by operating the TB6612FNG H-bridge at 25,000 Hz PWM using the ESP32 LEDC timer peripheral, exceeding the human hearing threshold.

### 4. Direct 4-Bit Parallel 1602 LCD Integration
Operates directly from ESP32 GPIOs without intermediary I2C backpack latencies. GPIO 12 is explicitly excluded to eliminate strapping pin contention and avoid corrupting the ESP32 internal flash SPI voltage regulator.

---

## Hardware Pinout Specifications

| Subsystem | Peripheral | ESP32 Pin | Protocol / Signal | Engineering Function |
| :--- | :--- | :--- | :--- | :--- |
| **Fail-Safe Trip** | 2N3904 NPN BJT | **GPIO 4** | Active-Low PS_ON# | Pulls PS_ON# LOW to energize; releases to cut power in < 5 ms |
| **Thermal Sensing** | Dual DS18B20 | **GPIO 32** | 1-Wire Digital | T1 (Winding Hotspot) and T2 (Ambient Air Intake), 4.7k pullup |
| **Power Monitoring** | 3x INA219 Shunts | **GPIO 21 (SDA)<br>GPIO 22 (SCL)** | I2C (400 kHz) | Addresses `0x40` (+12V), `0x41` (+5V), `0x44` (+3.3V) |
| **Fan Modulation** | TB6612FNG Driver | **GPIO 16 (PWMA)<br>GPIO 17 (AIN1)** | 25 kHz Ultrasonic PWM | High-efficiency variable forced convection cooling |
| **Parallel Display** | 1602 Character LCD | **GPIO 13, 14, 27, 26, 25, 33** | 4-Bit Parallel Bus | RS, EN, D4, D5, D6, D7 telemetry carousel (GPIO 12 strictly excluded) |
| **HMI Control** | Push Button | **GPIO 19** | Debounced Input | Cycle LCD telemetry pages (40 ms debounce window) |
| **Interlock Sense** | Rocker Switch | **GPIO 23** | Hardware Interlock | Physical operator safety bypass authorization |
| **Status Beacon** | LED Indicator | **GPIO 18** | Digital Output | System normal heartbeat and fault trip latch indicator |

---

## Repository Directory Structure

```
Transformer_CBM/
├── firmware/
│   └── transformer_cbm_esp32/
│       ├── transformer_cbm_esp32.ino   # Complete production C++ FreeRTOS sketch
│       └── README.md                   # Flashing instructions, pin table & libraries
├── software/
│   ├── public/                         # Apple / Linear Single Page Application
│   │   ├── index.html                  # Responsive interface with themed vector diagrams
│   │   ├── styles.css                  # Industrial design tokens & blueprint grid
│   │   ├── app.js                      # Real-time WebSockets/polling & prognostics engine
│   │   └── assets/                     # Industrial fan SVG & architectural schematics
│   ├── src/
│   │   ├── worker.js                   # Cloudflare Workers API route router
│   │   ├── db.js                       # D1 SQLite query abstraction layer
│   │   ├── email.js                    # Brevo transactional alert dispatcher
│   │   └── auth.js                     # Google OAuth JWT cryptographic validation
│   ├── tests/
│   │   ├── api.test.js                 # Automated unit tests (Node.js test runner)
│   │   └── mock_esp32_simulator.js     # Edge telemetry stress generator
│   ├── schema.sql                      # D1 database initialization script
│   └── wrangler.toml                   # Cloudflare Workers deployment configuration
├── documentation/
│   ├── hardware_commissioning_report.typ  # Typst commissioning report source
│   ├── hardware_commissioning_report.pdf  # Compiled 12-page verification report
│   └── diagrams/                          # Master schematics and block diagrams
├── PPT/                                # Presentation decks and review slides
└── README.md                           # Master repository documentation
```

---

## Firmware Compilation & Flashing

### Requirements
* Arduino IDE 2.x or PlatformIO
* Board: **ESP32 Dev Module**
* Libraries:
  * `OneWire` (Paul Stoffregen)
  * `DallasTemperature` (Miles Burton)
  * `Adafruit_INA219` (Adafruit)
  * `LiquidCrystal` (Built-in Arduino)
  * `ArduinoJson` (Benoit Blanchon, v6.x or v7.x)
  * `WiFi` & `HTTPClient` (ESP32 core)

### Flash Configuration
```
Board: ESP32 Dev Module
Upload Speed: 921600
CPU Frequency: 240MHz (WiFi/BT)
Flash Frequency: 80MHz
Flash Mode: QIO
Flash Size: 4MB (32Mb)
Partition Scheme: Default 4MB with spiffs (1.2MB APP/1.5MB SPIFFS)
Core Debug Level: None
PSRAM: Disabled
```

---

## Edge Software Platform Deployment

### Local Testing
```powershell
cd software
npm install
npm test
```

### Deploying to Cloudflare
```powershell
cd software
$env:CLOUDFLARE_API_TOKEN = "<YOUR_TOKEN>"
$env:CLOUDFLARE_ACCOUNT_ID = "<YOUR_ACCOUNT_ID>"
npx wrangler deploy
```

---

## Presentation Superpowers

* **One-Click Telemetry CSV Export:** Downloads up to 300 records of high-precision multi-sensor telemetry for lab reports and MATLAB modeling.
* **Viva Defense Fault Injection Simulator:** Interactive scenario bench allowing reviewers to trigger a controlled thermal spike to 67.5°C, observing OLS warnings, fan acceleration, and hardware relay isolation in real time.
* **Dynamic Fan PID Transfer Curve:** Responsive SVG piecewise curve illustrating the 4 firmware thermal operating regimes with a real-time tracking marker.
* **Acoustic Industrial Safety Chime:** Pure browser-synthesized dual-tone audio alarm operating via Web Audio API.
* **Operator Keyboard Shortcuts:** Quick-access navigation (`1`-`5` tabs, `T` theme toggle, `E` emergency cutoff, `?` shortcut guide).

---

## Capstone Project Attribution

**Institution:**
Rajalakshmi Institute of Technology, Chennai
Department of Electronics and Communication Engineering
Academic Batch: 2021–2025

**Project Researchers:**
* Selvakumari S &mdash; Reg. No: 211721106085
* Shreya S &mdash; Reg. No: 211721106095
* Susmitha G &mdash; Reg. No: 211721106103

**Project Mentor:**
* Mrs. V. Subashini &mdash; Assistant Professor, Department of ECE

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
