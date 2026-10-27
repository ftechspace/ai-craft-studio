# Driving PhotoCraft — operations manual

PhotoCraft is a Photoshop-class layered image editor (Rust; PSD/PSB read+write; 942 engine commands). Everything here
was **verified against PhotoCraft 0.6.0 on this machine (2026-10-10)** unless marked **UNVERIFIED**, and
**re-verified headless against 0.16.0 on 2026-10-27** (every command id below still exists; the §1 recipe, `convert`,
`batch`, `info`, `type.fonts`, MCP and the `auth` handshake re-run; what changed is marked "2026-10-27"). Paths are
relative to `C:\CodeHouse\AIFilmEditor\`.

## Binaries and setup

| What | Path |
|---|---|
| Desktop app | `apps\photocraft\target\release\photocraft.exe` |
| Headless CLI | `apps\photocraft\target\release\photocraft-cli.exe` (`help`, `<sub> --help`, `--version`) |
| Command registry with **param docs** | `photocraft-cli commands --filter <text>` or `--json` (fields `id,label,menu,params,shortcut,enabled`) |
| Source of truth when a param doc is unclear | `apps\photocraft\crates\engine\src\` (`commands.rs`, `layer_style.rs`, `*_cmds.rs`) |
| Settings / logs | `%APPDATA%\Photocraft\` (`preferences.json`, `logs\photocraft.log`) |
| Rebuild | `sh tools/build-apps.sh photocraft` (≈7 min incremental) |

Three ways in, from most to least file access:

| Way | File access | Use for |
|---|---|---|
| **CLI `run` / `convert` / `batch`** (trusted local) | any absolute path in any command | building deliverables, tests (≈1 s per build) |
| **MCP** (`photocraft-cli mcp`, headless or `--bridge`) / **`serve`** | only `doc_open`/`doc_save`/`doc_place` (headless) relative to `--automation-read-root` / `--automation-write-root` | an interactive session that keeps ids |
| **Control channel** of the desktop app (`--control`) | only `app.open`/`app.save`/`ui.screenshot` relative to the app's roots | building live while the user watches; showing a finished PSD |

In MCP, `serve` and the control channel, **every `file.*` command except `file.new`, `file.close*`, `file.fileInfo`,
`file.newFromClipboard`, `file.automate.fitImage`/`conditionalModeChange`, `file.scripts.flattenAll*`/
`deleteAllEmptyLayers`, `file.export.exportPreferences` is refused**, and so are path params elsewhere
(`layer.exportAs`, `layer.quickExportAsPng`, most `layer.smartObjects.*`, colour-lookup `file`, `image.mode.*` on
desktop): error `automation command `…` uses ambient filesystem paths and is disabled`. So no `file.placeEmbedded`,
`file.saveACopy` or `file.scripts.browse` there (verified).

## 1. Headless CLI — the workhorse (verified)

```sh
CLI=apps/photocraft/target/release/photocraft-cli.exe
$CLI run (<in-file> | --new '<file.new json>') --cmd <id> [--params '<json>'] [--cmd …] [--out <file>] [--quality 1-100]
$CLI convert <in> <out> [--quality 1-100]     # PSD → PNG etc.; warns "N layer(s) flattened" for flat formats
$CLI info <file> [--compact]                  # JSON: width/height/depth, layer tree (id, name, kind, bounds [x,y,w,h],
                                              #   effects, text {font,sizePt,text}, clipped), warnings (missing fonts)
