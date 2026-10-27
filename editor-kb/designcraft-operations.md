# Driving DesignCraft — operations manual

DesignCraft is an InDesign-class page-layout app (Rust). Every action is an engine **command**
(`crates/engine/src/cmd/*`, 542 of them on 0.13.0) reachable from the headless CLI, the MCP server and the running app's
control channel. Paths are relative to `C:\CodeHouse\AIFilmEditor\`.

Status of this manual: written from the source of `apps/designcraft/` (DesignCraft 0.5.0) and **verified on this
machine on 2026-10-10** — headless scripts, `run` exports (PNG at scale 0.25/1/4.17, `--all-pages`, PDF screen/print/
PDF-X-4), parent pages, guides, `frame.grid`, tables from text, PNG and SVG placement, preflight, `font.list`, the
live app through `tools/craft.js` (commands, `script --connect`, `ui.render`, `ui.screenshot`, `app.export`,
`file.saveAs`, `app.quit`) and the headless MCP handshake. **Re-verified headless 2026-10-27 on DesignCraft 0.13.0**:
poster script (renders identically), `run` PNG with bleed / `--all-pages` / `--pdf-options`, `script --export`,
print PDF (bleed + marks), screen PDF (`compressImages`), PDF/X-4 (+ `validate-pdf`), PDF/X-1a, parent pages,
`frame.grid`, paragraph/character styles, CMYK swatch with tint, table from text, image in an ellipse frame,
**Paste Into**, preflight, `font.list`, overset reporting, MCP `tools/list` and `export_png`. The live app /
control channel was not re-run. Anything marked **UNVERIFIED** is read from the source but not yet run here — check
it on first use and update this file.

A worked, verified example (1080×1350 poster: background, full-width photo, headline, date line) is in
**§ Recipes → Poster script**. Start from it.

## Binaries

| What | Path |
|---|---|
| Desktop app | `apps\designcraft\target\release\designcraft.exe [--control 9877] [--sample] [files…]` |
| Headless CLI | `apps\designcraft\target\release\designcraft-cli.exe` (no args = usage) |
| Control client | `node tools\craft.js designcraft …` (port 9877) |
| Rebuild | `sh tools/build-apps.sh designcraft` (or `cargo build --release -p designcraft -p designcraft-cli` in `apps\designcraft`) |

Launch the app with its control port: `node tools\craft.js designcraft --start` (= `designcraft.exe --control 9877`;
`DESIGNCRAFT_CONTROL_PORT=9877` also works). It opens a window — ask the user before launching it, and quit it when
you're done with `node tools\craft.js designcraft --ui app.quit` if you started it (ask first if they have work open).

## Units and coordinates (read this first)
- **Everything is in points** (1/72 in): page sizes, rects, margins, bleed, font sizes, leading, offsets.
  1 mm = 2.834646 pt · 1 in = 72 pt · 1 pica = 12 pt.
- **A3** = 841.89 × 1190.55 pt (preset `"A3"`). A4 = 595.28 × 841.89. 3 mm bleed = **8.504 pt**; 5 mm = 14.173.
- **Screen documents: 1 px = 1 pt.** A 1080×1350 px poster is `width 1080, height 1350`; rendered at `scale 1`
  it is exactly 1080×1350 px.
- **Rects** are `[x0, y0, x1, y1]` (corners, not x/y/w/h), y down, in **spread** coordinates. With
  `facingPages: false` every page is its own spread and its top-left is (0, 0) — **always use `facingPages: false`**
  for posters, one-sheets, storyboards and carousels (the default is `true`, which puts page 2 at x = page width on
  spread 1). Bleed lies outside the page: a full-bleed image on A3 with 3 mm bleed is
  `[-8.504, -8.504, 850.394, 1199.055]`.
- `spread` params: a number (document spread index, 0-based) or `{"kind":"parent","index":0}` for parent (master)
  spread A. Page indices in `render_page` / `--page` / `ui.render` are **0-based**; `pages` in `file.exportPdf` /
  `layout.pageSize` / `layout.section` are **1-based**.
- Render `scale` = **pixels per point**. ppi = 72 × scale: scale 1 = 72 ppi, 2.0833 = 150 ppi, 4.1667 = 300 ppi.
  A3 at 300 ppi = 3508 × 4961 px. Hard cap: 65 024 px per side, 2^29 pixels per page.

## Three ways in

### 1. Headless CLI (default for building deliverables — fast, reproducible, no window)

**Script** (the workhorse): one command per line `command.id {json}`, `#` comments; also JSON lines or a JSON array
of `{command, params}`. `"$N.path"` in a param = that value of step N's result (0-based, **counting commands only —
comment and blank lines don't count**; `$last` = previous step); `"${N.path}"` interpolates inside a string.
`"ids": ["$4.id"]` works (the string becomes the number). A 20-step poster script runs in ~0.3 s.

