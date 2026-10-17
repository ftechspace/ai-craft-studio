# Driving EffectCraft — operations manual

Everything here was verified against EffectCraft 0.7.0 on this machine (Windows 11, 10 Oct 2026) unless marked
**UNVERIFIED**. Paths are relative to `C:\CodeHouse\AIFilmEditor\`. The test project from that verification is in the
session scratchpad (`…/scratchpad/effectcraft-test/`), not kept in the repo.

## Binaries and setup

| What | Path |
|---|---|
| Desktop app | `apps\effectcraft\target\release\effectcraft.exe` (`--control <port>`, `--demo`, or a `.ecproj` / media files as args) |
| Headless CLI + MCP server | `apps\effectcraft\target\release\effectcraft-cli.exe` (`--help` lists subcommands) |
| Control client | `node tools\craft.js effectcraft …` (port **9875**) |
| Probe a rendered file | `apps\filmcraft\target\release\filmcraft-cli.exe probe <file>` (codec, fps, frames, alpha) |

Rebuild after `git pull`: `sh tools/build-apps.sh effectcraft` (≈10 min incremental). App docs:
`apps/effectcraft/docs/agents.md` (full MCP/CLI cookbook), `control-protocol.md`, `effects.md`, `footage.md`, `gaps.md`.

In the examples `E` = `apps/effectcraft/target/release/effectcraft-cli.exe` (Git Bash; single-quoted JSON works as is).

## Three ways in

| Interface | Use it for | Notes |
|---|---|---|
| **CLI** (`effectcraft-cli`) | the default: build, check and render headless, no window | each call is a fresh engine: open a project, run commands, `--save`/`--save-as` |
| **Control channel** (`effectcraft.exe --control 9875`, `node tools/craft.js effectcraft …`) | when the user wants to watch, or to screenshot the UI | same engine commands via `engine.execute`; plus `ui.*` methods |
| **MCP** (`effectcraft-cli mcp`, headless or `--bridge 9875`) | when registered in `.mcp.json` | tools: `execute_command`, `get_comp`, `get_layer`, `set_property`, `add_keyframe`, `render_frame`, `batch`, `run_script`, `command_run`/`command_batch`/`doc_inspect`/`render_preview` … |

### CLI (verified)
```sh
$E run --empty comp.new '{…}' layer.newText '{…}' … --save-as C:/…/motion/intro.ecproj --json   # build
$E run motion/intro.ecproj prop.addKey '{…}' … --save --json                                    # edit in place
$E info motion/intro.ecproj                         # items, active comp (size, fps, duration), layers with ids
$E props <comp> <layer> motion/intro.ecproj         # every property path + value + key count
$E get <comp> <layer> <path> --time 4.77 motion/intro.ecproj --json     # value at a comp time, keys with their times
$E render-frame motion/intro.ecproj --comp Intro --time 1.2 --out check.png [--max-side 960] [--transparent] [--frame N]
$E render motion/intro.ecproj --comp Intro --out motion/intro.mp4       # H.264 MP4 (format from the extension)
$E commands --filter mask --empty                    # discover command ids + params doc
$E exec layer.newNull '{}' --bridge 9875             # any command against the running app
$E script build.jsx --save-as x.ecproj               # After Effects-style JavaScript (app.project, layers.addText…) UNVERIFIED here
```
- **`run`/`exec`/`info`/`props` open the DEMO project unless you pass a `.ecproj` or `--empty`.** `render` without a
  project renders the demo. Always pass the project path (or `--empty` to start fresh).
- `run` takes `<id> '<json>'` pairs in order; one failing step aborts the whole call and **nothing is saved** (the
  error names the step). Re-run the corrected call against the last saved file.
- `--save` writes back to the opened project; `--save-as` a new path. Relative paths resolve against the working
  directory. `--save-as` silently overwrites — check the target doesn't exist (never-overwrite rule).
- Errors: exit 1 and `{"error": …}` with `--json`; unknown parameter keys are rejected with the accepted list.

### Control channel (verified, matches `tools/craft.js`)
- Start: `node tools/craft.js effectcraft --start` (spawns `effectcraft.exe --control 9875`; window opens without
  stealing focus, port is up in ~2 s). The app starts with an empty Untitled project.
- Protocol: TCP 127.0.0.1, JSON lines. Request `{"id","method","params"}` → reply `{"id","ok":true,"result"}` or
  `{"id","ok":false,"error":"message string"}`. No auth token. Engine commands are `engine.execute {command, params}`
  (what `craft.js <cmd> '<json>'` sends). 16 connections max; 60 s per request.
- Useful: `node tools/craft.js effectcraft file.open '{"path":"C:/…/intro.ecproj"}'`, `comp.open {"comp":"Intro"}`,
  `time.set {"time":1.5}` (moves the CTI; reply has `frame` and timecode), `project.summary`, `comp.info`.
- `--ui render.frame '{"time":1,"max_side":960,"path":"C:/…/f.png"}'` renders a comp frame (GPU in the app).
- `--ui ui.screenshot '{"path":"C:/…/shot.png"}'` = the whole window (or `"panel":"Timeline"`).
- `--ui ui.set '{"viewer":{"zoom":null}}'` fits the viewer; `--ui ui.playback '{"action":"play"}'`.
- Close: `node tools/craft.js effectcraft --ui app.quit '{"force":true}'` (force skips the save prompt — save first
  if the work matters; without force a modified project shows Save / Don't Save / Cancel).

### MCP
`.mcp.json` entries (UNVERIFIED as registered servers; the same binary was verified speaking MCP over stdio in both modes):
```json
"effectcraft":     {"command": "C:/CodeHouse/AIFilmEditor/apps/effectcraft/target/release/effectcraft-cli.exe", "args": ["mcp", "--autosave"]},
"effectcraft-app": {"command": "C:/CodeHouse/AIFilmEditor/apps/effectcraft/target/release/effectcraft-cli.exe", "args": ["mcp", "--bridge", "9875"]}
```
Headless MCP starts with an **empty** project (CLI subcommands default to the demo); `--autosave` checkpoints unsaved
work after each edit; still `save_project {"path"}` at milestones. Bridge mode needs the app already running with
`--control 9875` and adds `screenshot`, `ui_*`. MCP tool args: layers by id, `"#n"` or name; times in seconds.

## Units and coordinates (verified)
- **Time is seconds** everywhere (not FilmCraft ticks). Keyframe times are **layer time** (= comp time unless the
  layer starts later or is stretched; precomp layers placed later need the offset subtracted).
- **Frame rate 29.97** → stored as 30000/1001 exactly. Comp `duration` and key times **snap to whole frames**:
  `duration 2` → 60 frames = 2.002 s; `4.8` → 144 frames = 4.8048 s; `7.2` → 216 frames = 7.2072 s; a key at 0.6 lands
  at 0.6006 (frame 18). Think in frames: `t = frame × 1001 / 30000`; `frame = round(t × 30000/1001)`.
- Positions are comp pixels, origin top-left (`[960,540]` = centre of 1920×1080). Transform values are 3D
  (`[x,y,z]`, scale `[x,y,z]` %) — 2-element arrays are accepted on `prop.set`.
- Colours: `"#RRGGBB"` on create params; properties read back as `[r,g,b,a]` 0–1.
- New layers go on **top** of the stack (`#1`). Name every layer (`name`) and refer to it by name.
- Text layer origin = the **baseline** at `position`; with `justify:"center"` the line is centred on x. Cap height
  sits above y (a 120 px Inter line at y 700 spans ≈ y 612–700).
