"""Footage analyser: turns raw clips into a "moment map" the editors cut from (moments, not durations).

  tools/footage/.venv/Scripts/python.exe tools/footage/analyze.py <clip|folder> [...] --out <dir>
        [--model large-v3|medium|small] [--lang en] [--no-asr] [--sheet-step 1]
  tools/footage/.venv/Scripts/python.exe tools/footage/analyze.py dense <clip> <from_s> <to_s> [step_s] --out <dir>

Per clip it writes into --out:
  <stem>.analysis.json   everything: probe, 1 Hz picture/sound series, words with timestamps, shots, moments
  <stem>.md              human/agent summary: quality, transcript, the moment table with word-safe in/out points
  <stem>-sheet-NN.jpg    contact sheets, one frame per --sheet-step seconds, labelled with source time
Picture is analysed at 4 frames/s (luma, sharpness, motion, camera movement, shot cuts); sound at 10 Hz
(level, silence, bursts, clipping); speech with faster-whisper word timestamps (GPU if available).
The tool finds *where* things happen and where it is safe to cut; the editor still looks and decides *what* matters.
"""
import json, os, re, subprocess, sys
from pathlib import Path

import numpy as np

AFPS = 4          # analysis frames per second
AHZ = 10          # audio analysis rate
VIDEO_EXT = {".mp4", ".mov", ".mxf", ".mkv", ".avi", ".m4v", ".mts"}


def ffmpeg():
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


def probe(path):
    err = subprocess.run([ffmpeg(), "-hide_banner", "-i", str(path)], capture_output=True, text=True,
                         encoding="utf-8", errors="replace").stderr
    d = re.search(r"Duration: (\d+):(\d+):([\d.]+)", err)
    v = re.search(r"Video: (\w+).*?, (\d{2,5})x(\d{2,5})[^\n]*?([\d.]+) fps", err)
    a = re.search(r"Audio: (\w+)[^\n]*?(\d+) Hz", err)
    rot = re.search(r"rotate\s*:\s*(-?\d+)", err) or re.search(r"rotation of (-?[\d.]+) degrees", err)
    dur = int(d[1]) * 3600 + int(d[2]) * 60 + float(d[3]) if d else 0.0
    return {"duration": round(dur, 3), "vcodec": v and v[1], "width": v and int(v[2]), "height": v and int(v[3]),
            "fps": v and float(v[4]), "acodec": a and a[1], "audio_hz": a and int(a[2]),
            "rotation": rot and float(rot[1]), "has_audio": bool(a)}


