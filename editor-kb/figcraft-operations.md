# Driving FigCraft — operations manual

FigCraft 0.11.2 is an open-source Figma-class interface design and prototyping app (Rust, `apps/figcraft/`): frames,
auto layout, components and variants, styles and variables, prototypes, Dev Mode. Every user-visible action is an
engine **command** (`id` + JSON params) from one registry (615 in this build); the menus, the CLI, the control channel and the MCP
server all run the same commands. Paths are relative to `C:\CodeHouse\AIFilmEditor\`.
Status tags: **VERIFIED** = run on this machine (see "Verification log" at the end); everything else is taken from
the app's docs/source and is **UNVERIFIED** until someone runs it. Verified on 2026-10-26.

## Binaries and setup

| What | Path |
|---|---|
| Desktop app | `apps\figcraft\target\release\figcraft.exe [--control <port>] [--automation-read-root DIR]… [--automation-write-root DIR]… [file]` |
| Headless CLI / MCP server | `apps\figcraft\target\release\figcraft-cli.exe` (`info`, `export`, `convert`, `render`, `run`, `commands`, `mcp`, `perf`) |
| Control client (shared) | `node tools\craft.js figcraft …` (port **9878**) |
| Command catalogue | `figcraft-cli commands --json [--filter TEXT]` → `{id, label, menu, params, shortcut, undoable}`; `params` is a prose doc and **is the reference**: grep it before guessing |
| App docs | `apps\figcraft\docs\mcp.md` (the real manual: conventions, every topic), `control-protocol.md`, `cli.md`, `prototyping-parity.md`, `components-parity.md`, `gaps.md` (what's missing) |

Rebuild after `git pull`: `sh tools/build-apps.sh figcraft` (log `output/build-logs/figcraft.log`). Note: the
script's default app list doesn't include figcraft — name it explicitly.

## Units, coordinates, conventions
- Page units = px at 100 %. x right, **y down**. `x`/`y` in `node.create`/`node.set` are **relative to the parent
  frame** (the page when none); `absoluteBounds` in inspect results are page coordinates. Groups have no coordinate
  space of their own.
- New layers become the selection; commands without `ids` act on the selection. Every mutation is one undo step;
  a failing command changes nothing. **Programmatic calls never open dialogs.**
- Colours `"#RRGGBB"` / `"#RRGGBBAA"`. `fill`/`stroke` take a colour or `"none"`; `fills`/`strokes` take lists of
  colours or paints; gradient shorthand `{"type":"linearGradient","stops":["#hex","#hex"],"from":[x,y],"to":[x,y]}`
  (points in the layer's 0–1 box; also `radialGradient`, `angularGradient`, `diamondGradient`).
- Ids are integers assigned in order: a new document's first page is 1, so the first layer is 2.
- Text props: `fontFamily`, `fontStyle` ("Regular", "SemiBold", "Bold"…), `fontSize`, `lineHeight` (`auto`, px,
  `"120%"`), `letterSpacing` (px or `"2%"`), `textAlign`, `textAutoResize` (`widthAndHeight|height|none|truncate`),
  `textCase`, `fills` (text colour), `maxLines`, `fontVariations {"wght": 550}`, `features {"tnum": true}`. With
  `start`/`end` they style a character range.
- Full `node.set` key list: `figcraft-cli commands --filter node.set` (or `crates/engine/src/cmd/props.rs` `KEYS`).

## Four ways to drive it

### 1. `figcraft-cli run` — scripts (default for real work)
```sh
figcraft-cli run build.json [--in start.figcraft] --out result.figcraft
```
A JSON array of `{"command", "params", "as"?}` (or JSON lines). The whole script is **one undo step and
all-or-nothing**: a failing step prints `{"step":n,"ok":false,"error":…,"rolledBack":true}`, writes nothing, exits 1.
**Step references:** name a step with `"as": "card"`; `{"$ref": "card"}` anywhere in a later step's params is that
step's result `id` (`{"$ref":"copy","field":"ids/0"}` for another key/path; `{"$step": n}` by position). So a script
never has to guess ids. `--out` saves by extension (`.figcraft`, `.svg`, `.png`, `.pdf`, `.fig`, `.json`).
Then export from the saved file with `figcraft-cli export` (below).

### 2. Headless MCP session from Node (ids flow, look at renders between steps)
`figcraft-cli mcp` speaks JSON-RPC 2.0 on stdio (tools below). Helper (copy into the scratchpad):
```js
// fig.js — const { run, tool, done } = require("./fig");
const { spawn } = require("child_process");
const p = spawn("C:/CodeHouse/AIFilmEditor/apps/figcraft/target/release/figcraft-cli.exe", ["mcp"]);
let buf = "", n = 0; const wait = new Map();
p.stdout.on("data", d => { buf += d; let i; while ((i = buf.indexOf("\n")) >= 0) { const m = JSON.parse(buf.slice(0, i)); buf = buf.slice(i + 1); wait.get(m.id)?.(m); } });
const rpc = (method, params) => new Promise(r => { const id = ++n; wait.set(id, r); p.stdin.write(JSON.stringify({ jsonrpc: "2.0", id, method, params }) + "\n"); });
const ready = rpc("initialize", { protocolVersion: "2025-06-18", capabilities: {}, clientInfo: { name: "fig", version: "0" } });
async function tool(name, args = {}) {
  await ready;
  const m = await rpc("tools/call", { name, arguments: args });
  const c = m.result?.content?.[0];
  if (m.error || m.result?.isError) throw new Error(`${name} ${args.command || ""}: ${c?.text || JSON.stringify(m.error)}`);
  if (c?.type === "image") return c;            // {type:"image", data (base64 PNG), mimeType}
  try { return JSON.parse(c?.text); } catch { return c?.text; }
}
const run = (command, params = {}) => tool("run_command", { command, params });
module.exports = { run, tool, rpc, done: () => p.stdin.end() };
```
Usage: `const { id } = await run("frame.create", {preset: "YouTube thumbnail"}); await tool("export", {ids: [id],
format: "png", path: "C:/…/t.png"});`

### 3. Live app + control channel (the user watches)
```sh
node tools/craft.js figcraft --start [file.figcraft]       # figcraft.exe --control 9878
node tools/craft.js figcraft <command.id> '<json>'          # engine.execute → result JSON
node tools/craft.js figcraft --ui <method> '<json>'         # raw control method
node tools/craft.js figcraft --run steps.jsonl              # one {"id","params"} per line
```
Protocol (`docs/control-protocol.md`): newline-delimited JSON on `127.0.0.1:<port>`, `{id, method, params}` →
`{id, ok: true, result}` / `{id, ok: false, error: "message"}` — **exactly what craft.js speaks; no auth token, no
extra flags needed.** Differences worth knowing:
- A line that isn't JSON gets `{"id":null,"ok":false,…}` and **closes the connection**; lines are limited to 32 MiB;
  at most 8 connections and 8 queued requests; 60 s timeout per request and per idle socket.
- Requests run on the UI thread at the next frame; a minimised window still answers everything except
  `ui.screenshot` (parked until it paints).
- The app starts with a new untitled document when given `--control` (so commands work at once).
- Optional confinement: `--automation-read-root DIR` / `--automation-write-root DIR` (repeatable; unknown flags
  stop the app with `unknown option`). craft.js doesn't pass them; pass them after `--start` if wanted.
- The app's own fallback port is the `FIGCRAFT_CONTROL_PORT` env var; there is no fixed default — always 9878 here.
- For several steps with references, send one `command.batch {commands:[…], label?}` (same `as`/`$ref` rules as
  `run`): `craft.js --run` sends steps one by one and can't pass ids between them.

| Control method | Use |
|---|---|
| `engine.execute {command, params}` | any command (what `craft.js figcraft <id>` sends) |
| `engine.commands {}` | the catalogue |
| `document.inspect {depth?, allPages?}` | layer tree, selection, styles, images, colour profile, undo history |
| `node.get {id, depth?}` | one layer: geometry, fills, layout, sizing, text, component links, overrides, interactions |
| `ui.render {path?, scale?, ids?}` | PNG of the selection / ids / page's top-level layers, no UI chrome (works hidden) |
| `ui.screenshot {path?}` | the window as the user sees it |
| `ui.inspect {}` | tool, panels, dialogs, and while a prototype plays `presenter` / `preview` state (current screen, hotspots) |
| `ui.set {rightTab: design\|prototype\|inspect, preview: true\|frameId, …}` | switch panels, open the prototype preview pane |
| `ui.pointer`, `ui.key`, `ui.type`, `ui.input`, `ui.menu.invoke` | canvas gestures, shortcuts, raw input (reaches the presenter too) |
| `window.list`, `window.new {path?}`, `app.quit {}` | windows; `app.quit` closes **without asking** about unsaved changes |

### 4. MCP server (agents with tools)
| Mode | `.mcp.json` entry | Notes |
|---|---|---|
| Headless | `"figcraft": {"command": "C:/CodeHouse/AIFilmEditor/apps/figcraft/target/release/figcraft-cli.exe", "args": ["mcp"]}` | in-process engine, one untitled document, CPU renderer. Optional `"--automation-read-root", "C:/CodeHouse/AIFilmEditor", "--automation-write-root", "C:/CodeHouse/AIFilmEditor/projects"` |
| Bridged | `"figcraft-app": {"command": "…/figcraft-cli.exe", "args": ["mcp", "--attach", "9878"]}` | drives the app started with `node tools/craft.js figcraft --start`; user sees every change. `--attach` refuses the automation-root flags (the app confines). Calls aren't retried after a dropped connection: inspect before re-sending an edit |

Tools: `list_commands {filter?}`, `run_command {command, params}`, `batch {commands, label?}`, `create_node {type, x,
y, width, height, parent, name, text, path, props}`, `set_properties {ids, props}`, `inspect_document`, `get_node`,
`select`, `export {ids, format, scale|size, path?}` (no path → inline image), `screenshot {ids?, scale?, maxSize?,
window?}` (inline PNG), `open_file`, `save_file`, `undo`/`redo`, `pointer`, `key`, `type_text {text, id?}`,
`inspect_ui`. Prompts `mobile_screen`, `design_system`, `landing_page`, `prototype_flow` return step plans.
Resources `figcraft://document`, `figcraft://commands`, `figcraft://node/{id}`, `figcraft://command/{id}`.

