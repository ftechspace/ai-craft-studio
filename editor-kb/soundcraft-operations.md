# Driving SoundCraft — operations manual

SoundCraft 0.4.0 (Pro Tools-class DAW, pure Rust). Everything here was run on this machine (Windows 11, release
build) unless marked **UNVERIFIED** (read from source/docs, not exercised). Paths are relative to
`C:\CodeHouse\AIFilmEditor\`. Use forward slashes in every JSON path (`C:/CodeHouse/...`).
**Re-verified 2026-10-27 against SoundCraft 0.13.1** (482 commands; headless CLI only, no app): every command id and
param in this manual still exists; the session skeleton, preset workaround, hit on a downbeat (onset 2.40 s), noise
riser with automation, maximizer, `file.bounce_mix`, `file.bounce_stems`, reverse + fade, `--keep-going` all re-run
and behave as written. Changes are marked *(0.13.1)*. Control-channel/`ui.*` methods were not re-run.

## Binaries and setup

| What | Path / command |
|---|---|
| Desktop app | `apps/soundcraft/target/release/soundcraft.exe [--demo] [--control <port>] [--no-audio] [session.scraft \| audio files…]` |
| Headless CLI | `apps/soundcraft/target/release/soundcraft-cli.exe` (`--help`) |
| Launch app with control port | `node tools/craft.js soundcraft --start [session.scraft]` (port **9873**) |
| Command to the app | `node tools/craft.js soundcraft <command id> '<json>'` · raw methods: `--ui <method> '<json>'` |
| Level meter for WAVs | `node tools/wavlevels.js` (see Verifying) — installed and verified 2026-10-27 |
| Rebuild | `sh tools/build-apps.sh soundcraft` (log `output/build-logs/soundcraft.log`) |

`soundcraft-cli` subcommands:
```
info FILE                         audio file probe (rate, channels, frames, seconds) or .scraft text summary
convert IN OUT [--bit-depth 16|24|32f] [--rate HZ] [--normalize] [--dither | --no-dither]   (0.13.1: dithers only when resolution drops)
run [--in S.scraft | --demo] [--cmd ID[=JSON]]… [--bounce OUT] [--start T --end T] [--save S.scraft] [--inspect]
script FILE [--in S | --demo] [--save S] [--bounce OUT] [--start T --end T] [--keep-going]   one `ID JSON` per line, # comments
commands [FILTER]                 list ids (id, label, menu)
describe ID                       one command's params doc
app [--port P] METHOD [JSON]      call a running app (default port 7979 — always pass --port 9873)
mcp [--connect PORT] [--demo]     MCP server on stdio (headless, or bridged to the app)
plugins                           built-in plugin ids
```
`run`/`script` execute in order and stop at the first error (exit 1, message on stderr `file:line: id: error`);
then `--bounce` (with `--start/--end` in seconds or time strings), then `--save`, then `--inspect`. Each command's
result JSON is printed as `id: {…}`. A bounce ≈ 3 s for a 60 s, 9-track song.

## Which mode

| Mode | Use it for | How |
|---|---|---|
| **Headless script** (default for deliverables) | building score/SFX sessions reproducibly, bouncing, experiments | a generator (`audio/<name>.build.js`) writes `<name>.sc.txt`; `soundcraft-cli script <name>.sc.txt --save … --bounce … --start 0 --end 60` |
| **Live app** | showing the user the session, screenshots, review, small tweaks they watch | `node tools/craft.js soundcraft --start "<abs path>.scraft"` then craft.js commands |
| **MCP headless** | interactive exploration where you need results (ids) back | `.mcp.json` entry `soundcraft` (below) |
| **MCP bridge** | same tools against the running app + screenshot/click/key | `.mcp.json` entry `soundcraft-app` (below) |

Script mode can't read earlier results, but ids are predictable (see Ids). Prefer it: the generator is the score's
source, so "make it slower" = change one number and rebuild as v2.

## Control channel (verified)

TCP `127.0.0.1:<port>`, newline-delimited JSON, no auth/token, one request per line:
`{"id":1,"method":"engine.execute","params":{"command":"track.new","params":{…}}}` →
`{"id":1,"ok":true,"result":{…}}` or `{"id":1,"ok":false,"error":"<string>"}`. Exactly what `tools/craft.js`
sends. Start flag: `--control <port>` (space-separated; `0` = free port printed as `SOUNDCRAFT_CONTROL_PORT=…`).

| Method | Params | Notes |
|---|---|---|
| `engine.execute` | `{command, params}` | every command; never opens a dialog |
| `engine.commands` | `{filter?}` | ids + params docs + enabled |
| `session.inspect` | `{detail?: "summary"\|"full"}` | the document (full = insert params too) |
| `ui.inspect` | `{}` | window, panels, audio device, `edit_layout` (track row rects for clicks) |
| `ui.set` | e.g. `{"window":"Mix"}` / `{"window":"Edit"}` | verified |
| `ui.screenshot` | `{path}` | PNG of the window (1600×1000 here); verified |
| `ui.menu.invoke` | `{path}` | may open a dialog — avoid |
| `ui.click/drag/move/key/text` | see `apps/soundcraft/docs/control-protocol.md` | UNVERIFIED here |
| `app.quit` | `{}` | **quits immediately, even with unsaved changes — save first** (verified) |

craft.js treats `session.*`/`ui.*`/`app.*` as engine commands unless you use `--ui`: `session.inspect` and
`session.open` also exist as engine commands, so both work; `ui.*` and `app.quit` need `--ui`.

## MCP

```jsonc
// .mcp.json: "soundcraft" (headless) is registered as of 2026-10-27; "soundcraft-app" is not.
// (0.13.1) mcp also takes --automation-read-root DIR / --automation-write-root DIR to confine file access.
"soundcraft":     {"command": "C:/CodeHouse/AIFilmEditor/apps/soundcraft/target/release/soundcraft-cli.exe", "args": ["mcp"]},
"soundcraft-app": {"command": "C:/CodeHouse/AIFilmEditor/apps/soundcraft/target/release/soundcraft-cli.exe", "args": ["mcp", "--connect", "9873"]}
```
Tools (verified via stdio): `list_commands {filter}`, `execute {command, params}`, `batch {calls:[{command,params}],
keep_going}`, `inspect_session {detail}`, `new_session {name, sample_rate, template: blank|demo}`, `open_session
{path}`, `save_session {path}`, `import_audio {path, track, at}`, `bounce_mix {path, format, bit_depth, start, end,
normalize}`, `parity`; bridge only: `screenshot {path}`, `ui_inspect`, `ui_set {state}`, `menu_invoke`, `click`,
`drag`, `key`. Resources `soundcraft://session`, `soundcraft://commands`. `--connect` takes a port or `host:port`
(FilmCraft's flag is `--bridge`; SoundCraft's is `--connect`).

