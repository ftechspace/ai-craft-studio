#!/bin/sh
# One-time setup: fetch the seven ArtCraft apps (submodules), apply the FilmCraft patch, build everything.
#   sh setup.sh            apps + build
#   sh setup.sh --tts      also install the local voice engines (Kokoro, Piper; Chatterbox needs conda + an NVIDIA GPU)
# Needs: git, Rust (rustup), Node.js. Windows: run in Git Bash.
set -e
cd "$(dirname "$0")"

echo "== Fetching the ArtCraft apps (git submodules)"
git submodule update --init --recursive

echo "== Applying the FilmCraft patch (contact sheets + autoedit)"
if git -C apps/filmcraft apply --check ../../patches/filmcraft-studio.patch 2>/dev/null; then
  git -C apps/filmcraft apply ../../patches/filmcraft-studio.patch
elif git -C apps/filmcraft apply --check -R ../../patches/filmcraft-studio.patch 2>/dev/null; then
  echo "   already applied"
else
  echo "   patch does not apply cleanly to this FilmCraft version; trying a 3-way merge"
  git -C apps/filmcraft apply --3way ../../patches/filmcraft-studio.patch
fi

echo "== Building all seven apps (release; ~45 min the first time)"
sh tools/build-apps.sh

if [ "$1" = "--tts" ]; then
  echo "== Local voice engines (Kokoro + Piper)"
  PY=${PYTHON:-python}
  $PY -m venv tools/tts/.venv
  V=tools/tts/.venv/Scripts/python.exe; [ -x "$V" ] || V=tools/tts/.venv/bin/python
  $V -m pip install -q --upgrade pip
  $V -m pip install -q kokoro-onnx piper-tts soundfile
  mkdir -p tools/tts/models/kokoro tools/tts/models/piper
  base=https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0
  curl -sSL -o tools/tts/models/kokoro/kokoro-v1.0.onnx "$base/kokoro-v1.0.onnx"
  curl -sSL -o tools/tts/models/kokoro/voices-v1.0.bin "$base/voices-v1.0.bin"
  for v in en_US-lessac-medium en_US-ryan-high en_GB-alan-medium en_GB-jenny_dioco-medium; do
    $V -m piper.download_voices --download-dir tools/tts/models/piper $v
  done
  echo "   Chatterbox (voice cloning, NVIDIA GPU): see tools/tts/README.md"
fi

echo "== Done. Open this folder in Claude Code; start with: \"New project <name>: footage is in <folder>, …\""