- Shape layer from `layer.newShape`: layer position = shape centre.
- Image/footage layers: anchor at the image centre, placed at `position` (default comp centre).

## Building blocks (all verified unless marked)

### Composition
`comp.new {"name":"Intro","width":1920,"height":1080,"frameRate":29.97,"duration":4.8,"background":"#1B1612"}` →
`{comp}`; it becomes active. `comp.settings {comp?, duration?, frameRate?, background?, …}` edits;
`comp.open {"comp":"Intro"}` switches the active comp; `comp.info {comp?}` → size, fps, duration, layers with in/out.
`comp.setSwitch {"switch":"motionBlur","value":true}` turns on comp motion blur (shutter via `comp.settings
{shutterAngle:180}`). Work area: `comp.workArea {start,end}`.

### Layers
| Command | Params (main ones) | Notes |
|---|---|---|
| `layer.newText` | `{text, name, font, style, size, fill, tracking, leading, justify, position, box?, allCaps?}` | `tracking` in 1/1000 em (200 = airy caps). `box:[x,y,w,h]` makes paragraph text |
| `layer.setText` | `{layer, range?:[start,end], text?, font?, style?, size?, fill?, tracking?, …}` | restyle all or a character range |
| `layer.newShape` | `{kind: rect\|rounded\|ellipse\|star\|polygon\|none, name, size:[w,h], fill, stroke, strokeWidth, position}` | `rounded` = roundness 30 (`contents/group/contents/rect/roundness`) |
| `layer.addShapeItem` | `{layer, kind: rect\|ellipse\|path\|fill\|stroke\|trim\|repeater\|round\|offset\|…, group?}` → `{uid, path}` | `trim` → `contents/trim/start|end|offset` for draw-on strokes |
| `layer.newSolid` | `{name, color, width, height}` | full-frame plate: give it the comp size |
| `layer.newNull` | `{name}` | parent several layers with `layer.setParent {layers, parent}` |
| `file.import` | `{paths:[abs…], sequence?:false}` → `{items:[id], errors, warnings}` | PNG (alpha kept), JPEG, SVG, PSD, PDF/AI, MOV/MP4, WAV… |
| `layer.addItem` | `{item: id\|name, position?, time?, duration?, index?}` → `{layer}` | puts an imported item in the active comp |
| `layer.create` | `{"op":"shapesFromVector"}` on the **selected** SVG/PDF/AI layer (`layer.select {"layers":[…]}` first) | makes "<name> Outlines" shape layer (editable fills/strokes, trim-able) and hides the source layer |
| `layer.precompose` | `{layers, name, mode:"move"}` → `{comp, layer}` | |
| `layer.setTrackMatte` | `{layer, matte: layer\|null, kind: alpha\|alphaInverted\|luma\|lumaInverted}` | UNVERIFIED render |
| `layer.setSwitch` | `{layers, switch: motionBlur\|video\|threeD\|lock\|…, value}` | `video:false` hides a layer |
| `layer.timing` | `{layers, start?, in?, out?}` (comp seconds) | |
| `layer.rename`, `layer.arrange {layers, above\|to}` | | |