def frames(path, fps, width):
    """Yield (t, rgb uint8 HxWx3) at `fps`, scaled to `width` (ffmpeg applies rotation)."""
    h_probe = probe(path)
    w, h = h_probe["width"] or 16, h_probe["height"] or 9
    if h_probe["rotation"] and abs(h_probe["rotation"]) % 180 == 90:
        w, h = h, w
    height = int(round(width * h / w / 2) * 2)
    cmd = [ffmpeg(), "-hide_banner", "-loglevel", "error", "-i", str(path), "-vf", f"fps={fps},scale={width}:{height}",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    n, size = 0, width * height * 3
    while True:
        buf = p.stdout.read(size)
        if len(buf) < size:
            break
        yield n / fps, np.frombuffer(buf, np.uint8).reshape(height, width, 3)
        n += 1
    p.wait()


def audio(path, rate=16000):
    cmd = [ffmpeg(), "-hide_banner", "-loglevel", "error", "-i", str(path), "-vn", "-ac", "1", "-ar", str(rate),
           "-f", "s16le", "-"]
    raw = subprocess.run(cmd, capture_output=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768.0


# ---------------------------------------------------------------- picture
ZONES = ["top-left", "top", "top-right", "left", "centre", "right", "bottom-left", "bottom", "bottom-right"]


rgb_for_faces = [None]


def grid_stats(gray, prev_gray, faces_det):
    """Per 3×3 cell: busyness (edge density), mean luma (0–100), motion, and whether a face sits in it.
    Captions go in calm cells away from faces; the luma says whether light or dark text will read there."""
    import cv2
    h, w = gray.shape
    edges = cv2.Canny(gray, 60, 160)
    diff = np.abs(gray.astype(np.int16) - prev_gray.astype(np.int16)) if prev_gray is not None else None
    faces = []
    if faces_det is not None:  # YuNet face detector on the colour frame
        faces_det.setInputSize((w, h))
        _, found = faces_det.detect(rgb_for_faces[0])
        for d in (found if found is not None else []):
            if d[-1] >= 0.6:
                x, y, fw, fh = (float(v) for v in d[:4])
                faces.append([round(x / w, 3), round(y / h, 3), round(fw / w, 3), round(fh / h, 3)])
    busy, luma, mot, face = [], [], [], []
    for gy in range(3):
        for gx in range(3):
            y0, y1, x0, x1 = gy * h // 3, (gy + 1) * h // 3, gx * w // 3, (gx + 1) * w // 3
            busy.append(round(float(np.mean(edges[y0:y1, x0:x1] > 0)) * 100, 1))
            luma.append(round(float(np.mean(gray[y0:y1, x0:x1])) / 2.55, 1))
            mot.append(round(float(np.mean(diff[y0:y1, x0:x1])), 1) if diff is not None else 0.0)
            cx0, cx1, cy0, cy1 = gx / 3, (gx + 1) / 3, gy / 3, (gy + 1) / 3
            face.append(any(fx < cx1 and fx + fw > cx0 and fy < cy1 and fy + fh > cy0 for fx, fy, fw, fh in faces))
    return {"busy": busy, "luma": luma, "motion": mot, "face": face, "faces": faces}


def analyse_picture(path, sheet_step):
    import cv2
    rows, thumbs, prev, prev_hist = [], [], None, None
    model = Path(__file__).parent / "models" / "face_detection_yunet_2023mar.onnx"
    faces_det = cv2.FaceDetectorYN.create(str(model), "", (320, 180), 0.6, 0.3, 50) if model.exists() else None
    prev_grid_gray = None
    for t, rgb in frames(path, AFPS, 320):
        gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
        g = gray.astype(np.float32)
        hist = cv2.calcHist([gray], [0], None, [32], [0, 256])
        cv2.normalize(hist, hist)
        r = {"t": round(t, 3), "y2": float(np.percentile(gray, 2) / 2.55), "y50": float(np.percentile(gray, 50) / 2.55),
             "y98": float(np.percentile(gray, 98) / 2.55), "sharp": float(cv2.Laplacian(gray, cv2.CV_64F).var()),
             "white": float(np.mean(gray >= 252)), "motion": 0.0, "cam": 0.0, "histcorr": 1.0}
        if prev is not None:
            r["motion"] = float(np.mean(np.abs(g - prev)))
            (dx, dy), _ = cv2.phaseCorrelate(prev, g)
            r["cam"] = float(np.hypot(dx, dy))
            r["histcorr"] = float(cv2.compareHist(prev_hist, hist, cv2.HISTCMP_CORREL))
        rows.append(r)
        if abs(t - round(t)) < 1e-6:  # once per second: caption zones (calm cells, faces, light/dark)
            rgb_for_faces[0] = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
            r["grid"] = grid_stats(gray, prev_grid_gray, faces_det)
            prev_grid_gray = gray
        if abs((t / sheet_step) - round(t / sheet_step)) < 1e-6:
            thumbs.append((t, cv2.resize(rgb, (240, int(240 * rgb.shape[0] / rgb.shape[1])))))
        prev, prev_hist = g, hist
    return rows, thumbs


def shot_cuts(rows):
    """Hard cuts: a sharp drop in histogram correlation together with a big pixel change."""
    if len(rows) < 3:
        return []
    mot = np.array([r["motion"] for r in rows])
    base = np.median(mot) + 1e-6
    cuts = [rows[i]["t"] for i in range(1, len(rows))
            if rows[i]["histcorr"] < 0.6 and mot[i] > max(12, 3 * base)]
    out = []
    for c in cuts:  # merge cuts closer than 0.75 s
        if not out or c - out[-1] > 0.75:
            out.append(c)
    return out


# ---------------------------------------------------------------- sound
def analyse_sound(samples, rate=16000):
    hop = rate // AHZ
    n = len(samples) // hop
    if n == 0:
        return [], {}
    frames_ = samples[: n * hop].reshape(n, hop)
    rms = np.sqrt(np.mean(frames_ ** 2, axis=1)) + 1e-9
    db = 20 * np.log10(rms)
    peak = np.max(np.abs(frames_), axis=1)
    floor = float(np.percentile(db, 10))
    p90 = float(np.percentile(db, 90))
    series = [{"t": round(i / AHZ, 2), "db": round(float(db[i]), 1), "clip": bool(peak[i] > 0.985)} for i in range(n)]
    # silences: below floor + 6 dB for ≥ 0.6 s
    quiet = db < floor + 6
    silences, i = [], 0
    while i < n:
        if quiet[i]:
            j = i
            while j < n and quiet[j]:
                j += 1
            if (j - i) / AHZ >= 0.6:
                silences.append([round(i / AHZ, 2), round(j / AHZ, 2)])
            i = j
        else:
            i += 1
    # bursts: sudden rises well above the clip's usual loud level (laughs, shouts, claps, hits)
    bursts = [round(i / AHZ, 2) for i in range(2, n) if db[i] > p90 + 4 and db[i] - db[i - 2] > 10]
    stats = {"floor_db": round(floor, 1), "p90_db": round(p90, 1), "max_db": round(float(db.max()), 1),
             "clipping_s": round(float(np.sum(peak > 0.985)) / AHZ, 1), "silences": silences, "bursts": bursts}
    return series, stats


# ---------------------------------------------------------------- speech
def load_whisper(model_name):
    import site
    for sp in site.getsitepackages():  # make the pip-installed CUDA libraries visible on Windows
        for sub in ("nvidia/cublas/bin", "nvidia/cudnn/bin"):
            d = Path(sp) / sub
            if d.is_dir():
                os.add_dll_directory(str(d))
                os.environ["PATH"] = str(d) + os.pathsep + os.environ["PATH"]
    from faster_whisper import WhisperModel
    local = Path(__file__).parent / "models" / model_name  # pre-downloaded copy (see setup.sh) beats the hub
    if (local / "model.bin").exists():
        model_name = str(local)
    try:
        return WhisperModel(model_name, device="cuda", compute_type="float16"), "cuda"
    except Exception as e:  # no GPU / CUDA libs → CPU
        print(f"  whisper on CPU ({e.__class__.__name__}: {e})")
        return WhisperModel(model_name, device="cpu", compute_type="int8"), "cpu"


def transcribe(model, samples, lang):
    segs, info = model.transcribe(samples, language=lang, word_timestamps=True, vad_filter=True,
                                  vad_parameters={"min_silence_duration_ms": 300}, condition_on_previous_text=False)
    words, segments = [], []
    for s in segs:
        ws = [{"w": w.word.strip(), "s": round(w.start, 2), "e": round(w.end, 2), "p": round(w.probability, 2)}
              for w in (s.words or []) if w.word.strip()]
        if not ws:
            continue
        words += ws
        segments.append({"s": ws[0]["s"], "e": ws[-1]["e"], "text": s.text.strip(),
                         "p": round(float(np.mean([w["p"] for w in ws])), 2)})
    return words, segments, {"language": info.language, "language_p": round(info.language_probability, 2)}


# ---------------------------------------------------------------- moments
def speech_units(segments, gap=0.7):
    """Join whisper segments into utterances (a person's complete turn) when the pause between them is short."""
    units = []
    for s in segments:
        if units and s["s"] - units[-1]["e"] < gap:
            units[-1]["e"] = s["e"]
            units[-1]["text"] += " " + s["text"]
            units[-1]["p"] = min(units[-1]["p"], s["p"])
        else:
            units.append(dict(s))
    return units


def build_moments(dur, rows, cuts, units, words, sound_stats):
    """Split the clip into candidate moments at real boundaries: shot cuts, utterance edges, and changes between
    still / moving picture. No fixed lengths: a moment is as long as what happens in it."""
    edges = {0.0, round(dur, 2)} | {round(c, 2) for c in cuts}
    for u in units:
        edges |= {round(max(0.0, u["s"] - 0.2), 2), round(min(dur, u["e"] + 0.3), 2)}
    # still ↔ moving changes in stretches without speech (smoothed over 2 s)
    if rows:
        mot = np.convolve([r["motion"] + 2 * r["cam"] for r in rows], np.ones(8) / 8, mode="same")
        thr = max(6.0, float(np.median(mot)) * 1.5)
        state = mot > thr
        for i in range(1, len(state)):
            if state[i] != state[i - 1]:
                t = rows[i]["t"]
                if not any(u["s"] - 0.2 <= t <= u["e"] + 0.3 for u in units):
                    edges.add(round(t, 2))
    hard = {0.0, round(dur, 2)} | {round(c, 2) for c in cuts}
    for u in units:
        hard |= {round(max(0.0, u["s"] - 0.2), 2), round(min(dur, u["e"] + 0.3), 2)}
    edges = sorted(e for e in edges if 0 <= e <= dur)
    merged = [edges[0]]
    for e in edges[1:]:
        # still/moving edges are soft: keep them only if both sides stay ≥ 2.5 s (handheld wobble isn't a moment);
        # cuts and utterance edges are hard: keep unless they'd leave a < 0.8 s sliver
        min_gap = 0.8 if e in hard else 2.5
        if e - merged[-1] >= min_gap or e == edges[-1]:
            merged.append(e)
    while len(merged) > 2 and merged[-1] - merged[-2] < (0.8 if merged[-2] in hard else 2.5):
        merged.pop(-2)

    def window(a, b):
        return [r for r in rows if a <= r["t"] < b] or rows[:1]

    sharp_all = np.array([r["sharp"] for r in rows]) if rows else np.array([1.0])
    blur_thr = max(15.0, float(np.percentile(sharp_all, 20)) * 0.6)
    moments = []
    for a, b in zip(merged, merged[1:]):
        w = window(a, b)
        talk = [u for u in units if u["s"] < b and u["e"] > a]
        text = " ".join(x["w"] for x in words if a <= (x["s"] + x["e"]) / 2 < b)
        sharp = np.array([r["sharp"] for r in w])
        cam = float(np.mean([r["cam"] for r in w]))
        mot = float(np.mean([r["motion"] for r in w]))
        flags = []
        if np.mean(sharp < blur_thr) > 0.5: flags.append("blurry")
        if np.mean([r["y98"] for r in w]) < 20: flags.append("dark")
        if np.mean([r["y50"] for r in w]) < 3: flags.append("black")
        if np.mean([r.get("white", 0) for r in w]) > 0.25: flags.append("blown")  # > 25 % of the frame clipped
        if cam > 6: flags.append("shaky/fast-pan")
        kind = "talk" if talk and text else ("moving" if mot + 2 * cam > 10 else "still")
        bursts = [t for t in sound_stats.get("bursts", []) if a <= t < b]
        # word-safe cut points: never inside a word; prefer the nearest pause
        in_s = a
        inside = [x for x in words if x["s"] < in_s < x["e"]]
        if inside: in_s = max(0.0, inside[0]["s"] - 0.1)
        out_s = b
        inside = [x for x in words if x["s"] < out_s < x["e"]]
        if inside: out_s = min(dur, inside[-1]["e"] + 0.15)
        zones = caption_zones([r["grid"] for r in w if "grid" in r])
        moments.append({"id": f"m{len(moments) + 1:03d}", "zones": zones, "start": round(a, 2), "end": round(b, 2),
                        "dur": round(b - a, 2), "in": round(in_s, 2), "out": round(out_s, 2), "kind": kind,
                        "text": text, "motion": round(mot, 1), "camera": round(cam, 1), "bursts": bursts,
                        "flags": flags, "y50": round(float(np.mean([r["y50"] for r in w])), 1)})
    return moments


def caption_zones(grids):
    """Rank the 3×3 cells for captions over a moment: calm (few edges, little motion), never where a face appears,
    and say which text tone reads there. Returns e.g. [{"zone": "top", "tone": "dark text", "calm": 91}, …]."""
    if not grids:
        return []
    busy_all = np.array([[g["busy"][i] for i in range(9)] for g in grids]).mean(axis=0)
    mot_all = np.array([[g["motion"][i] for i in range(9)] for g in grids]).mean(axis=0)
    # calm is judged RELATIVE to this shot: in a leafy forest every cell is busy in absolute terms, but some are
    # still much calmer than others (a patch of sky, a dark trunk, the path). 100 = calmest cell in the shot.
    lo, hi = float(busy_all.min()), float(busy_all.max())
    rel = (busy_all - lo) / (hi - lo + 1e-6)
    mlo, mhi = float(mot_all.min()), float(mot_all.max())
    mrel = (mot_all - mlo) / (mhi - mlo + 1e-6)
    out = []
    for i, name in enumerate(ZONES):
        if name == "centre" or any(g["face"][i] for g in grids):
            continue
        luma = float(np.mean([g["luma"][i] for g in grids]))
        calm = 100 * (1 - 0.7 * rel[i] - 0.3 * mrel[i])
        tone = "dark text" if luma > 62 else "light text" if luma < 45 else "light text + shadow"
        if busy_all[i] > 30:  # busy texture even at its calmest: text needs a stronger treatment here
            tone += " (busy: outline/plate)"
        out.append({"zone": name, "calm": round(calm), "luma": round(luma), "busy": round(float(busy_all[i]), 1),
                    "tone": tone})
    return sorted(out, key=lambda z: -z["calm"])[:3]


# ---------------------------------------------------------------- outputs
def contact_sheets(thumbs, out, stem, cols=6, rows_=5, label=""):
    import cv2
    paths, per = [], cols * rows_
    for k in range(0, len(thumbs), per):
        chunk = thumbs[k:k + per]
        th, tw = chunk[0][1].shape[:2]
        sheet = np.full((rows_ * (th + 18), cols * tw, 3), 20, np.uint8)
        for i, (t, img) in enumerate(chunk):
            y, x = (i // cols) * (th + 18), (i % cols) * tw
            sheet[y:y + th, x:x + tw] = img
            cv2.putText(sheet, f"{label}{fmt(t)}", (x + 4, y + th + 13), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (235, 235, 235), 1,
                        cv2.LINE_AA)
        used_rows = (len(chunk) - 1) // cols + 1
        p = Path(out) / f"{stem}-sheet-{k // per + 1:02d}.jpg"
        cv2.imwrite(str(p), cv2.cvtColor(sheet[: used_rows * (th + 18)], cv2.COLOR_RGB2BGR),
                    [cv2.IMWRITE_JPEG_QUALITY, 85])
        paths.append(p.name)
    return paths


def zones_txt(m):
    return ", ".join(f"{z['zone']} ({z['tone']})" for z in m.get("zones", [])) or "—"


def fmt(t):
    return f"{int(t // 60)}:{t % 60:04.1f}"


def write_md(path, a):
    L = [f"# {a['file']}", "",
         f"- {a['probe']['duration']} s · {a['probe']['width']}×{a['probe']['height']} · {a['probe']['fps']} fps · "
         f"{a['probe']['vcodec']} · audio: {a['probe']['acodec'] or 'none'}",
         f"- Sound: floor {a['sound']['floor_db']} dB, loud ≈ {a['sound']['p90_db']} dB, clipping "
         f"{a['sound']['clipping_s']} s, {len(a['sound']['bursts'])} bursts (laughs/shouts/claps/hits)",
         f"- Speech: {len(a['words'])} words" + (f" ({a['speech_info']['language']})" if a.get("speech_info") else "")
         + " — **transcripts are machine-made: confirm any line by ear before captioning it**",
         f"- Shot cuts inside the clip: {', '.join(fmt(c) for c in a['cuts']) or 'none'}",
         f"- Contact sheets ({a['sheet_step']} s per frame): {', '.join(a['sheets'])}", "",
         "## Moments (candidate units — the editor decides what each is worth)", "",
         "| id | from–to | dur | safe in–out | kind | flags | caption zones (calmest first) | what's said / heard |",
         "|---|---|---|---|---|---|---|---|"]
    for m in a["moments"]:
        said = (m["text"][:110] + "…") if len(m["text"]) > 110 else m["text"]
        heard = f" · bursts {', '.join(fmt(b) for b in m['bursts'])}" if m["bursts"] else ""
        L.append(f"| {m['id']} | {fmt(m['start'])}–{fmt(m['end'])} | {m['dur']} | {m['in']}–{m['out']} | {m['kind']} | "
                 f"{' '.join(m['flags'])} | {zones_txt(m)} | {said}{heard} |")
    if a["segments"]:
        L += ["", "## Transcript (utterances)", ""]
        L += [f"- **{fmt(u['s'])}–{fmt(u['e'])}** {u['text']}" + ("  *(low confidence)*" if u["p"] < 0.6 else "")
              for u in a["units"]]
    Path(path).write_text("\n".join(L) + "\n", encoding="utf-8")


def analyse(path, out, model, lang, sheet_step):
    path = Path(path)
    stem = path.stem
    print(f"- {path.name}")
    pr = probe(path)
    rows, thumbs = analyse_picture(path, sheet_step)
    cuts = shot_cuts(rows)
    samples = audio(path) if pr["has_audio"] else np.zeros(1, np.float32)
    sound_series, sound_stats = analyse_sound(samples)
    words, segments, info = ([], [], None)
    if model is not None and pr["has_audio"] and len(samples) > 16000:
        words, segments, info = transcribe(model, samples, lang)
    units = speech_units(segments)
    moments = build_moments(pr["duration"], rows, cuts, units, words, sound_stats)
    sheets = contact_sheets(thumbs, out, stem) if thumbs else []
    pic_1hz = [r for r in rows if abs(r["t"] - round(r["t"])) < 1e-6]
    a = {"file": str(path), "probe": pr, "cuts": cuts, "sound": sound_stats, "speech_info": info,
         "words": words, "segments": segments, "units": units, "moments": moments, "sheets": sheets,
         "sheet_step": sheet_step,
         "picture_1hz": [{k: (round(v, 2) if isinstance(v, float) else v) for k, v in r.items()} for r in pic_1hz],
         "sound_10hz": sound_series}
    (Path(out) / f"{stem}.analysis.json").write_text(json.dumps(a, ensure_ascii=False), encoding="utf-8")
    write_md(Path(out) / f"{stem}.md", a)
    print(f"  {pr['duration']} s, {len(cuts)} cuts, {len(words)} words, {len(moments)} moments → {stem}.md")


def dense(path, t0, t1, step, out):
    path = Path(path)
    thumbs = []
    for t, rgb in frames_range(path, t0, t1, step):
        import cv2
        thumbs.append((t, cv2.resize(rgb, (240, int(240 * rgb.shape[0] / rgb.shape[1])))))
    p = contact_sheets(thumbs, out, f"{path.stem}-dense-{t0:g}-{t1:g}", cols=6, rows_=10)
    print("\n".join(str(Path(out) / x) for x in p))


def frames_range(path, t0, t1, step):
    pr = probe(path)
    w, h = pr["width"] or 16, pr["height"] or 9
    if pr["rotation"] and abs(pr["rotation"]) % 180 == 90:
        w, h = h, w
    height = int(round(320 * h / w / 2) * 2)
    cmd = [ffmpeg(), "-hide_banner", "-loglevel", "error", "-ss", str(t0), "-t", str(t1 - t0), "-i", str(path),
           "-vf", f"fps={1 / step},scale=320:{height}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    n, size = 0, 320 * height * 3
    while True:
        buf = p.stdout.read(size)
        if len(buf) < size:
            break
        yield t0 + n * step, np.frombuffer(buf, np.uint8).reshape(height, 320, 3)
        n += 1


def main(argv):
    def opt(name, default=None):
        return argv[argv.index(name) + 1] if name in argv else default
    out = Path(opt("--out", "analysis"))
    out.mkdir(parents=True, exist_ok=True)
    if argv and argv[0] == "dense":
        dense(argv[1], float(argv[2]), float(argv[3]), float(argv[4]) if len(argv) > 4 and not argv[4].startswith("--")
              else 0.25, out)
        return
    skip = {opt("--out"), opt("--model"), opt("--lang"), opt("--sheet-step")}
    inputs = [a for a in argv if not a.startswith("--") and a not in skip]
    clips = []
    for i in inputs:
        p = Path(i)
        clips += sorted(x for x in p.iterdir() if x.suffix.lower() in VIDEO_EXT and not x.name.startswith("._")) \
            if p.is_dir() else [p]
    model = None
    if "--no-asr" not in argv:
        model, dev = load_whisper(opt("--model", "large-v3"))
        print(f"whisper {opt('--model', 'large-v3')} on {dev}")
    for c in clips:
        try:
            analyse(c, out, model, opt("--lang"), float(opt("--sheet-step", 1)))
        except Exception as e:
            print(f"  FAILED {c.name}: {e}")
    print(f"done: {len(clips)} clip(s) → {out}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main(sys.argv[1:])
