# Yogesh's feedback log (hard rules, apply on the first pass)

Every item came from a real review. Treat each one as a failing test.

## Round 1 (v1 → v2), 2026-10-13

| # | Feedback | Rule going forward |
|---|---|---|
| 1 | Number tiles sat on the left side, not centred | Every overlay group is horizontally centred on the frame (x = 540 in a 1080 frame) unless the design deliberately anchors to a corner. QA checks the alpha centroid of each overlay group. |
| 2 | CTA looked off-centre | Same rule. Also caused by the zoom bug below: the subject drifted off-centre, so centred text looked wrong. |
| 3 | Same font for headings and body text | Use two families. Display/heading face for numbers, card labels, big glow words and CTA; a separate text face for running captions. Current pair: **Funnel Display 800** (heading) + **Onest 600/700** (captions). |
| 4 | Zooms were not centred, they zoomed into the side | Never do `scale=...:eval=frame` followed by `crop` in ffmpeg (crop keeps its first-frame geometry, so zoomed frames get cropped from the left edge). Zoom with a per-frame affine in Python (`scripts/compose.py`), anchored on the tracked face. |
| 5 | Pacing good but not smooth | Change framing exactly ON the existing jump cuts (detect them with `scripts/analyze.py`), never between them. Ease every animated zoom (cubic in-out, 0.3–0.45 s). Keep a slow drift inside long shots. Use zoom-blur and RGB-split transitions on a few cuts. Keep a continuous music bed under everything. Captions build word by word with a blur-fade instead of popping a whole chunk. |
| 6 | Fonts looked basic | Pick distinctive current faces (not Inter or Sora defaults). Check them against the reference with a specimen render before building. |
| 7 | "Reduce letter space to 20–30" | Tracking **-20 to -30** in AE/Premiere units, which is `letter-spacing: -0.02em` to `-0.03em`. Default is -0.025em on every text layer. (-25 px would collapse the letters.) |
| 8 | SFX were all the same and sounded old and synthetic | Never synthesize SFX with sine/noise. Use the real libraries (`references/sfx-library.md`). Never repeat the same file twice in a row. Rotate variants, pitch ±1–2 semitones, layer whoosh+impact on big moments, add risers into reveals, and add a music bed. |
| 9 | Text sometimes landed on the chin | Captions are face-aware. Per chunk, take the max tracked chin y (after the zoom transform) over the chunk's duration, add a margin, and place the caption below it. QA intersects caption alpha boxes with the face box on every frame. |
| 10 | "Match the reference in every detail": SFX, animation styles, rotoscoping, transitions | Do a frame-level reference breakdown first (`references/reference-breakdown-method.md`) and build an element-by-element checklist from it. Every element in the reference needs a counterpart in the edit or a written reason why not. |
| 11 | Keep saving learnings as a skill | Update this skill at the end of every job: new feedback here, new pitfalls in `pitfalls.md`, new working scripts in `scripts/`. |

## Round 2 (v2 → v3), 2026-10-13

| # | Feedback | Rule going forward |
|---|---|---|
| 12 | Too many SFX, and too loud | **SFX on key moments only: about 1 cue per 2.5 s** (v3: 17 cues in 44 s; v2 had 55). Use them on card-ins (whoosh only, one impact on the first card), zoom-blur cuts, chips, the one scramble, the riser into the loop, the CTA. **No SFX on every emphasis word**, no label clicks, no card-out swishes, no tension beds. Levels are auto-set in `audio.py`: each cue's loudest 0.4 s window sits **9–13 dB under the voice speech level**. QA checks that no SFX window gets closer than -6 dB to the voice. Avoid long-swell files (impact-bass-2, whoosh-cinematic) because the swell sits on the voice for 2 s. |
| 13 | Forgot to colour grade (v2's grade was too subtle to see) | Always grade the base with `scripts/grade.py` and show a before/after strip next to a reference frame before compositing. Look for the reference: saturated purple-blue light shifted toward teal (-30° hue on blues), blues darkened (-42% value) and desaturated a little, skin warmed and brightened, teal shadows / warm highlights, crushed blacks, S-curve, strong vignette, fine grain. It's baked into a 128³ LUT (about 180 ms/frame). |

## Round 3: v3 delivered 2026-10-13, awaiting feedback
Log his next notes here as Round 3 and turn each one into a rule.
