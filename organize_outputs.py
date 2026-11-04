# -*- coding: utf-8 -*-
"""
Organize all generated diagram PNG and SVG files into dedicated output folders:
- documentation/output/
- output/ (root workspace mirror for direct convenience)
- brain artifact directory mirror

Structure:
output/
  ├── png/                  (All high-res PNGs organized with clean sequential prefixes)
  ├── svg/                  (All vector SVGs organized with clean sequential prefixes)
  ├── by_category/
  │     ├── 01_block_diagrams/   (Diagrams 1, 2, 3)
  │     ├── 02_flowcharts/       (Diagrams 4, 5, 6)
  │     └── 03_schematic/        (Master Wiring Circuit Diagram)
  ├── system_diagrams_gallery.html (Interactive browser viewer)
  └── README.md             (Index and file manifest with resolutions & descriptions)
"""

import os
import shutil

DIAGRAM_MANIFEST = [
    {
        "num": "01",
        "name": "diagram_1_hardware_block",
        "clean_name": "01_hardware_circuit_block_diagram",
        "category": "01_block_diagrams",
        "title": "Diagram 1: Hardware Circuit Block Diagram",
        "src_svg": "diagram_1_hardware_block.svg",
        "src_png": "diagram_1_hardware_block.png",
        "desc": "ATX PSU -> INA219 multi-rail monitor -> Dynamic loads, ESP32 core, LCD display, fan driver & cooling fan, cutoff switch interlock."
    },
    {
        "num": "02",
        "name": "diagram_2_software_cloud_block",
        "clean_name": "02_software_cloud_architecture_block_diagram",
        "category": "01_block_diagrams",
        "title": "Diagram 2: Software & Cloud Architecture Block Diagram",
        "src_svg": "diagram_2_software_cloud_block.svg",
        "src_png": "diagram_2_software_cloud_block.png",
        "desc": "Embedded FreeRTOS firmware pipeline (Sensors, Thermal Model, Safety Machine, LittleFS UI) bridged to Firebase RTDB, Hosting, Cloudflare Watchdog & Brevo."
    },
    {
        "num": "03",
        "name": "diagram_3_combined_architecture_block",
        "clean_name": "03_combined_system_architecture_block_diagram",
        "category": "01_block_diagrams",
        "title": "Diagram 3: Combined Hardware & Software System Architecture",
        "src_svg": "diagram_3_combined_architecture_block.svg",
        "src_png": "diagram_3_combined_architecture_block.png",
        "desc": "Full 3-tier end-to-end architecture: Tier 1 Cloud Supervision, Tier 2 Embedded Firmware, Tier 3 Physical Hardware & Actuation with zero crossing lines."
    },
    {
        "num": "04",
        "name": "diagram_4_hardware_state_flowchart",
        "clean_name": "04_hardware_operational_state_flowchart",
        "category": "02_flowcharts",
        "title": "Diagram 4: Hardware Operational Flowchart (10-State Machine)",
        "src_svg": "diagram_4_hardware_state_flowchart.svg",
        "src_png": "diagram_4_hardware_state_flowchart.png",
        "desc": "Complete 10-state supervisory engine: Standby, Inrush Blanking, Running, Cutoffs (Electric, Bus, Thermal), Auto-Recovery test loop, and Lockouts."
    },
    {
        "num": "05",
        "name": "diagram_5_predictive_thermal_flowchart",
        "clean_name": "05_predictive_thermal_algorithm_flowchart",
        "category": "02_flowcharts",
        "title": "Diagram 5: Predictive Thermal Algorithm Flowchart",
        "src_svg": "diagram_5_predictive_thermal_flowchart.svg",
        "src_png": "diagram_5_predictive_thermal_flowchart.png",
        "desc": "1.00 Hz closed-loop algorithm: Sensor acquisition, EMA filter, rate-of-rise calculation, 30s forward projection, dual-demand cooling & cloud upload."
    },
    {
        "num": "06",
        "name": "diagram_6_combined_supervisory_flowchart",
        "clean_name": "06_combined_supervisory_system_flowchart",
        "category": "02_flowcharts",
        "title": "Diagram 6: Combined System Supervisory Flowchart",
        "src_svg": "diagram_6_combined_supervisory_flowchart.svg",
        "src_png": "diagram_6_combined_supervisory_flowchart.png",
        "desc": "End-to-end supervisory flowchart: Path A Normal Closed-Loop Regulation vs. Path B Emergency Hardware Cutoff (< 5 ms trip, NVS latch, email alert, lockout)."
    },
    {
        "num": "07",
        "name": "master_circuit_schematic",
        "clean_name": "07_master_hardware_circuit_schematic",
        "category": "03_schematic",
        "title": "Master Hardware Schematic: Cirkit Designer Wiring Diagram",
        "src_svg": "transformer_cbm_circuit_diagram.svg",
        "src_png": "circuit_diagram_preview.png",
        "desc": "Complete breadboard & circuit wiring schematic: ESP32, ATX Breakout, 3x INA219, 2x DS18B20, TB6612FNG driver, 12V fan, 16x2 LCD & 2N3904 cutoff switch."
    }
]

