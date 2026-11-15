# -*- coding: utf-8 -*-
"""
Complete generator for Version 3.0 specification:
Development of an IoT-Based Transformer Condition Monitoring System with Predictive Adaptive Thermal Management
"""

import os

def generate_v3():
    content = []
    
    # Header & Styles
    content.append('''// Formal Technical Specification Document - Version 3.0
// Platform: Small-Scale ATX SMPS Demonstration Bench
// Classification: Controlled Engineering Specification

#import "@preview/fletcher:0.5.8" as fletcher: diagram, node, edge, shapes
#import "@preview/cetz:0.5.3"
#import "@preview/cetz-plot:0.1.4": plot

#set page(
  paper: "a4",
  margin: (x: 2.2cm, top: 2.5cm, bottom: 2.5cm),
  header: context {
    let page-num = counter(page).get().first()
    if page-num > 2 [
      #grid(
        columns: (1fr, 1fr),
        align: (left, right),
        [#text(size: 7.5pt, font: "Segoe UI", fill: rgb("475569"))[Transformer Condition Monitoring & Predictive Thermal Management]],
        [#text(size: 7.5pt, font: "Segoe UI", fill: rgb("475569"))[Engineering Specification Baseline -- Rev 3.0]]
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
  size: 8.8pt,
  fill: rgb("0f172a"),
  spacing: 120%,
  lang: "en"
)

#set par(
  justify: true,
  leading: 0.62em,
)

#set heading(numbering: none)
#show heading.where(level: 1): it => block(below: 12pt, above: 18pt)[
  #text(size: 13.5pt, weight: "bold", fill: rgb("0f172a"))[#it.body]
  #v(2pt)
  #line(length: 100%, stroke: 1.2pt + rgb("0f172a"))
]

#show heading.where(level: 2): it => block(below: 8pt, above: 12pt)[
  #text(size: 10.5pt, weight: "bold", fill: rgb("1e293b"))[#it.body]
]

#show heading.where(level: 3): it => block(below: 6pt, above: 9pt)[
  #text(size: 9.2pt, weight: "bold", fill: rgb("334155"))[#it.body]
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
      inset: (x: 8pt, y: 8pt),
      fill: rgb("ffffff"),
      [
        #body
        #v(5pt)
        #text(size: 7.5pt, weight: "bold", font: "Segoe UI", fill: rgb("334155"))[#caption]
      ]
    )
  ]
}

#let eng-box(title: "NOTE", body) = {
  block(
    width: 100%,
    stroke: (left: 3pt + rgb("0284c7"), rest: 0.5pt + rgb("cbd5e1")),
    inset: (x: 9pt, y: 7pt),
    fill: rgb("f8fafc"),
    [
      #text(size: 8pt, weight: "bold", fill: rgb("0284c7"))[#title]
      #v(2pt)
      #text(size: 8.3pt, fill: rgb("1e293b"))[#body]
    ]
  )
}

#let hazard-box(title: "ELECTRICAL HAZARD STATEMENT", body) = {
  block(
    width: 100%,
    stroke: (left: 3pt + rgb("b91c1c"), rest: 0.5pt + rgb("fecaca")),
    inset: (x: 9pt, y: 7pt),
    fill: rgb("fef2f2"),
    [
      #text(size: 8pt, weight: "bold", fill: rgb("b91c1c"))[#title]
      #v(2pt)
      #text(size: 8.3pt, fill: rgb("7f1d1d"))[#body]
    ]
  )
}

// ============================================================================
// TITLE COVER PAGE (PROFESSIONAL ENGINEERING BASELINE)
// ============================================================================

#align(center)[
  #v(20pt)
  #text(size: 10pt, weight: "bold", tracking: 0.15em, fill: rgb("475569"))[CONTROLLED ENGINEERING SPECIFICATION]
  #v(5pt)
  #text(size: 8.5pt, weight: "medium", tracking: 0.08em, fill: rgb("64748b"))[HARDWARE ARCHITECTURE, EMBEDDED CONTROL & CLOUD SUPERVISION]
  #v(12pt)
  #line(length: 100%, stroke: 1.5pt + rgb("0f172a"))
  #v(14pt)
  
  #text(size: 17pt, weight: "bold", fill: rgb("0f172a"))[
    Development of an IoT-Based Transformer Condition Monitoring System with Predictive Adaptive Thermal Management
  ]
  
  #v(8pt)
  #text(size: 10pt, style: "italic", fill: rgb("334155"))[
    Consolidated Project Design, Circuit Interfaces, Real-Time Predictive Algorithms, and Validation Protocols
  ]
  
  #v(14pt)
  #line(length: 100%, stroke: 0.75pt + rgb("cbd5e1"))
  #v(18pt)
]

#grid(
  columns: (1fr, 1fr),
  gutter: 16pt,
  [
    #block(
      stroke: 0.75pt + rgb("cbd5e1"),
      inset: 11pt,
      fill: rgb("f8fafc"),
      width: 100%,
      [
        #text(size: 8.5pt, weight: "bold", fill: rgb("0f172a"))[DOCUMENT INFORMATION]
        #v(5pt)
        #line(length: 100%, stroke: 0.5pt + rgb("cbd5e1"))
        #v(5pt)
        #grid(
          columns: (1.1fr, 1.4fr),
          row-gutter: 5pt,
          [*Document Type:*], [Consolidated Engineering Spec],
          [*Baseline Rev:*], [3.0 -- Production Baseline],
          [*Date:*], [October 30, 2026],
          [*Classification:*], [Engineering Design Record],
          [*Target System:*], [Small-Scale ATX SMPS Bench],
          [*Primary Controller:*], [ESP32-WROOM DevKitC (30-pin)],
          [*Status:*], [Engineering Design Baseline (Pre-Commissioning)]
        )
      ]
    )
  ],
  [
    #block(
      stroke: 0.75pt + rgb("cbd5e1"),
      inset: 11pt,
      fill: rgb("f8fafc"),
      width: 100%,
      [
        #text(size: 8.5pt, weight: "bold", fill: rgb("0f172a"))[ARCHITECTURE ALLOCATION]
        #v(5pt)
        #line(length: 100%, stroke: 0.5pt + rgb("cbd5e1"))
        #v(5pt)
        #grid(
          columns: (1.1fr, 1.4fr),
          row-gutter: 5pt,
          [*Embedded Core:*], [ESP32 (Acquisition & Trips)],
          [*Power Isolation:*], [Active-Low PS_ON\\# Circuit],
          [*Cooling Driver:*], [TB6612FNG H-Bridge (PWM)],
          [*Instrumentation:*], [3x INA219 + 2x DS18B20 + 16#sym.times;2 LCD],
          [*Local Interface:*], [ESP32 LittleFS & 16#sym.times;2 LCD],
          [*Cloud Storage:*], [Firebase Realtime Database],
          [*Supervision:*], [Cloudflare Worker + Brevo API]
        )
      ]
    )
  ]
)

#v(12pt)

#eng-box(
  title: "SYSTEM ARCHITECTURAL GOVERNING PRINCIPLE",
  [All safety-critical thermal monitoring, multi-rail electrical supervision, forward temperature trend projection, and protective shutdown decisions execute autonomously within the local ESP32 firmware loop. The ATX switch-mode power supply (SMPS) remains fully monitored and controllable locally from uninterrupted +5VSB standby power, even during total external internet, Wi-Fi, or cloud service outages.]
)

#v(8pt)

#eng-box(
  title: "PROJECT PLATFORM & SCOPE DELIMITATION",
  [This specification establishes the hardware, firmware, and supervisory implementation for demonstrating condition monitoring and predictive adaptive thermal control on a small-scale ATX switch-mode power supply assembly. This design demonstrates the monitoring and control principles using low-voltage instrumentation -- it does not constitute a certified utility-grid transformer protective device, substation protection relay, or safety-instrumented emergency-stop (SIS/E-stop) system.]
)

#pagebreak()

// ============================================================================
// TABLE OF CONTENTS
// ============================================================================

#v(8pt)
#text(size: 13.5pt, weight: "bold", fill: rgb("0f172a"))[Table of Contents]
#v(4pt)
#line(length: 100%, stroke: 1.2pt + rgb("0f172a"))
#v(8pt)

#outline(
  title: none,
  indent: auto,
  depth: 2
)

#pagebreak()
''')

    # Return partial for testing
    return "".join(content)

if __name__ == "__main__":
    print("Base template loaded.")
