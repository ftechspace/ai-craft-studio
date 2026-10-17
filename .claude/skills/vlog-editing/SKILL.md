---
name: vlog-editing
description: Edit vlog footage (day-in-the-life, travel, family, trips, slow living, couple/BTS) into a story-driven YouTube vlog in the user's house style, building on youtube-editing. Use whenever the footage is a vlog — a person or family filming their own day — to find the story spine, write story.md, keep every important and nice scene, and protect the creator's personality and honest moments.
---

# Vlog editing

Builds on `youtube-editing` (workflow, platform specs) but a vlog is **not** a retention-optimised talking head. This
user's references (26 analysed vlogs — Georgene Loh, Mei Time, MAZELEE, Riri Travels, Komorebi Tales, couple-shoot
BTS…; see the `taste-profile` skill and `references/analysis-*.md`) keep viewers through **story, intimacy, sound and
light**, not punch-ins and whooshes. Where `youtube-editing/retention.md` disagrees with this file, this file and the
taste profile win for vlogs.

Companion skill: `vlog-techniques` — the vlog editor's toolbox (A-roll jump cuts and punch-ins, B-roll progressions,
transitions between places and times, time compression, sound design, text, look, and the emotional pacing map).
Use it while building steps 4–8; the taste profile decides how much of each tool (this user is calm: fewer
effects; per project, "no names" overrides its name cards; montages that skip routine are fine as long as no
important or nice scene is dropped).

## Overrides to the retention rules (for vlogs)
| youtube-editing says | for vlogs do this instead |
|---|---|
| visual change every 3–6 s | median shot ≈ 4–6 s, but hold real moments 15 s – 3 min; rituals in a few held angles |
| cut the middle hard | **don't shorten** — keep every important and nice scene; cut only unusable or repetitive takes, and list what you cut |
| no slow fade-ins; movement in frame 1 | either a short promise montage (≤ 25–30 s) or one held atmospheric frame with a quiet line — both fine |
| pattern interrupts every 30–90 s (SFX, memes, callouts) | chapter changes, a new place, light changing, a silence, music switching on/off, a caption line |
| SFX on graphics and transitions | none as decoration; real sounds from the footage carry transitions |
| remove every pause / "hey guys" | keep the creator's natural greetings, pauses and laughter when they carry personality |
| CTA + end screen | a quiet thank-you over a small final moment; end screen only if the user asks |

## Workflow

### 1. Inventory the day
For every file (video and photos; skip `._*` macOS files): time from the file name, length, fps, audio, who is in it,
where, what happens, talk vs ambient. Contact sheets for every clip (`contact.exe`), dense `range` sheets around
anything promising, a rough transcript (Whisper) — mark every quoted line "check by ear". Note the **light across the
day** and any **real event sounds** (a door, a strobe, a needle, rain). Write it to
`projects/<project>/edit/footage-log.md`.

### 2. Find the story → `story.md`
Before any cut, write `projects/<project>/edit/story.md`:
- **The truth in one sentence** — what the day was really about for this person (look for their own words: "I need to
  refresh myself", "we're not ready for this").
- **The spine** — pick one from the taste profile (clock/light, condition arc, roll call + one chapter per person,
  countdown + "coming up", place chapters entered the same way, material spine, then-and-now, pose loop) and say why it
  fits *this* footage. Name 2 you rejected.
- **Plants → payoffs** — things said or seen early that return changed later (a line, a number, a mirror shot, a sign).
- **Chapters** — one per place/person/ritual, each with a mini-goal and its best moment; how each is entered.
- **Energy map** — the wave across the chapters (`vlog-techniques`: hook → setup → rising → a calm breath → peak/turn →
  calm resolution → short outro); never two high-energy chapters in a row without a breath.
- **The ending** — a small, real moment that rhymes with the opening (the youngest, the empty lit room, eyes closing in
  the taxi). No recap, no outro speech.
- **Personality & honesty** — the moments that show who the creator is (jokes, teasing, fear, tiredness, tenderness).
  These are protected: never cut them for pace.

Show `story.md` (and the chapter table) to the user before building when they're present.

### 3. Selects — generous
Rate every moment ★–★★★ in `edit/selects.md`. Keep ★★ and up, and ★ moments that carry talk, laughter, light or a
transition. List what you leave out and why (unusable, repeated take), so the user can ask for it back.

### 4. Build talk and natural sound first
Lay the scenes with their own sound: conversations whole (cut on the breath, never mid-word — check word timings and
levels), J/L-cuts to carry a voice into the next place. Does the day make sense with only the natural sound? Then add
picture coverage (hands, details, wides) — prefer the footage's own inserts to effects.

### 5. Sound plan (with `sound-designer`)
Natural sound first in every chapter. Music is **earned** (switched on by an on-screen action or once settled) and
**removed** (nightfall, arrival, tears, a confession). Silence or near-silence at chapter breaks and before reveals.
Music ≈ 12–16 dB under speech. If there's no licensed music, cues may be built from the footage's own sounds.

### 6. Text = the creator's voice
First-person captions, small serif/humanist, no box, sentence case; humble and a little funny; a few playful labels
only if they're jokes and name tags at once. Place names fading in on arrival. Never captions that describe the
picture. Respect "no names" and privacy requests; never caption a line you haven't confirmed.

### 7. Photos
Use the creator's photos (developed by `photo-grader` to match the footage): a gallery between chapters in near
silence, the photo a moment produced right after the moment, then-and-now dissolves.

### 8. Look
One consistent soft, warm, filmic grade per location (`photo-grader` gives Lumetri values); light is a subject.
Watch the FilmCraft Lumetri bug (keep Shadows at 0) and run **one** preview render at a time.

### 9. Review & package
`creative-critic` review against the taste profile (Fit ≥ 4 to pass). Package: 3 title options (first person, names
the stakes, one concrete hook, CAPS on 1–3 words, optional `*aside*`), chapters from the chapter table (0:00 first),
a description, and a **real-frame thumbnail with no text** (`photo-artist`). Export only after the user approves.

## Checklist
- [ ] `story.md` exists: truth, spine (+2 rejected), plants → payoffs, chapters, ending, protected moments
- [ ] Every important and nice scene is in; what's out is listed with a reason
- [ ] Conversations play whole; no clipped words; captions match what's said
- [ ] Natural sound carries; music switches on/off for a reason; silences at breaks
- [ ] The ending is small and rhymes with the opening
- [ ] Creator's personality and honest moments intact; no generic YouTuber devices
- [ ] Grade consistent; photos match; no Lumetri artefacts
- [ ] Titles, chapters, description, real-frame thumbnail ready; nothing exported without approval
