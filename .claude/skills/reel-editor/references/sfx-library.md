# SFX and music library map (installed by scripts/setup.sh into $W/assets)

Licences: the plain names are Pixabay Content License (commercial OK, from HyperFrames media-use). `h_*` files are ElevenLabs-generated, from hassancs91/claude-youtube-editor (MIT repo, commercial use per the generator's plan). Music beds are ElevenLabs-generated, from the same repo.

| Moment | First choice | Rotate with | Gain | Align |
|---|---|---|---|---|
| Card in (whoosh layer) | whoosh-cinematic | whoosh, h_whoosh-wind, whoosh-short (-2 st), h_whoosh-soft | -6 to -7 dB | peak on cut |
| Card in (impact layer) | impact-bass-1 | h_impact-deep-soft, h_launch-thump, impact-bass-2 (peak), h_impact-soft | -11 to -13 dB, tail cut 0.35 s | onset on cut |
| Card label blur-in | h_ui-click-soft | click-soft | -10 dB | onset |
| Card out | h_whoosh-reverse | whoosh-short (+3 st) | -15 dB | peak on cut |
| Zoom-blur cut | whoosh-short | ±2 st variants | -9 dB | peak on cut |
| Glow word | sparkle | ping, h_chime-magic | -16 to -19 dB | onset |
| Gold word | h_chime-reward | h_pop-reveal (-2 st), sparkle (+3 st) | -14 to -17 dB | onset |
| Big white word | h_stamp-hit | h_knock-solid, impact-bass-1 (+2 st) | -15 dB | onset |
| Letter scramble | glitch-3 | h_glitch-zap | -10 dB | onset |
| Chip pop | pop | h_ui-toggle-on, pop (+3 st) | -9 to -10 dB | onset |
| Typing text | typing | key-press per char | -11 dB | peak at start |
| Tiles / list build | pop | pitch 0, 2, 4, 5, 7 | -12 dB | onset |
| Tension creep | h_scan-hum | h_wind-soft | -20 dB | onset |
| Reveal build | h_riser-soft | riser (10 s, peak at 3.04 s) | -9 dB | peak on reveal |
| Music bed | tech-pulse (steady pulse, even energy) | cinematic-min (builds late), lofi-warm (drums from 12 s) | -17 dB then sidechain duck | from 0, fades 0.4 s in / 1.4 s out |
