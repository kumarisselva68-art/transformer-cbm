# Engineering Documentation & Technical Specification Suite

This directory contains the formal engineering specification documentation and code-driven PDF compilation pipeline for the **IoT-Based Transformer Condition Monitoring System with Predictive Adaptive Thermal Management**.

Powered by a self-contained **Typst v0.15.1** compiler and vector graphics engine, all documentation is maintained as pure code and compiles into publication-grade PDFs.

---

## 📁 Repository Structure

```text
documentation/
├── bin/
│   └── typst.exe                  # Standalone portable Typst compiler (v0.15.1)
├── transformer_cbm_spec.typ       # Master formal engineering specification (22 pages)
├── transformer_cbm_spec.pdf       # Compiled formal technical specification PDF
├── showcase.typ                   # Component showcase reference
├── showcase.pdf                   # Compiled component showcase PDF
├── build.ps1                      # Automation build & live-watch script
├── spec_page_1.png ... 22.png     # Rendered page previews for visual auditing
└── README.md                      # Documentation reference manual
```

---

## 📐 Formal Engineering Document Design Standards

In strict accordance with ISO, IEEE, and military technical report standards:
1. **Monochrome Precision & Typography:**
   - Standard 2.5 cm formal engineering margins.
   - Clean, high-legibility typographic hierarchy (`Segoe UI` / `Arial`, `Cambria Math` for formal equation display).
   - Crisp 0.5pt to 1.2pt solid black rules; **zero rounded corners or website-style card bubbles**.
2. **Booktabs Tabular Standards:**
   - Formal technical tables with heavy top/bottom rules (`1.2pt`), clean header underlines (`0.75pt`), and light row dividers.
3. **Engineering Schematics & Flow Diagrams:**
   - Sharp-cornered, clean technical diagrams with orthogonal interconnects (`node-corner-radius: 0pt`).
4. **Header & Footer Instrumentation:**
   - Running formal document control header: `DOC REF: TMS-ESP32-SPEC-2026-V2.0 | REV 2.0 (CONSOLIDATED)`.
   - Continuous page accounting: `Page X of 22` with classification and baseline status notice.

---

## 📑 Specification Table of Contents (22 Pages)

- **1. Document Control & Interpretation** (Version 2.0 Baseline, Normative Definitions)
- **2. Project Purpose & Measurement Boundaries** (Transformer vs. Rail Physical Boundaries, Excluded Claims)
- **3. Final Scope** (Included Scope vs. Deferred Extensions, Sensor Instrumentation Boundaries)
- **4. Architecture and Responsibility Boundaries** (Interconnect Diagram, Subsystem Responsibility Allocation)
- **5. Complete Data-Flow Design** (Flows A through G: Local, Cloud Ingest, History, Urgent Alerts, Heartbeat, Remote OFF, Recovery)
- **6. Hardware Architecture & Electrical Design** (Standby +5VSB vs. Main Domains, 3-Rail Shunt Sizing, I2C, Isolation, Fan Drive, PS_ON\# Interface)
- **7. Commissioning, Provisioning, and Operating Modes** (Setup Workflow, Local, Cloud, Maintenance Invariants)
- **8. Firmware Structure and Real-Time Scheduling** (12 Subsystem Modules, Task Cadence Table)
- **9. Measurement Quality and Telemetry Telemetry Integrity** (Metadata Schema, JSON Cloud Packet)
- **10. Predictive Adaptive Thermal Management** (EMA Filter, OLS Linear Regression, Horizon Projection, Piecewise Duty Transfer Function)
- **11. Electrical Supervisory Protection** (Per-Rail Warning/Trip Limits, Startup Inrush Blanking)
- **12. Main-Output Supervisory State Machine** (State Diagram, Verification of De-energization)
- **13. Thermal Shutdown and Qualified Automatic Recovery** (Passive Cooldown Physics, 8-Point Restart Eligibility, Retry Policy)
- **14. Remote Operator Commands** (Time-Bounded Remote OFF Protocol, Invariants)
- **15. Cloud Database Schema and Access Control** (Firebase Tree, Security Rule Permissions Matrix)
- **16. Data Retention, Storage Buffering, and Outage Recovery** (RAM Ring-Buffer, 30-Day Automated Pruning)
- **17. Independent Heartbeat Supervision** (Cloudflare Cron Verification, 6 Supervisory States)
- **18. Brevo Transactional Email Notification Backend** (Worker Endpoints, Secret Isolation, Event Triggers)
- **19. Dashboard Interface Specifications** (Common Visual Layout, Local vs. Remote Features)
- **20. Privacy, Telemetry Minimization, and Security**
- **21. Deployment Decision and Free-Tier Infrastructure Budgets** (Quota Matrix, Deployment Sequence)
- **22. Verification, Calibration, and Bench Acceptance Testing** (12-Point Acceptance Test Matrix)
- **23. Future Extension: Independent Branch and Rail Control** (External eFuse Architecture)
- **24. Comprehensive Safety Limitations and Disclaimers** (6 Critical Safety Boundaries)
- **25. Formal Handover Deliverables Register** (13 Engineering Handover Artifacts)
- **Final System Architectural Summary & Central Governing Principle** (Decoupled Flow Table & Sign-Off)

---

## 🛠️ Build and Automation Commands

Use [build.ps1](file:///e:/Client/Transformer_CBM/documentation/build.ps1) from PowerShell:

```powershell
# 1. Compile the master engineering specification PDF:
powershell -ExecutionPolicy Bypass -File documentation\build.ps1 -Target spec

# 2. Re-generate all PNG page previews:
powershell -ExecutionPolicy Bypass -File documentation\build.ps1 -Target spec -Preview

# 3. Live watch mode (auto-recompiles on file save):
powershell -ExecutionPolicy Bypass -File documentation\build.ps1 -Target spec -Watch
```
