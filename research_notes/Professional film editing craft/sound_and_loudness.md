# Sound Editing, Mixing and Loudness Delivery for Video Editors

Scope: actionable numbers an AI film-editor agent can apply in an NLE (clip gain, volume keyframes, crossfades, ducking, EQ, compression, limiter, loudness-normalised export). Research date: 2026-10-10. Primary sources (EBU, Spotify, Apple, Netflix help centre, Adobe, FFmpeg) are preferred; tutorial and vendor pages are flagged as such.

## 1. Mixing order and level targets (dialogue, music beds, ambience, SFX, headroom, true-peak ceilings)

### Takeaway
Dialogue is the anchor. Set it first, peaking around -12 to -6 dBFS (roughly -23 to -16 LUFS short-term, depending on delivery). Then place music 12–25 dB under the voice during speech (15–20 dB is the usual default, 20 dB is the accessibility benchmark), and let it rise in the gaps. Ambience sits well below music, and SFX can be louder but are short. Finish with a true-peak limiter at -1 dBTP for web/streaming, or -2 dBTP for US broadcast and Netflix.

### Cited Findings
**Dialogue level (sample-peak meter conventions, NLE-level)**
- University Premiere Pro guide: overall audio "should be in the -12 to -6dB range, especially during dialogue", and should never hit 0 dB. — [PLU Premiere Pro KB](https://kb.plu.edu/100573)
- Adorama filmmaker guide calls -12 to -6 dBFS the "sweet spot" for dialogue: "high enough to avoid noise, low enough to leave headroom for sudden spikes." — [Adorama: Mastering Audio Levels](https://www.adorama.com/alc/mastering-audio-levels/)
- An Adobe Community expert says broadcast work typically aims for peaks of -12 dB or -6 dB. A client spec in the same thread asked for a 1 kHz reference tone at -20 dBFS, which shows delivery specs override the rule of thumb. — [Adobe Community thread](https://community.adobe.com/t5/premiere-pro-discussions/generated-audio-tone-6db-adobe-help-says-12db-client-asking-for-20dbfs-help-please/m-p/11064957/highlight/true)
- One documentary practitioner reported client broadcast limits of dialogue roughly -20 to -12 dBFS, maximum -6 dBFS and absolute peak -3 dBFS. This is a client spec, not a universal standard. — [DVInfo forum](https://www.dvinfo.net/forum/archive/index.php/t-112986.html)
- A Syracuse sound-mixing guide is internally inconsistent: it says dialogue should peak at -6 to -12 dB, and elsewhere at -6 to -3 dB. — [Syracuse: The Art of Sound Mixing](https://nhtraining.syr.edu/the-art-of-sound-mixing/)

**Per-element loudness targets (Adobe Premiere Pro Essential Sound "Auto-Match")**
- Reported Auto-Match targets: Dialogue **-23 LUFS**, Music **-25 LUFS**, SFX **-21 LUFS**, Ambience **-30 LUFS**. The targets are not adjustable in the panel; changing them means editing a config file. — [LinkedIn Learning/Lynda: Premiere Pro Guru, Essential Sound loudness](https://www.lynda.com/Premiere-Pro-tutorials/Using-Essential-Sound-panel-Loudness-dynamics/758641/2215703-4.html); [Adobe Community: Auto-Match question](https://community.adobe.com/t5/premiere-pro-discussions/audio-auto-match-question/m-p/14820232); [Larry Jordan: Modify Essential Sound Panel Settings](https://larryjordan.com/?p=82186). Caveat: these come from older courses and community posts, and no current Adobe page listing the values was found.
- Auto-Match measures per clip. After a clip is split, Premiere must recalculate LUFS for each segment. — [Adobe Community](https://community.adobe.com/t5/premiere-pro-discussions/audio-auto-match-question/m-p/14820232)

**Music bed under dialogue**
- WCAG 2.2 Success Criterion 1.4.7 (AAA): in prerecorded speech-primary audio, background sound must be at least **20 dB below** the foreground speech, or absent, or able to be turned off. — [WCAG 1.4.7 summary](https://www.disabilityworld.org/toolkit/standards/wcag/1-4-7-low-or-no-background-audio/)
- Pixflow suggests music roughly -18 to -25 dB under the voice, rising to about -10 dB when no one is speaking. — [Pixflow: How to Mix Dialogue, Music, and SFX in Premiere Pro](https://pixflow.net/blog/?p=92478)
- A production guide in the same search recommends music "often 15 to 20 dB under during talking," brought up in gaps. — [IRPR Sound: How to mix audio for YouTube](https://sounddesign.irpr.agency/guides/how-to-mix-audio-for-youtube/) (the search snippet did not show clearly whether this or [Morphic docs](https://morphic.com/docs/compose/audio) was the origin)
- A documentary editor sets music about 12 dB below the voice, which is the light end of the range. — [Adobe Community: VO and music](https://community.adobe.com/t5/premiere-pro-discussions/help-with-audio-settings-for-voice-over-and-music/m-p/12039621/highlight/true)

**Headroom and true-peak ceilings** (detailed in section 2)
- EBU R128: true peak ≤ **-1 dBTP**. — [EBU R128 (2014)](https://tech.ebu.ch/docs/r/r128-2014.pdf)
- ATSC A/85 / CALM Act practice: ≤ **-2 dBTP**. — [ProVideo Coalition: CALM Act](https://www.provideocoalition.com/the-calm-act-commercial-advertisement-loudness-mitigation/)
- Netflix: ≤ **-2 dBTP**. — [Netflix Sound Mix Specifications v1.5](https://partnerhelp.netflixstudios.com/hc/en-us/articles/360001794307-Netflix-Sound-Mix-Specifications-Best-Practices-v1-5)
- Spotify: below -1 dBTP, or below -2 dBTP if the master is louder than -14 LUFS. — [Spotify: Loudness normalization](https://support.spotify.com/artists/article/loudness-normalization/)
- Stems: dipped DME stems summed at unity should reproduce the full mix exactly. — [Frame.io Insider: 5 Broadcast Audio Specs (Jeff Hinton, 2017, updated 2020)](https://blog.frame.io/?p=2602)

### Inferences
- **Mixing order for the agent:** (1) Edit and level dialogue/VO with clip gain so the clips match. (2) Add room tone and ambience fill. (3) Add music and set the bed level. (4) Duck the music under speech. (5) Add SFX and transitions. (6) Bus processing: gentle compression on the dialogue bus, then a limiter on the master. (7) Measure integrated LUFS and true peak, adjust master gain, re-measure, export.
- **Starting relative levels** (synthesised from the Auto-Match targets plus the ducking guidance), with dialogue as 0 dB reference:
  - music under speech: -15 to -20 dB (no less than -12 dB)
  - music in gaps or a music-only montage: -6 to -10 dB relative, or the music becomes the anchor
  - ambience/room tone: about -7 dB relative to dialogue loudness (-30 vs -23 LUFS) and well below the speech
  - SFX: around dialogue level or up to about +2 LU for short hits (-21 vs -23 LUFS), but keep them short so they don't move the integrated loudness much
- In practice, -12 to -6 dBFS sample peaks on dialogue in a 48 kHz NLE timeline lands most speech around -20 to -16 LUFS short-term. Treat that as a rough relationship, not a conversion, since it depends on crest factor.

### Gaps
- No primary, standards-body source gives a numeric "music X dB under dialogue" rule for film/TV mixing. WCAG's 20 dB is the only formal number found. The rest are tutorial and practitioner figures.
- No current (2024–2026) Adobe documentation confirming the Auto-Match targets was found. Values come from older courses and community answers.
- No authoritative absolute level for ambience/room tone was found, beyond Adobe's -30 LUFS Auto-Match target and the advice to scale it to the scene (quieter for intimate moments, louder for wide shots) from [Production Expert](https://www.production-expert.com/production-expert-1/5-techniques-for-dialogue-editing-in-film-and-tv).

## 2. Loudness standards and platform targets (exact values) and what to export for online social video

### Takeaway
Broadcast specs are fixed: EBU R128 is -23 LUFS ±0.5 LU at -1 dBTP, ATSC A/85 is -24 LKFS ±2 dB at -2 dBTP, and Netflix is -27 LKFS dialogue-gated ±2 LU at -2 dBTP. Streaming and social platforms mostly normalise around -14 LUFS (Spotify official; YouTube widely measured but not officially published). Apple Podcasts is -16 LKFS ±1 dB at -1 dBTP. For online social video, export at -14 LUFS integrated with true peak ≤ -1 dBTP. TikTok, Instagram and Facebook publish no official targets.

### Cited Findings
**Measurement basics (ITU-R BS.1770 / EBU Tech 3341/3342)**
- EBU Mode meters (Tech 3341) use these windows:
  - momentary: 0.4 s sliding window, ungated
  - short-term: 3 s sliding window, ungated
  - integrated: gated per BS.1770-4, with an absolute gate at -70 LUFS and a relative gate at -10 LU below the absolute-gated level, using 400 ms blocks with 75% overlap
  - meters refresh at ≥10 Hz
  — [EBU Tech 3341](https://tech.ebu.ch/docs/tech/tech3341.pdf); [EBU loudness page](https://tech.ebu.ch/loudness)
- Loudness Range (LRA) is measured per EBU Tech 3342. R128 sets no maximum LRA. It is descriptive, and producers may limit it for aesthetic or practical reasons. — [EBU R128 (Wikipedia summary of the recommendation)](https://en.wikipedia.org/wiki/EBU_R_128); [EBU R128 (2014)](https://tech.ebu.ch/docs/r/r128-2014.pdf)
- Apple calculates LKFS and true peak according to **ITU-R BS.1770-5**, the current revision. — [Apple Podcasts: Audio requirements](https://podcasters.apple.com/support/audio-requirements)

**EBU R128 (Europe broadcast)**
- Target **-23.0 LUFS**, tolerance **±0.5 LU**. Where that is impractical (e.g. live), ±1.0 LU is allowed, but the exception "shall be clearly indicated". The ±0.5 LU tolerance dates from V3 (June 2014). — [EBU R128 (2014)](https://tech.ebu.ch/docs/r/r128-2014.pdf); [Wikipedia: EBU R 128](https://en.wikipedia.org/wiki/EBU_R_128)
- Maximum true peak **-1 dBTP** during production, measured to BS.1770/Tech 3341, with ±0.3 dB measurement tolerance. Lower ceilings may apply to some distribution and data-reduced systems. — [EBU R128 (2014)](https://tech.ebu.ch/docs/r/r128-2014.pdf)
- Current edition is **R128 V5 (November 2023)**, which adds references to R128 s3, s4 and Tech 3401. — [EBU R128 v5.0 PDF](https://tech-qual.ebu.ch/files/live/sites/tech/files/shared/r/r128v5_0.pdf); [Wikipedia](https://en.wikipedia.org/wiki/EBU_R_128)
- R128 s1 (ads/promos): a secondary source says it adds a **maximum short-term loudness of -18 LUFS**. This was not verified against the s1 text. — [Wikipedia: EBU R 128](https://en.wikipedia.org/wiki/EBU_R_128)

**ATSC A/85 / US CALM Act**
- Target **-24 LKFS**, tolerance **±2 dB** (acceptable -26 to -22). True peak not above **-2 dBTP**. Short-term (3 s) readings may briefly exceed the window. Some networks demand ±1 dB, and some still keep a legacy -10 dBFS peak limit. — [ProVideo Coalition: CALM Act](https://www.provideocoalition.com/the-calm-act-commercial-advertisement-loudness-mitigation/)
- The A/85 target is the long-term average loudness of the "anchor element", which is dialogue for long-form programmes. — [Sports Video Group](https://www.sportsvideo.org/2011/01/12/calm-act-suppliers-give-broadcasters-the-tools-to-manage-loudness/)
- The CALM Act references A/85 "and any successor thereto." — [TV Technology: LKFS & the CALM Act](https://www.tvtechnology.com/opinions/lkfs-amp-the-calm-act)
- Frame.io's general editor guidance is "between -23 and -25 LKFS for the entire length of the program", varying by distributor. — [Frame.io Insider (2017/2020)](https://blog.frame.io/?p=2602)
- Caveat: these A/85 numbers come from trade press. The ATSC A/85 PDF itself was not retrieved.

**Netflix**
- Dialogue loudness **-27 LKFS ±2 LU**, measured dialogue-gated with ITU-R BS.1770-1 over the full programme. True peak **-2 dBTP**. Peaks are to be handled by peak limiting, not by lowering the mix. Recommended monitoring reference is **79 or 82 dB SPL**. For Atmos, true-peak limiters on all beds and objects should be at -2.3 or lower, and loudness is measured on a 5.1 re-render. — [Netflix Sound Mix Specifications & Best Practices v1.5](https://partnerhelp.netflixstudios.com/hc/en-us/articles/360001794307-Netflix-Sound-Mix-Specifications-Best-Practices-v1-5) (page now redirects to a login-gated studiopartner.netflix.net "Knowledge Hub"; values taken from search extracts of the help-centre page); [Production Expert: optimise a mix for Netflix](https://www.production-expert.com/production-expert-1/how-to-optimise-an-audio-mix-for-delivery-to-netflix?format=amp)
- Netflix QC flag thresholds (QC partners only): print master -27 LKFS (±3), M&E and print-master true peak not above -1 dBTP, with a 1770-3 fallback of -24 LKFS. These are QC flag thresholds, not mix targets. — [Netflix: Loudness and True Peaks – How to Measure and When to Flag](https://backlothelp.netflix.com/hc/en-us/articles/360050414014-Loudness-and-True-Peaks-How-to-Measure-and-When-to-Flag)
- Dialogue gating was controversial when introduced in 2018, partly because Dolby had discontinued its Dolby Media Meter. — [Pro Tools Expert (2018)](https://www.pro-tools-expert.com/home-page/2018/8/23/has-netflix-turned-the-clock-back-10-years-or-is-their-new-loudness-delivery-spec-a-stroke-of-genius)

**Spotify (official)**
- Playback target about **-14 LUFS integrated** ("Normal"). Premium settings are Loud -11, Normal -14, Quiet -19 LUFS, applied across all formats including lossless.
- Spotify turns loud tracks down and quiet tracks up, but upward gain is limited by headroom: it leaves 1 dB headroom for lossy formats. Example: a -20 LUFS track peaking at -5 dBTP is raised only to -16 LUFS.
- Mastering advice: target -14 LUFS integrated and keep true peak below **-1 dBTP**, or below **-2 dBTP** if the master is louder than -14 LUFS.
- Spotify's playback limiter acts at -1 dB with 5 ms attack and 100 ms decay. The "Loud" setting applies regardless of true peak.
- Source for all four points above: [Spotify for Artists: Loudness normalization](https://support.spotify.com/artists/article/loudness-normalization/)

**YouTube (no official published number)**
- YouTube changed its playback reference to about **-14 LUFS** (integrated, BS.1770-style) in September 2019, per mastering engineer Ian Shepherd's measurements. YouTube turns loud content down but generally does **not** turn quiet content up. — [MeterPlugs / Ian Shepherd: YouTube changes loudness reference to -14 LUFS](https://meterplugs.com/blog/2019/09/18/youtube-changes-loudness-reference-to-14-lufs.html)
- "Stats for nerds" → "Volume / Normalized" shows "content loudness": the video's loudness relative to YouTube's reference. Worked example: a -22.2 LUFS video sits 8.2 dB under the -14 LUFS reference. — [Youlean: YouTube loudness](https://youlean.co/?p=30813)
- Frame.io describes YouTube as targeting "-12 to -14 LUFS" (approximate, undated page, ©2021). — [Frame.io Workflow Guide: Loudness for YouTube](https://workflow.frame.io/guide/loudness-for-youtube)

**Apple**
- Apple Podcasts (official): precondition audio to about **-16 dB LKFS ±1 dB**, true peak no higher than **-1 dBFS**, measured to BS.1770-5, done before encoding. — [Apple Podcasts: Audio requirements](https://podcasters.apple.com/support/audio-requirements)
- Mono measures differently from stereo: -16 LUFS stereo corresponds to about -19 LUFS mono when exporting a mono podcast. — [Podnews: LUFS/LKFS FAQ for podcasters](https://podnews.net/article/lufs-lkfs-for-podcasters)
- Apple Music Sound Check: third-party mastering guides put playback at about **-16 LUFS** with a recommended -1 dBTP ceiling. They disagree on whether quiet tracks are turned up. No official Apple doc was found. — [MasteringBOX: Mastering for streaming](https://masteringbox.com/learn/mastering-for-streaming); [RoEx: master for streaming](https://www.roexaudio.com/blog/how-to-master-music-for-streaming-spotify-apple-music-deezer-youtube)

**Podcasts in general**
- -16 LUFS is the de facto podcast target and Auphonic's default for new productions. — [Podnews](https://podnews.net/article/lufs-lkfs-for-podcasters); [Auphonic: loudness targets](https://us.auphonic.com/blog/2013/01/07/loudness-targets-mobile-audio-podcasts-radio-tv/)

**TikTok / Instagram Reels / Facebook (no official numbers)**
- Tool vendors say TikTok and Reels normalise to around -14 LUFS, "similar to YouTube". One guide instead claims Instagram/TikTok "prefer louder mixes closer to -12 to -10 LUFS" without evidence. All are marketing pages, and none cites Meta or TikTok documentation. — [OpenClip: Audio normalization targets](https://openclip.app/learn/audio-normalization); [Opus Clip: Best loudness normalizers](https://opus.pro/blog/best-loudness-normalizers); [Sound&Go LUFS table](https://soundandgo.com/loudness-analyzer-and-lufs-normalizer/)

**Export tooling (FFmpeg loudnorm, EBU R128-based)**
- `loudnorm` defaults are I = **-24 LUFS**, LRA = **7 LU**, TP = **-2 dBTP**, `linear=true`. Linear mode needs `measured_I`, `measured_LRA`, `measured_TP` and `measured_thresh` from a first pass (`print_format=json`). — [FFmpeg loudnorm commit](https://ffmpeg.org/pipermail/ffmpeg-cvslog/2016-May/100083.html); [FFmpeg patch: two-pass example](https://patchwork.ffmpeg.org/patch/10029/)
- Linear mode only runs when the target LRA ≥ input LRA and the target TP allows it after the gain change. Otherwise it silently falls back to dynamic (compressing) normalisation. — [ffmpeg-user list (2022)](https://ffmpeg.org/pipermail/ffmpeg-user/2022-March/054422.html)
- loudnorm upsamples internally to 192 kHz, so set the output rate explicitly, e.g. `-ar 48000`. — [AnimeThemes wiki: audio normalization](https://animethemes.moe/wiki/encoding/audio_normalization)

### Inferences
- **Export decision table:**

| Destination | Integrated loudness | True peak | Notes |
|---|---|---|---|
| Online social video (YouTube, Shorts, Reels, TikTok, Facebook, Vimeo) | -14 LUFS | ≤ -1 dBTP | Mixing quieter loses perceived loudness, since YouTube does not turn quiet uploads up. Going louder than -14 just gets turned down and costs dynamics. |
| Dialogue-heavy web / podcast / Apple Podcasts | -16 LUFS ±1 | ≤ -1 dBTP | |
| Europe broadcast | -23 LUFS ±0.5 | ≤ -1 dBTP | |
| US broadcast | -24 LKFS ±2 | ≤ -2 dBTP | |
| Netflix | -27 LKFS dialogue-gated ±2 | ≤ -2 dBTP | |
| Spotify video/music | -14 LUFS | ≤ -1 dBTP | ≤ -2 dBTP if louder than -14 |

- **Safe automated recipe:** mix by ear with the master limiter ceiling at -1.0 dBTP (or -2.0 for broadcast/Netflix). Measure integrated loudness, apply static master gain to hit the target, and re-measure. If FFmpeg is the renderer, use two-pass `loudnorm=I=-14:TP=-1:LRA=11` with the measured values and `linear=true`, then confirm the second-pass output reports `normalization_type: linear`. If it reports dynamic, the mix's LRA or peaks are too wide and should be fixed in the mix, not by the normaliser.
- Short-form social content is consumed on phone speakers. A narrower LRA (roughly ≤ 8–11 LU) keeps speech intelligible. This is an inference: no platform publishes an LRA requirement.

### Gaps
- **YouTube, TikTok, Instagram/Facebook, Vimeo:** no official published loudness targets were found (2023–2026). The YouTube -14 LUFS figure is industry-measured. TikTok/Meta figures are vendor claims only.
- **Apple Music Sound Check:** no official Apple document stating -16 LUFS was found. The Apple Digital Masters loudness rules were not found either.
- The ATSC A/85 primary document was not retrieved. Values are from trade press and are consistent across sources.
- The current Netflix spec page moved behind a login (studiopartner.netflix.net). The v1.5 values were confirmed only through search extracts of the help-centre page.

## 3. Audio editing technique: J/L-cuts, crossfades at cuts, room tone, music endings, cutting on downbeats, ducking settings, sidechain

### Takeaway
At every audio edit:
- put the cut on or near a zero crossing
- add the shortest fade or crossfade that kills the click, about 10 ms to 1–2 frames
- fill dialogue gaps with room tone (never dead silence)
- use J/L split edits so sound changes before or after picture

Cut music just before the "1" (downbeat) at phrase boundaries of 4 or 8 bars, and end on the track's real ending by back-timing it. Duck music 6–10 dB as a start (more for VO-led content), with about 30–60 ms attack and 300–700 ms release, or keyframe fades of about 800 ms.

### Cited Findings
**Crossfades and clicks**
- Sound On Sound: snap edits to zero crossings first (1-sample grid, zero-crossing snap), then apply an automatic crossfade if a click remains. — [Sound On Sound: Removing clicks with crossfades](https://www.soundonsound.com/techniques/removing-clicks-crossfades-sonar)
- Avid Pro Tools help: place selection starts and ends where the waveform meets the zero line, and crossfade between clips where a click or pop occurs. — [Avid Pro Tools First Help: Avoiding Clicks and Pops](https://apps.avid.com/protoolsfirsthelp/version12.3/enu/Pro%20Tools%20First%20Help/ed1.basics.23.08.html)
- Film Editing Pro: audio dissolves at dialogue edits are "usually … pretty short, either a 1 or 2 frame duration." — [Film Editing Pro](https://www.filmeditingpro.com/?p=24342)
- VEGAS's default "Quick Fade Length for Audio Events" is **10 ms**, and users report it prevents clicks at frame-boundary cuts. — [VEGAS forum: Auto Crossfades](https://www.vegascreativesoftware.info/us/forum/auto-crossfades--83076)
- Don't cover every pop with a long fade: long fades dull consonants and transients. Check that the fade hasn't removed the first consonant. — [DaVinci Resolve Club: fix clicks and pops](https://davinciresolveclub.com/fix-audio-clicks-pops-davinci-resolve/)
- Zero-crossing edits cannot fix a level mismatch, stereo phase mismatch, or a reverb tail cut at the boundary. — [Getly: how to loop audio seamlessly](https://www.getly.store/blog/how-to-loop-audio-seamlessly)

**J-cuts, L-cuts and room tone**
- A J-cut starts the incoming shot's audio before its picture. An L-cut lets the outgoing audio continue over the next picture, for example a cutaway or reaction shot while the speaker is still heard. Split edits stop dialogue feeling abrupt or ping-ponging. — [VEGAS: L-cuts and J-cuts](https://www.vegascreativesoftware.com/blog/l-cuts-and-j-cuts/); [Filmsupply: J-Cut and L-Cut](https://wpengine.fm.co/filmsupply/?p=3642)
- Record "at least a couple of minutes of room tone" on set and use it to bridge edits and underpin ADR. Scale it to the scene: quieter for intimate moments, louder for wide shots. Lower breaths rather than deleting them. Apply noise reduction in small, targeted sections, A/B against the original. — [Production Expert: 5 Techniques for Dialogue Editing (Paul Maunder, 17 Feb 2025)](https://www.production-expert.com/production-expert-1/5-techniques-for-dialogue-editing-in-film-and-tv)
- Room tone should fill the gaps, not sit under the dialogue, because levels add and the room would get louder whenever people speak. Crossfades handle the hand-offs between dialogue and room-tone fill. — [Videomaker: Radio edit techniques](https://www.videomaker.com/article/c3/14246-audio-for-video-using-radio-edit-techniques/)

**Music editing to picture**
- Listeners hear music in 4- and 8-bar phrases. Cut "right before the '1' beat, ideally after a full phrase", and never mid-beat or mid-chord. — [Artlist: editing music into your videos](https://artlist.io/blog/how-to-add-music-to-a-video/); [Storyblocks tutorial](https://www.storyblocks.com/resources/?p=25313)
- To end on the song's real ending:
  1. Find the beat to cut on.
  2. Cut on the beat right before the song's natural end.
  3. Join the two pieces with a short crossfade.
  4. If it sounds wrong, move the cut back 4 bars.
  5. Make sure the final downbeat lands after all dialogue.
  — [Storyblocks](https://www.storyblocks.com/resources/?p=25313); [RouteNote: sync music with visuals](https://licensing.routenote.com/blog/?p=9560)
- In montages, cut picture every 2 or 4 beats rather than on every beat. A fade-out, or a reverb/delay tail, can hide an awkward music edit. — [RouteNote](https://licensing.routenote.com/blog/?p=9560); [Artlist](https://artlist.io/blog/how-to-add-music-to-a-video/)

**Ducking (Premiere Pro Essential Sound auto-ducking)**
- Auto-ducking lives on clips tagged **Music**. Its parameters are:
  - Duck Against: which audio types trigger it (Dialogue, SFX, Ambience, unassigned)
  - Sensitivity
  - Reduce By (dB)
  - Fades (ms)
  - Generate Keyframes
- Adobe's tutorial example uses **800 ms** fades ("a little under a second"). Setting Sensitivity too high ducks almost the whole clip. Gaps in dialogue make the keyframed dips more pronounced.
- Source for all three points above: [Adobe: Automatic audio ducking](https://www.adobe.com/learn/premiere-pro/web/automatic-audio-ducking); [No Film School](https://nofilmschool.com/2018/04/save-time-adobe-premiere-pros-new-auto-ducking-tool)

**Sidechain compressor ducking**
- Route the voice to the music compressor's key or sidechain input. The music is reduced only while the voice is above threshold. — [Avid: Sidechain compression](https://www.avid.com/pro-tools/user-guide/sidechain-compression)
- Ratio: about 4:1 gives a typical music-under-speech duck, and 10:1 or more gives an obvious "radio" dip. Sound On Sound suggests a very high ratio so the duck is fully engaged whenever dialogue is present. — [Vindral Composer: Sidechain Ducking](https://composer-docs.vindral.com/operators/operators-sidechain-ducking.html); [Sound On Sound](https://www.soundonsound.com/node/4929859)
- Attack: 1–10 ms ducks instantly. 50–200 ms gives a softer fade-down but lets the first syllable's onset leak through. — [Vindral Composer docs](https://composer-docs.vindral.com/operators/operators-sidechain-ducking.html)
- A starting preset of **6–10 dB reduction, 30–60 ms attack, 300–500 ms release** appears in a creator-tool guide. That guide also says to lengthen release to **400–700 ms** if the music pumps or jumps back between phrases, and to shorten attack or move keyframes earlier if the first word is buried. — [CapCut: audio ducking guide](https://www.capcut.com/create/audio-ducking-for-clear-dialogue-in-video) (vendor tutorial)
- OBS compressor defaults (generic, not ducking-specific): -18 dB threshold, 6 ms attack, 60 ms release. — [OBS: Compressor filter](https://obsproject.com/kb/compressor-filter)

### Inferences
**Default edit parameters for the agent:**
- Dialogue cut: snap to a zero crossing, then a 5–10 ms crossfade, or up to 1–2 frames (≈42–83 ms at 24 fps; 33–67 ms at 30 fps). Room-tone fill joins: crossfade of about 2–5 frames.
- Ambience bed handoffs between scenes: crossfade 0.5–2 s, or J-cut the ambience 0.5–1 s ahead of picture.
- Split edits: lead the next scene's sound by about 6–24 frames on a J-cut. Hold the outgoing line through a reaction on an L-cut.
- These numbers synthesise the sources above. Only the "1–2 frames" and "10 ms" figures are directly sourced.

**Ducking via keyframes when the NLE has no sidechain:**
- Music at full bed level in gaps, and 10–20 dB lower under speech. Use 6–10 dB for light VO over energetic music, and 15–20 dB for dense information or accessibility.
- Ramp down starting about 200–300 ms before the first word, and ramp up about 300–800 ms after the last word.
- Don't let the music bounce back up for gaps shorter than about 1 s. Bridge them instead.

**Music ending:** back-time the track so its natural final hit lands on the last picture beat. Make the edit on a downbeat at a phrase boundary 4 or 8 bars earlier, with a 1–3 frame crossfade (longer if reverb tails clash). If a fade-out is unavoidable, fade over 2–4 s ending at the end of a phrase rather than mid-phrase.

### Gaps
- No primary source (Adobe, Avid or Apple docs) stating NLE default audio-transition durations was retrieved. Premiere's "Default Audio Transition Duration" preference and FCP's audio fade defaults were not verified.
- Adobe does not document numeric defaults or ranges for auto-ducking Sensitivity or Reduce By in the sources found.
- No authoritative source gives a numeric pre-lap (J-cut lead) duration. It is a craft judgement.
- No primary source gives exact ducking attack/release values for film/TV. The numbers above are creator-tool and product-doc starting points.

## 4. Sound design for short-form: whooshes, risers, impacts, swells, shutter/flash SFX, foley, silence, sound-led transitions

### Takeaway
Transition SFX should be cut to length, not stretched:
- whoosh: peak exactly on the cut
- riser or reverse riser: crest on the cut, then hard-stop into silence or a hit
- impact or boom: lands on the cut or reveal to resolve the movement

For photography content, put shutter clicks on the exact frame changes, choose a shutter type that matches the camera on screen, mix them under the music, and save flash and whoosh sounds for key reveals. Silence after a riser is itself an effect. Evidence here is thin and mostly from SFX vendors.

### Cited Findings
- "A whoosh has to match the move it covers, so length is everything." Cut the sweep to the transition rather than stretching a stock file. "A short whoosh peaking on the edit point carries the eye across it." — [Morphic: Whoosh sound effects](https://morphic.com/resources/sounds/whoosh-sound-effect) (SFX vendor)
- A reverse riser "leads into a cut rather than covering one, so the silence after is the effect." Pairing a rush with a dull hit means the "hit resolves the movement, so the transition arrives somewhere." — [Morphic: Whoosh](https://morphic.com/resources/sounds/whoosh-sound-effect)
- Shutter SFX should match the camera in shot: mirror slap for a pro DSLR, leaf blade, or a synthetic phone click. A rapid run of clicks can carry rhythm in slideshow openers or recaps. Overlapping releases suggest an off-screen crowd of photographers. — [Morphic: Camera shutter sound effects](https://morphic.com/resources/sounds/camera-shutter-sound-effect)
- Sync each click to the frame change using the waveform, keep it from competing with dialogue or music, and use fades/EQ to polish. Example brief: "subtle camera shutter clicks in sync with image changes (not too loud)". Flash-plus-shutter suits "caught on camera" reveals. — [Pippit/CapCut: shutter SFX templates](https://pippit.capcut.com/templates/shutter-sound-effect); [ElevenLabs: whoosh SFX](https://elevenlabs.io/sv/sound-effects/whoosh); [Motion Array: camera flash SFX](https://motionarray.com/sound-effects/camera-flash-362700/)
- Recorded camera audio often doesn't deliver the needed impact, even at normal speed. Designers layer many effects to build the final sound. — [DIY Photography: Slow motion sound is fake](https://www.diyphotography.net/slow-motion-sound-in-videos-is-fake-well-most-of-it-is/)
- J-cuts and L-cuts are the standard way to let sound lead or trail picture. — [Filmsupply](https://wpengine.fm.co/filmsupply/?p=3642)

### Inferences
**Placement rules for the agent:**
- Whoosh: align the loudest point of the waveform (not the clip start) to the cut. Typical lengths are 6–20 frames for fast cuts and up to about 1 s for slow pushes.
- Riser: end it exactly on the cut frame. Follow with either an impact on the cut or 4–12 frames of near-silence then the impact.
- Impact or sub-drop: transient on the reveal frame.
- Shutter click: transient on the frame where the still appears or the flash white-frame happens.
- Level SFX so the transient peaks don't push true peak past the limiter. Short transients barely move integrated LUFS but do hit TP.
- Use SFX sparingly: whooshes only on major transitions, and flash sounds for one or two punchlines. Otherwise they turn into noise. This follows the vendor advice.
- **Sound-led transitions:** start the next scene's ambience, music hit or line of dialogue before the visual cut (J-cut). The audio change tells the viewer a transition is coming and makes hard cuts feel motivated.
- **Silence as a tool:** a brief music or ambience drop-out of about 0.5–1 s before a reveal or punchline, keeping only a low room tone, increases the impact of the next sound.

### Gaps
- Soundworks Collection, No Film School and PremiumBeat pages giving specific numeric guidance on whoosh/riser timing were not retrieved. Sourced material is SFX-vendor pages, so treat it as practitioner opinion.
- No authoritative source on "sound leads picture" (e.g. Walter Murch) was retrieved in this session. The principle is standard practice but is uncited here.
- No sourced numeric SFX level targets relative to dialogue, beyond the reported Adobe Auto-Match SFX target of -21 LUFS (section 1).

## 5. Natural/on-camera audio in montages and BTS content, and under slow motion

### Takeaway
In slow motion, don't keep the camera audio stretched or pitched. Replace it with designed sound: a continuous real-time ambience or room-tone bed plus a pitched-down whoosh, impact "bloom" or sustained swell timed so it bottoms out at the slowest point. Only keep pitched audio deliberately, as an effect. In montages and BTS edits, natural sound works as punctuation: short real-time "nat sound" pops under or between music phrases.

### Cited Findings
- Audio recorded while shooting slow-mo "becomes indistinguishable and just quite muddy" and adds nothing. Most slow-mo sound in finished videos is designed from other SFX, not camera audio (cameras often don't record audio at high frame rates). — [RouteNote: Slow-mo sound effects](https://licensing.routenote.com/blog/?p=7109); [DIY Photography](https://www.diyphotography.net/slow-motion-sound-in-videos-is-fake-well-most-of-it-is/)
- Premiere Pro keeps audio pitch when clips are slowed ("Maintain Audio Pitch"), which can create artifacts. Unchecking it lets audio slow and drop in pitch with the video. VEGAS has an equivalent preference. — [Storyblocks: slow motion in Premiere](https://www.storyblocks.com/resources/wp-json/wp/v2/posts/520); [VEGAS forum: Super slow motion sound](https://www.vegascreativesoftware.info/us/forum/super-slow-motion-sound--84317)
- Designed slow-mo sound is typically a downward whoosh or warbling time-stretch that drops in pitch, sometimes over a low sustained hum. Match the sound's length to the slow-motion clip "so the sweep bottoms out exactly as the shot reaches its slowest point." An "impact bloom" turns one hit into a slow swelling boom with a long tail. — [Morphic: Slow motion sound effects](https://morphic.com/resources/sounds/slow-motion-sound-effects) (vendor)

### Inferences
**Slow-motion recipe:**
1. Mute or lower the speed-ramped camera audio.
2. Keep a real-time (unstretched) ambience/room-tone bed running continuously across the ramp so the world doesn't change speed sonically.
3. Add a designed slow-mo element (pitched-down whoosh or swell) aligned to the ramp-in, and an impact or bloom on the key moment.
4. Optionally duck or low-pass the music during the slow section, about 6–10 dB and/or a low-pass filter around 1–3 kHz, then restore on the ramp-out.

**Montage/BTS nat-sound handling:**
- Keep 0.5–2 s bursts of real sound (laugh, shutter click, "that's the shot!", door slam) at or near dialogue level.
- Duck the music about 6–12 dB under each burst with short ramps of about 100–300 ms, then return.
- Under continuous montage music, run a quiet bed of location ambience (about 15–25 dB under the music) so cuts don't feel sterile.
- Whenever camera audio is cut on picture cuts, add 5–10 ms fades to every nat-sound clip edge to avoid clicks.

### Gaps
- No authoritative source (post-production textbook, Soundworks Collection interview) explicitly states "use real-time ambience under slow motion". That point is inference from the designed-sound guidance and general practice.
- No sourced numeric guidance on nat-sound levels in montage/BTS edits was found.

## 6. Basic dialogue processing chain (HPF, de-noise, EQ, compression, de-essing, limiter)

### Takeaway
Order of operations:
1. Clean-up (de-noise, de-click, de-hum)
2. High-pass about 80–100 Hz at a gentle slope (higher for thin voices, lower for deep voices)
3. Subtractive EQ: cut mud/boxiness about 200–500 Hz and nasal resonance about 800 Hz–1.5 kHz
4. Presence lift of 1–2 dB around 2–5 kHz
5. Gentle compression, 2:1–3:1, soft knee 5–10 dB, a few dB of gain reduction
6. De-esser at 5–10 kHz after any high-frequency boost
7. Bus or master limiter at the delivery true-peak ceiling (-1 or -2 dBTP)

### Cited Findings
- Production Expert (Feb 2025):
  - do clean-up and noise reduction in targeted sections and A/B it
  - high-pass to remove rumble, but don't thin the voice
  - presence boost "around 2–5 kHz", especially in noisy scenes
  - "gentle compression (2:1 or 3:1 ratio)"
  - "a knee of 5 to 10 dB" is more natural on dialogue than a hard knee
  - use a de-esser for harsh sibilance, or a resonance suppressor such as Oeksound Soothe
  — [Production Expert: 5 Techniques for Dialogue Editing](https://www.production-expert.com/production-expert-1/5-techniques-for-dialogue-editing-in-film-and-tv)
- iZotope vocal EQ guide (music-oriented but transferable):
  - steep high-pass "anywhere between 50–100 Hz and below"
  - 1–100 Hz holds room rumble, handling noise and bleed
  - presence and intelligibility sit at 1.5–5 kHz, where boosts or cuts of "no more than 1 or 2 dB" are common
  - nasal resonance sits at 800 Hz–1.5 kHz
  — [iZotope: How to EQ vocals](https://www.izotope.com/community/blog/how-to-eq-vocals)
- iZotope: a gentle 6 dB/octave slope removes less than a steep one at the same corner frequency. — [iZotope: Parametric EQ](https://www.izotope.com/community/blog/parametric-eq)
- iZotope: high-frequency boosts may induce more sibilance, so compensate with a de-esser. A dynamic EQ can pull a presence boost back on loud lines so it doesn't turn harsh. — [iZotope: When to use dynamic EQ in a mix](https://www.izotope.com/en/learn/when-to-use-dynamic-eq-in-a-mix)
- Sibilance sits roughly between 2 and 10 kHz depending on the speaker, and is typically targeted at 5–10 kHz. De-essers can work split-band (dip only the offending band) or wideband. — [Kdenlive docs: De-esser](https://docs.kdenlive.org/de/effects_and_filters/audio_effects/volume_and_dynamics/deesser.html); [Soundcy: what is de-essing](https://soundcy.com/article/what-is-deess-sound-editing)
- A typical engineer chain runs de-esser → compressor → limiter. A lot of production dialogue arrives already compressed or limited, so check the source before adding more. — [Gearspace: dialogue compression thread](https://gearspace.com/threads/dialogue-compression.951277/)
- Dedicated dialogue processors bundle the same chain: Wave Arts Dialog has low/high-pass brickwall filters, de-ess, compressor and peak limiter. McDSP SA-2 has five EQ bands plus a de-esser. — [Adorama: Wave Arts Dialog](https://www.adorama.com/wave-arts-dialog-post-production-speech-voice-processor-plugin/p/wadialog); [Thomann: McDSP SA-2](https://www.thomannmusic.com/mcdsp_sa_2_dialog_processor_hd.htm)

### Inferences
**Agent default dialogue preset** (starting points, adjust by ear and metering):
- **Clip gain:** match clip levels first so dialogue peaks at about -12 to -6 dBFS.
- **De-noise:** light broadband reduction of about 6–12 dB at most. Heavy settings cause "underwater" artifacts.
- **HPF:** 80 Hz at 12 dB/oct for male voices, 100–120 Hz for female or child voices, and 60–70 Hz if the voice is very deep.
- **EQ:**
  - cut -2 to -4 dB at 200–400 Hz (Q about 1–2) if muddy or boxy
  - cut -2 to -3 dB around 800 Hz–1.2 kHz if nasal
  - boost +1 to +3 dB shelf or bell at 3–5 kHz for presence
  - optional gentle air shelf of +1 to +2 dB above 10 kHz
- **Compressor:**
  - 2:1–3:1, soft knee 5–10 dB
  - 3–6 dB of gain reduction on louder phrases
  - attack about 5–20 ms, release about 50–150 ms (or auto)
- **De-esser:** 5–8 kHz (up to 10 kHz), 3–6 dB of reduction on "s" sounds only.
- **Limiter:** on the dialogue bus or master, ceiling -1 dBTP for web/podcast or -2 dBTP for broadcast/Netflix, with true-peak detection enabled.
- Of these values, only 2:1–3:1, the 5–10 dB knee, 2–5 kHz presence, 50–100 Hz HPF and 1–2 dB boosts are directly sourced. The attack/release, cut depths and de-noise amounts are practitioner synthesis.

### Gaps
- No iZotope or Adobe document giving a full numeric dialogue chain for film/TV (attack/release, threshold, de-noise amount) was found. Most iZotope material retrieved is music-vocal oriented.
- Adobe Essential Sound "Dialogue" preset internals (Clarity, Reduce Noise and Dynamics values) were not documented in the retrieved sources.