```sh
designcraft-cli script poster.dcs --save out/poster.designcraft --export out/poster.pdf
designcraft-cli script poster.dcs --in existing.designcraft --save out/poster-v2.designcraft
designcraft-cli script poster.dcs --connect 9877      # same steps, live in the running app
```
A script starts with an empty Letter document already open; its first line should be `file.new {…}` (that creates
and activates a new document). Output: `{"completed": n, "results": [...]}`; on failure `failedIndex`,
`failedCommand`, `error` and a non-zero exit. `--keep-going` records errors and continues. `--export` runs after the
script: `.pdf` → `file.exportPdf` with **default options (no bleed, no marks)**, `.idml`, `.epub`, anything else →
PNG/JPEG of **page 1 only at scale 2**. For print PDFs and per-page PNGs, export explicitly (below).

**run** (single commands, rendering at a chosen resolution):
```sh
designcraft-cli run --in out/poster.designcraft --scale 1 --export out/poster-1080x1350.png
designcraft-cli run --in out/storyboard.designcraft --scale 2 --all-pages out/pages     # page-001.png, page-002.png …
designcraft-cli run --in doc.designcraft --page 2 --scale 4.1667 --export p3-300ppi.png  # --page is 0-based, set before --export
designcraft-cli run --in doc.designcraft --pdf-options "{\"bleed\":true,\"marks\":true}" --export print.pdf
designcraft-cli run --cmd file.new={\"width\":1080,\"height\":1350,\"facingPages\":false} --cmd … --export x.png
```
Options are processed **in order** (`--scale`/`--page`/`--pdf-options` must come before the `--export` they affect;
several `--export`s with different settings in one call work). The CLI prints `wrote <file> (W×H, …)` per file.
`run`'s PNG/JPEG export **includes the bleed area** (verified: A3 + 3 mm bleed at scale 1 = 859×1208, not 842×1191);
`app.export` / `ui.render` (live app), MCP `export_png` and `script --export` render the trim only. So for a screen
PNG of a bleed document use the live app's `app.export`, or build the screen version as its own no-bleed document
(recommended anyway). JPEG by `.jpg` extension (quality 90).

**Discover:** `designcraft-cli commands <filter>` (JSON of every matching command), `designcraft-cli describe <id>`.
**Check a PDF:** `designcraft-cli validate-pdf x.pdf` → `{standard, valid, issues, warnings}` (built-in PDF/X-4 checks,
incl. unembedded fonts; new 2026-10-27, verified).

