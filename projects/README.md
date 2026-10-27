# Projects

One folder per project. Every Craft app reads from and writes into the same project folder, so the output of one
app is the input of the next. Source footage and photos are never copied or changed; the brief points at them.

```
projects/<project-name>/
  brief.md         what we're making: purpose, audience, length, platforms, mood, sources, palette, deadlines
  storyboard.md    the plan: panels/shots, timing, and which app makes which piece
  handoff.md       log: every agent appends what it delivered (file, size, format, notes) and what it needs next
  stills/          LightCraft  - culled, developed photos (JPEG/TIFF)           + lightcraft library/catalog
  art/             PhotoCraft  - composites, retouches, thumbnails (PSD + PNG)
  graphics/        VectorCraft - logo, title lockups, icons, lower-third shapes (.vectorcraft + SVG + PNG)
  motion/          EffectCraft - animated intros, titles, end cards (project + MP4/MOV)
  audio/           SoundCraft  - score, sound design, mix stems (session + WAV 48 kHz 24-bit)
  ui/              FigCraft    - UI screens, prototypes, social/thumbnail templates (.figcraft + PNG/PDF)
  print/           DesignCraft - posters, one-sheets, storyboard pages (document + PDF + PNG)
  edit/            FilmCraft   - the edit (.fcproj) and its cut plans
  exports/         finished deliverables, only after the user approves them
```

## Starting a new project
Tell Claude: *"New project `<name>`: footage is in E:\…, I want a 1-minute promo for Instagram, warm and playful."*
The **producer** agent creates the folder, writes `brief.md` and `storyboard.md`, and shows you the storyboard
before anything is built. After you approve it, it hands each piece to the right specialist agent.

## Working on an existing project
Name it: *"In `three-looks`, make the music slower"* or *"three-looks: new thumbnail, darker"*. The agents read
`brief.md`, `storyboard.md` and `handoff.md` first, so they pick up where the last session stopped. New versions go
next to the old ones (`logo-v2.svg`, sequence "… v2"); nothing is overwritten.

## The agents
| Agent | App | Makes |
|---|---|---|
| producer | all | brief, storyboard, schedules the others, checks the pieces fit together |
| film-editor | FilmCraft | the edit: cut, grade, sound, titles, export (story, mood, cinematic pieces) |
| content-editor | FilmCraft | YouTube long-form, vlogs (skill: `vlog-editing`), Shorts, TikTok, Reels; cutting long videos into clips (skill: `youtube-editing`) |
| creative-critic | all | reviews every piece for idea, emotion and fit with the user's taste |
| photo-grader | LightCraft | culls and develops photos, consistent looks |
| photo-artist | PhotoCraft | retouching, composites, thumbnails, covers |
| graphic-designer | VectorCraft | logos, wordmarks, title lockups, icons |
| motion-designer | EffectCraft | animated intros, logo reveals, motion titles, end cards |
| sound-designer | SoundCraft | music beds, sound design, mixes |
| layout-designer | DesignCraft | posters, one-sheets, printed storyboards, press kits |
| ui-designer | FigCraft | thumbnail/social templates, carousels, channel art, app screens and clickable prototypes |

Ops manuals (commands, CLI, pitfalls) live in `editor-kb/<app>-operations.md`.
Launch any app with its control channel: `node tools/craft.js <app> --start` (ports: `node tools/craft.js ports`).
Rebuild after `git pull`: `sh tools/build-apps.sh [app …]`.
