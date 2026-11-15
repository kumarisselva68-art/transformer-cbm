import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const srcDir = path.join(__dirname, '../public/assets/diagrams');
const darkDir = path.join(srcDir, 'dark');
const lightDir = path.join(srcDir, 'light');

if (!fs.existsSync(darkDir)) fs.mkdirSync(darkDir, { recursive: true });
if (!fs.existsSync(lightDir)) fs.mkdirSync(lightDir, { recursive: true });

const files = [
  '01_hardware_circuit_block_diagram.svg',
  '02_software_cloud_architecture_block_diagram.svg',
  '03_combined_system_architecture_block_diagram.svg',
  '04_hardware_operational_state_flowchart.svg',
  '05_predictive_thermal_algorithm_flowchart.svg',
  '06_combined_supervisory_system_flowchart.svg',
  '07_master_hardware_circuit_schematic.svg'
];

files.forEach(file => {
  const filePath = path.join(srcDir, file);
  if (!fs.existsSync(filePath)) return;

  const raw = fs.readFileSync(filePath, 'utf8');

  // Light version
  let light = raw;
  fs.writeFileSync(path.join(lightDir, file), light, 'utf8');

  // Dark version
  let dark = raw;
  dark = dark.replace(/fill="#ffffff"/g, 'fill="#09090b"');
  dark = dark.replace(/fill="#f8fafc"/g, 'fill="#121215"');
  dark = dark.replace(/fill="#f1f5f9"/g, 'fill="#18181f"');
  dark = dark.replace(/fill="#e2e8f0"/g, 'fill="#22222a"');

  dark = dark.replace(/fill="#0f172a"/g, 'fill="#f4f4f5"');
  dark = dark.replace(/fill="#1e293b"/g, 'fill="#e4e4e7"');
  dark = dark.replace(/fill="#334155"/g, 'fill="#d4d4d8"');
  dark = dark.replace(/fill="#64748b"/g, 'fill="#a1a1aa"');

  dark = dark.replace(/stroke="#1e293b"/g, 'stroke="#f59e0b"');
  dark = dark.replace(/stroke="#0f172a"/g, 'stroke="#f59e0b"');
  dark = dark.replace(/stroke="#334155"/g, 'stroke="#71717a"');
  dark = dark.replace(/stroke="#cbd5e1"/g, 'stroke="#27272a"');
  dark = dark.replace(/stroke="#e2e8f0"/g, 'stroke="#27272a"');

  dark = dark.replace(/fill="#1e293b"/g, 'fill="#f59e0b"');

  fs.writeFileSync(path.join(darkDir, file), dark, 'utf8');
});

console.log('Generated dark and light mode SVG diagrams successfully.');
