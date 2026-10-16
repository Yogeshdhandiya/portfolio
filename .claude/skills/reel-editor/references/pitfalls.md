# Pitfalls and fixes (environment and pipeline)

Each one cost time once. Don't pay for it twice.

## Environment (Claude Code cloud container)
- **Google Drive downloads are blocked by default.** Ask the user to add `drive.google.com` and `drive.usercontent.google.com` to the environment's Allowed domains and set the file to "Anyone with the link". Then:
  `curl -L -o footage.mp4 "https://drive.usercontent.google.com/download?id=<ID>&export=download&confirm=t"`.
  The Drive MCP connector caps downloads at 10 MB.
- **HuggingFace is blocked**, so Whisper, faster-whisper and HF-hosted models won't download. GitHub release downloads, storage.googleapis.com, PyPI and npm do work.
  - ASR: sherpa-onnx + Parakeet TDT 0.6B v2 int8 from `github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-nemo-parakeet-tdt-0.6b-v2-int8.tar.bz2` (word timestamps; tokens start with a space, not "▁").
  - MediaPipe task models: `storage.googleapis.com/mediapipe-models/...` (face_landmarker.task, hand_landmarker.task, selfie_multiclass_256x256.tflite).
  - Matting: rembg models from `github.com/danielgatis/rembg/releases/download/v0.0.0/` (birefnet-portrait, u2net_human_seg). rembg caches to `~/.rembg/models/<name>/`.
- **mediapipe ≥1.0 has no `mp.solutions`.** Use the Tasks API. It needs `apt-get install libegl1 libgles2 libgl1`.
- **Image hosts are blocked** (unsplash, pexels, pixabay, wikimedia). raw.githubusercontent.com works, so use Microsoft Fluent 3D emoji (MIT) for hero objects: `raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets/<Name>/3D/<name>_3d.png`.
- **Google Fonts is blocked.** npm works: `npm pack @fontsource/<family>`. Fontshare (Satoshi, Clash) isn't reachable.
- **SendUserFile limit is 30 MB.** Deliver a 2-pass export at about 4.8 Mbps video + 192k AAC for a 45 s reel (about 27 MB). Keep the CRF-17 master too.

## Rendering
- `openedit-cli render` only serves files under the page's folder. Copy fonts and assets next to `index.html`.
- `--transparent` gives ProRes 4444 with alpha (`yuva444p12le`), about 15 MB/s at 1080x1920. Fine as an intermediate.
- The renderer drives time via `window.__seek(t)`. Write every animation as a pure function of t. Never use CSS transitions or `setTimeout` for motion.
- 4 workers on 4 cores: about 170–300 ms/frame for an overlay page.

## ffmpeg
- **`scale=...:eval=frame` + `crop` does not work for animated zoom.** Crop keeps the first frame's geometry, so zoomed frames get cropped from the left edge and the subject drifts off-centre. Do zoom and reframe per frame in Python (`scripts/compose.py`: pre-scale the source to 1.2x output with lanczos, then OpenCV `warpAffine` INTER_LINEAR, so warps stay near 1:1 without aliasing), which also gives sub-pixel smooth easing.
- Loudness: 2-pass `loudnorm=I=-14:TP=-1:LRA=9` with measured values and `linear=true`. Reference reels sit at -14 LUFS.

## Editorial
- The user's "footage" may already be a cut sequence. Detect its jump cuts (`analyze.py` → local-peak frame difference) and build all framing changes and cards on those exact frames.
- The ASR mishears some words ("audit" came out as "or did") and keeps stumbles. Fix captions only. Don't cut audio you haven't verified.

## Learned during v2 (2026-10-13)
- **Don't `pkill -f <pattern>`** when the pattern also appears in your own bash command line. It kills the tool shell (exit 144). Kill by PID (`ps aux | grep`, then `kill <pid>`).
- **BiRefNet-portrait on CPU** gives the best hair edges, but it OOMs through rembg (more than 15 GB) and takes 40 s to 4 min per frame through raw onnxruntime with the arena off. Only use it for a handful of keyframes. For sequences, use `roto_fast.py` (u2net_human_seg + two-pass guided filter, about 1 s/frame) and smooth over time (0.25/0.5/0.25). u2net also grabs the chair headrest, so keep behind-text above the shoulders.
- **Word-by-word captions drift off-centre** while building because hidden words still take up layout space. Translate the line by `(fullWidth - visibleWidth)/2`, eased per word. Build multi-item rows (tiles) from the centre outward (order 3,2,4,1,5).
- **Lead/tail lines under 48 px vanish at phone size.** Use 50 px lead/tail, 60 px plain, 120–170 px emphasis.
- **Impact SFX tails mud up the low end.** Fade them out about 0.35 s after the hit and set them 4 dB under the whooshes. Check the mix spectrogram (`showspectrumpic`) against the reference.
- Overlay QA (`qa.py`) checks caption alpha against the face box (brow to chin) on every frame, and the caption-band centroid. Run it on the overlay before the expensive composite.

## Learned on job 3 (2026-10-14)
- **Wide shots: FaceLandmarker finds 0 faces at 540 px** (face is about 50 px). Run `FACE_CROP=x0,y0,x1,y1 analyze.py ...` (normalised crop around the subject, decoded from the full-res source at 640 px wide); landmarks are mapped back to full-frame coordinates.
- **Wide 4K source needs big punch-ins.** `compose.py` pre-scales to 1.2x output by default, so anything above z=1.2 goes soft. Set `PRESCALE=1.8` (or up to 2.0 for 4K) for BOTH `plan.py` and `compose.py`; they must match.
- **Few real cuts:** add punch-in cuts on sentence boundaries (word gaps) and alternate the zoom on them. They read as jump cuts.
- **White clothing behind captions:** use the double text-shadow (tight 1-3 px plus soft 12-26 px) already in `template_minimal.html`.
- Junk frames at the tail show up as a burst of "cuts" in the last 0.6 s. Trim with `ffmpeg -t <end> -c copy` and set `N` in the plan.

## Learned on the 4-reel batch (2026-10-16)
- **SendUserFile is 30 MB:** a 67 s reel at 5.2 Mbps is 45 MB. `run_minimal.sh` sets the video bitrate to `min(5200, 28.5 MB*8/duration - 160k)`.
- **CSS class clash:** naming an MG container class `ring` picked up the template's 92 px avatar `.ring` style. MG containers use `mg mg-<type>`.
- **Fluent emoji names 404 sometimes** (`Direct hit` is not there, use `bullseye`). Check every `f:` icon exists in the assets dir before rendering; `gen_mg.py` reports missing ones.
- **`set -e` + a broken `$(python3 -c ...)` kills the whole run instantly.** Test one-liners before putting them in a pipeline script.
- **Preview before rendering:** `node templates/preview.js front.html out.png t1 t2 ...` screenshots the overlay at given times in seconds, which catches layout bugs before a 4-15 minute render.
- Single-take footage (no jump cuts): put punch-in cuts on sentence boundaries every 2-3.5 s and merge the few real cuts `analyze.py` finds.
- **Leaning in at the end:** on a sign-off ("bye-bye") he moves toward the lens, the chin drops below the 1320 caption clamp and the caption touches the face. `planlib` now warns; drop the sign-off caption or move it.
- **`pgrep -f`/`pkill -f` with a bracketed pattern still self-matches** when the plain word appears elsewhere in the same command (e.g. `[r]erun.sh` plus `bash rerun.sh` later in the line). It killed the tool shell (exit 144) and left the renderer orphaned. Look up PIDs with `ps aux | grep` in one call, then `kill <pid>` in a separate call.
