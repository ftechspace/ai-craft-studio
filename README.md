# ai-craft-studio — a creative studio of AI agents on the ArtCraft apps

**Give it your footage and photos; get back a finished film, its music, titles, thumbnails and posters —
made by a team of AI agents that drive real, open-source creative apps while you watch.**

This repository is a **content-creation workflow** built on top of the
[ArtCraft](https://github.com/storytold) apps, a family of open-source creative tools. It adds the structure that
turns those apps into a studio: [Claude Code](https://claude.com/claude-code) agents with a specialty each, skills that
carry craft and taste, tested operating manuals for every app, small tools, and a project layout that lets one app's
output become the next app's input.

> **Credit where it's due.** All the creative software here — the editor, the DAW, the compositor, the vector,
> photo, raw, layout and interface-design apps — is the work of the **ArtCraft Team**. This project doesn't contain or fork their apps;
> it pulls them in as git submodules and builds a workflow around them. See [Acknowledgements](#acknowledgements).

---

## What it can do

- **Edit films and vlogs** from raw footage: it watches the footage (contact sheets, dense frame sampling, scene
  detection, audio levels), finds the story, plans the cut, builds it **live in the editor** chapter by chapter,
  verifies every cut, grades it and mixes it. Nothing is exported until you approve.
- **Make the pieces around a film**: logo and title lettering, animated intros and lower thirds, developed stills,
  thumbnails, posters, printed storyboards, save-the-dates — each by the agent and app made for it.
- **Score and sound-design** with the DAW, including cinematic cues built from the footage's own sounds.
- **Narrate** app tutorials or explainers with local, offline voices (optional).
- **Learn a creator's taste**: study reference videos they love and turn them into a house style every agent follows,
  with a critic that rejects work that doesn't fit.

## How it works

```
                      ┌──────────── producer (plans, storyboards, dispatches, checks) ────────────┐
                      │                                                                            │
  brief + storyboard  ▼                                                                            ▼
  projects/<name>/ ── wave 1 ───────────────────────────── wave 2 ─────────────────────── wave 3 ── creative-critic
                      graphic-designer  → VectorCraft      motion-designer → EffectCraft  film-editor / content-editor
                      photo-grader      → LightCraft       photo-artist    → PhotoCraft   → FilmCraft (the edit)
                      sound-designer    → SoundCraft       layout-designer → DesignCraft
                                                         ui-designer     → FigCraft
```

1. **Projects are folders** (`projects/<name>/`): `brief.md`, `storyboard.md`, a `handoff.md` log every agent appends
   to, and one subfolder per app (`graphics/`, `stills/`, `art/`, `motion/`, `audio/`, `print/`, `edit/`). Files are
   the interface between apps. See [projects/README.md](projects/README.md).
2. **Agents** (`.claude/agents/`) each own one craft and one app, and follow the skills.
3. **Skills** (`.claude/skills/`) carry the craft:
   - `creative-direction` — how to have an idea before building (truth → five concepts → kill the obvious → one
     signature device → plant and pay off), with playbooks for edit, graphics, thumbnails, music and photos;
   - `creative-review` — the critic's rubric (hook, idea, surprise, emotion, specificity, coherence, fit, craft);
   - `taste-profile` — the creator's taste (see [Your taste profile](#your-taste-profile));
   - `vlog-editing`, `vlog-techniques`, `youtube-editing` — vlog and platform editing workflows and toolboxes.
4. **Operating manuals** (`editor-kb/<app>-operations.md`) — every command, parameter, verification method and
   pitfall the agents rely on, tested against the real apps.
5. **Tools** (`tools/`) — a shared control-channel client for all apps (`craft.js`), FilmCraft helpers (`fc.js`,
   `cut.js` builds a whole cut from a JSON plan), an audio meter so agents can "hear" by measurement (`wavlevels.js`),
   the app build script, and the local voice tools (`tools/tts/`).
6. **MCP** — `.mcp.json` connects Claude Code to every app (headless engines, plus FilmCraft's live window).

### The agents

| Agent | App | Makes |
|---|---|---|
| `producer` | all | brief, storyboard, dispatches the specialists, checks everything fits |
| `film-editor` | FilmCraft | story-led films: cut, grade, sound, titles, export |
| `content-editor` | FilmCraft | YouTube long-form, vlogs, Shorts/TikTok/Reels, cutting long videos into clips |
| `sound-designer` | SoundCraft | music cues, sound design, mixes, sound plans |
| `motion-designer` | EffectCraft | logo reveals, animated titles, lower thirds, end cards |
| `graphic-designer` | VectorCraft | logos, monograms, wordmarks, lettering, icons |
| `photo-grader` | LightCraft | culling, developing and grading stills; frame grabs from video |
| `photo-artist` | PhotoCraft | thumbnails, composites, retouching, covers |
| `layout-designer` | DesignCraft | posters, save-the-dates, printed storyboards, press kits |
| `ui-designer` | FigCraft | thumbnail and social templates, carousels, channel art, app screens and clickable prototypes |
| `creative-critic` | all | reviews every piece before you see it — PASS or REVISE with concrete notes |

## Setup

**Requirements:** Windows 10/11 (the workflow was built and tested on Windows; the apps also build on macOS/Linux),
[Git](https://git-scm.com/), [Rust](https://rustup.rs/), [Node.js](https://nodejs.org/) 20+,
[Claude Code](https://claude.com/claude-code). A GPU helps (FilmCraft and the optional voice cloning use it).

```sh
git clone --recursive https://github.com/ftechspace/ai-craft-studio.git
cd ai-craft-studio
sh setup.sh            # fetches the 8 apps, applies the FilmCraft patch, builds everything (~45 min)
sh setup.sh --tts      # optional: also installs the local voice engines
```

Then open the folder in Claude Code (VS Code extension or CLI). The MCP servers in `.mcp.json` start automatically.
Launch FilmCraft with its control channel so you can watch the agents edit: `start-filmcraft.cmd`, or any app with
`node tools/craft.js <app> --start`.

**Updating the apps:** `git submodule update --remote` (or `git pull` inside an app), re-apply the FilmCraft patch if
needed, then `sh tools/build-apps.sh`. Big upstream changes can rename commands — the manuals in `editor-kb/` record
what was tested.

## Using it

Talk to Claude Code in plain language:

- *"New project `beach-day`: footage is in D:\footage\beach, a vlog, keep all the nice moments."*
  → the producer inventories the footage, writes the brief and storyboard, the critic reviews it, you approve,
  then the specialists build and the editor cuts it live.
- *"beach-day: make the music quieter under the talking."* → picks up from the project's `handoff.md`.
- *"Here are three YouTube videos I love: …"* → the agents study them (`references/STUDY-BRIEF.md`) and update the
  taste profile.
- *"Make a save-the-date from the photos in D:\photos\engagement, wine and gold, several options."*

Nothing is exported to `exports/` until you approve, and every revision is a new version — nothing is overwritten.

## Your taste profile

The agents are only as good as their sense of *your* taste. `.claude/skills/taste-profile/profile.example.md` is a
worked example (an intimate, real-life vlog style distilled from 26 reference videos). Copy it to `profile.md` —
which is git-ignored, so your taste stays yours — and let the agents keep it up to date as you react to their work.

## What's in this repo (and what isn't)

| In the repo | Not in the repo (git-ignored) |
|---|---|
| agents, skills, manuals, tools, patch, setup, docs | your `projects/`, `output/`, media and exports |
| `apps/` as **submodules** pointing at ArtCraft's repos | the apps' build output |
| `references/STUDY-BRIEF.md` (the method) | downloaded reference videos and analyses (other people's work) |
| `taste-profile/profile.example.md` | your personal `profile.md` |
| `tools/tts/*.py` | voice engines, models and samples (~4 GB, installed by `setup.sh --tts`) |

`patches/filmcraft-studio.patch` adds two small things to FilmCraft that the agents use: a `contact` example
(contact sheets, dense frame sampling, full-resolution frame grabs with luma/RGB levels — the agents' "eyes") and an
`autoedit` command (a Claude API auto-edit experiment).

## Known limits

- The agents **see** by frames and **hear** by measurement only — a human should always listen to the mix.
- SoundCraft's instruments are synthesizers; for natural-sounding music, use tracks you've licensed or the
  footage's own sounds.
- The apps are young and move fast; after big updates, re-check the manuals.
- Some sites (e.g. YouTube) rate-limit downloads of reference videos. Study references for learning only — never
  reuse their footage or music.

## Acknowledgements

This project stands entirely on the shoulders of the **ArtCraft Team** and the contributors to their open-source
apps. Thank you for building professional creative software in the open — this workflow is only possible because
every one of your apps exposes its features as commands that an agent can drive:

| App | Repository | What it is |
|---|---|---|
| **FilmCraft** | [storytold/filmcraft](https://github.com/storytold/filmcraft) | non-linear video editor |
| **SoundCraft** | [storytold/soundcraft](https://github.com/storytold/soundcraft) | digital audio workstation |
| **EffectCraft** | [storytold/effectcraft](https://github.com/storytold/effectcraft) | motion graphics and compositing |
| **VectorCraft** | [storytold/vectorcraft](https://github.com/storytold/vectorcraft) | vector illustration |
| **PhotoCraft** | [storytold/photocraft](https://github.com/storytold/photocraft) | image editing and compositing |
| **LightCraft** | [storytold/lightcraft](https://github.com/storytold/lightcraft) | photo library and raw developer |
| **DesignCraft** | [storytold/designcraft](https://github.com/storytold/designcraft) | page layout and publishing |
| **FigCraft** | [storytold/figcraft](https://github.com/storytold/figcraft) | interface design and prototyping |

Find out more at [getartcraft.com](https://getartcraft.com/). The apps keep their own licences (see each app's
LICENSE files). "ArtCraft" and the app names are trademarks of the ArtCraft Team; **this project is independent and
not affiliated with or endorsed by them.**

Also thanks to the creators of the optional local voice engines —
[Kokoro](https://github.com/thewh1teagle/kokoro-onnx), [Piper](https://github.com/OHF-Voice/piper1-gpl) (GPL-3.0) and
[Chatterbox](https://github.com/resemble-ai/chatterbox) — used under their own licences, and to
[Anthropic](https://www.anthropic.com/) for Claude Code, which runs the agents.

## License

The workflow in this repository (agents, skills, manuals, tools, docs) is licensed under the
[Apache License 2.0](LICENSE). See [NOTICE](NOTICE). The apps in `apps/` are under their own licences.
