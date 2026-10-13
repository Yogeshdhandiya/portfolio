# Pre-delivery audit (think like a senior editor)

Check every line on the rendered file, not the plan. "Not checked" counts as a fail.

## Framing and camera
- [ ] Face centred horizontally in every shot (zoomed frames included). No drift toward an edge.
- [ ] Framing changes land exactly on the source's jump cuts. No unmotivated zoom jump between cuts.
- [ ] Animated zooms are eased, and none snaps except deliberate punch words (≤ 0.15 s snap).
- [ ] Zoom-blur/RGB-split transitions: 2–3 max, centred on the cut frame, no visible edge repeat.
- [ ] Max zoom keeps detail (source ≥ 1.2x output at max zoom).

## Captions and text
- [ ] Zero caption pixels inside the brow-to-chin box (`qa.py` collisions = 0).
- [ ] Every text group horizontally centred. Building lines re-centre.
- [ ] Two font families (heading vs body). Tracking -0.025em.
- [ ] Captions build word by word in sync with speech (word start ±1 frame).
- [ ] Emphasis every 3–6 s, styles varied (glow / gold / white / scramble / chip). Never two big emphases on screen at once.
- [ ] Nothing in the bottom ~280 px (platform UI) or the right ~120 px of the lower half (like/comment rail).
- [ ] Spelling and ASR fixes applied. Stumbles removed from captions.

## Graphics
- [ ] Cards cut in on a jump cut, hold 1.3–1.7 s, label blur-in, slow push.
- [ ] Rotoscoped text: the subject overlaps no more than about 30% of the glyph height, and the text stays readable.
- [ ] Hero images consistent (same duotone, same scale logic).

## Sound
- [ ] Music bed present the whole time, ducked under the voice, fade in and out.
- [ ] SFX on every card in/out, cut transition, emphasis and chip. No file repeated back to back. Pitch variety.
- [ ] Impacts don't mask the voice (check the spectrogram: no long low-end slabs over speech).
- [ ] -14 LUFS integrated, ≤ -1 dBTP. Voice intelligible over everything.

## Delivery
- [ ] Audio and video durations match. No black or frozen frames (`qa.py`).
- [ ] 1080x1920, 23.976/24 fps, H.264 high, yuv420p, faststart.
- [ ] Delivered file ≤ 30 MB (2-pass), master kept.
- [ ] Skill updated with new feedback and pitfalls.
