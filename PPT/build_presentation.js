/**
 * build_presentation.js
 * 
 * Generates the clean, human-designed 21-slide academic engineering presentation:
 * "IoT-Based Transformer Condition Monitoring with Predictive Adaptive Thermal Management Using ESP32"
 * (Executed using an ATX SMPS Demonstration Platform)
 * 
 * Strict Design Principles:
 * - NO dark/cyber backgrounds — clean, crisp, pure white academic engineering style (#FFFFFF) throughout
 * - Professional Green, Slate-Black, and White color palette
 * - Perfectly calculated geometry: zero overlapping text boxes, zero clipped tables, zero overflowing cards
 * - All components fit within the standard content area (y <= 6.80 in)
 * - All 6 high-res block diagrams and flowcharts + circuit schematic cleanly showcased
 * - Dedicated Component List / BOM table with optimized column widths
 * - Dedicated prototype and experimental proof placeholder slides
 * - Dedicated academic references slide and clean separate thank-you slide
 */

const fs = require('fs');
const path = require('path');
const pptxgen = require('pptxgenjs');

// -------------------------------------------------------------
// DESIGN SYSTEM TOKENS — CLEAN ACADEMIC GREEN / SLATE / WHITE
// -------------------------------------------------------------
const C = {
  white: 'FFFFFF',        // Pure white background across all slides
  surface: 'F8FAFC',      // Soft clean panel fill (#F8FAFC)
  mintSurface: 'F0FDF4',  // Light subtle green tint for cards (#F0FDF4)
  mintBadge: 'DCFCE7',    // Badge and accent background (#DCFCE7)
  text: '111827',         // High-contrast near-black text (#111827)
  textSec: '374151',      // Secondary body text (#374151)
  muted: '6B7280',        // Muted gray labels and descriptions (#6B7280)
  green: '15803D',        // Classic academic forest green (#15803D)
  greenDark: '166534',    // Dark forest green for titles and headers (#166534)
  greenBorder: '000000',  // Black border for all boxed elements (#000000)
  border: '000000',       // Black border for all boxes (#000000)
  borderDark: '000000',   // Black border (#000000)
  warning: '000000',      // Black border for callout/warning boxes (#000000)
  warningBg: 'FFFBEB',    // Soft amber card fill (#FFFBEB)
  tableHeader: 'F0FDF4'   // Table header fill (#F0FDF4)
};

const FONT = 'Calibri';

// Diagram asset paths in E:\Client\Transformer_CBM\output\
const DIAG_1_HW = 'E:/Client/Transformer_CBM/output/diagram_1_hardware_block.png';
const DIAG_2_SW = 'E:/Client/Transformer_CBM/output/diagram_2_software_cloud_block.png';
const DIAG_3_COMB = 'E:/Client/Transformer_CBM/output/diagram_3_combined_architecture_block.png';
const DIAG_4_STATE = 'E:/Client/Transformer_CBM/output/diagram_4_hardware_state_flowchart.png';
const DIAG_5_ALGO = 'E:/Client/Transformer_CBM/output/diagram_5_predictive_thermal_flowchart.png';
const DIAG_6_SUP = 'E:/Client/Transformer_CBM/output/diagram_6_combined_supervisory_flowchart.png';
const CIRCUIT_IMG = 'E:/Client/Transformer_CBM/output/circuit_diagram_preview.png';

// Mathematical equation assets
const EQ_PROJECTION = path.join(__dirname, 'equation_projection.png');
const EQ_OLS = path.join(__dirname, 'equation_ols.png');

// -------------------------------------------------------------
// STANDARD SLIDE CREATION HELPER (Clean White Academic Style)
// -------------------------------------------------------------
function createStandardSlide(pres, titleText, subtitleText, slideNum, totalSlides = 21, presenterNote = '') {
  const slide = pres.addSlide();
  slide.background = { color: C.white };

  // Slide Title (Clean Near-Black with Green Category Bar)
  slide.addShape('rect', {
    x: 0.90,
    y: 0.44,
    w: 0.08,
    h: 0.44,
    fill: { color: C.green },
    line: { color: C.green, width: 0 }
  });

  slide.addText(titleText, {
    x: 1.10,
    y: 0.40,
    w: 11.33,
    h: 0.48,
    fontFace: FONT,
    fontSize: 22,
    bold: true,
    color: C.text,
    margin: 0
  });

  // Slide Subtitle
  if (subtitleText) {
    slide.addText(subtitleText, {
      x: 1.10,
      y: 0.90,
      w: 11.33,
      h: 0.28,
      fontFace: FONT,
      fontSize: 12,
      color: C.greenDark,
      margin: 0
    });
  }

  // Footer Rule (Clean Light Gray)
  slide.addShape('line', {
    x: 0.90,
    y: 6.70,
    w: 11.53,
    h: 0,
    line: { color: C.border, width: 1.0 }
  });

  // Footer Left
  slide.addText('IoT-Based Transformer Condition Monitoring with Predictive Adaptive Thermal Management Using ESP32', {
    x: 0.90,
    y: 6.80,
    w: 9.00,
    h: 0.25,
    fontFace: FONT,
    fontSize: 9,
    color: C.muted,
    margin: 0
  });

  // Footer Right (Slide Number)
  const numStr = slideNum < 10 ? `0${slideNum}` : `${slideNum}`;
  slide.addText(`${numStr} / ${totalSlides}`, {
    x: 10.20,
    y: 6.80,
    w: 2.23,
    h: 0.25,
    fontFace: FONT,
    fontSize: 9.5,
    bold: true,
    color: C.greenDark,
    align: 'right',
    margin: 0
  });

  if (presenterNote) {
    slide.addNotes(presenterNote);
  }

  return slide;
}

// =============================================================
// SLIDE 1 — TITLE PAGE (Clean Light Academic Style)
// =============================================================
function buildSlide1(pres) {
  const s1 = pres.addSlide();
  s1.background = { color: C.white };

  // Top Institution Bar
  s1.addShape('rect', {
    x: 0.90,
    y: 0.50,
    w: 11.53,
    h: 0.72,
    fill: { color: C.mintSurface },
    line: { color: C.greenBorder, width: 1.0 }
  });

  s1.addText('RAJALAKSHMI INSTITUTE OF TECHNOLOGY, CHENNAI', {
    x: 1.15,
    y: 0.58,
    w: 11.00,
    h: 0.28,
    fontFace: FONT,
    fontSize: 12.5,
    bold: true,
    color: C.greenDark,
    margin: 0
  });

  s1.addText('DEPARTMENT OF ELECTRONICS AND COMMUNICATION ENGINEERING  ·  CAPSTONE ENGINEERING PRESENTATION', {
    x: 1.15,
    y: 0.88,
    w: 11.00,
    h: 0.22,
    fontFace: FONT,
    fontSize: 9,
    bold: true,
    color: C.muted,
    margin: 0
  });

  // Main Project Title
  s1.addText('IoT-Based Transformer Condition Monitoring with\nPredictive Adaptive Thermal Management Using ESP32', {
    x: 0.90,
    y: 1.55,
    w: 11.53,
    h: 1.15,
    fontFace: FONT,
    fontSize: 26,
    bold: true,
    color: C.text,
    lineSpacingMultiple: 1.15,
    margin: 0
  });

  // Green Accent Divider
  s1.addShape('line', {
    x: 0.90,
    y: 2.85,
    w: 2.20,
    h: 0,
    line: { color: C.green, width: 2.5 }
  });

  // Subtitle / Execution Platform
  s1.addText('Demonstration Platform Executed on an ATX Switch-Mode Power Supply (SMPS)', {
    x: 0.90,
    y: 3.00,
    w: 11.53,
    h: 0.32,
    fontFace: FONT,
    fontSize: 14.5,
    color: C.textSec,
    margin: 0
  });

  // Team Box (Left) — Clean card with mint border
  s1.addShape('rect', {
    x: 0.90,
    y: 3.65,
    w: 6.80,
    h: 2.65,
    fill: { color: C.surface },
    line: { color: C.border, width: 1.2 }
  });

  s1.addShape('rect', {
    x: 0.90,
    y: 3.65,
    w: 6.80,
    h: 0.38,
    fill: { color: C.mintBadge },
    line: { color: C.greenBorder, width: 1.0 }
  });
  s1.addText('PROJECT TEAM MEMBERS', {
    x: 1.15,
    y: 3.73,
    w: 6.30,
    h: 0.24,
    fontFace: FONT,
    fontSize: 10.5,
    bold: true,
    color: C.greenDark,
    margin: 0
  });

  const students = [
    { name: 'Selvakumari S', reg: 'Reg. No: 211721106085' },
    { name: 'Shreya S', reg: 'Reg. No: 211721106095' },
    { name: 'Susmitha G', reg: 'Reg. No: 211721106103' }
  ];

  students.forEach((st, i) => {
    const y = 4.22 + i * 0.52;
    s1.addText(`${i + 1}.  ${st.name}`, {
      x: 1.15,
      y: y,
      w: 2.80,
      h: 0.28,
      fontFace: FONT,
      fontSize: 12,
      bold: true,
      color: C.text,
      margin: 0
    });
    s1.addText(st.reg, {
      x: 4.00,
      y: y + 0.02,
      w: 3.50,
      h: 0.26,
      fontFace: FONT,
      fontSize: 11,
      color: C.muted,
      margin: 0
    });
  });

  s1.addText('Department of Electronics and Communication Engineering  ·  Batch 2021–2025', {
    x: 1.15,
    y: 5.88,
    w: 6.30,
    h: 0.24,
    fontFace: FONT,
    fontSize: 9.5,
    color: C.muted,
    margin: 0
  });

  // Mentor Box (Right) — Mentor Name Only, NO email or phone
  s1.addShape('rect', {
    x: 8.00,
    y: 3.65,
    w: 4.43,
    h: 2.65,
    fill: { color: C.surface },
    line: { color: C.border, width: 1.2 }
  });

  s1.addShape('rect', {
    x: 8.00,
    y: 3.65,
    w: 4.43,
    h: 0.38,
    fill: { color: C.mintBadge },
    line: { color: C.greenBorder, width: 1.0 }
  });
  s1.addText('PROJECT MENTOR', {
    x: 8.25,
    y: 3.73,
    w: 3.90,
    h: 0.24,
    fontFace: FONT,
    fontSize: 10.5,
    bold: true,
    color: C.greenDark,
    margin: 0
  });

  s1.addText('Mrs. V. Subashini', {
    x: 8.25,
    y: 4.30,
    w: 3.90,
    h: 0.38,
    fontFace: FONT,
    fontSize: 17,
    bold: true,
    color: C.text,
    margin: 0
  });

  s1.addText(
    'Assistant Professor\n' +
    'Department of ECE\n' +
    'Rajalakshmi Institute of Technology, Chennai',
    {
      x: 8.25,
      y: 4.80,
      w: 3.90,
      h: 0.90,
      fontFace: FONT,
      fontSize: 11.5,
      color: C.muted,
      lineSpacingMultiple: 1.25,
      margin: 0
    }
  );

  s1.addNotes(
    'Introduce the project as an experimental monitoring and predictive thermal management platform using ESP32. ' +
    'The project is demonstrated on an ATX switch-mode power supply testbed to evaluate non-intrusive thermal sensing, ' +
    'trend extrapolation, and active cooling supervisory control.'
  );
  return s1;
}

