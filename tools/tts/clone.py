"""Chatterbox TTS (GPU): natural narration, optionally in a cloned voice.

  tools/tts/.venv-chatterbox/python.exe tools/tts/clone.py "<text or @file.txt>" out.wav [--ref voice.wav]
      [--exaggeration 0.5] [--cfg 0.5]

--ref: ~10 s of clean speech from the person whose voice to use (with their permission). Without it, the default voice.
"""
import sys
from pathlib import Path

import torch
import torchaudio
from chatterbox.tts import ChatterboxTTS


def opt(name, default):
    a = sys.argv
    return a[a.index(name) + 1] if name in a else default


text, out = sys.argv[1], sys.argv[2]
if text.startswith("@"):
    text = Path(text[1:]).read_text(encoding="utf-8")
model = ChatterboxTTS.from_pretrained(device="cuda" if torch.cuda.is_available() else "cpu")
wav = model.generate(text, audio_prompt_path=opt("--ref", None),
                     exaggeration=float(opt("--exaggeration", 0.5)), cfg_weight=float(opt("--cfg", 0.5)))
torchaudio.save(out, wav, model.sr)
print(out)
