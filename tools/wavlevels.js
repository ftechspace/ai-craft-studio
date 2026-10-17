// Numeric "ears" for audio: peak / RMS per window and onsets of a PCM or float WAV (any rate, any channels).
//   node tools/wavlevels.js file.wav                 summary: format, length, peak dBFS, RMS dBFS
//   node tools/wavlevels.js file.wav 0.6             + one line per 0.6 s window (peak/RMS dBFS and a bar)
//   node tools/wavlevels.js file.wav 0.6 10 20       … only windows between 10 s and 20 s
//   node tools/wavlevels.js file.wav onsets [dB]     times where the 10 ms RMS jumps ≥ dB (default 12) above the last 100 ms
// Integrated LUFS / true peak come from SoundCraft's bounce result, not from here.
const fs = require("fs");
const [file, a1, a2, a3] = process.argv.slice(2);
if (!file) { console.error("usage: node tools/wavlevels.js file.wav [window_s [from to] | onsets [dB]]"); process.exit(1); }
const b = fs.readFileSync(file);
if (b.toString("ascii", 0, 4) !== "RIFF" && b.toString("ascii", 0, 4) !== "RF64") throw new Error("not a WAV file");
let fmt, data, p = 12;
while (p + 8 <= b.length) {
  const id = b.toString("ascii", p, p + 4); let len = b.readUInt32LE(p + 4);
  if (id === "data" && (len === 0xffffffff || p + 8 + len > b.length)) len = b.length - p - 8;
  if (id === "fmt ") fmt = { tag: b.readUInt16LE(p + 8) === 0xfffe && len >= 40 ? b.readUInt16LE(p + 32) : b.readUInt16LE(p + 8), ch: b.readUInt16LE(p + 10), sr: b.readUInt32LE(p + 12), bits: b.readUInt16LE(p + 22) };
  if (id === "data") data = { off: p + 8, len };
  p += 8 + len + (len & 1);
}
if (!fmt || !data) throw new Error("no fmt/data chunk");
const bps = fmt.bits / 8, frames = Math.floor(data.len / (bps * fmt.ch));
const sample = o => fmt.tag === 3 ? (bps === 8 ? b.readDoubleLE(o) : b.readFloatLE(o))
  : bps === 2 ? b.readInt16LE(o) / 32768 : bps === 3 ? b.readIntLE(o, 3) / 8388608 : bps === 4 ? b.readInt32LE(o) / 2147483648 : (b[o] - 128) / 128;
const db = x => (x > 0 ? 20 * Math.log10(x) : -Infinity).toFixed(1).padStart(6);
// Per-frame max |sample| across channels.
const mono = new Float32Array(frames);
for (let i = 0; i < frames; i++) {
  let m = 0;
  for (let c = 0; c < fmt.ch; c++) m = Math.max(m, Math.abs(sample(data.off + (i * fmt.ch + c) * bps)));
  mono[i] = m;
}
const stats = (s, e) => { let pk = 0, sq = 0; for (let i = s; i < e; i++) { pk = Math.max(pk, mono[i]); sq += mono[i] * mono[i]; } return [pk, Math.sqrt(sq / Math.max(1, e - s))]; };
const [pk, rms] = stats(0, frames);
console.log(`${file}: ${fmt.sr} Hz, ${fmt.ch} ch, ${fmt.bits}-bit ${fmt.tag === 3 ? "float" : "PCM"}, ${(frames / fmt.sr).toFixed(3)} s, peak ${db(pk).trim()} dBFS, RMS ${db(rms).trim()} dBFS`);
if (a1 === "onsets") {
  const thr = Number(a2 || 12), w = Math.round(fmt.sr / 100), hist = [];
  let last = -1;
  for (let s = 0; s + w <= frames; s += w) {
    const r = stats(s, s + w)[1], prev = hist.length ? Math.max(...hist) : 0;
    if (r > 0.001 && 20 * Math.log10(r / Math.max(prev, 1e-6)) >= thr && s / fmt.sr - last > 0.1) { console.log(`onset ${(s / fmt.sr).toFixed(3)} s  ${db(r).trim()} dBFS RMS`); last = s / fmt.sr; }
    hist.push(r); if (hist.length > 10) hist.shift();
  }
} else if (a1) {
  const win = Number(a1), from = Number(a2 || 0), to = Number(a3 || frames / fmt.sr);
  for (let t = from; t < to - 1e-9; t += win) {
    const s = Math.round(t * fmt.sr), e = Math.min(frames, Math.round((t + win) * fmt.sr));
    if (s >= e) break;
    const [wp, wr] = stats(s, e);
    const bar = "#".repeat(Math.max(0, Math.round((60 + 20 * Math.log10(Math.max(wr, 1e-6))) / 2)));
    console.log(`${t.toFixed(2).padStart(7)} s  peak ${db(wp)}  rms ${db(wr)}  ${bar}`);
  }
}