// =============================================================
// SLIDE 2 — PRESENTATION OUTLINE
// =============================================================
function buildSlide2(pres) {
  const s2 = createStandardSlide(
    pres,
    'Presentation Outline',
    'Comprehensive structure across hardware, software, predictive control, and validation',
    2,
    21,
    'This roadmap outlines our presentation across eight core sections, covering the problem context, ' +
    'system architecture, detailed BOM, flowcharts, predictive regression methodology, prototype arrangement, and validation.'
  );

  const sections = [
    { num: '01', title: 'Introduction & Problem Context', desc: 'Thermal stress in power magnetics and motivation for predictive CBM' },
    { num: '02', title: 'Project Aim, Objectives & Scope', desc: 'Target specifications, validated boundaries, and platform delimitations' },
    { num: '03', title: 'System Architecture (End-to-End)', desc: 'Dual power domains, sensing array, ESP32 controller, and cloud sync' },
    { num: '04', title: 'Hardware Design & Component BOM', desc: 'Detailed bill of materials, circuit schematic, pinout, and load arrays' },
    { num: '05', title: 'Software & Concurrency Design', desc: 'Dual-core FreeRTOS tasks, local LittleFS dashboard, and cloud sync' },
    { num: '06', title: 'Predictive Thermal Algorithm', desc: 'Ordinary least-squares linear regression slope and forward projection' },
    { num: '07', title: 'Operational State Machine & Flowcharts', desc: 'Firmware state transitions, algorithmic sequences, and supervisory trips' },
    { num: '08', title: 'Prototype Bench, Proof & References', desc: 'Hardware setup, validation waveforms, testing matrix, and IEEE citations' }
  ];

  sections.forEach((sec, i) => {
    const col = i % 2;
    const row = Math.floor(i / 2);
    const x = 0.90 + col * 5.86;
    const y = 1.45 + row * 1.20;

    s2.addShape('rect', {
      x: x,
      y: y,
      w: 5.67,
      h: 1.05,
      fill: { color: C.surface },
      line: { color: C.border, width: 1.0 }
    });

    // Green number badge
    s2.addShape('rect', {
      x: x + 0.15,
      y: y + 0.16,
      w: 0.65,
      h: 0.72,
      fill: { color: C.mintBadge },
      line: { color: C.greenBorder, width: 1.0 }
    });
    s2.addText(sec.num, {
      x: x + 0.15,
      y: y + 0.30,
      w: 0.65,
      h: 0.40,
      fontFace: FONT,
      fontSize: 16,
      bold: true,
      color: C.greenDark,
      align: 'center',
      margin: 0
    });

    s2.addText(sec.title, {
      x: x + 0.95,
      y: y + 0.16,
      w: 4.55,
      h: 0.30,
      fontFace: FONT,
      fontSize: 13.5,
      bold: true,
      color: C.text,
      margin: 0
    });

    s2.addText(sec.desc, {
      x: x + 0.95,
      y: y + 0.48,
      w: 4.55,
      h: 0.48,
      fontFace: FONT,
      fontSize: 10.5,
      color: C.muted,
      lineSpacingMultiple: 1.15,
      margin: 0
    });
  });

  return s2;
}

// =============================================================
// SLIDE 3 — INTRODUCTION & PROBLEM CONTEXT
// =============================================================
function buildSlide3(pres) {
  const s3 = createStandardSlide(
    pres,
    'Introduction & Problem Context',
    'Shortcomings of legacy thermal protection and motivation for edge condition monitoring',
    3,
    21,
    'Transformers and power magnetics are vulnerable to thermal degradation. Conventional protection systems ' +
    'rely on reactive switches that only trip after core temperatures exceed safety thresholds. By combining surface ' +
    'and ambient digital sensing with multi-rail DC electrical telemetry, our ESP32 prototype projects temperature ' +
    'trajectories in advance and activates cooling proactively.'
  );

  // Left side: 3 clean cards
  const points = [
    {
      title: 'Power Transformer Vulnerability',
      desc: 'High-frequency magnetics and distribution transformers experience continuous thermal stress from harmonic losses, ambient heat, and sudden load surges, leading to accelerated Arrhenius dielectric insulation wear.'
    },
    {
      title: 'Shortcomings of Legacy Protection',
      desc: 'Conventional arrangements rely on reactive bi-metallic thermostats or external manual logbooks. They trip only AFTER temperatures breach critical thresholds, offering zero advance warning or adaptive speed regulation.'
    },
    {
      title: 'Proposed Edge CBM Architecture',
      desc: 'Consolidates multi-channel digital temperature sensing and multi-rail secondary power telemetry into a single ESP32 embedded node, using an ATX SMPS as a bench demonstration testbed.'
    }
  ];

  points.forEach((p, i) => {
    const y = 1.45 + i * 1.55;
    s3.addShape('rect', {
      x: 0.90,
      y: y,
      w: 6.20,
      h: 1.38,
      fill: { color: C.surface },
      line: { color: C.border, width: 1.0 }
    });
    s3.addText(p.title, {
      x: 1.15,
      y: y + 0.14,
      w: 5.70,
      h: 0.28,
      fontFace: FONT,
      fontSize: 13,
      bold: true,
      color: C.greenDark,
      margin: 0
    });
    s3.addText(p.desc, {
      x: 1.15,
      y: y + 0.44,
      w: 5.70,
      h: 0.82,
      fontFace: FONT,
      fontSize: 10.5,
      color: C.textSec,
      lineSpacingMultiple: 1.18,
      margin: 0
    });
  });

  // Right side: 3-step vertical flow (Observe -> Decide -> Respond)
  const flow = [
    { step: 'OBSERVE', sub: 'Non-Intrusive Sensing Array', text: 'Dual DS18B20 digital probes (surface & inlet ambient) + 3× INA219 power monitors on 12V, 5V, 3.3V.' },
    { step: 'DECIDE', sub: 'Edge Predictive Firmware', text: 'ESP32 executes 1Hz EMA filtering, rolling 30s linear regression trend projection, and boundary checks.' },
    { step: 'RESPOND', sub: 'Adaptive Actuation & Protection', text: 'High-frequency 25kHz PWM fan speed modulation via TB6612FNG, sub-5ms PS_ON# cutoff, and web telemetry.' }
  ];

  flow.forEach((f, i) => {
    const y = 1.45 + i * 1.55;
    s3.addShape('rect', {
      x: 7.45,
      y: y,
      w: 4.98,
      h: 1.38,
      fill: { color: C.mintSurface },
      line: { color: C.greenBorder, width: 1.0 }
    });
    s3.addText(f.step, {
      x: 7.70,
      y: y + 0.12,
      w: 4.48,
      h: 0.24,
      fontFace: FONT,
      fontSize: 11.5,
      bold: true,
      color: C.greenDark,
      margin: 0
    });
    s3.addText(f.sub, {
      x: 7.70,
      y: y + 0.36,
      w: 4.48,
      h: 0.24,
      fontFace: FONT,
      fontSize: 11,
      bold: true,
      color: C.text,
      margin: 0
    });
    s3.addText(f.text, {
      x: 7.70,
      y: y + 0.62,
      w: 4.48,
      h: 0.66,
      fontFace: FONT,
      fontSize: 10,
      color: C.textSec,
      lineSpacingMultiple: 1.15,
      margin: 0
    });

    if (i < 2) {
      s3.addShape('line', {
        x: 9.94,
        y: y + 1.38,
        w: 0,
        h: 0.17,
        line: { color: C.green, width: 1.8 }
      });
    }
  });

  return s3;
}

// =============================================================
// SLIDE 4 — PROBLEM STATEMENT & OBJECTIVES
// =============================================================
function buildSlide4(pres) {
  const s4 = createStandardSlide(
    pres,
    'Problem Statement & Project Objectives',
    'Engineering problem statement and specific technical milestones',
    4,
    21,
    'Our objective is to design a cohesive embedded prototype that bridges the gap between discrete instrumentation ' +
    'and smart supervisory protection. We monitor three DC output rails and two temperature points simultaneously, ' +
    'applying forward trend extrapolation to modulate cooling demand and protect hardware.'
  );

  // Top Problem Statement Panel
  s4.addShape('rect', {
    x: 0.90,
    y: 1.45,
    w: 11.53,
    h: 0.85,
    fill: { color: C.mintSurface },
    line: { color: C.greenBorder, width: 1.0 }
  });
  s4.addText('CORE ENGINEERING CHALLENGE', {
    x: 1.15,
    y: 1.55,
    w: 11.00,
    h: 0.22,
    fontFace: FONT,
    fontSize: 10,
    bold: true,
    color: C.greenDark,
    margin: 0
  });
  s4.addText(
    'Develop an autonomous, low-cost condition monitoring prototype that measures multi-channel thermal and DC electrical parameters, ' +
    'extrapolates short-term temperature trajectories to drive predictive cooling, and enforces local supervisory safety trips ' +
    'without internet dependency.',
    {
      x: 1.15,
      y: 1.78,
      w: 11.00,
      h: 0.45,
      fontFace: FONT,
      fontSize: 12.5,
      bold: true,
      color: C.text,
      lineSpacingMultiple: 1.18,
      margin: 0
    }
  );

  // 6 Numbered Objectives (2 columns x 3 rows)
  const objs = [
    { num: '01', title: 'Surface & Ambient Sensing', desc: 'Acquire calibrated surface and ambient inlet air temperatures via dual OneWire digital probes.' },
    { num: '02', title: 'Multi-Rail DC Supervision', desc: 'Continuously measure bus voltages, currents, and power across +12V, +5V, and +3.3V secondary rails.' },
    { num: '03', title: 'Rolling Trend Extrapolation', desc: 'Compute temperature-rise gradients (r in °C/s) over a 30-sample sliding FIFO buffer using linear regression.' },
    { num: '04', title: 'Adaptive Predictive Cooling', desc: 'Modulate a 12V cooling fan dynamically using 25kHz PWM to suppress thermal inertia before trip thresholds.' },
    { num: '05', title: 'Supervisory Hardware Shutdown', desc: 'De-assert the active-low PS_ON# signal to collapse all main output rails upon confirmed threshold breach.' },
    { num: '06', title: 'Dual-Tier Telemetry & Dashboards', desc: 'Serve local real-time diagnostics via 16x2 LCD & LittleFS AP, with asynchronous remote cloud synchronization.' }
  ];

  objs.forEach((o, i) => {
    const col = i % 2;
    const row = Math.floor(i / 2);
    const x = 0.90 + col * 5.95;
    const y = 2.48 + row * 1.18;

    s4.addShape('rect', {
      x: x,
      y: y,
      w: 5.58,
      h: 1.05,
      fill: { color: C.surface },
      line: { color: C.border, width: 1.0 }
    });

    s4.addShape('rect', {
      x: x + 0.15,
      y: y + 0.15,
      w: 0.55,
      h: 0.65,
      fill: { color: C.mintBadge },
      line: { color: C.greenBorder, width: 1.0 }
    });
    s4.addText(o.num, {
      x: x + 0.15,
      y: y + 0.28,
      w: 0.55,
      h: 0.38,
      fontFace: FONT,
      fontSize: 15,
      bold: true,
      color: C.greenDark,
      align: 'center',
      margin: 0
    });

    s4.addText(o.title, {
      x: x + 0.85,
      y: y + 0.15,
      w: 4.55,
      h: 0.28,
      fontFace: FONT,
      fontSize: 12.5,
      bold: true,
      color: C.text,
      margin: 0
    });
    s4.addText(o.desc, {
      x: x + 0.85,
      y: y + 0.44,
      w: 4.55,
      h: 0.50,
      fontFace: FONT,
      fontSize: 10,
      color: C.textSec,
      lineSpacingMultiple: 1.15,
      margin: 0
    });
  });

  return s4;
}

