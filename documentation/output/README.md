# Transformer CBM — System Diagrams & Flowcharts Output Package

This directory contains the publication-ready, human-engineered block diagrams, algorithmic flowcharts, and master wiring schematics for the **Power Transformer Condition-Based Monitoring (CBM)** system.

## Folder Structure

```
output/
├── png/                  # High-resolution PNG image exports (150 PPI)
├── svg/                  # Scalable vector graphics (lossless SVG)
├── by_category/
│   ├── 01_block_diagrams/    # Architectural block diagrams (Diag 1, 2, 3)
│   ├── 02_flowcharts/        # Algorithmic & state flowcharts (Diag 4, 5, 6)
│   └── 03_schematic/         # Cirkit Designer master hardware schematic
├── system_diagrams_gallery.html # Interactive dark-mode web viewer
└── README.md             # This file manifest
```

## Diagram Manifest

| # | Diagram Name | Category | Description |
|---|---|---|---|
| **01** | `01_hardware_circuit_block_diagram` | `01_block_diagrams` | ATX PSU -> INA219 multi-rail monitor -> Dynamic loads, ESP32 core, LCD display, fan driver & cooling fan, cutoff switch interlock. |
| **02** | `02_software_cloud_architecture_block_diagram` | `01_block_diagrams` | Embedded FreeRTOS firmware pipeline (Sensors, Thermal Model, Safety Machine, LittleFS UI) bridged to Firebase RTDB, Hosting, Cloudflare Watchdog & Brevo. |
| **03** | `03_combined_system_architecture_block_diagram` | `01_block_diagrams` | Full 3-tier end-to-end architecture: Tier 1 Cloud Supervision, Tier 2 Embedded Firmware, Tier 3 Physical Hardware & Actuation with zero crossing lines. |
| **04** | `04_hardware_operational_state_flowchart` | `02_flowcharts` | Complete 10-state supervisory engine: Standby, Inrush Blanking, Running, Cutoffs (Electric, Bus, Thermal), Auto-Recovery test loop, and Lockouts. |
| **05** | `05_predictive_thermal_algorithm_flowchart` | `02_flowcharts` | 1.00 Hz closed-loop algorithm: Sensor acquisition, EMA filter, rate-of-rise calculation, 30s forward projection, dual-demand cooling & cloud upload. |
| **06** | `06_combined_supervisory_system_flowchart` | `02_flowcharts` | End-to-end supervisory flowchart: Path A Normal Closed-Loop Regulation vs. Path B Emergency Hardware Cutoff (< 5 ms trip, NVS latch, email alert, lockout). |
| **07** | `07_master_hardware_circuit_schematic` | `03_schematic` | Complete breadboard & circuit wiring schematic: ESP32, ATX Breakout, 3x INA219, 2x DS18B20, TB6612FNG driver, 12V fan, 16x2 LCD & BC547 cutoff switch. |

---
*Generated automatically by Antigravity Engineering Toolkit.*