$CLI batch --actions steps.json --in <dir> --out <dir> [--format jpg] [--quality 90]   # refuses --out == --in
```
2026-10-27: `run` and `convert` now also **refuse an output that is the input file** (exit 1; `--in-place` allows
it), like `batch` (verified). New output flags on all three: `--format <ext>`, `--jpeg-format
baseline|optimized|progressive`, `--tiff-layers`, `--tiff-compression`; `--quality` on WebP makes it lossy. New
subcommand `droplet` runs a saved droplet.
- `run` opens or creates **one** document, runs the commands in order (each `--params` belongs to the preceding
  `--cmd`), prints one JSON line per command (`{"command","result"}`), then writes `--out` (format from the
  extension: `.psd .psb .pcraft .png .jpg .tif .webp .exr …`). A failing `--cmd` stops with exit code 1.
- Commands default to the **active layer**, and every creating command (place, shape, type, adjustment, fill layer,
  paste) makes its new layer active — so `place → style → transform`, `type → style → transform` chain without ids.
- Layer ids are sequential per process: in a fresh `run --new`, the first layer ("Background" or the empty
  "Layer 1" of a transparent document) is **id 2** (still true 2026-10-27); later ids are in the results (they
  skip numbers — read them, don't count). A `layer` param now also takes a layer **name** (2026-10-27). Delete the empty layer with
  `layer.delete {"layer":2}` after something else exists (a document must keep ≥ 1 layer).
- **Use a step script** (no Windows quoting trouble, reproducible, easy v2):
  ```sh
  $CLI run --new '{"width":1280,"height":720,"background":"transparent","name":"Thumbnail"}' \
    --cmd file.scripts.browse --params '{"path":"C:/…/art/thumbnail.steps.txt"}' --out C:/…/art/thumbnail.png
  ```
  Script = one `command.id {json}` per line, `#` comments (or a JSON array of `[id, params]`). Result:
  `{"ok":bool,"steps":n,"results":[{"command","result"|"error"}…]}`. **The script stops at the first failing step but
  the CLI still exits 0 and still writes `--out`** — always check `"ok":true` (verified; re-verified 2026-10-27).
  2026-10-27: an **unknown command id** is now caught before anything runs: exit 1, nothing written. Steps can also be
  given inline: `file.scripts.browse {"steps":[["select.all",{}],…]}` or `{"script":"<text>"}` (verified).