// =============================================================
// SLIDE 5 — PROJECT SCOPE & LIMITATIONS
// =============================================================
function buildSlide5(pres) {
  const s5 = createStandardSlide(
    pres,
    'Project Scope, Boundaries & Limitations',
    'Academic engineering delimitation between verified prototype features and excluded claims',
    5,
    21,
    'Boundary definition is essential for engineering integrity. This prototype validates embedded predictive monitoring ' +
    'on a low-voltage switch-mode power supply bench. We monitor surface temperature rather than internal copper hot spots, ' +
    'and fan control operates as a command percentage without tachometer feedback. Standby power requires AC mains; ' +
    'the prototype has no auxiliary battery.'
  );

  // Left Panel: Included
  s5.addShape('rect', {
    x: 0.90,
    y: 1.45,
    w: 5.60,
    h: 4.10,
    fill: { color: C.surface },
    line: { color: C.greenBorder, width: 1.2 }
  });
  s5.addShape('rect', {
    x: 0.90,
    y: 1.45,
    w: 5.60,
    h: 0.40,
    fill: { color: C.mintBadge },
    line: { color: C.greenBorder, width: 1.0 }
  });
  s5.addText('Included in This Prototype', {
    x: 1.15,
    y: 1.52,
    w: 5.10,
    h: 0.26,
    fontFace: FONT,
    fontSize: 12.5,
    bold: true,
    color: C.greenDark,
    margin: 0
  });

  const includedItems = [
    'ATX SMPS Demonstration Platform: Low-voltage bench testbed providing switched rails and continuous standby.',
    'Dual-Channel Temperature Sensing: Core surface probe and ambient inlet air probe via calibrated OneWire.',
    '3-Rail DC Secondary Monitoring: Real-time voltage, current, and power tracking on 12V, 5V, and 3.3V.',
    'Predictive PWM Fan Modulation: High-frequency duty cycle control to mitigate thermal rise before trips.',
    'Autonomous Supervisory Shutdown: Active-low PS_ON# cutoff upon confirmed threshold limit.',
    'Dual-Tier UI: Local 16x2 character LCD carousel and remote Firebase cloud web view.'
  ];

  includedItems.forEach((item, i) => {
    const y = 1.95 + i * 0.58;
    s5.addText(`•  ${item}`, {
      x: 1.10,
      y: y,
      w: 5.20,
      h: 0.52,
      fontFace: FONT,
      fontSize: 9.5,
      color: C.textSec,
      lineSpacingMultiple: 1.15,
      margin: 0
    });
  });

  // Right Panel: Outside Scope
  s5.addShape('rect', {
    x: 6.83,
    y: 1.45,
    w: 5.60,
    h: 4.10,
    fill: { color: C.surface },
    line: { color: C.border, width: 1.2 }
  });
  s5.addShape('rect', {
    x: 6.83,
    y: 1.45,
    w: 5.60,
    h: 0.40,
    fill: { color: 'F1F5F9' },
    line: { color: C.border, width: 1.0 }
  });
  s5.addText('Outside the Validated Scope', {
    x: 7.08,
    y: 1.52,
    w: 5.10,
    h: 0.26,
    fontFace: FONT,
    fontSize: 12.5,
    bold: true,
    color: C.text,
    margin: 0
  });

  const excludedItems = [
    'Direct Winding Hot-Spot: Only surface temperature is measured; internal hot-spots are estimated mathematically.',
    'Mains-Input AC Power Analysis: Primary AC mains current, power factor, and harmonics are not instrumented.',
    'Direct Fan Speed RPM Feedback: Fan command is output as PWM %; direct tachometer speed feedback is not wired.',
    'Certified Substation Protection: Demonstration bench—not a certified utility safety relay or emergency-stop.',
    'Battery-Backed Uninterrupted Power: Standby monitoring requires AC mains; the prototype has no battery backup.',
    'Galvanic Power Isolation: Standby (+5VSB) and switched rails share a common circuit ground reference.'
  ];

  excludedItems.forEach((item, i) => {
    const y = 1.95 + i * 0.58;
    s5.addText(`•  ${item}`, {
      x: 7.03,
      y: y,
      w: 5.20,
      h: 0.52,
      fontFace: FONT,
      fontSize: 9.5,
      color: C.muted,
      lineSpacingMultiple: 1.15,
      margin: 0
    });
  });

  // Bottom Notice
  s5.addShape('rect', {
    x: 0.90,
    y: 5.75,
    w: 11.53,
    h: 0.45,
    fill: { color: C.warningBg },
    line: { color: C.warning, width: 1.0 }
  });
  s5.addText('Standby-powered operation requires continuous AC mains power. The system contains no auxiliary battery backup.', {
    x: 1.15,
    y: 5.86,
    w: 11.00,
    h: 0.24,
    fontFace: FONT,
    fontSize: 10.5,
    bold: true,
    color: C.warning,
    margin: 0
  });

  return s5;
}

// =============================================================
// SLIDE 6 — SYSTEM ARCHITECTURE (COMBINED OVERVIEW)
// =============================================================
function buildSlide6(pres) {
  const s6 = createStandardSlide(
    pres,
    'End-to-End System Architecture',
    'Comprehensive architectural overview: sensing, edge processing, local control, and cloud supervision',
    6,
    21,
    'This diagram illustrates the complete system architecture. On the left, physical temperature probes and high-side ' +
    'power monitors stream data into the ESP32. In the centre, FreeRTOS tasks execute digital filtering, rolling regression, ' +
    'and trip evaluation. Actuation controls the fan and the PS_ON line, while cloud services provide non-blocking remote visibility.'
  );

  // Diagram Image on Left: w=7.60, h=4.75
  if (fs.existsSync(DIAG_3_COMB)) {
    s6.addShape('rect', {
      x: 0.90,
      y: 1.45,
      w: 7.60,
      h: 4.75,
      fill: { color: C.surface },
      line: { color: C.border, width: 1.0 }
    });
    s6.addImage({
      path: DIAG_3_COMB,
      x: 1.00,
      y: 1.55,
      w: 7.40,
      h: 4.55,
      sizing: { type: 'contain', w: 7.40, h: 4.55 }
    });
  }

  // Right Side Concise Architecture Cards: w=3.63, h=4.75
  s6.addShape('rect', {
    x: 8.80,
    y: 1.45,
    w: 3.63,
    h: 4.75,
    fill: { color: C.mintSurface },
    line: { color: C.greenBorder, width: 1.0 }
  });
  s6.addText('Core Architecture Zones', {
    x: 9.05,
    y: 1.65,
    w: 3.15,
    h: 0.28,
    fontFace: FONT,
    fontSize: 13,
    bold: true,
    color: C.greenDark,
    margin: 0
  });
  s6.addShape('line', { x: 9.05, y: 1.98, w: 1.80, h: 0, line: { color: C.green, width: 2 } });

  const zones = [
    { title: '1. Sensing Domain', desc: 'Dual OneWire DS18B20 probes & 3× INA219 I2C high-side rail power monitors.' },
    { title: '2. ESP32 Controller', desc: 'Deterministic 1Hz FreeRTOS loop: EMA filter, 30s regression, and trips.' },
    { title: '3. Local Actuation', desc: '25kHz PWM fan control via TB6612FNG & active-low NPN PS_ON# cutoff.' },
    { title: '4. Cloud Supervision', desc: 'Non-blocking Firebase push, Cloudflare Worker watchdog, and Brevo email.' }
  ];

  zones.forEach((z, i) => {
    const y = 2.15 + i * 1.00;
    s6.addText(z.title, {
      x: 9.05,
      y: y,
      w: 3.15,
      h: 0.24,
      fontFace: FONT,
      fontSize: 11,
      bold: true,
      color: C.text,
      margin: 0
    });
    s6.addText(z.desc, {
      x: 9.05,
      y: y + 0.24,
      w: 3.15,
      h: 0.65,
      fontFace: FONT,
      fontSize: 9.5,
      color: C.textSec,
      lineSpacingMultiple: 1.15,
      margin: 0
    });
  });

  return s6;
}

// =============================================================
// SLIDE 7 — HARDWARE CIRCUIT BLOCK DIAGRAM
// =============================================================
function buildSlide7(pres) {
  const s7 = createStandardSlide(
    pres,
    'Hardware Circuit Architecture',
    'Physical electrical subsystem topology, digital sensor buses, and actuator interfaces',
    7,
    21,
    'This hardware circuit block diagram details the physical layout. Notice the clear separation between the +5VSB ' +
    'uninterruptible standby domain and the main switched DC power buses. The ESP32 interfaces with digital sensors via ' +
    'I2C and 1-Wire, while driving the cooling motor through an isolated H-bridge.'
  );

  // Diagram on Left: w=7.60, h=4.75
  if (fs.existsSync(DIAG_1_HW)) {
    s7.addShape('rect', {
      x: 0.90,
      y: 1.45,
      w: 7.60,
      h: 4.75,
      fill: { color: C.surface },
      line: { color: C.border, width: 1.0 }
    });
    s7.addImage({
      path: DIAG_1_HW,
      x: 1.00,
      y: 1.55,
      w: 7.40,
      h: 4.55,
      sizing: { type: 'contain', w: 7.40, h: 4.55 }
    });
  }

  // Right Side Notes: w=3.63, h=4.75
  s7.addShape('rect', {
    x: 8.80,
    y: 1.45,
    w: 3.63,
    h: 4.75,
    fill: { color: C.surface },
    line: { color: C.border, width: 1.0 }
  });
  s7.addText('Circuit Key Features', {
    x: 9.05,
    y: 1.65,
    w: 3.15,
    h: 0.28,
    fontFace: FONT,
    fontSize: 13,
    bold: true,
    color: C.greenDark,
    margin: 0
  });
  s7.addShape('line', { x: 9.05, y: 1.98, w: 1.80, h: 0, line: { color: C.green, width: 2 } });

  const hwPoints = [
    { title: 'Standby Power Path', desc: '+5VSB continuous rail feeds ESP32 DevKit through AMS1117-3.3 regulator.' },
    { title: 'Independent Rail Shunts', desc: 'Three separate INA219 modules monitor 12V, 5V, 3.3V with 0.1Ω precision shunts.' },
    { title: 'Active-Low PS_ON# Circuit', desc: '2N2222A NPN clamps PS_ON# to COM; cutoff safely floats wire to 5V (< 5ms).' },
    { title: 'Shared Communication', desc: 'I2C (SDA/SCL) and OneWire (GPIO4) operate with common ground reference.' }
  ];

  hwPoints.forEach((p, i) => {
    const y = 2.15 + i * 1.00;
    s7.addText(p.title, {
      x: 9.05,
      y: y,
      w: 3.15,
      h: 0.24,
      fontFace: FONT,
      fontSize: 11,
      bold: true,
      color: C.text,
      margin: 0
    });
    s7.addText(p.desc, {
      x: 9.05,
      y: y + 0.24,
      w: 3.15,
      h: 0.65,
      fontFace: FONT,
      fontSize: 9.5,
      color: C.textSec,
      lineSpacingMultiple: 1.15,
      margin: 0
    });
  });

  return s7;
}