## Time, ids, units

- **48 kHz sessions.** At 100 BPM: beat = 0.6 s = 28 800 samples, bar (4/4) = 2.4 s = 115 200 samples,
  60.0 s = 2 880 000 samples. MIDI: **960 ticks per quarter** (bar = 3840).
- Positions: integer samples, `{"seconds": 4.8}`, `"bars_beats:3|1|000"` (bar 3 = 4.8 s at 100 BPM — verified),
  `"min_secs:0:12.500"`, `"timecode:…"`, `"samples:48000"`. Bars are 1-based.
- **Lengths are measured like positions from zero**: `"length":"bars_beats:3|1|000"` = 2 bars, not 3. Use
  `{"seconds": x}` or samples for lengths.
- `session.format_time {"at": 1382400, "format": "bars_beats"}` → `"13| 1| 000"` (check your maths).
- **Ids: one counter for everything** (tracks, clips, busses, markers…), starting at 1 in a new session, +1 per
  object created, in order. Example verified: track 1, its MIDI clip 2, bus 3, aux 4, audio track 5, master 6,
  marker 7. `file.import_audio` makes a source, a track and a clip: source n, track n+1, clip n+2 (verified 0.13.1:
  `{source:1, track:2, clip:3}` in a new session) — read the printed result. Tracks can always be named; clips need ids (`midi.note_add {"clip": 2}` — a string `"2"` is rejected).
