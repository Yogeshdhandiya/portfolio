#!/usr/bin/env bash
# One-time setup for the reel-editor pipeline in a fresh cloud container.
# Usage: setup.sh <work_dir>   (models, assets and fonts land in <work_dir>/{models,assets,fonts})
set -eu
W="${1:?work dir}"; mkdir -p "$W"/{models,assets/sfx,assets/music,assets/fluent,fonts}
HERE="$(cd "$(dirname "$0")" && pwd)"; REPO="$(cd "$HERE/../../../.." && pwd)"

apt-get install -y -q libegl1 libgles2 libgl1 >/dev/null 2>&1 || (apt-get update -q >/dev/null && apt-get install -y -q libegl1 libgles2 libgl1 >/dev/null)
pip install -q sherpa-onnx soundfile mediapipe opencv-python-headless onnxruntime scipy pillow 2>&1 | grep -v WARNING || true

cd "$W/models"
[ -d sherpa-onnx-nemo-parakeet-tdt-0.6b-v2-int8 ] || { curl -sSL -o p.tar.bz2 https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-nemo-parakeet-tdt-0.6b-v2-int8.tar.bz2 && tar xjf p.tar.bz2 && rm p.tar.bz2; }
for u in face_landmarker/face_landmarker/float16/latest/face_landmarker.task hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task; do
  [ -f "$(basename $u)" ] || curl -sSL -o "$(basename $u)" "https://storage.googleapis.com/mediapipe-models/$u"; done
[ -f u2net_human_seg.onnx ] || curl -sSL -o u2net_human_seg.onnx https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net_human_seg.onnx

# SFX: Pixabay-licensed set vendored in this repo (HyperFrames media-use) + ElevenLabs-made set from hassancs91/claude-youtube-editor (MIT repo)
cp "$REPO"/video-editing-arsenal/skills/05-hyperframes-official/skills/media-use/audio/assets/sfx/*.mp3 "$W/assets/sfx/"
if [ ! -d "$W/assets/_yt" ]; then git clone -q --depth 1 --filter=blob:none --sparse https://github.com/hassancs91/claude-youtube-editor.git "$W/assets/_yt" && git -C "$W/assets/_yt" sparse-checkout set media/library/sfx media/library/music; fi
for f in "$W"/assets/_yt/media/library/sfx/clips/*.mp3; do cp "$f" "$W/assets/sfx/h_$(basename "$f")"; done
cp "$W"/assets/_yt/media/library/music/clips/*.mp3 "$W/assets/music/"
python3 -I "$HERE/index_audio.py" "$W/assets"

# Hero objects for cards: Microsoft Fluent 3D emoji (MIT)
cd "$W/assets/fluent"
for n in "Ladder" "Hourglass not done" "Stopwatch" "Toolbox" "Hammer and wrench" "Compass" "Construction" "Robot" "Clipboard" "Rocket" "Bullseye" "Light bulb" "Memo" "Busts in silhouette" "Puzzle piece" "Gear" "Laptop" "Spiral calendar" "Money bag" "Chart increasing" "Camera" "Microphone" "Brain" "Fire" "Trophy" "Key" "Magnifying glass tilted left" "Check mark button"; do
  f=$(echo "$n" | tr 'A-Z ' 'a-z_')_3d.png; [ -f "$f" ] || curl -sS -o "$f" "https://raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets/$(echo "$n" | sed 's/ /%20/g')/3D/$f" || rm -f "$f"; done

# Fonts (Google Fonts is blocked; npm works): heading Funnel Display, body Onest
cd "$W/fonts"
for p in funnel-display onest; do [ -d $p ] || { npm pack -s @fontsource/$p >/dev/null && tar xzf fontsource-$p-*.tgz && mv package $p; }; done
npx --yes @veedstudio/openedit-cli --version >/dev/null 2>&1 || true
echo "setup done: $W"
