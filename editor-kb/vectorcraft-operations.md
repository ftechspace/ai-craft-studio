# Driving VectorCraft — operations manual

VectorCraft 0.8.0 is an Illustrator-class vector app (Rust, `apps/vectorcraft/`). Every user-visible action is an
engine **command** (`id` + JSON params); the CLI, the control channel and MCP all run the same commands.
Paths are relative to `C:\CodeHouse\AIFilmEditor\`. Everything here was run on this machine on 2026-10-10 unless
marked **UNVERIFIED** (taken from the app's docs/source only).

## Binaries and setup

| What | Path |
|---|---|
| Desktop app | `apps\vectorcraft\target\release\vectorcraft.exe [--control <port>] [files…]` |
| Headless CLI / MCP server | `apps\vectorcraft\target\release\vectorcraft-cli.exe` (`help` lists subcommands and every readable/writable format) |
| Control client (shared) | `node tools\craft.js vectorcraft …` (port **9874**) |
| Command catalogue | `vectorcraft-cli commands` → JSON array of 701 `{id, label, menu, params, shortcut, enabled}`; `params` is a prose doc and **is the reference** — grep it before guessing a parameter |
| App docs | `apps\vectorcraft\docs\mcp.md` (commands by topic), `docs\control-protocol.md` (control methods, dialogs) |

Rebuild after `git pull`: `sh tools/build-apps.sh vectorcraft` (≈8 min; log `output/build-logs/vectorcraft.log`).

## Units and coordinates
- Points (1 pt = 1 px at 72 ppi; `units: "Pixels"` only changes what the UI shows). y points **down**, origin =
  top-left of the first artboard. `file.new` with no size = 612×792 (US Letter).
- New objects become the selection; commands without `ids` act on the selection.
- Bounds come back as `{x, y, width, height}` (`document.inspect`) or `[x, y, w, h]` (`cli info`, `exportSelection`).
- Colours: `"#rrggbb"`, `[r,g,b]` 0..1, `{c,m,y,k}`, `{gray}`, `{l,a,b}`, or `{swatch: "name"}`; none = `{none: true}`.
- Raster size = artboard pt × `scale` (or × `ppi/72`; `ppi` wins over `scale`). 1920-pt artboard at `scale: 2` = 3840 px.

## Three ways to drive it

### 1. Headless MCP script (default for real work: no window, ids flow between steps)
`vectorcraft-cli mcp --headless` speaks JSON-RPC on stdio. This Node helper (verified) runs any command and returns
its parsed result, so later steps can use earlier ids:
```js
// vc.js — const { run, done } = require("./vc"); …; done();
const { spawn } = require("child_process");
const p = spawn("C:/CodeHouse/AIFilmEditor/apps/vectorcraft/target/release/vectorcraft-cli.exe", ["mcp", "--headless"]);
let buf = "", n = 0; const wait = new Map();
p.stdout.on("data", d => { buf += d; let i; while ((i = buf.indexOf("\n")) >= 0) { const m = JSON.parse(buf.slice(0, i)); buf = buf.slice(i + 1); wait.get(m.id)?.(m); } });
const rpc = (method, params) => new Promise(r => { const id = ++n; wait.set(id, r); p.stdin.write(JSON.stringify({ jsonrpc: "2.0", id, method, params }) + "\n"); });
const ready = rpc("initialize", { protocolVersion: "2025-06-18", capabilities: {}, clientInfo: { name: "vc", version: "0" } });
async function run(id, params = {}) {
  await ready;
  const m = await rpc("tools/call", { name: "command_run", arguments: { id, params } });
  const t = m.result?.content?.[0]?.text;
  if (m.error || m.result?.isError) throw new Error(`${id}: ${t || JSON.stringify(m.error)}`);
  try { return JSON.parse(t); } catch { return t; }
}
module.exports = { run, rpc, done: () => p.stdin.end() };
```
Usage: `const { id } = await run("shape.rectangle", {...}); await run("paint.setFill", { ids: [id], color: "#D08C5B" });`
Put scripts in the scratchpad or `output/`, not in the project folder. `rpc("tools/call", {name: "render_preview",
arguments: {max_side: 512}})` returns an inline PNG (base64) of artboard 1.

### 2. Headless batch CLI (quick one-liners)
```sh
vectorcraft-cli run [--in FILE] --cmd ID [--params JSON] … [--export FILE]… [--scale N]
```
New document (or opens `--in`), runs each `--cmd` in order, `--export`s by extension, prints one JSON line per step,
stops non-zero at the first failure. `--params` belongs to the `--cmd` before it. Ids can't flow between steps (rely on
"new object = selection"). **`--export x.svg` keeps live `<text>`**; for delivery use
`--cmd document.export --params '{"path":"…svg","outlineText":true}'` and for PNG options
`--cmd document.export --params '{"path":"…png","scale":2,"background":"transparent"}'`.
On Git Bash pass Windows paths (`$(pwd -W)`) inside JSON.

### 3. Live app + control channel (the user watches)
```sh
node tools/craft.js vectorcraft --start [file.vectorcraft]   # vectorcraft.exe --control 9874 (window opens ~2 s later)
node tools/craft.js vectorcraft <command.id> '<json>'        # engine.execute; prints result JSON
node tools/craft.js vectorcraft --ui <method> '<json>'       # raw control methods
```
Protocol (`apps/vectorcraft/src/control_server.rs`): JSON lines on `127.0.0.1:9874`, `{id, method, params}` →
`{id, ok: true, result}` / `{id, ok: false, error}` — exactly what `craft.js` speaks. No auth token. A malformed line
gets an error and **closes the connection**. The app's own default port is 7979; always go through `craft.js` (9874).
Before the first document exists, document commands fail with "no document open" — that also proves the port is up.

| Control method | Use (all verified unless noted) |
|---|---|
| `engine.execute {command, params}` | any command (what `craft.js <id>` sends) |
| `document.inspect {depth?, childLimit?}` | layer tree: ids, kinds, names, bounds, fill/stroke, text; selection; history |
| `ui.render {path, scale?}` | **first artboard only**, rendered without UI chrome (works with a locked screen) |
| `ui.screenshot {path}` | the window as the user sees it (fails after ~8 s if the screen is locked/window covered) |
| `app.save {path}` / `app.export {path, scale?, background?, format?}` | write through the app **in the background**: returns `{background: true, status}` at once; wait until `ui.inspect` → `background` is `[]` before using the file. `engine.execute document.export` is synchronous — prefer it |
| `app.open {path}` | open any readable file as a new tab |
| `app.quit` | with unsaved changes opens a `saveChanges` dialog: `--ui ui.dialog.set '{"field":"discard","value":true}'` then `--ui ui.dialog.confirm` (or confirm alone to save) |
| `ui.inspect` | documents (dirty), tool, open `dialog`, background jobs, perf |
| `ui.menu.list`, `ui.tool.select`, `ui.pointer`, `ui.key`, `ui.dialog.*` | UI driving (UNVERIFIED here) |
In the app, many menu commands open a dialog when called **without params** (`file.new`, `object.expand`,
`file.export.svg`…): always pass params.

### MCP config
| Mode | Command | Notes |
|---|---|---|
| Headless | `vectorcraft-cli mcp --headless` | engine + CPU renderer; UI tools error |
| Bridged | `vectorcraft-cli mcp --connect 127.0.0.1:9874` | app must run with `--control 9874`; verified: `draw_shape` appeared in the live window, `ui_inspect` and `doc_inspect` answered |
| (no flag) | tries 127.0.0.1:7979, else headless | don't use: wrong port here |
Tools: `command_run {id, params}`, `command_batch {steps:[{id,params}], stop_on_error}`, `command_list {filter}`,
`doc_inspect`, `render_preview {max_side}`, `ui_inspect`, `ui_screenshot`, and the older `draw_shape`, `draw_path`,
`add_text`, `set_paint`, `pathfinder`, `transform`, `export`, `save_file`, `open_file`, `screenshot`,
`inspect_document`, `undo`/`redo`.

## Core commands

### Document, artboards, layers
| Command | Params | Notes |
|---|---|---|
| `file.new` | `{width, height, units?: "Pixels", name?}` | → `{index}`; also `artboards`, `backgroundContents: "transparent"`, `colorMode` |
| `artboard.new` | `{x, y, width, height, name}` | → `{index}` (0-based). One artboard per colour variant, 100+ pt apart |
| `artboard.setProps` | `{index, name?, x?, y?, width?, height?}` | |
| `artboard.fitToArt` / `fitToSelection` | `{index?}` | hugs the art exactly — add clear space yourself (UNVERIFIED) |
| `layer.new` / `layer.setProps` / `layer.setCurrent` | `{name}` / `{id, name, locked, visible}` / `{id}` | new art goes to the current layer (UNVERIFIED) |
| `object.setProps` | `{ids, name?, opacity?, blend?, visible?, locked?}` | verified: `name` becomes the SVG `id` (`id="frame-1"`) — name parts for the motion-designer |
| `document.node` | `{id, summary: true}` | one object (bounds, paint) |

### Shapes and paths
| Command | Params |
|---|---|
| `shape.rectangle` | `{x, y, width, height, radius?, rotation?}` → `{id}`; `radius` makes a live rounded rectangle (verified) |
| `shape.ellipse` | `{x, y, width, height}` (verified) |
| `shape.polygon` / `shape.star` / `shape.line` | `{cx, cy, radius, sides}` / `{cx, cy, radius1, radius2, points}` / `{x1, y1, x2, y2}` |
| `path.create` | `{anchors: [{x, y, in?: [x,y], out?: [x,y]}], closed}` or `{d: "M… C… Z"}` (UNVERIFIED) |
| `object.setLiveShape` | `{ids, radius, kind: round\|invertedRound\|chamfer, corners?: [0..3]}` (UNVERIFIED) |
| `object.expandShape` | live shapes → plain paths |
| `object.path.offsetPath` | `{offset, joins}` (negative insets) (UNVERIFIED) |
| `object.path.outlineStroke` | strokes → filled outlines → `{ids}` (verified) |
| `object.compoundPath.make` / `.release` | |

### Pathfinder (on the selection, back → front)
`object.pathfinder.unite | minusFront | minusBack | intersect | exclude | divide | trim | merge | crop | outline` → `{ids}`.
`select.set {ids}` the operands first. Verified: unite of two ellipses → one compound shape. `divide` splits overlaps
into separate pieces (for colouring overlap areas; UNVERIFIED). Shape Builder: `shapeBuilder.merge {ids, points}`.

### Paint, strokes, swatches
| Command | Params |
|---|---|
| `paint.setFill` / `paint.setStroke` | `{ids?, color}`, `{none: true}`, `{swatch}`, `{gradient: {kind: linear\|radial, angle, stops: [{offset, color, opacity?}]}}` — result `null` on success |
| `stroke.set` | `{weight, cap, join, align: center\|inside\|outside, dash?}` — acts on the **selection** (no `ids`): `select.set` first (verified) |
| `transparency.set` | `{ids, opacity 0..100, blend: "Multiply"…}` |
| `swatch.new` | `{name, color, global: true}`; `swatch.edit {name, color}` recolours linked art (UNVERIFIED) |
**Paint commands also set the default for the next object.** Verified: two ellipses drawn after a 12 pt coral stroke
came out with a 12 pt coral stroke. Set fill **and** stroke explicitly on every new object (or `paint.default`).

### Type
| Command | Params |
|---|---|
| `text.fontList` | `{}` → `{families}`; `{family}` → `{styles}` (error if missing) |
| `text.create` | `{x, y, text, size, font, style?, color?}` → `{id}`. **`y` is the baseline**, `x` the left edge. Area type: `area: {width, height}` |
| `text.setStyle` | `{ids?, font?, style?, size?, leading?, tracking (1/1000 em), justify: left\|center\|right, fill?, features?}` |
| `text.setRangeStyle` | `{id, start, end (byte offsets), kerning (1/1000 em), tracking?, fill?, size?, baselineShift?}` — per-pair kerning: runs on the first glyph of the pair (verified it applies and splits runs; judge the gap by eye) |
| `text.setFormat` | `{ids, kerning: "auto"\|n, allCaps?, smallCaps?}` |
| `text.setText` / `type.changeCase` | `{ids, text}` / `{case}` |
| `type.createOutlines` | selection → group of compound paths → `{ids}` (verified). Keep a live-text master; outline a copy |

### Arrange, align, group, transform
| Command | Params |
|---|---|
| `select.set {ids}` → `{count, ids}` / `select.all` / `select.none` | |
| `object.align` | `{horizontal: left\|center\|right, vertical: top\|center\|bottom, to: selection\|artboard\|key, bounds: geometric\|preview}` (verified `to: "artboard"` on a one-artboard document; with several artboards check which one it uses) |
| `object.distribute` / `object.distributeSpacing` | `{horizontal…}` / `{axis, spacing}` (UNVERIFIED) |
| `object.group` → `{id}` / `object.ungroup` | verified |
| `object.move {dx, dy, copy?}` / `object.rotate {angle (CCW), origin?}` / `object.scale {sx, sy?, strokes?}` / `object.reflect {axis}` | |
| `object.arrange.sendToBack` / `bringToFront` / `bringForward` / `sendBackward` | verified (sendToBack) |
| `edit.duplicate {dx?, dy?}` → `{ids}` / `edit.clear {ids?}` / `edit.undo` → `{undone}` | verified |
| `object.clippingMask.make` | top selected path clips the rest |

### Save and export (all synchronous in headless and via `engine.execute`)
| Command | Params | Notes |
|---|---|---|
| `document.save` | `{path: "…/x.vectorcraft"}` | native master (JSON). The document takes this path |
| `file.saveCopy` | `{path}` | copy; document keeps its path |
| `document.export` PNG | `{path, artboard?: 0-based, scale? \| ppi?, background: transparent\|white\|black\|"#hex", antiAlias: art\|type\|none}` | verified: RGBA with transparent pixels where there's no art; **art covering the whole artboard is written as RGB** (no alpha channel) |
| `document.export` SVG | `{path, artboard?, outlineText: true, decimals?, styling?, embedFonts?}` | verified: `outlineText` leaves no `<text>`; colours as lowercase hex; coordinates relative to the chosen artboard; only that artboard's art |
| `document.exportPdf` | `{path, range?: "1-3"}` | one page per artboard (verified it writes) |
| `document.exportSelection` | `{path, format?, scale}` | selected objects cropped to bounds incl. stroke (verified) |
| `document.exportForScreens` | `{folder, artboards?, formats: [{format, scale: "2x"\|"3840w", suffix}]}` | batch sizes — **UNVERIFIED** |

## Recipes (verified)
- Transparent 3840-px PNG of a 1920-pt artboard 0:
  `document.export {"path":"…/lockup-light-3840.png","artboard":0,"scale":2,"background":"transparent"}`
- Delivery SVG: `document.export {"path":"…/lockup-light.svg","artboard":0,"outlineText":true}`
- Thumbnail test (~64 px wide): `scale: 64 / artboardWidth`, `background: "#F5EFE6"` (or the ink hex) and Read it.
- Light-on-dark preview without baking a background into the art: export with `background: "#1B1612"` to a
  `-preview.png`; deliver the transparent one.
- Check a PNG's size and alpha (no Python here):
  ```sh
  node -e "const b=require('fs').readFileSync(process.argv[1]);console.log(b.readUInt32BE(16),'x',b.readUInt32BE(20),'colorType',b[25],'(6=RGBA, 2=RGB)')" file.png
  ```
- Summary of a saved file: `vectorcraft-cli info file.vectorcraft` (artboards, object counts by kind, fonts used).

## Fonts available here (verified with `text.fontList` and a rendered sample sheet)
- **Bundled (OFL, in every VectorCraft build):** Inter (Regular, Medium, SemiBold), Source Sans 3 (Regular, Italic,
  Semibold, Bold), Source Serif 4 (Regular only), JetBrains Mono (Regular).
- **Windows 11 installed:** Sitka (variable; styles = optical sizes Small, Text, Subheading, Heading, Display,
  Banner, each also Semibold, Bold, Italic), Palatino Linotype, Georgia, Cambria, Constantia, Times New Roman,
  Segoe UI Variable (Display/Text/Small optical sizes, Light→Bold), Bahnschrift, Arial, Calibri, Candara, Corbel,
  Franklin Gothic Medium, Gabriola, Trebuchet MS, Verdana, Roboto, Tahoma, plus user-installed fonts.
- **No true Didone** (Bodoni/Didot class) is installed. The highest-contrast serif available is **Sitka, style
  "Banner"** (`font: "Sitka", style: "Banner"`): sharp, fine hairlines, elegant in tracked caps; "Display" is a
  touch heavier. Source Serif 4 and Georgia are lower-contrast text faces.
- Clean sans: **Inter** (bundled here and the face FilmCraft's text styles use), Medium/SemiBold for labels.
- Sitka and Segoe are Microsoft fonts licensed with Windows: fine to use and to outline into artwork; don't embed or
  ship the font files (`embedFonts`) — deliver outlined SVG/PNG so other apps don't need them.
- No craft-fonts (Japanese/Arabic): `tools/build-apps.sh` doesn't set `CRAFT_FONTS_DIR`.

## Verify what you made
- **Look**: export PNG and Read it — full size, a ~64 px version, and on paper and ink backgrounds. In the live app,
  `ui.screenshot` shows what the user sees; `ui.render` shows artboard 1 only.
- **Inspect**: `document.inspect` (ids, names, kinds, bounds, paint, text); grep delivery SVGs for `<text` (must be 0)
  and the palette hexes (`#d08c5b`…).
- **Files**: PNG size/alpha with the `node -e` check above; `vectorcraft-cli info` for masters.

## Gotchas
1. Paint commands set the default for new art — set fill and stroke on every object.
2. `stroke.set` has no `ids`: select first.
3. `y` in `text.create` is the baseline.
4. CLI `--export x.svg` keeps live text; use `document.export` with `outlineText: true`.
5. Exports overwrite silently — `ls` first, version the names.
6. Fully opaque art exports as RGB PNG even with `background: "transparent"` (correct, just no alpha channel).
7. In the GUI, `app.save`/`app.export` run in the background; `engine.execute document.save/export` don't.
8. `ui.render` = artboard 1 only; for other artboards use `document.export {artboard}`.
9. A malformed control line closes the connection; the app's built-in default port 7979 is shared by sibling apps.
10. `app.quit` with unsaved work waits on a `saveChanges` dialog (see above) — ask the user before discarding theirs.
