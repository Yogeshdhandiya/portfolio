# Job: "5 things before I started freelancing" (2026-10-13)

- Source: 4K 9:16 23.976 fps, 43.6 s, already a Premiere sequence with 14 jump cuts.
- Reference: Ashmit Shahi blue-glow reel (see ../../references/style-blue-glow.md).
- v1 (rejected): sentence-time zooms through a broken ffmpeg crop (zoomed into the side), a single font, synthesized SFX, chunk-pop captions, text on the chin, tiles not centred.
- v2: everything in `plan.py` here. Camera keys per shot, 33 designed phrases, 5 image cards + loop card, "5 THINGS" rotoscoped behind the head, 55 SFX cues (`sfx_cues.json`) + tech-pulse bed.
- QA v2: 0 caption/face collisions over 1046 frames, no black or frozen frames, -14.0 LUFS / -1.0 dBTP, A/V 43.627 s.
- Reuse: copy `plan.py`, then replace CUTS (from analyze.py), CAM keys, CARDS, P (phrases) and FIX for the new transcript.
