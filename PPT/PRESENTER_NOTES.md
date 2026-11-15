# Transformer Condition Monitoring System — Presenter Notes

**Project:** IoT-Based Transformer Condition Monitoring with Predictive Adaptive Thermal Management Using ESP32  
**Execution Platform:** ATX Switch-Mode Power Supply (SMPS) Demonstration Testbed  
**Deck Format:** 21-Slide Academic Engineering Presentation (16:9 Widescreen)  
**Theme:** Clean Light Academic — Forest Green (#15803D), Slate Text (#111827), Soft Mint (#F0FDF4), and Pure White (#FFFFFF)  
**Team Members:** Selvakumari S (211721106085), Shreya S (211721106095), Susmitha G (211721106103)  
**Project Mentor:** Mrs. V. Subashini (Assistant Professor, Dept. of ECE, Rajalakshmi Institute of Technology)  

---

### Slide 01 — Title Page
* **Title:** IoT-Based Transformer Condition Monitoring with Predictive Adaptive Thermal Management Using ESP32
* **Subtitle:** Demonstration Platform Executed on an ATX Switch-Mode Power Supply (SMPS)
* **Presenter Script:**
  > "Introduce the project as an experimental monitoring and predictive thermal management platform using ESP32. The project is demonstrated on an ATX switch-mode power supply testbed to evaluate non-intrusive thermal sensing, trend extrapolation, and active cooling supervisory control."
* **Reference:** `transformer_cbm_spec.typ` Section 1.1

---

### Slide 02 — Presentation Outline
* **Title:** Presentation Outline
* **Presenter Script:**
  > "This presentation roadmap covers our engineering design from core physical principles to full system integration. We proceed through the problem background, system architecture, hardware component selection, firmware flowcharts, predictive regression equations, prototype testbed arrangements, validation methodology, and academic references."
* **Reference:** `transformer_cbm_spec.typ` Table of Contents

---

### Slide 03 — Introduction & Problem Context
* **Title:** Introduction & Problem Context
* **Presenter Script:**
  > "Transformers and power magnetics are vulnerable to thermal runaway and insulation degradation. Conventional monitoring relies on reactive bi-metallic switches or external inspection. By integrating dual-channel digital temperature probes with multi-rail DC electrical telemetry, the ESP32 calculates temperature trends in real time and executes proactive cooling before thermal inertia leads to an emergency trip."
* **Reference:** `transformer_cbm_spec.typ` Section 1.2 & Section 2.1

---

### Slide 04 — Problem Statement & Project Objectives
* **Title:** Problem Statement & Project Objectives
* **Presenter Script:**
  > "Our objective is to design a cohesive embedded prototype that bridges the gap between discrete instrumentation and smart supervisory protection. We monitor three DC output rails and two temperature points simultaneously, applying forward trend extrapolation to modulate cooling demand and protect hardware."
* **Reference:** `transformer_cbm_spec.typ` Section 2.2 & 2.4

---

### Slide 05 — Project Scope, Boundaries & Limitations
* **Title:** Project Scope, Boundaries & Limitations
* **Presenter Script:**
  > "Boundary definition is essential for engineering integrity. This prototype validates embedded predictive monitoring on a low-voltage switch-mode power supply bench. We monitor surface temperature rather than internal copper hot spots, and fan control operates as a command percentage without tachometer feedback. Standby power requires AC mains; the prototype has no auxiliary battery."
* **Reference:** `transformer_cbm_spec.typ` Section 1.3 & Section 3.1

---

### Slide 06 — End-to-End System Architecture
* **Title:** End-to-End System Architecture
* **Presenter Script:**
  > "This diagram illustrates the complete system architecture. On the left, physical temperature probes and high-side power monitors stream data into the ESP32. In the centre, FreeRTOS tasks execute digital filtering, rolling regression, and trip evaluation. Actuation controls the fan and the PS_ON line, while cloud services provide non-blocking remote visibility."
* **Reference:** `transformer_cbm_spec.typ` Section 4.1 & `diagram_3_combined_architecture_block.png`

---

### Slide 07 — Hardware Circuit Architecture
* **Title:** Hardware Circuit Architecture
* **Presenter Script:**
  > "This hardware circuit block diagram details the physical layout. Notice the clear separation between the +5VSB uninterruptible standby domain and the main switched DC power buses. The ESP32 interfaces with digital sensors via I2C and 1-Wire, while driving the cooling motor through an isolated H-bridge."
* **Reference:** `transformer_cbm_spec.typ` Section 5.1 & `diagram_1_hardware_block.png`

---

### Slide 08 — Circuit Design and Interconnections
* **Title:** Circuit Design and Interconnections
* **Presenter Script:**
  > "This detailed schematic shows the exact pin-to-pin wiring. Four distinct functional domains interact: power distribution, digital sensor communication, motor actuation, and the supervisory PS_ON shutdown interface. Note that the LCD PCF8574 pull-up resistors are tied to 3.3V to protect the ESP32 GPIOs."
* **Reference:** `transformer_cbm_spec.typ` Section 6.1 & `circuit_diagram_preview.png`

---

### Slide 09 — Component List & Bill of Materials (BOM)
* **Title:** Component List & Bill of Materials (BOM)
* **Presenter Script:**
  > "Here is our complete bill of materials. The system is built around the dual-core ESP32, paired with digital sensors to avoid analog ADC noise. The INA219 power monitors stream 12-bit bus metrics over I2C, while the TB6612FNG provides MOSFET PWM motor control. The total cost remains well under standard industrial monitoring hardware."
* **Reference:** `transformer_cbm_spec.typ` Section 5.1 & Section 5.2

---

### Slide 10 — Software & Cloud Supervision Architecture
* **Title:** Software & Cloud Supervision Architecture
* **Presenter Script:**
  > "The software architecture enforces strict task segregation across three tiers. Deterministic FreeRTOS Core 1 tasks handle sensor acquisition, filtering, regression, and safety trips every second. Core 0 hosts the local LittleFS web server, while non-blocking asynchronous cloud tasks push frames to Firebase and trigger Brevo email alerts through Cloudflare Workers."
* **Reference:** `transformer_cbm_spec.typ` Section 7.1 & `diagram_2_software_cloud_block.png`

---

### Slide 11 — Working Methodology & Predictive Algorithm
* **Title:** Working Methodology & Predictive Algorithm
* **Presenter Script:**
  > "Our predictive thermal algorithm anticipates temperature rise before physical thermal inertia reaches critical limits. The 1-hertz acquisition feeds an exponential moving average filter. An ordinary least-squares regression calculates the temperature-rise slope over a 30-second sliding buffer, projecting forward by horizon H to drive PWM fan duty cycle."
* **Reference:** `transformer_cbm_spec.typ` Section 8.1 & Section 8.2

---

### Slide 12 — Predictive Thermal Algorithm Flowchart
* **Title:** Predictive Thermal Algorithm Flowchart
* **Presenter Script:**
  > "This flowchart details the algorithm running inside the ESP32 timer loop. Every second, raw digital temperature readings are validated and smoothed with an EMA filter. If the 30-sample buffer is full, ordinary least-squares calculates the heating slope. Projected temperature determines whether cooling increases or whether an emergency trip is required."
* **Reference:** `transformer_cbm_spec.typ` Section 8.3 & `diagram_5_predictive_thermal_flowchart.png`

---

### Slide 13 — Hardware Operational State Flowchart
* **Title:** Hardware Operational State Flowchart
* **Presenter Script:**
  > "This flowchart illustrates the finite state machine running in firmware. The node starts in Standby Boot, checking sensors before asserting PS_ON to energize the main outputs. It transitions seamlessly into Normal Run or Thermal Boost based on temperature gradient, and locks into Fault Trip upon exceeding electrical or thermal safety thresholds."
* **Reference:** `transformer_cbm_spec.typ` Section 9.1 & `diagram_4_hardware_state_flowchart.png`

---

### Slide 14 — Combined Supervisory System Flowchart
* **Title:** Combined Supervisory System Flowchart
* **Presenter Script:**
  > "This flowchart illustrates the multi-core software architecture. FreeRTOS Core 1 runs the safety-critical loop with zero network overhead, guaranteeing sub-millisecond trip decisions. Core 0 handles web serving and cloud synchronization in the background. Even during a complete Wi-Fi dropout, protective functions continue uninterrupted."
* **Reference:** `transformer_cbm_spec.typ` Section 9.2 & `diagram_6_combined_supervisory_flowchart.png`

---

### Slide 15 — Hardware Prototype Setup & Testbed (Placeholder)
* **Title:** Hardware Prototype Setup & Testbed
* **Presenter Script:**
  > "This slide reserves space for the physical prototype assembly photograph. The bench arrangement incorporates the ATX power supply, the ESP32 breakout carrier, the digital temperature probe mounts, and the parallel test loads. Callouts highlight each physical component for clear evaluation."
* **Reference:** `transformer_cbm_spec.typ` Section 10.1 & Prototype Assembly Log

---

### Slide 16 — Experimental Proof & Validation Waveforms (Placeholder)
* **Title:** Experimental Proof & Validation Waveforms
* **Presenter Script:**
  > "This slide provides placeholders for our experimental proof data. When bench testing is executed, oscilloscope captures of the sub-millisecond PS_ON# cutoff and time-domain temperature suppression plots will be inserted directly into these panels to substantiate performance claims."
* **Reference:** `transformer_cbm_spec.typ` Section 10.2 & Laboratory Test Records

---

### Slide 17 — Testing Matrix & Validation Plan
* **Title:** Testing Matrix & Validation Plan
* **Presenter Script:**
  > "Our verification plan encompasses five distinct testing areas: sensor calibration accuracy, predictive thermal response under load steps, supervisory shutdown transition timing, network disconnect resilience, and transactional cloud alerting. Each test defines a specific method and evidence required for formal sign-off."
* **Reference:** `transformer_cbm_spec.typ` Section 10.3

---

### Slide 18 — Project Conclusion & Key Technical Takeaways
* **Title:** Project Conclusion & Key Technical Takeaways
* **Presenter Script:**
  > "In conclusion, this project demonstrates an integrated condition monitoring architecture for transformer thermal and electrical supervision. By coupling digital OneWire sensors and multi-rail I2C monitoring directly with an ESP32, we achieve predictive cooling and supervisory disconnect locally on bare metal. Standby power maintains monitoring even after a fault trip, delivering an autonomous, physics-grounded CBM platform."
* **Reference:** `transformer_cbm_spec.typ` Section 11.1

---

### Slide 19 — Future Scope & Grid Scalability
* **Title:** Future Scope & Grid Scalability
* **Presenter Script:**
  > "Looking forward, this project establishes a foundational architecture that scales directly to utility-scale transformers. Future enhancements will integrate tachometer fan speed feedback, fiber-optic winding sensors, Rogowski AC coils, and on-device Arrhenius insulation loss-of-life calculations to deliver automated predictive maintenance advisories."
* **Reference:** `transformer_cbm_spec.typ` Section 11.2

---

### Slide 20 — References
* **Title:** References
* **Presenter Script:**
  > "Here are our academic references from leading literature and IEEE standards. Our thermal modeling and predictive formulations are grounded in IEEE Standard C57.91 and IEC 60076-7, supported by recent research in IEEE Transactions on Industrial Electronics, Power Delivery, and Instrumentation and Measurement."
* **Reference:** IEEE Standard C57.91-2011 & IEC 60076-7:2018

---

### Slide 21 — Thank You & Technical Discussion
* **Title:** Thank You · Questions & Technical Discussion
* **Presenter Script:**
  > "Thank you for your time and attention. We now welcome questions, feedback, and technical discussion on our embedded condition monitoring architecture and predictive thermal management methodology."