// =============================================================
// SLIDE 8 — MASTER CIRCUIT SCHEMATIC & INTERCONNECTIONS
// =============================================================
function buildSlide8(pres) {
  const s8 = createStandardSlide(
    pres,
    'Circuit Design and Interconnections',
    'Complete schematic wiring diagram connecting ESP32, power supply, sensors, and actuation',
    8,
    21,
    'This detailed schematic shows the exact pin-to-pin wiring. Four distinct functional domains interact: power distribution, ' +
    'digital sensor communication, motor actuation, and the supervisory PS_ON shutdown interface. Note that the LCD PCF8574 ' +
    'pull-up resistors are tied to 3.3V to protect the ESP32 GPIOs.'
  );

  // Diagram on Left: w=7.60, h=4.50
  if (fs.existsSync(CIRCUIT_IMG)) {
    s8.addShape('rect', {
      x: 0.90,
      y: 1.45,
      w: 7.60,
      h: 4.50,
      fill: { color: C.surface },
      line: { color: C.border, width: 1.0 }
    });
    s8.addImage({
      path: CIRCUIT_IMG,
      x: 1.00,
      y: 1.55,
      w: 7.40,
      h: 4.30,
      sizing: { type: 'contain', w: 7.40, h: 4.30 }
    });
  }

  // Caption below schematic
  s8.addText('General interconnection concept — interface details pending final revision.', {
    x: 0.90,
    y: 6.05,
    w: 7.60,
    h: 0.25,
    fontFace: FONT,
    fontSize: 9.5,
    italic: true,
    color: C.muted,
    margin: 0
  });

  // Right Side Notes: w=3.63, h=4.75
  s8.addShape('rect', {
    x: 8.80,
    y: 1.45,
    w: 3.63,
    h: 4.75,
    fill: { color: C.mintSurface },
    line: { color: C.greenBorder, width: 1.0 }
  });
  s8.addText('Schematic Notes', {
    x: 9.05,
    y: 1.65,
    w: 3.15,
    h: 0.28,
    fontFace: FONT,
    fontSize: 13,
    bold: true,
    color: C.greenDark,
    margin: 0
  });
  s8.addShape('line', { x: 9.05, y: 1.98, w: 1.80, h: 0, line: { color: C.green, width: 2 } });

  const notes = [
    { title: 'Power Segregation', text: '+5VSB standby rail powers ESP32 continuously. Switched rails power test loads.' },
    { title: 'I2C Addressing', text: 'Three INA219 monitors at 0x40, 0x41, and 0x44; PCF8574 LCD backpack at 0x27.' },
    { title: 'OneWire Bus Line', text: 'DS18B20 digital probes tied to GPIO4 with a 4.7kΩ pull-up resistor to 3.3V.' },
    { title: 'Actuation & Trip', text: 'GPIO19 drives TB6612FNG PWM. GPIO32 drives 2N2222A for PS_ON# clamp.' }
  ];

  notes.forEach((n, i) => {
    const y = 2.15 + i * 1.00;
    s8.addText(n.title, {
      x: 9.05,
      y: y,
      w: 3.15,
      h: 0.24,
      fontFace: FONT,
      fontSize: 11,
      bold: true,
      color: C.text,
      margin: 0
    });
    s8.addText(n.text, {
      x: 9.05,
      y: y + 0.24,
      w: 3.15,
      h: 0.65,
      fontFace: FONT,
      fontSize: 9.5,
      color: C.textSec,
      lineSpacingMultiple: 1.15,
      margin: 0
    });
  });

  return s8;
}

// =============================================================
// SLIDE 9 — DETAILED COMPONENT LIST & BILL OF MATERIALS (BOM)
// =============================================================
function buildSlide9(pres) {
  const s9 = createStandardSlide(
    pres,
    'Component List & Bill of Materials (BOM)',
    'Comprehensive hardware specifications, interface protocols, and system roles',
    9,
    21,
    'Here is our complete bill of materials. The system is built around the dual-core ESP32, paired with digital sensors ' +
    'to avoid analog ADC noise. The INA219 power monitors stream 12-bit bus metrics over I2C, while the TB6612FNG provides ' +
    'MOSFET PWM motor control. The total cost remains well under standard industrial monitoring hardware.'
  );

  const bomRows = [
    [
      { text: 'Subsystem', options: { fill: { color: C.tableHeader }, bold: true, color: C.text, fontSize: 11 } },
      { text: 'Component / Part', options: { fill: { color: C.tableHeader }, bold: true, color: C.text, fontSize: 11 } },
      { text: 'Key Specifications', options: { fill: { color: C.tableHeader }, bold: true, color: C.text, fontSize: 11 } },
      { text: 'Interface / Domain', options: { fill: { color: C.tableHeader }, bold: true, color: C.text, fontSize: 11 } },
      { text: 'Role in Prototype', options: { fill: { color: C.tableHeader }, bold: true, color: C.text, fontSize: 11 } }
    ],
    [
      { text: 'Processing', options: { bold: true, color: C.greenDark } },
      { text: 'ESP32-WROOM-32D', options: { bold: true, color: C.text } },
      { text: 'Dual-Core Xtensa LX6 @ 240MHz, 520KB SRAM, 4MB Flash' },
      { text: '+5VSB Standby' },
      { text: 'Main controller: acquisition, regression math, and trips' }
    ],
    [
      { text: 'Thermal Sensing', options: { bold: true, color: C.greenDark } },
      { text: '2× Maxim DS18B20', options: { bold: true, color: C.text } },
      { text: 'Digital probe, ±0.5°C accuracy (-10 to +85°C), 12-bit' },
      { text: '1-Wire Bus (GPIO4)' },
      { text: 'CH1: Core surface temp; CH2: Ambient air inlet' }
    ],
    [
      { text: 'Power Telemetry', options: { bold: true, color: C.greenDark } },
      { text: '3× TI INA219', options: { bold: true, color: C.text } },
      { text: 'High-side voltage & current, 0-26V, 0.1Ω shunt, 12-bit ADC' },
      { text: 'I2C (0x40, 0x41, 0x44)' },
      { text: 'Continuous telemetry on +12V, +5V, +3.3V secondary rails' }
    ],
    [
      { text: 'Fan Actuator', options: { bold: true, color: C.greenDark } },
      { text: 'Toshiba TB6612FNG', options: { bold: true, color: C.text } },
      { text: 'Dual H-Bridge MOSFET driver, 1.2A cont, 25kHz PWM capable' },
      { text: 'PWM (GPIO19) + 12V' },
      { text: 'Adaptive speed modulation of cooling fan' }
    ],
    [
      { text: 'Supervisory Trip', options: { bold: true, color: C.greenDark } },
      { text: '2N2222A NPN Transistor', options: { bold: true, color: C.text } },
      { text: '40V / 600mA discrete BJT with 1kΩ base current limiting resistor' },
      { text: 'GPIO32 to ATX PS_ON#' },
      { text: 'Clamps active-low PS_ON# to COM; releases upon trip' }
    ],
    [
      { text: 'Local Display', options: { bold: true, color: C.greenDark } },
      { text: '16×2 LCD + PCF8574', options: { bold: true, color: C.text } },
      { text: 'HD44780 character LCD with 3.3V pull-up modification' },
      { text: 'I2C Bus (0x27)' },
      { text: 'Continuous local display of temperatures, rails, and trip state' }
    ],
    [
      { text: 'Power Platform', options: { bold: true, color: C.greenDark } },
      { text: 'ATX SMPS (450W)', options: { bold: true, color: C.text } },
      { text: 'Switch-mode power supply: +12V, +5V, +3.3V, +5VSB standby' },
      { text: 'AC Mains (230V)' },
      { text: 'Demonstration platform simulating multi-rail transformer loads' }
    ]
  ];

  s9.addTable(bomRows, {
    x: 0.90,
    y: 1.45,
    w: 11.53,
    colW: [1.60, 2.20, 3.10, 1.80, 2.83],
    fontFace: FONT,
    fontSize: 9.5,
    border: { pt: 1, color: C.border },
    rowH: [0.38, 0.52, 0.52, 0.52, 0.52, 0.52, 0.52, 0.52]
  });

  return s9;
}

// =============================================================
// SLIDE 10 — SOFTWARE & CLOUD ARCHITECTURE
// =============================================================
function buildSlide10(pres) {
  const s10 = createStandardSlide(
    pres,
    'Software & Cloud Supervision Architecture',
    'Multi-tier execution: bare-metal deterministic loops, local web server, and cloud alerting',
    10,
    21,
    'The software architecture enforces strict task segregation across three tiers. Deterministic FreeRTOS Core 1 tasks ' +
    'handle sensor acquisition, filtering, regression, and safety trips every second. Core 0 hosts the local LittleFS web server, ' +
    'while non-blocking asynchronous cloud tasks push frames to Firebase and trigger Brevo email alerts through Cloudflare Workers.'
  );

  // Diagram on Left: w=7.60, h=4.75
  if (fs.existsSync(DIAG_2_SW)) {
    s10.addShape('rect', {
      x: 0.90,
      y: 1.45,
      w: 7.60,
      h: 4.75,
      fill: { color: C.surface },
      line: { color: C.border, width: 1.0 }
    });
    s10.addImage({
      path: DIAG_2_SW,
      x: 1.00,
      y: 1.55,
      w: 7.40,
      h: 4.55,
      sizing: { type: 'contain', w: 7.40, h: 4.55 }
    });
  }

  // Right Side Notes: w=3.63, h=4.75
  s10.addShape('rect', {
    x: 8.80,
    y: 1.45,
    w: 3.63,
    h: 4.75,
    fill: { color: C.mintSurface },
    line: { color: C.greenBorder, width: 1.0 }
  });
  s10.addText('Software Principles', {
    x: 9.05,
    y: 1.65,
    w: 3.15,
    h: 0.28,
    fontFace: FONT,
    fontSize: 13,
    bold: true,
    color: C.greenDark,
    margin: 0
  });
  s10.addShape('line', { x: 9.05, y: 1.98, w: 1.80, h: 0, line: { color: C.green, width: 2 } });

  const swPoints = [
    { title: 'Core 1: Real-Time Engine', desc: '1Hz deterministic loop executing sensor checks, rolling regression, and trip logic.' },
    { title: 'Core 0: Local Web Server', desc: 'Lightweight LittleFS HTTP server providing diagnostic access over captive Wi-Fi AP.' },
    { title: 'Non-Blocking Cloud Sync', desc: 'Telemetry pushed asynchronously; cloud disconnect never blocks local protection.' },
    { title: 'Serverless Worker Watchdog', desc: 'Cloudflare Worker monitors heartbeats and triggers Brevo email alerts on trip events.' }
  ];

  swPoints.forEach((p, i) => {
    const y = 2.15 + i * 1.00;
    s10.addText(p.title, {
      x: 9.05,
      y: y,
      w: 3.15,
      h: 0.24,
      fontFace: FONT,
      fontSize: 11,
      bold: true,
      color: C.text,
      margin: 0
    });
    s10.addText(p.desc, {
      x: 9.05,
      y: y + 0.24,
      w: 3.15,
      h: 0.65,
      fontFace: FONT,
      fontSize: 9.5,
      color: C.textSec,
      lineSpacingMultiple: 1.15,
      margin: 0
    });
  });

  return s10;
}

