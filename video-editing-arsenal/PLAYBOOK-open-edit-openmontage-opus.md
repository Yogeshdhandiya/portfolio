# Using open-edit, OpenMontage and the Opus 5.5 prompt library

These three sources are worth more together than apart:

- The Opus 5.5 prompts give you motion-graphics ideas that already work.
- open-edit turns any HTML animation into a real video file, including a transparent one.
- OpenMontage supplies individual tools (face tracking, stock B-roll search, a review protocol) to slot into your pipeline.

Tested on 2026-10-13: a canvas animation rendered through `openedit-cli render` gave a frame-accurate 1080x1920 MP4 in 19s. With `--transparent` it gave ProRes 4444 with an alpha channel (`yuva444p12le`).

## 1. Opus 5.5 prompt library → a motion-graphics bank

**What it is:** 703 prompts creators shared for videos Claude Opus 5.5 built as code. 418 have live remakes on [Skillry](https://skillry.dev/ai-videos/opus-5-5).
- Categories: motion 369, 3D 117, explainer 116, interactive 101.
- Tech tags: canvas 267, svg 183, threejs 131, shader 92, gsap 86.
- 207 of the prompts are partial.
- Vendored at `prompts/opus-5-5-videos/` (MIT). Each prompt is in `prompts/<slug>.md`, and all of them are in `data/videos.json`.

**What it doesn't include:** the actual HTML code. You get the prompt, and Opus writes the code again each time. Results vary between runs, so render, review and iterate.

**How to use it in your 18 steps:**

| Step | Use |
|---|---|
| 5 Planning | When a beat needs a visual, filter `data/videos.json` by `category` (`explainer` for process and data beats, `motion` for hook and title cards) and pick a prompt as the starting brief |
| 14 Style + motion kit | Adapt a prompt to your brand (colors, font, 9:16, duration), then save the HTML that works into your own card library next to Nate's `style-library`. The prompt is disposable, the rendered HTML is the asset. |
| 12 Gen video | Covers the shots you'd otherwise generate but that are really graphics, such as data, maps, UI or 3D product spins. Code renders are free, exact and editable, which Veo isn't. |
| 13 Rotoscopy | Render with `--transparent` and put the element behind the speaker using a matte from `embedded-captions` or SAM 3 + MatAnyone 2 |

**Find prompts fast:**

```bash
# all complete explainer prompts that use gsap or svg
python3 -c "import json;[print(v['slug'],v['tech_tags']) for v in json.load(open('prompts/opus-5-5-videos/data/videos.json')) if v['category']=='explainer' and not v['prompt_partial'] and {'gsap','svg'}&set(v['tech_tags'])]"
```

## 2. open-edit (VEED) → render, cut verification, NLE hand-off

Skill vendored at `skills/08-render-any-html/open-edit/` (Apache-2.0). The CLI runs with `npx @veedstudio/openedit-cli`. It works on macOS, Linux and Windows with Node 20.18+.

**Its main value is the renderer.** It renders any HTML page, so the page doesn't need to follow the HyperFrames composition contract. That makes it the missing piece for the Opus prompts, which output plain canvas, SVG or Three.js pages.

How the renderer works:
- It owns time. It controls `performance.now`, `requestAnimationFrame`, timers, seeded `Math.random`, CSS animations and GSAP, so every frame is exact.
- Anything else that moves goes in `window.__seek(t)`.
- `--transparent` outputs ProRes 4444 with alpha, which goes straight onto a track above your footage in Premiere, Resolve or CapCut.
- `--from 4 --to 6` re-renders only the part you changed.
- `--stills 0.5,2,4 --sheet s.jpg` shows you chosen moments without a full render.

```bash
openedit render runs/hook/index.html --out runs/hook/hook.mov --fps 30 --duration 4 --transparent
```

**What else to use from it:**

| Step | Command | Why |
|---|---|---|
| 1 Watch | `frames <video> --at 12.5,1:02 --sheet` | One contact sheet of the moments you name. Cheap for the model to look at. |
| 3 Audio | `transcribe --provider whisperx` | Free, local word timings. It also imports whisper.cpp or WhisperX JSON via `whisper`. |
| 4/7 Cutting | `speech-probe <video> --gap 250` | Measures the noise floor, speech onset and decay, and real gaps from the audio. Its rule is that transcript word boundaries aren't cut points: if there's no gap, don't cut. Run it on Nate's `cut-mistakes` candidates before you apply them, so no cut clips a word. |
| 4/7 Cutting | `apply-edl --crossfade 40` then `retime-transcript` | Frame-snapped assembly with 40ms audio crossfades, with captions retimed onto the cut |
| 10 Capture | `stills search "berlin skyline"` | Real, licensed stock pictures |
| 13 Roto | `background-removal video.mp4` | Free through VEED's route. It only spends money on fal if you pass `--fal`. |
| 16 SFX/mix | `mix-audio`, `mux-audio` | Voice ducks the music bed, then muxes at delivery loudness |
| NLE | `veed-project plan.json` / `veed-pull` | Sends the agent's cut into VEED's editor as an editable project and pulls changes back |

You need a VEED login for: VEED transcription, the free background-removal route, Fabric AI presenters, and the editor hand-off. Rendering, WhisperX, the cut tools and mixing are fully local.

## 3. OpenMontage → individual tools, not the whole system

The whole system (12 pipelines, more than 700 skill files) is built to produce videos from a prompt, not to polish your own talking-head footage. Your pipeline is already better for that. Take the parts it does better than anything else:

| Your step | OpenMontage piece | What it gives you |
|---|---|---|
| 9 Geometry | `tools/analysis/face_tracker.py` | MediaPipe Face Mesh: per-frame face bbox, landmarks and **head pose** as JSON |
| 6 Short-form | `tools/video/auto_reframe.py` | Converts 16:9 to 9:16 while following the face. Feed it the face tracker output. |
| 11 B-roll | `tools/video/corpus_builder.py` + `clip_search.py` | Searches 17 free and public-domain stock sources (Pexels, Pixabay, Mixkit, Coverr, Videvo, archive.org, NASA, Wikimedia...), downloads clips, embeds them with CLIP ViT-B/32, then ranks clips for a scene description with diversity re-ranking (MMR). It's the best automated **stock** B-roll finder available. It doesn't index your own footage folder. |
| 8 Cut audit | `tools/analysis/visual_qa.py` | Frame pulls, probe checks, audio levels, a **caption-over-face occlusion check**, and transition checks |
| 12 Gen video | `tools/video/veo_video.py` | Veo 3.1 by API: text, image, reference and first/last-frame to video. A pay-per-second alternative to flow-mcp's free Flow credits. |
| 16 SFX / music | `tools/audio/freesound_music.py`, `pixabay_music.py`, `music_library.py` | Licensed music and SFX sourcing |
| 18 Review gate | `skills/meta/reviewer.md` + `checkpoint-protocol.md` | The best-written review protocol in this whole collection. Its CHAI rules say every finding must cite a concrete frame or field, the reviewer must scan for the rest of the same class of mistake, and every critical finding must come with a fix. Copy these rules into whatever review step you run. |
| 1/2 Reference analysis | `skills/meta/video-reference-analyst.md` | A 417-line protocol for breaking down a reference video |
| Knowledge | `skills/creative/broll-planning.md`, `short-form.md`, `sound-design.md`, `storytelling.md` | Dense editorial rules to feed your planning step |

**How to run it:** use `./clone-external.sh`, which puts it in `_external/calesthio__OpenMontage`. Then run `make setup` inside that folder. The tools depend on its `tools/base_tool.py` and `lib/`, so call them inside that checkout. List what's available with:

```bash
python -c "from tools.tool_registry import registry; import json; registry.discover(); print(json.dumps(registry.capability_catalog(), indent=2))"
```

**License:** OpenMontage is AGPL-3. Running it on your own machine for client work is fine. Copying its code into something you distribute, or running it as a service for others, triggers AGPL obligations. That's why it isn't vendored here.

## The combined flow for one talking-head reel

1. **Cut:** Nate's `cut-silences` and `cut-mistakes` propose cuts. open-edit `speech-probe` verifies every cut point. `apply-edl --crossfade 40` assembles the cut, and `retime-transcript` moves the captions onto it.
2. **Reframe:** OpenMontage `face_tracker` then `auto_reframe` if the source is 16:9.
3. **Plan:** Nate's `video-storytelling` and `video-beats`. For each beat that needs a graphic, take an Opus 5.5 prompt as the brief.
4. **Build graphics:** Opus writes the HTML, then `openedit render --transparent` gives you alpha overlays. Branded pieces go through HyperFrames.
5. **B-roll:** OpenMontage `corpus_builder` and `clip_search` for stock, flow-mcp or `veo_video` for generated shots.
6. **Captions:** HyperFrames `embedded-captions`.
7. **Sound:** hassancs91 `suggest-sfx`, then open-edit `mix-audio` and `mux-audio`.
8. **Review:** OpenMontage reviewer rules applied to krusemediallc `video-qa` output.
9. **Hand-off** if a human finishes the edit: open-edit `veed-project`, or alpha MOVs dropped into Premiere or Resolve.
