// Build an edit plan:  node tools/cut.js plan.json                 live, in the running app (port 9876)
//                      node tools/cut.js plan.json --headless out.fcproj   hidden session, saved to out.fcproj
// The plan format is documented in editor-kb/filmcraft-operations.md ("Plan format").
// Writes <plan>.built.json (clip ids, starts, mid-shot times) for checking with contact.exe.
const fs = require("fs");
const { connect, connectHeadless, TPS } = require("./fc");

const planPath = process.argv[2];
const hi = process.argv.indexOf("--headless");
const headlessOut = hi > 0 ? process.argv[hi + 1] : null;
if (!planPath || (hi > 0 && !headlessOut)) { console.error("usage: node tools/cut.js plan.json [--headless out.fcproj]"); process.exit(2); }
const P = JSON.parse(fs.readFileSync(planPath, "utf8"));
const fps = P.sequence.fps || 29.97;
// exact rate: 29.97 → 30000/1001, 23.976 → 24000/1001, 59.94 → 60000/1001
const ntsc = Math.abs(fps - Math.round(fps)) > 0.001;
const [num, den] = ntsc ? [Math.round(fps * 1.001) * 1000, 1001] : [fps, 1];
const frames = s => Math.max(1, Math.round(s * num / den));
const ticks = f => Math.round(f * TPS * den / num);
const pause = ms => new Promise(r => setTimeout(r, ms));