// =============================================================
// SLIDE 11 — WORKING METHODOLOGY & MATHEMATICAL FORMULATION
// =============================================================
function buildSlide11(pres) {
  const s11 = createStandardSlide(
    pres,
    'Working Methodology & Predictive Algorithm',
    'Mathematical formulation: rolling linear regression slope, forward horizon, and PWM cooling demand',
    11,
    21,
    'Our predictive thermal algorithm anticipates temperature rise before physical thermal inertia reaches critical limits. ' +
    'The 1-hertz acquisition feeds an exponential moving average filter. An ordinary least-squares regression calculates the ' +
    'temperature-rise slope over a 30-second sliding buffer, projecting forward by horizon H to drive PWM fan duty cycle.'
  );

  // 6-step pipeline across top
  const steps = ['1. Acquire', '2. Validate', '3. Filter (EMA)', '4. OLS Slope (r)', '5. Project (Tp)', '6. Set Fan PWM'];
  const stepW = 1.68;
  const stepGap = 0.28;
  const startX = 0.90;

  steps.forEach((st, i) => {
    const x = startX + i * (stepW + stepGap);
    s11.addShape('rect', {
      x: x,
      y: 1.45,
      w: stepW,
      h: 0.60,
      fill: { color: C.mintSurface },
      line: { color: C.greenBorder, width: 1.0 }
    });
    s11.addText(st, {
      x: x + 0.05,
      y: 1.60,
      w: stepW - 0.10,
      h: 0.28,
      fontFace: FONT,
      fontSize: 10,
      bold: true,
      color: C.greenDark,
      align: 'center',
      margin: 0
    });

    if (i < steps.length - 1) {
      s11.addShape('line', {
        x: x + stepW + 0.04,
        y: 1.75,
        w: stepGap - 0.08,
        h: 0,
        line: { color: C.green, width: 1.8, endArrowType: 'triangle' }
      });
    }
  });

  // Equation Panel (Left): w=6.80, h=3.68
  s11.addShape('rect', {
    x: 0.90,
    y: 2.20,
    w: 6.80,
    h: 3.68,
    fill: { color: C.surface },
    line: { color: C.border, width: 1.2 }
  });
  s11.addText('Forward Temperature Projection Equation', {
    x: 1.15,
    y: 2.34,
    w: 6.30,
    h: 0.26,
    fontFace: FONT,
    fontSize: 13,
    bold: true,
    color: C.greenDark,
    margin: 0
  });

  // Display Equation Box
  s11.addShape('rect', {
    x: 1.15,
    y: 2.65,
    w: 6.30,
    h: 0.70,
    fill: { color: C.mintBadge },
    line: { color: C.greenBorder, width: 1.0 }
  });

  s11.addImage({
    path: EQ_PROJECTION,
    x: 2.25,
    y: 2.68,
    w: 4.10,
    h: 0.64
  });

  s11.addText([
    { text: 'Mathematical Variables & Formulations:\n', options: { bold: true, color: C.greenDark, fontSize: 10.5 } },
    { text: '•  ', options: { bold: true, color: C.greenDark } },
    { text: 'T', options: { italic: true, bold: true } },
    { text: 'p', options: { subscript: true, bold: true } },
    { text: ' : Projected surface temperature forward across prediction horizon H (°C)\n' },
    { text: '•  ', options: { bold: true, color: C.greenDark } },
    { text: 'T', options: { italic: true, bold: true } },
    { text: 'f', options: { subscript: true, bold: true } },
    { text: ' : Exponential Moving Average (EMA) filtered core surface temperature (°C)\n' },
    { text: '•  ', options: { bold: true, color: C.greenDark } },
    { text: 'r', options: { italic: true, bold: true } },
    { text: ' : Temperature-rise gradient from 30-sample rolling OLS regression (°C/s)\n' },
    { text: '•  ', options: { bold: true, color: C.greenDark } },
    { text: 'H', options: { italic: true, bold: true } },
    { text: ' : Proposed forward prediction horizon constant (H = 30 seconds)\n' },
    { text: '•  ', options: { bold: true, color: C.greenDark } },
    { text: 'max(0, r)', options: { bold: true } },
    { text: ' : Half-wave rectification ensuring fan is not throttled down during rapid heating\n' },
    { text: '•  ', options: { bold: true, color: C.greenDark } },
    { text: 'D', options: { italic: true, bold: true } },
    { text: 'auto', options: { subscript: true, bold: true } },
    { text: ' = max(g(T', options: { bold: true } },
    { text: 'f', options: { subscript: true, bold: true } },
    { text: '), g(T', options: { bold: true } },
    { text: 'p', options: { subscript: true, bold: true } },
    { text: ')) : Dynamic dual-demand fan PWM modulation function', options: { bold: true } }
  ], {
    x: 1.15,
    y: 3.45,
    w: 6.30,
    h: 2.30,
    fontFace: FONT,
    fontSize: 9.5,
    color: C.textSec,
    lineSpacingMultiple: 1.18,
    margin: 0
  });

  // Parameter Panel (Right): w=4.48, h=3.68
  s11.addShape('rect', {
    x: 7.95,
    y: 2.20,
    w: 4.48,
    h: 3.68,
    fill: { color: C.surface },
    line: { color: C.border, width: 1.2 }
  });
  s11.addText('Proposed Baseline Parameters', {
    x: 8.20,
    y: 2.34,
    w: 4.00,
    h: 0.26,
    fontFace: FONT,
    fontSize: 13,
    bold: true,
    color: C.text,
    margin: 0
  });
  s11.addShape('line', { x: 8.20, y: 2.65, w: 1.80, h: 0, line: { color: C.green, width: 2 } });
  s11.addText([
    { text: '•  Sampling Frequency: ', options: { bold: true, color: C.text } },
    { text: 'f', options: { italic: true } },
    { text: 's', options: { subscript: true } },
    { text: ' = 1.0 Hz (T = 1.0 s)\n\n' },
    { text: '•  Sliding Buffer Depth: ', options: { bold: true, color: C.text } },
    { text: 'N', options: { italic: true } },
    { text: ' = 30 samples\n\n' },
    { text: '•  Forward Horizon: ', options: { bold: true, color: C.text } },
    { text: 'H', options: { italic: true } },
    { text: ' = 30 seconds\n\n' },
    { text: '•  EMA Smoothing Factor: ', options: { bold: true, color: C.text } },
    { text: 'α = 0.20\n\n' },
    { text: '•  Minimum Cooling Duty: ', options: { bold: true, color: C.text } },
    { text: '20% PWM (Idling baseline)\n\n' },
    { text: '•  Thermal Warning Ceiling: ', options: { bold: true, color: C.text } },
    { text: 'T', options: { italic: true } },
    { text: 'warn', options: { subscript: true } },
    { text: ' = 65°C\n\n' },
    { text: '•  Critical Shutdown Limit: ', options: { bold: true, color: C.text } },
    { text: 'T', options: { italic: true } },
    { text: 'trip', options: { subscript: true } },
    { text: ' = 75°C' }
  ], {
    x: 8.20,
    y: 2.76,
    w: 4.00,
    h: 3.00,
    fontFace: FONT,
    fontSize: 9.5,
    color: C.textSec,
    lineSpacingMultiple: 1.15,
    margin: 0
  });

  // Bottom Qualification Note
  s11.addShape('rect', {
    x: 0.90,
    y: 6.05,
    w: 11.53,
    h: 0.38,
    fill: { color: C.mintSurface },
    line: { color: C.greenBorder, width: 1.0 }
  });
  s11.addText('A 30-second projection horizon represents a dynamic estimation window—not a guaranteed 30-second warning in all conditions.', {
    x: 1.15,
    y: 6.13,
    w: 11.00,
    h: 0.24,
    fontFace: FONT,
    fontSize: 10,
    italic: true,
    color: C.greenDark,
    margin: 0
  });

  return s11;
}

// =============================================================
// SLIDE 12 — PREDICTIVE THERMAL ALGORITHM FLOWCHART
// =============================================================
function buildSlide12(pres) {
  const s12 = createStandardSlide(
    pres,
    'Predictive Thermal Algorithm Flowchart',
    'Step-by-step flowchart of the 1-hertz temperature acquisition, linear regression, and fan modulation logic',
    12,
    21,
    'This flowchart details the algorithm running inside the ESP32 timer loop. Every second, raw digital temperature ' +
    'readings are validated and smoothed with an EMA filter. If the 30-sample buffer is full, ordinary least-squares calculates ' +
    'the heating slope. Projected temperature determines whether cooling increases or whether an emergency trip is required.'
  );

  // Portrait Flowchart on Left: w=3.80, h=4.80
  if (fs.existsSync(DIAG_5_ALGO)) {
    s12.addShape('rect', {
      x: 0.90,
      y: 1.45,
      w: 3.80,
      h: 4.80,
      fill: { color: C.surface },
      line: { color: C.border, width: 1.0 }
    });
    s12.addImage({
      path: DIAG_5_ALGO,
      x: 1.00,
      y: 1.55,
      w: 3.60,
      h: 4.60,
      sizing: { type: 'contain', w: 3.60, h: 4.60 }
    });
  }

  // Right Side Explanation Panel: w=7.48, h=4.80
  s12.addShape('rect', {
    x: 4.95,
    y: 1.45,
    w: 7.48,
    h: 4.80,
    fill: { color: C.mintSurface },
    line: { color: C.greenBorder, width: 1.0 }
  });
  s12.addText('Algorithm Execution Stages', {
    x: 5.20,
    y: 1.62,
    w: 6.90,
    h: 0.26,
    fontFace: FONT,
    fontSize: 13.5,
    bold: true,
    color: C.greenDark,
    margin: 0
  });
  s12.addShape('line', { x: 5.20, y: 1.92, w: 2.00, h: 0, line: { color: C.green, width: 2 } });

  const stages = [
    {
      num: '1',
      title: 'Digital Acquisition & Bound Check',
      text: 'OneWire probes are polled at 1 Hz. CRC integrity is confirmed, and values outside [-20°C, 125°C] are rejected.'
    },
    {
      num: '2',
      title: 'Exponential Moving Average (EMA) Filter',
      text: 'Suppresses measurement quantization noise: Tf[k] = 0.20·Traw[k] + 0.80·Tf[k-1].'
    },
    {
      num: '3',
      title: '30-Sample Rolling Regression Slope (r)',
      text: 'A circular FIFO buffer tracks the last 30 filtered samples. The heating rate r (°C/s) is calculated via closed-form OLS.'
    },
    {
      num: '4',
      title: 'Forward Horizon Temperature Projection',
      text: 'Computes projected temperature Tp = Tf + 30·max(0, r). Negative slopes are clamped to 0 to prevent premature fan slowdown.'
    },
    {
      num: '5',
      title: 'Adaptive Fan PWM & Supervisory Evaluation',
      text: 'Fan duty cycle maps linearly between 45°C (20% PWM) and 65°C (100% PWM). If Tp > 75°C, emergency shutdown executes.'
    }
  ];

  stages.forEach((st, i) => {
    const y = 2.05 + i * 0.76;
    s12.addShape('rect', {
      x: 5.20,
      y: y + 0.02,
      w: 0.32,
      h: 0.28,
      fill: { color: C.mintBadge },
      line: { color: C.greenBorder, width: 1.0 }
    });
    s12.addText(st.num, {
      x: 5.20,
      y: y + 0.05,
      w: 0.32,
      h: 0.22,
      fontFace: FONT,
      fontSize: 11,
      bold: true,
      color: C.greenDark,
      align: 'center',
      margin: 0
    });
    s12.addText(st.title, {
      x: 5.65,
      y: y,
      w: 6.50,
      h: 0.24,
      fontFace: FONT,
      fontSize: 11.5,
      bold: true,
      color: C.text,
      margin: 0
    });
    s12.addText(st.text, {
      x: 5.65,
      y: y + 0.22,
      w: 6.50,
      h: 0.50,
      fontFace: FONT,
      fontSize: 9.5,
      color: C.textSec,
      lineSpacingMultiple: 1.15,
      margin: 0
    });
  });

  return s12;
}

// =============================================================
// SLIDE 13 — HARDWARE OPERATIONAL STATE FLOWCHART
// =============================================================
function buildSlide13(pres) {
  const s13 = createStandardSlide(
    pres,
    'Hardware Operational State Flowchart',
    'Finite state machine governing boot sequence, soft-start, thermal boost, trip latching, and recovery',
    13,
    21,
    'This flowchart illustrates the finite state machine running in firmware. The node starts in Standby Boot, checking ' +
    'sensors before asserting PS_ON to energize the main outputs. It transitions seamlessly into Normal Run or Thermal Boost ' +
    'based on temperature gradient, and locks into Fault Trip upon exceeding electrical or thermal safety thresholds.'
  );

  // Portrait Flowchart on Left: w=3.80, h=4.80
  if (fs.existsSync(DIAG_4_STATE)) {
    s13.addShape('rect', {
      x: 0.90,
      y: 1.45,
      w: 3.80,
      h: 4.80,
      fill: { color: C.surface },
      line: { color: C.border, width: 1.0 }
    });
    s13.addImage({
      path: DIAG_4_STATE,
      x: 1.00,
      y: 1.55,
      w: 3.60,
      h: 4.60,
      sizing: { type: 'contain', w: 3.60, h: 4.60 }
    });
  }

  // Right Side State Descriptions: w=7.48, h=4.80
  s13.addShape('rect', {
    x: 4.95,
    y: 1.45,
    w: 7.48,
    h: 4.80,
    fill: { color: C.surface },
    line: { color: C.border, width: 1.0 }
  });
  s13.addText('Finite State Machine States', {
    x: 5.20,
    y: 1.62,
    w: 6.90,
    h: 0.26,
    fontFace: FONT,
    fontSize: 13.5,
    bold: true,
    color: C.text,
    margin: 0
  });
  s13.addShape('line', { x: 5.20, y: 1.92, w: 2.00, h: 0, line: { color: C.green, width: 2 } });

  const states = [
    { state: 'STATE 0: STANDBY_BOOT', desc: 'Node powered from +5VSB. Initializes I2C, OneWire, and LittleFS. Main outputs disabled (PS_ON# HIGH).' },
    { state: 'STATE 1: SOFT_START', desc: 'Validates all bus voltages. Asserts PS_ON# LOW via 2N2222A. Checks 12V, 5V, 3.3V rail rise within 200ms.' },
    { state: 'STATE 2: NORMAL_RUN', desc: 'Nominal closed-loop monitoring. Fan runs at baseline idle (20% PWM). Telemetry streams to local LCD & cloud.' },
    { state: 'STATE 3: THERMAL_BOOST', desc: 'Triggered when projected temperature Tp > 50°C. Dynamically ramps fan PWM from 20% up to 100%.' },
    { state: 'STATE 4: FAULT_TRIP', desc: 'Triggered by core T > 75°C, overcurrent > 3.5A, or rail collapse. Releases PS_ON# (< 5ms) and locks alarm.' },
    { state: 'STATE 5: SAFE_RESET', desc: 'Enforces cooldown hysteresis (T < 50°C) before allowing operator or authorized remote re-energization.' }
  ];

  states.forEach((st, i) => {
    const y = 2.05 + i * 0.66;
    s13.addText(st.state, {
      x: 5.20,
      y: y,
      w: 6.90,
      h: 0.22,
      fontFace: FONT,
      fontSize: 11,
      bold: true,
      color: C.greenDark,
      margin: 0
    });
    s13.addText(st.desc, {
      x: 5.20,
      y: y + 0.20,
      w: 6.90,
      h: 0.42,
      fontFace: FONT,
      fontSize: 9.5,
      color: C.textSec,
      lineSpacingMultiple: 1.15,
      margin: 0
    });
  });

  return s13;
}