- PSD + PNG in one run: last script step `file.saveACopy {"path":"C:/…/x.psd"}`, plus `--out C:/…/x.png`.
  (`file.saveACopy` JPEG `quality` is Photoshop's 0–12; the CLI `--quality` is 1–100.) Or `convert x.psd x.png`
  afterwards — re-rendering the saved PSD gave a pixel-identical PNG (verified).
- Phone-size check copy: `$CLI run x.png --cmd image.imageSize --params '{"width":320,"height":180}' --out x-320.png`.

### Verified recipe: printed photo on a transparent canvas (border, soft shadow, tilt, caption) — re-run unchanged 2026-10-27
```text
# art/print-01.steps.txt — run with --new '{"width":1280,"height":720,"background":"transparent"}'
shape.create {"kind":"rect","rect":[420,170,440,330],"fill":"#F5EFE6","name":"Paper"}
layer.layerStyle.dropShadow {"color":"#1B1612","opacity":45,"angle":120,"distance":14,"size":36}
edit.transform {"matrix":[0.99863,0.052336,-0.052336,0.99863,18.148,-33.043]}
layer.delete {"layer":2}
file.placeEmbedded {"path":"C:/CodeHouse/AIFilmEditor/output/story-work/full-136.44.png","scale":41.6667,"center":[640,302]}
layer.setProps {"name":"Photo"}
edit.transform {"matrix":[0.99863,0.052336,-0.052336,0.99863,18.148,-33.043]}
layer.newAdjustmentLayer.vibrance {"vibrance":12}
layer.createClippingMask {}
type.create {"x":640,"y":482,"text":"LOOK I · EARTH TONES","font":"Segoe UI","fontStyle":"Semibold","size":15,"color":"#1B1612","align":"center","tracking":250,"name":"Caption"}
edit.transform {"matrix":[0.99863,0.052336,-0.052336,0.99863,18.148,-33.043]}
file.saveACopy {"path":"C:/…/print-01.psd"}
```
The matrix rotates **+3° clockwise about (640, 330)**; giving every layer the same document-space matrix keeps them
aligned. The PSD reopens with Paper (shape + drop shadow), Photo (embedded smart object), Vibrance (clipped), Caption
(live type). Prefer a shape layer for a paper border: a `stroke` layer style with `position:"outside"` has **rounded
corners** (verified).

## 2. Control channel of the desktop app (authenticated; verified)

Launch with a port, a token file and file roots (one line; the roots are what `app.open`/`app.save`/`ui.screenshot`
may touch):
```sh
apps/photocraft/target/release/photocraft.exe --control 9871 --control-token-file C:/Users/<you>/AppData/Roaming/Photocraft/control.token --automation-read-root C:/CodeHouse/AIFilmEditor --automation-write-root C:/CodeHouse/AIFilmEditor/projects
```
Start it detached (e.g. Node `spawn(…, {detached:true, stdio:"ignore"}).unref()`); it prints
`photocraft: control server listening on 127.0.0.1:9871` on stderr after ~2 s.
- **Flags:** `--control <port>` (space-separated; env `PHOTOCRAFT_CONTROL_PORT`). `--control-token-file <path>`
  (env `PHOTOCRAFT_CONTROL_TOKEN_FILE`): created with a fresh 256-bit token (64 lowercase hex + newline) if missing,
  reused if present. Or `--control-token <64 hex>` (env `PHOTOCRAFT_CONTROL_TOKEN`; visible in the process list).
  Not both. With neither, the app makes a token and prints it **only to stderr**. Roots: `--automation-read-root`,
  `--automation-write-root` (envs `PHOTOCRAFT_AUTOMATION_READ_ROOT` / `_WRITE_ROOT`); without them file methods fail
  closed. Loopback only.
- **Handshake:** the first line on **every** TCP connection must be
  `{"id":"auth","method":"auth","params":{"token":"<64 hex>"}}` → `{"id":"auth","ok":true,"result":{"authenticated":true}}`.
  Anything else first, or a wrong token → `{"id":…,"ok":false,"error":"authentication required"}` and the server
  closes the connection. Then one JSON line per request `{"id","method","params"}` → `{"id","ok":true,"result"}` or
  `{"id","ok":false,"error":"…"}`. Limits: 60 s reply deadline, 30 s socket idle timeout, 1 MiB request, 8 MiB reply,
  16 connections.
- 2026-10-27 (0.16.0): flags, token file and handshake **unchanged**. Re-verified headless: `photocraft-cli serve
  --port 9881 --control-token-file %APPDATA%/Photocraft/control.token` speaks the same TCP `auth` protocol, and
  `craft.js connect("photocraft")` (with `PHOTOCRAFT_PORT=9881`) authenticated and ran commands; a non-`auth` first
  line got "authentication required" and the connection closed. (The desktop window itself wasn't launched.) A second
  `auth` on the same connection now gets "already authenticated" and the connection keeps serving.
- **`tools/craft.js` handles PhotoCraft (updated 2026-10-10, verified):** `--start` adds the token file
  (`%APPDATA%/Photocraft/control.token`) and the read/write roots (workspace / `projects/`); `connect()` sends `auth`
  first. So `node tools/craft.js photocraft --start` then `node tools/craft.js photocraft <command>` just work. The
  manual auth below is only needed if you start the app some other way:
  ```js
  const app = await require("C:/CodeHouse/AIFilmEditor/tools/craft").connect("photocraft");
  await app.call("auth", { token: require("fs").readFileSync(TOKEN_FILE, "utf8").trim() });
  await app.cmd("file.new", { width: 1280, height: 720, background: "transparent" });   // engine.execute
  await app.call("app.save", { path: "three-looks/art/x.psd" });                        // raw method
  ```
- **Methods:** `engine.execute {command, params, wait?}`, `engine.commands`, `app.open {path}` (→ `{name, path,
  warnings}`; opens as a new active document), `app.save {path?}` (format from the extension; without `path` only back
  to the document's own PSD/PSB/.pcraft), `ui.screenshot {path?}` (PNG of the window; path relative to the write root,
  else base64), `ui.inspect`, `ui.set {zoom, fit, tool, theme…}`, `ui.menu.invoke {id}`, `ui.dialog.*`, `ui.pointer`,
  `ui.key`, `ui.type`, `jobs.list`, `app.quit`. Session-level commands: `session.inspect` (open documents, active
  index), `document.activate {document}`, `file.close {document}`, `view.fitOnScreen`.
- **Bringing an image into a live document** (placeEmbedded is refused here; verified):
  `app.open {"path":"projects/three-looks/stills/x.jpg"}` → `select.all` → `edit.copy` → `document.activate
  {"document":0}` → `edit.paste {"center":[x,y]}` (pixel layer at 100%, centred there) →
  `layer.smartObjects.convertToSmartObject` → `edit.transform {"quad":[[x0,y0],[x1,y0],[x1,y1],[x0,y1]]}` to scale →
  `file.close {"document":1}` for the source. Then build as in §1 and `app.save`.
- **Simplest live review:** build headless (§1), then `app.open` the PSD in the app, `view.fitOnScreen`, screenshot.
- `app.save` to a flat format (`.png`) retitles the document to that file (the tab showed `live.png` after saving
  PSD then PNG). Save the PNG first and the PSD last, so the open document stays the PSD.
- **`app.quit` quits immediately without asking about unsaved documents** (verified) — save first, and ask the user
  before quitting if they may have their own unsaved work open.

## 3. MCP (headless and bridged; verified)

```jsonc
// .mcp.json — headless: own engine session, no window; doc_open/doc_save paths relative to the roots
"photocraft": {
  "command": "C:/CodeHouse/AIFilmEditor/apps/photocraft/target/release/photocraft-cli.exe",
  "args": ["mcp", "--automation-read-root", "C:/CodeHouse/AIFilmEditor", "--automation-write-root", "C:/CodeHouse/AIFilmEditor/projects"]
}
// bridge: forwards to the running app (§2); roots are the app's; the token file must already exist (start the app first)
"photocraft": {
  "command": "C:/CodeHouse/AIFilmEditor/apps/photocraft/target/release/photocraft-cli.exe",
  "args": ["mcp", "--bridge", "127.0.0.1:9871", "--control-token-file", "C:/Users/<you>/AppData/Roaming/Photocraft/control.token"]
}
```
**New 2026-10-27 (verified headless): `doc_place {path, scale?, center?, fit?}`** places a file from the read root as an
embedded smart object → `{layer, scale, bounds, smartObject}` — the MCP way to place (the bridge refuses it; there
use copy/paste as in §2). Also new: `doc_replace_smart_object {path, layer?}`, `doc_export_layers`,
`doc_export_data_sets` / `doc_import_data_sets`. `serve` has the same as `doc.place` etc.
Tools (both modes list all 26 as of 2026-10-27; 22 before): `command_list {filter?, enabled_only?}`, `command_run {id, params?, wait?}`,
`command_batch {steps:[{id,params}], stop_on_error}`, `doc_new`, `doc_open {path}`, `doc_save {path?}`,
`doc_export {path}`, `doc_inspect`, `doc_render_preview`/`render_preview {max_side?}` (headless: renders the document;
**bridge: a screenshot of the app window**), `doc_select`/`doc_close` (headless only), `jobs_list`, `jobs_cancel`,
`session_list`, and bridge-only `ui_inspect`, `ui_screenshot {max_side?}`, `ui_pointer`, `ui_menu_invoke`, `ui_set`,
`control_call {method, params}`. Same file policy as §2 (`file.placeEmbedded` → tool error, still 2026-10-27; headless use
`doc_place`, bridge `doc_open` + copy/paste).
The bridge needs `--control-token-file`/`--control-token` (or the env vars), else it refuses to start.

## 4. Commands for the photo-artist (ids + params)

Units: pixels; type `size` in **points** (= px at the default 72 ppi; at 300 ppi 1 pt = 4.17 px — keep 72 ppi for
screen work); colours `"#rrggbb"`; angles in degrees. `{"layer": id}` is optional almost everywhere (default: the
active layer). Every edit is one undo step (`edit.undo`). Look up anything else with `photocraft-cli commands --filter`.

### Documents and canvas
| Command | Params |
|---|---|
| `file.new` | `{"width","height","background":"white\|black\|transparent\|#rrggbb","resolution":72,"mode":"rgb","depth":8,"name"}` → `{document}` (index). `transparent` gives one empty "Layer 1" ✔ |
| `image.canvasSize` | `{"width","height","anchor":"center\|top\|topLeft…","extensionColor":"transparent\|white\|#rrggbb"}` |
| `image.imageSize` | `{"width","height","resample":"bicubic\|lanczos\|preserveDetails"}` ✔ |
| `image.crop` / `image.trim` | `{"x","y","width","height","angle"}` / `{"basedOn":"transparent"}` |
| `document.inspect` | `{}` → `layers[{id,name,kind:"Pixel\|Shape\|Type\|Smart Object\|Adjustment\|Group…",bounds:[x,y,w,h],effects,text,clipped,opacity,blend}]`, `history`, `activeLayer` ✔ |
| `document.pixel` | `{"x","y"}` → composite `[r,g,b,a]` in **0..1** (a = 0 → transparent) ✔ |
| `session.inspect` / `document.activate` | open documents / `{"document": index}` ✔ |

### Placing images
| Command | Params |
|---|---|
| `file.placeEmbedded` (CLI only) | `{"path": absolute,"scale": %,"center":[x,y],"fit":true}` → `{layer, scale, bounds:[x0,y0,x1,y1]}` — embedded **smart object** centred on `center` (default canvas centre). Without `scale` a larger image is fitted inside the canvas, a smaller one stays 100% — pass `scale` ✔ |
| `edit.copy` / `edit.copyMerged` → `edit.paste {"center"}` | engine clipboard, works across documents in one session ✔ |
| `layer.smartObjects.convertToSmartObject` / `.convertToLayers` / `.rasterize` | `{"layer"?}` (first one ✔) |

### Transform (scale / rotate / position)
| Command | Params |
|---|---|
| `edit.transform` | `{"matrix":[a,b,c,d,e,f]}` document-space affine applied on top (x' = a·x + c·y + e, y' = b·x + d·y + f) ✔, or `{"quad":[[x,y]×4]}` = where the content's bounding box corners go, clockwise from top-left ✔, or (new 2026-10-27, UNVERIFIED) relative `{"scaleX":%,"scaleY":%,"rotate":deg,"dx","dy"}` about the content's centre, as Free Transform. Smart objects, type and shapes stay live (re-rendered, no loss) |
| `layer.translate` | `{"dx","dy"}` (integers) |
| `edit.transform.flipHorizontal` / `.rotate90Cw` / … | `{}` |
Rotation by θ **clockwise on screen** about (cx, cy): `[cos θ, sin θ, −sin θ, cos θ, cx − cx·cos θ + cy·sin θ,
cy − cx·sin θ − cy·cos θ]`; negative θ tilts counter-clockwise. Scale s about (cx, cy): `[s,0,0,s,cx(1−s),cy(1−s)]`.

### Layers, blend modes, masks
| Command | Params |
|---|---|
| `layer.new.layer` / `layer.new.group` | `{"name"}` → `{layer}` ✔ |
| `layer.setProps` | `{"layer","name","visible","opacity":0..1,"fill":0..1,"blend":"multiply\|screen\|overlay\|soft light\|…","clipped","locked"}` ✔ — **opacity 0..1 here**, 0..100 in layer styles |
| `layer.select` | `{"layer","mode":"replace\|toggle\|range\|add"}` · `layer.groupLayers {"name"}` groups the selected layers |
| `layer.duplicate` / `layer.delete` ✔ / `layer.moveTo {"layer","target","position":"above\|below\|into"}` / `layer.arrange.bringToFront` | |
| `layer.createClippingMask` ✔ / `layer.releaseClippingMask` | `{"layer"?}` |
| `layer.layerMask.revealAll` / `hideAll` / `revealSelection` / `hideSelection` / `fromTransparency` / `apply` / `delete` | `{"layer"?}`; paint the mask with `paint.stroke {…,"target":"mask"}` |
| `layer.stampVisible` / `layer.mergeDown` / `layer.flattenImage` | |
Blend names are case/space-insensitive (`"Soft Light"` = `softLight`).

### Fills, shapes, gradients, selections
| Command | Params |
|---|---|
| `shape.create` | `{"kind":"rect\|roundedRect\|ellipse\|polygon\|star\|line","rect":[x,y,w,h],"radii":r,"fill":"#hex"\|{"gradient":{…}}\|null,"stroke":{"width","color","align":"inside\|center\|outside"}\|null,"name"}` → live shape layer ✔ |
| `layer.newFillLayer.solidColor` / `.gradient` | `{"color"}` / `{"from","to","angle":90,"style":"linear\|radial"}` (masked by the selection, if any) |
| `paint.gradient` | `{"from":[x,y],"to":[x,y],"style","stops":[[t,"#hex"]…],"transparency":[[t,0..100]…],"opacity","mode"}` (pixel layer) — e.g. a darkening ramp under a headline |
| `edit.fill` | `{"contents":"color\|foreground\|contentAware\|pattern","color","mode","opacity":0..100}` |
| `select.rect` | `{"x","y","width","height","ellipse","feather","mode"}` · `select.all` ✔ · `select.deselect` · `select.inverse` · `select.modify.feather {"radius"}` · `select.subject` · `select.colorRange` · `select.refineEdge` |
| `tools.setColors` | `{"foreground","background"}` |

### Layer styles (one effect of each kind per layer; `"add":true` adds a second)
| Command | Params (Photoshop units) |
|---|---|
| `layer.layerStyle.dropShadow` ✔ | `{"color","opacity":0..100=75,"blend":"multiply","angle":120,"useGlobalLight","distance":5,"spread":0..100,"size":5,"noise","layer"}` |
| `layer.layerStyle.stroke` ✔ | `{"size":3,"position":"outside\|inside\|center","color","opacity","blend"}` (gradient: `from`,`to`,`style`,`angle`); outside strokes get round corners |
| `outerGlow` / `innerGlow` / `innerShadow` / `colorOverlay` / `gradientOverlay` / `patternOverlay` / `satin` / `bevelEmboss` | `photocraft-cli commands --filter layerStyle` |
| `layer.layerStyle.replace` / `.clear` | `{"layer","effects":[{"kind","params"}…]}` / `{"layer"}` |

### Type
| Command | Params |
|---|---|
| `type.create` ✔ | `{"x","y" (baseline),"text","align":"left\|center\|right" (center centres on x),"font":"Family","fontStyle":"Bold","weight","size":pt,"color","tracking":1/1000 em,"leading","caps":"all","box":[x,y,w,h]? (paragraph text),"name"}` → `{layer, bounds}` |
| `type.setStyle` | `{"layer","range":[start,end]?, …character keys…, "align"}` (e.g. one word in the accent colour) |
| `type.edit` | `{"layer","text"?,"move":[dx,dy]?,"transform":[a,b,c,d,e,f]?}` |
| `type.fonts` ✔ | `{}` → `{families}`; `{"family":"Segoe UI"}` → `{faces:[{family, style, weight, italic, postscriptName, axes}]}` — use the exact `style` (Regular, Semibold, Semilight, …) as `fontStyle` (re-verified 2026-10-27) |
Fonts: bundled Inter (Regular/Medium/SemiBold) + JetBrains Mono, plus everything installed in `C:\Windows\Fonts` and
`%LOCALAPPDATA%\Microsoft\Windows\Fonts`. A missing family falls back to Inter in the pixels; the CLI prints
`warning: font '…' is not installed` and `info` lists it — check, never assume. Since 2026-10-27 the `type.create`
result also carries `"warnings":[…]` (so MCP/script runs see it). PSDs keep live type.

### Adjustments (layers = non-destructive; `image.adjustments.*` = baked into the active pixel layer)
`layer.newAdjustmentLayer.<kind>` ✔ (vibrance, curves) / `image.adjustments.<kind>`; edit later with
`layer.setAdjustment {"layer", …}`; restrict to one layer with `layer.createClippingMask` ✔. Kinds:
`brightnessContrast {brightness,contrast}`, `levels {inBlack,gamma,inWhite,outBlack,outWhite,red/green/blue:{…}}`,
`curves {points:[[in,out]…] 0..255, red/green/blue}`, `exposure`, `vibrance {vibrance,saturation}`,
`hueSaturation {hue,saturation,lightness,colorize}`, `colorBalance {shadows,midtones,highlights:[c-r,m-g,y-b]}`,
`blackWhite`, `photoFilter {filter:"warming85…",density}`, `channelMixer`, `gradientMap {stops}`, `selectiveColor`,
`colorLookup {lut:"warm|cool|fadedFilm|…"}`, `invert`, `posterize`, `threshold`. Also `image.autoTone`,
`image.adjustments.shadowsHighlights`.

### Retouching and filters
- Brush tools take `{"points":[[x,y,pressure?]…],"size","hardness":0..100,"opacity":1..100,"layer"?,"sampleAllLayers"}`:
  `paint.spotHealing {…,"type":"contentAware"}` ✔ (runs on an empty layer with `sampleAllLayers:true`; aim
  carefully — measure the defect's position on a full-size render first), `paint.healingBrush` / `paint.cloneStamp
  {…,"source":[sx,sy] | "offset":[dx,dy],"sampleLayer":"all"}`, `paint.dodge` / `paint.burn {…,"range","exposure"}`,
  `paint.patch`, `paint.redEye` — **UNVERIFIED** except spot healing.
- Area: `edit.contentAwareFill` on a selection, `paint.contentAwareMove` — UNVERIFIED.
- Filters: `filter.blur.gaussianBlur {radius}`, `filter.sharpen.unsharpMask {amount,radius,threshold}` ✔ (in batch),
  `filter.noise.addNoise {amount,distribution,monochromatic}`, `filter.noise.dustAndScratches`, `filter.other.highPass`,
  `filter.render.relight`. On a smart object they become editable smart filters.
- `filter.liquify`, `edit.puppetWarp`, `edit.transform.warp` exist; the photo-artist never uses them to reshape
  people (warping a flag or paper curl is fine).

### Saving and exporting
| Where | How |
|---|---|
| CLI | `--out x.psd/.png/.jpg` ✔, `convert` ✔, script step `file.saveACopy {"path","quality":0..12}` ✔, `batch --format jpg --quality 90` ✔ |
| MCP / serve / control | `doc_save {path}` ✔ / `doc.save {path,format?,quality?}` / `app.save {path}` ✔ — relative to the write root |
PNG keeps transparency (verified: corner alpha 0, shadow alpha ≈ 0.05). JPEG composites over **white** (warning
printed). Flat exports warn `N layer(s) flattened`. PSD keeps shapes, smart objects, live type, effects, clipped
adjustment layers (verified by reopening). Overwrites existing files without asking.

## 5. Verify what you made
1. `photocraft-cli info x.psd --compact` — size, layer kinds/names/bounds, effects, fonts, warnings.
2. Render and **look**: `convert x.psd x.png`, Read it at full size; then a 320×180 (and 168×94) copy for thumbnails.
3. Numbers: `document.pixel {"x","y"}` for exact colours / transparency.
4. Live: `ui.screenshot {"path":"…"}` (after `view.fitOnScreen`) shows what the user sees.

## 6. Pitfalls
1. MCP / serve / control channel refuse path-taking commands — place and save through the CLI, headless MCP
   `doc_place`/`doc_save` (2026-10-27), or in the live app `app.open` + copy/paste and `app.save`.
2. `file.scripts.browse` stops at a failing step, but the CLI exits 0 and still writes `--out`: check `"ok"`.
3. Opacity: `layer.setProps` 0..1, layer styles 0..100. JPEG quality: `file.saveACopy` 0–12, CLI 1–100.
4. `document.inspect` bounds are `[x,y,w,h]`; `file.placeEmbedded` returns `bounds` as `[x0,y0,x1,y1]`.
5. Type size is in points; a 300-ppi document makes text ≈ 4× bigger than the same number at 72 ppi.
6. Missing fonts silently fall back to Inter in the image — read the warnings.
7. `doc_render_preview` in bridge mode is a window screenshot, not the document.
8. `app.quit` doesn't ask about unsaved work. `app.save` to PNG retitles the open document.
9. Everything overwrites silently — `ls` before every save; new versions get new names. (Exception since
   2026-10-27: `run`/`convert`/`batch` refuse to overwrite their own input without `--in-place`.)
10. A layer-style `stroke` outside has rounded corners; use a shape layer for crisp paper borders.
