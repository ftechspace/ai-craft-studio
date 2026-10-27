---
name: moment-editing
description: Edit by moments, not by durations. The method every editor in this studio uses to turn footage into a story — analyse every clip into a moment map (word-timed transcript, sound events, shot cuts, motion, quality), watch the moments, log what each one means, build the story from moments, cut each shot from where its moment begins to where it resolves, then check the cut and read it like a viewer. Use for any edit of real footage (films, vlogs, BTS, family, events, recaps, shorts) and whenever a cut feels chopped, random, or "cut to a length".
---

# Moment editing

**The rule: the footage decides the length.** A shot lasts exactly as long as the moment in it — 1.5 s for a glance,
40 s for a conversation, the whole 3-minute clip if all of it is good. There is **no target shot length, no target
section length and no "one minute per clip"**. Shot-length statistics are something you *report* after cutting,
never something you aim for. A film's length is the sum of the moments that earn their place (and if the creator says
"don't shorten", that is every important and nice moment).

A **moment** is one complete unit of meaning: an action from its start to its resolution (she climbs the rock and
stands up laughing), an utterance or exchange from its first word to its last plus the reaction (the joke, the
laugh), a reveal (the view opening up), a reaction (his face when he sees it), a breath (a still, beautiful hold that
lets a scene land). Moments are what you select, order and protect. Cuts happen *between* moments, or inside one
only at a natural beat (a pause, a look, an action finishing).

## 1. Analyse every clip (the editor's eyes and ears)
```
tools/footage/.venv/Scripts/python.exe tools/footage/analyze.py <footage folder or clips> --out projects/<p>/edit/analysis
tools/footage/.venv/Scripts/python.exe tools/footage/analyze.py dense <clip> <from_s> <to_s> 0.25 --out projects/<p>/edit/analysis
```
Per clip you get `<stem>.md` (read it), `<stem>.analysis.json` and contact sheets (one frame per second, labelled with
source time): a **word-timed transcript** (Whisper on the GPU — machine-made, confirm lines by ear before quoting
them in captions), **sound** (noise floor, silences, bursts = laughs/shouts/claps, clipping), **shot cuts** inside the
clip, **motion and camera movement**, **quality flags** (blurry, dark, black, blown, shaky), and **candidate moments**
split at real boundaries with **word-safe in/out points**. Analysing a day of footage takes minutes; do it for every
clip, always.

## 2. Watch and log the moments → `edit/moments.md`
The analyser finds *where*; you decide *what* and *how much it matters*. For every clip: look at **every** contact
sheet (all of them — not a sample), read the transcript, then open `dense` sheets (0.25 s) around anything that
might matter. Log each real moment:

| id | clip | in–out (s) | what happens (concrete: who does what, what is said, the reaction) | value | story role | notes |
|---|---|---|---|---|---|---|

- **in–out = the moment's natural boundaries**: start just before the action/line begins (a breath before the first
  word, the hand starting to move), end after it resolves (the laugh finishes, the walk arrives, the reaction lands).
  Use the analyser's word-safe points and dense sheets to place them; never inside a word or a gesture.
- **value** ★–★★★ for emotion, story, personality, beauty, humour — not for length.
- **story role**: setup · character · turn · reveal · payoff · joke · breath · transition · establishing.
- Mark **duplicates** (the same thing filmed twice) and keep the stronger; mark **unusable** (black, lens cap,
  pocket, unreadable blur) — and list both, so nothing is silently lost.
- Long takes: decide whether the moment is the *whole take* (a conversation that's good all the way through, a
  performance) or several moments inside it (split at the beats, not at a clock).

## 3. Build the story from moments → `edit/story.md`
Use `creative-direction` and `taste-profile`: the truth in one sentence, the spine, plants → payoffs, chapters, the
ending. Then place **moments** (by id) into the chapters. Order by story (chronology unless the story needs
otherwise). Contrast and rhythm come from *which* moments sit next to each other — a still breath after a burst, a
reaction after a reveal — not from trimming everything to the same length. If a chapter feels long, ask whether a
weaker moment should go, never whether all moments should be shortened.

## 4. Cut moment by moment
- Each shot = one moment (or a beat of one), in at its natural start, out at its natural end. Keep conversations
  whole unless a line genuinely repeats; tighten *dead air between* moments, not the moments.
- Joins: J/L-cuts to carry a voice or a laugh across; cut on action; let sound lead into the next place.
- Inside long talk, cover with the clip's own cutaways (what is being described) rather than chopping the speech.
- Speed changes, freezes and effects only on moments that earn them.
- Write `edit/cutlist.json` next to your build plan (format in `tools/footage/checkcut.py`): every shot's clip, in,
  out, position, whether its sound plays, and **why** (the moment it carries).

## 5. Check, then read it like a viewer
```
tools/footage/.venv/Scripts/python.exe tools/footage/checkcut.py projects/<p>/edit/cutlist.json
```
Fix every **error** (words cut in half, black frames). Resolve or justify every **warning** (entering/leaving
mid-utterance, blurred cut points, the same moment used twice, slivers, long dead stretches). Then read
`cutlist.transcript.md` top to bottom as a viewer: does it make sense with eyes closed? Is anything cut off,
repeated, unexplained, or boring? Then a frame strip of the cut (`contact.exe program`) for the picture. Only then the
`creative-critic`.

## Never
- Cut to a target length (per shot, per clip, per section, per film) — lengths come from moments.
- Pick "the first N seconds" of a clip, or sample clips evenly.
- Cut mid-word, mid-sentence, mid-gesture, or before a reaction lands.
- Drop a ★★+ moment for pace without telling the creator.
- Trust the transcript blindly for captions; confirm by ear.
