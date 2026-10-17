# How to study a reference video (for agents)

Workspace `C:\CodeHouse\AIFilmEditor\`. Study only — never reuse any footage or music.
1. Download (no ffmpeg here, so picture and audio separately; 480p is enough):
   `cd references && py -m yt_dlp -q --no-warnings -f "135/134/136" --write-info-json -o "%(id)s.video.%(ext)s" https://youtu.be/<id>`
   `py -m yt_dlp -q --no-warnings -f "140/bestaudio[ext=m4a]" -o "%(id)s.audio.%(ext)s" https://youtu.be/<id>`
   Read the info.json (title, channel, views, description, chapters, tags).
   If YouTube asks "Sign in to confirm you're not a bot": retry with `--load-info-json <id>.video.info.json` instead
   of the URL (uses the already-fetched format list); otherwise fall back to the storyboard frames. Never use cookies
   without the user's OK.
2. Look: `apps/filmcraft/target/release/examples/contact.exe` (see `editor-kb/filmcraft-operations.md`) — a whole-video
   survey (≈ 1 frame / 10–15 s) into `references/sheets-<id>/`, plus 0.5 s `range` sheets for the first 30 s, the last
   30 s and 1–2 standout moments. Actually look at every sheet.
3. Cuts: headless FilmCraft `clip.sceneEditDetection` (`tools/fc.js` connectHeadless) → shot count, mean/median shot,
   distribution (<2 s, 2–4, 4–8, >8 s), pacing changes. Note the detector misses dark/jump cuts.
4. Sound (you can't hear): level curve per 1–10 s (convert audio to WAV via FilmCraft or `soundcraft-cli`, then
   `node tools/wavlevels.js`): music vs speech vs ambient, music share, where music drops out, ducking depth.
5. Write per video (≤ 40 lines): what it is · structure (open / chapters / end) · pacing numbers · camera · transitions ·
   text style · grade (levels numbers) · sound · what creates the feeling · the one thing to steal (structure, not
   surface) · anything that CONTRADICTS the current house style in `.claude/skills/taste-profile/SKILL.md`.
Subagents can't write report .md files here: return the analyses as text (sheets/JSON files are fine to write).
