# SFX and music library map (installed by scripts/setup.sh into $W/assets)

Licences: the plain names are Pixabay Content License (commercial OK, from HyperFrames media-use). `h_*` files are ElevenLabs-generated, from hassancs91/claude-youtube-editor (MIT repo, commercial use per the generator's plan). Music beds are ElevenLabs-generated, from the same repo.

**Rule (Yogesh, round 2): SFX on KEY moments only, about 1 cue per 2.5 s.** `audio.py` auto-levels each cue so its loudest 0.4 s window sits at (voice speech level + Rel dB).

| Moment | KEY? | File (rotate) | Rel dB | Align |
|---|---|---|---|---|
| Card in | yes | whoosh (-1 st), whoosh, h_whoosh-soft, whoosh-short (-2 st), h_whoosh-wind | -9 | peak on cut |
| First card only, impact | yes | h_impact-soft (tail cut 0.35 s) | -11 | onset |
| Zoom-blur cut | yes | whoosh-short (+2 / 0 / -1 st) | -11 | peak on cut |
| Roto text typing | yes | typing | -12 | peak at start |
| Tiles / list build | yes, ONE cue | pop | -13 | onset |
| Chip pop | yes | pop, h_ui-toggle-on, pop (+3 st) | -13 | onset |
| Letter scramble (max one) | yes | glitch-3 | -13 | onset |
| Into a full-screen reveal | yes | h_riser-soft | -12 | peak on reveal |
| CTA keyword | yes | h_impact-deep-soft | -11 | onset |
| Glow / gold / white emphasis words | **no** | (the music bed carries these) | | |
| Card label, card out, tension beds | **no** | | | |
| Avoid entirely | | impact-bass-2, whoosh-cinematic, riser (10 s): long swells sit on the voice | | |
| Music bed | always | tech-pulse (steady pulse, even energy); alternatives cinematic-min (builds late), lofi-warm (drums from 12 s) | -17 dB, then sidechain duck | fade 0.4 s in / 1.4 s out |
