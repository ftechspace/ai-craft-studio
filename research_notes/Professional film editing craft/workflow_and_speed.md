# Professional Post-Production Editing Workflow & Speed/Time Manipulation (Slow Motion, Speed Ramps, Freeze Frames)

> Research notes for an AI film-editor agent. Every cited line has an inline source. Items marked **[derived]** are arithmetic computed from the stated formulas (no external source needed). Items marked **[unsourced practice]** are common industry practice I could not find a citable source for during this pass; the report writer should treat them as lower-confidence. Source quality caveat: Adobe HelpX pages returned HTTP 403 to the fetcher and no official Blackmagic manual page surfaced, so much of the software-specific detail comes from third-party tutorials and Adobe Community threads (flagged where relevant).

## 1. Workflow stages from ingest to picture lock, and the handoff to colour, sound and deliverables

### Takeaway
The professional pipeline is: ingest + verified backup → organise (bins/naming) → log & pull selects → stringouts → assembly → rough cut → fine cut (plus director's/producer's cuts) → **picture lock** → turnover (AAF to sound, XML/EDL to colour/online conform) → finishing → deliverables. Picture lock is the hard gate: sound and colour are cut to the frame, so any change after lock forces re-conforms and adds cost. Edit offline on intraframe proxies (ProRes Proxy/DNxHR/CineForm) whose frame rate, duration and timecode match the camera originals, then conform to the original camera files (OCF) for the online.

