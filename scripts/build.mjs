import fsimport fs from 'node:fs';
import path from 'node:path';

const base = 'node_modules/@mediapipe/tasks-vision';
const out = 'dist';
const vendor = path.join(out, 'vendor');
fs.mkdirSync(vendor, { recursive: true });
if (!fs.existsSync(base)) throw new Error('MediaPipe ontbreekt: voer npm install uit.');

const files = fs.readdirSync(base);
console.log('MediaPipe bestanden:', files.join(', '));

let html = fs.readFileSync('index.html', 'utf8');
const js = path.join(base, 'vision_bundle.js');
const mjs = path.join(base, 'vision_bundle.mjs');
if (fs.existsSync(js)) {
  fs.copyFileSync(js, path.join(vendor, 'vision_bundle.js'));
} else if (fs.existsSync(mjs)) {
  fs.copyFileSync(mjs, path.join(vendor, 'vision_bundle.mjs'));
  fs.writeFileSync(path.join(vendor, 'vision_bundle.js'),
    "import * as mp from './vision_bundle.mjs'; window.vision = mp;\n");
  const old = "const tag=document.createElement('script');tag.src=base+'vision_bundle.js';";
  const replacement = "const tag=document.createElement('script');tag.type='module';tag.src=base+'vision_bundle.js';";
  if (!html.includes(old)) throw new Error('Kan de MediaPipe scriptloader in index.html niet vinden.');
  html = html.replace(old, replacement);
} else {
  throw new Error('Geen browserbundle gevonden. Beschikbaar: ' + files.join(', '));
}

const wasm = path.join(base, 'wasm');
if (!fs.existsSync(wasm)) throw new Error('MediaPipe wasm-map ontbreekt.');
fs.cpSync(wasm, path.join(vendor, 'wasm'), { recursive: true });

const model = 'vendor/pose_landmarker_lite.task';
if (!fs.existsSync(model)) throw new Error('Posemodel ontbreekt: ' + model);
fs.copyFileSync(model, path.join(vendor, 'pose_landmarker_lite.task'));
fs.writeFileSync(path.join(out, 'index.html'), html);
fs.writeFileSync(path.join(out, '.nojekyll'), 'GitHub Pages static files\n');
console.log('Website gebouwd in dist/.');
