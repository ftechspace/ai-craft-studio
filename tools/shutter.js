// Synthesises a camera-shutter click (original, no samples): node tools/shutter.js [out.wav]
// Open click + mirror clack + close click with a low thump; 48 kHz stereo 16-bit, peak −3 dBFS.
const fs = require("fs");
const out = process.argv[2] || require("path").join(__dirname, "..", "sfx", "shutter.wav");
const SR = 48000, N = Math.round(0.26 * SR);
let seed = 12345;
const noise = () => ((seed = (seed * 1103515245 + 12345) & 0x7fffffff) / 0x3fffffff) - 1;
const x = new Float64Array(N);
const burst = (at, ms, decayMs, amp, lowpass = 0) => {
  let lp = 0;
  for (let i = 0; i < (ms / 1000) * SR; i++) {
    const t = i / SR, n = noise();
    lp += (n - lp) * (lowpass ? lowpass : 1);
    const k = Math.round(at * SR) + i;
    if (k < N) x[k] += amp * lp * Math.exp(-t / (decayMs / 1000));
  }
};
const tone = (at, hz, decayMs, amp) => {
  for (let i = 0; i < 0.06 * SR; i++) {
    const t = i / SR, k = Math.round(at * SR) + i;
    if (k < N) x[k] += amp * Math.sin(2 * Math.PI * hz * t) * Math.exp(-t / (decayMs / 1000));
  }
};
burst(0, 6, 0.9, 1.0);            // shutter open: sharp tick
tone(0, 3200, 4, 0.35);
burst(0.042, 22, 4, 0.7, 0.35);   // mirror clack: duller, longer
tone(0.042, 420, 10, 0.25);
burst(0.105, 5, 0.8, 0.85);       // shutter close
tone(0.105, 180, 16, 0.45);       // body thump
const peak = Math.max(...x.map(Math.abs)), g = 0.708 / peak; // −3 dBFS
const data = Buffer.alloc(N * 4);
for (let i = 0; i < N; i++) {
  const v = Math.max(-32768, Math.min(32767, Math.round(x[i] * g * 32767)));
  data.writeInt16LE(v, i * 4);
  data.writeInt16LE(v, i * 4 + 2);
}
const h = Buffer.alloc(44);
h.write("RIFF", 0); h.writeUInt32LE(36 + data.length, 4); h.write("WAVE", 8);
h.write("fmt ", 12); h.writeUInt32LE(16, 16); h.writeUInt16LE(1, 20); h.writeUInt16LE(2, 22);
h.writeUInt32LE(SR, 24); h.writeUInt32LE(SR * 4, 28); h.writeUInt16LE(4, 32); h.writeUInt16LE(16, 34);
h.write("data", 36); h.writeUInt32LE(data.length, 40);
fs.mkdirSync(require("path").dirname(out), { recursive: true });
fs.writeFileSync(out, Buffer.concat([h, data]));
console.log(out, (N / SR).toFixed(2) + " s");