(async () => {
  const fc = headlessOut ? await connectHeadless() : await connect();
  const live = !fc.headless;
  const soft = (c, p) => fc.cmd(c, p).catch(e => console.log("warning:", e.message));
  if (P.newProject && live) await fc.cmd("file.newProject", { name: P.newProject });

  // media: reuse imported items (by file name), import the rest; note every item's length
  const dur = {}, byName = {};
  const scan = async () => (function walk(n) { if (n.item) { byName[n.name] = n.item; dur[n.item] = n.duration; } (n.children || []).forEach(walk); })((await fc.cmd("project.inspect")).root);
  await scan();
  const sfxPaths = Object.fromEntries(P.shots.flatMap((s, i) => (s.sfx ? [[`__sfx${i}`, s.sfx.path]] : [])));
  const media = { ...P.media, ...(P.music ? { __music: P.music.path } : {}), ...sfxPaths };
  const item = {};
  const missing = Object.keys(media).filter(k => !(item[k] = byName[media[k].split(/[\\/]/).pop()]));
  if (missing.length) {
    const r = await fc.cmd("file.import", { paths: missing.map(k => media[k]) });
    if (r.errors?.length) console.log("import errors:", JSON.stringify(r.errors));
    missing.forEach((k, i) => (item[k] = r.items[i]));
    await scan();
  }

  const S = P.sequence, W = S.width || 1920, H = S.height || 1080;
  const maxPanels = Math.max(0, ...P.shots.map(s => s.panels?.length || 0));
  await fc.cmd("file.newSequence", { name: S.name, width: W, height: H, fps, video: Math.max(3, maxPanels + 3), audio: 3 });

  // Live, the user may click another sequence tab mid-build: commands that create things would land in the wrong
  // sequence, and edits on our clips would fail. Re-select our sequence before creating, and retry once on failure.
  let seqItem = 0;
  (function walk(n) { if (n.type === "Sequence" && n.name === S.name) seqItem = Math.max(seqItem, n.item); (n.children || []).forEach(walk); })((await fc.cmd("project.inspect")).root);
  if (live && seqItem) {
    const raw = fc.cmd;
    const creates = /^(timeline\.place|graphics\.(newText|newShape|template\.apply)|playhead\.set|effects\.apply)$/;
    fc.cmd = async (c, p) => {
      if (creates.test(c)) await raw("sequence.open", { item: seqItem });
      try { return await raw(c, p); } catch (e) {
        if (!/no such track item|not available right now|no sequence/i.test(e.message)) throw e;
        await raw("sequence.open", { item: seqItem });
        return raw(c, p);
      }
    };
  }

  // picture
  let t = 0;
  const built = [];
  for (const [i, s] of P.shots.entries()) {
    const speed = s.freeze ? 100 : s.speed || 100;
    let f = frames(s.len);
    while ((f * speed) % 100) f++; // whole source frames at this speed
    const srcDur = ticks(f * speed / 100);
    const id = item[s.m];
    if (!id) throw new Error(`shot ${i}: unknown media key "${s.m}"`);
    // place doesn't stop at the end of the media: keep the range inside it
    const srcIn = Math.max(0, Math.min(Math.round(s.at * TPS - (s.freeze ? 0 : srcDur / 2)), (dur[id] || Infinity) - srcDur));
    const r = await fc.cmd("timeline.place", { item: id, track: "V1", time: t, sourceIn: srcIn, duration: srcDur, audio: false });
    const clip = r.clips[0];
    if (speed !== 100) await fc.cmd("clip.speedDuration", { clips: [clip], speed, ripple: true });
    if (s.freeze) await fc.cmd("clip.frameHoldOptions", { clips: [clip], enabled: true, holdOn: "in" });
    if (live) { await fc.cmd("playhead.set", { time: t }); await pause(120); }
    built.push({ shot: i, clip, item: id, start: t, frames: f, srcIn, mid: +((t + ticks(f) / 2) / TPS).toFixed(3) });
    t += ticks(f);
  }
  console.log(`placed ${built.length} shots, ${(t / TPS).toFixed(2)} s (${Math.round(t / TPS * num / den)} frames)`);

  // split screens: the shot is panel 0; each extra panel goes on the next video track; every panel keeps the
  // centre 1/n of its picture and sits in its column
  for (const [i, s] of P.shots.entries()) {
    if (!s.panels?.length) continue;
    const b = built[i], n = 1 + s.panels.length, speed = s.speed || 100, srcDur = ticks(b.frames * speed / 100);
    b.panels = [];
    for (const [j, pn] of s.panels.entries()) {
      const id = item[pn.m];
      if (!id) throw new Error(`shot ${i} panel ${j + 1}: unknown media key "${pn.m}"`);
      const srcIn = Math.max(0, Math.min(Math.round(pn.at * TPS - srcDur / 2), (dur[id] || Infinity) - srcDur));
      const c = (await fc.cmd("timeline.place", { item: id, track: `V${j + 2}`, time: b.start, sourceIn: srcIn, duration: srcDur, audio: false })).clips[0];
      if (speed !== 100) await fc.cmd("clip.speedDuration", { clips: [c], speed, ripple: false });
      b.panels.push(c);
    }
    const crop = (100 - 100 / n) / 2;
    for (const [k, c] of [b.clip, ...b.panels].entries()) {
      await soft("effects.apply", { clips: [c], effect: "crop" });
      await soft("effects.setParam", { clip: c, effect: "crop", param: "left", value: crop });
      await soft("effects.setParam", { clip: c, effect: "crop", param: "right", value: crop });
      await soft("effects.setParam", { clip: c, effect: "motion", param: "position", value: [((k + 0.5) * W) / n, H / 2] });
    }
  }

  // push-ins: Motion scale keyframed from → to across the shot
  for (const [i, s] of P.shots.entries()) {
    if (!s.push) continue;
    const b = built[i], [from, to] = s.push, end = b.start + ticks(b.frames - 1);
    await soft("effects.addKeyframe", { clip: b.clip, effect: "motion", param: "scale", time: b.start });
    await soft("effects.setParam", { clip: b.clip, effect: "motion", param: "scale", value: from, time: b.start });
    await soft("effects.setParam", { clip: b.clip, effect: "motion", param: "scale", value: to, time: end });
  }

  // transitions ("frames" overrides the default length, e.g. 3 for a camera-flash dip to white)
  for (const [i, s] of P.shots.entries()) {
    const b = built[i];
    const def = s.in === "fade" ? Math.min(frames(1.0), b.frames) : Math.max(2, Math.min(frames(0.7), Math.floor(b.frames / 3)) * 2);
    if (s.in === "fade") await soft("sequence.applyVideoTransition", { clip: b.clip, effect: "dip_to_black", frames: s.frames || def, edge: "in" });
    else if (s.in && s.in !== "cut") await soft("sequence.applyVideoTransition", { clip: b.clip, effect: s.in, frames: s.frames || def, edge: "in" });
    if (s.out === "fade") await soft("sequence.applyVideoTransition", { clip: b.clip, effect: "dip_to_black", frames: s.outFrames || Math.min(frames(1.5), b.frames), edge: "out" });
  }

  // camera sound: each shot's own sound from its first source frame, at real time (never pitched)
  const camera = [];
  if (P.sound === "camera") {
    for (const b of built) {
      const len = Math.min(ticks(b.frames), (dur[b.item] || Infinity) - b.srcIn);
      const r = await fc.cmd("timeline.place", { item: b.item, track: "A1", time: b.start, sourceIn: b.srcIn, duration: len }).catch(e => (console.log("no sound:", e.message), null));
      b.audio = r?.clips[0];
      if (b.audio) camera.push(b.audio);
    }
    for (const a of camera.slice(1)) await soft("sequence.applyAudioTransition", { clip: a, effect: "constant_power", frames: 6 });
    if (camera.length) {
      await soft("sequence.applyAudioTransition", { clip: camera[0], effect: "constant_power", frames: frames(1.0), edge: "in" });
      await soft("sequence.applyAudioTransition", { clip: camera.at(-1), effect: "constant_power", frames: frames(1.5), edge: "out" });
      if (P.soundDb) await soft("clip.audioGain", { clips: camera, mode: "set", db: P.soundDb });
    }
  }

  // sound effects on A3, e.g. a shutter click on a freeze: {"path", "offset" (s from the shot start, may be < 0), "db"}
  for (const [i, s] of P.shots.entries()) {
    if (!s.sfx) continue;
    const at = Math.max(0, built[i].start + ticks(frames(Math.abs(s.sfx.offset || 0))) * Math.sign(s.sfx.offset || 0));
    const r = await soft("timeline.place", { item: item[`__sfx${i}`], track: "A3", time: at });
    if (r && s.sfx.db) await soft("clip.audioGain", { clips: [r.clips[0]], mode: "set", db: s.sfx.db });
  }

  // music: full track on A2, remixed to the film's length at beat boundaries; else cut to length
  if (P.music) {
    const M = P.music, mi = item.__music, mdur = dur[mi];
    let mc = (await fc.cmd("timeline.place", { item: mi, track: "A2", time: 0, duration: mdur })).clips[0];
    if (mdur !== t) {
      const ok = await fc.cmd("clip.remix", { clip: mc, duration: t }).then(() => true, e => (console.log("music not remixed:", e.message), false));
      if (!ok && mdur > t) {
        await fc.cmd("edit.undo");
        mc = (await fc.cmd("timeline.place", { item: mi, track: "A2", time: 0, duration: t })).clips[0];
      }
    }
    if (M.db) await soft("clip.audioGain", { clips: [mc], mode: "set", db: M.db });
    await soft("sequence.applyAudioTransition", { clip: mc, effect: "constant_power", frames: frames(M.fadeIn ?? 0.5), edge: "in" });
    await soft("sequence.applyAudioTransition", { clip: mc, effect: "constant_power", frames: frames(M.fadeOut ?? 2), edge: "out" });
    await soft("essentialSound.setType", { clips: [mc], type: "music" });
    if (camera.length && M.duck !== false) {
      await soft("essentialSound.setType", { clips: camera, type: "dialogue" });
      await soft("essentialSound.generateDucking", { clips: [mc] });
    }
  }

  // grade: the plan's look on every shot, with per-shot corrections merged on top
  if (P.grade || P.shots.some(s => s.grade)) {
    await fc.cmd("effects.apply", { clips: built.flatMap(b => [b.clip, ...(b.panels || [])]), effect: "lumetri" });
    for (const [i, b] of built.entries())
      for (const c of [b.clip, ...(b.panels || [])])
        for (const [param, value] of Object.entries({ ...(P.grade || {}), ...(P.shots[i].grade || {}) }))
          await soft("effects.setParam", { clip: c, effect: "lumetri", param, value });
  }

  // letterbox: two black bars over the whole film, above every picture track (titles go above them)
  if (P.letterbox) {
    const bar = Math.round((H - W / P.letterbox) / 2);
    await fc.cmd("playhead.set", { time: 0 });
    const a = await fc.cmd("graphics.newShape", { shape: "rectangle", position: [W / 2, bar / 2], size: [W, bar], seconds: t / TPS });
    await fc.cmd("graphics.newShape", { shape: "rectangle", position: [W / 2, H - bar / 2], size: [W, bar], clip: a.clip });
    for (const layer of [0, 1]) await soft("graphics.set", { clip: a.clip, layer, props: { fill_color: "#000000", stroke: false } });
  }

  // animated text: style presets + in-animation + highlight words; every text fades out over its last 6 frames
  const STYLE = {
    vlog: (z, c) => ({ font: "Inter", font_style: "Black", fill_color: c || "#FFFFFF", stroke: true, stroke_color: "#000000", stroke_width: Math.round(z * 0.09), shadow: true, shadow_opacity: 60, shadow_distance: 6 }),
    pill: (z, c, a) => ({ font: "Inter", font_style: "Bold", fill_color: c || "#111111", background: true, background_color: a, background_opacity: 100, background_size: Math.round(z * 0.5), background_radius: Math.round(z * 0.9) }),
    caption: (z, c) => ({ font: "Inter", font_style: "Bold", fill_color: c || "#FFFFFF", background: true, background_color: "#000000", background_opacity: 55, background_size: Math.round(z * 0.4), background_radius: Math.round(z * 0.3) }),
    cinematic: (z, c) => ({ font: "Inter", font_style: "Medium", fill_color: c || "#FFFFFF", tracking: 400, shadow: true, shadow_opacity: 50 }),
    plain: (z, c) => ({ font: "Inter", font_style: "Bold", fill_color: c || "#FFFFFF", shadow: true, shadow_opacity: 70, shadow_distance: 4 }),
  };
  const DEF = { vlog: [96, [960, 260]], pill: [40, [960, 880]], caption: [46, [960, 960]], cinematic: [40, [960, 980]], plain: [60, [960, 200]] };
  const F = ticks(1);
  for (const X of P.texts || []) {
    const st = STYLE[X.style] ? X.style : "vlog";
    const size = X.size || DEF[st][0], [x, y] = X.position || DEF[st][1];
    const b = built[X.shot || 0], s = b.start + ticks(frames(X.offset ?? 0.3)), nf = frames(X.seconds ?? 2.5), e = s + ticks(nf - 1);
    const r = await soft("graphics.newText", { text: X.text, size, seconds: nf * den / num, time: s, position: [x, y] });
    if (!r) continue;
    const clip = r.clip;
    await soft("graphics.set", { clip, layer: 0, props: { align: "center", ...STYLE[st](size, X.color, X.accent || "#FFD60A"), ...(X.props || {}) } });
    for (const ph of X.highlight || []) {
      const at = X.text.indexOf(ph);
      if (at >= 0) await soft("graphics.setCharStyle", { clip, layer: 0, start: at, end: at + ph.length, style: { color: X.accent || "#FFD60A" } });
    }
    const fxs = (await fc.cmd("sequence.inspect")).video.flatMap(t => t.items).find(i => i.clip === clip)?.effects || [];
    const idx = fxs.findIndex(f => f.effect === "graphic_text");
    const on = new Set();
    const key = async (param, time, value) => {
      if (!on.has(param)) { on.add(param); await soft("effects.addKeyframe", { clip, effect: idx, param, time }); }
      await soft("graphics.set", { clip, layer: 0, props: { [param]: value }, time });
    };
    const a = X.anim || "fade";
    if (a === "pop") { await key("scale", s, 0); await key("scale", s + 4 * F, 115); await key("scale", s + 8 * F, 100); }
    if (a === "slide-up" || a === "slide-left") {
      await key("position", s, a === "slide-up" ? [x, y + 90] : [x + 260, y]);
      await key("position", s + 10 * F, [x, y]);
    }
    if (["fade", "slide-up", "slide-left", "track"].includes(a)) { await key("opacity", s, 0); await key("opacity", s + 8 * F, 100); }
    if (a === "track") { const t0 = X.props?.tracking ?? (st === "cinematic" ? 400 : 0); await key("tracking", s, t0); await key("tracking", e, t0 + 250); }
    if (a === "typewriter" || a === "words") {
      const parts = a === "words" ? X.text.split(" ").map((_, i, w) => w.slice(0, i + 1).join(" ")) : [...X.text].map((_, i, c) => c.slice(0, i + 1).join(""));
      const step = Math.max(1, Math.min(a === "words" ? 8 : 2, Math.floor((nf * 0.5) / parts.length)));
      for (const [i, p] of parts.entries()) await key("text", s + i * step * F, p);
    }
    await key("opacity", e - 6 * F, 100);
    await key("opacity", e, 0);
  }
  for (const M of P.templates || []) {
    const b = built[M.shot || 0], s = b.start + ticks(frames(M.offset ?? 0.5));
    const r = await soft("graphics.template.apply", { template: M.template, values: M.values || {}, time: s });
    if (!r) continue;
    await soft("graphics.resetDuration", { clip: r.clip, seconds: M.seconds ?? 4 });
    for (const edge of ["in", "out"]) await soft("sequence.applyVideoTransition", { clip: r.clip, effect: "cross_dissolve", frames: 8, edge });
  }

  // titles
  for (const T of P.titles || []) {
    const b = built[T.shot || 0];
    const r = await soft("graphics.newText", { text: T.text, size: T.size || 84, seconds: T.seconds || 2.4, time: b.start + ticks(frames(T.offset ?? 0.3)), ...(T.position ? { position: T.position } : {}) });
    if (!r) continue;
    await soft("graphics.set", { clip: r.clip, props: { align: "center", tracking: T.tracking ?? 200, shadow: true, ...(T.props || {}) } });
    for (const edge of ["in", "out"]) await soft("sequence.applyVideoTransition", { clip: r.clip, effect: "cross_dissolve", frames: frames(T.fade ?? 0.5), edge });
  }

  if (live) { await fc.cmd("playhead.set", { time: 0 }); await fc.call("ui.set", { timeline: { fit: true } }); }
  const saveTo = headlessOut || P.saveAs;
  await (saveTo ? fc.cmd("file.saveAs", { path: saveTo }) : fc.cmd("file.save"));
  const out = planPath.replace(/\.json$/, "") + ".built.json";
  fs.writeFileSync(out, JSON.stringify({ sequence: S.name, seconds: t / TPS, shots: built }, null, 1));
  console.log(`saved${saveTo ? " " + saveTo : ""}; ${out}\nverify: contact.exe <dir> program <project.fcproj> ${built.map(b => b.mid).join(" ")}`);
  fc.close();
})().catch(e => { console.error(e.message); process.exit(1); });
