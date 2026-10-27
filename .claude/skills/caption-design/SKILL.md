---
name: caption-design
description: Design and place on-screen text (captions, asides, labels, place/time cards, sound words, emphasis words) creatively and consistently — a per-project caption kit (fonts, colours, treatments, animations per caption type) plus shot-by-shot placement in each shot's calm, face-free caption zone. Use whenever an edit gets text: vlogs, films, shorts, tutorials. Not one white caption in one place — every caption is targeted to its shot.
---

# Caption design

**Consistent system, targeted placement.** A film's text should feel like one designer made it (same fonts, colours,
treatments, motion vocabulary) while every single caption is *placed and timed for its shot* — top in one scene,
tucked beside a person in the next, low and small over the floor, riding the empty sky. Never the same white line in
the same spot for the whole film.

## 1. The caption kit (once per project) → `graphics/caption-kit.md` (+ VectorCraft/EffectCraft samples)
Made by the graphic-designer (type, colour, treatments) with the motion-designer (animations). Two directions are
always offered until the creator has a standing preference in `taste-profile`:
- **Playful & bold** — a heavy rounded/condensed display face, one bright accent colour for the key word, thick
  outline or soft drop shadow, small tilted tags/stickers for asides, pop/bounce/word-by-word motion.
- **Elegant & cinematic** — a script or handwritten face paired with a refined serif or wide tracked caps, soft
  gold/cream, thin rules or no decoration, slow fades, gentle drift, letter-tracking reveals.

The kit defines, for each **caption type**, font + size range + colour + treatment + entrance/exit + max words:
| Type | Job | Typical treatment |
|---|---|---|
| **voice** | the creator's first-person line ("I need a rest") | main face, sentence case, word-by-word or fade |
| **aside** | a joke / honest comment on what we see | secondary face, smaller, slight tilt, pop |
| **place/time** | where and when | tracked caps, thin rule, slide/track-in |
| **sound word** | *splash*, *creak*, *whoosh* — the sound made visible | display face, motion matches the sound |
| **emphasis** | one or two words that land a beat ("259.") | big, short, centred on the beat, hard cut in/out |
| **label** | who/what, only when it's also a joke | tag/pill with an arrow toward the subject |

Rules for the kit: max **two typefaces**; one accent colour; every type legible at phone size (cap height ≥ 3.5 % of
frame height for voice/aside); contrast handled by tone (light/dark from the zone) plus outline/shadow — never a heavy
box unless it *is* the style; flash-safe motion.

## 2. Placement — per shot, from the analysis
`tools/footage/analyze.py` reports **caption zones** for every moment (calmest 3×3 cells first, never cells with a face,
with the text tone that reads there: "dark text", "light text", "light text + shadow"). For each caption:
- Start from the zones, then *look at the frame*: put text where the eye can afford it — sky, wall, floor, the side
  the subject is looking away from, the space a person walks into.
- **Vary position with the composition**, not at random: follow the action's direction, sit opposite the subject,
  echo the shot's lines (a horizon, a railing, a stair edge). Consecutive shots shouldn't put text in the same spot
  unless it's a deliberate series (e.g. every place card bottom-left as a chapter signature).
- Respect safe areas (90 % title-safe for 16:9; 9:16 platform UI zones), never over faces, mouths or hands doing the
  action, never under a burned-in logo or the photographer's mark.
- **Integrate when it helps**: text partly behind a person/rail (masked), riding a pan, pinned to a sign.

## 3. Timing
Enter on the beat the caption comments on (a word, a look, a sound), hold long enough to read twice (≈ 0.3 s per word,
min 1.2 s), leave before the next idea; asides land *after* the moment, not before it. Sound words hit on the sound's
onset (from the analyser's bursts). No more than one caption on screen at a time (two only for a deliberate exchange).

## 4. Write it down, then check
In the cut plan, every caption carries: type, text, start/end, zone, position (x,y), tone, animation. Then render a
frame at each caption's mid-time (`contact.exe program`) and look: readable at 360 px wide? clear of faces? does the
position suit the shot? is the variety deliberate? The `creative-critic` checks the same.

## Never
- One style, one position, one size for every caption.
- Captions that describe what we can already see.
- Text over faces, or text that fights the busiest part of the frame.
- More than two typefaces, rainbow colours, or motion with no relationship to the moment.
