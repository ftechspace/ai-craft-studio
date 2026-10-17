# Driving FilmCraft — operations manual

Everything here was verified against FilmCraft 0.4.0 on this machine unless marked **(verify on first use)**.
Paths are relative to `C:\CodeHouse\AIFilmEditor\`.

## Binaries and setup

| What | Path |
|---|---|
| Desktop app (release, fast) | `apps\filmcraft\target\release\filmcraft.exe --control 9876` (or double-click `start-filmcraft.cmd`) |
| Headless CLI | `apps\filmcraft\target\release\filmcraft-cli.exe` (`help` lists subcommands) |
| Contact sheets | `apps\filmcraft\target\release\examples\contact.exe` |
| Control client | `node tools\fc.js` |
| Plan → live cut | `node tools\cut.js plan.json` |
| Outputs | `output\` (projects `.fcproj`, exports `.mp4`, plans, selects) |

The debug build (`target\debug\`) is 5–10× slower; never use it for playback or export. Rebuild after source changes:
`cargo build --release -p filmcraft -p filmcraft-cli` (≈18 min clean, minutes incremental; cargo is in `%USERPROFILE%\.cargo\bin`).

Check the app is up: `node tools\fc.js project.inspect`. If it isn't, ask the user before launching it (it opens a window).
A second instance for experiments: `filmcraft.exe --control 9877` and `FILMCRAFT_PORT=9877 node tools\fc.js …`; quit it with
`node tools\fc.js --ui app.quit`.

## Plan format (`tools/cut.js`)

Write plans to `output/<name>.plan.json`. Unknown keys (e.g. `"note"`) are ignored, so annotate freely.

```jsonc
{
  "newProject": "Name",                 // optional, live only: start a fresh project (ask the user first)
  "saveAs": "C:/…/output/x.fcproj",     // optional: else file.save into the open project
  "sequence": {"name": "Cut v1", "width": 1920, "height": 1080, "fps": 29.97},
  "media": {"kiss": "D:/footage/…/A.MP4"},  // short keys → absolute paths (reuses already-imported files by name)
  "shots": [
    {"m": "kiss", "at": 21.2, "len": 2.5,   // source time the shot centres on (s), seconds on the timeline
     "speed": 50,                           // %, use the clean conform (timeline fps ÷ capture fps)
     "in": "dip_to_white", "frames": 3,     // cut | fade | cross_dissolve | film_dissolve | dip_to_black | dip_to_white; frames = length
     "out": "fade", "outFrames": 45,        // last shot: fade to black
     "push": [100, 108],                    // Motion scale keyframed across the shot (push-in; [108,100] = pull-out)
     "freeze": true,                        // hold the frame at `at` for `len` (photo moment)
     "grade": {"look": 6, "look_intensity": 100}}   // per-shot Lumetri on top of the global grade
  ],
  "sound": "camera",                    // or "off": each shot's own sound, real-time under slow motion, crossfaded
  "soundDb": -3,                        // optional absolute gain on the camera sound
  "music": {"path": "C:/…/song.wav", "db": -6, "fadeIn": 0.5, "fadeOut": 2, "duck": true},
                                        // A2; remixed to the film's length at beat boundaries, else cut to length;
                                        // ducked under the camera sound unless "duck": false
  "grade": {"temperature": 1, "look": 2, "look_intensity": 25},   // Lumetri on every shot (look = index)
  "titles": [{"text": "TITLE", "shot": 3, "offset": 0.3, "seconds": 2.4, "size": 84, "tracking": 300,
              "position": [960, 990], "fade": 0.5, "props": {"font_style": "Bold", "fill_color": "#ffffff"}}]
}
```

Also in a plan (all verified):
```jsonc
  "letterbox": 2.39,                    // black bars over the whole film, above all picture tracks
  // shots[i] extras:
  "panels": [{"m": "b", "at": 103}, {"m": "c", "at": 345}],   // split screen: this shot + panels side by side
  "sfx": {"path": "C:/CodeHouse/AIFilmEditor/sfx/shutter.wav", "offset": -0.05, "db": -4},  // on A3
  "texts": [{"text": "WE SHOT 3 LOOKS", "shot": 0, "offset": 0.3, "seconds": 2.5,
             "style": "vlog", "highlight": ["3 LOOKS"], "accent": "#FFD60A", "anim": "pop",
             "position": [960, 260], "size": 96, "color": "#FFFFFF", "props": {}}],
  "templates": [{"template": "builtin:lower-third-slab", "values": {"name": "…", "role": "…"}, "shot": 5, "offset": 0.5, "seconds": 4}],
  "titles": [ … ]                       // older simple titles (centred, tracked, cross-dissolved)
