# Engineering & Automation Scripts

This directory contains standalone Python build, assembly, and diagram synthesis scripts utilized to generate the system schematics, architecture diagrams, and formal specification documents for the Transformer Condition-Based Monitoring (CBM) system.

---

## Directory Overview

### 1. Document Builders & Assemblers
- `assemble_v3.py`: Merges and compiles modular Typst specification sections into the master 26-page engineering document `documentation/transformer_cbm_spec.typ`.
- `build_v3_document.py`: Driver script orchestrating section assembly and Typst compilation.
- `build_v3_sections_1_to_8.py`: Generates Typst source code for Sections 1 through 8 (Executive Summary, Mathematical Formulations, Sensor Topology).
- `build_v3_sections_9_to_15.py`: Generates Typst source code for Sections 9 through 15 (INA219 Power Diagnostics, TB6612 Fan Controller, FreeRTOS Safety Tasks).
- `build_v3_sections_16_to_24.py`: Generates Typst source code for Sections 16 through 24 (Predictive Thermal Prognostics, Edge State Machine, Cloud Integration).
- `generate_v3_spec.py`: Automated generator synthesizing the complete Typst specification.
- `build_paper.py`: Compiles the complete research manuscript `documentation/transformer_cbm_paper.typ`.
- `build_ieee_conference_paper.py`: Compiles the 4-page IEEE double-column conference paper `documentation/transformer_cbm_conference_paper.typ`.

---

### 2. Architecture & Block Diagram Generators
- `build_all_system_diagrams.py`: Master synthesis runner compiling all 6 core system diagrams into SVG and PNG formats.
- `build_diagrams_full.py`: High-resolution vector synthesis engine for diagrams 1 through 6.
- `build_diag1_hw.py` / `build_diag1_hw_simple.py`: Diagram 1 - Hardware Circuit Block Diagram (ATX SMPS, INA219, TB6612, ESP32, DS18B20).
- `build_diag2_sw.py` / `build_diag2_sw_simple.py`: Diagram 2 - Embedded Software & Cloud Architecture Block Diagram.
- `build_diag3_comb.py` / `build_diag3_comb_simple.py`: Diagram 3 - Combined Hardware & Software System Architecture.
- `build_diag4_state.py` / `build_diag4_state_simple.py`: Diagram 4 - Hardware Operational State Machine Flowchart.
- `build_diag5_algo.py` / `build_diag5_algo_simple.py`: Diagram 5 - Predictive Thermal & Arrhenius Life-Loss Algorithm Flowchart.
- `build_diag6_e2e.py` / `build_diag6_e2e_simple.py`: Diagram 6 - Combined Supervisory & Cloud Failsafe Flowchart.

---

### 3. Circuit Schematics & Galleries
- `build_cirkit_designer_schematic.py`: Vector schematic layout engine producing professional wiring diagrams with pin-accurate footprints.
- `build_clean_layout_schematic.py`: High-density schematic rendering script with explicit bus routing and terminal post callouts.
- `generate_svg_schematic.py`: Standalone SVG vector generator for the master wiring harness.
- `generate_clean_schematic.py`: Minimalist schematic generator for quick rendering and vector asset exports.
- `build_diagram_gallery.py`: Builds the standalone HTML gallery viewer (`system_diagrams_gallery.html`) for interactive review.
- `organize_outputs.py`: Asset syndication script copying generated SVG/PNG assets into category-indexed directories.

---

## Execution Environment

All scripts are written in standard Python 3. To run any script:

```bash
python scripts/build_all_system_diagrams.py
```