- Master fader tracks ignore `name` and are called `Master 1` — address them by id.

## Command reference (sound-designer subset; `soundcraft-cli describe ID` for any other of the 482)

**Session/files**
- `session.new {name?, sample_rate?: 48000, bit_depth?: 24}` · `session.open {path}` → `{missing: […]}` ·
  `session.save {path?}` · `session.save_as {path}` · `setup.session {frame_rate?, bit_depth?, timecode_start?}`
- Saving writes `X.scraft` (JSON) + `Audio Files/` next to it. **The folder must exist** (else os error 3).
- `file.import_audio {path | paths, track?, at?, new_tracks?: true}` (WAV/AIFF/FLAC/MP3/OGG/AAC/ALAC/CAF, MP4/MOV
  audio) → `{imported:[{track, clip, source, frames}]}` — new track named after the file.
- `file.import_midi {path, at?, tempo_map?: true}` → one instrument track per SMF track; all-channel-10 tracks get
  `drum_synth`, others `subtractive_synth` (an exported drum track came back as synth — fix with `mix.instrument`).
  The clip ends at the last note, not the bar.
- `file.export_midi {path, tracks?}` (verified) · `file.export_session_text` · `file.get_info`
- `file.bounce_mix {path, format?: wav|aiff|flac, bit_depth?: 16|24|32f, start?, end?, source?: main|bus, normalize?,
  dither?: true}` → `{seconds, peak_db, true_peak_db, lufs}` (integrated). Default range = 0 → end of the last clip:
  **reverb/decay tails after the last clip are cut — always pass `start` AND `end`** (an `end` without `start`
  is ignored and you get the default range — verified; same for the CLI's `--start/--end`). `normalize` = −0.1 dBFS peak (never for
  deliverables).
- `file.bounce_stems {dir, format?, bit_depth?, start?, end?}` → one `<session> - <track>.wav` per **audio, instrument
  and MIDI track** (each soloed, so its sends/aux returns are included). Aux-only tracks (e.g. a generator on an aux)
  get no stem — put generated SFX on audio tracks.

**Tracks** — `track.new {count?, format?: mono|stereo, kind?: audio|aux|master|midi|instrument|vca|folder, name?,
instrument?: plugin id}` → `{tracks:[ids]}` · `track.rename {track, name}` · `track.delete {tracks}` ·
`track.duplicate {tracks, …}` · `track.input {tracks, input: bus name}` · `track.output {tracks, output: main|bus}` ·
`track.color {tracks, color:[r,g,b]}` · `track.view {tracks, view: "volume"|"plugin:a:level"|…}` (shows a lane in
the app) · `track.save_preset {path, track}` · `track.load_preset {path, tracks}` · `track.inspect {track}` ·
`mix.instrument {track, plugin}` (resets the instrument to defaults).

**MIDI** — `midi.new_clip {track, start?, end? | length?}` → `{clip, start, end}` ·
`midi.note_add {clip, pitch, start_ticks, length_ticks?: 480, velocity?: 100, channel?: 0}` — **`start_ticks` is
relative to the clip start** (verified) · `midi.notes {clip}` · `midi.note_edit {clip, index, …}` ·
`midi.note_delete {clip, indices}` · `midi.notes_move {clip, indices, ticks?, semitones?}` ·
`event.transpose {semitones, clips?}` · `event.quantize {grid?: "1/16", strength?, swing?, clips?}` ·
`event.change_velocity` · `event.midi_note {clip, pitch, start_ticks, length_ticks, velocity}`.

**Tempo/markers** — `event.tempo {bpm, at?}` · `event.meter {numerator, denominator, at?}` ·
`event.tempo_linear {start, end, end_bpm, …}` (UNVERIFIED) · `event.add_key_change {key: "D major", at?}` ·
`markers.add {name, at}` (or `start`/`end` for a range) · `markers.edit {number|id, …}` · `markers.delete`.