## Core commands

### Documents, pages, frames
| Command | Params / notes |
|---|---|
| `file.new` / `file.newFromTemplate {template}` | templates (`template.list`): `mobile-app`, `landing-page`, `dashboard`, `design-system`, `wireframe-kit`, `social-posts` (one post in 5 sizes), `slides` (1920×1080), `icon-set` — synthetic, editable; structure only, never the look |
| `file.open {path}` / `file.import {path\|data, x?, y?}` | `.figcraft`, `.fig` (best effort), `.sketch`, REST API JSON, `.svg` (editable), images. `import` adds to the current page |
| `file.save {path}` / `file.saveAs {path}` | `.figcraft` (zip of JSON + images). First programmatic save needs a path. A `.fig` path writes an experimental copy |
| `page.add {name}` / `page.select` / `page.rename` / `page.list` | |
| `frame.create {preset? \| width, height, x?, y?, name?, parent?, props?}` | presets (`frame.presets`): `YouTube thumbnail` 1280×720, `Instagram post` 1080×1350, `Instagram story` 1080×1920, `Facebook post` 1200×630, `X post` 1200×675, `LinkedIn post` 1200×1200, `Slide 16:9` 1920×1080, `TV` 1280×720, `iPhone 16` 393×852, `iPhone 16 Pro Max` 440×956, `Android Compact` 412×917, `iPad Pro 11"` 834×1194, `Desktop` 1440×1024, `MacBook Air` 1280×832, A4/Letter… A preset without x/y lands right of the existing frames. No YouTube-banner preset: `width: 2560, height: 1440` |
| `node.create {type, x?, y?, width?, height?, parent?, index?, name?, text?, path?, props?}` | `type`: frame, rectangle, ellipse, polygon, star, line, arrow, vector (SVG `path`), text, section, component, slice → `{id, …}` |
| `node.set {ids, props}` | any property (geometry, paints, effects, layout, text, `name`, `visible`, `clip`, `isMask`, `exports`, `interactions`) |
| `node.reparent {ids, parent, index?}` / `node.reorder {id, index}` | index counts bottom first (= first in auto-layout flow) |
| `edit.duplicate {ids}` → `{ids}` / `edit.delete` / `object.group` / `object.mask` | |
| `grid.add {ids?, grid? {kind: grid|columns|rows, …}}` | layout grids; or `grids: […]` in `node.set` |

