# How to break down a reference reel (do this before planning anything)

1. **Probe:** resolution, fps, duration, loudness (`ebur128`).
2. **Overview sheet:** `fps=1,scale=240:-1,tile=6x9`. This gives section structure and recurring graphics.
3. **Section sheets at 8–12 fps** for every distinct moment (hook, first caption, first emphasis, each card in/out, each overlay, CTA):
   `ffmpeg -ss <t> -t 2.5 -i ref.mp4 -vf "fps=8,scale=180:-1,tile=10x2" -frames:v 1 sec.jpg`.
   Look for: how text enters and exits (blur, scale, word-by-word, letter scramble), stacking hierarchy, what changes on cuts (zoom alternation), transition types (zoom-blur, RGB split, hard cut), what sits behind the subject (roto), counters, UI overlays.
4. **Transcribe the reference** to map emphasis words to their styles (which words got glow, gold, chip...).
5. **Spectrogram:** `showspectrumpic=s=1800x500:scale=log:fscale=log`. A continuous low band means a music bed. Horizontal lines are sustained synth notes. Full-band vertical lines are SFX transients. Count SFX density per second.
6. **Write the style file** (`references/style-<name>.md`) with measurable values: positions as % of height, sizes, durations, colours, the emphasis taxonomy, card anatomy, SFX density.
7. **Element checklist:** every reference element maps to an element in our edit, or gets a written reason why not (e.g. no name lower-third because the creator's name is unknown, so ask for it next time).
