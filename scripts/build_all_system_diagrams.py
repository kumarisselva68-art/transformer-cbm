# -*- coding: utf-8 -*-
"""
High-Quality System Diagrams & Flowcharts Generator for Transformer_CBM
Produces 6 Publication-Quality Vector SVGs:
1. Diagram 1: Hardware / Circuit Block Diagram
2. Diagram 2: Software & Cloud Architecture Block Diagram
3. Diagram 3: Combined Hardware + Software Architecture Diagram
4. Diagram 4: Hardware Operational State Machine Flowchart
5. Diagram 5: Predictive Thermal Algorithm Execution Flowchart
6. Diagram 6: Combined System Supervisory End-to-End Flowchart
"""

import os
import subprocess

def get_base_svg(title, subtitle, content, w=2200, h=1400):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <defs>
    <!-- Background Grid -->
    <pattern id="grid" width="25" height="25" patternUnits="userSpaceOnUse">
      <path d="M 25 0 L 0 0 0 25" fill="none" stroke="#e2e8f0" stroke-width="0.75"/>
    </pattern>
    <!-- Card Drop Shadow -->
    <filter id="shadow" x="-3%" y="-3%" width="108%" height="110%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="2" dy="4" stdDeviation="5" flood-color="#0f172a" flood-opacity="0.08"/>
    </filter>
    <!-- Arrow Markers -->
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#0f172a"/>
    </marker>
    <marker id="arrow-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#2563eb"/>
    </marker>
    <marker id="arrow-cyan" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#0284c7"/>
    </marker>
    <marker id="arrow-green" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#059669"/>
    </marker>
    <marker id="arrow-red" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#dc2626"/>
    </marker>
    <marker id="arrow-purple" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#9333ea"/>
    </marker>
    <marker id="arrow-orange" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#ea580c"/>
    </marker>
  </defs>

  <style>
    text {{
      font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, 'Inter', Roboto, sans-serif;
      user-select: none;
    }}
  </style>

  <!-- Background -->
  <rect width="{w}" height="{h}" fill="#f8fafc"/>
  <rect width="{w}" height="{h}" fill="url(#grid)"/>

  <!-- Clean Official Header -->
  <g transform="translate(60, 52)">
    <text font-size="32" font-weight="900" fill="#0f172a" letter-spacing="-0.5px">{title}</text>
    <text font-size="18" font-weight="700" fill="#64748b" y="32">{subtitle}</text>
  </g>

{content}
</svg>'''

print("get_base_svg ready")
