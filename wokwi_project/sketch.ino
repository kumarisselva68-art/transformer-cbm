/*
  Transformer Condition Monitoring & Predictive Thermal Management System (TMS-ESP32)
  Official Wokwi Simulation Sketch - Rev 3.0 Production Baseline
*/

#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <OneWire.h>
#include <DallasTemperature.h>

// --- PIN ASSIGNMENTS ---
#define I2C_SDA_PIN    21
#define I2C_SCL_PIN    22
#define ONE_WIRE_BUS   27   // DS18B20 1-Wire DQ Bus (with 4.7k pull-up)
#define PS_ON_PIN      32   // Active-Low PS_ON# Driver
#define SW_MAIN_PIN    18   // SPST Main Output Enable Toggle (Active-LOW)
#define SW_SETUP_PIN   23   // SPST Local SoftAP Setup Toggle (Active-LOW)

LiquidCrystal_I2C lcd(0x27, 16, 2);
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

// Mathematical model variables
float t_core = 35.0;
float t_inlet = 28.0;
float t_filtered = 35.0;
float t_predicted = 35.0;
float rate_of_rise = 0.0;
const float alpha = 0.2; // Exponential Moving Average coefficient
const float horizon_seconds = 30.0;

unsigned long lastTick = 0;
bool pson_active = false;

void setup() {
  Serial.begin(115200);
  
  pinMode(PS_ON_PIN, OUTPUT);
  digitalWrite(PS_ON_PIN, LOW); // Main SMPS outputs de-energized initially
  
  pinMode(SW_MAIN_PIN, INPUT_PULLUP);
  pinMode(SW_SETUP_PIN, INPUT_PULLUP);

  Wire.begin(I2C_SDA_PIN, I2C_SCL_PIN);
  lcd.init();
  lcd.backlight();
  
  lcd.setCursor(0, 0);
  lcd.print("Transformer CBM");
  lcd.setCursor(0, 1);
  lcd.print("Rev 3.0 Baseline");
  delay(1500);
  
  sensors.begin();
  int count = sensors.getDeviceCount();
  Serial.printf("[SETUP] %d DS18B20 probes detected on 1-Wire Bus (GPIO 27)\n", count);

  lcd.clear();
}

void loop() {
  unsigned long now = millis();
  if (now - lastTick >= 1000) {
    lastTick = now;

    // 1. Read Switches
    bool sw_main = (digitalRead(SW_MAIN_PIN) == LOW);   // Switch closed to GND = Enabled
    bool sw_setup = (digitalRead(SW_SETUP_PIN) == LOW); // Switch closed to GND = Setup Mode

    // 2. Read Sensors
    sensors.requestTemperatures();
    float raw_core = sensors.getTempCByIndex(0);
    float raw_inlet = (sensors.getDeviceCount() > 1) ? sensors.getTempCByIndex(1) : 28.5;

    if (raw_core != DEVICE_DISCONNECTED_C) {
      t_core = raw_core;
    }
    if (raw_inlet != DEVICE_DISCONNECTED_C) {
      t_inlet = raw_inlet;
    }

    // 3. Mathematical EMA Filtering & Trend Extrapolation
    float prev_filtered = t_filtered;
    t_filtered = (alpha * t_core) + ((1.0 - alpha) * prev_filtered);
    rate_of_rise = t_filtered - prev_filtered; // deg C per sec
    t_predicted = t_filtered + (horizon_seconds * max(0.0f, rate_of_rise));

    // 4. Supervisory Protection Decision
    bool thermal_trip = (t_core >= 65.0 || t_predicted >= 70.0);
    
    if (sw_main && !thermal_trip) {
      pson_active = true;
      digitalWrite(PS_ON_PIN, HIGH); // Pulls PS_ON# to GND -> SMPS Main Rails ON
    } else {
      pson_active = false;
      digitalWrite(PS_ON_PIN, LOW);  // Releases PS_ON# -> SMPS Main Rails CUT
    }

    // 5. Update 16x2 LCD
    static bool screenToggle = false;
    screenToggle = !screenToggle;

    lcd.clear();
    if (!screenToggle) {
      // Screen 1: Temperatures & Delta T
      lcd.setCursor(0, 0);
      lcd.printf("T1:%4.1fC T2:%4.1fC", t_core, t_inlet);
      lcd.setCursor(0, 1);
      lcd.printf("dT:%4.1fC Tp:%4.1fC", (t_core - t_inlet), t_predicted);
    } else {
      // Screen 2: System Status & PS_ON State
      lcd.setCursor(0, 0);
      lcd.printf("Main: %s", pson_active ? "ACTIVE [ON]" : "DE-ENERGIZED");
      lcd.setCursor(0, 1);
      if (thermal_trip) {
        lcd.print("FAULT: OVERTEMP!");
      } else if (sw_setup) {
        lcd.print("MODE: LOCAL AP  ");
      } else {
        lcd.print("SYSTEM: NORMAL  ");
      }
    }

    // 6. Serial Telemetry Log
    Serial.printf("[TELEMETRY] T_Core=%.2f C | T_Inlet=%.2f C | T_Pred=%.2f C | Main_ON=%d | Fault=%d\n",
                  t_core, t_inlet, t_predicted, pson_active, thermal_trip);
  }
}