### Properties and keyframes
- `prop.set {layer, path, value}` — static value (no keys). `prop.addKey {layer, path, time, value}` — adds a key and
  turns animation on. `prop.reset {layer, path}` — removes keys/expression.
- Paths: `transform/position`, `transform/scale`, `transform/rotation`, `transform/opacity`, `transform/anchor`;
  shape internals `contents/group/contents/rect/size`, `contents/group/contents/fill/color`,
  `contents/trim/end`; masks `masks/mask/path|feather|opacity|expansion`; effects `effects/#1/<param>`; text
  animators `text/animators/animator/selectors/rangeSelector/offset` … `props <comp> <layer>` lists them all.
- **Easing (verified by sampling values):** new keys are Bezier but with *linear speed* — motion is linear until you
  ease it. Select the keys, then:
  - `keys.easyEase {}` (F9; `{"which":"in"|"out"}`) — standard 33 % ease both sides.
  - `keys.velocity {"inSpeed":0,"outSpeed":0,"outInfluence":30,"inInfluence":85}` — a strong "arrive and settle"
    ease-out (measured: 16 % of the distance after ⅙ of the time, 59 % at ⅓, 99 % at ⅚). **`inSpeed`/`outSpeed: 0`
    are required** — influence alone keeps the linear speed and nothing changes.
  - Per key: `keys.setEase {layer, path, time, side: in|out, speed, influence}`. `keys.interpolation
    {"interpolation":"hold"|"linear"}`.
  - Select keys: `keys.select {"keys":[{"layer":"Frame","path":"transform/position","time":0},{…,"time":0.6006}]}`
    — use the **snapped** key times (read them with `get … --json`, `keys[].time`). The reply is the count selected:
    check it equals the number you meant.
  - MCP `add_keyframe {layer, path, keys:[{time,value}], interpolation:"easyEase"}` does keys + ease in one call.
