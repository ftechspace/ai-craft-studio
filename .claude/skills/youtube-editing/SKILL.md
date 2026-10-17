---
name: youtube-editing
description: Edit raw footage into retention-focused content for YouTube long-form, YouTube Shorts, TikTok and Instagram Reels using FilmCraft. Use for any request to cut, recut, tighten or repurpose footage for a social or video platform, or to turn one long video into short clips.
---

# YouTube & Platform Editing

This skill turns footage into videos that people keep watching. It sits on top of
`creative-direction` (taste and style) and uses FilmCraft for every edit. It does not
replace `creative-direction/edit.md`: read that first for the house style, then apply
the platform rules here.

Supporting files in this folder:
- `retention.md` - the editing craft rules (hooks, pacing, pattern interrupts, endings)
- `platforms.md` - specs per platform (aspect ratio, length, loudness, safe zones, captions)

## Before you touch the timeline

1. **Read the brief.** You need: platform(s), target length, audience, the one thing the
   viewer should feel or learn, and the call to action. If any is missing and the user
   is present, ask once. If not, choose sensible defaults and write them at the top of
   the edit plan.
2. **Read the taste.** Load `creative-direction/edit.md` and the `taste-profile` skill so
   the cut matches the user's style, not a generic YouTube style.
3. **Read the platform spec** in `platforms.md` for every target platform.

## Workflow

### 1. Log the footage
For every clip in the project's footage folder, produce a log entry in
`projects/<project>/edit/footage-log.md`:
- file, duration, what happens (one line)
- transcript with timestamps (use FilmCraft's speech-to-text if enabled, otherwise Whisper)
- best moments (timestamp + why), bad takes, dead air, technical problems
  (blur, shake, clipped audio, bad exposure)
- a 1-5 "energy" score

Take screenshots at a few points per clip (`ui.screenshot`) so judgments about picture
come from looking, not guessing.

### 2. Find the story
Before cutting, write `projects/<project>/edit/edit-plan.md`:
- **Hook (first 3-15 s):** the exact moment or line that opens the video, and why it
  makes people stay. See `retention.md`.
- **Promise:** what the viewer gets if they keep watching.
- **Beats:** an ordered list of sections, each with source clip, in/out timecodes,
  purpose, and target duration.
- **Payoff and ending:** where the promise is delivered, and the CTA.
- **Cut-downs:** for multi-platform jobs, which beats become Shorts/Reels/TikToks.

The plan is the contract. If the user is present, show it before building anything
longer than a few minutes of runtime.

### 3. Build the radio edit
Assemble only the dialogue/main audio track first, from the plan:
- Remove dead air, ums, false starts and repeated takes (keep the best take).
- Tighten pauses to breathing length, not silence.
- Check: does it make sense with eyes closed? If not, fix structure before visuals.

### 4. Cover and pace
- Add B-roll, inserts, zooms (scale keyframes on the A-roll), screen recordings and
  graphics to hide jump cuts and keep visual change frequent (`retention.md` has the
  rhythm rules).
- Hand titles, lower thirds and on-screen text to the `graphic-designer` agent.
- Hand music, SFX, ducking and loudness to the `sound-designer` agent.
- Hand the grade to whichever agent owns colour in this setup.

### 5. Captions
- Long-form YouTube: export a caption file (SRT) from the caption track.
- Short-form: burned-in captions, large, high-contrast, inside the safe zone,
  2-5 words per line, synced to the word.

### 6. Review
Send the cut to the `creative-critic` agent with the brief and edit plan. Fix every
"must fix" note before export. Then run the checklist below yourself.

### 7. Export and package
- Export one master per platform using the specs in `platforms.md`.
- Write `projects/<project>/output/<platform>-package.md` with: title options (3),
  description, chapters (long-form, from the beat list, first chapter at 0:00),
  tags/hashtags, and a thumbnail brief for the `graphic-designer`
  (see `creative-direction/thumbnails.md`).

## Working with FilmCraft

- Never guess command names. List them with `filmcraft-cli commands` or the MCP
  server's tool list, and check parameters before calling.
- FilmCraft time is integer ticks: 254,016,000,000 per second. Convert timecodes
  exactly; never round to frames by hand.
- Make each logical step one undoable action where possible, and save the project
  after each workflow stage.
- Look before you judge: screenshot the Program monitor after placing hooks,
  graphics and grades.

## Final checklist

- [ ] The first 3 seconds contain motion, a face, or a strong line - no logo intro, no "hey guys"
- [ ] The promise is stated or implied in the first 15 seconds
- [ ] No shot holds unchanged longer than the platform's pacing limit (`retention.md`)
- [ ] No dead air, no repeated takes, no audio pops at cuts
- [ ] Captions are correct, synced and inside the safe zone
- [ ] Loudness and peak meet the platform target
- [ ] Aspect ratio, resolution and length match `platforms.md`
- [ ] The ending delivers the payoff, and the CTA is short
- [ ] Package file written (titles, description, chapters, thumbnail brief)