### 2. Control channel (the running app; the user watches)
JSON lines on `127.0.0.1:<port>`: `{"id","method","params"}` → `{"id","ok":true,"result"}` or
`{"id","ok":false,"error":"text"}`. No auth, loopback only, max 16 connections, a malformed line closes the
connection. `tools/craft.js` speaks it as is:
```sh
node tools/craft.js designcraft frame.create "{\"rect\":[36,36,300,200],\"content\":\"text\",\"text\":\"Hi\"}"
node tools/craft.js designcraft --ui document.inspect
node tools/craft.js designcraft --ui ui.render "{\"path\":\"C:/…/p1.png\",\"page\":0,\"scale\":1}"
node tools/craft.js designcraft --ui ui.screenshot "{\"path\":\"C:/…/window.png\"}"
designcraft-cli script steps.dcs --connect 9877        # a whole script live, with $N references
designcraft-cli app --port 9877 file.save "{\"path\":\"…\"}"   # NB: `app` defaults to port 7979
```
Methods: `engine.execute {command, params}`, `engine.commands`, `document.inspect`, `ui.inspect`,
`ui.menu.list`, `ui.tool.list`, `ui.tool.select {tool}`, `ui.pointer {events}`, `ui.key`, `ui.text`, `ui.click`,
`ui.drag`, `ui.move`, `ui.set {zoom?, page?, fit?, guides?, rulers?, frameEdges?, screenMode?, …}`,
`ui.dialog.open/set/confirm/cancel`, `ui.screenshot {path}`, `ui.render {path?, page?, scale?, bleed?}`,
`app.open/save/export {path, page?, scale?}`, `app.quit`. `ui.render` without `path` returns `pngBase64`.
The app starts on its start screen with no document (`file.new` returns `index 0`); `ui.set {"fit":true}` fits the
page in the window. Unknown commands come back as `{"ok":false,"error":"unknown command `x`"}` (craft.js prints it
and exits 1). A missing font shows as pink highlight in the window. (All verified.)