def organize():
    doc_dir = os.path.join("documentation")
    target_dirs = [
        os.path.join("documentation", "output"),
        os.path.join("output"),
        r"C:\Users\yogar\.gemini\antigravity\brain\c8a2b1d7-8ed1-4cbd-9cdf-f9046c74bbcb\output"
    ]

    for base_out in target_dirs:
        png_dir = os.path.join(base_out, "png")
        svg_dir = os.path.join(base_out, "svg")
        cat_dir = os.path.join(base_out, "by_category")

        os.makedirs(png_dir, exist_ok=True)
        os.makedirs(svg_dir, exist_ok=True)

        for item in DIAGRAM_MANIFEST:
            cat_sub = os.path.join(cat_dir, item["category"])
            os.makedirs(cat_sub, exist_ok=True)

            src_png = os.path.join(doc_dir, item["src_png"])
            src_svg = os.path.join(doc_dir, item["src_svg"])

            if os.path.exists(src_png):
                # Copy into root of output for HTML gallery support
                shutil.copy2(src_png, os.path.join(base_out, item["src_png"]))
                # Copy into png/ with numbered clean name and standard name
                shutil.copy2(src_png, os.path.join(png_dir, f"{item['clean_name']}.png"))
                shutil.copy2(src_png, os.path.join(png_dir, f"{item['name']}.png"))
                # Copy into by_category/
                shutil.copy2(src_png, os.path.join(cat_sub, f"{item['clean_name']}.png"))

            if os.path.exists(src_svg):
                # Copy into root of output for HTML gallery support
                shutil.copy2(src_svg, os.path.join(base_out, item["src_svg"]))
                # Copy into svg/ with numbered clean name and standard name
                shutil.copy2(src_svg, os.path.join(svg_dir, f"{item['clean_name']}.svg"))
                shutil.copy2(src_svg, os.path.join(svg_dir, f"{item['name']}.svg"))
                # Copy into by_category/
                shutil.copy2(src_svg, os.path.join(cat_sub, f"{item['clean_name']}.svg"))

        # Copy interactive gallery viewer
        src_gallery = os.path.join(doc_dir, "system_diagrams_gallery.html")
        if os.path.exists(src_gallery):
            shutil.copy2(src_gallery, os.path.join(base_out, "system_diagrams_gallery.html"))

        # Generate README manifest
        readme_path = os.path.join(base_out, "README.md")
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write("# Transformer CBM — System Diagrams & Flowcharts Output Package\n\n")
            f.write("This directory contains the publication-ready, human-engineered block diagrams, algorithmic flowcharts, and master wiring schematics for the **Power Transformer Condition-Based Monitoring (CBM)** system.\n\n")
            f.write("## Folder Structure\n\n")
            f.write("```\n")
            f.write("output/\n")
            f.write("├── png/                  # High-resolution PNG image exports (150 PPI)\n")
            f.write("├── svg/                  # Scalable vector graphics (lossless SVG)\n")
            f.write("├── by_category/\n")
            f.write("│   ├── 01_block_diagrams/    # Architectural block diagrams (Diag 1, 2, 3)\n")
            f.write("│   ├── 02_flowcharts/        # Algorithmic & state flowcharts (Diag 4, 5, 6)\n")
            f.write("│   └── 03_schematic/         # Cirkit Designer master hardware schematic\n")
            f.write("├── system_diagrams_gallery.html # Interactive dark-mode web viewer\n")
            f.write("└── README.md             # This file manifest\n")
            f.write("```\n\n")
            f.write("## Diagram Manifest\n\n")
            f.write("| # | Diagram Name | Category | Description |\n")
            f.write("|---|---|---|---|\n")
            for item in DIAGRAM_MANIFEST:
                f.write(f"| **{item['num']}** | `{item['clean_name']}` | `{item['category']}` | {item['desc']} |\n")
            f.write("\n---\n*Generated automatically by Antigravity Engineering Toolkit.*\n")

        print(f"Successfully organized output in: {base_out}")

if __name__ == "__main__":
    organize()
