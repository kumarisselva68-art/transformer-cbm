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
| **Status Indicator** | 5mm LED + 330Ω | **GPIO 18** | `STATUS_LED` | Active-HIGH push-pull output. Blinks at 400ms in setup mode. |
| **Tactile Push Button** | Push Button (SW1) | **GPIO 19** | `BTN_SETUP` | `INPUT_PULLUP`. Active-LOW. 40ms software debounced. |
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

## 3. Required Arduino Libraries

Install the following libraries via the Arduino IDE Library Manager (`Ctrl + Shift + I`):
1. **ArduinoJson** by *Benoît Blanchon* (v6.x or v7.x)
2. **Adafruit INA219** by *Adafruit* (v2.2+)
3. **DallasTemperature** by *Miles Burton* (v3.9+)
4. **OneWire** by *Paul Stoffregen* (v2.3+)
5. **LiquidCrystal** (Built-in standard library)

---

## 4. Flashing Configuration (Arduino IDE)

1. Connect the ESP32 Dev Module via micro-USB (Silicon Labs CP2102 UART bridge).
2. In Arduino IDE:
   - **Board:** `ESP32 Dev Module`
   - **CPU Frequency:** `240MHz (WiFi/BT)`
   - **Flash Frequency:** `80MHz`
   - **Flash Mode:** `QIO`
   - **Flash Size:** `4MB (32Mb)`
   - **Partition Scheme:** `Default 4MB with spiffs (1.2MB APP/1.5MB SPIFFS)`
   - **Upload Speed:** `921600` or `115200`
3. Edit your local WiFi credentials in `transformer_cbm_esp32.ino`:
   ```cpp
   const char* WIFI_SSID = "YOUR_WIFI_SSID";
   const char* WIFI_PASS = "YOUR_WIFI_PASSWORD";
   ```
4. Click **Upload**.
5. Open Serial Monitor at **115200 baud** to observe live commissioning telemetry.

---

## 5. Cloud Ingestion & Edge Synchronization

- **Cloud Endpoint:** `https://transformer-cbm.kumarisselva68.workers.dev/api/telemetry`
- **Device Security Key:** `cbm_esp32_sec_key_2026`
- **Cadence:** Telemetry syncs every 3.0 seconds.
- **Bi-directional Supervisory Actions:** The firmware ingests pending remote commands (`POWER_ON`, `POWER_OFF`, `RESET_FAULT`, `SET_FAN`) dispatched from the authenticated web portal.
- **Fail-safe Standalone Operation:** If WiFi is disconnected, the autonomous FreeRTOS loop maintains continuous local LCD carousel updates, 25 kHz closed-loop fan regulation, and $<5\text{ ms}$ overtemperature interlock protection without crashing.