// =============================================================
// SLIDE 14 — COMBINED SUPERVISORY SYSTEM FLOWCHART
// =============================================================
function buildSlide14(pres) {
  const s14 = createStandardSlide(
    pres,
    'Combined Supervisory System Flowchart',
    'Dual-core FreeRTOS concurrency: safety-critical protective loop decoupled from network tasks',
    14,
    21,
    'This flowchart illustrates the multi-core software architecture. FreeRTOS Core 1 runs the safety-critical loop ' +
    'with zero network overhead, guaranteeing sub-millisecond trip decisions. Core 0 handles web serving and cloud ' +
    'synchronization in the background. Even during a complete Wi-Fi dropout, protective functions continue uninterrupted.'
  );

  // Portrait Flowchart on Left: w=3.80, h=4.80
  if (fs.existsSync(DIAG_6_SUP)) {
    s14.addShape('rect', {
      x: 0.90,
      y: 1.45,
      w: 3.80,
      h: 4.80,
      fill: { color: C.surface },
      line: { color: C.border, width: 1.0 }
    });
    s14.addImage({
      path: DIAG_6_SUP,
      x: 1.00,
      y: 1.55,
      w: 3.60,
      h: 4.60,
      sizing: { type: 'contain', w: 3.60, h: 4.60 }
    });
  }

  // Right Side Concurrency Breakdown: w=7.48, h=4.80
  s14.addShape('rect', {
    x: 4.95,
    y: 1.45,
    w: 7.48,
    h: 4.80,
    fill: { color: C.mintSurface },
    line: { color: C.greenBorder, width: 1.0 }
  });
  s14.addText('Dual-Core FreeRTOS Concurrency', {
    x: 5.20,
    y: 1.62,
    w: 6.90,
    h: 0.26,
    fontFace: FONT,
    fontSize: 13.5,
    bold: true,
    color: C.greenDark,
    margin: 0
  });
  s14.addShape('line', { x: 5.20, y: 1.92, w: 2.00, h: 0, line: { color: C.green, width: 2 } });

  const concNotes = [
    {
      core: 'CORE 1 — Safety-Critical Execution (Priority 24)',
      text: '• Dedicated to 1 Hz deterministic sensor acquisition and emergency decisions.\n' +
            '• Directly controls GPIO32 (PS_ON#) and GPIO19 (PWM Fan Driver).\n' +
            '• Zero dependency on Wi-Fi, TCP/IP stack, or external network sockets.'
    },
    {
      core: 'CORE 0 — User Interface & Networking (Priority 5)',
      text: '• Manages Wi-Fi Station connection and Soft-AP captive portal.\n' +
            '• LittleFS internal web server serves live browser diagnostics locally.\n' +
            '• Asynchronously syncs telemetry snapshots to Firebase Realtime Database.'
    },
    {
      core: 'Inter-Core Communication & Resilience',
      text: '• Thread-safe FreeRTOS Queues pass telemetry frames from Core 1 to Core 0.\n' +
            '• Wi-Fi reconnect timeouts never stall or delay Core 1 safety trips.\n' +
            '• Hardware watchdog timer resets system in the event of unexpected task lockup.'
    }
  ];

  concNotes.forEach((cn, i) => {
    const y = 2.05 + i * 1.30;
    s14.addText(cn.core, {
      x: 5.20,
      y: y,
      w: 6.90,
      h: 0.22,
      fontFace: FONT,
      fontSize: 11.5,
      bold: true,
      color: C.text,
      margin: 0
    });
    s14.addText(cn.text, {
      x: 5.20,
      y: y + 0.24,
      w: 6.90,
      h: 0.90,
      fontFace: FONT,
      fontSize: 9.5,
      color: C.textSec,
      lineSpacingMultiple: 1.18,
      margin: 0
    });
  });

  return s14;
}

// =============================================================
// SLIDE 15 — HARDWARE PROTOTYPE SETUP (PLACEHOLDER SLIDE)
// =============================================================
function buildSlide15(pres) {
  const s15 = createStandardSlide(
    pres,
    'Hardware Prototype Setup & Testbed',
    'Physical bench assembly, sensor probe mounting, and load bank interconnection',
    15,
    21,
    'This slide reserves space for the physical prototype assembly photograph. The bench arrangement incorporates ' +
    'the ATX power supply, the ESP32 breakout carrier, the digital temperature probe mounts, and the parallel test loads. ' +
    'Callouts highlight each physical component for clear evaluation.'
  );

  // Left Placeholder Box: w=7.60, h=4.75
  s15.addShape('rect', {
    x: 0.90,
    y: 1.45,
    w: 7.60,
    h: 4.75,
    fill: { color: C.surface },
    line: { color: C.border, width: 1.2 }
  });

  // Inner dashed photo frame
  s15.addShape('rect', {
    x: 1.20,
    y: 1.75,
    w: 7.00,
    h: 4.15,
    fill: { color: C.mintSurface },
    line: { color: C.greenBorder, width: 1.5, dashType: 'dash' }
  });

  s15.addText('[ PROTOTYPE BENCH PHOTOGRAPH PLACEHOLDER ]', {
    x: 1.40,
    y: 3.20,
    w: 6.60,
    h: 0.35,
    fontFace: FONT,
    fontSize: 14,
    bold: true,
    color: C.greenDark,
    align: 'center',
    margin: 0
  });

  s15.addText(
    'Insert high-resolution photograph of the wired prototype bench setup here\n(Showing ATX SMPS, ESP32 carrier, INA219 modules, probe attachments, and LED load bank)',
    {
      x: 1.40,
      y: 3.65,
      w: 6.60,
      h: 0.60,
      fontFace: FONT,
      fontSize: 10.5,
      color: C.muted,
      align: 'center',
      lineSpacingMultiple: 1.2,
      margin: 0
    }
  );

  // Right Side Subsystem Callouts: w=3.63, h=4.75
  s15.addShape('rect', {
    x: 8.80,
    y: 1.45,
    w: 3.63,
    h: 4.75,
    fill: { color: C.surface },
    line: { color: C.border, width: 1.2 }
  });
  s15.addText('Bench Subsystem Callouts', {
    x: 9.05,
    y: 1.65,
    w: 3.15,
    h: 0.28,
    fontFace: FONT,
    fontSize: 13,
    bold: true,
    color: C.greenDark,
    margin: 0
  });
  s15.addShape('line', { x: 9.05, y: 1.98, w: 1.80, h: 0, line: { color: C.green, width: 2 } });

  const benchItems = [
    { title: 'A. ATX SMPS Test Platform', desc: '450W power supply supplying continuous +5VSB and switched 12V/5V/3.3V rails.' },
    { title: 'B. ESP32 Microcontroller Node', desc: 'Breadboard/perfboard carrier hosting ESP32-WROOM-32D and decoupling passives.' },
    { title: 'C. INA219 Telemetry Array', desc: 'Three breakout boards connected via shared I2C bus with distinct hardware addresses.' },
    { title: 'D. DS18B20 Temperature Probes', desc: 'Probe 1 mounted to transformer core surface; Probe 2 measuring ambient inlet air.' },
    { title: 'E. Demonstration Load Array', desc: 'Parallel LED strip and USB buck converter drawing variable current on 12V rail.' },
    { title: 'F. 16x2 Character LCD Panel', desc: 'I2C display providing local operator visibility during offline test runs.' }
  ];

  benchItems.forEach((b, i) => {
    const y = 2.10 + i * 0.70;
    s15.addText(b.title, {
      x: 9.05,
      y: y,
      w: 3.15,
      h: 0.22,
      fontFace: FONT,
      fontSize: 10.5,
      bold: true,
      color: C.text,
      margin: 0
    });
    s15.addText(b.desc, {
      x: 9.05,
      y: y + 0.20,
      w: 3.15,
      h: 0.46,
      fontFace: FONT,
      fontSize: 9,
      color: C.textSec,
      lineSpacingMultiple: 1.15,
      margin: 0
    });
  });

  return s15;
}