- Expressions: `prop.setExpression {layer, path, expression}` (MCP `set_property {…, expression}`) UNVERIFIED here.

### Masks (reveals and wipes)
`layer.addMask {layer, shape:"rect", rect:[x,y,w,h]}` (layer space; for text, origin = baseline point) → `{mask}`.
Animate the path with `prop.addKey {layer, path:"masks/mask/path", time, value}` where value is the full path object:
`{"closed":true,"vertices":[[x,y]×4],"in_tangents":[[0,0]×4],"out_tangents":[[0,0]×4]}` (omitting the tangents →
"bad value"). Feather `prop.set {path:"masks/mask/feather", value:[40,40]}`. Verified: a left-to-right wipe on text.

### Text animators
- Presets: `layer.applyTextPreset {layer, preset: typewriter|fadeUpCharacters|bounceInWords|trackingIn|scramble|blurIn|jitter|dropInLines}`
  → keys `rangeSelector/offset` −100→100 from the layer's start over 1.5 s (verified `fadeUpCharacters`: opacity 0 +
  y +40 per character). Retime by moving/replacing those two keys and easing them.
- Build your own: `layer.addTextAnimator {layer, properties:[opacity, position, scale, tracking, blur, fillColor…]}`,
  `layer.addTextSelector {layer, kind: range|wiggly|expression}`, then key `…/rangeSelector/start|end|offset`.
- Avoid `bounceInWords`, `jitter`, `scramble` for premium work.

### Effects
`effect.apply {layers:["Title"], effect:"Gaussian Blur"}` → `{effects:[uid], paths:["effects/#1"]}`, then
`prop.set {layer, path:"effects/#1/blurriness", value}`. `commands`/`list_effects` (MCP) list 306 effects. Layer
styles (Drop Shadow…) exist. UNVERIFIED in this session beyond the docs.

### Fonts (verified)
`exec text.fonts '{}' --empty --json` → `{count, families:[{family, styles, origin}]}` (83 here). Bundled: Inter
(Regular, Medium, SemiBold, Bold, Italic), Noto Serif (Regular only), JetBrains Mono. System serifs: Georgia, Times New
Roman, Cambria, Constantia (R/B/I/BI); Segoe UI (all weights), Bahnschrift. **No high-contrast display serif**
(Didot/Bodoni/Playfair) is installed — for the THREE LOOKS wordmark use VectorCraft's SVG/PNG, not live text.
A font installed after launch needs `text.fonts {"rescan":true}`. Use `font` + `style` exactly as listed.

## Seeing your work
1. **Frames:** `$E render-frame p.ecproj --comp Intro --time T --out motion/checks/intro_fNNN.png` (or `--frame N`),
   then Read the PNG. 1080p CPU frame ≈ 15–250 ms. `--transparent` keeps alpha (comp background dropped). Check first
   frame, each move's mid/settle, the hit frame, the hold, the last frame.
2. **Numbers:** `get <comp> <layer> transform/position --time T --json` (value + keys). Sample a few times to confirm
   the ease shape; check the settle value at the hit frame.
3. **The rendered file:** `filmcraft-cli probe out.mp4` (codec, `frame_rate` 30000/1001, `duration` ticks /
   254016000000 = seconds, `has_alpha`). Re-import into a scratch comp with a `#00ff00` background
   (`file.import` + `layer.addItem`) and `render-frame` to see the real decoded pixels and alpha.
4. **The app (when the user watches):** open the project via the control channel and `ui.screenshot`.

## Rendering (verified)
| Deliverable | Command | Result here |
|---|---|---|
| H.264 MP4 (opaque) | `$E render p.ecproj --comp Intro --out motion/intro.mp4` | H.264 High, 4:2:0 8-bit, Rec.709 limited, 30000/1001, 15 Mbps default, no audio stream; 60 frames in 23 s (CPU) |
| ProRes 4444 + alpha | `… --out x.mov --format prores --prores 4444 --channels rgba` | `has_alpha: true`, YUVA 4:4:4 12-bit, ~85 Mbps; alpha checked over green |
| PNG sequence + alpha | `… --out seq/intro_[####].png --channels rgba [--start 0 --end 0.2]` | `intro_0000.png …` (numbering from 0) |
| Other | `--format hevc\|av1\|webm\|gif\|jpeg\|tiff\|exr`, `--bitrate KBPS`, `--resolution half`, `--fps N`, `--audio off` | UNVERIFIED |