```
Text styles (defaults size/position): `vlog` (Inter Black, white, thick black outline, shadow — YouTube look; 96 px,
y 260), `pill` (dark bold text on an accent rounded box — labels; 40 px, y 880), `caption` (white bold on a 55 % black
box — what's happening; 46 px, y 960), `cinematic` (tracked 400, small; 40 px, y 980), `plain` (white bold + shadow;
60 px, y 200). `highlight` colours phrases in `accent`. Animations: `pop` (scale 0→115→100 in 8 frames),
`slide-up` / `slide-left` (10 frames + fade), `fade` (8 frames), `typewriter` (letter by letter), `words` (word by
word), `track` (tracking +250 across the text's life). Every text fades out over its last 6 frames.
Templates: `builtin:lower-third-slab` {name, role, slab_color, accent_color, text_color, show_role, font},
`builtin:lower-third-rule` {name, role, rule_color, font, name_size}, `builtin:title-centered` {title, subtitle,
title_size, title_color, accent, font}, `builtin:title-boxed` {title, text_color, box_color, box_opacity, position},
`builtin:callout-tag` {text, tag_color, dot_color, show_dot}, `builtin:callout-pointer` {label, color, pointer,
position}, `builtin:end-credits-roll` {heading, credits, font, color}, `builtin:ticker-crawl` {text, text_color, bar_color}.
Text keyframes by hand: `effects.addKeyframe {"clip","effect": <index of graphic_text in the clip's effects>,"param","time"}`
turns animation on, then `graphics.set {"clip","layer":0,"props":{param: value},"time"}`; params `scale`, `position`,
`opacity`, `rotation`, `tracking`, `text` (holds → typewriter), colours. `graphics.setCharStyle
{"clip","layer","start","end","style":{"color","fontStyle","size",…}}` styles a character range (of the text as it
reads at the playhead).

Frame maths: each shot is rounded to whole frames (and to whole source frames at its speed), so the total can drift
a frame or two from the sum of `len` — check the printed frame count against hard caps (30 s at 29.97 = ≤ 899 frames).
Not covered by plans (use `fc.js`): letterbox shapes, split screens, other keyframed effects, adjustment layers.

## Time and frames

- All engine time is integer **ticks: 254 016 000 000 per second**. `sourceIn`, `duration`, `time` take ticks.
  Many commands also take `seconds`, `frame` or `timecode` (not `timeline.place`'s `sourceIn`/`duration`).
- 29.97 = 30000/1001, 23.976 = 24000/1001, 59.94 = 60000/1001. Frames → ticks: `f × TPS × den / num`.
  Always compute from absolute frame counts, never by adding rounded seconds.

## Live and headless

- **Live (default):** tools talk to the running app on port 9876; the user watches. `node tools/cut.js plan.json`.
- **Headless (when the user asks, or for your own experiments):** `node tools/cut.js plan.json --headless out.fcproj`
  builds in a hidden `filmcraft-cli mcp` session (≈1 s for a short cut) and saves `out.fcproj`. In Node,
  `require("./tools/fc").connectHeadless(project?)` gives the same `cmd()` with real results (no UI methods).
  To show a headless result: `fc.js file.open '{"path":"…"}'` in the live app (ask if the user has unsaved work).
- `filmcraft-cli run script.jsonl --project in.fcproj --save-as out.fcproj` also works headless, but later lines
  can't use earlier results (ids are sequential) — prefer `connectHeadless`.

## Looking at footage

- **Probe** (length, fps, codec, audio, fast — no full read): a headless session doing `file.import` of every clip then
  `project.inspect` (durations) and `metadata.get {item}` (Frame Rate, Video Info, Video Codec, Audio Info) — 22 clips ≈ 3 s.
  `filmcraft-cli probe <file>` reads the whole file: fine for exports, slow on multi-GB camera files.
- **Contact sheets** (your eyes) — `contact.exe`, 5 columns, 384×216 cells, row-major; every run prints one JSON line
  per sheet with `times` and per-frame `levels`:
  - `contact.exe <dir> 20 <file>…` — one sheet per clip, frames evenly spread (at most one per 2 s). On long clips 20
    frames is sparse (one per 18 s on a 6-minute take): follow up with `range`.
  - `contact.exe <dir|x.jpg> range <file> <from> <to> <step>` — dense sampling of a source range (≤60 frames,
    ~3 s for 11 frames). Use 0.25–0.5 s steps around peak moments; ≥1 frame per 3–5 s to survey long takes.
  - `contact.exe <out.png|.jpg> frame <file> <seconds>` — one full-resolution frame of a clip (stills for LightCraft,
    storyboard frames, thumbnails).
  - `contact.exe <dir|x.jpg> program <project.fcproj> <seconds…>` — the project's active sequence (save first).
    `cut.js` prints the mid-shot times. Give a `.jpg` path to avoid overwriting `program.jpg`.
- **Levels** (a numeric waveform): each frame reports `y2`/`y50`/`y98` (Rec.709 luma percentiles, 0–100) and mean
  `rgb`. Read a white cyc/clothes from `y98` and the RGB balance (equal channels = neutral); shadows from `y2`; skin by
  rendering a tight `range` on a close-up. Typical targets: `y2` 2–8, white clothes ~85–90, cyc 90–100 and neutral.
- **Scene detection** (when clips contain several shots): place clips on a sequence, then
  `clip.sceneEditDetection {"clips":[…],"applyCuts":false,"generateMarkers":true,"wait":true}` → `clips[{clip, mediaCuts:[ticks]}]`.
- **One frame, full size:** `filmcraft-cli render --project p.fcproj --seconds S --out f.png --scale 0.5` (active
  sequence) or `file.exportFrame {"path","target":"source","item","time"}` (source, full-res PNG ~2.4 MB). **`time` must be ticks** (s × 254016000000): `seconds` is silently ignored and you get frame 0. Simpler: `contact.exe <out.png> frame <file> <s>`.
- **Screenshot the app** (what the user sees): `node tools\fc.js --ui ui.screenshot "{\"path\":\"C:/…/shot.png\"}"`.
- **Scene detection** (when clips contain several shots): place clips on a sequence, then
  `clip.sceneEditDetection {"clips":[…],"applyCuts":false,"generateMarkers":true,"wait":true}` → `clips[{clip, mediaCuts:[ticks]}]`.
- **Screenshot the app** (what the user sees): `node tools\fc.js --ui ui.screenshot "{\"path\":\"C:/…/shot.png\"}"`.
- The DJI `.LRF` files are 720p 29.97 previews of 59.94 clips: useless as proxies (FilmCraft requires equal fps and
  duration) but fine to skim.

## Core commands (engine, via `fc.js <id> '<json>'`)

### Project and sequences
| Command | Params | Notes |
|---|---|---|
| `file.newProject` | `{"name"}` | replaces the open project in memory — save first, and only when the user wants a new project |
| `file.open` / `file.save` / `file.saveAs` | `{"path"}` / `{}` / `{"path"}` | |
| `file.import` | `{"paths":[abs…]}` | → `{items:[ids], errors:[…]}`; per-file failures land in `errors` |
| `project.inspect` | `{}` | tree: nodes `{item, name, type: Movie/Audio/Sequence, duration(ticks), children}` |
| `file.newSequence` | `{"name","width","height","fps","video":3,"audio":2}` | becomes active; `fromItem` copies a clip's settings but also places it |
| `sequence.open` | `{"item": sequenceItemId}` | switch the active sequence (id from `project.inspect`) |
| `sequence.inspect` | `{}` | `video[n].items[{clip,item,name,start,duration,sourceIn,speed,effects}]`, `audio`, `settings{width,height,frame_rate{num,den}}`, `duration` |
| `metadata.get` | `{"item"}` | fields incl. Frame Rate, Video Info, Video Codec, Audio Info |

### Editing
| Command | Params | Notes |
|---|---|---|
| `timeline.place` | `{"item","track":"V1","time","sourceIn","duration","audio":false}` | → `clips:[video, audio…]`. `track:"A1"` places sound only. **Does not stop at the end of the media — clamp `sourceIn + duration` yourself.** |
| `clip.speedDuration` | `{"clips":[id],"speed":50,"ripple":true}` | timeline length scales exactly (2× at 50%). Linked audio would follow — place picture with `audio:false` |
| `playhead.set` | `{"time"}` or `{"seconds"}` | move it as you build so the user can follow |
| `sequence.applyVideoTransition` | `{"clip","effect","frames","edge":"in"/"out"}` | effects: `cross_dissolve`, `film_dissolve`, `dip_to_black`, `dip_to_white`. Abutting neighbour → centred on the cut; lone edge → fade from/to black or transparent (on upper tracks) |
| `sequence.applyAudioTransition` | `{"clip","effect":"constant_power","frames","edge"?}` | same rules; `constant_gain`, `exponential_fade` also exist |
| `clip.audioGain` | `{"clips","mode":"set","db"}` | default mode is relative (`adjust`) |
| `timeline.razor` | `{"time","track"?,"clip"?}` | |
| `timeline.select` | `{"clips":[…]}` | most commands take `clips`/`clip` directly, no selection needed |
| `clip.frameHoldOptions` | `{"clips","enabled":true,"holdOn":"in"}` | freeze frame of the clip's In frame (verified) |
| `clip.insertFrameHoldSegment` | `{"clip","time","seconds"}` | freeze a section mid-clip **(verify on first use)** |
| `file.newAdjustmentLayer` | `{"seconds"}` | → item; place on the top track, put the look on it **(verify on first use)** |
| `clip.remix` | `{"clip","duration":ticks}` | retimes music to a length at beat boundaries; fails on beatless audio ("no beat found") |

### Colour (Lumetri)
`effects.apply {"clips":[…],"effect":"lumetri"}`, then per clip
`effects.setParam {"clip","effect":"lumetri","param","value"}`.

| Param | Range | Param | Range |
|---|---|---|---|
| `temperature`, `tint` | −100…100 | `exposure` | −5…5 |
| `contrast`, `highlights`, `shadows`, `whites`, `blacks` | −100…100 | `saturation` | 0…200 (100 = none) |
| `vibrance`, `sharpen` | −100…100 | `faded_film` | 0…100 |
| `look` | **integer** 0 None, 1 Teal & Orange, 2 Warm Film, 3 Cool Blue, 4 Bleach Bypass, 5 Faded Matte, 6 Monochrome, 7 Golden Hour, 8 Night | `look_intensity` | 0…200 (100 = full) |
| `vignette_amount` | −5…5 | `vignette_midpoint`, `vignette_feather` | 0…100 |
| `input_lut`, `look_lut` | text: `builtin:look-warm-film` etc. or a `.cube` path | | |

Also: `lumetri.setInputLut {"clip","path"}` for log conversion LUTs, `lumetri.applyMatch` (match to a reference frame),
`lumetri.presets` / `lumetri.applyPreset`. Choice params reject names — pass the index.
**Crash risk (2026-10-10, vlog-29th):** two `sequence.renderInToOut` jobs at once on long (30 min) sequences of HEVC
+ 4K60 footage crashed the app (fail-fast 0xc0000409 inside GPU HEVC decoding; the log showed 331 hardware-decoder
sessions). Run **one** preview render at a time, only for the sequence on screen, and save before starting it.
**Lumetri bug (found 2026-10-10, vlog-29th):** with Shadows > 0 **and** Blacks < 0 **and** Temperature or Tint ≠ 0 at
the same time, near-black pixels turn into saturated red/green blocks (seen on a dark taxi dashboard). Set any one of
them to 0 — keep **Shadows at 0** by default — and check dark interiors with `contact.exe program` after grading.

Grades tried on bright Rec.709 DJI studio footage (white cyc, darker skin), measured with contact levels:
- **Warm** (on the user's first two cuts, which they saw): `{"temperature":9,"tint":2,"exposure":0.25,"contrast":20,
  "highlights":-15,"shadows":5,"whites":5,"blacks":-15,"saturation":102,"vibrance":18,"look":2,"look_intensity":30,
  "vignette_amount":-0.6}` — cyc warms to ≈R191/G187/B179, white clothes ≈80 %. Cosy, but the whites aren't clean.
- **Clean-warm** (measured better): `{"temperature":1,"tint":1,"exposure":0.1,"contrast":20,"highlights":10,"shadows":0,
  "whites":25,"blacks":-15,"saturation":100,"vibrance":15,"look":2,"look_intensity":25,"vignette_amount":-0.5}` —
  cyc ≈R197/G197/B192 (near neutral), white clothes 84–86 %, skin ≈R117/G82/B61 (dense, warm).
- Avoid: `highlights −30`, `faded_film 6`, `look_intensity 40` — turned the cyc dull beige.
The "never raise global exposure" rule is about brightening dark skin; small exposure moves to set the white point are fine.

### Motion, keyframes, text, shapes
- Motion params: `scale` (%), `position` `[x,y]` (sequence px, centre 960,540), `rotation`, `anchor`.
  Opacity: effect `opacity`, param `opacity` 0–100.
- Keyframes: `effects.addKeyframe {"clip","effect":"motion","param":"scale","time":ticks}` turns animation on (it's a
  toggle — calling it on an existing key removes it); then `effects.setParam` with `"time"` sets values at times.
  `setParam` without existing keys only sets the static value. Easing: `effects.setInterpolation {…,"mediaTime","interpolation":"easeIn|easeOut|bezier|…"}` (media ticks).
- Text: `graphics.newText {"text","size","seconds"(= duration),"time"(ticks),"position":[x,y]?,"font"?,"fontStyle"?,"box":[w,h]?,"track"?}` → `{clip}`
  (`graphics.set` without `clip` acts on the text just created);
  style with `graphics.set {"clip","props":{"align":"center","tracking":300,"shadow":true,"fill_color":"#ffffff","font":"Inter","font_style":"Bold","opacity":100}}`.
  Default position is frame centre; `align:"center"` is needed to centre the text on it.
- Shapes: `graphics.newShape {"shape":"rectangle","position":[x,y],"size":[w,h],"seconds","clip"?}` (pass `clip` to add a
  second layer to the same graphic) — for letterbox bars 1920×138 at top and bottom for 2.39:1 **(verify the position
  anchor by screenshot)**.
- Templates: `graphics.template.list`, `graphics.template.apply {"template":"builtin:lower-third-slab","values":{…}}`.

### Sound
- Camera sound under picture: place sound-only clips (`track:"A1"`) under each shot with the **shot's source In at real
  time** — under slow motion this gives natural, unpitched sound. 6-frame `constant_power` crossfades at every cut,
  1 s fade in, 1.5 s fade out. (`cut.js` with `"sound":"camera"` does all of this.)
- Music: `timeline.place {"item","track":"A2","time":0,"duration": min(media, film)}` then `clip.remix` to fit, fade
  out 2 s. Ducking: `essentialSound.setType {"clips","type":"music"|"dialogue"}`, then
  `essentialSound.generateDucking {"clips":[music]}`.
- Loudness is set at export (`loudnessLufs`).

### Export, jobs, playback
- `file.exportMedia {"path","format":"h264","quality":85,"loudnessLufs":-14}` → `{job}` (background job; add
  `"wait":true` only headless). The export **snapshots the project when it starts**: switching sequences or editing
  afterwards is safe. `"sequence": id` exports a specific sequence.
- `jobs.list` → `[{id,label,finished,progress,status}]`; `jobs.cancel {"job": id}` (key is `job`, not `id`).
  `node tools\fc.js --wait` blocks until no job runs.
- After export, verify: `filmcraft-cli probe <file>` → duration, 1920×1080, fps, `AAC 2ch`.
- Smooth playback: `sequence.renderInToOut {}` (a job; green render bar). Lower preview cost:
  `fc.js --ui ui.set '{"program":{"res":"Quarter"}}'`. `ui.inspect` → `playback.dropped/shown` shows if playback keeps up.
- Fit the timeline to the window: `fc.js --ui ui.set '{"timeline":{"fit":true}}'`.

## Gotchas learned the hard way
1. Placing beyond the media end silently makes a clip longer than the source — clamp.
2. Never slow audio: place picture with `audio:false`, add real-time sound separately.
3. Speed must give whole source frames: at 50 % use an even number of timeline frames (cut.js handles it).
4. 59.94 → 29.97 at 50 % is the only clean slow motion for 60p DJI footage on a 29.97 timeline; on 23.976 use 40 %.
5. `effects.setParam` on `look` needs an integer.
6. An export or render job and live playback compete for CPU — tell the user playback may stutter meanwhile.
7. Long `ui.inspect` output is large; extract the fields you need.
9. Commands act on the **active sequence**. If the user clicks another sequence tab during a live build, creations
   land in the wrong sequence and edits fail with "no such track item". `cut.js` re-selects its sequence before every
   creating command and retries once; hand-written scripts must do the same (`sequence.open {"item"}`), and after any
   such warning, inspect every sequence for strays (`edit.clear {"clips":[…]}` removes one).
8. Editing while the user is watching: move the playhead to where you work, pause ~100 ms between placements, and fit the
   timeline at the end so they can follow.