// =============================================================
// SLIDE 16 — EXPERIMENTAL PROOF & VALIDATION WAVEFORMS (PLACEHOLDER SLIDE)
// =============================================================
function buildSlide16(pres) {
  const s16 = createStandardSlide(
    pres,
    'Experimental Proof & Validation Waveforms',
    'Measured laboratory evidence: oscilloscope shutdown capture and temperature suppression curves',
    16,
    21,
    'This slide provides placeholders for our experimental proof data. When bench testing is executed, ' +
    'oscilloscope captures of the sub-millisecond PS_ON# cutoff and time-domain temperature suppression plots ' +
    'will be inserted directly into these panels to substantiate performance claims.'
  );

  // Left Placeholder: Oscilloscope Capture (w=5.60, h=3.85)
  s16.addShape('rect', {
    x: 0.90,
    y: 1.45,
    w: 5.60,
    h: 3.85,
    fill: { color: C.surface },
    line: { color: C.border, width: 1.2 }
  });
  s16.addText('Oscilloscope Shutdown Timing Proof', {
    x: 1.15,
    y: 1.62,
    w: 5.10,
    h: 0.26,
    fontFace: FONT,
    fontSize: 12.5,
    bold: true,
    color: C.greenDark,
    margin: 0
  });

  s16.addShape('rect', {
    x: 1.15,
    y: 1.95,
    w: 5.10,
    h: 2.30,
    fill: { color: C.mintSurface },
    line: { color: C.greenBorder, width: 1.0, dashType: 'dash' }
  });
  s16.addText('[ OSCILLOSCOPE CAPTURE PLACEHOLDER ]', {
    x: 1.30,
    y: 2.75,
    w: 4.80,
    h: 0.32,
    fontFace: FONT,
    fontSize: 12.5,
    bold: true,
    color: C.greenDark,
    align: 'center',
    margin: 0
  });
  s16.addText('Insert scope trace showing GPIO32 trip transition, PS_ON# release, and 12V/5V/3.3V rail voltage decay curves.', {
    x: 1.30,
    y: 3.15,
    w: 4.80,
    h: 0.55,
    fontFace: FONT,
    fontSize: 9.5,
    color: C.muted,
    align: 'center',
    lineSpacingMultiple: 1.18,
    margin: 0
  });

  s16.addText('• Target Shutdown Metric: PS_ON# release latency < 5.0 ms upon fault trigger.\n• Rail Voltage Collapse: All switched rails drop < 0.4V within 150 ms.', {
    x: 1.15,
    y: 4.40,
    w: 5.10,
    h: 0.65,
    fontFace: FONT,
    fontSize: 9.5,
    color: C.textSec,
    lineSpacingMultiple: 1.18,
    margin: 0
  });

  // Right Placeholder: Temperature Response Curves (w=5.60, h=3.85)
  s16.addShape('rect', {
    x: 6.83,
    y: 1.45,
    w: 5.60,
    h: 3.85,
    fill: { color: C.surface },
    line: { color: C.border, width: 1.2 }
  });
  s16.addText('Thermal Suppression Response Plot', {
    x: 7.08,
    y: 1.62,
    w: 5.10,
    h: 0.26,
    fontFace: FONT,
    fontSize: 12.5,
    bold: true,
    color: C.greenDark,
    margin: 0
  });

  s16.addShape('rect', {
    x: 7.08,
    y: 1.95,
    w: 5.10,
    h: 2.30,
    fill: { color: C.mintSurface },
    line: { color: C.greenBorder, width: 1.0, dashType: 'dash' }
  });
  s16.addText('[ THERMAL RESPONSE PLOT PLACEHOLDER ]', {
    x: 7.23,
    y: 2.75,
    w: 4.80,
    h: 0.32,
    fontFace: FONT,
    fontSize: 12.5,
    bold: true,
    color: C.greenDark,
    align: 'center',
    margin: 0
  });
  s16.addText('Insert time-domain plot comparing baseline reactive cooling vs. predictive adaptive cooling under step load.', {
    x: 7.23,
    y: 3.15,
    w: 4.80,
    h: 0.55,
    fontFace: FONT,
    fontSize: 9.5,
    color: C.muted,
    align: 'center',
    lineSpacingMultiple: 1.18,
    margin: 0
  });

  s16.addText('• Advance Fan Activation: Anticipates thermal ramp 30 seconds ahead of static ceiling.\n• Temperature Attenuation: Suppresses peak core surface temperature rise under load.', {
    x: 7.08,
    y: 4.40,
    w: 5.10,
    h: 0.65,
    fontFace: FONT,
    fontSize: 9.5,
    color: C.textSec,
    lineSpacingMultiple: 1.18,
    margin: 0
  });

  // Bottom Qualification Note
  s16.addShape('rect', {
    x: 0.90,
    y: 5.50,
    w: 11.53,
    h: 0.55,
    fill: { color: C.mintSurface },
    line: { color: C.greenBorder, width: 1.0 }
  });
  s16.addText('Pre-Commissioning Status: This presentation specifies the complete measurement methodology and validation protocol. Empirical waveforms will be integrated upon completion of load testing.', {
    x: 1.15,
    y: 5.62,
    w: 11.00,
    h: 0.30,
    fontFace: FONT,
    fontSize: 10.5,
    italic: true,
    color: C.greenDark,
    margin: 0
  });

  return s16;
}

// =============================================================
// SLIDE 17 — TESTING MATRIX & PRE-COMMISSIONING VALIDATION PLAN
// =============================================================
function buildSlide17(pres) {
  const s17 = createStandardSlide(
    pres,
    'Testing Matrix & Validation Plan',
    'Systematic experimental verification protocol across five engineering test areas',
    17,
    21,
    'Our verification plan encompasses five distinct testing areas: sensor calibration accuracy, predictive thermal ' +
    'response under load steps, supervisory shutdown transition timing, network disconnect resilience, and transactional ' +
    'cloud alerting. Each test defines a specific method and evidence required for formal sign-off.'
  );

  const testRows = [
    [
      { text: 'Test Area', options: { fill: { color: C.tableHeader }, bold: true, color: C.text, fontSize: 11 } },
      { text: 'Testing Method & Stimulus', options: { fill: { color: C.tableHeader }, bold: true, color: C.text, fontSize: 11 } },
      { text: 'Pass / Fail Acceptance Criteria', options: { fill: { color: C.tableHeader }, bold: true, color: C.text, fontSize: 11 } },
      { text: 'Evidence to Record', options: { fill: { color: C.tableHeader }, bold: true, color: C.text, fontSize: 11 } }
    ],
    [
      { text: '1. Measurement Accuracy', options: { bold: true, color: C.greenDark } },
      { text: 'Compare DS18B20 and INA219 readings against calibrated bench multimeter.' },
      { text: 'Temp error < ±0.5°C; Voltage error < 1.0%; Current error < 2.0% across all rails.' },
      { text: 'Tabulated comparison points and calculated percentage deviations.' }
    ],
    [
      { text: '2. Predictive Cooling Response', options: { bold: true, color: C.greenDark } },
      { text: 'Apply step-load changes on the 12V rail; log temperature rise rate and PWM fan command.' },
      { text: 'Fan duty ramps up before surface temperature reaches 65°C; smooth hysteresis.' },
      { text: 'Time-domain temperature curves and PWM fan command percentage traces.' }
    ],
    [
      { text: '3. Supervisory Main Shutdown', options: { bold: true, color: C.greenDark } },
      { text: 'Inject intentional over-temperature (>75°C) or overcurrent condition to trigger trip.' },
      { text: 'PS_ON# released in < 5 ms; switched rails collapse < 0.4V in < 150 ms.' },
      { text: 'Oscilloscope capture of GPIO32, PS_ON#, and rail decay response.' }
    ],
    [
      { text: '4. Network Loss Resilience', options: { bold: true, color: C.greenDark } },
      { text: 'Sever Wi-Fi connection during active run under load; monitor Core 1 acquisition.' },
      { text: 'Core 1 protection and fan PWM continue running at 1 Hz with zero interruption.' },
      { text: 'Logic analyzer execution trace verifying deterministic FreeRTOS loop timing.' }
    ],
    [
      { text: '5. Alerts & Event Logging', options: { bold: true, color: C.greenDark } },
      { text: 'Trigger controlled threshold limit; verify Firebase sync and email notification.' },
      { text: 'Event stored in LittleFS NVS; Brevo email dispatched via Cloudflare Worker.' },
      { text: 'Time-stamped event log export and received email delivery confirmation.' }
    ]
  ];

  s17.addTable(testRows, {
    x: 0.90,
    y: 1.45,
    w: 11.53,
    colW: [2.20, 3.30, 3.10, 2.93],
    fontFace: FONT,
    fontSize: 9.5,
    border: { pt: 1, color: C.border },
    rowH: [0.38, 0.70, 0.70, 0.70, 0.70, 0.70]
  });

  return s17;
}

// =============================================================
// SLIDE 18 — PROJECT CONCLUSION & KEY TECHNICAL TAKEAWAYS
// =============================================================
function buildSlide18(pres) {
  const s18 = createStandardSlide(
    pres,
    'Project Conclusion & Key Technical Takeaways',
    'Summary of engineering contributions, autonomous edge protection, and demonstration outcomes',
    18,
    21,
    'In conclusion, this project demonstrates an integrated condition monitoring architecture for transformer thermal ' +
    'and electrical supervision. By coupling digital OneWire sensors and multi-rail I2C monitoring directly with an ESP32, ' +
    'we achieve predictive cooling and supervisory disconnect locally on bare metal. Standby power maintains monitoring even ' +
    'after a fault trip, delivering an autonomous, physics-grounded CBM platform.'
  );

  // Left 5 Major Takeaways: w=7.20, h=4.80
  s18.addShape('rect', {
    x: 0.90,
    y: 1.45,
    w: 7.20,
    h: 4.80,
    fill: { color: C.surface },
    line: { color: C.border, width: 1.2 }
  });
  s18.addText('Key Engineering Achievements', {
    x: 1.15,
    y: 1.65,
    w: 6.70,
    h: 0.28,
    fontFace: FONT,
    fontSize: 14,
    bold: true,
    color: C.greenDark,
    margin: 0
  });
  s18.addShape('line', { x: 1.15, y: 1.95, w: 2.20, h: 0, line: { color: C.green, width: 2 } });

  const takeaways = [
    { title: 'Unified Edge Telemetry', text: 'Consolidates multi-channel digital thermal sensing and 3-rail DC electrical monitoring onto a single ESP32 embedded bus.' },
    { title: 'Predictive Adaptive Cooling', text: 'Combines EMA filtering with a 30-sample rolling OLS regression slope to project temperature rise and adjust fan PWM ahead of thermal inertia.' },
    { title: 'Autonomous Local Protection', text: 'Protective actions and cooling loops execute deterministically on bare metal (Core 1), immune to external Wi-Fi or internet outages.' },
    { title: 'Uninterruptible Standby Visibility', text: 'Powered continuously from the +5VSB standby rail, maintaining LCD diagnostics, memory logs, and cloud telemetry post-trip.' },
    { title: 'Scalable Physics-Grounded Methodology', text: 'Validates non-intrusive CBM principles on an ATX SMPS testbed that map directly to utility-scale power distribution transformers.' }
  ];

  takeaways.forEach((t, i) => {
    const y = 2.10 + i * 0.80;
    s18.addText(`•  ${t.title}:`, {
      x: 1.15,
      y: y,
      w: 6.70,
      h: 0.22,
      fontFace: FONT,
      fontSize: 11,
      bold: true,
      color: C.text,
      margin: 0
    });
    s18.addText(t.text, {
      x: 1.40,
      y: y + 0.22,
      w: 6.45,
      h: 0.50,
      fontFace: FONT,
      fontSize: 9.5,
      color: C.textSec,
      lineSpacingMultiple: 1.15,
      margin: 0
    });
  });

  // Right Architectural Flow Recap: w=4.03, h=4.80
  s18.addShape('rect', {
    x: 8.40,
    y: 1.45,
    w: 4.03,
    h: 4.80,
    fill: { color: C.mintSurface },
    line: { color: C.greenBorder, width: 1.2 }
  });
  s18.addText('Operational Flow Recap', {
    x: 8.55,
    y: 1.65,
    w: 3.73,
    h: 0.28,
    fontFace: FONT,
    fontSize: 13.5,
    bold: true,
    color: C.greenDark,
    align: 'center',
    margin: 0
  });

  const flowSteps = [
    { title: 'SENSE', sub: 'DS18B20 Probes + 3× INA219 Shunts' },
    { title: 'DECIDE LOCALLY', sub: 'ESP32 Rolling OLS Slope & Trip Logic' },
    { title: 'RESPOND & PROTECT', sub: '25kHz PWM Fan Drive & PS_ON# Cutoff' },
    { title: 'SUPERVISE & REPORT', sub: '16x2 LCD, LittleFS & Firebase Sync' }
  ];

  flowSteps.forEach((fs, i) => {
    const y = 2.10 + i * 0.98;
    s18.addShape('rect', {
      x: 8.65,
      y: y,
      w: 3.53,
      h: 0.65,
      fill: { color: C.white },
      line: { color: C.greenBorder, width: 1.2 }
    });
    s18.addText(fs.title, {
      x: 8.75,
      y: y + 0.08,
      w: 3.33,
      h: 0.24,
      fontFace: FONT,
      fontSize: 11,
      bold: true,
      color: C.greenDark,
      align: 'center',
      margin: 0
    });
    s18.addText(fs.sub, {
      x: 8.75,
      y: y + 0.32,
      w: 3.33,
      h: 0.26,
      fontFace: FONT,
      fontSize: 9,
      color: C.textSec,
      align: 'center',
      margin: 0
    });

    if (i < 3) {
      s18.addShape('line', {
        x: 10.41,
        y: y + 0.65,
        w: 0,
        h: 0.33,
        line: { color: C.green, width: 2 }
      });
    }
  });

  return s18;
}

