# Transformer CBM — ESP32 Production Firmware
**Platform:** ESP32 Dev Module (WROOM-32)  
**Document Reference:** `CBM-ESP32-BENCH-TEST-2026-V1.0`  
**Target:** IoT-Based Transformer Condition Monitoring & Predictive Thermal Management System

---

## 1. Subsystems & Wiring Allocation

All pins match the physical circuit validated in `documentation/hardware_commissioning_report.pdf`:

| Subsystem | Peripheral | ESP32 GPIO | Net Name | Electrical Characteristics & Notes |
| :--- | :--- | :--- | :--- | :--- |
| **SMPS Master Power** | 2N3904 NPN Base | **GPIO 4** | `PS_ON_CMD` | Output LOW on boot. HIGH saturates 2N3904 to pull `PS_ON#` to GND. |
| **Parallel 1602 LCD** | LCD RS (Pin 4) | **GPIO 13** | `LCD_RS` | Register select (LOW = Command, HIGH = Data). |
| **Parallel 1602 LCD** | LCD E (Pin 6) | **GPIO 14** | `LCD_E` | Enable strobe. |
| **Cooling Fan Actuation** | TB6612 AIN1 | **GPIO 16** | `FAN_DIR` | Direction control (repurposed RX2). HIGH = Forward. |
| **Cooling Fan Actuation** | TB6612 PWMA | **GPIO 17** | `FAN_PWM` | **25 kHz Ultrasonic PWM** (silent, zero acoustic coil whine). |
| **Status Indicator** | 5mm LED + 330Ω | **GPIO 18** | `STATUS_LED` | Active-HIGH push-pull output with dynamic state strobe patterns. |
| **Tactile Push Button** | Push Button (SW1) | **GPIO 19** | `BTN_SETUP` | `INPUT_PULLUP`. Active-LOW. Short tap cycles LCD; Long hold toggles Local AP. |
| **Hardware I2C Bus** | 3x INA219 (SDA) | **GPIO 21** | `I2C_SDA` | I2C Data bus. 100 kHz clock speed. |
| **Hardware I2C Bus** | 3x INA219 (SCL) | **GPIO 22** | `I2C_SCL` | I2C Clock bus. 100 kHz clock speed. |
| **Master Rocker Interlock**| Rocker Switch (SW2)| **GPIO 23** | `SW_ROCKER` | `INPUT_PULLUP`. Active-LOW. Governs GPIO 4 transistor command. |
| **Parallel 1602 LCD** | LCD D6 (Pin 13) | **GPIO 25** | `LCD_D6` | 4-bit data bus line 2. |
| **Parallel 1602 LCD** | LCD D5 (Pin 12) | **GPIO 26** | `LCD_D5` | 4-bit data bus line 1. |
| **Parallel 1602 LCD** | LCD D4 (Pin 11) | **GPIO 27** | `LCD_D4` | 4-bit data bus line 0. |
| **Dallas 1-Wire Bus** | 2x DS18B20 (DQ) | **GPIO 32** | `ONEWIRE_DQ`| Multi-drop thermal bus with 4.7 kΩ pull-up to +3.3V. |
| **Parallel 1602 LCD** | LCD D7 (Pin 14) | **GPIO 33** | `LCD_D7` | 4-bit data bus line 3. |

> **Critical Strapping Pin Notice:**  
> **GPIO 12 (MTDI)** is deliberately **left disconnected**. Sampling GPIO 12 HIGH during boot forces the internal flash LDO to 1.8V, corrupting 3.3V SPI flash and causing permanent bootloops.

---

## 2. INA219 I2C Address Strapping

The three INA219 breakout boards share the I2C bus (`GPIO 21 / 22`) using hardware address jumpers:
- **Sensor 1 (`0x40`):** 12V Main Output Rail (A0 = GND, A1 = GND)
- **Sensor 2 (`0x41`):** 5V Standby / Auxiliary Rail (A0 = VS+, A1 = GND)
- **Sensor 3 (`0x44`):** 3.3V Logic Rail (A0 = GND, A1 = VS+)

---

## 3. Front-Panel Operator Controls & LED Telemetry

