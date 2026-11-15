# ESP32 Firmware Cloud Integration Guide

This guide explains how to connect your ESP32 Arduino/ESP-IDF firmware to the Cloudflare Worker backend to stream telemetry and process remote **Turn ON / Turn OFF** commands.

---

## 1. Network & Protocol Architecture

* **Protocol:** HTTPS REST (TLS 1.3 encrypted)
* **Ingestion Method:** `POST /api/telemetry`
* **Handshake Interval:** Every 5 to 10 seconds (in a non-blocking FreeRTOS task)
* **Authentication Header:** `X-Device-Key: <SECRET_KEY>`
* **Command Execution:** Piggybacked in the HTTPS response (zero incoming router port forwarding required).

---

## 2. Production Arduino C++ Code Template

Add the following routines to your ESP32 project:

```cpp
#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <HTTPClient.h>
#include <ArduinoJson.h> // ArduinoJson v6 or v7

// Configuration
const char* WIFI_SSID     = "Your_WiFi_SSID";
const char* WIFI_PASSWORD = "Your_WiFi_Password";
const char* WORKER_URL    = "https://transformer-cbm-backend.<your-subdomain>.workers.dev/api/telemetry";
const char* DEVICE_KEY    = "cbm_esp32_sec_key_2026";
const char* DEVICE_ID     = "TRANSFORMER_01";

#define PS_ON_PIN 32 // Active-Low ATX SMPS control (HIGH = ON, LOW = OFF)

extern float t_core;
extern float t_inlet;
extern float t_predicted;
extern float rate_of_rise;
extern bool pson_active;
extern int fault_code;

void sendTelemetryToCloud() {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("[WIFI] Offline. Telemetry deferred.");
    return;
  }

  WiFiClientSecure client;
  client.setInsecure(); // Uses TLS encryption without hardcoding expiring root certs

  HTTPClient http;
  http.begin(client, WORKER_URL);
  http.addHeader("Content-Type", "application/json");
  http.addHeader("X-Device-Key", DEVICE_KEY);

  // 1. Serialize Telemetry Payload
  StaticJsonDocument<384> doc;
  doc["device_id"]    = DEVICE_ID;
  doc["t_core"]       = t_core;
  doc["t_inlet"]      = t_inlet;
  doc["t_predicted"]  = t_predicted;
  doc["rate_of_rise"] = rate_of_rise;
  doc["v_12v"]        = 12.04; // Read from INA219
  doc["i_12v"]        = 2.85;  // Read from INA219
  doc["pson_active"]  = pson_active ? 1 : 0;
  doc["fault_code"]   = fault_code;

  String jsonPayload;
  serializeJson(doc, jsonPayload);

  // 2. Transmit HTTPS POST
  int httpCode = http.POST(jsonPayload);

  if (httpCode == HTTP_CODE_OK) {
    String response = http.getString();
    
    // 3. Parse Piggybacked Remote Command
    StaticJsonDocument<256> respDoc;
    DeserializationError err = deserializeJson(respDoc, response);

    if (!err) {
      const char* command = respDoc["pending_command"] | "NONE";

      if (strcmp(command, "POWER_ON") == 0) {
        // Enforce Local Hardware Safety Interlock
        if (t_core < 65.0 && t_predicted < 70.0) {
          pson_active = true;
          digitalWrite(PS_ON_PIN, HIGH); // Pulls PS_ON# to GND -> SMPS ON
          Serial.println("[CLOUD_CMD] Executed Remote Turn ON");
        } else {
          Serial.println("[SAFETY] Rejected Turn ON: Core overtemperature detected!");
        }
      } else if (strcmp(command, "POWER_OFF") == 0) {
        pson_active = false;
        digitalWrite(PS_ON_PIN, LOW); // Releases PS_ON# -> SMPS OFF
        Serial.println("[CLOUD_CMD] Executed Remote Turn OFF");
      }
    }
  } else {
    Serial.printf("[HTTP] POST failed, error code: %d\n", httpCode);
  }

  http.end();
}
```

---

## 3. Wi-Fi SoftAP Provisioning Fallback

When operating in the field where router credentials may change:
* Hold the **Setup Switch (GPIO 23)** to GND during boot.
* The ESP32 switches to SoftAP mode (`SSID: ESP32-TMS-SETUP`, IP: `192.168.4.1`).
* Connect via any smartphone or laptop browser, enter the new router SSID/password, and save to flash (NVS).