### Images
`image.place {path | data (base64), x?, y?, width?, height?, parent?, target?, mode?: fill|fit|crop|tile}` →
`{id, image, width, height, imageProfile}`. With `target` (an existing frame/rectangle) the image is added **on top of
its fills** (VERIFIED: the frame keeps its solid fill underneath, so a second `image.place` on the same target
stacks a third paint — clear first with `node.set {ids, props: {fills: []}}` or set `fill` back to one colour when
swapping a photo); without it a new rectangle layer is made. Adjust with `image.adjust {ids, preset?:
vivid|muted|warm|cool|blackAndWhite|fade|reset, filters? {exposure, contrast, saturation, temperature, tint,
highlights, shadows: -1..1}}`. Embedded ICC profiles are honoured. HEIC and video fills are not supported.

### Auto layout
`layout.add {ids, direction: horizontal|vertical|grid}` or set props on a frame: `layout`, `gap`, `padding` (n or
`[t,r,b,l]`), `mainAlign` (`min|center|max|spaceBetween|spaceAround|spaceEvenly`), `crossAlign`
(`min|center|max|baseline`), `wrap` + `crossGap`, `sizingH`/`sizingV` (`fixed|hug|fill`), `min/maxWidth/Height`,
`absolute: true` on a child to take it out of the flow. Grid: `gridColumns`, `gridRows`, `columnTracks` `[120,
"1fr", "auto"]`, child `gridColumn`/`gridRow`/spans. A child can't `fill` an axis its parent hugs (the parent turns
fixed). `layout.suggest` guesses auto layout from positions.