### Button Dual-Action Logic (GPIO 19)
- **Short Tap (< 1.5s):** Immediately advances to the next 1602 LCD diagnostic screen without waiting for the automatic 2.5-second carousel timer.
- **Long Hold (>= 2.0s):** Toggles the embedded **Local SoftAP & Web Console Server**. The LCD displays `AP: CBM-AP / IP: 192.168.4.1`, and the DNS captive portal activates.

### 1602 LCD Telemetry Carousel Pages
- **Screen 0:** Core ($T_1$), Inlet ($T_2$), Delta $T$ ($\Delta T$), and Virtual Hotspot ($T_{\text{HST}}$).
- **Screen 1:** Multi-rail DC power telemetry (+12V, +5V, +3.3V voltage & current).
- **Screen 2:** Ultrasonic fan duty cycle % and IEEE Std C57.91 Health Index (HI %).
- **Screen 3:** Output rail energization status and Wi-Fi station IP address.
- **Screen 4:** Local SoftAP status and gateway IP address (`192.168.4.1`).
- *Emergency Override:* Any overtemperature or overcurrent event immediately forces the display to `! SAFETY TRIP !`.

### Multi-Pattern LED Signaling (GPIO 18)

| Optical Flash Cadence | Operational State | Hardware Meaning |
| :--- | :--- | :--- |
| **Solid Continuous ON** | Normal Nominal Operation | Main rails energized (`PS_ON#` active LOW), Wi-Fi station connected |
| **1 Hz Cadence (500ms ON / 500ms OFF)** | Local SoftAP Active | Local configuration web portal running on `192.168.4.1` |
| **Double-Strobe (every 2000ms)** | Disconnected / Standalone | Operating autonomously without active Wi-Fi connection |
| **Rapid Strobe (10 Hz / 100ms)** | Latching Safety Trip | Core overtemperature, rate-of-rise excursion, or overcurrent lockout |

---

## 4. Local Embedded Web Console (Zero-CDN)

When Local AP mode is active (or automatically upon boot Wi-Fi timeout), the ESP32 serves a self-contained, responsive Apple/Linear styled dashboard directly from PROGMEM:
- **SoftAP Network:** `TRANSFORMER-CBM-AP` (Password: `12345678`)
- **Console Gateway:** `http://192.168.4.1/` (Captive DNS server auto-redirects mobile browsers)
- **Zero External Dependencies:** 100% offline operation with zero CDN or cloud asset requirements.
- **Local Control Capabilities:**
  - Real-time 1 Hz telemetry metrics and rail diagnostics.
  - Emergency Main Power Cutoff & Energize toggles.
  - Manual fan duty cycle PWM slider (0% to 100%) and Auto-PID restore.
  - Safety trip fault clear.
  - 2.4 GHz spectrum scanner and Wi-Fi credential provisioning saved to ESP32 non-volatile storage (`Preferences` NVS).

---

## 5. Required Arduino Libraries

Install the following libraries via the Arduino IDE Library Manager (`Ctrl + Shift + I`):
1. **ArduinoJson** by *Benoît Blanchon* (v6.x or v7.x)
2. **Adafruit INA219** by *Adafruit* (v2.2+)
3. **DallasTemperature** by *Miles Burton* (v3.9+)
4. **OneWire** by *Paul Stoffregen* (v2.3+)
5. **LiquidCrystal** (Built-in standard library)
6. **WebServer**, **DNSServer**, **Preferences** (Standard built-in ESP32 core libraries)

---

## 6. Flashing Configuration (Arduino IDE)

1. Connect the ESP32 Dev Module via micro-USB (Silicon Labs CP2102 UART bridge).
2. In Arduino IDE:
   - **Board:** `ESP32 Dev Module`
   - **CPU Frequency:** `240MHz (WiFi/BT)`
   - **Flash Frequency:** `80MHz`
   - **Flash Mode:** `QIO`
   - **Flash Size:** `4MB (32Mb)`
   - **Partition Scheme:** `Default 4MB with spiffs (1.2MB APP/1.5MB SPIFFS)`
   - **Upload Speed:** `921600` or `115200`
3. Click **Upload**.
4. Open Serial Monitor at **115200 baud** to observe live commissioning telemetry.