### 3. MCP (`designcraft-cli mcp`)
Newline JSON-RPC on stdio. Headless (`mcp`, own in-process engine, starts with an empty Letter document) or bridged
(`mcp --connect 9877`, drives the running app; window tools `screenshot`, `click`, `drag`, `ui_*`, `dialog_*` only
work here). Tools: `list_commands`, `execute {command, params}`, `batch {commands | script}`, `inspect_document`,
`get_story`, `set_story_text`, `new_document`, `open_document`, `save_document`, `place_image`,
`render_page {page, scale?, bleed?, path?}` (returns the PNG as an image — the quickest way to look at a page),
`export_png {path, page?, scale?}`, `screenshot`, `select_tool`, `pointer`, `key`, `type_text`, `menu_list`,
`ui_inspect`, `ui_set`, `ime`, `dialog_*`. Optional (new 2026-10-27): `mcp --automation-read-root DIR
--automation-write-root DIR` (repeatable) confines every file the agent reads/writes to those folders; once roots are
given, a kind left out grants no access. Without any roots the headless server is unconfined (verified:
`export_png` to the scratchpad works with the plain `["mcp"]` entry). `.mcp.json` entries:
```json
"designcraft":     {"command": "C:/CodeHouse/AIFilmEditor/apps/designcraft/target/release/designcraft-cli.exe", "args": ["mcp"]},
"designcraft-app": {"command": "C:/CodeHouse/AIFilmEditor/apps/designcraft/target/release/designcraft-cli.exe", "args": ["mcp", "--connect", "9877"]}
```
(The bridged server fails to start if the app isn't running; it reconnects once if the app restarts.)
Headless `initialize` + `tools/list` verified (25 tools; 26 on 0.13.0, 2026-10-27 — `ime` added); the bridged variant is **UNVERIFIED** (same control methods
that were verified through craft.js).

## Core commands (ids and params)

### Document, pages, parents
| Command | Params | Notes |
|---|---|---|
| `file.new` | `{preset?, width?, height?, pages?, facingPages?, columns?, gutter?, margins?: n \| {top,bottom,inside,outside}, bleed?: n, title?, primaryTextFrame?}` | → `{index}`; becomes active. Presets: `Letter`, `Legal`, `Tabloid`, `A3`, `A4`, `A5`, `B5`, `Business Card`, `Postcard`, `Web 1920 × 1080`, `Mobile 1080 × 1920`, `Tablet 1024 × 1366`, … (`file.presets`). Defaults: Letter, 1 page, facing, 36 pt margins, no bleed |
| `layout.documentSetup` | `{width?, height?, pages?, facingPages?, intent?: print\|web\|mobile, bleed?, slug?, adjustLayout?}` | change later |
| `layout.marginsAndColumns` | `{pages?, margins?, columns?, gutter?}` | |
| `layout.pages.insert` | `{count?, after?: page index, parent?: "A" \| null}` | |
| `layout.pages.delete` / `.move` / `.duplicateSpread` | `{pages:[i]}` / `{from,to}` / `{spread}` | |
| `layout.parents.new` | `{prefix?, name?}` | parent (master) spreads; put items on them with `spread: {"kind":"parent","index":0}` |
| `layout.pages.applyParent` | `{pages:[i], parent:"A"\|null}` | |
| `layout.overrideParentItems` | `{page}` | editable copies of parent items |
| `layout.section` | `{page (1-based), startNumber?, style?, prefix?}` | page numbering |
| `document.preferences` | `{horizontalUnits?, verticalUnits?, baselineGrid?: {start, increment, …}, grid?, …}` | display units only; commands still take points |

### Frames and objects
| Command | Params | Notes |
|---|---|---|
| `frame.create` | `{rect, spread?, shape?: rectangle\|ellipse\|polygon, sides?, starInset?, content?: text\|graphic\|unassigned, text?, caret?, vertical?}` | text → `{id, story}`; others → `{id}`. A shape/graphic frame is left **selected**; a text frame made with `text` leaves a **caret at the end of its story** (see pitfall 4). **Changed 2026-10-27:** a frame with no `content` now has **no stroke**; only `content: "unassigned"` gets the 1 pt black stroke (verified) |
| `frame.grid` | `{rect, cols, rows, gutter? (12), content?: graphic, spread?}` | → `{ids}` row-major; a grid of frames filling rect (storyboard panels). Cells take the rect's proportions — compute the rect so cells are 16:9 when they hold film frames (verified) |
| `object.fill` | `{swatch, tint?: 0..1, ids?}` | swatch **name** (`"[Paper]"`, `"[Black]"`, `"[None]"`, or one you made) |
| `object.color` | `{color: "#rrggbb" \| {c,m,y,k} \| [r,g,b], target?: fill\|stroke, ids?}` | unnamed colour; prefer swatches |
| `object.stroke` | `{swatch?, weight?, align?, tint?, ids?}` | `{"swatch":"[None]"}` removes the default stroke |
| `object.opacity` / `object.dropShadow` / `object.feather` / `object.gradient` | see `describe` | |
| `object.cornerOptions` | `{shape: rounded\|…, size, ids?}` | |
| `object.textFrameOptions` | `{columns?, gutter?, inset?, verticalJustification?: top\|center\|bottom\|justify, autoSize?, ids?}` | |
| `object.textWrap` | `{mode: none\|boundingBox\|contour\|…, offset?, ids?}` | |
| `object.align` / `object.distribute` | `{edge, to?: selection\|margins\|page\|spread, ids?}` / `{axis, by?, spacing?, ids?}` | |
| `object.arrange` | `{to: front\|forward\|backward\|back, ids?}` | |
| `transform.set` | `{x?, y?, width?, height?, rotation?, ref?: 0..8, ids?}` | absolute geometry |
| `transform.move` / `.rotate` / `.scale` | `{dx,dy}` / `{angle}` / `{sx,sy}` + `ids?` | |
| `selection.set` | `{ids:[id], add?}` | most commands take `ids`; text formatting acts on the **selection** |
| `edit.deselectAll`, `edit.clear {ids?}`, `edit.undo`, `object.group {ids?}`, `object.lock` | | |
| `object.label` / `object.findByLabel` | `{label, ids?}` / `{label}` | name things for later scripts |

### Images
| Command | Params | Notes |
|---|---|---|
| `file.place` | `{path, frame?: id, spread?, x?, y?, width?, pdfPage?, pdfCrop?}` | → `{id, asset}`. Into `frame`: **fills proportionally, centred** (cropped). Without `frame`: new frame at x,y (default top-left margin) `width` wide (default ≤ 60 % page width), proportional height. PNG, JPEG, TIFF, WebP, GIF, BMP, PSD, **SVG**, **PDF** (pdfPage) |
| `object.fit` | `{mode: fillProportionally\|fitProportionally\|fitContentToFrame\|centerContent\|fitFrameToContent, ids?}` | |
| `object.fittingOptions` | `{autoFit?, fitting?, align?: 0..8 (4 = centre; 1 = top centre…), crop?: n \| [t,l,b,r], ids?}` | crop focus: `align` picks which part of the image the fill keeps |
| `object.clippingPath`, `object.caption` | | captions from metadata (`{ppi}` variable) |
| `edit.pasteInto` | `{id?}` | **Paste Into** (new 2026-10-27, verified): the copied/cut objects become the content of the selected frame (or `id`), clipped by its shape → `{id, items}` |

**Image in a shape (verified 2026-10-27).** Simplest: `frame.create {"rect":…, "shape":"ellipse", "content":"graphic"}`
then `file.place {"path":…, "frame": id}` — fills proportionally, clipped to the ellipse. **Paste Into** (any
object(s) into any frame): select the object → `edit.copy` / `edit.cut` → `selection.set {"ids":[frame]}` →
`edit.pasteInto {}`. The pasted content keeps its own size and is **centred** in the frame; `object.fit` on the
frame does nothing to it — size it with `transform.set {"ids":[contentId], "x","y","width","height","ref":0}`, where
`contentId` is the frame's `children[0].id` in `document.inspect` (a new id, not the original's). If you `edit.copy`
a placed image, delete the original afterwards (`edit.clear {"ids":[…]}`).