- `render` re-queues only that comp (the project's own queue is unqueued) and **overwrites an existing output file** —
  check first. `--queue` renders the project's Render Queue as saved.
- In the app: `renderQueue.add {comp, format, output, channels, proresProfile}` then `renderQueue.render
  {"wait":true}` (or `wait:false` + `jobs.list`). The CLI `render` refuses `--bridge`.
- **RGBA renders drop the comp background colour** (as in After Effects). For an opaque MP4 the background colour
  is used; if a piece must be opaque in an RGBA format, put a solid layer at the bottom.
- CPU render ≈ 0.4 s/frame at 1080p with blur/text: a 216-frame end card ≈ 1.5 min. `--gpu` UNVERIFIED for render.
- MP4 has no audio track unless the comp has audio layers; the film-editor adds music in FilmCraft.

## Recipe: 2-second test (the verification run)
```sh
$E run --empty \
 comp.new '{"name":"Test","width":1920,"height":1080,"frameRate":29.97,"duration":2,"background":"#1B1612"}' \
 layer.newText '{"text":"THREE LOOKS","name":"Title","size":120,"fill":"#F5EFE6","tracking":200,"justify":"center","position":[960,700]}' \
 layer.newShape '{"kind":"rounded","name":"Frame","size":[300,200],"fill":"#D08C5B","position":[960,400]}' \
 prop.addKey '{"layer":"Frame","path":"transform/position","time":0,"value":[-200,400]}' \
 prop.addKey '{"layer":"Frame","path":"transform/position","time":0.6,"value":[960,400]}' \
 keys.select '{"keys":[{"layer":"Frame","path":"transform/position","time":0},{"layer":"Frame","path":"transform/position","time":0.6006}]}' \
 keys.velocity '{"inSpeed":0,"outSpeed":0,"outInfluence":30,"inInfluence":85}' \
 comp.setSwitch '{"switch":"motionBlur","value":true}' \
 layer.setSwitch '{"layers":["Frame"],"switch":"motionBlur","value":true}' \
 --save-as test.ecproj --json
$E render-frame test.ecproj --time 0.3 --out f.png      # motion-blurred mid-move; look at it
$E render test.ecproj --comp Test --out test.mp4        # 60 frames, 29.97
```
SVG mark: `file.import {"paths":["C:/…/graphics/logo-mark.svg"]}` → `layer.addItem {"item":"logo-mark.svg"}` →
`layer.select` → `layer.create {"op":"shapesFromVector"}` (vector shapes, crisp at any scale). PNG lockup:
`file.import` + `layer.addItem`, scale via `transform/scale` (import PNGs at ≥ display size; 3840-wide PNG at 50 % on
1080p is ideal).

## Pitfalls
1. CLI subcommands default to the **demo project** — always pass the `.ecproj` or `--empty`.
2. Keys snap to frames; select them by their snapped time or the selection silently matches fewer keys.
3. Keys without easing move linearly; `keys.velocity` needs speed 0 to ease.
4. Mask path values need `in_tangents`/`out_tangents`.
5. `mask rect` is `[x, y, w, h]` in layer space, not two corners.
6. A comp of `duration 4.8` at 29.97 is 144 frames (0–143, last frame at 4.7714 s); film time 4.8 s is frame 144 —
   the first frame **after** such a clip. Plan the hit inside the clip (frame 143 at the latest) or make it longer.
7. `--save-as` and `render --out` overwrite without asking.
8. `layer.create shapesFromVector` hides the original SVG layer and adds "<name> Outlines" above it; animate the
   Outlines layer. It has one group per SVG element in **reverse** order: `contents/group` = the SVG's last
   element (topmost), `contents/group#2`, `#3` … = earlier ones — so each frame of the three-frame mark can be keyed
   separately via `contents/group#N/transform/position|scale|opacity` (group positions start at [0,0], relative).
9. Headless renders are CPU; heavy blurs/glows over many frames are slow — check a few frames before a full render.
10. RGBA output drops the comp background (see Rendering).
