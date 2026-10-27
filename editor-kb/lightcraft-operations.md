# Driving LightCraft — operations manual

LightCraft 0.14.0 (Lightroom-class photo library + raw developer, pure Rust; 376 commands, 122 develop controls).
Paths are relative to `C:\CodeHouse\AIFilmEditor\`. Verified on this machine (2026-10-10): frame grab, headless
`run`/`render`, persistent project-style library, preset/sync/mask/crop/export, MCP headless, GUI via `craft.js` with
`--memory` (import, develop, histogram, screenshot, export, quit). **Re-verified headless 2026-10-27 on 0.14.0**
(throwaway library): import, select, develop.set/get, preset.create/list, rate/flag, develop.sync, radial mask +
mask.adjust, crop.aspect/rotateAspect, export JPEG full size + 16-bit TIFF, persistence across runs, `render
--settings/--preset/--set`, MCP `--compact` handshake + tool list (tool *calls* not re-run). GUI/control channel not
re-run. Lines marked **UNVERIFIED** were read from the source/docs but not run.

**Quick recipe (stills from footage, verified end to end):**
```sh
F=apps/filmcraft/target/release/examples/contact.exe; L=apps/lightcraft/target/release/lightcraft-cli.exe
$F projects/x/stills/frames/0011-25.2.png frame D:/footage/DJI_0011.MP4 25.2
$L render projects/x/stills/frames/0011-25.2.png -o projects/x/stills/still-01-earth.jpg --settings projects/x/stills/clean-warm.json --quality 92
$F projects/x/stills/lv.jpg range projects/x/stills/still-01-earth.jpg 0 0.1 0.1     # levels
```

## Binaries and setup

| What | Path |
|---|---|
| Desktop app | `apps\lightcraft\target\release\lightcraft.exe` |
| Headless CLI (run / render / mcp / snapshot) | `apps\lightcraft\target\release\lightcraft-cli.exe` (`--help`) |
| Control client (shared) | `node tools\craft.js lightcraft …` (port 9872) |
| Frame grab from video | FilmCraft (see *Stills from video*) |
| Levels meter | `apps\filmcraft\target\release\examples\contact.exe` (reads PNG/JPEG too) |

Rebuild: `sh tools/build-apps.sh lightcraft` (log `output/build-logs/lightcraft.log`). Command registry and control
ranges straight from the binary: `lightcraft-cli commands`, `lightcraft-cli controls` (add `--json`).

## Libraries: never the user's

The desktop app, run bare, opens `%USERPROFILE%\Pictures\LightCraft Library` (or the library last chosen in its
Settings; env `LIGHTCRAFT_LIBRARY` overrides the default) and seeds a *new* library with demo photos. That is the
user's personal catalog: **never open it.** Instead:

| Use | How |
|---|---|
| Project library (persistent, the normal case) | `--library projects/<name>/stills/library` (created on first use) — app: also `--no-demo` |
| Throwaway (tests, experiments) | CLI/MCP: no `--library` = in-memory session (`library.info` → `persistent:false`); app: `--memory` (writes nothing — no prefs, no log, no `%APPDATA%\LightCraft` — but starts with 24 demo photos; your imports get the next ids, e.g. 25) |

A project library folder holds `catalog.snap`, `catalog.log`, `catalog.lock`, `presets.json` (user presets),
`view.json` — small, safe to keep in `stills/library/`. Ratings, flags, edits and presets persist between runs (verified).

- A library is open in one program at a time (`catalog.lock`). If the app has the project library open, headless
  `--library` on it fails ("already open in LightCraft (process N)") — use the app's control channel or MCP connect.
- `--library` on the command line does **not** change the app's remembered library; the Settings panel **does**
  (it'd make the user's next launch open the project) — don't use it. (2026-10-27: `app.openLibrary` is no longer a
  command.)
- A non-memory app session saves its UI preferences (`%APPDATA%\LightCraft\ui.json`: view, panels) — harmless, but a
  reason to prefer `--memory` for experiments.
- Import with `mode: "add"` (the default): photos are referenced in place, never copied/moved/renamed. Edits live in
  the library, not in the files. **XMP sidecars:** `photo.saveMetadataToFile`, `library.toggleAutoWriteXmp` /
  `library.xmpPreferences {autoWrite:true}` write `.xmp` files *next to the originals* — never on source folders.

## Stills from video (frame grab)

LightCraft can't read video (no video import, no frame grab). Grab full-resolution frames with FilmCraft.

**Simplest (verified):** `apps/filmcraft/target/release/examples/contact.exe <out.png|.jpg> frame <video> <seconds>`
→ one full-res 8-bit frame, prints `{"frame","w","h"}` (1920×1080 PNG ≈ 2 MB). Seconds are plain seconds.

**16-bit, or many frames in one go** — headless `filmcraft-cli` (verified, ~0.5 s):

```sh
# grab.jsonl — one import, then one exportFrame per still (time in TICKS: seconds × 254016000000)
{"id":"file.import","params":{"paths":["D:/footage/DJI_0011.MP4"]}}
{"id":"file.exportFrame","params":{"path":"C:/…/stills/frames/0011-25.200.png","format":"png","depth":16,"target":"source","item":1,"time":6401203200000}}
```
`apps/filmcraft/target/release/filmcraft-cli.exe --compact run grab.jsonl` → `{"width":1920,"height":1080,"depth":16,"time":…}`.

- **`time` must be ticks.** `seconds` is silently ignored and you get frame 0. Ticks = `Math.round(s * 254016000000)`.
- The frame returned is the one at or just before `time` (25.2 s → 25.1918 s on 59.94p); the result's `time` says which.
- Item ids are sequential per run: one `file.import` of N paths → items 1…N in that order.
- `depth: 16` (8 MB PNG) gives grading headroom; `depth: 8` (2.3 MB) is fine for straight use. `format` also takes
  `jpeg|tiff|bmp`. Don't pass `"import": true` (it adds the frame to a project).
- The source footage is read only; write frames to `projects/<name>/stills/frames/`.
- LightCraft imports both 8- and 16-bit PNG (verified); untouched photos export pixel-identical in levels.
- Pick the moment first: `contact.exe <sheet.jpg> range <video> <from> <to> 0.1` and choose the sharpest peak frame.

## Three ways to drive it

### 1. One-shot CLI: `lightcraft-cli run` (preferred for batch work)
One process, a chain of commands, one JSON line per command (`{"command","ok","result"|"error","ms"}`; exit ≠ 0 on
failure). A word without `=` starts the next command; `key=value` values are JSON when they parse; a `'{…}'`
argument merges an object into the params. `--script file.jsonl` runs `{"command": id, "params": {…}}` lines (or
`{"method": …}` control requests); `--keep-going` continues after errors. `run --connect ADDR` drives the running
app instead — its default is 127.0.0.1:**7980**, so pass `--connect 127.0.0.1:9872` for an app started by `craft.js`.

```sh
L=apps/lightcraft/target/release/lightcraft-cli.exe
$L run --import frame.png develop.set '{"values":{"light.exposure":0.1}}' app.export path=out.jpg longEdge=1920 quality=92
$L run --library projects/x/stills/library --import projects/x/stills/frames library.info
$L run --library projects/x/stills/library --script develop.jsonl
```

### 2. Single file: `lightcraft-cli render`
`$L render in.png -o out.jpg --settings look.json --quality 92 --opt longEdge=1920` — develop one file with a settings
JSON (`--settings`, partial develop JSON), sliders (`--set light.exposure=0.2`, repeatable), a preset (`--preset id`)
and any `app.export` option (`--opt key=value`); `--size N` = long edge. No library at all — the fastest way to
apply a saved look. Output format by extension: `.jpg .png .tif .webp .avif .jxl .psd .dng`. `--settings` also takes a
`.lcpreset` (from `preset.export`) or an XMP preset (2026-10-27).
Default output is full size (cropped), JPEG quality 92. **Only one `--settings` file counts** (a second one replaces the
first): merge look + crop into one JSON. The settings JSON uses `develop.get`'s snake_case shape, e.g.
`{"wb":{"mode":"custom","temp":6700,"tint":1},"light":{"exposure":0.05,"whites":15},"crop":{"geometry":{"rect":{"x0":0.3,"y0":0.2,"x1":0.4,"y1":0.3}}}}`.

### 3. Running app (control channel), when the user should watch
```sh
node tools/craft.js lightcraft --start --library C:/CodeHouse/AIFilmEditor/projects/<name>/stills/library --no-demo   # UNVERIFIED in the GUI (flags verified in source)
node tools/craft.js lightcraft --start --memory          # throwaway (verified; ready in ~2 s)
node tools/craft.js lightcraft library.info              # engine command
node tools/craft.js lightcraft --ui ui.screenshot '{"path":"C:/…/ui.png"}'
node tools/craft.js lightcraft --ui app.quit             # close it when done (ask first if it's the user's session)
```
Protocol: JSON lines on 127.0.0.1:PORT, `{id, method, params}` → `{id, ok, result | error}` (error is a string).
No authentication (loopback only). Methods: `engine.execute {command, params}`, `engine.commands`, `ui.inspect`,
`ui.set`, `ui.widgets`, `ui.clickWidget {id}`, `ui.key`, `ui.pointer`, `ui.screenshot {path, headless?}`,
`ui.render {id?, size?, path?}` (without `path`: returns the **histogram**), `app.quit`. Any malformed line closes
the connection. Requests run on the UI thread between frames (60 s timeout).

### MCP
`.mcp.json` entries (not installed; the user/coordinator adds them):
```json
"lightcraft":     {"command": "C:/CodeHouse/AIFilmEditor/apps/lightcraft/target/release/lightcraft-cli.exe",
                   "args": ["mcp", "--compact"]},