### Text and styles
| Command | Params | Notes |
|---|---|---|
| `story.setText` | `{story, text}` | `\n` = new paragraph; replaces the whole story |
| `story.get` | `{story? \| frame?}` | text, frames, paragraphs, lines. Its `overset` field is **not reliable** (it said `0` for a fully overset headline — `lines: 0` was the tell; on 0.13.0 it is a character count, 6 where preflight said 5); use `document.inspect` → `stories[].overset` (bool) or `preflight.run` |
| `text.select` | `{story, anchor, focus}` | **UTF-8 byte** offsets (· and — count 2–3 bytes) → format part of a story |
| `type.char` | `{attrs: {fontFamily, fontStyle, size, leading: {"kind":"points","value":n} \| {"kind":"auto"}, tracking, kerning, hScale, vScale, baselineShift, fill: swatch name, fillTint, capitalization: allCaps\|smallCaps\|normal, underline, ligatures, otfFeatures, …}}` | acts on the selected text range, or the whole story of each **selected text frame** — so `selection.set {"ids":[frameId]}` first (verified). Attrs may also be passed bare (`{"size":40}`). `tracking` in 1/1000 em (150 on a 36 pt date looks right, verified) |
| `type.para` | `{attrs: {align: left\|center\|right\|leftJustified\|fullyJustified…, leftIndent, firstLineIndent, spaceBefore, spaceAfter, dropCapLines, hyphenate, keepWithNext, balanceRagged, ruleAbove/ruleBelow, …}}` | same targeting |
| `style.paragraph.create` | `{name, basedOn?, nextStyle?, para?: {…}, chars?: {…}}` | attrs as above |
| `style.character.create` | `{name, basedOn?, chars?: {…}}` | |
| `style.paragraph.apply` / `style.character.apply` | `{name, clearOverrides?}` | to the selection / selected frames |
| `swatch.create` | `{name, color: "#rrggbb" \| {c,m,y,k} (0..100) \| [r,g,b], spot?}` or `{name, gradient: {kind?: linear\|radial, stops: [{location 0–100, swatch? \| color?, opacity?}]}}` | → `{name}`. Built-ins: `[None]`, `[Paper]`, `[Black]`, `[Registration]`. CMYK swatches avoid preflight `rgbColor` (verified). Gradient swatches new 2026-10-27 (UNVERIFIED) |
| `font.list` | `{}` | fonts **used in the document**, with `missing` — run after typesetting |
| `font.replace` | `{family, style?, toFamily, toStyle?}` | |
| `type.createOutlines` | `{ids?}` | text → paths (last resort) |

