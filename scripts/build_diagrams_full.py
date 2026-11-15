# -*- coding: utf-8 -*-
"""
Full System Diagrams & Flowcharts Generator for Transformer_CBM
Rev 1.0 Baseline
Generates:
1. diagram_1_hardware_block.svg
2. diagram_2_software_cloud_block.svg
3. diagram_3_combined_architecture_block.svg
4. diagram_4_hardware_state_flowchart.svg
5. diagram_5_predictive_thermal_flowchart.svg
6. diagram_6_combined_supervisory_flowchart.svg
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

def build_card(x, y, w, h, title, subtitle, bg="#ffffff", border="#cbd5e1", title_fill="#0f172a", sub_fill="#64748b"):
    return f'''  <g transform="translate({x}, {y})" filter="url(#shadow)">
    <rect width="{w}" height="{h}" rx="10" fill="{bg}" stroke="{border}" stroke-width="2"/>
    <text x="24" y="38" font-size="22" font-weight="900" fill="{title_fill}">{title}</text>
    <text x="24" y="64" font-size="16" font-weight="700" fill="{sub_fill}">{subtitle}</text>
  </g>'''

def build_subcard(x, y, w, h, title, lines_text, bg="#f8fafc", border="#e2e8f0", title_fill="#1e293b", text_fill="#475569"):
    body_lines = ""
    curr_y = 60
    for l in lines_text:
        body_lines += f'<text x="20" y="{curr_y}" font-size="16" font-weight="600" fill="{text_fill}">{l}</text>\n'
        curr_y += 24
    return f'''  <g transform="translate({x}, {y})">
    <rect width="{w}" height="{h}" rx="8" fill="{bg}" stroke="{border}" stroke-width="1.5"/>
    <text x="20" y="30" font-size="18" font-weight="800" fill="{title_fill}">{title}</text>
    {body_lines}
  </g>'''

# Continued in next part
