# -*- coding: utf-8 -*-
"""
Generator script for Document Version 3.0:
Development of an IoT-Based Transformer Condition Monitoring System with Predictive Adaptive Thermal Management
"""

import sys

def build_typst_spec():
    parts = []
    
    # -------------------------------------------------------------------------
    # Document Setup & Styling
    # -------------------------------------------------------------------------
    parts.append('''// Formal Technical Specification Document - Version 3.0
// Platform: Small-Scale ATX SMPS Demonstration Bench
// Classification: Controlled Engineering Specification

#import "@preview/fletcher:0.5.8" as fletcher: diagram, node, edge, shapes
#import "@preview/cetz:0.5.3"
#import "@preview/cetz-plot:0.1.4": plot

// Formal Page Configuration
#set page(
  paper: "a4",
  margin: (x: 2.2cm, top: 2.5cm, bottom: 2.5cm),
  header: context {
    let page-num = counter(page).get().first()
    if page-num > 2 [
      #grid(
        columns: (1fr, 1fr),
        align: (left, right),
        [#text(size: 7.5pt, font: "Segoe UI", fill: rgb("64748b"))[Transformer Condition Monitoring & Predictive Thermal Management]],
        [#text(size: 7.5pt, font: "Segoe UI", fill: rgb("64748b"))[Engineering Specification Baseline -- Rev 3.0]]
      )
      #line(length: 100%, stroke: 0.5pt + rgb("cbd5e1"))
    ]
  },
  footer: context {
    let page-num = counter(page).get().first()
    if page-num > 1 [
      #line(length: 100%, stroke: 0.5pt + rgb("cbd5e1"))
      #v(2pt)
      #grid(
        columns: (1fr, 1fr),
        align: (left, right),
        [#text(size: 7.5pt, font: "Segoe UI", fill: rgb("64748b"))[Hardware & Firmware Systems Architecture Baseline]],
        [#text(size: 7.5pt, font: "Segoe UI", fill: rgb("64748b"))[Page #counter(page).display("1 of 1", both: true)]]
      )
    ]
  }
)

#set text(
  font: "Segoe UI",
  size: 9pt,
  fill: rgb("0f172a"),
  spacing: 120%,
  lang: "en"
)

#set par(
  justify: true,
  leading: 0.65em,
)

#set heading(numbering: none)
#show heading.where(level: 1): it => block(below: 14pt, above: 20pt)[
  #text(size: 14pt, weight: "bold", fill: rgb("0f172a"))[#it.body]
  #v(2pt)
  #line(length: 100%, stroke: 1.2pt + rgb("0f172a"))
]

#show heading.where(level: 2): it => block(below: 10pt, above: 14pt)[
  #text(size: 11pt, weight: "bold", fill: rgb("1e293b"))[#it.body]
]

#show heading.where(level: 3): it => block(below: 8pt, above: 10pt)[
  #text(size: 9.5pt, weight: "bold", fill: rgb("334155"))[#it.body]
]

// Professional Engineering Helpers
#let formal-table(columns: auto, align: auto, ..cells) = {
  table(
    columns: columns,
    align: align,
    stroke: none,
    fill: (x, y) => if y == 0 { rgb("f1f5f9") } else if calc.even(y) { rgb("f8fafc") } else { none },
    table.hline(stroke: 1.2pt + rgb("0f172a")),
    table.hline(y: 1, stroke: 0.6pt + rgb("334155")),
    ..cells,
    table.hline(stroke: 1.2pt + rgb("0f172a"))
  )
}

#let tech-figure(caption: "", body) = {
  align(center)[
    #block(
      width: 100%,
      stroke: 0.75pt + rgb("cbd5e1"),
      inset: (x: 10pt, y: 10pt),
      fill: rgb("ffffff"),
      [
        #body
        #v(6pt)
        #text(size: 7.5pt, weight: "bold", font: "Segoe UI", fill: rgb("334155"))[#caption]
      ]
    )
  ]
}

#let eng-box(title: "NOTE", body) = {
  block(
    width: 100%,
    stroke: (left: 3pt + rgb("0284c7"), rest: 0.5pt + rgb("e2e8f0")),
    inset: (x: 10pt, y: 8pt),
    fill: rgb("f8fafc"),
    [
      #text(size: 8pt, weight: "bold", fill: rgb("0284c7"))[#title]
      #v(3pt)
      #text(size: 8.5pt, fill: rgb("1e293b"))[#body]
    ]
  )
}

#let hazard-box(title: "ELECTRICAL HAZARD STATEMENT", body) = {
  block(
    width: 100%,
    stroke: (left: 3pt + rgb("b91c1c"), rest: 0.5pt + rgb("fecaca")),
    inset: (x: 10pt, y: 8pt),
    fill: rgb("fef2f2"),
    [
      #text(size: 8pt, weight: "bold", fill: rgb("b91c1c"))[#title]
      #v(3pt)
      #text(size: 8.5pt, fill: rgb("7f1d1d"))[#body]
    ]
  )
}
''')

    # -------------------------------------------------------------------------
    # Cover Page
    # -------------------------------------------------------------------------
    parts.append('''
// ============================================================================
// TITLE COVER PAGE (PROFESSIONAL ENGINEERING BASELINE)
// ============================================================================

#align(center)[
  #v(20pt)
  #text(size: 11pt, weight: "bold", tracking: 0.15em, fill: rgb("475569"))[CONTROLLED ENGINEERING SPECIFICATION]
  #v(6pt)
  #text(size: 9pt, weight: "medium", tracking: 0.08em, fill: rgb("64748b"))[HARDWARE ARCHITECTURE, EMBEDDED CONTROL & CLOUD SUPERVISION]
  #v(14pt)
  #line(length: 100%, stroke: 1.5pt + rgb("0f172a"))
  #v(16pt)
  
  #text(size: 18pt, weight: "bold", fill: rgb("0f172a"))[
    Development of an IoT-Based Transformer Condition Monitoring System with Predictive Adaptive Thermal Management
  ]
  
  #v(8pt)
  #text(size: 10.5pt, style: "italic", fill: rgb("334155"))[
    Consolidated Project Design, Circuit Interfaces, Real-Time Predictive Algorithms, and Validation Protocols
  ]
  
  #v(16pt)
  #line(length: 100%, stroke: 0.75pt + rgb("cbd5e1"))
  #v(20pt)
]

#grid(
  columns: (1fr, 1fr),
  gutter: 18pt,
  [
    #block(
      stroke: 0.75pt + rgb("cbd5e1"),
      inset: 12pt,
      fill: rgb("f8fafc"),
      width: 100%,
      [
        #text(size: 8.5pt, weight: "bold", fill: rgb("0f172a"))[DOCUMENT INFORMATION]
        #v(6pt)
        #line(length: 100%, stroke: 0.5pt + rgb("cbd5e1"))
        #v(6pt)
        #grid(
          columns: (1fr, 1.5fr),
          row-gutter: 6pt,
          [*Document Type:*], [Consolidated Engineering Spec],
          [*Baseline Rev:*], [3.0 -- Production Baseline],
          [*Date:*], [October 30, 2026],
          [*Classification:*], [Engineering Design Record],
          [*Target System:*], [Small-Scale ATX SMPS Bench],
          [*Primary Controller:*], [ESP32-WROOM DevKitC (30-pin)],
          [*Status:*], [Procurement in Progress]
        )
      ]
    )
  ],
  [
    #block(
      stroke: 0.75pt + rgb("cbd5e1"),
      inset: 12pt,
      fill: rgb("f8fafc"),
      width: 100%,
      [
        #text(size: 8.5pt, weight: "bold", fill: rgb("0f172a"))[ARCHITECTURE ALLOCATION]
        #v(6pt)
        #line(length: 100%, stroke: 0.5pt + rgb("cbd5e1"))
        #v(6pt)
        #grid(
          columns: (1fr, 1.5fr),
          row-gutter: 6pt,
          [*Embedded Core:*], [ESP32 (Acquisition & Trips)],
          [*Power Isolation:*], [Active-Low PS_ON\\# Circuit],
          [*Cooling Driver:*], [TB6612FNG H-Bridge (PWM)],
          [*Instrumentation:*], [3x INA219 (I2C) + 2x DS18B20],
          [*Local Interface:*], [ESP32 Embedded LittleFS Server],
          [*Cloud Storage:*], [Firebase Realtime Database],
          [*Supervision:*], [Cloudflare Worker + Brevo API]
        )
      ]
    )
  ]
)

#v(14pt)

#eng-box(
  title: "SYSTEM ARCHITECTURAL GOVERNING PRINCIPLE",
  [All safety-critical thermal monitoring, multi-rail electrical supervision, forward temperature trend projection, and protective shutdown decisions execute autonomously within the local ESP32 firmware loop. The ATX switch-mode power supply (SMPS) remains fully monitored and controllable locally from uninterrupted +5VSB standby power, even during total external internet, Wi-Fi, or cloud service outages.]
)

#v(10pt)

#eng-box(
  title: "PROJECT PLATFORM & SCOPE DELIMITATION",
  [This specification establishes the hardware, firmware, and supervisory implementation for demonstrating condition monitoring and predictive adaptive thermal control on a small-scale ATX switch-mode power supply assembly. This design demonstrates the monitoring and control principles using low-voltage instrumentation -- it does not constitute a certified utility-grid transformer protective device, substation protection relay, or safety-instrumented emergency-stop (SIS/E-stop) system.]
)

#pagebreak()

// ============================================================================
// TABLE OF CONTENTS
// ============================================================================

#v(10pt)
#text(size: 14pt, weight: "bold", fill: rgb("0f172a"))[Table of Contents]
#v(6pt)
#line(length: 100%, stroke: 1.2pt + rgb("0f172a"))
#v(10pt)

#outline(
  title: none,
  indent: auto,
  depth: 2
)

#pagebreak()
''')

    return "".join(parts)

if __name__ == "__main__":
    print("Document header generator ready.")