### Tables, guides, grids
| Command | Params | Notes |
|---|---|---|
| `table.insert` | `{rows? (4), cols? (4), headerRows?, footerRows?, width?}` | at the text insertion point (needs a caret: `frame.create {…,"content":"text","caret":true}`) **UNVERIFIED** |
| `table.convertFromText` | `{columnSeparator?: tab\|comma}` | verified recipe: `frame.create {…,"text":"A\tB\n1\t2"}` → `edit.selectAll {}` → `table.convertFromText {"columnSeparator":"tab"}` → `{rows, table}`. Default look: equal columns across the frame, 1 pt black cell strokes, body font — restyle with `table.setCell` / `table.options` |
| `table.select` / `table.setCell` / `table.setColumnWidth` / `table.setRowHeight` / `table.options` / `table.get` | see `describe` | `setCell {fill, insets, vj, text, stroke}` |
| `table.placeGraphic` | `{path, fit?}` | image in a cell |
| `layout.createGuides` | `{rows?, columns?, rowGutter?, columnGutter?, fitTo?: margins\|page, page?}` | the layout grid as guides (→ `{guides: n}`; `guide.list` gives positions to snap frames to; guides don't print) |
| `guide.add` | `{orientation: horizontal\|vertical, position, spread?}` | |

### Checking and exporting
| Command | Params | Notes |
|---|---|---|
| `document.inspect` (method, or MCP `inspect_document`) | | stories (**overset**), styles, swatches, parents, selection. **Changed 2026-10-27:** items and pages are per spread — `spreads[n].items[]` (`id, kind, bounds, fill, stroke, story?, children?` for frame contents) and `spreads[n].pages[]` — no top-level `items`/`pages` |
| `preflight.run` | `{minPpi?: 150}` | → issues `[{severity, kind, message, item?, page?}]`, kinds: `overset`, `lowResolution`, `missingFont`, `missingGlyphs`, `missingLink`, `emptyText`, `rgbColor`, `unsupportedTypography` |
| `file.exportPdf` | `{path, pages?, bleed?, marks?: bool \| {crop, bleed, pageInfo, weight, offset}, standard?: none\|x4\|x1a\|a2b, compressImages?, spreads?, title?, author?, tagged?, flatten?, created?}` | → `{path, bytes, pages, warnings}`. Real text with embedded font subsets; images embedded **at full resolution, lossless** unless `compressImages` |
| `app.export` (method) | `{path, page?, scale? (2)}` | one page PNG/JPEG, trim only |
| `file.save` / `file.saveAs` / `file.saveACopy` | `{path}` | native `.designcraft` |
| `file.exportIdml` | `{path}` | InDesign hand-off |
| `file.package` | `{dir, pdf?}` | document + Links + fonts + report |

## Recipes

### Print vs screen exports
- **Print PDF (A3 poster):** document with `bleed: 8.504`; background art extends to the bleed edge; then
  `file.exportPdf {"path": "…/poster-A3.pdf", "bleed": true, "marks": true, "title": "…"}` (or
  `run --in x.designcraft --pdf-options "{\"bleed\":true,\"marks\":true}" --export x.pdf`) — verified (again
  2026-10-27). Without `bleed: true` the bleed is cropped off. `"standard": "x4"` writes PDF/X-4 (Generic CMYK
  output intent). On 0.10 it warned about RGB images needing an ICC profile; **on 0.13.0 (2026-10-27) an RGB PNG
  exported with no warnings and `validate-pdf` says `valid: true`** — still tell the printer the photos are RGB.
  New: `"standard": "x1a"` (PDF/X-1a:2003 — flattened, CMYK/gray/spot only; verified it exports) for printers that
  ask for X-1a.
- **Screen PDF:** `{"path", "compressImages": true}` (no bleed, no marks) — verified 827 KB → 77 KB on the test
  poster.
- **Screen PNG at exact pixels:** build the document in px-as-pt (1080×1350) and render at scale 1. For an A3
  document rendered for screen, scale = target width ÷ 841.89 (1080 px wide → 1.2828).
- **Per-page PNGs** (storyboard proofs, carousels): `run --in doc --scale S --all-pages DIR`.

### Image resolution
Effective ppi = image pixel width ÷ (frame width in pt ÷ 72), after the crop of a fill. Print: ≥ 300 ppi ideal,
≥ 200 acceptable for a poster, < 150 is visibly soft (preflight `lowResolution` uses `minPpi`). A 1920×1080 still
filling the full width of A3 (842 pt = 11.7 in) is **164 ppi** — acceptable for a poster viewed at a metre, soft at
reading distance; say so in the report and ask LightCraft for a larger export if it matters. Screen: the image
needs ≥ the frame's pixel size × render scale (1080 px wide frame at scale 1 needs ≥ 1080 px of image across it).

### Poster script (verified; 1080×1350, renders as expected — re-run 2026-10-27 on 0.13.0, same result)
```text
file.new {"width": 1080, "height": 1350, "facingPages": false, "margins": 72, "title": "Poster"}
swatch.create {"name": "ink", "color": "#1B1612"}
swatch.create {"name": "paper", "color": "#F5EFE6"}
swatch.create {"name": "coral", "color": "#F0644B"}
frame.create {"rect": [0, 0, 1080, 1350]}
object.fill {"swatch": "paper", "ids": ["$4.id"]}
object.stroke {"swatch": "[None]", "ids": ["$4.id"]}
frame.create {"rect": [0, 0, 1080, 860], "content": "graphic"}
file.place {"path": "C:/…/stills/still-hero.jpg", "frame": "$7.id"}
object.fittingOptions {"fitting": "fillProportionally", "align": 4, "ids": ["$7.id"]}
frame.create {"rect": [72, 900, 1008, 1080], "content": "text", "text": "THREE LOOKS"}
selection.set {"ids": ["$10.id"]}
type.char {"attrs": {"fontFamily": "Source Serif 4", "fontStyle": "Bold", "size": 120, "leading": {"kind": "points", "value": 120}, "tracking": -10, "fill": "ink"}}
type.para {"attrs": {"align": "center"}}
frame.create {"rect": [72, 1120, 1008, 1180], "content": "text", "text": "26 · 09 · 2026"}
selection.set {"ids": ["$14.id"]}
type.char {"attrs": {"fontFamily": "Source Sans 3", "fontStyle": "Semibold", "size": 36, "tracking": 150, "fill": "coral"}}
type.para {"attrs": {"align": "center"}}
preflight.run {"minPpi": 150}
font.list {}
```
`designcraft-cli script poster.dcs --save poster.designcraft` then
`designcraft-cli run --in poster.designcraft --scale 1 --export poster.png --scale 0.25 --export poster-thumb.png`.
At 140 pt the headline wrapped to two lines in a 180 pt-high frame and vanished entirely (overset) — the PNG showed
an empty band; preflight caught it. Always check.

### Parent pages and multi-page documents (verified)
`file.new {"preset":"A3","facingPages":false,"pages":2,"bleed":8.504}` → every page uses parent `A-Parent` by default;
`frame.create {"spread":{"kind":"parent","index":0}, …}` puts furniture (header, folio, footer line) on every page.
Page *n* (0-based) is `"spread": n`. `layout.parents.new {"prefix":"B","name":"Board"}` → `{id, prefix}`; apply with
`layout.pages.applyParent`. Parent items draw **under** page items — a full-bleed background on a page hides the
parent's footer (put backgrounds on the parent too, or furniture on the page). Page-number markers in folios:
**UNVERIFIED** — there is no `type.insertSpecial` (2026-10-27); try `variables.define` / `variables.insert` (types
include `lastPageNumber`, `runningHeader`) or `describe text.insert`.

### Formatting part of a story
`text.select {"story": S, "anchor": a, "focus": b}` (byte offsets; count UTF-8 bytes in Node:
`Buffer.byteLength(prefix)`), then `type.char` / `style.character.apply {"name"}` (runs without error, 2026-10-27; look at the render). Simpler and verified:
one frame per typographic role (headline, deck, date) — the usual way to build posters anyway.

## Verify (every page, every time)
1. **Look at it:** render each page to PNG (`run --all-pages`, `ui.render`, or MCP `render_page`) and Read the PNG.
   Check at full size and at thumbnail size (scale 0.25) for hierarchy and legibility.
2. **Overset:** `document.inspect` → every `stories[].overset` is `false` (not `story.get`, see above).
3. **Preflight:** `preflight.run {"minPpi": 200}` (print) → `{errors, warnings, issues}`. Fix every `overset`
   (severity error: "Overset text: 11 characters"), `missingFont`, `missingGlyphs`, `missingLink`; judge
   `lowResolution` ("effective 45 ppi (< 150)" — the ppi is computed from the frame size in points, so on a
   px-as-pt screen document read it as "image px per 72 page px": ≥ 72 means 1:1 or better); `rgbColor` is
   expected for hex swatches (fine for screen, note it for print).
4. **Fonts:** `font.list` — every entry `missing: false` **and** `styleMissing: false`. A missing family is drawn
   with a substitute (and highlighted pink in the app); a missing style falls back to another style of the family.
5. **Exports:** confirm the files exist and their sizes; PNG dimensions from the CLI's `wrote … (W×H …)` line.

## Fonts
Bundled (always available, also on other machines): **Source Serif 4** (Regular, It, Semibold, Bold, BoldIt —
the document default, 12 pt), **Source Sans 3** (Regular, It, Semibold, Bold), **Inter** (Regular, Medium,
SemiBold), **JetBrains Mono** (Regular). Installed Windows fonts are also loaded (`C:\Windows\Fonts`, user fonts):
verified on this machine (`source: installed`, style found): **Georgia** (Regular/Bold/Italic/Bold Italic),
**Palatino Linotype** (Bold…), **Cambria** (Bold…), **Constantia**, **Times New Roman**, **Segoe UI**
(Semibold…), **Bahnschrift** (Regular only), **Franklin Gothic Medium**; also present in `C:\Windows\Fonts`:
Calibri, Candara, Corbel, Arial, Verdana, Trebuchet MS, Tahoma, Consolas, Roboto Regular.
**Variable system fonts don't resolve their named styles** (verified): `Sitka` + "Banner"/"Bold"/"Regular",
`Segoe UI Variable` + "Display Semibold", `Bahnschrift` + "Bold"/"SemiBold" all report `styleMissing: true`, and
"Sitka Banner" as a family is missing. Don't use them. No Didone (Bodoni/Didot) is installed: for an elegant
high-contrast serif title the best choices here are **Source Serif 4** (Semibold/Bold, tight tracking at display
sizes — bundled, so it also renders identically everywhere), Palatino Linotype or Georgia. Use the project's fonts
from `handoff.md`; family and style names must match exactly (`fontStyle` "Bold", "Semibold", "SemiBold" for Inter,
"It" style names are "Italic"…) — always confirm with `font.list`.

## Pitfalls
1. **`file.place` without `frame` goes into the selected empty/graphic frame** — including an already-placed image
   frame (replacing its picture). Always pass `frame` (place into a frame you made) or `edit.deselectAll` first.
2. Coordinates are rects of corners in points, spread space; facing pages shift x. Use `facingPages: false`.
3. Frames made with `content: "unassigned"` have a 1 pt black stroke: `object.stroke {"swatch":"[None]"}`.
   (2026-10-27: frames with no `content` no longer get one; the `[None]` call in old scripts is harmless.)
4. `type.char` / `type.para` / style apply act on the **selection**. `frame.create` with `text` leaves a *caret*
   (empty range) at the end of the story: `type.char` then only changes the typing format and **silently does
   nothing to the text** (returns `null`, no error) while `type.para` does apply. Always
   `selection.set {"ids":[frameId]}` before formatting a frame (verified — this cost a whole test run).
5. `fill` in text attributes is a swatch name — create the swatch first (`swatch.create`).
6. `run`'s PNG export includes the bleed; `script --export x.png` exports page 1 only at scale 2.
7. DesignCraft writes without asking — check the target doesn't exist before every save/export.
8. `designcraft-cli app` defaults to port 7979; pass `--port 9877`.
9. Text-selection offsets are UTF-8 bytes, not characters.
10. Large placed images are embedded whole in PDFs (no downsampling): use `compressImages` for screen PDFs.
11. `story.get`'s `overset` lies for fully overset text; trust `document.inspect` / preflight and look at the PNG.
12. Script `$N` indices count commands only; a `#` comment line shifted every reference by one in the first test.
13. Placed SVGs keep their text and colours (VectorCraft lockup SVG verified) — prefer SVG over PNG for logos;
    a light-on-dark lockup on a white page is invisible, pick the right variant.
14. The `.designcraft` file embeds the placed images (≈ the image's size) and keeps the link path.
