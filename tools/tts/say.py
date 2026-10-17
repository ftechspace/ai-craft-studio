"""Text-to-speech for the studio (local, offline).

  tools/tts/.venv/Scripts/python.exe tools/tts/say.py <engine> <voice> "<text or @file.txt>" out.wav [--speed 1.0]

engines:
  kokoro   voices e.g. af_heart, af_bella, af_nicole, am_michael, am_fenrir, bf_emma, bm_george (models/kokoro)
  piper    voices = model names in models/piper, e.g. en_US-ryan-high, en_GB-alan-medium
  list     print available voices
Chatterbox (voice cloning) lives in its own env: see tools/tts/README.md.
"""
import sys, wave
from pathlib import Path

HERE = Path(__file__).parent
MODELS = HERE / "models"


def text_arg(t):
    return Path(t[1:]).read_text(encoding="utf-8") if t.startswith("@") else t


def kokoro(voice, text, out, speed):
    import soundfile as sf
    from kokoro_onnx import Kokoro
    k = Kokoro(str(MODELS / "kokoro/kokoro-v1.0.onnx"), str(MODELS / "kokoro/voices-v1.0.bin"))
    lang = "en-gb" if voice[:1] == "b" else "en-us"
    samples, sr = k.create(text, voice=voice, speed=speed, lang=lang)
    sf.write(out, samples, sr)


def piper(voice, text, out, speed):
    from piper import PiperVoice, SynthesisConfig
    v = PiperVoice.load(str(MODELS / f"piper/{voice}.onnx"))
    with wave.open(out, "wb") as wf:
        v.synthesize_wav(text, wf, syn_config=SynthesisConfig(length_scale=1.0 / speed))


def list_voices():
    from kokoro_onnx import Kokoro
    k = Kokoro(str(MODELS / "kokoro/kokoro-v1.0.onnx"), str(MODELS / "kokoro/voices-v1.0.bin"))
    print("kokoro:", ", ".join(sorted(k.get_voices())))
    print("piper:", ", ".join(p.stem for p in sorted((MODELS / "piper").glob("*.onnx"))))


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or a[0] == "list":
        list_voices()
        sys.exit()
    engine, voice, text, out = a[:4]
    speed = float(a[a.index("--speed") + 1]) if "--speed" in a else 1.0
    {"kokoro": kokoro, "piper": piper}[engine](voice, text_arg(text), out, speed)
    print(out)