### Components, variants, instances
| Command | Params |
|---|---|
| `component.create {ids}` | one frame becomes a main component (several layers are wrapped) → `{id}` |
| `component.combineVariants {ids}` | mains → a component set; name variants `Style=Primary, State=Default` |
| `instance.create {component, x?, y?, parent?}` | component or set (its default = top-left variant) → `{id}` |
| `instance.setProperties {ids, properties {name: value}}` | switch variants / set text, boolean, swap props |
| `component.addProperty {type: text\|boolean\|instanceSwap\|variant\|slot, name, default, layer?}` / `component.bindProperty {field: characters\|visible\|…}` | expose a text layer as a property |
| `instance.swap {ids, component}` / `component.detach` / `component.resetInstance` / `component.pushChanges` | |
| `text.set {id, text}` (or MCP `type_text {id, text}`) | override text inside an instance (find the inner id with `get_node {id, depth: 3}`) |
Overrides allowed on instances: fills, strokes, effects, opacity, visibility, names, radius, text and text props,
auto-layout padding/gap/alignment, interactions. **Refused:** moving/resizing/adding layers inside an instance —
resize the instance or edit the main.

### Styles and variables (colour tokens)
- `variable.createCollection {name, modes?: ["Light","Dark"]}`; `variable.create {collection, name, type:
  color|number|string|boolean, value | values {Light: "#…", Dark: "#…"}}`; `variable.set {variable, mode?, value |
  {alias}}`; `variable.bind {ids, field: fill|stroke|fills/0/color|gap|cornerRadius|fontSize|characters|…, variable}`.
  Names are accepted where ids are (VERIFIED: create collection + colour variable + bind to a frame's fill by name).
  `variable.setMode {ids, collection, mode}` shows a frame (and its children) in a mode (Light/Dark).
- `style.create {type: paint|text|effect|grid, name, from?: nodeId, value?}`; `style.apply {style, ids?, start?,
  end?}`; `style.update`; `style.list`. Editing a styled value on a layer unlinks the style.
- Export/import tokens: `variable.export` / `variable.import` (JSON).

### Effects, booleans, vectors
- `effect.add {ids, type: dropShadow|innerShadow|layerBlur|backgroundBlur|noise|texture|glass}` or full object, e.g.
  `effects: [{"type":"dropShadow","color":"#00000026","offset":[0,4],"radius":16,"spread":0}]` in `node.set`;
  progressive blur: `{"type":"layerBlur","blurType":"progressive","startRadius":0,"radius":24,"startOffset":[0.5,0],
  "endOffset":[0.5,1]}`.
- `bool.union|subtract|intersect|exclude {ids}` → a live boolean group (operands stay editable); `bool.flatten`.
- Vectors: `node.create {type: "vector", path: "M… C… Z"}`; `vector.outlineStroke`, `vector.flatten`; pen/pencil via
  `pointer` gestures.

### Text
`node.create {type:"text", parent, text, props {fontFamily, fontStyle, fontSize, fills, …}}` (or `text.create {text,
x, y, width?}`; `width` makes it wrap). `text.fit {ids, maxLines?, minSize?}` shrinks text to fit its box (largest
size within `maxLines`, avoids one-word last lines). `text.fonts {}` lists families; `{family, axes: true}` lists
styles/axes. `text.missingFonts` lists fonts the file names that aren't installed (drawn in a fallback).
`text.loadFont {path}` adds a font file for the session.

### Filling copies with data (series, carousels, multi-size)
`data.fill {id (template frame), rows: [{<layer name>: "text" | {text?, fill?, visible?, fit?}, name?}], gap?,
formats? [{name?, width, height}], dir?, format? png|jpg|webp|svg|pdf, scale?}` → `{ids, missing, files, errors}`.
Copies the frame once per row (to the right), sets every layer with that name, optionally once per size (the copy is
resized so **auto layout reflows** — fixed-position children keep their place), and with `dir` exports each copy as
`<name>.<format>`. Up to 500 rows, one undo step. This is the series/thumbnail/carousel workhorse: name the layers
you vary (`Headline`, `Ep`, `Badge`) in the template. Image swaps per row are not a `data.fill` field: do them with
`image.place {target}` on each copy's photo layer.

### Prototypes
| Command | Params |
|---|---|
| `proto.interaction.add` | `{id, dest}` = on-click navigate; full: `{id, trigger {type: onClick\|onHover\|onPress\|onDrag\|afterDelay {ms}\|keyPress {key}…}, action {type: navigate\|back\|scrollTo\|openOverlay\|swapOverlay\|closeOverlay\|openUrl\|changeTo\|setVariable\|setVariableMode\|conditional, dest?}, transition {type: instant\|dissolve\|smartAnimate\|moveIn\|moveOut\|push\|slideIn\|slideOut, direction?}, durationMs?, easing?}` → `{index}` |
| `proto.interaction.remove {index}` / `.clear` | |
| `proto.flow.add {start, name?}` | flow starting point (top-level frame) |
| `proto.settings {device?, rotation?, background?, responsive?}` | `iPhone 16`, `iPhone 16 Pro Max`, `Android Compact`, `iPad mini`, `MacBook Air`, `Desktop`, `Custom size` (+width/height), `None` |
| `proto.present {start?}` / `proto.preview {start?}` / `proto.closePreview` | play full-window (a Present tab) / in a pane over the canvas — **app only** |
Smart animate matches layers by name and hierarchy. Interactive components: put interactions on variants
(`changeTo`) and every instance plays them. **No video export of a prototype, no share link, no media triggers.**
To get a prototype into a video: export each screen/state as PNG (in flow order) and let the editor/motion designer
animate between them; or play it in the app and grab `ui.screenshot` after each `ui.input` click (stills only).

### Export
| How | Notes |
|---|---|
| `figcraft-cli export file.figcraft -o outdir/ [--format png\|jpg\|webp\|svg\|pdf] [--scale N] [--page NAME]` | one file per **top-level frame**, named after the frame (`Thumb.png`); `--scale` up to 64 for rasters |
| `figcraft-cli export file.figcraft -o x.png --node "Thumb"` | one layer by name or id |
| `figcraft-cli export file.figcraft -o all.pdf` | all top-level frames, one page each, vector text (selectable); `--bleed 3mm --crop-marks --cmyk` for print (naive CMYK, no profile) |
| `figcraft-cli render file.figcraft -o page.png [--scale N]` | the whole page with its background (contact-sheet view of every frame) |
| `file.export {ids?, format, scale? \| size? ("2x", "1080w", "2160h"), path?}` | in a session; without `path` returns base64 |
| `export.add {ids, setting {size?, suffix?, format?}}` + `file.exportLayers {ids?, dir}` | per-layer export settings, then batch export (`<layer><suffix>.<format>`) |
| `file.exportFramesPdf {page?, path}` | every top-level frame of a page to one PDF |
| MCP `export {ids, format, scale\|size, path?}` / `screenshot {ids?}` | without path, inline image you can look at |
Exports carry the frame's clip, effects and colour profile (sRGB default). `--format fig` writes an experimental
`.fig`. `--format xml` = Android Vector Drawable.

## Fonts (VERIFIED with `text.fonts {}` and rendered exports)
The app and CLI use FigCraft's built-in fonts **plus every installed system font** (indexed on first text layout).
This build has **no craft-fonts** (`apps/craft-fonts` isn't checked out; `.cargo/config.toml` points
`CRAFT_FONTS_DIR` at it), so **Inter is missing** — FigCraft's own default for new text and the face its docs,
templates and examples use. Text in Inter renders in a fallback and `figcraft-cli info --json` lists it under
`missingFonts`. **Always set `fontFamily` + `fontStyle` explicitly.**
- Installed and listed here: Segoe UI Variable, Segoe UI, Bahnschrift, Sitka, Georgia, Palatino Linotype, Cambria,
  Constantia, Corbel, Candara, Calibri, Arial, Verdana, Tahoma, Trebuchet MS, Franklin Gothic Medium, Gabriola,
  Roboto, Times New Roman, Cascadia Code/Mono, Consolas, Segoe Print/Script, Ink Free, Impact, Yu Gothic, Malgun
  Gothic, Microsoft YaHei, plus a few user fonts.
- **Style names are the font's own:** Segoe UI Variable's are `Regular`, `Semibold Text`, `Semibold Display`,
  `Bold Display`, `Light Small`… (`text.fonts {family}` lists them). `fontStyle: "SemiBold"` or `"Semibold"` is
  accepted without error but isn't a real style — use the listed name. VERIFIED: `Semibold Display` for a 64 px
  headline, `Semibold Text` for a 20 px button label, both rendered correctly with `missingFonts: []`.
- Good defaults: UI/social sans = **Segoe UI Variable** (Display optical size ≥ 28 px, Text below) or Bahnschrift
  (condensed, sporty); editorial serif = **Sitka** (style `Banner`/`Display` for big type) or Georgia. Same set
  as VectorCraft, so a project's type stays consistent across apps.
- Microsoft fonts are licensed with Windows: fine in exported PNG/PDF (PDF embeds subsets); SVG export outlines text
  by default (VERIFIED: 0 `<text>` elements). Don't ship font files.
- `--no-system-fonts` / `FIGCRAFT_NO_SYSTEM_FONTS=1` would leave only built-ins — don't use it here.

## Verify what you made
- **Look:** export every delivered frame and Read the PNG at full size, plus a small version (`--scale 0.15` for a
  ~190 px-wide thumbnail check). `figcraft-cli render` shows all frames on one image for an overview. In the live app
  `ui.screenshot` shows what the user sees.
- **Inspect:** `document.inspect` / `node.get {id, depth}` (sizes, sizing modes, overrides, interactions, bound
  variables); `figcraft-cli info file.figcraft --json` (frames with sizes, missing fonts, counts).
- **Files:** PNG size check without Python:
  `node -e "const b=require('fs').readFileSync(process.argv[1]);console.log(b.readUInt32BE(16),'x',b.readUInt32BE(20))" f.png`

## Pitfalls
1. Exports, `data.fill {dir}` and `--out` overwrite silently — `ls` first, version the names.
2. `x`/`y` are parent-relative; children of auto-layout frames ignore x/y (use `absolute: true` to place freely).
3. Layers inside instances can't be moved/resized/added — change the main component.
4. `figcraft-cli run` is all-or-nothing: one bad step and nothing is written; read the `error` line.
5. `craft.js --run` can't chain ids; use one `command.batch` (or `figcraft-cli run`) with `as`/`$ref`.
6. Malformed control JSON closes the socket; `app.quit` discards unsaved changes without asking — save first.
7. `figcraft-cli export -o dir/` exports only **top-level frames** of the first page (`--page` for others); loose
   layers outside frames export only when the page has no frames.
8. Prototypes play only in the GUI; there's no video/GIF export.
9. `.fig` import/export is best effort/experimental; don't promise round-trips to Figma.
10. No craft-fonts in this build: Inter (the default, and the font of templates/examples) is missing → fallback. Check
    `info --json` → `missingFonts` and restyle.
11. `text.fit` (and `data.fill`'s `fit`) **fails the whole script** on auto-width text ("grows to its text: give it
    a fixed width"): set the template's text to `textAutoResize: "height"` with a `width` first. Height-auto text
    grows **downward** from its y, so anchor bottom-aligned headlines with room below or put them in a bottom-aligned
    auto-layout frame.
12. `image.place {target}` adds a paint on top of the existing fills; swapping photos stacks paints (see Images).
13. `ui.input` clicks in the presenter: send move, down and up as **separate calls with ~0.3–0.5 s between** them;
    sent back to back the first click was ignored (VERIFIED). Hotspot rects come from `ui.inspect` → `presenter.hotspots`
    (window points = screenshot pixels at 100 % UI scale).
14. A layer you leave on the page (a main component, a spare instance) is a top-level layer: `export -o dir/`
    writes it too (`Button.png`, `Button 2.png`). Keep mains on a separate "Components" page or inside a frame.

## Verification log (2026-10-26, figcraft 0.11.2, scratchpad `figcraft-test/`)
VERIFIED:
- `figcraft-cli run build.json --out test.figcraft` (18 steps with `as`/`$ref`): colour variable collection +
  variable; `frame.create {preset: "YouTube thumbnail"}` (1280×720); `image.place {target, mode: "fill"}` (a JPG
  still filled the frame, cropped); a gradient scrim rectangle; a text layer; an auto-layout pill button (horizontal,
  padding, hug/hug, radius 999) with its fill bound to the variable; `component.create`; two instances (one inside the
  thumbnail, one on the page); two `iPhone 16` frames; `proto.interaction.add` (on click → navigate, push left,
  300 ms, easeOut) on an instance; `proto.flow.add`; `proto.settings {device}`.
- Instance text override with `text.set {id: <inner text id>}` ("Episode 4"); the hugging instance resized to it.
- `figcraft-cli export file -o dir/` (one PNG per top-level frame, named after it), `--node "Thumb" -o x.jpg`,
  `-o x.svg` (text outlined), `-o all.pdf`, `--node "01 Home" --scale 3` → 1179×2556 PNG; `render --scale 0.5`
  (whole page). Looked at the PNGs: image fill, scrim, text and button all correct.
- `data.fill` with `dir` (2 rows, one with `fit: {maxLines: 2}`, one hiding the scrim) → `ep-05.png`, `ep-06.png`.
- Headless MCP via the `fig.js` helper: `open_file`, `run_command image.place` on a copy, `get_node`, `screenshot`
  (inline PNG), `export {size: "640w", path}`.
- GUI: `node tools/craft.js figcraft --start file.figcraft` → `window.list`, `view.zoomFit`, `node.create` (appeared
  live), `ui.screenshot`; `proto.present {start}` opened a Present tab with an iPhone device frame;
  `ui.inspect` → `presenter.hotspots`; a `ui.input` click on the hotspot navigated to the second screen
  (`presenter.current` changed, history `[11]`); `file.save {path}` from the app; `app.quit`.
- Bridged MCP: `figcraft-cli mcp --attach 9878` → `initialize`, `create_node` (the frame appeared in the app's
  document), `tools/list`.
UNVERIFIED: variants/`combineVariants`/`instance.setProperties`, styles, `variable.setMode`, effects, booleans,
`grid.add`, `data.fill {formats}`, `.fig`/`.sketch`/REST import, plugins, `--automation-*` roots, PDF print options,
smart animate, overlays, the preview pane.