### Cited Findings
**Editing stages**
- Assembly: editorial works "a day or two behind" production, building from the previous day's dailies. It follows the script closely, includes every line and action shot, and is "sometimes more than twice the length of the final film". It has no VFX, colour, SFX and usually no temp music. Its main value is catching unusable shots while reshoots are still possible. — [Frame.io Workflow Guide: Editing Stages](https://workflow.frame.io/guide/editing-stages)
- First assembly is often 2–3× the finished duration. — [Motion Array: The 5 Stages of Video Editing](https://motionarray.com/blog/the-5-stages-of-video-editing) (per search summary); consistent with "more than twice" from [Frame.io](https://workflow.frame.io/guide/editing-stages)
- Rough cut: "several months of work" on a feature, usually with the director closely involved. The editor may trim the assembly or start over. VFX appear only as simplified temps, and sound is untouched by professionals. — [Frame.io Workflow Guide](https://workflow.frame.io/guide/editing-stages)
- Rough cut is frequently the longest stage. One estimate is "up to 10 weeks or more for a feature". A documented feature case reached its rough cut after three months. — [Macmillan *Filmmaking* ch.12](https://digfir-published.macmillanusa.com/filmmaking1e/filmmaking1e_ch12_2.html); [DoHistory: post-production of *A Midwife's Tale*](https://dohistory.org/film/process_post.html) (per search summary; which source gave "10 weeks" was not confirmed)
- Intermediate cuts vary by project: a "first cut" may be audience-tested, a "fine cut" may be shown to producers, a "director's cut" is common on features, and a "producer's cut" may follow and often becomes final. The director "seldom has the last word" unless they also produce or finance. — [Frame.io Workflow Guide](https://workflow.frame.io/guide/editing-stages)
- The fine cut works shot by shot ("fixing each frame individually"), where the rough cut works on overall structure. — [Cutback: Assembly vs Rough Cut](https://cutback.video/blog/assembly-cut-vs.-rough-cut-what-s-the-difference) (per search summary)
- Picture lock: "no further editorial changes are allowed". Locking is required so colour, sound and finishing can start, and later changes "cause issues and extra costs". VFX ideally wait for lock, but big VFX shows often lock sequences individually. — [Frame.io Workflow Guide](https://workflow.frame.io/guide/editing-stages)

**Organisation, selects, stringouts**
- Start with bins for Audio, Graphics, Media and Sequences. Organise bins by scene, shoot day or interview subject (bins can be nested), and label clips with a comprehensive naming convention. — [Curtin Univ. PrP Media Management](https://curtinmcasi.atlassian.net/wiki/spaces/POS/pages/2583639/PrP+-+Media+Management)
- A stringout is "a sequence of clips, with light trimming, laid out in linear order on an editing timeline". Narrative stringouts are ordered by scene/slate. Documentary stringouts are grouped by topic or subject. Selects are the clips pulled for the cut. — [Cutback: Stringouts vs Selects](https://cutback.video/blog/stringout-vs-selects-the-ultimate-guide-to-modern-video-prep-(with-ai-tools))

**Proxies / offline–online / conform**
- Premiere's proxy workflow makes lower-resolution, lightweight copies for smoother editing. It can also attach proxies made outside Premiere (other apps or cameras), which must be attached to the full-resolution media. — [Adobe HelpX: Ingest and proxy workflow](https://helpx.adobe.com/premiere-pro-next/organize-media/ingest-proxy-workflow/ingest-and-proxy-workflow.html)
- Premiere's built-in ProRes proxy presets are reportedly High/Medium/Low = 1920×1080 / 1280×720 / 960×540, all with "stretch to fill" on by default. Medium is suggested as the general default. — [Cutback: Proxy workflow in Premiere](https://cutback.video/blog/proxy-workflow-in-premiere-pro-full-guide); **contradicted by** an older 2020 Adobe Community answer listing 1536×790 / 1280×720 / 1024×540 — [Adobe Community](https://community.adobe.com/t5/premiere-pro-discussions/resolution-of-prores-low-medium-high-resolution-proxies/m-p/13894659). Preset values vary by version.
- Avoid H.264 for proxies (Long-GOP, poor for editing). Use ProRes, CineForm or DNxHR, which are intraframe and "visually lossless". — [Elements.tv: Proxy workflow in Premiere](https://elements.tv/blog/everything-you-need-to-know-about-the-proxy-workflow-in-adobe-premiere-pro/)
- Proxy frame size may differ if it divides evenly into the original (e.g. 960×540 for 1920×1080). Frame rate, duration and fielding must match. Only audio-channel mismatches trigger a warning in Premiere. — [Larry Jordan](https://larryjordan.com/?p=144414) (per search summary)
- "Online" is a workflow phase (working from the OCF). "Offline" is working from low-bandwidth transcodes (proxies). "Conform" is the process of rebuilding the proxy-edited timeline from the OCF or master-quality transcodes (e.g. DPX), usually via an EDL or XML. EDLs carry clip names, source timecode and record timecode. XMLs can also carry effects and transform data. — [Frame.io Insider: Conform category](https://blog.frame.io/category/workflow/conform)
- NLEs relink offline to online by metadata and timecode. If metadata is stripped or the **frame rate is changed**, the conform may fail to find the originals. — [OWC: Online vs Offline Editing](https://www.owc.com/ca/blog/online-vs-offline-editing-why-you-still-need-to-consider-proxy-videos); common timecode enables accurate relinks — [ProVideo Coalition](https://www.provideocoalition.com/frame-io-brings-filmic-pro-to-the-cloud-testing-the-workflow/)

**Sound turnover (after lock)**
- Lock picture first. Every sound is edited to the frame, so cut changes force the sound team to re-conform. "Locked" means no more changes to timing or shot order. — [Henri Rapp: Preparing delivery to audio post](https://henrirapp.com/preparing-delivery-to-audio-post-production/); [IRPR: Preparing files for audio post](https://sounddesign.irpr.agency/guides/how-to-prepare-files-for-audio-post-production/)
- AAF is preferred over OMF as more modern and reliable. OMF is capped at 2 GB with embedded audio. AAF keeps on-set track/channel names, while OMF keeps filenames. Premiere Clip Gain does not survive to Pro Tools via OMF. — [Production Expert: AAF and OMF from video editors](https://www.production-expert.com/home-page/2020/8/27/aaf-and-omf-from-video-editors-how-to-make-sure-what-they-provide-works-for-us); [Production Expert panel](https://www.production-expert.com/production-expert-1/aaf-and-omfs-post-audio-expert-panel-on-the-good-the-bad-and-the-ugly)
- Handle lengths vary by facility: one spec asks for embedded AAFs with **2-second handles**, another guide says a **minimum of 5 s, 10 s preferred**, and a mixer asks new clients for a consolidated AAF with **75-frame handles**. — [Todd-AO Sound Editorial turnover spec (PDF)](https://toddao.com/turnover_specs.pdf); [IRPR](https://sounddesign.irpr.agency/guides/how-to-prepare-files-for-audio-post-production/); [Production Expert panel](https://www.production-expert.com/production-expert-1/aaf-and-omfs-post-audio-expert-panel-on-the-good-the-bad-and-the-ugly) (exact per-source mapping of the 2 s and 5–10 s figures came from a search summary)
- Export at the native sample rate (usually 48 kHz) with embedded media. Keep production sound on its original tracks and don't bake in plugins. Supply a reference video exactly matching the locked cut, with burned-in timecode (BITC). Mark 29.97 DF with a semicolon and NDF with a colon. Two EDLs are typical: an audio EDL (clip names + sound roll names) for dialogue assembly and a video EDL for Foley cueing and re-conform. Always request and follow the facility's own turnover document "to the letter". — [Todd-AO turnover spec](https://toddao.com/turnover_specs.pdf); [Henri Rapp](https://henrirapp.com/preparing-delivery-to-audio-post-production/); [IRPR](https://sounddesign.irpr.agency/guides/how-to-prepare-files-for-audio-post-production/)
- After lock, sound design and colour can take weeks or months on features. — [Motion Array](https://motionarray.com/blog/the-5-stages-of-video-editing) (per search summary)

### Inferences
- **Agent pipeline checklist** (synthesised from the findings above, with gaps filled by [unsourced practice]):
  1. **Ingest**: copy cards with checksum verification to two separate drives (3-2-1 rule). Never edit from the card. Keep the original folder structure for the conform. [unsourced practice]
  2. **Organise**: bins `01_Footage/{Day or Scene or Subject}`, `02_Audio`, `03_Music`, `04_GFX`, `05_Sequences`, `06_Exports` ([Curtin](https://curtinmcasi.atlassian.net/wiki/spaces/POS/pages/2583639/PrP+-+Media+Management) bins plus numbering). Don't rename source files after the proxies are made, because metadata and timecode drive relinking ([OWC](https://www.owc.com/ca/blog/online-vs-offline-editing-why-you-still-need-to-consider-proxy-videos)).
  3. **Proxies**: make them when the source is Long-GOP H.264/H.265, RAW, or above 4K on a weak machine. Use ProRes Proxy / DNxHR LB at 1/2 or 1/4 resolution with the same frame rate and timecode ([Elements.tv](https://elements.tv/blog/everything-you-need-to-know-about-the-proxy-workflow-in-adobe-premiere-pro/), [Larry Jordan](https://larryjordan.com/?p=144414)).
  4. **Log/selects**: one pass through all footage, marking In/Out or subclips on usable moments and giving each a rating plus keywords (see section 2).
  5. **Stringouts**: one sequence per scene, topic or subject, built from selects only ([Cutback](https://cutback.video/blog/stringout-vs-selects-the-ultimate-guide-to-modern-video-prep-(with-ai-tools))).
  6. **Assembly**: everything in script or story order, about 2–3× final length.
  7. **Rough cut**: structure and story, temp music, temp VO. Target about 1.2–1.5× final length (unsourced estimate).
  8. **Fine cut**: frame-level trims, rhythm, J/L cuts, temp graphics, and speed effects finalised.
  9. **Picture lock**: written sign-off from the client or director.
  10. **Turnover**: AAF (embedded, 48 kHz, handles per spec, default 2–5 s if no spec) + reference MOV with BITC + EDLs to sound. XML/EDL/AAF + reference MOV to colour/online.
  11. **Conform/online**: relink to OCF and check every speed effect, reframe and freeze survived the round-trip (speed effects are a classic XML/EDL failure point; EDLs carry only limited speed info [unsourced practice]).
  12. **Deliverables**: master (e.g. ProRes 422 HQ/4444), web H.264/H.265, social cut-downs and aspect ratios, captions, M&E/stems as contracted. [unsourced practice]
- **Versioning** [unsourced practice]: never overwrite a sequence. Duplicate it before each round of notes and name it like `PROJ_CutName_v03_YYYY-MM-DD` (ISO date so it sorts). Keep an `_OLD` bin. Each client review export carries the version and date in the filename and a burned-in version slate.
- **Client notes loop** [unsourced practice]: collect timecode-anchored notes (e.g. in Frame.io), triage them into must, should and discuss, apply them on a duplicated version, and reply note by note. Typical contracts include 2–3 revision rounds. Notes after lock are change orders.
- **Render previews**: render-in-place or smart-render only for heavy segments (optical flow, Speed Warp, stacked effects). Resolve speed effects often need render-in-place to preview in real time ([Tuts+](https://photography.tutsplus.com/tutorials/how-to-create-slow-motion-in-davinci-resolve-with-optical-flow--cms-106752)).

### Gaps
- Official Adobe HelpX pages (time remapping, proxies) returned HTTP 403. I couldn't confirm current (2025–2026) preset resolutions or official wording.
- I found no authoritative source for sequence versioning/date-naming conventions, client-note handling or revision-round counts. These are [unsourced practice].
- I found no source giving typical fine-cut duration or colour/online deliverable specs (codec, loudness such as -23 LUFS / -24 LKFS, or caption formats). Another researcher's scope may cover deliverables.
- Avid-specific workflow guides (ScriptSync, PhraseFind, bin views) weren't reached.

## 2. Reviewing large amounts of footage efficiently (shooting ratios, selects-first, ratings, time per stage)

### Takeaway
Shooting ratios run from about 1:1 (animation) through 2:1–10:1 (scripted drama) to 20:1–100:1+ (documentary, reality, effects-heavy action). A 40-minute-for-1-minute brief is a 40:1 ratio, which is normal for documentary-style or commercial work. The efficient method is selects-first: one disciplined viewing pass that tags and rates, then cutting only from selects and stringouts. Budget about 45–60 minutes of editing per finished minute for a standard piece, 1–2+ hours for stylised work, plus the review time.

### Cited Findings
- Documentaries have the highest ratios, often above 100:1 since video. Film-stock productions typically ran 6:1–10:1, with video much higher. Animation is close to 1:1. — [Wikipedia: Shooting ratio](https://en.wikipedia.org/wiki/Shooting_ratio)
- One filmmaker's documentary ran about 60:1, i.e. one hour of footage per minute used. — [Moonblink / Mud Lake: shooting ratio](https://moonblink.info/MudLake/tech/ratio)
- Controlled narrative films are typically 2:1–4:1. Documentaries and reality "sometimes exceeding 20:1". — [Beverly Boy: What is shooting ratio](https://beverlyboy.com/filmmaking/what-is-shooting-ratio-in-film/)
- Hitchcock was about 3:1. *Apocalypse Now* was 95:1. *Primer* was 1.04:1 (about 78 minutes exposed for a 77-minute film). Golden-age Hollywood (1930–59) was about 10:1 (90-minute feature ≈ 25 hours shot). Effects-heavy films "will always, by necessity, have bigger ratios". — [No Film School](https://nofilmschool.com/2016/03/shooting-ratios-mad-max-fury-road-primer-hitchcock)
- *Mad Max: Fury Road* about 240:1. — [Vashi Visuals: shooting ratios of feature films](https://vashivisuals.com/shooting-ratios-of-feature-films/)
- Commercials are argued (opinion, not data) to run "well in excess" of *Fury Road* and *The Hateful Eight* ratios. — [TrinityP3](https://www.trinityp3.com/?p=22949)
- Editing time per finished minute: about 30–60 minutes for simple work. 20–30 minutes for a simple talking-head or social clip. 45–60 minutes for an experienced editor on a typical video. 1–2 hours for stylised, motion-heavy or story-driven work. Some estimates go to 3 hours, or 2–10 hours, per finished minute. Raw-footage volume is a major driver ("if the editor needs to sift through 10 hours of raw footage, it's going to take much more time"). — [TastyEdits](https://www.tastyedits.com/how-long-does-it-take-to-edit-a-video/); [VeedYou](https://www.veedyou.com/how-long-does-it-take-to-edit-a-video/); [Beverly Boy](https://beverlyboy.com/video-production/how-long-does-video-editing-take/); [DVinfo forum](https://www.dvinfo.net/forum/archive/index.php/t-64229.html) (blog and forum figures; which number came from which site was taken from a search summary)
- Feature editorial runs a day or two behind the shoot, assembling dailies as they come in. — [Frame.io Workflow Guide](https://workflow.frame.io/guide/editing-stages)

### Inferences
- **Selects-first protocol for a 40:1 job (40 minutes of raw for a 1-minute piece)** [derived + unsourced practice]:
  1. **Pre-sort (about 5 min)**: group clips by type (interview/A-roll, B-roll, action, establishing, cutaways) and by subject or location using bins or keywords.
  2. **Audio-first for interviews**: transcribe (Premiere Text-Based Editing, Resolve transcription, Avid ScriptSync/PhraseFind) and pull soundbites from the transcript. A 1-minute piece holds about 130–160 spoken words, so pick about 2–3× that in candidate bites. [unsourced: speech rate estimate]
  3. **Single viewing pass for visuals at 1.5–2× (J-K-L shuttle)**: mark In/Out on every usable moment and subclip it or add a marker. Viewing 40 minutes at 2× takes about 20 minutes ([derived]).
  4. **Rating scale** (map to NLE features [unsourced practice]): 3 = hero/must-use, 2 = good, 1 = usable/backup, X = reject (soft focus, bad exposure, camera bump, talent blink). FCP has Favorite/Reject natively. Resolve uses flags, clip colours and markers. Premiere uses marker colours, clip labels and the "Good" metadata column. Avid uses locators and clip colours.
  5. **Selects sequence**: put every 2–3-rated moment on one "SELECTS" timeline in story order. Aim for about 5–8× the final duration (5–8 minutes for a 1-minute piece) before the first cut. [unsourced heuristic]
  6. **Stringout to assembly**: cut down from the selects timeline, never from raw again unless a gap appears.
- **Time-budget template for a 1-minute piece from 40 minutes of raw** [derived from the per-finished-minute rates above]: ingest/proxies 15–30 min, review/selects 30–60 min, assembly/rough 30–60 min, fine cut and speed effects 30–60 min, revisions 30–60 per round. Total 3–5 hours plus colour and mix. This is consistent with the 2–10 hours/minute upper-range estimates once review and revisions are counted.

### Gaps
- I found no authoritative (survey or industry-body) data on commercial or branded-content shooting ratios. Figures are blog or anecdotal.
- I found no published guidance from professional editors on specific star-rating scales, review playback speeds or selects-to-final ratios. These are [unsourced practice].
- Frame.io Insider assistant-editor interviews on logging didn't surface in search.

## 3. Slow-motion frame-rate math, interpolation methods (frame sampling / blending / optical flow) and shutter angle

### Takeaway
**Conform speed % = timeline fps ÷ capture fps × 100.** Slow motion is cleanest when footage is *conformed* (interpreted) to the timeline rate, so every output frame is a real captured frame. Clean results need the "source frames advanced per output frame" to be a whole number (or exactly 1/n). Anything else makes uneven cadence (judder) unless you use frame blending (ghosting) or optical flow (warping artefacts). Optical flow is best used sparingly, on simple, high-contrast motion, at modest stretch (about 50% speed or faster). Shutter angle captured at high fps controls blur, and it shows up as strobing when HFR footage is ramped back to real time.

### Cited Findings
**Interpolation methods (Premiere)**
- **Frame Sampling** duplicates or drops whole frames and can look choppy. It suits sped-up footage, clips where quality doesn't matter, or footage already shot at a very high frame rate. — [Aiarty: Premiere time interpolation](https://www.aiarty.com/edit-video/premiere-pro-time-interpolation.htm)
- **Frame Blending** composites neighbouring real frames with partial transparency, giving motion blur and ghosting/double images. It's suggested for mild slow motion (about **70–90%** speed) or for a deliberately dreamy look. — [Aiarty](https://www.aiarty.com/edit-video/premiere-pro-time-interpolation.htm)
- **Optical Flow** estimates motion vectors and synthesises new frames, and works best with strong contrast. It doesn't separate subject from background pixels, so it warps where similar colours meet or where objects are occluded. Slowing to **20% or less** forces many synthetic frames, and the best results are at **50% speed or higher**. — [Aiarty](https://www.aiarty.com/edit-video/premiere-pro-time-interpolation.htm) (third-party, consistent with general practice)
- Export has its own Time Interpolation setting. An Adobe Community moderator advised leaving export at Frame Sampling when the export doesn't change frame rate (per-clip settings still apply). — [Adobe Community](https://community.adobe.com/t5/premiere-pro-discussions/time-interpolation-frame-sampling-and-opitcal-flow-in-ppro-then-again-in-media-encoder/m-p/12073975/highlight/true)
- **Known issue:** users report that Optical Flow and Frame Blending "haven't worked on speed ramps for about 7 years" in Premiere's time remapping. Adobe staff said it worked on their system, so the status is unresolved. — [Adobe Community bug thread](https://community.adobe.com/t5/premiere-pro-bugs/optical-flow-and-frame-blending-haven-t-worked-on-speed-ramps-for-about-7-years/idc-p/15460106)

**Interpolation methods (DaVinci Resolve)**
- Inspector → Retime and Scaling → Retime Process: **Project Settings / Nearest / Frame Blend / Optical Flow**. Nearest drops frames for fast motion and duplicates them for slow. Frame Blend dissolves adjacent frames. Optical Flow builds new frames by motion estimation and is the highest quality but most demanding. — [Tuts+: Slow motion in Resolve with Optical Flow](https://photography.tutsplus.com/tutorials/how-to-create-slow-motion-in-davinci-resolve-with-optical-flow--cms-106752)
- Motion Estimation options include Standard Faster/Better and Speed Warp Faster/Better. **Speed Warp (AI-based) is Studio-only** and very resource-heavy. Naming varies between versions. — [Tuts+: Speed Warp guide](https://photography.tutsplus.com/tutorials/mastering-slow-motion-with-speed-warp-in-davinci-resolve-a-comprehensive-guide--cms-108738); [Aiarty: Resolve slow motion](https://www.aiarty.com/edit-video/davinci-resolve-slow-motion.htm); older project-settings limitation — [Blackmagic Forum](https://forum.blackmagicdesign.com/viewtopic.php?p=752571)
- Two elements crossing in different directions, or unpredictable camera movement, cause optical-flow artefacts. In those cases **Frame Blend can look better**. Speed effects may need **render in place** to preview. — [Tuts+](https://photography.tutsplus.com/tutorials/how-to-create-slow-motion-in-davinci-resolve-with-optical-flow--cms-106752)

**Shutter angle at high frame rate**
- Shutter ≈ 1/(2 × fps) for a 180° shutter, so 120 fps → 1/240 s (or round to 1/250). Faster shutters cut exposure, so HFR needs more light. — [Stocksy support](https://support.stocksy.com/hc/en-us/articles/360049933392); [LibreTexts Video Production Handbook 7.09](https://human.libretexts.org/Bookshelves/Theater_Film_and_Storytelling/Video_Production_Handbook/07%3A_Camera_Functions/7.09%3A_Frame_Rate_and_Shutter_Speed)
- 180° is generally considered "normal" motion blur regardless of frame rate. — [DIY Photography: shutter angle vs shutter speed](https://www.diyphotography.net/why-shutter-angle-is-way-better-than-shutter-speed-when-shooting-video/). **Contradicted by** a forum view that 180° applies only to standard rates and HFR should use 360°. — [Blackmagic Forum](https://forum.blackmagicdesign.com/viewtopic.php?p=487822) / [Creative COW](https://creativecow.net/?p=1246952)
- HFR flickers under mains-powered lights (e.g. 240 fps under fluorescents). Match the shutter to mains frequency (50 Hz/60 Hz) as closely as the 180° rule allows. — [Blackmagic Forum](https://forum.blackmagicdesign.com/viewtopic.php?p=487822); [Creative COW](https://creativecow.net/?p=1246952)
- Interpreting 120 fps as 23.976 in Premiere gave "extreme strobing of the light sources" in one case. The workaround was to transcode to 59.94 first and then interpret as 23.976 (smoother, but less slow). — [DVinfo: FS700 120fps in 23.976](https://www.dvinfo.net/forum/archive/index.php/t-515430.html); [Adobe Community: 120 fps footage](https://community.adobe.com/questions-729/working-with-120-fps-footage-1399834)
- Shoot 60–120 fps to smooth handheld shots without a stabiliser, then slow down in post. — [PremiumBeat](https://www.premiumbeat.com/blog/tips-for-better-slow-motion-video)

### Inferences
- **Core formulas** [derived]:
  - `conform_speed% = timeline_fps / capture_fps × 100`
  - `slowdown_factor = capture_fps / timeline_fps`, and output duration = source duration × slowdown_factor
  - `source_frames_per_output_frame (k) = (capture_fps / timeline_fps) × (speed% / 100)`
    - k = 1 → full conform: every frame is real, perfectly smooth. **This is the "clean" target.**
    - k = an integer ≥ 2 → even frame skipping (e.g. 200%): clean fast motion.
    - k = 1/n (0.5, 0.333, 0.25) → each real frame held n times: even but stepped ("stutter-slow"). Needs optical flow or blending to look smooth.
    - k not an integer and not 1/n (e.g. 1.25, 0.4, 2.5) → uneven repeat/skip pattern = **judder** with Frame Sampling. Blending or optical flow hides it.
  - NTSC rates are exact fractions: 23.976 = 24000/1001, 29.97 = 30000/1001, 59.94 = 60000/1001, 119.88 = 120000/1001, 239.76 = 240000/1001. Within the same family (all /1001 or all integer) the ratios come out exact. Mixing the families gives about 99.9% ratios, e.g. true 120 → 23.976 = 19.98%, which leaves a frame repeat or skip roughly every 1000 frames. Agent rule: interpret to the timeline rate exactly (e.g. tell the NLE the clip is 23.976) instead of typing a percentage.
- **Conform table** [derived]:

| Capture fps | Timeline fps | Conform speed | Slow-down | Notes |
|---|---|---|---|---|
| 59.94 | 29.97 | **50%** | 2× | clean |
| 59.94 | 23.976 | **40%** | 2.5× | clean only as a conform. 50% on a 23.976 timeline gives k = 1.25, which judders |
| 119.88 | 59.94 | **50%** | 2× | clean |
| 119.88 | 29.97 | **25%** | 4× | clean |
| 119.88 | 23.976 | **20%** | 5× | clean |
| 239.76 | 29.97 | **12.5%** | 8× | clean |
| 239.76 | 23.976 | **10%** | 10× | clean |
| 50 | 25 | **50%** | 2× | clean (PAL) |
| 100 | 25 | **25%** | 4× | clean |
| 200 | 25 | **12.5%** | 8× | clean |
| 48 | 24 | **50%** | 2× | clean |
| 60 / 120 / 240 (integer) | 24 | 40% / 20% / 10% | 2.5× / 5× / 10× | clean within the integer family |
| 120 (integer) | 23.976 | 19.98% | 5.005× | family mismatch, so conform by interpreting |
| 50 | 23.976 | 47.95% | 2.085× | PAL capture on an NTSC timeline: non-integer, interpolate or accept judder |
| 59.94 | 25 | 41.71% | 2.398× | cross-standard, avoid |
| 29.97 | 23.976 | **80%** | 1.25× | subtle "dreamy" slow motion |
| 25 | 23.976 | 95.9% | 1.043× | near-real-time. Audio pitch drops about 0.7 semitone if not corrected |
| 1000 | 23.976 | 2.40% | 41.7× | specialist high-speed |

- **Maximum clean slow motion without interpolation** = timeline_fps ÷ capture_fps (e.g. 59.94 footage on a 23.976 timeline bottoms out at 40%). Going slower than that (e.g. 59.94 at 20%) gives k = 0.5, which needs optical flow and creates 1 synthetic frame per real frame. Practical limit: at most about 2× synthesis (k ≥ 0.5) for good results, matching the "50% or higher" guidance from [Aiarty](https://www.aiarty.com/edit-video/premiere-pro-time-interpolation.htm). Fall back to Frame Blend when objects cross or occlude ([Tuts+](https://photography.tutsplus.com/tutorials/how-to-create-slow-motion-in-davinci-resolve-with-optical-flow--cms-106752)).
- **Method choice for the agent**: (a) footage is HFR and the speed equals the conform % → Frame Sampling/Nearest (perfect). (b) Speed above 100% → Frame Sampling (or Frame Blend for a motion-blurred look). (c) Mild slow motion of 70–99% on standard-rate footage → Frame Blend. (d) Slow motion beyond the conform limit on simple, high-contrast motion → Optical Flow, or Speed Warp in Resolve Studio. (e) Optical-flow warping on crossing limbs, water, hair or foreground occlusion → switch to Frame Blend, shorten the shot, or cut away at the artefact.
- **Shutter implications** [derived]: a 180° shutter at 120 fps (1/240 s) keeps blur at half the frame-to-frame displacement, so conformed slow motion looks "normal-smooth". Played at real time in a 24p ramp (every 5th frame), that 1/240 s exposure equals an effective **36° shutter** (360 × 24/240), so real-time sections look staccato or strobed. General form: **effective_angle = captured_angle × (timeline_fps / capture_fps) ÷ (S / 100)**. Check: 180° × 24/120 ÷ 0.2 = 180° at the 20% conform speed, and 180° × 24/120 ÷ 1.0 = 36° at 100%. At conform speed it equals the captured angle. At 100% it shrinks by the slowdown factor. Below conform speed the formula exceeds the captured angle, but interpolated or repeated frames don't add real blur, so the look stays at the captured angle. Fixes: shoot HFR at about 270–360° when heavy ramps are planned (matching the forum 360° view, [Blackmagic Forum](https://forum.blackmagicdesign.com/viewtopic.php?p=487822)), or add synthetic motion blur to the real-time portions (Resolve Motion Blur, [Creative Video Tips](https://creativevideotips.com/tutorials/speed-ramp-with-motion-blur-in-davinci-resolve)).

### Gaps
- I couldn't access ASC/American Cinematographer HFR articles or official Adobe/Blackmagic manuals this pass. Interpolation descriptions come from third-party tutorials (consistent with each other).
- No source verified current (2025–2026) Premiere speed limits (e.g. maximum % in Speed/Duration vs time remapping) or whether Premiere's ramp + Optical Flow bug is fixed.
- No measured data on artefact thresholds (at what % optical flow fails) beyond the "≥50%" heuristic.

## 4. Speed ramps: construction, ease curves, durations, placement against action and music

### Takeaway
A speed ramp is a time-remap curve, normally 100% → slow (or fast) → 100%, with eased (Bezier) transitions. Land the slowest point on the peak of the action and on a strong musical accent (drop or downbeat), and snap back to speed after the impact. Use ramps on big moments, not every beat. Build them from HFR footage so the slow section is made of real frames, and manage motion blur so the fast sections don't strobe.

### Cited Findings
- **Premiere**: right-click the clip's fx badge → Time Remapping → Speed. Ctrl/Cmd-click the rubber band to add speed keyframes and drag the segment up or down. Split the keyframe and drag its halves to create a gradual transition, then use the Bezier handles to curve the acceleration or deceleration. — [Pixflow: Speed ramp in Premiere](https://pixflow.net/blog/how-to-speed-ramp-in-premiere-pro-a-step-by-step-tutorial-for-stunning-video-effects/); music-video workflow (markers, Automate to Sequence for beat cutting) — [Adobe: Edit a music video tutorial](https://www.adobe.com/learn/premiere-pro/web/edit-music-video)
- **After Effects**: Layer → Time → Enable Time Remapping (creates start and end keyframes). Add keyframes, apply Easy Ease, and refine in the Graph Editor (steeper curve = faster playback, flatter = slower). — [AEJuice: Speed ramping in After Effects](https://aejuice.com/blog/how-to-speed-ramp-footage-in-after-effects/)
- Beat sync: mark the beats, then use slower speed in quiet passages and faster speed on hits. For a hit, slow the frames leading into the beat and return to normal after the impact. A worked example at about 30 fps: 100% until frame 20, ease to **25% by frame 28** (the hit lands on the beat), ease back to **100% by frame 40**. That is an 8-frame (≈0.27 s) ramp in and a 12-frame (≈0.4 s) ramp out. Keep motion blur consistent through the ramp. — [AEJuice](https://aejuice.com/blog/how-to-speed-ramp-footage-in-after-effects/); [beat-sync skill page](https://www.claudemarket.ai/skills/iart-ai/motion-design-skills/beat-sync-editing) (low-authority source; treat the frame numbers as illustrative)
- Ramps work best on the big moments of a song, such as a drop: "ramp into a hit with slow-motion, then snap back to speed". Use HFR footage for smooth slow segments. — [Pixflow](https://pixflow.net/blog/how-to-speed-ramp-in-premiere-pro-a-step-by-step-tutorial-for-stunning-video-effects/); [AEJuice](https://aejuice.com/blog/how-to-speed-ramp-footage-in-after-effects/)
- Resolve: add motion blur to speed ramps to keep the fast parts natural. — [Creative Video Tips: Speed Ramp with Motion Blur in Resolve](https://creativevideotips.com/tutorials/speed-ramp-with-motion-blur-in-davinci-resolve)
- Premiere caveat: users report Optical Flow and Frame Blending are ignored inside time-remap transitions. — [Adobe Community bug thread](https://community.adobe.com/t5/premiere-pro-bugs/optical-flow-and-frame-blending-haven-t-worked-on-speed-ramps-for-about-7-years/idc-p/15460106)

### Inferences
- **Ramp recipe for the agent** [derived from the sources above + unsourced practice]:
  1. Use HFR source (≥59.94 for a 23.976 timeline). Set the clip's slowest speed to its conform % (e.g. 40% for 59.94 → 23.976, 20% for 119.88 → 23.976), so the slow plateau needs no interpolation.
  2. Find the action peak frame (impact, apex of a jump, kiss, ring placed on the finger, ball contact) and the music accent (drop, downbeat, snare hit). Align them so the **ramp reaches its slowest speed on or just before the peak**.
  3. Ramp-in: about 6–12 frames (0.25–0.5 s at 24 fps) for punchy action and sports. Up to 1 s+ for emotional, wedding or romantic pieces (unsourced ranges, consistent with the 8- and 12-frame example above).
  4. Hold the slow plateau for about 1–3 beats of the music (at 120 BPM, 1 beat = 0.5 s = 12 frames at 24 fps) [derived: frames per beat = fps × 60 / BPM].
  5. Ramp-out to 100% (or above 100% for a whip-like "speed-up then snap") over 8–16 frames, ending on the next downbeat or the cut.
  6. Ease all transitions (Bezier or Easy Ease). Linear changes look mechanical.
  7. Check fast segments for strobing. Add motion blur, or keep fast segments short.
  8. Sound: ramps need designed audio (whoosh or riser into the slow section, impact on the peak). Never let the camera audio pitch-glide unless that's the intended effect (see section 6).
- **Speed-ramp transition between two shots** [unsourced practice]: ramp the outgoing shot up (e.g. 100% → 300–500%) over its last 6–10 frames, cut on the fastest frame, and ramp the incoming shot down from the same speed to 100%. Matching motion direction across the cut hides it.
- **Frames-per-beat table** [derived, 23.976/24 fps]: 90 BPM = 16 frames, 100 BPM = 14.4 frames, 120 BPM = 12 frames, 128 BPM = 11.25 frames, 140 BPM ≈ 10.3 frames. At 29.97 multiply by 1.25.

### Gaps
- No authoritative (Adobe/Blackmagic or professional editor) source giving standard ramp durations. The only numeric example came from a low-authority page.
- No official Resolve documentation on the retime-curve UI (speed vs frame curve, Ctrl/Cmd+R retime controls) was retrieved. That is [unsourced practice].

## 5. Freeze frames: uses, durations, and combining with flash, zoom or B&W

### Takeaway
Freeze frames are used for character introductions (often with name-card text and narration), "photo-taken" moments (shutter click + white flash + optional desaturation or border), comic or narrative pauses for voice-over, and endings (the iconic final-frame freeze). Choose a sharp, expressive, motion-blur-free frame. Tie the freeze to a sound hit, and use it sparingly. No source gave standard durations, so the numbers below are practice-based heuristics.

### Cited Findings
- The common modern method is editorial: duplicate one frame and extend it for the desired duration. — [Vizard: What is a freeze-frame effect](https://vizard.ai/knowledge-base/video-production/what-is-a-freeze-frame-effect)
- Frame selection criteria: sharpness and focus, motion-blur artefacts, facial expression or body position, composition, and grain/noise consistency. — [Vizard](https://vizard.ai/knowledge-base/video-production/what-is-a-freeze-frame-effect)
- Character intros often overlay text or graphics with background info or quirky traits. *Snatch*'s opening names characters on screen in a specific style. *The Wolf of Wall Street* "literally pauses" on a freeze frame so the narrator can introduce himself. — [StudioBinder: freeze-frame examples](https://www.studiobinder.com/blog/what-is-a-freeze-frame-the-best-examples-why-they-work/); [Clipchamp: What is a freeze frame](https://clipchamp.com/en/blog/what-freeze-frame-film)
- Audio during a freeze may continue, fade out, shift to music or narration, or cut abruptly for emphasis. — [Vizard](https://vizard.ai/knowledge-base/video-production/what-is-a-freeze-frame-effect)
- A "crisp shutter click" turns the held frame into a photograph, "ideal for character intros and end-of-round summaries". Record scratches and metallic stabs are alternatives for other tones. — [Morphic freeze-frame SFX](https://morphic.com/resources/sounds/freeze-frame-sound-effects) (commercial SFX catalogue, so marketing copy)
- Overuse reduces impact or feels gimmicky. — [How To Film School: Freeze frame](https://howtofilmschool.com/dictionary/freeze-frame/); [Filmdaft](https://filmdaft.com/?p=24588)

### Inferences
- **Durations** [unsourced heuristics; no source found]:
  - Photo-taken beat: 0.5–1.5 s (12–36 frames at 24 fps), then cut or resume.
  - Character intro with a name card: long enough to read the card at about 3 words/s plus 0.5 s, typically 1.5–3 s.
  - Narrated pause (Wolf of Wall Street style): as long as the VO line needs.
  - Ending freeze: 2–5 s, often under music swell and the start of credits, or cut to black.
- **Build recipe** [unsourced practice]: (1) pick the frame (a sharp peak expression, no motion blur, using the sources' criteria above). (2) Premiere Frame Hold / Add Frame Hold, Resolve Retime → Freeze Frame, or export the frame and re-import it. (3) Optionally slow-ramp into the freeze (100% → 30% over 4–8 frames) so it doesn't feel like a glitch. (4) Photo moment: 1–2 frames of white (a flash, or a 2–4-frame white dip) + shutter SFX + snap to B&W/sepia or a slight desaturation, optional 2–5% punch-in or a slow push (Ken Burns) across the hold. (5) Intro: a freeze plus a hard-hit SFX or record scratch, then a name card animating on within 4–8 frames. (6) Keep ambience or music running under the hold unless an abrupt silence is the point.
- Limit freezes to one device per piece (e.g. all character intros) for stylistic consistency, per the overuse warnings above.

### Gaps
- No source (No Film School, PremiumBeat, StudioBinder) provided numeric hold durations or flash-frame counts. All timings above are heuristics.
- No source on whether reframed or scaled freezes survive an XML/EDL conform (generally they don't round-trip reliably; unsourced).

## 6. When slow motion works emotionally and when it hurts; audio under slow motion

### Takeaway
Slow motion earns its place on fast motion or intense emotion: action peaks, sports impacts, wedding and romance beats, laughs, tears, splashes, story turning points. It hurts when overused (it dilutes impact, as critics said of *Lord of the Rings*), when it drags a scene, or on dialogue (lip sync and pitch problems). For audio, don't play the camera sound pitched down by default. Mute it or keep it minimal and drive the moment with music, real-time ambience or designed sound. If original audio must stay, time-stretch with pitch correction, or ADR dialogue.

### Cited Findings
- "Slow-motion moments work best when there's either fast motion or intense emotions", e.g. laughing, crying, yelling, running, jumping, splashing. Save it for important moments, because using it everywhere makes it dull. "If changing the frame rate adds nothing, skip it." Don't stretch a sequence beyond what the scene needs. — [PremiumBeat: Tips for better slow motion](https://www.premiumbeat.com/blog/tips-for-better-slow-motion-video)
- Use slow motion at pivotal points: a significant shift in story direction, a climax of emotional intensity, or a complex action sequence that needs clarity. Dramas use it in tender, intimate moments "to savor the onscreen chemistry". — [FilmLifestyle: How to use slow motion](https://filmlifestyle.com/how-to-use-slow-motion-in-film/); [StudioBinder: slow motion iconic moments](https://www.studiobinder.com/blog/how-to-use-slow-motion-in-film-to-create-iconic-moments/)
- Rarity gives it power: if every punch is slow-mo the effect is diluted, while if only the crushing blow is, the impact is "monumental". Juxtapose slow and normal speed to keep momentum. — [StudioBinder](https://www.studiobinder.com/blog/how-to-use-slow-motion-in-film-to-create-iconic-moments/)
- A critic found *Lord of the Rings*' over-reliance on slow motion "grating" in the climax and argued that speeding up is often more effective than slowing down. — [Middlebury Videographic course](https://sites.middlebury.edu/videographiccourse/?p=485) (per search summary)
- Walter Murch: music is an emotional boost, but it must be the right music in the right dose (applies to scoring slow-mo moments). — [Web of Stories: Walter Murch](https://www.webofstories.com/play/56751)
- NLEs tie audio pitch to clip speed by default. Built-in pitch correction can sound "harsh, metallic". Premiere's correction was acceptable for instructional footage but not for a feature. — [DVinfo: pitch in slow-motion dialogue](https://www.dvinfo.net/forum/archive/index.php/t-537570.html)
- Options: mute the slow-mo audio and replace it with music, SFX or VO that fits the slower pace. — [Finchley: Mastering slow motion video editing](https://www.finchley.co.uk/finchley-learning/mastering-slow-motion-video-editing-cinematic-tips-for-your-next-shoot). Treat slowed dialogue as ADR — [DVinfo](https://www.dvinfo.net/forum/archive/index.php/t-537570.html). Use a better time-stretch algorithm (e.g. élastique in Vegas), or disable the auto pitch fix when a pitched effect is wanted — [DVinfo: slow-mo with sound](https://dvinfo.net/forum/what-happens-vegas/20375-slow-mo-sound.html); [Vegas forum](https://www.vegascreativesoftware.info/us/forum/super-slow-motion-sound--84317)
- A deliberate pitch-drop can work as a special effect on a ramp (game- and film-style "bullet time"). Designed slow-mo sound includes downward whooshes, slowing-tape textures, low-passed "underwater" beds, swelling booms with long tails for impacts, and reverse risers that stop when normal speed returns. Match the sweep length to the slow segment. — [DVinfo](https://www.dvinfo.net/forum/archive/index.php/t-537570.html); [Morphic slow-motion SFX](https://morphic.com/resources/sounds/slow-motion-sound-effects) (commercial catalogue)

### Inferences
- **Decision rules for the agent** [synthesised]:
  - USE slow motion when: (a) the shot has fast motion or peak emotion, (b) it lands on a story turning point or musical climax, (c) the genre expects it (sports highlights, weddings: walk-down, ring, first kiss, confetti, dress twirl; romance; action impacts; product hero shots), and (d) the source is HFR, so the conform gives real frames.
  - AVOID when: (a) someone is speaking on camera (lip sync breaks and slowed speech sounds wrong). Cut to a real-time sync shot or play the slow-mo only as B-roll under a real-time voice. (b) Pacing is information-driven (explainers, interviews, corporate). (c) It has already been used in the last 15–30 s of a short piece (unsourced spacing heuristic). (d) The footage is 24/25p and would need under 50% optical flow on complex motion.
  - **Budget** [unsourced heuristic]: in a 60 s promo, at most about 15–25% of runtime in slow motion. Individual slow shots about 1.5–4 s. Wedding films and music videos tolerate more.
- **Audio rule under slow motion** [synthesised from the above]: by default, mute the camera audio on any clip under about 90% speed. Carry the moment with music (cut the music, not the picture, to land the swell on the slow peak), plus a **real-time ambience bed** from the same location (unslowed room tone or crowd) for continuity, plus designed SFX (whoosh in, impact, reverse riser out). For 80–99% speeds, keep the original audio with pitch-preserving time-stretch (Premiere: Maintain Audio Pitch in Speed/Duration [unsourced UI detail]; Resolve's pitch correction option [unsourced]). Only use pitched-down audio as a deliberate stylistic effect.

### Gaps
- No primary sound-editor or MPSE source on slow-motion sound design conventions. Guidance comes from forums and SFX catalogues.
- No source with quantitative limits on how much slow motion is "too much" (percent of runtime, spacing). The heuristics above are unsourced.
- ASC/American Cinematographer pieces on the emotional use of HFR (e.g. *Raging Bull*, *Chariots of Fire*, Zack Snyder) were not retrieved.