**Clips/editing** — `clip.gain {clips, db | delta_db}` · `clip.rename {clip, name}` · `clip.loop {clips, count}` ·
`edit.fades_create {tracks, start, end, shape?: linear|equal power|s-curve|exponential|logarithmic}` — the range
over a clip's head makes a fade-in of that length (verified: 0.6 s), over its tail a fade-out ·
`edit.select {tracks, start, end, clips}` · `edit.separate {tracks, at}` · `edit.duplicate` / `edit.repeat {count}` ·
`edit.move_clips {clips, by | to, track?}` · `edit.clear` · `edit.consolidate` · `clip.place_source {source, track,
at}` · `audiosuite.process {process: <plugin id>|normalize|reverse|invert|gain|time_stretch|pitch_shift|varispeed|
signal_generator, params?, clips}` (reverse verified; rendered into a new source, saved to `Audio Files/`).

**Mixer** — `mix.volume {tracks, db}` · `mix.pan {tracks, pan: -1..1}` · `mix.mute` · `mix.solo {tracks, value,
exclusive?}` · `mix.new_bus {name}` · `mix.send {track, slot?, bus, level_db?, pre_fader?}` ·
`mix.send_level {track, slot, db?}` · `mix.insert {track, slot: 0..9|a..j, plugin, params?}` ·
`mix.insert_param {track, slot, param, value}` · `mix.insert_params {track, slot, params}` · `mix.insert_bypass` ·
`mix.insert_remove`. **Insert slots only** — `slot:"instrument"` is rejected by `mix.insert_param(s)`.

**Automation** — `automation.set_point {track, param, at, value}` · `automation.write_range {track, param, start,
end, value}` · `automation.clear {track, param?}`. Params: `volume` (dB), `pan`, `mute` (0/1), `send_a_level`…,
`plugin:<slot letter>:<param id>` (e.g. `plugin:a:level`, `plugin:b:lpf_freq` — verified). Breakpoints ramp
linearly; `mute` steps. **A lane with one point holds that value for the whole session** (a single `mute 1` point
silenced the track from 0 s): always give a lane a start point.

**Inspection** — `session.inspect {detail?}` (tracks, clips with `start_time`/`length`/`fade_in`/`gain_db`/`notes`,
inserts, sends, automation lanes with point counts, busses, markers, tempo, `sources[].loaded`, undo label) ·
`track.inspect {track}` · `clip.inspect {clip}` · `midi.notes {clip}` · `engine.plugins` (every param id, range,
default) · `session.audio_health` · `engine.history` · `transport.status`.

