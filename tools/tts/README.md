# Local text-to-speech (offline, no account)

| Engine | Env | Licence | Notes |
|---|---|---|---|
| **Kokoro** v1.0 (82M) | `.venv` (Python 3.13) | Apache 2.0 | top-rated open model; 54 preset voices; fast on CPU |
| **Piper** (piper1-gpl) | `.venv` | engine GPL-3.0-or-later; each voice model has its own licence (see its model card) | very fast, a bit flatter; 4 voices in `models/piper`. Not bundled in this repo — installed separately by `setup.sh --tts` |
| **Chatterbox** | `.venv-chatterbox` (Python 3.11, CUDA torch) | MIT | most natural; clones a voice from ~10 s of clean audio; output carries an inaudible watermark |

```
tools/tts/.venv/Scripts/python.exe tools/tts/say.py list
tools/tts/.venv/Scripts/python.exe tools/tts/say.py kokoro af_heart "Hello there" out.wav --speed 1.0
tools/tts/.venv/Scripts/python.exe tools/tts/say.py piper en_US-ryan-high @script.txt out.wav
tools/tts/.venv-chatterbox/python.exe tools/tts/clone.py "Hello there" out.wav [--ref my-voice.wav]
```
Install: `sh setup.sh --tts` sets up Kokoro + Piper. Chatterbox (NVIDIA GPU, conda):
```
conda create -y -p tools/tts/.venv-chatterbox python=3.11
tools/tts/.venv-chatterbox/python.exe -m pip install torch==2.6.0 torchaudio==2.6.0 --index-url https://download.pytorch.org/whl/cu124
tools/tts/.venv-chatterbox/python.exe -m pip install chatterbox-tts
```
Samples of each voice: `tools/tts/samples/`. Only clone a voice with that person's permission.
Narration workflow: one script line per sentence → render → check pronunciation of names/local words (respell
phonetically if needed) → place in FilmCraft under the screen recording.
