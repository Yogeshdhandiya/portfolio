---
name: reel-editor
description: Edit a talking-head reel (9:16) to match a reference video's style end to end. Covers the frame-level reference breakdown, transcription, jump-cut detection, face-anchored punch-ins and zoom-blur transitions, word-by-word stacked captions placed below the chin, glow/gold/scramble/chip emphasis, rotoscoped text behind the head, image cards, varied cinematic SFX plus a ducked music bed, an automated QA gate, and a sub-30 MB delivery. Use when Yogesh shares footage (file or Drive link) plus a reference reel and asks for an edited MP4, a v2/revision, or "make it like this reference". Read references/user-feedback.md first; every rule there came from his reviews.
---

# Reel editor

Built from real jobs for Yogesh (yog.visuals). It encodes his feedback, the reference house style and every environment pitfall hit so far. Goal: get it right on the first pass.

**Read first, every time:**
1. `references/user-feedback.md`: hard rules from his reviews. Treat each as a failing test.
2. `references/pitfalls.md`: environment and pipeline traps, with the fixes.
3. Style files, one per reference he has used: `references/style-blue-glow.md` (heavy: glow captions, roto, image cards; overlay `templates/template.html`, `GRADE_PRESET=blueglow`) and `references/style-minimal-clean.md` (minimal: 1-2 word captions, condensed emphasis, white cutaway cards with blur dissolve; overlay `templates/template_minimal.html`). **Grade is always `GRADE_PRESET=blueglow`, whatever the reference's own grade** (his rule 14: it's his look across every reel). `neutral` exists only if he asks for it.
4. `references/audit-checklist.md`: run it before delivering.

**Low-credit mode (he asked for it).** Same reference as a past job: skip the breakdown, copy that job's `plan.py` and template, only rewrite the cut list, cards, emphasis and SFX. Look at no more than 3 images (one grade strip, one final contact sheet). Run long steps in the background and don't poll them.

## Pipeline (scripts in `scripts/`, overlay in `templates/`)

| Step | What | Command |
|---|---|---|
| 0 | One-time setup: ASR model, MediaPipe, u2net, SFX + music libraries, Fluent 3D hero images, fonts, renderer | `bash scripts/setup.sh $W` |
| 1 | Get the footage. Drive needs `drive.google.com` and `drive.usercontent.google.com` allowed and "Anyone with the link" sharing | `curl -L -o src/footage.mp4 "https://drive.usercontent.google.com/download?id=<ID>&export=download&confirm=t"` |
| 2 | **Reference breakdown at frame level** (contact sheets at 8–12 fps per section + full spectrogram). Write or extend the style file and list every element. | see `references/reference-breakdown-method.md` |
| 3 | Transcribe (word timestamps, Parakeet via sherpa-onnx) | `python3 -I scripts/transcribe.py src.wav src.words.json` |
| 4 | Analyse the source: jump cuts (local-peak frame diff), per-frame face box, chin, hands | `python3 -I scripts/analyze.py footage.mp4 analysis.json $W/models` |
| 5 | **Plan** (edit `plan.py`): cut list, camera keys per shot (wide/tight alternating ON cuts, eased punch-ins on emphasis words, drift), zoom-blur cuts, cards on cut frames, phrase design (lead / EMPH / tail + style), roto text, tiles. It computes face-aware caption y and the output-space face box per frame. | `python3 -I plan.py src.words.json` |
| 6 | Rotoscope the frames where text goes behind the subject | `python3 -I scripts/roto_fast.py footage.mp4 matte $W/models/u2net_human_seg.onnx 1.25:3.10` |
| 7 | Overlay layers (front = captions/cards/tiles/loop; behind = roto text), rendered with alpha | `python3 templates/gen.py` then `npx @veedstudio/openedit-cli render front.html --out front.mov --fps 24000/1001 --duration <d> --transparent --workers 4` (same for behind.html over its range) |
| 8 | QA the overlay before compositing: caption/face collisions, centring | `python3 -I scripts/qa.py plan.json front.mov <any.mp4>` |
| 9 | Sound: cue sheet (put it in `plan['sfx']` as [t, file, rel_dB, semitones, align]; `plan['music']`, `plan['music_db']`), music bed ducked under the voice, 2-pass loudnorm -14 LUFS | `python3 -I scripts/audio.py footage.mp4 plan.json $W/assets mix.wav` |
| 10 | Composite: face-anchored sub-pixel reframe, zoom-blur + RGB split (`cam.blur`), blur dissolve (`cam.gblur`), grade (`GRADE_PRESET`), roto, overlay, encode | `python3 -I scripts/compose.py footage.mp4 plan.json front.mov behind.mov matte mix.wav master.mp4 16` |
| 11 | QA the final + contact sheet; fix and re-run what failed | `python3 -I scripts/qa.py ...` + `ffmpeg ... tile=8x3` |
| 12 | Deliver: SendUserFile limit 30 MB, so make a 2-pass export at about 4.8 Mbps video + 192k AAC | see `references/pitfalls.md` |
| 13 | **Update this skill**: new feedback goes to user-feedback.md, new traps to pitfalls.md, script fixes to scripts/ | always |

## Design system (current, approved direction)
- Fonts: **Funnel Display 800** for headings, numbers, card labels and emphasis words. **Onest 600/700** for captions. Tracking -0.025em everywhere (his "-20 to -30").
- Sizes at 1080x1920: lead/tail 50 px, plain 60 px, emphasis 120–170 px fitted to 930 px, chip 52 px, card number 330 px, card label 104 px.
- Caption anchor: below the max chin y during the phrase + 78 px, clamped to 1060–1330. Nothing in the brow-to-chin box, ever.
- Centring: every group centred on x = 540. Building lines re-centre on visible words. Rows build centre-out.
- Motion: everything is a pure function of t (`window.__seek`). Words blur-fade up (0.13 s). Emphasis scales from 1.16 to 1 with blur 12→0. Gold has a light sweep. Chips pop with overshoot, and the sparkle follows 0.12 s later. Phrases exit with a blur-fade (0.09 s).
- Camera: framing changes only on the source's jump cuts. Eased (cubic) punch-ins of 0.3–1.1 s inside long shots. 2.2% drift per shot. Zoom-blur + RGB split on 2–3 cuts. Min zoom 1.06 so the face can stay centred.
- Sound: never synthesize SFX. **Key moments only (about 1 cue per 2.5 s)**, auto-levelled 9–13 dB under the voice. Never repeat the same file back to back. Peak-align whooshes to the cut. No long-swell files. Use a steady music bed (`tech-pulse`) sidechain-ducked under the voice. Final -14 LUFS / -1 dBTP.
- Grade: always (`scripts/grade.py`). Blues shifted to teal and darkened, warm bright skin, teal shadows / warm highlights, crushed blacks, S-curve, vignette, grain. Approve a before/after strip next to a reference frame before compositing.

## Time budget seen on a 44 s reel (4 CPU container)
Setup about 3 min · transcription 20 s · analysis 65 s · roto (44 frames) 80 s · overlay render 3.5 min · audio 80 s · composite 3.5 min · QA 1 min.