// =============================================================
// SLIDE 19 — FUTURE SCOPE & GRID SCALABILITY
// =============================================================
function buildSlide19(pres) {
  const s19 = createStandardSlide(
    pres,
    'Future Scope & Grid Scalability',
    'Strategic roadmap for expanding instrumentation, edge analytics, and utility-scale deployment',
    19,
    21,
    'Looking forward, this project establishes a foundational architecture that scales directly to utility-scale transformers. ' +
    'Future enhancements will integrate tachometer fan speed feedback, fiber-optic winding sensors, Rogowski AC coils, and on-device ' +
    'Arrhenius insulation loss-of-life calculations to deliver automated predictive maintenance advisories.'
  );

  const pillars = [
    {
      num: 'PILLAR 1',
      title: 'Advanced Instrumentation',
      bullets: [
        'Fan Tachometer Feedback: Interfacing 4-wire fan tachometer signals to detect bearing wear and convective airflow stall.',
        'Fiber-Optic Core Sensing: Interfacing GaAs optical probes directly on winding copper to calibrate internal thermal resistance.',
        'Ambient Telemetry: Incorporating solar irradiance and ambient wind speed inputs into predictive thermal expectations.'
      ]
    },
    {
      num: 'PILLAR 2',
      title: 'Utility Grid Adaptation',
      bullets: [
        'AC Power Telemetry: Replacing DC shunts with high-accuracy Rogowski coils or current transformers (CTs) for 3-phase AC.',
        'Dissolved Gas Analysis: Integrating edge gas-in-oil sensor inputs (H2, CO, C2H2) for comprehensive fault diagnosis.',
        'Industrial SCADA Protocols: Adding native Modbus-TCP and IEC 61850 protocol support for direct substation automation.'
      ]
    },
    {
      num: 'PILLAR 3',
      title: 'Predictive Edge Maintenance AI',
      bullets: [
        'IEEE C57.91 Arrhenius Life Wear: On-device tracking of insulation loss-of-life accumulation based on hot-spot integration.',
        'Adaptive Kalman Filtering: Implementing state estimation to dynamically adapt thermal model parameters to seasonal variations.',
        'Automated Maintenance Advisories: Generating explainable maintenance dispatch tickets before physical dielectric breakdown.'
      ]
    }
  ];

  pillars.forEach((p, i) => {
    const x = 0.90 + i * 3.94;
    s19.addShape('rect', {
      x: x,
      y: 1.45,
      w: 3.65,
      h: 4.75,
      fill: { color: C.surface },
      line: { color: C.border, width: 1.2 }
    });
    s19.addText(p.num, {
      x: x + 0.20,
      y: 1.65,
      w: 3.25,
      h: 0.22,
      fontFace: FONT,
      fontSize: 10,
      bold: true,
      color: C.greenDark,
      margin: 0
    });
    s19.addText(p.title, {
      x: x + 0.20,
      y: 1.88,
      w: 3.25,
      h: 0.30,
      fontFace: FONT,
      fontSize: 13.5,
      bold: true,
      color: C.text,
      margin: 0
    });
    s19.addShape('line', { x: x + 0.20, y: 2.22, w: 1.60, h: 0, line: { color: C.green, width: 2 } });

    p.bullets.forEach((b, j) => {
      const by = 2.40 + j * 1.20;
      s19.addText(`•  ${b}`, {
        x: x + 0.20,
        y: by,
        w: 3.25,
        h: 1.05,
        fontFace: FONT,
        fontSize: 9.5,
        color: C.textSec,
        lineSpacingMultiple: 1.15,
        margin: 0
      });
    });
  });

  return s19;
}

// =============================================================
// SLIDE 20 — ACADEMIC REFERENCES (IEEE CITATIONS)
// =============================================================
function buildSlide20(pres) {
  const s20 = createStandardSlide(
    pres,
    'References',
    'Peer-reviewed journal literature, international standards, and conference proceedings',
    20,
    21,
    'Here are our academic references from leading literature and IEEE standards. Our thermal modeling and predictive ' +
    'formulations are grounded in IEEE Standard C57.91 and IEC 60076-7, supported by recent research in IEEE Transactions ' +
    'on Industrial Electronics, Power Delivery, and Instrumentation and Measurement.'
  );

  const refs = [
    {
      num: '[1]',
      text: 'J. I. Aizpurua, S. D. J. McArthur, et al., "Adaptive power transformer lifetime predictions through machine learning and uncertainty modeling in nuclear power plants," IEEE Transactions on Industrial Electronics, vol. 66, no. 6, pp. 4726–4737, Jun. 2019.'
    },
    {
      num: '[2]',
      text: 'A. Doolgindachbaporn, G. Callender, P. L. Lewin, et al., "Data driven transformer thermal model for condition monitoring," IEEE Transactions on Power Delivery, vol. 37, no. 4, pp. 3133–3141, Aug. 2022.'
    },
    {
      num: '[3]',
      text: 'IEEE Guide for Loading Mineral-Oil-Immersed Transformers and Step-Voltage Regulators, IEEE Standard C57.91-2011 (Revision of IEEE Std C57.91-1995), IEEE Power and Energy Society, Mar. 2012.'
    },
    {
      num: '[4]',
      text: 'T. F. Rodrigues, D. S. Gazzana, P. F. Silva, and R. Q. Machado, "Evaluation of power transformer thermal performance and optical sensor positioning using CFD simulations," IEEE Transactions on Instrumentation and Measurement, vol. 72, pp. 1–11, 2023.'
    },
    {
      num: '[5]',
      text: 'Power Transformers — Part 7: Loading Guide for Mineral-Oil-Immersed Power Transformers, IEC Standard 60076-7:2018, International Electrotechnical Commission, Jan. 2018.'
    },
    {
      num: '[6]',
      text: 'G. Swift, T. S. Molinski, and W. Lehn, "A fundamental approach to transformer thermal modeling — Part I: Theory and equivalent circuit," IEEE Transactions on Power Delivery, vol. 16, no. 2, pp. 171–175, Apr. 2001.'
    }
  ];

  refs.forEach((r, i) => {
    const y = 1.48 + i * 0.78;

    // Point number indicator (Green Bold)
    s20.addText(r.num, {
      x: 0.90,
      y: y,
      w: 0.45,
      h: 0.35,
      fontFace: FONT,
      fontSize: 11,
      bold: true,
      color: C.greenDark,
      margin: 0
    });

    // Reference point text
    s20.addText(r.text, {
      x: 1.45,
      y: y - 0.02,
      w: 10.98,
      h: 0.65,
      fontFace: FONT,
      fontSize: 10,
      color: C.text,
      lineSpacingMultiple: 1.18,
      margin: 0
    });

    // Subtle divider line between reference points
    if (i < refs.length - 1) {
      s20.addShape('line', {
        x: 0.90,
        y: y + 0.68,
        w: 11.53,
        h: 0,
        line: { color: 'E2E8F0', width: 0.8 }
      });
    }
  });

  return s20;
}

// =============================================================
// SLIDE 21 — SEPARATE THANK YOU & DISCUSSION SLIDE (Clean Light)
// =============================================================
function buildSlide21(pres) {
  const s21 = pres.addSlide();
  s21.background = { color: C.white };

  // Top Institution Bar
  s21.addShape('rect', {
    x: 0.90,
    y: 0.60,
    w: 11.53,
    h: 0.75,
    fill: { color: C.mintSurface },
    line: { color: C.greenBorder, width: 1.0 }
  });

  s21.addText('RAJALAKSHMI INSTITUTE OF TECHNOLOGY, CHENNAI', {
    x: 1.15,
    y: 0.68,
    w: 11.03,
    h: 0.28,
    fontFace: FONT,
    fontSize: 13,
    bold: true,
    color: C.greenDark,
    align: 'center',
    margin: 0
  });

  s21.addText('Department of Electronics and Communication Engineering', {
    x: 1.15,
    y: 0.98,
    w: 11.03,
    h: 0.25,
    fontFace: FONT,
    fontSize: 10,
    color: C.muted,
    align: 'center',
    margin: 0
  });

  // Thank You Large Clean Banner
  s21.addText('Thank You', {
    x: 0.90,
    y: 1.70,
    w: 11.53,
    h: 1.00,
    fontFace: FONT,
    fontSize: 48,
    bold: true,
    color: C.text,
    align: 'center',
    margin: 0
  });

  // Green Accent Divider
  s21.addShape('line', {
    x: 5.16,
    y: 2.85,
    w: 3.00,
    h: 0,
    line: { color: C.green, width: 2.5 }
  });

  // Questions and Discussion
  s21.addText('Questions & Technical Discussion', {
    x: 0.90,
    y: 3.05,
    w: 11.53,
    h: 0.38,
    fontFace: FONT,
    fontSize: 18,
    bold: true,
    color: C.greenDark,
    align: 'center',
    margin: 0
  });

  // Project Summary Card
  s21.addShape('rect', {
    x: 1.40,
    y: 3.75,
    w: 10.53,
    h: 2.45,
    fill: { color: C.surface },
    line: { color: C.border, width: 1.2 }
  });

  s21.addText('IoT-Based Transformer Condition Monitoring with Predictive Adaptive Thermal Management Using ESP32', {
    x: 1.60,
    y: 3.95,
    w: 10.13,
    h: 0.35,
    fontFace: FONT,
    fontSize: 13,
    bold: true,
    color: C.text,
    align: 'center',
    margin: 0
  });

  s21.addText('Demonstration Platform Executed on an ATX Switch-Mode Power Supply (SMPS)', {
    x: 1.60,
    y: 4.32,
    w: 10.13,
    h: 0.26,
    fontFace: FONT,
    fontSize: 11,
    color: C.greenDark,
    align: 'center',
    margin: 0
  });

  s21.addShape('line', {
    x: 3.50,
    y: 4.70,
    w: 6.33,
    h: 0,
    line: { color: C.border, width: 1.0 }
  });

  s21.addText('Project Team: Selvakumari S  ·  Shreya S  ·  Susmitha G  (Dept. of ECE)\nProject Mentor: Mrs. V. Subashini (Assistant Professor, Dept. of ECE)', {
    x: 1.60,
    y: 4.90,
    w: 10.13,
    h: 0.85,
    fontFace: FONT,
    fontSize: 11,
    color: C.textSec,
    align: 'center',
    lineSpacingMultiple: 1.35,
    margin: 0
  });

  s21.addNotes(
    'Thank you for your time and attention. We now welcome questions, feedback, and technical discussion ' +
    'on our embedded condition monitoring architecture and predictive thermal management methodology.'
  );

  return s21;
}

// -------------------------------------------------------------
// MAIN GENERATION FUNCTION
// -------------------------------------------------------------
function generatePresentation(outputPath) {
  const pres = new pptxgen();
  pres.defineLayout({ name: 'CUSTOM_16_9', width: 13.333, height: 7.5 });
  pres.layout = 'CUSTOM_16_9';
  pres.author = 'Selvakumari S, Shreya S, Susmitha G — Dept. of ECE, Rajalakshmi Institute of Technology';
  pres.title = 'IoT-Based Transformer Condition Monitoring with Predictive Adaptive Thermal Management Using ESP32';
  pres.subject = 'Executed using an ATX SMPS Demonstration Platform';

  console.log('Building 21 slides in Clean Light Academic Green/Slate/White theme...');
  buildSlide1(pres);
  buildSlide2(pres);
  buildSlide3(pres);
  buildSlide4(pres);
  buildSlide5(pres);
  buildSlide6(pres);
  buildSlide7(pres);
  buildSlide8(pres);
  buildSlide9(pres);
  buildSlide10(pres);
  buildSlide11(pres);
  buildSlide12(pres);
  buildSlide13(pres);
  buildSlide14(pres);
  buildSlide15(pres);
  buildSlide16(pres);
  buildSlide17(pres);
  buildSlide18(pres);
  buildSlide19(pres);
  buildSlide20(pres);
  buildSlide21(pres);

  return pres.writeFile({ fileName: outputPath });
}

module.exports = { generatePresentation };

if (require.main === module) {
  const outputPath = path.join(__dirname, 'Transformer_CBM_Presentation.pptx');
  generatePresentation(outputPath).then(() => {
    console.log(`Presentation successfully created at: ${outputPath}`);
  }).catch(err => {
    console.error('Error generating presentation:', err);
    process.exit(1);
  });
}