"lightcraft-app": {"command": "C:/CodeHouse/AIFilmEditor/apps/lightcraft/target/release/lightcraft-cli.exe",
                   "args": ["mcp", "--connect", "127.0.0.1:9872"]}
```
Verified headless (`--compact`: 17 tools; `import` → `set_develop {values}` → `render_photo` returning a PNG image;
2026-10-27 on 0.14.0: still 17 tools, server reports version 0.14.0).
Connect mode (`lightcraft-app`) is UNVERIFIED but is a thin layer over the control channel, which is verified.
Headless MCP without `--library` is in memory; pass the project library per session with `--library` only if it's
fixed (it's a server argument, so a per-project library is easier through `run`). Helper tools: `import`,
`query_photos`, `select_photos`, `list_controls`, `get_develop`, `set_develop {values|settings}`, `apply_preset`,
`crop {rect, angle, reset}`, `render_photo {id?, size?, format?, path?}` (returns the image), `render_preview`,
`export`, `command_list`/`list_commands`, `command_run`/`run_command`, `command_batch`, `doc_inspect`; connect mode
adds `screenshot`, `inspect_ui`, `click`, `press_key`, `pointer_gesture`. Without `--compact` every command is also a
tool (393 tools on 0.14.0 — use `--compact`).

## Commands for the photo-grader (ids and params)

Run on this machine: `library.import`, `library.info`, `catalog.query`, `library.select`, `library.filter`,
`develop.set/merge/get`, `presets.list`, `preset.create`, `photo.rate`, `photo.flag`, `develop.sync`, `mask.add`
(radial), `mask.adjust`, `crop.aspect`, `crop.rotateAspect`, `crop.set`, `app.export` (path and dir) — ids and params all still current on 0.14.0 (2026-10-27). The rest are
taken from the command registry (`lightcraft-cli commands`) — **UNVERIFIED** until first use; check the result.

Most commands act on the **active photo** or the **selection**; `ids` overrides. `library.select {ids, active}` first.
Import ids are sequential in path order (a folder of `a.png, b.png` → 1, 2); `catalog.query` lists newest first, so
map ids by `fileName`, not by position. After an import the first new photo is active.

### Library, import, culling
| Command | Params | Notes |
|---|---|---|
| `library.import` | `{paths:[file\|folder], mode?: add\|copy\|move, album?, preset?}` | → imported ids; **always `add`** for sources. Folders recurse; duplicates skipped |
| `library.importPreview` | `{paths}` | candidates, formats, duplicates — nothing added |
| `library.info` / `library.state` / `catalog.stats` | `{}` | counts, selection, active, unsaved |
| `catalog.query` | `{filter?, sort?, offset?, limit?}` | photos in view (`id`, name, rating, flag…) |
| `library.select` | `{ids, active?, mode?: replace\|add\|toggle\|range}` | |
| `library.filter` / `library.clearFilter` | `{text?, rating?, ratingOp?, flag?, label?, keyword?, camera?, edited?}` | search: `rating:>3 flag:pick` |
| `library.sort` | `{key: captureDate\|importDate\|fileName\|rating…, ascending?}` | |
| `photo.rate` | `{rating: 0..5, ids?, advance?}` | |
| `photo.flag` / `photo.pick` / `photo.reject` / `photo.unflag` | `{flag: pick\|reject\|none, ids?}` | |
| `photo.label` | `{label: red\|yellow\|green\|blue\|purple\|none, ids?}` | |
| `photo.analyze` | `{ids?, rejectBelow?: 0..100, pickBest?: bool, burstGap?: s (10), similarity?: 0..1 (0.93)}` | sharpness 0–100, clipping, look-alike groups, best of each |
| `library.findSimilar` | `{id?, similarity?: 0.8}` | |
| `stack.auto` | `{gap?: s}` | stack bursts |
| `album.create` | `{name, addSelected?}` | collections; `album.addPhotos {id, ids}`; `albums.list` |
| `photo.virtualCopy` | `{ids?, name?}` | a second version with independent settings (B&W variant etc.) |
| `photo.setMeta` | `{ids?, title?, caption?, altText?, creator?, copyright?, keywords?}` | |
| `photo.inspect` | `{id?}` | file, size, format, metadata, settings |

### Develop
| Command | Params | Notes |
|---|---|---|
| `develop.set` | `{values: {controlId: number}, ids?}` or `{control, value}` | the main tool; ids below |
| `develop.merge` | `{settings: partial develop JSON, label?}` | whole groups at once (curves, grading, masks) |
| `develop.get` | `{id?}` | full settings JSON — save it as the look file |
| `develop.controls` | `{section?}` | every slider: range, default, current |
| `develop.wb` | `{mode: asShot\|auto\|daylight\|…\|custom, temp?, tint?}` | |
| `develop.wbPick` | `{x, y}` (normalized) | eyedropper on a neutral (cyc, white shirt) |
| `develop.auto` | `{}` | Auto tone — a starting point only |
| `develop.curve` | `{channel: master\|red\|green\|blue, points: [[x,y],…] 0..1}` | point curve |
| `curve.presets` / `curve.applyPreset {name}` / `curve.reset` | | |
| `develop.profile` | `{id, amount?: 0..200}` | `profiles.list` |
| `develop.treatment` | `{bw?: bool}` | B&W; `develop.autoBwMix` |
| `develop.targeted` | `{target: curve\|hue\|sat\|lum, x, y, delta}` | adjust the colour under a point (e.g. skin) |
| `pointColor.pick` | `{x, y}` | samples lum/chroma/hue at a point — a skin probe |
| `develop.reset` / `develop.resetSection {section}` / `develop.resetControl {control}` | | |
| `edit.undo` / `edit.redo`, `history.list`, `version.create {name}` | | |

### Develop control ids (`develop.set` values; ranges)
- White balance: `wb.temp` (K, 2000–50000; on JPEG/PNG relative to an as-shot 6500 → **higher = warmer**),
  `wb.tint` (−150…150, + = magenta).
- Light: `light.exposure` (−5…5 EV), `light.contrast`, `light.highlights`, `light.shadows`, `light.whites`,
  `light.blacks` (−100…100).
- Parametric curve: `curve.highlights`, `curve.lights`, `curve.darks`, `curve.shadows` (−100…100), splits
  `curve.splitShadows/Mid/Highlights`, `curve.refineSaturation` (0–100, default 100).
- Colour: `color.vibrance`, `color.saturation` (−100…100).
- Color Mixer (HSL): `mixer.<band>.hue|sat|lum` (−100…100), bands `red orange yellow green aqua blue purple magenta`.
  Skin lives mostly in **orange** (and red).
- Color Grading: `grading.shadows|midtones|highlights|global.hue` (0–360°), `.sat` (0–100), `.lum` (−100…100),
  `grading.blending` (0–100, def 50), `grading.balance` (−100…100). Warm ≈ hue 30–45°.
- Effects: `effects.texture`, `effects.clarity`, `effects.dehaze` (−100…100).
- Vignette: `vignette.amount` (−100…100), `.midpoint`, `.roundness`, `.feather`, `.highlights`.
- Grain: `grain.amount` (0–100), `grain.size` (def 25), `grain.roughness` (def 50).
- Detail: `detail.sharpenAmount` (0–150), `.sharpenRadius`, `.sharpenDetail`, `.sharpenMasking`, `detail.nrLuminance`,
  `detail.nrColor`.
- B&W mix: `bw.<band>`; calibration `calibration.*`; optics `optics.*`; geometry `geometry.*`; `crop.angle`.

### Presets, copy and sync
| Command | Params | Notes |
|---|---|---|
| `presets.list` | `{}` | built-ins (`lc.warm-glow`, `lc.warm-film`, `lc.soft-pastel`, `lc.faded-matte`, `lc.muted-film`, `lc.clean-studio`, `lc.bright-airy`, `lc.soft-skin`, `lc.golden-glow`, `lc.cinematic`, `lc.moody`, `lc.bw-soft`, `lc.bw-high-contrast`, `lc.bw-selenium`; 41 on 0.14, new ones incl. `lc.golden-hour`, `lc.moody-portrait`, `lc.warm-table`, `lc.bw-sepia`, `lc.bleach-bypass`) + user presets (`user.<n>.<slug>`) |
| `preset.apply` | `{id, amount?: 0..200, ids?}` | amount 100 = full |
| `preset.create` | `{name, group?, groups?: [settingsGroup]}` | from the active photo — save the hero look |
| `develop.copy` | `{groups?}` | default: all but crop, masks, remove |
| `develop.paste` | `{ids?, groups?}` | |
| `develop.sync` | `{groups?}` | active photo → all selected |
| `develop.quickAdjust` | `{control, delta, ids?}` | relative nudge on many photos |
| `develop.autoSync` | `{on?}` | edits follow to the selection |

Settings groups: `profile treatment whiteBalance light toneCurve color colorMixer colorGrading effects vignette grain
detail optics geometry crop masks spots redEye lensBlur calibration`.

### Crop
`crop.aspect {aspect: "16x9"|"4x5"|"1x1"|"original"|"free"|"current"|[w,h], orientation?: crop|given}`, `crop.set {rect: [x0,y0,x1,y1] normalized, angle?}`,
`crop.straighten {angle}`, `crop.autoStraighten`, `crop.reset`. MCP: `crop {rect, angle}`.
- **Aspect follows the photo's orientation:** `crop.aspect "4x5"` on a 1920×1080 frame gives a *landscape* 5:4
  (1350×1080). Add `crop.rotateAspect` for portrait 4:5 → 864×1080 (verified). **New 2026-10-27:** an `[w,h]`
  array is used as given, so `crop.aspect {"aspect":[4,5]}` is portrait 4:5 in one step (verified: 1200×900 → 720×900). `rect` is normalized per axis
  (x × width, y × height), so a portrait 4:5 from 16:9 is 0.45 wide: `[x0, 0, x0+0.45, 1]` — slide `x0` to frame the subject.
- A 1080-high frame can't make a 1080×1350 Instagram portrait without upscaling: export with `height:1350,
  dontEnlarge:false` (1.25×) and say so, or deliver 864×1080.

### Masks (local adjustments)
| Command | Params |
|---|---|
| `mask.add` | `{kind: radial, center:[x,y], rx, ry, angle?, feather?, name?}` · `{kind: linear, start:[x,y], end:[x,y]}` · `{kind: luminanceRange, lo, hi}` · `{kind: subject\|sky\|background}` · brush/colorRange/object/prompt |
| `mask.adjust` | `{id?, values: {exposure, contrast, highlights, shadows, whites, blacks, temp, tint, texture, clarity, dehaze, hue, saturation, sharpness, noise, amount}}` |
| `mask.addComponent` | `{id?, op: add\|subtract\|intersect, kind, …}` |
| `mask.invert` / `mask.delete` / `mask.select` / `mask.refine {value}` | |

Coordinates are normalized (0–1) image coordinates; radii relative to the long edge. Subject/sky are classical
heuristics, not AI (`object`/`prompt` need the 3.4 GB SAM 3 model — don't download without the user's OK).

### Export (`app.export`; MCP `export`)
`{path: out.jpg | dir, ids?, format?: jpeg|png|tiff|psd|webp|avif|jxl|dng|original, longEdge|shortEdge|width+height|megapixels|percent,
fit?: dimensions|widthHeight, dontEnlarge? (true), quality?: 1..100, colorSpace?: srgb|displayP3|adobeRgb|proPhoto|rec2020,
bitDepth?: 8|10|16|32 (TIFF defaults to 16, PNG to 8), tiffCompression?: none|lzw|zip,
ppi?, sharpen?: none|screen|matte|glossy, sharpenAmount?, metadata?: all|allExceptCamera|copyright|none,
removeLocation?, naming?, conflict?: unique|overwrite|skip, limitKb?, watermark?}` → `{files}`.
- No size param = **3000 px long edge**; `longEdge: 0` = full size. `width`+`height` fit inside the box.
- `conflict` defaults to `unique` (a new name, never overwrite) — keep it.
- Unknown keys are errors, not ignored. `export.presets` lists saved export presets.
- Verified 2026-10-27: `{path:"a.jpg", longEdge:0, quality:92}` and `{path:"a.tif", format:"tiff", bitDepth:16}`.

### New in 0.14 (2026-10-27, UNVERIFIED — check before relying on them)
`photo.removeRegion` (content-aware remove), `geometry.upright`, `denoise.*` (AI Denoise; needs a model download —
ask the user first), `develop.hdr {enabled, maxEv}` + export `hdr: true`, `merge.hdr` / `merge.panorama` /
`merge.hdrBatch` (also `lightcraft-cli merge …`), `library.importLightroom {path: .lrcat}`, `activity.list` /
`activity.cancel` (background tasks). `lightcraft-cli snapshot` renders the full app UI headless to PNG (no window).

## Verifying (look and measure)

- **Look:** export (or `render_photo`/`ui.render path`) and open the file with the Read tool. Check the pixel size in
  the export result.
- **Levels:** `contact.exe <sheet.jpg> range <image.png|jpg> 0 0.1 0.1` prints `levels: {y2, y50, y98, rgb}` for a
  still (Rec.709 luma percentiles 0–100 and mean RGB). Read whites from `y98`, blacks from `y2`, balance from `rgb`.
- **Skin / cyc in isolation (verified):** `render` the photo with the look *plus* a crop rect around the face (or a
  patch of cyc) merged into one settings JSON, to a small PNG, and measure that file with `contact.exe … range`. Also
  `pointColor.pick {x,y}` for lum/chroma/hue at a point (UNVERIFIED).
- **Histogram (verified, app only):** `node tools/craft.js lightcraft --ui ui.render '{"size":512}'` →
  `histogram: {r, g, b, luma: [256 bins], total}`. (Headless `run` has no histogram; use contact levels.)
- **Screenshot:** `--ui ui.screenshot '{"path":"C:/…/ui.png"}'` (1600×1000 window).
- **Side by side:** contact-sheet the exported set and compare levels across photos.

## Measured looks (DJI 0011 @25.2, white cyc, darker skin; 16-bit PNG frame)
| Look | Settings | Whole frame `rgb / y2 y50 y98` | Cyc patch RGB | Her face RGB / y50 |
|---|---|---|---|---|
| Untouched | — | 161/156/152 · 13 71 85 | 183/186/188 (slightly cool) | 130/101/84 · 36 |
| Warm (too warm) | temp 7300, tint 2, exp 0.1, contrast 12, hl −10, whites 8, blacks −12, vibrance 12, grading hl 40°/10, mid 35°/6, grain 8, vignette −8 | 169/154/139 · 12 71 84 | cream/beige | — |
| **Clean-warm** (recommended start) | `{"wb":{"mode":"custom","temp":6700,"tint":1},"light":{"exposure":0.05,"contrast":12,"whites":15,"blacks":-10},"color":{"vibrance":10},"grading":{"midtones":{"hue":35,"sat":8},"shadows":{"hue":30,"sat":4},"highlights":{"hue":45,"sat":3}},"grain":{"amount":6},"vignette":{"amount":-6}}` | 168/159/151 · 12 73 88 | 192/191/189 (neutral) | 134/100/80 · 35 (warmer, still dense) |

On rendered sources (PNG/JPEG) `wb.temp` is relative to an as-shot 6500 K: **+200 K is already visible**, +800 K turns a
white cyc cream. Setting `wb.temp`/`wb.tint` switches `wb.mode` to `custom` automatically.

## Gotchas
1. Bare `lightcraft.exe` opens the user's personal library — always `--library <project>/stills/library --no-demo` or `--memory`.
2. `file.exportFrame` (FilmCraft) ignores `seconds`: pass `time` in ticks.
3. Export without a size param gives 3000 px long edge (upscaled from 1920 only if `dontEnlarge:false`).
4. XMP writes go next to the original file — never on source folders.
5. A library is locked by the program that has it open; headless `--library` fails while the app has it.
6. Exports never overwrite by default (`-1`, `-2` suffixes): delete your own test exports or name versions.
7. `lightcraft-cli render`: only the last `--settings` file applies — merge look and crop into one JSON.
8. `crop.aspect` follows orientation: portrait from a landscape frame needs `crop.rotateAspect`.
9. `dontEnlarge` is on by default: asking for 1350 px from a 1080 px frame silently returns 1080 — check the
   `width`/`height` in the export result against the spec.
10. `app.export` with `dir` names files after the source (`a.png` → `a.jpg`); use `path` (one photo) for spec'd names.
11. In `--memory` app sessions the 24 demo photos are there too: always pass `ids` or select your imported id.
12. Commands from `node tools/craft.js` that return `null` (e.g. `develop.merge`, `crop.aspect`) succeeded.