**Transport (app)** — `transport.play {from?}`, `transport.stop`, `transport.locate {at}` (plays on this PC's default
device; you can't hear it).

## Built-in instruments and plugins (all original DSP, no samples)

`subtractive_synth` (16 voices, 2 PolyBLEP oscs, resonant LP filter + env, amp ADSR, glide):
`osc1_wave`/`osc2_wave` 0 Saw · 1 Square · 2 Sine · 3 Triangle; `osc2_semitones` ±24, `osc2_detune` ±100 c (7),
`osc_mix` %, `cutoff` 20–20k Hz (2000), `resonance` %, `filter_env_amount` ±100, `amp_attack/decay/release` ms,
`amp_sustain` %, `filter_attack/decay/sustain/release`, `glide` ms, `velocity` % (sensitivity), `level` dB (−6).

`drum_synth` (GM-style map): 35/36 kick · 37/39 clap · 38/40 snare · 42/44 closed hat · 46 open hat ·
41/43 floor tom · 45 low tom · 47/48 mid tom · 50 high tom · 49/57 crash · 51/59 ride. Params `level`,
`kick_tune` ±12 st, `kick_decay` 50–2000 ms (450), `snare_tune`, `snare_snappy`, `snare_decay`, `hat_decay`,
`open_hat_decay`, `tom_tune`, `tom_decay`, `cymbal_decay` 200–6000 ms. Kick at vel 127 ≈ −7.6 dBFS peak alone.

Effects: `eq_7band` (hpf_on/hpf_freq, low_shelf_*, low_mid_*, mid_*, high_mid_*, high_shelf_*, lpf_on/lpf_freq,
gains ±24 dB), `eq_1band`, `compressor` (threshold, ratio, attack, release, knee, makeup, limiter, lookahead, mix),
`expander_gate`, `de_esser`, `maximizer` (threshold, ceiling, release), `channel_strip`, `room_reverb` /
`plate_reverb` (mix %, pre_delay, decay s, size, damping, diffusion, width, low_cut), `mod_delay` (time ms,
feedback, mix, mod_rate, mod_depth, lpf), `chorus`, `flanger`, `phaser`, `saturator`, `lofi`, `pitch_shifter`,
`time_shift`, `gain`, `trim`, `signal_generator` (waveform 0 Sine · 1 Square · 2 Saw · 3 Triangle · 4 White ·
5 Pink noise; `freq`, `level` dB — replaces the track's input, works on audio and aux tracks with no clips),
`dither`. CLAP/VST3 hosting exists (`engine.clap_plugins`, `engine.vst3_plugins`) — none installed here.
Full param list: `soundcraft-cli run --cmd engine.plugins`.

### Setting instrument parameters
*(0.13.1, verified — simplest)* Set them directly in the script:
`mix.instrument {"track":"Bass","plugin":"subtractive_synth","params":{"osc1_wave":2,"cutoff":400,"level":-8}}` (resets
the instrument, then applies `params`; values clamped into range, unknown ids are errors) and
`mix.instrument_param {"track":"Bass","param":"amp_release","value":800}` for one param. Both persist in the `.scraft`.
The track-preset route below still works and is the way to reuse a sound across sessions (verified again 0.13.1):
1. `track.save_preset {"track":"Keys","path":".../keys.json"}` once (any instrument track).
2. Edit the JSON: `instrument.params = {"osc1_wave":3,"osc2_wave":2,"cutoff":1800,"amp_attack":5,"amp_decay":900,
   "amp_sustain":20,"amp_release":600,"level":-6}` (unset params keep defaults). Keep `format:
   "soundcraft-track-preset"` and `mixer`.
3. `track.load_preset {"tracks":["Keys"],"path":".../keys.json"}` — applies instrument **and** mixer (inserts,
   sends, volume) from the file, so load it *before* adding inserts/sends, or put them in the preset.
Verified: the params persist in the saved `.scraft`. Keep presets in `audio/presets/`.

## Verified recipes

**Session skeleton (script lines)**
```
session.new {"name":"score"}
event.tempo {"bpm":100}
markers.add {"name":"HIT","at":{"seconds":4.8}}
mix.new_bus {"name":"Verb"}
track.new {"kind":"aux","name":"Verb Return"}
track.input {"tracks":["Verb Return"],"input":"Verb"}
mix.insert {"track":"Verb Return","slot":0,"plugin":"plate_reverb","params":{"mix":100,"decay":2.2}}
track.new {"kind":"instrument","name":"Keys","instrument":"subtractive_synth"}
track.load_preset {"tracks":["Keys"],"path":"C:/…/audio/presets/keys-soft.json"}
midi.new_clip {"track":"Keys","start":{"seconds":4.8},"length":{"seconds":7.2}}
midi.note_add {"clip":<id>,"pitch":60,"start_ticks":0,"length_ticks":1800,"velocity":90}
mix.send {"track":"Keys","slot":0,"bus":"Verb","level_db":-12}
track.new {"kind":"master","name":"Master"}           # becomes "Master 1": use its id
mix.insert {"track":<master id>,"slot":0,"plugin":"maximizer","params":{"threshold":-6,"ceiling":-2.5}}
```
Run: `soundcraft-cli script score.sc.txt --save C:/…/audio/score/score.scraft --bounce C:/…/audio/score.wav --start 0 --end 60`
(create `audio/score/` first). Bounce = WAV 48 kHz 24-bit stereo with dither by default (verified with `info`).

**Peaks ≤ −1 dBTP** — the maximizer's `ceiling` is a sample-peak ceiling; true peak lands higher (ceiling −1.5 →
true peak −0.95 dB, and −0.26 dB when driven 10 dB; ceiling −2.5 → −1.98 dB). Use ceiling −2.5 and read
`true_peak_db` from every bounce; lower it if > −1.0.

**Hit on a downbeat** — drum_synth track, clip at the hit, notes 36 (kick, vel 127) + 49 (crash) at tick 0; layer a
low synth note and a reverb send. Verified: onset measured at exactly 2.400 s for a hit placed at 2.4 s.

**Noise riser** (verified) — audio track `Riser` with `signal_generator {waveform:4, level:-60}` in slot a,
`eq_7band {hpf_on:1, hpf_freq:200, lpf_on:1, lpf_freq:1000}` in slot b; automation `plugin:a:level` −60 → −14 dB and
`plugin:b:lpf_freq` 1000 → 14000 Hz across the riser; `mute` automation 1 before / 0 during / 1 after (with a
point at 0). Measured: smooth 6–7 dB per 0.3 s climb, cut to silence at the end point.
Pitfall: the generator plays from its default level for ~60 ms at the start of every render (a −18 dBFS blip at
0.00 s) — keep generator tracks muted by automation outside their span, and don't start them at 0.

**Reverse swell / whoosh** — import or bounce a hit/noise burst, `audiosuite.process {"process":"reverse","clips":[id]}`
(verified), fade-in with `edit.fades_create`, align the end to the cut.

**Separate SFX files** (`hit.wav`, `riser.wav`, `whoosh.wav`): build each in its own small session (or bounce the
whole score with only that track soloed: `mix.solo {"tracks":["Riser"],"value":true,"exclusive":true}`) with a
`start`/`end` that includes the full tail (soloing with `exclusive:true` then bouncing verified 0.13.1; stems are verified).

**Re-open in the app for the user**: `node tools/craft.js soundcraft --start "C:/…/audio/score/score.scraft"`
(or `session.open {path}` if it's running; ask first if they have unsaved work), `ui.screenshot` to see it.

## Verifying (you can't hear — measure)

1. **Structure:** `session.inspect` — every track, clip start/length, note counts, inserts, sends, automation lanes,
   markers, tempo. `midi.notes {clip}` for the actual notes.
2. **Loudness:** the bounce result: `peak_db`, `true_peak_db`, integrated `lufs`. Targets in the agent file.
3. **Timing and shape:** `node tools/wavlevels.js file.wav` (summary), `… file.wav 0.6` (peak/RMS per beat at 100 BPM —
   a text waveform), `… file.wav 0.05 4.6 5.0` (zoom on a hit), `… file.wav onsets [dB]` (onset times; sustained
   chords under a pad won't register — use windows). Expect onsets within ±10 ms of the planned time.
4. **Format:** `soundcraft-cli info file.wav` → rate, channels, `sample_format: Int24`, seconds.
5. **Picture:** in the app, `ui.screenshot` (Edit window shows clips, lanes chosen with `track.view`; `ui.set
   {"window":"Mix"}` for the mixer).

## Pitfalls (all hit during testing)
- **`file.bounce_stems` reads bare numbers in `start`/`end` as samples** (you get 1 ms files): pass `{"seconds": …}`.
- **The maximizer threshold also acts as input (makeup) gain**: lowering it raises level going in.
- `--save` into a folder that doesn't exist fails (`…scraft.tmp: The system cannot find the path specified`).
- Bounce without `start`+`end` stops at the last clip end — tails cut; `end` alone is ignored.
- Maximizer ceiling ≠ true peak (see above).
- `"length":"bars_beats:…"` is a position-from-zero, not a bar count.
- `midi.note_add {"clip":"2"}` fails — ids are numbers. Note times are clip-relative ticks.
- `mix.insert_params {"slot":"instrument"}` fails — use `mix.instrument {params}` / `mix.instrument_param` (or a preset).
- A single automation point applies to the whole lane.
- `app.quit` doesn't ask to save.
- `track.new {"kind":"master","name":"Master"}` → "Master 1".
- `file.import_midi` may assign `subtractive_synth` to drums; re-set with `mix.instrument` (then re-apply params).
- Signal generator start blip (above).
- `view.zoom_fit` didn't fit a 4.8 s session in the app (showed ~25 s) — cosmetic.
- `soundcraft-cli app` defaults to port 7979; craft.js uses 9873.
- Test runs that shouldn't touch the user's prefs/log: set `SOUNDCRAFT_NO_PREFS=1` (UNVERIFIED effect).
