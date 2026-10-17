# Professional Colour Correction and Colour Grading for Video (Lumetri-style reference for an AI editor agent)

Scope note: research for an agent that grades through Lumetri-style controls (Temperature, Tint, Exposure, Contrast, Highlights, Shadows, Whites, Blacks, Saturation, Vibrance, Curves, Colour Wheels, HSL Secondary, Creative Look + Intensity, Faded Film, Vignette). Primary books (Van Hurkman's *Color Correction Handbook* / *Look Book*) and paywalled Mixing Light / Lowepost content could not be read directly; where their numbers appear they come via secondhand reproductions and are flagged. Search result pages were treated as leads; facts below cite the page the fact came from. "Inferences" are my synthesis and practical starting values, not sourced standards.

---

## 1. Correction vs grading, and the order of operations

### Takeaway
Correction makes footage neutral and consistent: input transform for log, then white balance, exposure, contrast, saturation, then shot matching. Grading then adds the creative look, with secondaries and vignette last. Every source agrees on "balance first, look after", because each operation feeds the next and a look applied on unbalanced footage behaves unpredictably.

### Cited Findings
- Adobe calls white balance "a common first step": an unwanted colour cast distracts, so you "begin by restoring the image to natural-looking colors". Temperature, Tint, Exposure, Contrast, etc. follow in Basic Correction — [Adobe: Correct skin tones](https://www.adobe.com/learn/premiere-pro/web/correct-skin-tones)
- Lumetri's WB Selector eyedropper: click a neutral object (white shirt, sign, paper) in the Program Monitor and Temperature/Tint update automatically. Then verify on the RGB Parade ("more balanced color channels") instead of trusting your eyes — [Adobe: Correct skin tones](https://www.adobe.com/learn/premiere-pro/web/correct-skin-tones)
- Larry Jordan's order: set grey-scale (exposure) first, then colour (hue and saturation). Anything that should be grey forms a single dot at the centre of the vectorscope — [Larry Jordan: Make People Look Normal](https://larryjordan.com/articles/color-correction-make-people-look-normal/)
- Node and operation order matters because each step's output is the next step's input. A colour-wheel balance before a desaturation gives a different result from the reverse order — [Pomfort: Order of Operations](https://pomfort.com/article/order-of-operations-for-creating-looks-on-set/); [DVResolve: Building node trees](https://dvresolve.com/tutorial/building-node-trees-davinci-resolve/)
- Common diagnostic sequence: correct exposure, neutral balance and obvious shot-to-shot differences first, then shape contrast and colour with primaries/curves, then build the creative look. Colourists often use a fixed structure so "the same types of adjustments are done on the same node for each shot" — [DVResolve: Recommended node tree](https://dvresolve.com/tutorial/recommended-node-tree-color-grading/)
- Cullen Kelly (feature-film first pass): exposure is the first adjustment on every shot. He works in "a fixed node tree built on simple, photographically-oriented tools", and the philosophy is to "establish a strong global look, then adjust only what needs it" (a "presumption of innocence" for each shot). The group-level look is built from layered film-LUT instances, and primary/HDR contrast sets a scene-wide contrast foundation — [Mixing Light: Inside the Grade – First Pass on a Feature](https://mixinglight.com/color-grading-tutorials/inside-the-grade-the-first-pass-on-a-feature)
- Stylised looks (bleach bypass) should come after the basics: "Do your white balance and contrast correction first, then apply the effect, then fine-tune" — [Imagineer/Boris FX: Bleach bypass in Resolve](https://blog.imagineersystems.com/blog/bleach-bypass-in-davinci-resolve-step-by-step-guide)
- Teal-orange guides say the same: correct contrast and exposure before applying the look — [Adobe: Why use orange & teal grading](https://www.adobe.com/creativecloud/video/hub/features/why-use-orange-teal-grading); [PetaPixel: Orange & Teal](https://petapixel.com/2017/02/23/orange-teal-look-popular-hollywood/)
- Lumetri adjustments in all sections combine, so a look plus Faded Film, Vibrance, HSL Secondary and Vignette stack and can be tuned independently — [Adobe: Create a color look](https://www.adobe.com/learn/premiere-pro/web/create-color-look-video)
- Moonlight's colourist Alex Bickel started look development in pre-production. Test grades on pre-production footage informed how the DP exposed and lit, and they experimented to decide "how much of the contrast would come from the grade versus the lighting" — [Post Magazine: Coloring Moonlight](https://www.postmagazine.com/Publications/Post-Magazine/2017/March-1-2017/Coloring-Best-Picture-winner-i-Moonlight-i-.aspx); [ARRI: Moonlight DP James Laxton](https://arri.com/news-en/-moonlight-dp-james-laxton-creates-poetic-look-on-alexa)

### Inferences
- **Recommended agent pipeline for Lumetri (stop at any step that is already correct):**
  1. **Detect the profile.** Log/flat (see Q5) → Basic Correction > Input LUT = the camera-maker's log→Rec.709 LUT. Rec.709/Normal → no input LUT.
  2. **White balance.** Use WB Selector on a true neutral, or nudge Temperature/Tint until the RGB parade channels align on neutrals and greys sit at the vectorscope centre.
  3. **Exposure.** Use Exposure to place the subject's skin and midtones (Q2/Q3 targets).
  4. **Range.** Whites/Highlights set the top (no clipping unless deliberate), Blacks/Shadows set the floor.
  5. **Contrast.** Use Contrast or an RGB-curve S-curve.
  6. **Saturation/Vibrance.** Prefer Vibrance because it protects skin.
  7. **Shot match** to a hero shot.
  8. **Creative look** (LUT + Intensity, Faded Film, shadow/highlight tint) on an adjustment layer.
  9. **Secondaries** (HSL Secondary for skin/sky fixes).
  10. **Vignette.**
- Put corrections on individual clips and the look on an adjustment layer above the sequence or scene. This mirrors Kelly's "global look, adjust only what needs it" and keeps the look editable in one place.
- Correction targets are objective (scopes, neutrals, legal range). Grading targets are subjective, so agent rules should treat correction numbers as constraints and grading numbers as defaults.

### Gaps
- Adobe's Lumetri overview page returned 404 on direct fetch, so its exact wording on panel order is quoted only via a search snippet. I found no Adobe page that mandates an order. The Lumetri panel's section order (Basic → Creative → Curves → Colour Wheels & Match → HSL Secondary → Vignette) is from product knowledge, not a fetched source.
- Kelly's exact node-by-node layout is behind the Mixing Light paywall.

---

## 2. Lumetri-style controls: what each does and safe working ranges

### Takeaway
Most Lumetri sliders are bipolar (–100…+100, or ±5 for Exposure and Vignette Amount). Professional results come from small moves verified on scopes, not large slider swings. Creative looks usually come in too strong and get dialled back with Intensity.

### Cited Findings
- **Vibrance vs Saturation:** Saturation affects all colours equally. Vibrance increases the value of more muted colours and protects skin tones, so it adds colour "without making things like skin tones look unnatural" — [Adobe: Lumetri Color overview](https://www.adobe.com/learn/premiere-pro/web/lumetri-color-overview) (via search snippet); [Bucknell Color Lesson 2](https://colorandlight.blogs.bucknell.edu/2018/04/11/color-lesson-2-color-grading/)
- **Creative Look Intensity:** sits under the look preview and scales the whole look. Many preset looks are "a little on the extreme side" when first applied, so dial them back (or up) with Intensity — [Bucknell Color Lesson 2](https://colorandlight.blogs.bucknell.edu/2018/04/11/color-lesson-2-color-grading/)
- **Faded Film:** lifts black levels for a vintage film look. Adobe describes it as "chopping off the shadows a little" — [Adobe: Create a color look](https://www.adobe.com/learn/premiere-pro/web/create-color-look-video); [Bucknell](https://colorandlight.blogs.bucknell.edu/2018/04/11/color-lesson-2-color-grading/)
- **Worked Lumetri example** (sports/aged-film look): lower Highlights and raise Shadows to recover range, add a little Contrast, Look Intensity **120%**, Faded Film **20** "to simulate aged film" (softens blacks, gentle roll-off), lower Saturation while raising Vibrance, push shadow tint toward blue and highlight tint toward light orange, then add a vignette — [ProVideo Coalition: A closer look at the Lumetri Color panel](https://www.provideocoalition.com/a-closer-look-at-the-lumetri-color-panel/amp/)
- **HSL Secondary** isolates a colour range so a secondary correction applies only to it — [Evergreen Lumetri wiki](https://helpwiki.evergreen.edu/wiki/index.php/Lumetri_Color_-_Premiere_Pro)
- **Vignette** has four sliders:
  - **Amount:** starting point around **–1.5**.
  - **Midpoint:** how far the darkening reaches inward. Lower values move it toward the centre; **40–60** gives "a balanced look".
  - **Roundness:** closer to 100 is more circular, lower is more oval.
  - **Feather:** higher values give a smoother transition, and a softer feather is recommended.

  — [Boris FX: Vignette in Premiere Pro](https://borisfx.com/blog/how-to-add-a-video-vignette-effect-in-premiere-pro/)
- **Lumetri Scopes:** the Vectorscope YUV shows a skin-tone line along the –I axis that "appears for all people regardless of their skin color" — [Adobe: Correct skin tones](https://www.adobe.com/learn/premiere-pro/web/correct-skin-tones)

### Inferences
- **Slider ranges (product knowledge, not verified against an Adobe page this session):**
  - Temperature, Tint, Contrast, Highlights, Shadows, Whites, Blacks, Vibrance, Sharpen: –100 to +100, default 0.
  - Exposure: –5 to +5 (stops-like).
  - Saturation: 0–200, where 100 is unchanged.
  - Look Intensity: 0–200, default 100.
  - Faded Film: 0–100.
  - Vignette Amount: –5 to +5, Midpoint 0–100, Roundness –100 to +100, Feather 0–100.
- **Conservative "correction" band (agent default; exceed only with scope evidence):**
  - Temperature/Tint: ±5–25 for camera-WB errors. ±40+ means the footage is badly mis-balanced, so prefer the WB eyedropper.
  - Exposure: ±0.3–1.0 typical. Beyond ±1.5 on 8-bit, expect noise or banding (Q8).
  - Contrast: 0 to +25.
  - Highlights: –10 to –50 to recover. Shadows: +5 to +30 to open. Whites/Blacks: ±5–20 to set end points.
  - Saturation: 90–120.
  - Vibrance: 0 to +25.
- **"Grading" band:**
  - Look Intensity: 30–70% for subtle commercial or documentary work, 80–120% for stylised work.
  - Faded Film: 10–30 (above 40 reads as heavily stylised).
  - Vignette Amount: –0.5 to –2.0, Feather 50–80, Midpoint 40–60.
  - Shadow/Highlight tint: small saturation, about 5–20% of the wheel radius.
- Vibrance before Saturation when adding colour to scenes with people.

### Gaps
- No official Adobe page with exact slider ranges or HSL Secondary sub-controls (Key, Refine, Denoise, Blur, Correction) was retrieved. Confirm against current Premiere Pro help.
- No source gave numeric limits for Sharpen.

---

## 3. Scopes and numeric targets (waveform, parade, vectorscope, histogram, legal range)

### Takeaway
Use the waveform (luma, 0–100%/IRE) for exposure and range, the RGB parade for white balance (neutrals show three equal-height channel traces), the vectorscope for hue and saturation (neutrals at centre, skin on the I-line at about 10:30), and the histogram only as a rough distribution check. Broadcast-safe output keeps luma within 0–100% (8-bit codes 16–235). EBU R103 allows small excursions.

### Cited Findings
- **Waveform bands:**

  | Band | Level |
  |---|---|
  | Super-white | above 100% |
  | White | 100% |
  | Highlights | 66–100% |
  | Mid-tones | 33–66% |
  | Shadows | 0–33% |
  | Black | 0% |
  | Super-black | below 0% |

  Rule of thumb: "Caucasian skin is about 70% of white; black skin is about 20% of white" — [Larry Jordan: Make People Look Normal](https://larryjordan.com/articles/color-correction-make-people-look-normal/)
- **Vectorscope:** the skin-tone line sits at roughly the **10:30** position, running up-left. Skin should sit on the line or within tolerance. Neutral greys collapse to a single centre dot — [Larry Jordan](https://larryjordan.com/articles/color-correction-make-people-look-normal/); [Adobe: Correct skin tones](https://www.adobe.com/learn/premiere-pro/web/correct-skin-tones)
- **Sampling skin:** crop or isolate bare skin (throat, arm, leg) rather than the made-up face to read skin on the vectorscope — [Larry Jordan: Secret to setting skin colors](https://larryjordan.com/articles/the-secret-to-setting-skin-colors-accurately/)
- **RGB parade for white balance:** after correct WB, the Parade "will likewise show more balanced color channels" — [Adobe: Correct skin tones](https://www.adobe.com/learn/premiere-pro/web/correct-skin-tones)
- **Luma waveforms hide single-channel clipping.** Only fully white pixels reach the top of luma, so check the RGB parade for one channel clipping — [Kdenlive docs: Waveform and RGB Parade](https://docs.kdenlive.org/en/_sources/tips_and_tricks/scopes/waveform_and_rgb_parade.rst.txt)
- **Not every shot has a 100% white or 0% black.** For example, a shot's white point (paper) "might be between 85-90 IRE" so it looks white without glowing — [PremiumBeat: Non-absolute white and black points](https://www.premiumbeat.com/blog/color-grading-quick-tip-non-absolute-white-and-black-points/)
- **EBU R103:**
  - Each R, G, B component should ideally lie within 0–100% of the black-to-peak range.
  - A tolerance exists because YUV manipulation can create out-of-range RGB.
  - 8-bit system: expected video range **16–235**, preferred min/max **5–246**, total signal range **1–254**.

  — [EBU R103 (tech.ebu.ch)](https://tech.ebu.ch/publications/r103); [EBU R103 PDF](https://knowledgehub.ebu.ch/files/live/sites/tech/files/shared/r/r103.pdf)
- A Blackmagic forum user says broadcasters commonly use R103, which "allows for luma to go few % outside perfect levels". The same post cites a 10-bit luma tolerance window of 20–984 (user paraphrase, not the standard) — [Blackmagic forum](https://forum.blackmagicdesign.com/viewtopic.php?p=901371). The nominal 10-bit range of 64–940 is from general knowledge and was not fetched.
- **General Rec.709 guidance:** skin typically falls at **45–70 IRE**, depending on skin tone and lighting style — [MediaGear: Master video scopes](https://mediagear.ee/?p=421470)

### Inferences
- **Agent numeric targets (Rec.709 SDR, full-scale 0–100% Lumetri waveform):**

  | Element | Target |
  |---|---|
  | Deepest blacks | 0–5% (crush-free: keep a few pixels above 0 unless stylised) |
  | Faded/film look floor | 5–12% |
  | Shadows with detail | 5–30% |
  | Midtones / grey card (18%) | ~40–50% (Rec.709 normally maps 18% grey near 40–45%) |
  | Skin | see Q4 (roughly 35–75% for lit lighter skin; darker skin naturally lower) |
  | Diffuse whites (white shirt, paper) | 80–90% |
  | Brightest highlights / speculars | ≤100% for web, ≤100% luma (≤103% tolerance) for broadcast |
  | Pure white cyc | 95–100% (Q7) |

- **Reading the parade:** on a known neutral (grey/white object), R, G and B tops and bottoms should match.
  - R high and B low means too warm: lower Temperature.
  - B high means too cool: raise Temperature.
  - G high or low means a Tint error: G high → push Tint toward magenta (+), G low → toward green (–).
- **Histogram:** a pile-up against either edge signals clipping. A "comb" of gaps signals over-stretched 8-bit data (see Q8).
- For web delivery, export full legal range without hard-clipping. Only apply broadcast-safe limiting when delivering to broadcast.

### Gaps
- The commonly quoted EBU R103 tolerance of **–1% to 103% luma** (and –5%/105% RGB, which matches codes 5–246) was not confirmed in fetched text. Verify in the R103 PDF before hard-coding it.
- The I-line angle (often quoted as about 123°) was not confirmed by a fetched source. Only "about 10:30" was sourced.

---

## 4. Skin tones across all complexions, especially darker skin

### Takeaway
Hue is consistent across complexions: all skin sits on, or within about ±2° of, the vectorscope skin line. Luminance and saturation differ, and darker skin naturally sits lower on the waveform. Leading DPs and colourists working with Black skin preserve density, warmth and texture rather than lifting it toward "Caucasian" IRE levels. Lifting darker skin to brighten it and cool or teal shadow grades are the main causes of grey/ashy skin, and generic LUTs commonly push darker skin orange.

### Cited Findings
- **Van Hurkman's skin table**, as reproduced secondhand by Larry Jordan ("guidelines, not absolute rules"):

  | Skin type | Luma | Hue vs skin line | Saturation |
  |---|---|---|---|
  | Female Caucasian | 50–70% | +2° | 40% |
  | Male Caucasian | 45–65% | +2° | 35% |
  | Female Asian | 40–60% | –2° | 35% |
  | Male Asian | 35–50% | –2° | 30% |
  | Female Hispanic | 35–50% | +2° | 35% |
  | Male Hispanic | 30–45% | +2° | 30% |
  | Female Black | 15–35% | +2° | 20% |
  | Male Black | 15–35% | +2° | 15% |

  Mood-driven scenes may depart deliberately — [Larry Jordan: Secret to setting skin colors](https://larryjordan.com/articles/the-secret-to-setting-skin-colors-accurately/)
  - **Conflict:** another Larry Jordan article gives *maximum skin highlights* of Black female **25–50%** and Black male **15–35%** (excluding reflections), Caucasian female 50–75%, and Hispanic/Asian 35–55%. Saturation there is Black female ~25% and Black male 10–20% — [Larry Jordan: Make People Look Normal](https://larryjordan.com/articles/color-correction-make-people-look-normal/). The difference is likely "average skin" vs "max skin highlight".
- **A practitioner calls the older tables "a bit out of date" and "euro-centric".** For lit skin on linear/Rec.709 footage they work to lightest skin **60–65 IRE** and darkest skin **45–50 IRE** (about 42 IRE on V-Log L). Their own tests measured some darkest skin at 18–29 IRE. Forum opinion — [EOSHD forum](https://www.eoshd.com/comments/topic/49416-what-are-the-correct-skintone-values-in-ire-for-hlg-acquisition/)
- **Another shooter exposes faces at 45–75 IRE depending on complexion.** On very dark skin they expose "to keep the skin tone from being 'lost' in the shadows" — [DVInfo forum](https://www.dvinfo.net/forum/archive/index.php/t-481996.html)
- **Ava Berkofsky (DP, HBO *Insecure*):**
  - She rejects the convention of exposing dark skin around **70 IRE**. Pushing skin "up to 50 or 70 is just going to make the rest of the image look weird".
  - She prefers reflected or bounced light (white or canvas muslin, "so instead of adding more light, the skin can reflect it"), uses a reflective makeup base, and uses low-intensity LED (S2 LiteMat 4) when direct.
  - She uses a polarising filter to sculpt faces.
  - She rejects universal rules such as green or amber light on dark skin: "Everybody's skin is different, and there's no formula".

  — [SLR Lounge](https://slrlounge.com/ava-berkofsky-of-hbos-insecure-on-how-to-light-dark-skin); [PetaPixel](https://petapixel.com/2017/09/14/look-hbos-insecure-lights-black-actors); [DIYPhotography](https://www.diyphotography.net/?p=82613)
- **Bradford Young (DP, *Selma*, dir. Ava DuVernay):** deliberately limits "the amount of light we see in a space or a face". The darkness "doesn't totally sink the black actors" but "brings out the rich tones and textures of their skin", running against the assumption that Black skin needs maximum light. DuVernay: "It's challenging to differentiate all those skin tones." Kodachrome photography of the period was a reference — [The Stranger](https://www.thestranger.com/film/2015/01/14/21456854/cinematographer-bradford-young-illuminates-the-color-below-the-color-of-selma-and-a-most-violent-year); [Grantland Q&A](https://grantland.com/hollywood-prospectus/qa-selma-dp-bradford-young-on-the-lbj-controversy-being-a-black-cinematographer-and-a-most-violent-year/)
- **Moonlight** (DP James Laxton, colourist Alex Bickel):
  - Laxton wanted Black actors to "look natural and interesting" and skin to feel warm, not harsh.
  - Bickel brought out "a rainbow of rich beautiful skin tones".
  - He reportedly used a different film-emulation LUT per life chapter: Fuji (childhood), Agfa (adolescence), Kodak (adulthood).

  — [ARRI](https://arri.com/news-en/-moonlight-dp-james-laxton-creates-poetic-look-on-alexa); [Post Magazine](https://www.postmagazine.com/Publications/Post-Magazine/2017/March-1-2017/Coloring-Best-Picture-winner-i-Moonlight-i-.aspx); [Filmmaker Magazine](https://filmmakermagazine.com/?p=100603), which cites an IndieWire interview I did not fetch.
- **Ash and teal risk:** when teal is added to shadows, darker complexions can lose warmth and go ash/grey. The fix is to keep warmth in darker-skin areas while cooling the rest of the image — [Toolfarm: Achieve perfect skin tones](https://www.toolfarm.com/tutorial/achieve-perfect-skin-tones-when-color-grading/) (via search summary; page returned 403).
- **Generic LUTs on darker skin** can turn faces "orange, blotchy, or noisy". The same author recommends density adjustments over saturation sliders. This is a single low-authority blog, unverified — [Passion Fuels Ambition](https://www.passionfuelsambition.com/dark-skin-tone-color-grading/)
- **Lumetri check:** the YUV vectorscope skin line applies "for all people regardless of their skin color" — [Adobe: Correct skin tones](https://www.adobe.com/learn/premiere-pro/web/correct-skin-tones)

### Inferences
- **Agent rules for skin (all complexions):**
  1. Hue: put the skin cluster on the skin line (±2–5°). Off toward red/magenta → shift Tint toward green slightly or use HSL Secondary hue. Off toward yellow/green → shift Tint toward magenta.
  2. Saturation: skin cluster length roughly 20–40% toward the vectorscope's 75% targets. Lighter skin trends longer, very dark skin often shorter, but **do not desaturate darker skin to "clean" it**. It must keep a visible warm (red-yellow) vector or it reads ashy.
  3. Luma: expose for the face's character, not a fixed IRE.
     - Light skin: lit side about 55–75%.
     - Medium/olive skin: about 40–60%.
     - Dark/deep skin: about 25–50% (highlights on the lit side may reach 45–55%).
     - Keep the face above the scene's shadow mass so it separates. Never lift whole-frame Exposure just to brighten darker skin. That flattens the scene, raises noise and greys the skin.
  4. To add presence to darker skin, use Highlights and Whites, or an HSL Secondary on skin with a small luma lift (+3–8 IRE) plus a small saturation lift, so that specular sheen and texture carry the face. Leave Blacks and Shadows dense.
  5. With a teal/cool shadow look, protect skin. Use an HSL Secondary skin key to restore warmth, or limit the shadow-tint wheel so it does not reach skin luma (skin at 25–50% overlaps "shadows" for deep complexions). Keep Look Intensity lower (40–70%) when deep skin is in frame.
  6. Avoid orange: if a LUT or Vibrance pushes skin past the skin line toward orange-red with saturation above about 50% of the 75% target, reduce Intensity, lower orange saturation in HSL, or nudge Tint.
  7. In multi-complexion scenes, balance for the range rather than for one face. Check each face's cluster separately (isolate with a crop or mask).
- "Density" in colourist usage means skin that keeps colour and tonal weight (not milky or lifted). In Lumetri terms that means don't raise Blacks/Shadows or Faded Film heavily on dark-skin close-ups. Use contrast to keep the skin's internal tonal variation.

### Gaps
- I could not find direct, technical grading interviews (node or slider level) from the *Insecure* colourist, Joe Gawler, or Alex Bickel on Black skin. Available sources are DP-level lighting philosophy plus general grading blogs.
- Van Hurkman's own updated skin data (later editions reportedly revise the older table) could not be accessed.

---

## 5. Shot matching and a consistent look across a sequence

### Takeaway
Match the balance and exposure of every shot to a "hero" reference shot first, so the look sits on consistent inputs. Then apply the look once at group or sequence level (adjustment layer). Make per-shot tweaks only where a shot visibly breaks continuity.

### Cited Findings
- Kelly: "establish a strong global look, then adjust only what needs it". The global look is applied at group level (layered film-LUT instances) over a fixed per-shot tree. The first pass favours scrubbing and spot-checking over real-time playback, with a later pass at speed — [Mixing Light](https://mixinglight.com/color-grading-tutorials/inside-the-grade-the-first-pass-on-a-feature)
- Correct obvious shot-to-shot differences early, before the creative look — [DVResolve: Recommended node tree](https://dvresolve.com/tutorial/recommended-node-tree-color-grading/)
- Use a consistent structure so the same adjustment type lives in the same place on every shot — [DVResolve](https://dvresolve.com/tutorial/recommended-node-tree-color-grading/)

### Inferences
- **Agent matching procedure:**
  1. Pick a hero shot per scene (best-exposed, primary angle).
  2. For each other shot, match in this order:
     - black floor (waveform bottom),
     - white/highlight ceiling,
     - skin luma (same face within ±3–5 IRE across angles),
     - neutral balance (parade matched on a common neutral),
     - skin vectorscope angle and length,
     - overall saturation.
  3. Then compare background hue and luma.
- Use Lumetri's Colour Wheels & Match Comparison View and "Apply Match" (with Face Detection) as a first guess, then correct manually. This is product knowledge, not verified this session.
- Cross-camera mixes (e.g. Pocket 3 D-Log M + phone Rec.709 + Action cam) need each source converted to Rec.709 first, via the input LUT for log. Only then match.
- **Adjustment layers vs per-clip:**
  - Per-clip: input LUT, WB, exposure, range, shot matching, skin secondaries.
  - Adjustment layer per scene or sequence: creative look, Faded Film, grain/film effects, vignette.
  - Never put WB or exposure on a sequence-wide adjustment layer when sources differ.
- Continuity tolerance: shots cut together should not differ by more than about 5 IRE in skin luma or about 3–5° in skin hue unless motivated (lighting change, story beat).

### Gaps
- No fetched source gave numeric matching tolerances, and no source covered Lumetri's auto-match accuracy. The tolerances above are my own heuristics.

---

## 6. Log/flat footage: DJI D-Log M, D-Log, Rec.709/Normal (Osmo Pocket 3, Osmo Action)

### Takeaway
D-Log M is DJI's flat, wide-dynamic-range 10-bit profile. It must be transformed to Rec.709, normally with DJI's official "D-Log M to Rec.709" LUT, before any creative grading. Normal-profile footage is already Rec.709 8-bit and gets no input LUT. Action-cam LUTs from DJI are "vivid" variants.

### Cited Findings
- **DJI official LUTs:**
  - Osmo Pocket 3: "D-Log M to Rec.709 LUT".
  - Osmo Action 4 and Action 5 Pro: "D-Log M to Rec.709 **vivid** LUT".
  - Mini 4 Pro, Air 3, Air 3S: "D-Log M to Rec.709 LUT".
  - Mavic 3: separate D-Log M→Rec.709, D-Log→Rec.709, and D-Log→Rec.709 vivid LUTs.

  The page gives download links only, with no usage instructions — [DJI LUT downloads](https://www.dji.com/lut)
- D-Log M is "not a LUT" but "a lower-contrast video with a flat colour profile". It captures wide dynamic range with colours distributed evenly for more room in post — [Heliguy: What is D-Log M (Pocket 3)](https://heliguy.com/blogs/knowledge-base/what-is-the-dji-osmo-pocket-3-s-colour-mode-d-log-m/)
- Pocket 3 profiles: D-Log M is 10-bit and Normal is 8-bit. Normal suits quick turnarounds, D-Log M suits grading. Zebras around **95%** flag clipped skin and skies. Lock manual white balance (e.g. 5500K daylight). Expose slightly brighter while keeping highlights below clipping — [OMG Adrian: Pocket 3 settings](https://omgadrian.beehiiv.com/p/the-only-osmo-pocket-3-settings-that-matter)
- **Base ISO conflict for Pocket 3 D-Log M:** a low-quality article says ISO 400, a community wiki says "Base ISO 800 best", and a LUT vendor lists 50. Unresolved — [r/osmopocket wiki (mirror)](https://redlib.hbubli.cc/r/osmopocket/wiki/index); [Gamut BaseLUTs](https://gamut.io/camera/osmo-pocket-3/)
- A third-party vendor claims DJI's LUT "often clips saturated colors" and adds heavy contrast. This is a vendor claim and is not independent — [Gamut BaseLUTs](https://gamut.io/camera/osmo-pocket-3/)

### Inferences
- **How to tell footage is log/flat**, any two of:
  - The waveform is compressed: blacks float well above 0% (roughly 5–15%) and brights sit well below 100% even on bright scenes.
  - Low contrast and washed-out appearance.
  - The vectorscope trace is short (low saturation) even on colourful subjects.
  - Metadata or filename indicates a 10-bit HEVC/H.264 10-bit profile; on DJI, D-Log M is the 10-bit option.
  - Footage looks "milky grey" with skin reading pale or greenish-grey.

  Normal-profile footage already shows full contrast and saturation.
- **D-Log M workflow in Lumetri:**
  1. Basic Correction > Input LUT = DJI D-Log M to Rec.709 (Pocket 3) or the vivid version (Action).
  2. Set WB/Exposure *after* the LUT, with small moves. If the LUT clips highlights, reduce Highlights/Whites, or apply the LUT in Creative with Intensity 70–90% and rebuild contrast manually.
  3. Then do the look.

  Do not stack a creative "cinematic" LUT on raw log without the conversion.
- Action-cam "vivid" LUTs run hot. Expect to reduce Saturation 85–95 or Look Intensity to 70–85% for skin-heavy shots.
- Normal (8-bit) profile: grade gently (Q8 limits). It has less latitude than D-Log M 10-bit.

### Gaps
- DJI's official D-Log M documentation (black level, middle grey IRE, recommended exposure offset, native ISO) was not found. The ISO conflict remains unresolved.
- Whether Pocket 3 HLG footage needs a LUT for Rec.709 delivery was not covered by any fetched source.

---

## 7. Popular looks and how to build them with basic controls

### Takeaway
Most named looks are combinations of four levers: contrast curve shape, black-point lift, split-toning (shadow/highlight hue), and saturation or hue-selective saturation. Build each on top of a corrected base and protect skin.

### Cited Findings
- **Teal-orange:** push blue/teal into shadows and orange/yellow into highlights. Skin sits in orange, so teal shadows make skin pop. It needs foreground/background separation, so avoid tan or orange backgrounds. Correct first — [PetaPixel](https://petapixel.com/2017/02/23/orange-teal-look-popular-hollywood/); [Adobe](https://www.adobe.com/creativecloud/video/hub/features/why-use-orange-teal-grading)
  - Stills-tool starting values: Lightroom calibration Blue hue –100 / Red hue about +50; Zoner Red hue 100, Blue hue 75. These are tool-specific — [Zoner: Teal & Orange](https://learn.zoner.com/color-grading-step-by-step-iii-how-to-get-the-popular-teal-orange-look/)
- **Bleach bypass:** emulates skipping bleach in processing, retaining silver, giving low saturation and high contrast, often with grain.
  - Resolve tutorial: drop saturation to "around 15 or 20" (Resolve default is 50, so about 30–40% of normal) and use an S-curve.
  - Real film was often shot 1 stop under for this process.
  - Order: WB and contrast first, then the effect, then fine-tune.

  — [PremiumBeat: Bleach bypass in Resolve](https://www.premiumbeat.com/blog/color-grading-bleach-bypass-look-in-davinci-resolve/); [Imagineer/Boris FX](https://blog.imagineersystems.com/blog/bleach-bypass-in-davinci-resolve-step-by-step-guide); [HitFilm manual](https://www.manula.com/manuals/fxhome/hitfilm-pro/9/en/topic/color)
- **Aged or faded film (Lumetri):** Faded Film 20, Look Intensity 120%, shadows → blue, highlights → light orange, lower Saturation with higher Vibrance, vignette — [ProVideo Coalition](https://www.provideocoalition.com/a-closer-look-at-the-lumetri-color-panel/amp/)
- **Film emulation:**
  - There is "no one 'film look'" — [Mixing Light: Emulating halation](https://mixinglight.com/color-tutorial/emulating-film-halation-in-davinci-resolve)
  - Halation is a subtle red-orange glow around very bright sources. Grain is more visible in midtones. The film curve has deep but not crushed blacks and bright but not blown whites — [Imagen AI: Film emulation](https://imagen-ai.com/post/film-emulation-lightroom.md)
  - Typical stack: grain + halation + diffusion (Pro-Mist) + print-emulation LUT after a log→Cineon transform — [Video tutorial: Emulating 16mm/35mm](https://videohighlight.com/v/45z60vnPOBw)
  - Moonlight used different stock emulations per era — [Filmmaker](https://filmmakermagazine.com/?p=100603)
- **Black and white done well:** don't just desaturate, because different colours of equal luminance merge into "muddy gray". Use a channel mixer: skin lives mostly in the red channel.
  - Lower red and raise the others for moodier, darker skin.
  - Raise red and lower the others to brighten skin.
  - Lower red and blue and raise green for close-up skin contrast and lip definition.

  — [PremiumBeat: Channel mixer B&W](https://www.premiumbeat.com/blog/using-the-channel-mixer-for-a-better-black-and-white). Reducing blue darkens skies (yellow/red filter analogy) — [iColorist](https://icolorist.com/?p=2868) (via search summary). For near-monochrome with natural skin, blend a channel-mixer B&W over colour in Lighten mode — [iColorist](https://icolorist.com/?p=2868)

### Inferences — Lumetri recipes (starting values; apply on adjustment layer over corrected footage; verify skin on vectorscope)
- **Teal-orange (subtle commercial):**
  - Contrast +10–20.
  - Shadow Tint toward teal (about 200°) at low saturation. Highlight Tint toward orange (about 30–40°) at low saturation.
  - HSL Secondary: desaturate greens (–20 to –40) and shift green hue toward teal. Keep skin at its natural hue.
  - Saturation 100–110, Vibrance +10.
  - Check that deep-skin faces keep warmth (Q4 rule 5).
- **Warm film:**
  - Temperature +5 to +15.
  - Faded Film 10–20, or lift Blacks via the RGB curve's black point to 3–6%.
  - Soft highlight roll-off (Highlights –15 to –30, Whites –5 to –15).
  - Saturation 90–100, Highlight Tint warm, Shadow Tint slightly teal or neutral.
  - Grain if available.
- **Bleach bypass:**
  - Saturation 40–60 (of 100), Contrast +30–50 or a strong S-curve, Blacks –10 to –20.
  - Optional cool Temperature (–5 to –10).
  - Skin will go pale and metallic, which is intended. Use it sparingly on deep-skin close-ups, or restore a little warmth with HSL Secondary.
- **Pastel / airy / light wedding:**
  - Exposure +0.3 to +0.7 (keep the face below 80%).
  - Contrast –10 to –25, Highlights –20 to –40 (keep the dress at 85–92%, not clipped), Shadows +20 to +40.
  - Faded Film 10–25.
  - Saturation 80–95, Vibrance 0 to +10. Desaturate greens and yellows in HSL, warm the skin slightly.
  - On darker-skinned couples, rely on lifted shadows rather than raised Exposure so skin keeps density.
- **Moody / desaturated:**
  - Exposure –0.3 to –0.7, Contrast +10–25, Highlights –20, Blacks –5 to –15.
  - Saturation 60–85, Vibrance 0. Cool Temperature (–5 to –15) with skin protected.
  - Vignette Amount –1 to –2.
- **Film emulation:**
  - Faded Film 10–25 (blacks about 4–10%), soft highlight shoulder (Whites –10).
  - Subtle split-tone, grain overlay, slight halation (glow on highlights, red-orange) if the tool supports it.
  - Saturation 90–100 with yellows/greens shifted slightly.
- **B&W:**
  - Saturation 0 is the crude route. Better: before desaturating, use HSL Secondary or Hue-vs-Luma style curves to set the luminance of reds (skin), blues (sky) and greens.
  - Then add Contrast +15–30, Blacks set to about 0–3%, whites to about 95–100%.
  - Add grain for a film feel. Watch darker skin: don't let it merge into dark backgrounds, and raise red/orange luminance if it does.

### Gaps
- No authoritative colourist source with numbers was found for the "pastel/airy wedding" look. That recipe is my synthesis.
- The Van Hurkman *Look Book* recipes could not be accessed.
- No source verified the commonly quoted channel-mixer starting point of 70% red / 15% green / 15% blue for skin-friendly B&W; it surfaced only in a search summary.

---

## 8. Grading white-studio / cyclorama footage

### Takeaway
A white cyc meant to read as "infinite white" should sit at or just touch about 100% with a flat top and **all three RGB channels equal**. Hold the subject's whites (white wardrobe, paper) lower (about 85–92%) so they keep texture and separate from the background. Neutralise with the parade to avoid grey (too low) or blue/cyan (WB) whites.

### Cited Findings
- On cyc shots the background is often clipped deliberately to create the illusion of infinite white. If it doesn't clip, gradations and defects show — [CreativeCOW: White BG](https://creativecow.net/forums/thread/white-bg-no-waveform-monitor/)
- One shooter found the white looked grey until the background was lit just past 100 IRE, and that was accepted on a broadcast shoot — [CreativeCOW](https://creativecow.net/forums/thread/white-bg-no-waveform-monitor/)
- White objects (paper) may sit at 85–90 IRE so they look white without glowing — [PremiumBeat](https://www.premiumbeat.com/blog/color-grading-quick-tip-non-absolute-white-and-black-points/)
- Luma scopes hide single-channel clipping, so use the RGB parade to confirm a neutral, evenly topped white — [Kdenlive docs](https://docs.kdenlive.org/en/_sources/tips_and_tricks/scopes/waveform_and_rgb_parade.rst.txt)

### Inferences
- **Agent procedure for a white cyc:**
  1. WB on the cyc (eyedropper on an unclipped area of the backdrop), or align R=G=B on the parade. A blue top means warm it (Temperature +). Green or magenta means use Tint.
  2. Raise Whites until the cyc reaches 95–100% with a flat top. Use Highlights to even any falloff, and a vignette with *positive* Amount (+0.3 to +1.0) to brighten corners if the cyc falls off at the edges.
  3. Keep subject skin at its normal target (Q4). Don't let the Whites push drag skin up, and pull skin down with an HSL Secondary or mask if needed.
  4. Keep white wardrobe at 85–95% with visible texture.
  5. Preserve subject/background separation through a slight edge or shadow and contrast. If the cyc wraps into the subject's edges (glow), back it off 2–5%.
- Grey whites mean the cyc is under 85%: raise Whites/Exposure. Blue whites come from daylight-balanced LED vs a tungsten WB setting, or vice versa. Never use Saturation to "fix" a tinted cyc; use Temperature/Tint.
- 8-bit footage of a nearly-white gradient bands easily (Q9). Clipping the cyc to flat white is often cleaner than holding it at 97%, where banded falloff is visible.

### Gaps
- No colourist-authored source gives a formal cyc spec. The 95–100% figure comes from practitioner forum posts plus inference.

---

## 9. Avoiding banding, clipping and noise; 8-bit limits; how much is too much

### Takeaway
8-bit footage (256 levels per channel; Pocket 3 "Normal") tolerates only moderate pushes. Smooth gradients (skies, white cycs, studio walls) band first, and big shadow lifts expose noise and blockiness. 10-bit log (1,024 levels; D-Log M) withstands much larger moves, but nothing recovers clipped highlights.

### Cited Findings
- 10-bit has 1,024 levels per channel vs 256 for 8-bit. Pushing 8-bit too far produces banding and posterisation, with skies the worst case. A histogram shows "comb" gaps. Large whole-scene temperature or saturation shifts are risky — [DIYPhotography: 8-bit vs 10-bit editing](https://www.diyphotography.net/8-bit-vs-10-bit-editing/); [FilmDaft: Bit depth](https://filmdaft.com/what-is-bit-depth-definition-8-bit-vs-10-bit-vs-12-bit/)
- About 73 grey shades per stop with 10-bit S-Log. "8 bits for a 13 stop dynamic range is really not enough" — [Alister Chapman](https://alisterchapman.com/tag/bit)
- Many shooters consider log pointless without 10-bit, because log is designed to be stretched — [Digital Camera World: 10-bit vs 8-bit](https://www.digitalcameraworld.com/cameras/10-bit-vs-8-bit-video-what-are-they-and-is-there-a-real-difference)
- Dithering when reducing bit depth can disguise quantisation boundaries — [DIYPhotography](https://www.diyphotography.net/8-bit-vs-10-bit-editing/)
- Highlight protection at capture: use zebras around 95% on the Pocket 3 — [OMG Adrian](https://omgadrian.beehiiv.com/p/the-only-osmo-pocket-3-settings-that-matter)

### Inferences
- **"Too much" thresholds (agent guardrails; heuristics, not sourced standards):**

  | Control | 8-bit Rec.709 | 10-bit log after conversion |
  |---|---|---|
  | Exposure | ±1.0 | ±2.0 |
  | Shadows lift | ≤ +30 | ≤ +50 |
  | Saturation | 80–130 | 70–140 |
  | Temperature/Tint shifts | ≤ ±30 | ≤ ±50 |
  | Contrast stretch on flat 8-bit | ≤ +30 | n/a |

  Beyond these, inspect skies, gradients and dark areas for banding, block noise and colour noise.
- **Clipping checks:**
  - No large flat plateaus at 100% on skin or detailed highlights.
  - No channel clipping on the parade for coloured highlights (sunset reds, stage lights).
  - Blacks: no flat line at 0 over detail areas unless stylised.
- **Noise:** lifting shadows and raising Exposure amplifies noise, which matters most on small-sensor cameras (Pocket 3, Action) and in low light. Prefer lowering Highlights over raising Exposure. Prefer Faded Film or a black lift with slight darkening of midtones over brightening.
- **Banding mitigation:**
  - Grade in 32-bit/float (Premiere: enable high bit-depth/maximum render quality).
  - Add fine grain (it acts as dither).
  - Avoid heavy saturation on skies.
  - Export at high bitrate, and in 10-bit where the delivery allows.
  - Keep vignettes heavily feathered.
- Over-grading tells: skin off the skin line, orange or ashy faces, haloing around qualified (HSL) areas (soften with Denoise/Blur in HSL Secondary), crunchy blacks, neon saturation (vectorscope trace beyond the 75% target boxes), visible banding in skies or cyc.

### Gaps
- No source gave quantified thresholds for how far 8-bit or 10-bit footage can be pushed before banding. All numeric guardrails above are heuristics to be validated on real footage.
- Premiere-specific high-bit-depth render settings were not verified against Adobe docs this session.
