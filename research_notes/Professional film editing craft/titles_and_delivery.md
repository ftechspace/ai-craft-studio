# Titles, Graphics & Typography for Video + Technical Delivery Specs per Platform

Research date: 2026-10-10. All pages were fetched or searched on that date. A source's own date is given where the page shows one. "Official" means the platform's or standards body's own page. "Community" means third-party blogs or tools, and is flagged as such.

## 1. Title design: title cards, lower thirds, chapter titles, end cards, credits (safe areas, size, tracking, pairing, contrast, duration, animation, kinetic trends)

### Takeaway
Safe areas are the one hard standard. Keep action/essential picture inside 93% of the frame (3.5% margin per edge) and all text/graphics inside 90% (5% margin per edge), per EBU R95 v1.1 (June 2017) and SMPTE. Everything else is practitioner consensus with no single official standard: type size relative to frame height, tracking, fade timing and title duration. The agent should use the reading-rate rules from subtitling (Netflix 20 cps; BBC 160–180 wpm) to set on-screen duration, plus a "readable twice" floor.

### Cited Findings
**Safe areas**
- EBU R95 (Safe areas for 16:9 television production, v1.1, June 2017) sets an Action Safe margin of 3.5% and a Graphics Safe margin of 5%, measured at top, bottom and both sides. That leaves 93% and 90% of the frame. v1.1 added Note 5, taken from ITU-R BT.1848. Essential action goes in Action Safe and all graphics in Graphics Safe. — [EBU R95 publication page](https://tech.ebu.ch/publications/r095); [EBU R95 PDF](https://tech.ebu.ch/docs/r/r095.pdf)
- SMPTE (RP 2046-1 lineage) defines Safe Action as 93% of width × 93% of height of the production aperture and Safe Title as 90% × 90%. The legacy 80% × 80% safe-title area (SMPTE RP 218) is still used for CEA-708 closed captions. — [Wikipedia: Safe area (television)](https://en.wikipedia.org/wiki/Safe_area_(television)) (summarising SMPTE; secondary)
- A corporate broadcast style guide uses the same pairing: "Title Safe – 90% of 16:9 Full Frame; Action Safe – 93%". — [CNB video style guide](https://qaweb.nonprodaem.styleguide.cnb.com/visual-identity/video/safe-margins-titles.html)
- BBC caption positioning for 16:9 (via a secondary summary): keep captions within the central 90% vertically and central 75% horizontally. Captions may sit in letterbox black bars. Max line length is 68% of width for 16:9 and 90% for 4:3. — [Clevercast summary of BBC Subtitle Guidelines (updated 2023-09-06)](https://clevercast.com/bbc-subtitling-guidelines)

**Lower thirds: size and placement**
- No published broadcast standard gives lower-third text size as a % of frame height. Examples found:
  - YES TV technical spec (1920×1080 composition): lower-third "maximum creative area" 1920 × 240 px (≈22% of height) and a bottom safe space of 54 px (=5%, matching the 90% graphics-safe margin). — [YES TV advertise specs](https://yestv.com/advertise-with-yes-tv-staging)
  - Socialive suggests a full-width lower-third plate of 1920 × 225 px at 1080p, but says "there is no recommended exact size". — [Socialive support](https://support.socialive.us/support/solutions/articles/67000696654-creating-graphic-overlays-to-enhance-and-brand-sessions)
  - Northeastern University brand guide: name line size 38 in Avid/Premiere (75 in After Effects), subject/title line size 26 (47 in AE). Units depend on the app. — [Northeastern videography guide](https://brand.northeastern.edu/design-and-experiences/design/videography/)
- A blog claims caption type should be 7–10% of frame height, citing BBC/Netflix without links. This is weakly sourced. — [Blitzcut](https://blitzcutai.com/blog/how-to-make-captions-look-professional)
- Netflix sets subtitle font size "relative to video resolution", sized so 42 characters fit across the screen (Arial as placeholder, white text). — [Netflix English (USA) Timed Text Style Guide, change log to 2025-12-19](https://partnerhelp.netflixstudios.com/hc/en-us/articles/217350977-English-USA-Timed-Text-Style-Guide)

**Tracking, all-caps, font pairing**
- All-caps needs added tracking. Capitals are designed to sit next to lowercase, so caps set at default spacing look uneven. Add tracking, then kern individual pairs. Reserve all-caps for titles and short headlines. — [Pimp My Type: spacing all caps](https://pimpmytype.com/spacing-all-caps/)
- Cinematic title practice: an animated "tracking expansion" from tight to wide over a couple of seconds is a staple look. Very wide tracking can break a word into disconnected letters. — [Miracamp: cinematic titles in After Effects](https://www.miracamp.com/learn/after-effects/create-cinematic-titles)
- Genre conventions (community):
  - Serif (Trajan Pro, Cinzel) for epic, historical or drama.
  - Geometric sans (Gotham, Futura) for modern or sci-fi, often tracked out generously.
  - Script for elegant titles.
  - Bold condensed sans for thrillers and action.
  - Pairing rule: a characterful display face over a calm, legible body face, with a maximum of 2 typefaces per project. — [Miracamp](https://www.miracamp.com/learn/after-effects/create-cinematic-titles); [No Film School: tips for better titles](https://nofilmschool.com/2017/07/watch-tips-creating-better-titles-your-films-and-videos)
- No source gave a numeric tracking value for cinematic titles. A CSS example of 0.1em appeared only as a starting point (see Gaps).

**Contrast / legibility**
- WCAG 2.2 SC 1.4.3 requires a contrast ratio of at least 4.5:1 for normal text and 3:1 for large text. This is cited for video captions by a caption-readability guide. — [Kineclip caption readability checklist 2026](https://kineclip.com/blog/caption-readability-checklist-short-videos-2026/)
- Protect contrast over busy footage with a background plate/scrim, shadow or outline. — [Reap: short-form safe zones (2026-09-07)](https://reap.video/blog/short-form-video-safe-zones)

**On-screen duration (reading speed)**
- Netflix (adult): max 20 characters per second. Children's programmes: 17 cps. — [Netflix English (USA) TTSG](https://partnerhelp.netflixstudios.com/hc/en-us/articles/217350977-English-USA-Timed-Text-Style-Guide)
- Netflix event duration: minimum 5/6 s (20 frames at 24 fps), maximum 7 s. — [Netflix TTSG General Requirements (change log 2022-10-07)](https://partnerhelp.netflixstudios.com/hc/en-us/articles/215758617-Timed-Text-Style-Guide-General-Requirements)
- BBC: 160–180 words per minute (0.33–0.375 s per word). Minimum on-screen time is about 0.3 s per word (e.g. 1.2 s for a 4-word caption). — [Clevercast summary of BBC guidelines](https://clevercast.com/bbc-subtitling-guidelines)
- "Read-twice" rule (Pinnacle Studio help): a title should stay up long enough to read twice. That is about 3 s for a ~10-letter title, plus 1 s for every 5 additional letters. — [Pinnacle Studio help: Giving your project a title](https://help.pinnaclesys.com/pinnacle/v24/en/help/pinnacle-studio/h2-giving-your-project-a-title.html)
- Practitioner anecdotes: about 5 s average for names/titles, 6 s as an approximation, or "readable aloud at a normal conversational pace". — [Vegas Creative Software forum](https://www.vegascreativesoftware.info/us/forum/ot-titles-should-last-how-many-seconds--26080)
- Short branded intro cards: 2–3 s. — [Clueso glossary: Title Card](https://www.clueso.io/glossary/title-card)
- Silent-era intertitles followed a shared per-word timing that "doesn't quite fit the read-it-twice adage". — [silentfilmmusic.com: All in the Timing](https://silentfilmmusic.com/lsf24-titles-timing/)

**Kinetic typography trends 2024–2026 (trend commentary, mostly vendor blogs)**
- Kinetic type is described as the most-cited motion trend, driven partly by muted short-form viewing. — [autoae.online: motion graphics trends 2026](https://autoae.online/blog/motion-graphics-trends-2026)
- Variable fonts have moved from emerging to standard. They allow animating weight, width or slant from one file. — [Linearity: trending fonts 2025](https://www.linearity.io/blog/trending-fonts/); [InspoAI: typography trends 2026](https://www.inspoai.io/blog/typography-trends-2026)
- Other trends:
  - Expressive high-contrast serifs are returning. — [AND Academy](https://www.andacademy.com/resources/?p=23131)
  - Oversized, frame-filling and warped display type. — [autoae.online](https://autoae.online/blog/motion-graphics-trends-2026)
  - Playful kerning and contrasting weights. — [Wannathis](https://wannathis.one/blog/top-typography-trends-2026-for-designers)
  - A lo-fi, handwritten counter-trend. — [Wix typography trends](https://www.wix.com/wixel/resources/typography-trends)

### Inferences
- **Pixel safe areas at 1920×1080** (calculated from EBU R95 / SMPTE percentages):
  - Action safe: 1786 × 1004 px box, margins ≈67 px left/right and ≈38 px top/bottom.
  - Title/graphics safe: 1728 × 972 px box, margins 96 px left/right and 54 px top/bottom.
  - At 3840×2160, double the margins: action 134/76 px, title 192/108 px.
- **Default type sizes for an agent at 1080p** (unsourced working defaults; tune by eye; no official standard was found):
  - Lower-third name: cap height ≈4–5% of frame height (≈45–55 px; font size ≈60–72 px).
  - Lower-third title/role: ≈60–70% of the name size.
  - Main title card: font size ≈8–15% of frame height.
  - Burned-in captions (16:9): ≈5–7% of frame height.
  - Scale all of these linearly with frame height: ×2 at 2160p, ×1.78 for 1080×1920 vertical measured by height. Prefer sizing on the short dimension for vertical.
- **Lower-third placement at 1080p** (consistent with YES TV's 1920×240 creative area and 54 px bottom safe space): baseline of the lowest line ≥54 px above the bottom edge (title safe), plate ≤ ~225–240 px tall, left edge ≥96 px from the frame edge.
- **Duration formula for any on-screen text:**
  - duration_s = max(minimum, characters / 15–17 cps), with minimum = 2 s for short labels, ≈3 s for title cards and ≈4–5 s for lower thirds.
  - Cap captions at 7 s. Title cards can run longer for mood.
  - Netflix's 20 cps is a ceiling for trained subtitle readers. Use 15–17 cps for display text that viewers did not expect.
  - BBC's 160–180 wpm (≈2.7–3 words/s) gives an equivalent words-per-second check.
- **Cinematic tracking default:** about +100 to +300 tracking units (After Effects/Premiere units are 1/1000 em, i.e. 0.1–0.3 em) on all-caps titles. This is unsourced; verify visually so words still read as words.
- **Fades:** use about 6–12 frames (0.25–0.5 s) for in/out, and avoid hard cuts of text onto busy motion. This is unsourced common practice and needs a source (see Gaps).
- **Kinetic type:** treat it as a style option for short-form and promos. For legibility, the text must hold still and fully formed for the read time computed above; animation time does not count toward read time.

### Gaps
- No official or standards-body numbers were found for: title font size as % of frame height, tracking values for cinematic titles, fade/animation durations, credit roll (crawl) speed, or chapter-title conventions.
- End cards: YouTube end-screen rules (commonly cited as an end screen in the last 5–20 s of a video, with the video ≥25 s long) were not verified in this session.
- BBC primary guideline pages (bbc.co.uk and bbc.github.io) could not be fetched (blocked/404). BBC figures here come from a third-party summary (Clevercast, 2023), and the BBC font-size rule was not recovered.
- School of Motion, Adobe and Apple typography-for-video guides were not reached within the tool budget.

## 2. Captions/subtitles for social: line length, lines per caption, duration limits, burn-in vs sidecar, placement relative to platform UI

### Takeaway
Use Netflix TTSG as the timing backbone: 42 chars/line, 2 lines, 20 cps adult (17 children), min 20 frames (≈5/6 s), max 7 s, 2-frame gaps, and snap to shot changes. For vertical social video, cut lines to about 20–37 characters, keep 1–2 lines, and place captions in the lower-middle centre above the bottom UI band (keep the baseline at least ~450–480 px above the bottom on 1080×1920).

### Cited Findings
**Netflix Timed Text Style Guide (English USA, change log to 2025-12-19)**
- 42 characters per line, max 2 lines.
- Reading speed up to 20 cps for adult programmes and 17 cps for children's.
- Keep text on one line unless it exceeds 42 characters. Prefer a bottom-heavy pyramid when breaking.
- Break after punctuation and before conjunctions/prepositions. Never split article+noun, first+last name, or verb+auxiliary/negation.
- Source: [Netflix English (USA) TTSG](https://partnerhelp.netflixstudios.com/hc/en-us/articles/217350977-English-USA-Timed-Text-Style-Guide)

**Netflix General Requirements (change log 2022-10-07)**
- Minimum duration 5/6 s (20 frames at 24 fps), maximum 7 s per event.
- Max 2 lines, centre-justified, at top or bottom of screen.
- Move subtitles to avoid on-screen text.
- TTML must use percentages, not pixels.
- Source: [Netflix TTSG General Requirements](https://partnerhelp.netflixstudios.com/hc/en-us/articles/215758617-Timed-Text-Style-Guide-General-Requirements)

**Netflix Subtitle Timing Guidelines (change log 2025-07-04)**
- Minimum 2 frames between subtitles at any frame rate. Minimum duration 20 frames.
- Half a second = 12 frames at 24 fps, 15 at 30 fps, 30 at 60 fps.
- In-time on the first frame of audio (or within 1–2 frames).
- Lag-out: ideally ≥0.5 s after audio ends when no subtitle follows.
- Shot changes:
  - If dialogue starts within 0.5 s after a cut, snap the in-time to the cut.
  - If the out-time is within 0.5 s before a cut, extend it to the cut minus 2 frames.
  - Last resort: out-time 12 frames after the cut if there is no lingering effect.
- Chaining: gaps under 0.5 s are closed to 2 frames (at 24 fps, gaps of 3–11 frames must become 2). Gaps should be either 2 frames or ≥0.5 s.
- Source: [Netflix TTSG Subtitle Timing Guidelines](https://partnerhelp.netflixstudios.com/hc/en-us/articles/360051554394-Timed-Text-Style-Guide-Subtitle-Timing-Guidelines)

**BBC (secondary summary)**
- 160–180 wpm. Max 2 lines; 3 allowed if no important picture is obscured.
- Line length 68% of 16:9 width.
- Minimum gap: "a second and a half". This conflicts with Netflix's 2-frame chaining, and the context is likely different (time between separate captions rather than chained ones); not verified against the BBC primary source.
- Prefers system fonts (Helvetica on iOS, Roboto on Android).
- Source: [Clevercast summary of BBC guidelines](https://clevercast.com/bbc-subtitling-guidelines)
- The 37-characters/line figure is the teletext broadcast limit. BBC online sets line length as a share of picture width instead. — [Clevercast](https://clevercast.com/bbc-subtitling-guidelines)

**Vertical video**
- Nimdzi recommends 1–2 lines max with ≤37 characters per line, depending on font size. It notes 33-character subtitles have appeared in Netflix's vertical previews, and recommends edited rather than verbatim subtitles. — [Nimdzi: Subtitling vertical videos](https://www.nimdzi.com/subtitling-vertical-videos-guidelines-where-art-thou/)
- Simon Says (vendor) suggests about 20 characters per line works best for vertical video. — [Simon Says: Subtitles in vertical videos](https://www.simonsaysai.com/help/5520911-subtitles-in-vertical-videos)
- Instagram Reels captions (vendor blog):
  - Text height 60–75 px at 1080×1920 (≈3.1–3.9% of height).
  - Keep captions ≥450–480 px above the bottom edge.
  - Source: [Clipspeed: Instagram Reels captions 2026](https://www.clipspeed.ai/blog/instagram-reels-captions.html)
- Placement by platform (editorial):
  - Start lower-middle centre, away from right-side action rail, bottom metadata and extreme top.
  - TikTok: avoid the lowest quarter for essential text.
  - Reels: keep captions above the account/description area and avoid right-aligned text.
  - Shorts: keep central, away from far right and bottom.
  - Test the longest two-line caption.
  - Source: [Reap (2026-09-07)](https://reap.video/blog/short-form-video-safe-zones)

**Platform-native caption/text limits**
- TikTok ad captions are a non-customisable white font. Spark Ads captions are max 4 lines including emojis. — [TikTok Ads video specs (updated June 2026)](https://ads.tiktok.com/help/article/video-ads-specifications?lang=en)
- Instagram Reels ads: primary text 44 characters. Captions optional but recommended. — [Meta Ads Guide: Instagram Reels video](https://www.facebook.com/business/ads-guide/update/video/instagram-reels)

**Burn-in vs sidecar**
- Burned-in captions are always visible but cannot be edited after render.
- Recommended workflow: burn a stylised version for short-form feeds and upload a clean SRT for YouTube/Vimeo.
- Source: [convertaudiototext: burning subtitles](https://convertaudiototext.com/blog/burning-subtitles-into-video)

### Inferences
- **Agent caption defaults for 16:9 long-form (YouTube/Vimeo):** sidecar SRT/VTT with ≤42 chars/line, ≤2 lines, ≤17–20 cps, 0.83–7 s per event, 2-frame gaps, snapped to cuts per the Netflix rules.
- **Agent caption defaults for 9:16 social:**
  - Burn in, 1–2 lines of ≤20–32 characters (≤37 hard cap), 1–4 words per "pop" for kinetic word-by-word styles.
  - ≤15–17 cps.
  - Centre-aligned with a box/outline for ≥4.5:1 contrast.
  - Vertical position roughly 55–70% down the frame (baseline ≈1150–1400 px on 1920 height). That stays above the ≈480–672 px bottom UI band and clear of the right rail.
- **Do not double-caption:** if burning captions in, do not also upload a platform auto-caption track that renders on top. Conversely, for YouTube upload a sidecar track for accessibility and search.

### Gaps
- No official TikTok, Instagram or YouTube Shorts spec exists for organic caption size, chars/line or position. All vertical-caption numbers above are vendor or editorial.
- The BBC "1.5 s minimum gap" claim could not be checked against the primary BBC document.

## 3. Delivery specs per platform (YouTube, Instagram Reels/feed, TikTok, Facebook, X, Vimeo, LinkedIn)

### Takeaway
A single master export covers almost every platform: MP4, H.264 High Profile, progressive, constant (native) frame rate, 4:2:0, BT.709, AAC-LC 48 kHz stereo, moov atom at front (faststart), no edit lists. Then vary only resolution, aspect ratio, bitrate and duration per platform. Meta now recommends larger canvases for ads: 1440×2560 for Reels and 1440×1800 for feed 4:5.

### Cited Findings
**YouTube — "Recommended upload encoding settings" (official; no page date shown; fetched 2026-10-10)**
- Container and video:
  - MP4, no edit lists, moov atom at front (Fast Start).
  - H.264, progressive, High Profile, 2 consecutive B-frames, closed GOP of half the frame rate, CABAC, variable bitrate (no limit required), 4:2:0.
- Audio:
  - AAC-LC (or Opus / Eclipsa Audio), stereo or stereo+5.1, 48 kHz.
  - Audio bitrates: mono 128 kbps, stereo 384 kbps, 5.1 512 kbps.
- Frame rate: upload at the recorded frame rate. Common rates are 24, 25, 30, 48, 50 and 60. Deinterlace first (1080i60 → 1080p30).
- SDR video bitrates (Mbps, standard fps / high fps 48–60):
  - 8K: 80–160 / 120–240
  - 2160p: 35–45 / 53–68
  - 1440p: 16 / 24
  - 1080p: 8 / 12
  - 720p: 5 / 7.5
  - 480p: 2.5 / 4
  - 360p: 1 / 1.5
- HDR video bitrates (Mbps, standard fps / high fps):
  - 8K: 100–200 / 150–300
  - 2160p: 44–56 / 66–85
  - 1440p: 20 / 30
  - 1080p: 10 / 15
  - 720p: 6.5 / 9.5
- Colour: SDR in BT.709 (primaries, transfer and matrix). Full range is converted to limited, and BT.2020 primaries are converted to BT.709 at 8-bit. The player adapts to vertical or square video.
- Source: [YouTube Help 1722171](https://support.google.com/youtube/answer/1722171?hl=en)

**YouTube Shorts**
- Up to 3 minutes for uploads on or after 2024-10-15 (previously 60 s). This applies to square or taller aspect ratios and was announced 2024-10-03. — [Tubefilter 2024-10-03](https://www.tubefilter.com/2024/10/03/youtube-shorts-three-minutes-max-length-redesign-trends-templates/); [PetaPixel 2024-10-04](https://petapixel.com/2024/10/04/youtube-shorts-expands-video-length-to-three-minutes/) (secondary; YouTube's blog was not fetched)

**Instagram Reels — ads (Meta Ads Guide, official; footer ©2026, no spec date)**
- 9:16, recommended 1440 × 2560 px, MP4/MOV, max 4 GB, 0 s–15 min.
- Minimum width: 250 px for ads under 30 s, 500 px for 30 s and longer.
- H.264, square pixels, fixed frame rate, progressive, no edit lists.
- Audio: stereo AAC ≥128 kbps.
- Safe zone: keep the top 14%, bottom 35% and 6% on each side free of text/logos.
- Source: [Meta Ads Guide: Instagram Reels](https://www.facebook.com/business/ads-guide/update/video/instagram-reels)

**Instagram Reels — organic**
- Max length raised from 90 s to 3 min on 2025-01-18 (Adam Mosseri). The profile grid changed from square to a taller rectangle at the same time. — [Engadget](https://www.engadget.com/social-media/instagram-swoops-in-with-3-minute-reels-and-rectangular-profile-grids-as-the-tiktok-ban-gets-real-201316339.html); [Business Today 2025-01-21](https://www.businesstoday.in/technology/news/story/instagram-head-announces-big-changes-3-minute-reels-and-new-look-for-profile-grid-461527-2025-01-21)
- The exact grid ratio (3:4 vs 4:5) was not confirmed.
- 1080 × 1920 is still the widely cited organic Reels size (community). — [Hopper HQ](https://www.hopperhq.com/blog/instagram-reel-size/)

**Facebook Feed video ads (Meta Ads Guide, official; footer ©2026)**
- Recommended 4:5 at 1440 × 1800 px, minimum 120 × 120 px.
- MP4/MOV/GIF, max 4 GB, duration 1 s–241 min.
- H.264, square pixels, progressive, fixed frame rate, no edit lists.
- Audio: stereo AAC ≥128 kbps.
- Primary text 50–150 characters, headline 27 characters.
- Source: [Meta Ads Guide: Facebook Feed video](https://www.facebook.com/business/ads-guide/update/video/facebook-feed)

**TikTok — ads (official, updated June 2026)**
- Minimum resolutions: 9:16 at ≥540 × 960 (recommended format), 16:9 at ≥960 × 540, 1:1 at ≥640 × 640.
- Formats .mp4/.mov/.mpeg/.3gp/.avi, max 500 MB, up to 10 min, minimum bitrate 516 kbps.
- Spark Ads: .mp4/.mov with no duration restriction.
- Safe zones are supplied as downloadable templates with no pixel numbers in the text. Safe-zone size depends on aspect ratio, caption length and ad formats.
- Source: [TikTok Ads video specs](https://ads.tiktok.com/help/article/video-ads-specifications?lang=en)

**TikTok — organic (community; TikTok help page not reached)**
- Upload up to 60 min; in-app recording up to 10 min. — [Metricool](https://metricool.com/tiktok-video-length/)
- File size claims conflict:
  - 72 MB Android / 287.6 MB iOS / 500 MB web — [Stack Influence](https://stackinfluence.com/blog/tiktok-video-sizes-the-ultimate-guide)
  - Up to 30 GB — [Sociality](https://sociality.io/blog/tiktok-video-length/)
  - 500 MB max — [postfa.st](https://postfa.st/sizes/tiktok/video)
- TikTok compresses uploads to 1080p (community). — [Stack Influence](https://stackinfluence.com/blog/tiktok-video-sizes-the-ultimate-guide)

**X / Twitter (community; help.x.com returned 403)**
- Standard accounts: 140 s max, 512 MB, max dimensions 1920 × 1920. — [Emplifi API notes on X media upload](https://docs.emplifi.io/platform/latest/home/x-formerly-twitter-media-upload-v1-1-api-endpoints)
- Recommended size: 1280 × 720 landscape / 720 × 1280 vertical / 720 × 720 square, at 30 fps (60 supported). — [postfa.st X video specs](https://postfa.st/sizes/x/video)
- Premium limits conflict:
  - Premium users: 1080p, max ~8 GB, ~3 h; 4K uploads rolling out to some creators in April 2025. — [AOL/Engadget report](https://www.aol.com/x-bringing-4k-video-uploads-120044995.html)
  - Premium Plus: 4 h at 1080p, 16 GB (2–4 h videos at 720p). — [Adaptly 2026 guide](https://adaptlypost.com/blog/uploading-videos-to-twitter-complete-walkthrough)

**Vimeo (official help page; ©2025, no article date)**
- Codecs: H.264 High Profile (up to 4K), ProRes 422 HQ, or H.265 (up to 8K).
- Frame rate: native, constant (not variable). Footage over 60 fps is reduced. Common rates: 23.98, 24, 25, 29.97, 30, 50, 59.94, 60.
- Variable bitrate ranges (Mbps):
  - SD: 2–5
  - 720p: 5–10
  - 1080p: 10–20
  - 2K: 20–30
  - 4K: 30–60
  - 8K: 50–80
- Other video: CRF ≤18, square pixels, progressive.
- Colour/HDR: BT.709 or BT.2020. HDR needs PQ or HLG, 10-bit or higher, with SMPTE 2086 and CEA 861.3 metadata for PQ.
- Audio: AAC-LC, 320 kbps CBR suggested, 48 kHz.
- Source: [Vimeo compression guidelines](https://help.vimeo.com/hc/en-us/articles/12426043233169-Video-and-audio-compression-guidelines)

**LinkedIn (community; official help not reached)**
- Organic: MP4, 3 s to 15 min (desktop) or 10 min (mobile), up to 5 GB, aspect ratio 1:2.4 to 2.4:1, resolution 256 × 144 to 4096 × 2304, 10–60 fps.
- Ads: 3 s–30 min, 200 MB (one source says 500 MB). Size ranges:
  - 16:9: 640 × 360 to 1920 × 1080
  - 1:1: 360 × 360 to 1920 × 1920
  - 9:16: 360 × 640 to 1080 × 1920
- Sources: [HubSpot](https://blog.hubspot.com/sales/linkedin-video-specs); [Captions.ai 2025-07-30](https://www.captions.ai/blog-post/linkedin-video-specs); [Shootsta 2026](https://shootsta.com/blog/linkedin-video-ad-specs-and-formats-2026)

### Inferences
- **Universal master export (meets YouTube, Vimeo, Meta and TikTok):** MP4, H.264 High@L4.2 (1080p) or L5.1/5.2 (4K), progressive, CFR at native fps, 4:2:0 8-bit BT.709 limited range, AAC-LC 48 kHz stereo, `-movflags +faststart`, no edit lists.
- **Example ffmpeg export:** `-c:v libx264 -profile:v high -pix_fmt yuv420p -preset slow -crf 16-18 -g <fps/2> -bf 2 -c:a aac -b:a 320k -ar 48000 -movflags +faststart`. For bitrate targeting, use YouTube's 8/12 Mbps (1080p), 35–45/53–68 Mbps (4K) as floors and Vimeo's 10–20 Mbps (1080p) as the upper target.
- **Per-platform presets:**
  - YouTube: 16:9 3840×2160 or 1920×1080. Uploading 4K even for 1080p content gets VP9/AV1 processing (YouTube notes 4K plays only on VP9-capable clients).
  - YouTube Shorts: 1080×1920, ≤3:00.
  - Instagram/Facebook Reels: 1080×1920 organic; 1440×2560 for ads; ≤3:00 organic / ≤15:00 ads.
  - Instagram/Facebook feed: 4:5 at 1080×1350 (organic) or 1440×1800 (ads).
  - TikTok: 1080×1920, ≤10 min safest (60 min upload exists), ≤500 MB for ads.
  - X: 1920×1080 or 1080×1920, ≤2:20 and ≤512 MB for non-Premium.
  - LinkedIn: 1920×1080 or 1080×1920, ≤15 min / ≤5 GB organic, ≤200 MB ads.
  - Vimeo: 1080p at 10–20 Mbps or 4K at 30–60 Mbps, or ProRes 422 HQ.
- **Bitrate headroom:** for 1080×1920 vertical, use the 1080p row (8–12 Mbps minimum, up to 15–20 Mbps), since pixel count equals 1080p.

### Gaps
- Official X, LinkedIn and organic TikTok help pages could not be fetched (403 or not reached). Their numbers are community figures and conflict in places.
- The Facebook Reels ads page was not fetched separately; Meta generally mirrors the Instagram Reels spec (1440×2560).
- Official organic Instagram resolution/bitrate guidance was not found. Meta publishes ad specs only.
- YouTube's official Shorts announcement blog and the Instagram grid's exact ratio were not verified from primary sources.

## 4. Vertical video safe zones (TikTok, Reels, Shorts at 1080×1920)

### Takeaway
Only Meta publishes numeric safe zones: Reels ads keep the top 14%, bottom 35% and 6% each side clear. At 1080×1920 that is top 269 px, bottom 672 px and sides 65 px, leaving a ≈950 × 979 px safe box. TikTok and YouTube publish templates or ad previews, not text numbers. Community measurements vary widely. The conservative cross-platform rule is: keep essential text in a centred box from about y=290 to y=1250 and x=110 to x=930 (right side 150+ px clear).

### Cited Findings
- **Meta Reels ads:** keep top 14%, bottom 35% and 6% each side free of text/logos. — [Meta Ads Guide: Instagram Reels](https://www.facebook.com/business/ads-guide/update/video/instagram-reels)
- **TikTok ads:** safe zone varies with aspect ratio, caption length and ad formats. TikTok supplies downloadable safe-zone files (LTR, RTL, with anchors) but no pixel figures in text. — [TikTok Ads video specs (June 2026)](https://ads.tiktok.com/help/article/video-ads-specifications?lang=en)
- **TikTok community measurements at 1080×1920 (conflicting):**
  - Postiz: ≈90 px top / 330 px bottom / 65 px sides.
  - Adaptly: 150 top / 270 bottom / 40 sides.
  - Moda: top 110–270 px depending on app, bottom up to 480 px, about 130 top / 480 bottom / 150 right.
  - Sources: [Postiz](https://postiz.com/blog/tiktok-video-size-ratio); [Adaptly checker](https://adaptlypost.com/en/free-tools/safe-zone-checker); [Moda story safe-zone checker](https://moda.app/tools/story-safe-zone-checker)
- **YouTube Shorts community measurements (conflicting):**
  - Adkit (measured from official ad previews, March 2026): top 241 px, bottom 381 px, right 201 px, left 60 px. — [Adkit](https://adkit.so/tools/safe-zones/youtube)
  - Poster.ly: top/bottom 380 px, left 60, right 120, leaving a central safe area of 900 × 1160 px. — [Poster.ly Shorts checker](https://www.poster.ly/tools/youtube-shorts-safe-zone-checker)
  - AI Carousels: top 288, bottom 672, left 48, right 192. — [AI Carousels](https://www.aicarousels.com/free-tools/youtube-safe-zone-checker)
- **Instagram Reels organic community figures:** a 1080 × 1420 centred zone with the bottom ≈250 px clear, or an 880 × 1420 area. — [Hopper HQ](https://www.hopperhq.com/blog/instagram-reel-size/); [Fliki](https://fliki.ai/blog/instagram-reel-dimensions-and-size-guide)
- **Cross-platform editorial margins:** top ≈15% (≈288 px), sides 10–15% (108–162 px), bottom 25–35% (480–672 px). Described as "working margins, not official universal specifications". — [Reap (2026-09-07)](https://reap.video/blog/short-form-video-safe-zones)
- **Adaptly cross-platform zone:** 900 × 1400 px centred. — [Adaptly 2026 safe zones](https://adaptlypost.com/blog/social-media-safe-zones-2026-complete-guide)

### Inferences
- **One safe box at 1080×1920 for TikTok, Reels and Shorts** (union of the conservative figures above):
  - Top margin ≥270–290 px (Meta's 14% = 269 px; YouTube 241–288 px).
  - Bottom margin ≥672 px for ads/CTAs (Meta 35%). About 480 px is the minimum for organic captions.
  - Right margin ≥160–200 px (YouTube's right rail of 201 px is the widest).
  - Left margin ≥65–110 px.
  - Resulting box ≈ x 110–880, y 290–1248 for hard-safe essentials (logos, CTAs, key text). Organic captions can extend down to y ≈1440 (480 px bottom margin).
- **Scale for 1440×2560 ad canvases:** multiply by 1.333. Meta's numbers at that size are top 358, bottom 896 and sides 86 px.
- Faces and focal action should sit in the upper-middle third (about y 400–1100) so they are clear of both the top header and the bottom caption/UI band.

### Gaps
- No official numeric organic safe zones exist for TikTok, Instagram or YouTube Shorts. All organic figures are community measurements that change with app UI updates. The agent should treat them as configurable presets.

## 5. Aspect ratios, letterboxing and reframing 16:9 ↔ 9:16

### Takeaway
Letterbox bars are simple arithmetic. At 1920×1080 the bars are: 2.39:1 → 138 px each (active 1920×804); 2.35:1 → ≈131 px; 2.40:1 → 140 px; 2.00:1 → 60 px; 1.85:1 → ≈21 px. A 4:3 pillarbox → 240 px each side. For vertical deliverables, shoot or master at 4K: a full-height 9:16 crop from UHD is 1215×2160, which stays above 1080×1920 without upscaling.

### Cited Findings
- Platform aspect-ratio support (official):
  - YouTube's standard is 16:9; the player adapts to vertical and square video. — [YouTube Help 1722171](https://support.google.com/youtube/answer/1722171?hl=en)
  - Shorts classification needs square or taller. — [Tubefilter](https://www.tubefilter.com/2024/10/03/youtube-shorts-three-minutes-max-length-redesign-trends-templates/)
  - Meta recommends 9:16 for Reels and 4:5 for Facebook Feed. — [Meta Reels](https://www.facebook.com/business/ads-guide/update/video/instagram-reels); [Meta FB Feed](https://www.facebook.com/business/ads-guide/update/video/facebook-feed)
  - TikTok accepts 9:16 (recommended), 16:9 and 1:1. — [TikTok Ads specs](https://ads.tiktok.com/help/article/video-ads-specifications?lang=en)
  - LinkedIn accepts 1:2.4 to 2.4:1 (community). — [HubSpot](https://blog.hubspot.com/sales/linkedin-video-specs)
- Instagram moved its profile grid from square to a taller rectangle in January 2025, so square crops of vertical posts are reduced. — [Engadget](https://www.engadget.com/social-media/instagram-swoops-in-with-3-minute-reels-and-rectangular-profile-grids-as-the-tiktok-ban-gets-real-201316339.html)
- EBU R95 asks that the image centre remain fixed through production unless there is a creative reason to change it. This is relevant to centre-cut reframing. — [EBU R95](https://tech.ebu.ch/publications/r095)
- BBC allows captions to sit within letterbox black bars. — [Clevercast summary of BBC](https://clevercast.com/bbc-subtitling-guidelines)

### Inferences
**Bar and crop arithmetic** (calculated: active height = width ÷ ratio; bar = (frame height − active height) ÷ 2)

| Target ratio | In 1920×1080 | In 3840×2160 | Feel / typical use (craft consensus, unsourced) |
|---|---|---|---|
| 2.39:1 (scope, modern DCI) | active 1920×803–804, bars ≈138 px | active 3840×1607, bars ≈277 px | Epic, widescreen cinema, landscapes, two-shots |
| 2.35:1 (legacy scope) | active 1920×817, bars ≈131–132 px | bars ≈263 px | Same as above (older label) |
| 2.40:1 | active 1920×800, bars 140 px | bars 280 px | Common NLE "cinemascope" preset |
| 2.00:1 (Univisium) | active 1920×960, bars 60 px | bars 120 px | Streaming-drama look |
| 1.85:1 (flat) | active 1920×1038, bars ≈21 px | bars ≈42 px | Theatrical flat, subtle cinematic |
| 16:9 (1.78) | full frame | full frame | TV/web default |
| 4:3 (1.33) pillarbox | active 1440×1080, side bars 240 px | 2880×2160, sides 480 | Archival, retro, intimate, boxy |
| 1:1 in 16:9 | 1080×1080, sides 420 px | – | Social square |
| 4:5 | crop 864×1080 from 1080p → scale 1.25× to 1080×1350 | crop 1728×2160 → downscale | Mobile feed, maximum feed real estate |
| 9:16 | crop 607.5×1080 → upscale 1.78× (soft) | crop 1215×2160 → downscale to 1080×1920 (sharp) | Shorts, Reels, TikTok, full-screen mobile |

- **Reframing 16:9 → 9:16:** the crop keeps only ≈31.6% of the horizontal frame width. Track the subject (speaker face or action), avoid centre-locking, and keep the subject's eyes about one-third from the top (y ≈ 640 px of 1920). The subject must stay inside the vertical safe box from Q4.
- For 2.39:1 letterboxed masters going to 9:16, crop from the active picture only. Do not include the bars.
- Titles in letterboxed pieces: keep them inside the active picture (or deliberately inside the bar for a stylised subtitle look, which BBC permits). Never straddle the bar edge.

### Gaps
- No source fetched in this session gives the "emotional feel" of each aspect ratio. The feel column is craft consensus and needs a citation if precision matters.
- No published platform guidance on auto-reframe best practice was retrieved.

## 6. Frame rate choices: 23.976 vs 24 vs 25 vs 29.97 vs 50/59.94

### Takeaway
Finish at 23.976 for a film look on web/streaming in NTSC-heritage markets, 24.000 for theatrical DCP, 25 for 50 Hz (PAL) regions and broadcasts, 29.97 for US/JP broadcast, news and unscripted, and 50/59.94 for sports, gaming and high-motion content. Platforms want the native frame rate at constant frame rate (CFR); never convert just to suit a platform.

### Cited Findings
- **Platform rules:**
  - YouTube: upload at the recorded frame rate. Common rates are 24, 25, 30, 48, 50 and 60; deinterlace interlaced sources (1080i60 → 1080p30). — [YouTube Help 1722171](https://support.google.com/youtube/answer/1722171?hl=en)
  - Vimeo: use the native, constant frame rate. Footage over 60 fps is reduced. Common rates are 23.98, 24, 25, 29.97, 30, 50, 59.94 and 60. — [Vimeo compression guidelines](https://help.vimeo.com/hc/en-us/articles/12426043233169-Video-and-audio-compression-guidelines)
  - Meta: fixed frame rate required. — [Meta Ads Guide](https://www.facebook.com/business/ads-guide/update/video/instagram-reels)
  - LinkedIn: 10–60 fps, 30 recommended (community). — [HubSpot](https://blog.hubspot.com/sales/linkedin-video-specs)
- **Rate meanings:**
  - 23.976 is 24 fps slowed by 1000/1001 for NTSC compatibility. True 24 is for theatrical DCP.
  - For streaming film-look work, 23.976 is usually the safe choice.
  - 25 is for 50 Hz regions. 29.97 suits US/Japan broadcast, news, sports and unscripted, and reads as a "TV news" look.
  - 59.94 and 50 are the NTSC and PAL high frame rates for sports/HFR. Shoot 50/60 and conform to 23.976/24 for slow motion.
  - Sources: [The Post Flow frame rate cheat sheet](https://thepostflow.com/filmmaker-resources/frame-rate-cheat-sheet/); [RedShark News](https://redsharknews.com/production/item/5606-how-on-earth-do-you-choose-which-frame-rate-to-shoot-in)
- **PAL-region shooting:** features in 50 Hz regions are often shot at 24 fps with a 172.8° shutter (1/50 s) to avoid flicker from mains-powered lights. A 25p → 24/23.976 conversion is a slowdown that shifts audio pitch unless corrected. — [Pro Video Coalition: When 25p beats 24p](https://www.provideocoalition.com/when-25p-beats-24p3/); [The Post Flow](https://thepostflow.com/filmmaker-resources/frame-rate-cheat-sheet/)

### Inferences
- **Agent rule:** the timeline fps equals the dominant source fps. Export at the timeline fps as CFR. Never re-time 25 ↔ 23.976 for a platform; YouTube and Vimeo accept both.
- **Mixed sources:** conform high-fps clips (50/59.94/120) as slow motion into a 23.976/25 timeline. Frame-blend or optical-flow only as a last resort.
- **Title/caption timing must be in frames of the delivery fps:** Netflix's half-second is 12 frames at 24 fps, 15 at 30 and 30 at 60. Fades of 6–12 frames at 24 fps equal 7.5–15 frames at 29.97 (round to the nearest frame).
- **GOP:** YouTube's closed GOP of half the frame rate means keyframe interval 12 frames at 23.976/24, 13 at 25 (12.5 rounded), 15 at 29.97/30 and 30 at 59.94/60.

### Gaps
- Frame-rate "look" claims (e.g. 29.97 = "TV news" look) come from practitioner blogs, not standards bodies.
- No official TikTok or Instagram frame-rate recommendation was found beyond Meta's "fixed frame rate".
