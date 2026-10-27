"""Check a cut against the footage analysis, and print it as a viewer would "read" it.

  tools/footage/.venv/Scripts/python.exe tools/footage/checkcut.py projects/<p>/edit/cutlist.json

cutlist.json (every editor writes one next to its own build plan):
  {"analysis": "projects/<p>/edit/analysis",            # folder with <stem>.analysis.json from analyze.py
   "items": [{"clip": "D:/footage/DJI_0011.MP4", "in": 12.3, "out": 18.9,
              "rec": 0.0,                               # optional: position in the film (s); else list order
              "audio": true,                            # does the clip's own sound play here (default true)
              "why": "she laughs into the lens",        # the moment this shot carries
              "ok_short": false}]}                      # deliberate < 1 s shot (a burst, a flash)
Writes <cutlist>.check.md (problems first) and <cutlist>.transcript.md (the film's spoken words in order).
Problems found: words cut in half, utterances entered or left mid-way, cut points on blurred / black frames,
the same source moment used twice, accidental slivers, and long stretches with nothing said or happening.
"""
import json, sys
from pathlib import Path

import numpy as np


def fmt(t):
    return f"{int(t // 60)}:{t % 60:04.1f}"


def load(analysis_dir, clip):
    p = Path(analysis_dir) / f"{Path(clip).stem}.analysis.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None


def at(series, t):
    return min(series, key=lambda r: abs(r["t"] - t)) if series else None


def main(path):
    cl = json.loads(Path(path).read_text(encoding="utf-8"))
    adir = cl.get("analysis") or str(Path(path).parent / "analysis")
    items = cl["items"]
    rec = 0.0
    for it in items:
        it.setdefault("rec", rec)
        rec = it["rec"] + max(0.0, it["out"] - it["in"])
    items.sort(key=lambda x: x["rec"])
    errors, warns, lines, used = [], [], [], {}
    cache = {}
    for n, it in enumerate(items, 1):
        clip, a, b = it["clip"], it["in"], it["out"]
        tag = f"#{n} {Path(clip).stem} {a:.2f}–{b:.2f} @ {fmt(it['rec'])}"
        if b <= a:
            errors.append(f"{tag}: out ≤ in")
            continue
        an = cache.setdefault(clip, load(adir, clip))
        if an is None:
            warns.append(f"{tag}: no analysis for this clip (run analyze.py)")
            continue
        words, units = an["words"], an["units"]
        if it.get("audio", True):
            for cut, side in ((a, "in"), (b, "out")):
                w = [x for x in words if x["s"] + 0.03 < cut < x["e"] - 0.03]
                if w:
                    errors.append(f"{tag}: cuts the word “{w[0]['w']}” in half at the {side} point ({cut:.2f})")
            for u in units:
                if u["s"] + 0.3 < a < u["e"] - 0.3:
                    warns.append(f"{tag}: enters mid-utterance (“…{u['text'][:50]}”) — start at {u['s'] - 0.15:.2f}?")
                if u["s"] + 0.3 < b < u["e"] - 0.3:
                    warns.append(f"{tag}: leaves mid-utterance (“{u['text'][-50:]}…”) — end at {u['e'] + 0.2:.2f}?")
        pic = an.get("picture_1hz", [])
        if pic:
            sharp = np.array([r["sharp"] for r in pic])
            thr = max(15.0, float(np.percentile(sharp, 20)) * 0.6)
            for cut, side in ((a, "in"), (b, "out")):
                r = at(pic, cut)
                if r["y50"] < 3:
                    errors.append(f"{tag}: {side} point is on a black frame")
                elif r["sharp"] < thr:
                    warns.append(f"{tag}: {side} point is on a blurred frame ({cut:.2f})")
        dur = b - a
        if dur < 1.0 and not it.get("ok_short"):
            warns.append(f"{tag}: {dur:.2f} s sliver — intended? (set ok_short) or extend to the whole moment")
        for (c, x, y, m) in used.get(clip, []):
            if a < y and b > x:
                warns.append(f"{tag}: overlaps #{m} ({x:.2f}–{y:.2f}) of the same clip — the same moment twice?")
        used.setdefault(clip, []).append((clip, a, b, n))
        said = " ".join(x["w"] for x in words if a <= (x["s"] + x["e"]) / 2 < b) if it.get("audio", True) else ""
        lines.append((it, n, said))
    # long stretches where nothing is said and nothing is happening (possible dead air)
    quiet_run, run_start = 0.0, None
    for it, n, said in lines:
        an = cache.get(it["clip"])
        mot = [r["motion"] + 2 * r["cam"] for r in (an or {}).get("picture_1hz", []) if it["in"] <= r["t"] < it["out"]]
        still = (not said) and mot and float(np.mean(mot)) < 4
        if still:
            run_start = run_start if run_start is not None else it["rec"]
            quiet_run = it["rec"] + it["out"] - it["in"] - run_start
            if quiet_run > 25:
                warns.append(f"{fmt(run_start)}–{fmt(run_start + quiet_run)}: {quiet_run:.0f} s with no speech and "
                             f"little movement — is it earning its place (mood, breath) or dead air?")
                run_start, quiet_run = None, 0.0
        else:
            run_start, quiet_run = None, 0.0

    total = max((it["rec"] + it["out"] - it["in"] for it, _, _ in lines), default=0)
    lens = [it["out"] - it["in"] for it, _, _ in lines]
    rep = [f"# Cut check — {Path(path).name}", "",
           f"{len(lines)} shots · {fmt(total)} · shot length: median {np.median(lens):.1f} s, "
           f"min {min(lens):.1f}, max {max(lens):.1f} (lengths are an outcome of the moments, not a target)" if lens else "",
           "", f"## Errors ({len(errors)}) — fix before anyone sees it", ""] + [f"- {e}" for e in errors] + \
          ["", f"## Warnings ({len(warns)}) — check each, fix or justify", ""] + [f"- {w}" for w in warns]
    Path(str(path).replace(".json", ".check.md")).write_text("\n".join(rep) + "\n", encoding="utf-8")
    tr = [f"# The cut, read as a viewer — {Path(path).name}", "",
          "Every shot in order with what is said in it. Read it top to bottom: does it make sense, is anything cut "
          "off, repeated, or boring?", ""]
    for it, n, said in lines:
        tr.append(f"**{fmt(it['rec'])}** · #{n} {Path(it['clip']).stem} {it['in']:.1f}–{it['out']:.1f} "
                  f"({it['out'] - it['in']:.1f} s)" + (f" — *{it['why']}*" if it.get("why") else ""))
        tr.append(f"> {said}" if said else "> *(no speech)*")
        tr.append("")
    Path(str(path).replace(".json", ".transcript.md")).write_text("\n".join(tr), encoding="utf-8")
    print(f"{len(errors)} errors, {len(warns)} warnings → {Path(str(path).replace('.json', '.check.md')).name}")
    for e in errors[:10]:
        print("  ERROR", e)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main(sys.argv[1]))
