# Video Editing Arsenal

The best open-source skills, repos and engines for AI-assisted video editing, mapped to the 18-step pipeline. I researched GitHub, skill directories and creator-made kits from YouTubers, then compared tools that solve the same problem and picked one winner for each step.

Snapshot date: 2026-10-13. Star counts were taken from GitHub on that date.

## What's in this folder

| Path | What it is |
|---|---|
| `skills/` | Vendored copies of the winning skills. All are MIT or Apache-2.0. Each folder includes `SOURCE.md` (upstream URL and commit) and the upstream `LICENSE`. |
| `clone-external.sh` | Clones the picks that can't be vendored (no license, AGPL/GPL, or too big) into `_external/`, which is gitignored. |
| `install-skills.sh` | Symlinks the standalone vendored skills into `~/.claude/skills`. |
| `prompts/opus-5-5-videos/` | 703 creator-shared prompts for motion graphics, explainers and 3D that Claude Opus 5.5 built as code ([yihui-dev/awesome-opus5-5-videos](https://github.com/yihui-dev/awesome-opus5-5-videos), MIT). |
| `PLAYBOOK-open-edit-openmontage-opus.md` | How to combine open-edit, OpenMontage and the Opus prompts with the rest of the pipeline. |

Vendored skills:

| Folder | Upstream | Covers |
|---|---|---|
| `skills/01-watch-and-understand/video-use` | [browser-use/video-use](https://github.com/browser-use/video-use) (28.9k stars, MIT) | Watching footage, filler removal, cut self-check, grading, subtitles |
| `skills/02-full-edit-pipeline/nateherk-hyperframes-kit` | [nateherkai/hyperframes-student-kit](https://github.com/nateherkai/hyperframes-student-kit) (1.4k stars, MIT, by YouTuber Nate Herk) | cut-silences, cut-mistakes, short-form-edit, video-beats, storytelling, 406 motion-graphics cards, QA scripts |
| `skills/03-rough-cut-local/claude-code-video-editing-skill` | [vincentventalon/claude-code-video-editing-skill](https://github.com/vincentventalon/claude-code-video-editing-skill) (MIT) | One-command local rough cut (whisper.cpp): silences, false starts, keep-last-take |
| `skills/04-face-safe-reels/ghost-editor` | [kurbaitaev/ghost-editor](https://github.com/kurbaitaev/ghost-editor) (MIT) | Face tracking, captions that never cover the face, best-take selection, 7 reel styles |
| `skills/05-hyperframes-official` | [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) (62.6k stars, Apache-2.0) | Render engine skills, embedded-captions (text behind you, face safe zones), audio, media-use (SFX/BGM), motion graphics |
| `skills/06-youtube-editor-audio-sfx/claude-youtube-editor` | [hassancs91/claude-youtube-editor](https://github.com/hassancs91/claude-youtube-editor) (MIT, by YouTuber Hasan Aboul Hasan) | clean-cut, clean-audio (denoise), suggest-sfx (shared SFX library), fake-screencast, thumbnails |
| `skills/07-capture-and-utilities/digitalsamba-skills` | [digitalsamba/claude-code-video-toolkit](https://github.com/digitalsamba/claude-code-video-toolkit) (2.2k stars, MIT) | playwright-recording, ffmpeg, elevenlabs, moviepy |
| `skills/08-render-any-html/open-edit` | [veedstudio/open-edit](https://github.com/veedstudio/open-edit) (1.6k stars, Apache-2.0) | Renders any HTML page to MP4 or alpha ProRes, `speech-probe` cut verification, EDL assembly, mixing, VEED editor hand-off |

## Verdict table (your 18 skills)

| # | Your skill | Winner | Runner-up | In repo? |
|---|---|---|---|---|
| 1 | Watch | video-use | bsisduck/video-analyzer-skill | Vendored |
| 2 | Visual understanding | Gemini video API + video-use `timeline_view`; TransNetV2 for shots | Qwen3-VL (local) | Vendored (skill) |
| 3 | Audio analysis | ElevenLabs Scribe (paid) / WhisperX (local) + CrisperWhisper for fillers | faster-whisper, whisper.cpp | Engines linked |
| 4 | Silence + repetition cutting | Nate's `cut-silences` + `cut-mistakes`, cut points verified with open-edit `speech-probe` | auto-editor (no AI, NLE export) | Vendored |
| 5 | Edit planning | Nate's `video-storytelling` + `hyperframes-video-beats` | OpenMontage pipelines | Vendored |
| 6 | Rough cut + short-form cutaway | Nate's `short-form-edit` | ghost-editor, hassancs91 `clean-cut` | Vendored |
| 7 | Air / fumble / repeat removal | Nate's `cut-mistakes` (review-gated) | ghost-editor take selection, vincentventalon keep-last-take | Vendored |
| 8 | Cut auditing | krusemediallc `video-qa` (4 layers) | Nate's `qa-*.mjs` scripts, video-use self-check | Clone script / vendored |
| 9 | Geometry (face, hands, key areas) | HyperFrames `embedded-captions` safe-zones + ghost-editor `face_track.py` | OpenMontage `face_tracker` (head pose) + `auto_reframe`; MediaPipe for hands | Vendored / clone script |
| 10 | Capture + recording | shot-scraper + `playwright-recording` | krusemediallc `broll-capture`, Cap | Vendored / linked |
| 11 | B-roll understanding + tags | Own footage: video-db/skills (hosted) / VideoSeek (local). Stock: OpenMontage `corpus_builder` + `clip_search` | DIY: Qwen3-VL-Embedding or open_clip | Clone script |
| 12 | Gen video (Flow, Veo 3.1) | GTAI-1/flow-mcp | Veo API via Gemini; Wan2.2/LTX-2 local | Clone script |
| 13 | Rotoscopy | HyperFrames `embedded-captions` matte (skill); SAM 3 + MatAnyone 2 (engine) | RobustVideoMatting, CorridorKey | Vendored / clone script |
| 14 | Style + motion graphics kit | Nate's `style-library` (406 cards) + HyperFrames registry + 703 Opus 5.5 prompts | remotion-dev/skills | Vendored |
| 15 | Captions | HyperFrames `embedded-captions` | Remotion captions skill, pycaps | Vendored |
| 16 | Sound effects | hassancs91 `suggest-sfx` + HyperFrames `media-use` | krusemediallc `sound-design`, MMAudio | Vendored |
| 17 | Render | HyperFrames CLI for compositions, open-edit `render` for any HTML and alpha overlays, FFmpeg for assembly | Remotion | Vendored |
| 18 | Review gate | krusemediallc `video-qa` + `video-review-canvas`, judged with OpenMontage `reviewer.md` rules | OpenMontage checkpoint protocol | Clone script |

---

## 1. Watch skill

**Winner: [browser-use/video-use](https://github.com/browser-use/video-use)** (28.9k stars, MIT, vendored)

It doesn't dump frames into the model. It makes one transcript per source with word timestamps, speakers and audio events like laughter, packed into a ~12KB file. When it hits a decision point, such as an ambiguous pause or a retake comparison, it renders a `timeline_view` PNG: filmstrip, waveform and word labels for that time range. You get most of what full frame-by-frame watching would give you for a fraction of the tokens.

| Option | Approach | Verdict |
|---|---|---|
| video-use | Transcript plus on-demand filmstrip/waveform composites | Best balance of accuracy and token cost |
| [bsisduck/video-analyzer-skill](https://github.com/bsisduck/video-analyzer-skill) (GPL-3) | Frame extraction, scene detection, transcription, parallel subagents | Good for deep analysis of someone else's video. Heavier. |
| krusemediallc `video-qa` L3 | Gemini watches and listens to a 480p proxy | Best real "watching", but needs a Gemini key |
| [yt-dlp](https://github.com/yt-dlp/yt-dlp) (197k) + [youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api) (8.5k) | Download and pull transcripts | Required plumbing to watch any online reference |
| [dawoodabdullah010/insta-reel-research](https://github.com/dawoodabdullah010/insta-reel-research) | Paste an IG reel link, get a shot-by-shot breakdown | Handy for analyzing competitor reels |

## 2. Understanding videos visually

There's no single skill for this. The best setup is a model plus a shot detector:

| Layer | Pick | Why |
|---|---|---|
| Model (hosted) | Gemini API, which takes native video input | The only mainstream model that ingests video with its audio track |
| Model (local) | [QwenLM/Qwen3-VL](https://github.com/QwenLM/Qwen3-VL) (20.1k) | Best open video-language model |
| Shot boundaries | [soCzech/TransNetV2](https://github.com/soCzech/TransNetV2) (1.1k) | Neural, catches soft transitions that PySceneDetect misses |
| Shot boundaries (easy) | [Breakthrough/PySceneDetect](https://github.com/Breakthrough/PySceneDetect) (5.2k) | CPU, pip install, good enough for hard cuts |
| Style understanding | ghost-editor (reverse-engineers a reference edit), krusemediallc `reel-style-clone` | Turns "edit it like this reel" into a written style guide |

## 3. Audio analysis

| Job | Winner | Compared against | Notes |
|---|---|---|---|
| Transcription (paid) | ElevenLabs Scribe | Default in video-use and Nate's kit | Word timestamps, diarization and audio events in one call |
| Transcription (local) | [m-bain/whisperX](https://github.com/m-bain/whisperX) (24.5k) | [faster-whisper](https://github.com/SYSTRAN/faster-whisper) (25.8k), [whisper.cpp](https://github.com/ggml-org/whisper.cpp) (54.4k), [Qwen3-ASR](https://github.com/QwenLM/Qwen3-ASR) (3.7k), [parakeet-mlx](https://github.com/senstella/parakeet-mlx) (Mac) | WhisperX has forced alignment, so word timings are tight enough to cut on. whisper.cpp wins on CPU and Mac. |
| Fillers, stutters | [nyrahealth/CrisperWhisper](https://github.com/nyrahealth/CrisperWhisper) (1.4k) | Vanilla Whisper | Important: normal Whisper quietly drops "um", "uh" and stutters, so filler detection fails. CrisperWhisper transcribes them verbatim with timestamps. |
| Voice activity | [snakers4/silero-vad](https://github.com/snakers4/silero-vad) (10.4k) | ffmpeg `silencedetect` | Finds speech, not just loudness, so it isn't fooled by room noise |
| Speakers | [pyannote/pyannote-audio](https://github.com/pyannote/pyannote-audio) (10.6k) | | Standard for diarization |
| Music beats | [CPJKU/beat_this](https://github.com/CPJKU/beat_this) (420) | [librosa](https://github.com/librosa/librosa) (8.7k), [essentia](https://github.com/MTG/essentia) (3.8k) | beat_this is the most accurate beat and downbeat tracker. Use librosa for everything else (onsets, energy, RMS). |
| Loudness | [slhck/ffmpeg-normalize](https://github.com/slhck/ffmpeg-normalize) (1.5k) | | EBU R128. Target -14 LUFS for social. |
| Denoise | hassancs91 `clean-audio` (vendored) driving [DeepFilterNet](https://github.com/Rikorose/DeepFilterNet) (4.8k) or ElevenLabs Voice Isolator | [resemble-enhance](https://github.com/resemble-ai/resemble-enhance) (2.5k), [ClearerVoice-Studio](https://github.com/modelscope/ClearerVoice-Studio) (4.6k) | The skill diagnoses the noise type before picking a method |
| Stems | [nomadkaraoke/python-audio-separator](https://github.com/nomadkaraoke/python-audio-separator) (1.4k) | [demucs](https://github.com/facebookresearch/demucs) (10.4k, archived) | Pull music out from under voice |

## 4. Silence cutting and repetition removal

**Winner: Nate Herk's `cut-silences` + `cut-mistakes`** (vendored in `skills/02-full-edit-pipeline`)

It's transcript-driven and deterministic. Pauses get trimmed down to a natural breath instead of a hard zero gap. Every pass writes an EDL plus a retimed transcript that the next step reads. `cut-mistakes` sorts candidates into stutter, retake (by Jaccard similarity) and false start, and then makes you review them, because "never, never" said for emphasis looks exactly like a stutter.

| Tool | Method | Verdict |
|---|---|---|
| Nate's kit | Word-level transcript, EDL, review gate | Best quality. Built for agents. |
| [WyattBlue/auto-editor](https://github.com/WyattBlue/auto-editor) (5.5k) | Audio and motion thresholds | Best non-AI cutter. Exports Premiere, Resolve and FCP timelines, so use it when you finish in an NLE. |
| vincentventalon skill | Silence islands, whisper.cpp, keep the last take | Fastest fully-local one-command rough cut |
| video-use | Scribe transcript, filler words | Good, but tied to ElevenLabs |
| [lagmoellertim/unsilence](https://github.com/lagmoellertim/unsilence) (596), [carykh/jumpcutter](https://github.com/carykh/jumpcutter) (3.1k) | Volume threshold | Outdated. Skip. |

## 5. Planning the whole edit

**Winner: Nate's `video-storytelling` + `hyperframes-video-beats`** (vendored)

`video-storytelling` designs the visual layer as one persistent world the camera moves through, rather than a string of unrelated graphics. `video-beats` writes a beat sheet anchored to transcript words and validates sync with a script.

- [calesthio/OpenMontage](https://github.com/calesthio/OpenMontage) (67.9k, AGPL): research, proposal, script, scene plan, assets, edit, compose, with a checkpoint protocol between stages. Better for full productions like documentaries and explainers. Overkill for talking heads. In `clone-external.sh`.
- HyperFrames `hyperframes-creative` (vendored): design specs, palettes, typography, beat planning.

## 6. Rough cut and short-form cutaway

**Winner: Nate's `short-form-edit`** (vendored). Curiosity-led openings, earned payoffs, story-driven cuts, and validators for the footage and the plan.

| Option | Best for |
|---|---|
| Nate `short-form-edit` | Reels, Shorts and ads from talking-head footage |
| ghost-editor (vendored) | Vertical reels with face-safe captions and 7 styles |
| hassancs91 `clean-cut` (vendored) | Long-form YouTube master cut |
| [Anil-matcha/AI-Youtube-Shorts-Generator](https://github.com/Anil-matcha/AI-Youtube-Shorts-Generator) (5.3k) | Long video to many 9:16 clips (Opus Clip alternative) |
| [JayWebtech/autoshorts](https://github.com/JayWebtech/autoshorts) (1.2k) | Local desktop app for clipping with virality ranking |
| [kamilstanuch/Autocrop-vertical](https://github.com/kamilstanuch/Autocrop-vertical) (420) | YOLOv8 auto-reframe from 16:9 to 9:16 |

## 7. Air, fumble and repetition removal

Same engine as step 4. Ranked:

1. **Nate's `cut-mistakes`**: review-gated, keeps intentional emphasis.
2. **ghost-editor**: picks the best take of each sentence. Very good for phone-recorded reels with lots of retakes.
3. **vincentventalon**: keeps the last take of each repeated sentence. Simple heuristic, works most of the time.

Pair any of them with CrisperWhisper so "um", "uh" and half-words actually show up in the transcript.

## 8. Cut auditing

**Winner (design): [krusemediallc/video-editor-agent](https://github.com/krusemediallc/video-editor-agent) `video-qa`.** It has no license, so it's in `clone-external.sh` instead of vendored.

It runs four layers on the rendered file:

1. ffprobe/ffmpeg checks: black, frozen and flash frames, loudness, clipping.
2. Transcript edit-boundary checks mapped through the EDL: clipped words, duplicated dialogue at cuts.
3. An optional Gemini watch-and-listen pass.
4. Inspection packets for suspect timestamps (contact sheet, waveform, transcript).

Its `edl-tighten` skill is also the best tool for removing pauses from an already-finished cut without breaking caption or SFX sync.

Vendored alternatives:
- Nate's kit `scripts/qa-deadframe.mjs`, `qa-exposure.mjs`, `qa-legibility.mjs`, `qa-seamjump.mjs`, `qa-no-crossfade.mjs`, plus `VERIFY.md` per edit.
- video-use: after rendering, it runs `timeline_view` on every cut boundary, fixes and re-renders up to 3 times.

## 9. Geometry (protect face, hands, key areas)

**Winner: HyperFrames `embedded-captions` safe-zones** (vendored) for embedded text, and **ghost-editor `face_track.py`** (vendored) for reels.

- embedded-captions computes safe zones from scene palette and lighting. Its hard rule is that the face bbox must be at least 30% uncovered in every 0.3s window. It checks occlusion and overflow with `check-occlusion.cjs` and `check-overflow.cjs`.
- ghost-editor tracks the face, so captions and cards never cover it and stay inside the platform UI safe area.
- **Gap:** none of these protect hands. Add [google-ai-edge/mediapipe](https://github.com/google-ai-edge/mediapipe) (37.3k) Hand Landmarker for hands, and use [ultralytics](https://github.com/ultralytics/ultralytics) (62.5k) to detect products and objects. [insightface](https://github.com/deepinsight/insightface) (29.9k) is heavier and only needed for face identity.

## 10. Capturing and recording

| Need | Winner | Alternatives |
|---|---|---|
| Screenshot of an article or webpage | [simonw/shot-scraper](https://github.com/simonw/shot-scraper) (2.6k): full-page, CSS selector, JS before capture | [microsoft/playwright-mcp](https://github.com/microsoft/playwright-mcp) (38.1k), [chrome-devtools-mcp](https://github.com/ChromeDevTools/chrome-devtools-mcp) (53.5k) for agent-driven browsing |
| Scripted screen recording of a site | digitalsamba `playwright-recording` (vendored) | krusemediallc `broll-capture` (best design: screenshots, smooth scroll recordings, Screen Studio fallback for sites that block bots; unlicensed) |
| Screen recording without a live site | hassancs91 `fake-screencast` (vendored): screenshots become a simulated recording with an animated cursor | |
| Recording your own screen | [CapSoftware/Cap](https://github.com/CapSoftware/Cap) (23.3k), an open-source Loom | OBS + [obs-websocket](https://github.com/obsproject/obs-websocket) (4.4k) for agent-triggered recording |
| Grabbing online video | [yt-dlp](https://github.com/yt-dlp/yt-dlp) | [imputnet/cobalt](https://github.com/imputnet/cobalt) (44.9k) |
| Stock images, icons, logos, BGM | HyperFrames `media-use` (vendored) resolves them into frozen local files | |

## 11. B-roll understanding and tagging

This is the weakest category. No mature agent skill indexes your whole footage library yet. Best available:

| Option | Type | Verdict |
|---|---|---|
| [video-db/skills](https://github.com/video-db/skills) (128, MIT) | Hosted ingest, understand, search, edit | Most complete for agents. Your footage goes to VideoDB's servers. |
| [6v17/VideoSeek](https://github.com/6v17/VideoSeek) (~90) | Local, SigLIP2 embeddings, search by sentence, tag, screenshot or dialogue; exports Premiere XML and FCPXML | Best local option. Windows-first. |
| DIY | [Qwen3-VL-Embedding](https://github.com/QwenLM/Qwen3-VL-Embedding) (1.4k) or [open_clip](https://github.com/mlfoundations/open_clip) (14.2k) + PySceneDetect + LanceDB, with Gemini or Qwen3-VL writing tags per shot | Most control. You build the glue. |
| [rom1504/clip-retrieval](https://github.com/rom1504/clip-retrieval) (2.8k) | CLIP index and search | Solid base if you go DIY |

## 12. Gen video with Flow (Veo 3.1)

"Flow 3.1" is Veo 3.1 running inside Google Flow.

**Winner: [GTAI-1/flow-mcp](https://github.com/GTAI-1/flow-mcp)** (136, no license, so it's in `clone-external.sh`). It drives Google Flow from Claude using your own Flow credits (50/day free on any Google account) through its own Chrome window, so you don't pay per-call API prices. It can also join clips and add narration with FFmpeg.

| Option | Verdict |
|---|---|
| flow-mcp | Exact match for Flow. Needs a desktop that stays awake. |
| Veo 3.1 API (Gemini API / Vertex), [GoogleCloudPlatform/genmedia-creative-studio](https://github.com/GoogleCloudPlatform/genmedia-creative-studio) (1.2k) | Official path. Pay per second. Scriptable. |
| [smixs/visual-skills](https://github.com/smixs/visual-skills) (513) | Prompt syntax skill for Veo 3.1, Kling, Seedance. Use it with either option. |
| [Wan-Video/Wan2.2](https://github.com/Wan-Video/Wan2.2) (17.9k), [Lightricks/LTX-2](https://github.com/Lightricks/LTX-2) (9.7k) via [ComfyUI](https://github.com/Comfy-Org/ComfyUI) (137k) | Free local generation if you have a GPU. Below Veo quality. |

## 13. Rotoscopy (elements behind you)

**Skill winner: HyperFrames `embedded-captions`** (vendored). It mattes the person, puts the peak word behind you, and keeps the rest of the captions in front. It refuses footage where the matte would flicker, such as fast handheld shots.

**Best quality engine pipeline: SAM 3 mask → MatAnyone 2 alpha.**

| Engine | Strength | Weakness |
|---|---|---|
| [facebookresearch/sam3](https://github.com/facebookresearch/sam3) (12.0k) / [sam2](https://github.com/facebookresearch/sam2) (20.0k) | Segments and tracks any object from a click or text prompt | The mask is binary, so hair edges are hard |
| [pq-yang/MatAnyone2](https://github.com/pq-yang/MatAnyone2) (907, CVPR 2026 highlight) | Hair-level alpha with temporal consistency, seeded from a first-frame mask | Needs a GPU. Slower. |
| [PeterL1n/RobustVideoMatting](https://github.com/PeterL1n/RobustVideoMatting) (9.6k) | Real-time, no mask needed | Edges are softer and less reliable |
| [nikopueringer/CorridorKey](https://github.com/nikopueringer/CorridorKey) (14.8k) | Best keyer if you shoot green screen | Green screen only |
| [danielgatis/rembg](https://github.com/danielgatis/rembg) (25.1k), [BiRefNet](https://github.com/ZhengPeng7/BiRefNet) (4.3k) | Stills and thumbnails | Not temporal |

## 14. Style, format and motion graphics kit

**Winner: Nate's `style-library`** (406 motion-graphics cards with `registry.json`) **+ HyperFrames registry blocks and `motion-graphics` skill** (both vendored).

HyperFrames vs Remotion:

| | [HyperFrames](https://github.com/heygen-com/hyperframes) (62.6k) | [Remotion](https://github.com/remotion-dev/remotion) (63.8k) + [skills](https://github.com/remotion-dev/skills) (5.1k) |
|---|---|---|
| Authoring | HTML + GSAP | React |
| License | Apache-2.0 | Free for individuals and companies of up to 3 people, paid above that |
| Agent fit | Built for agents (lint, preview frames, registry) | Excellent official skills |
| Ecosystem in skills | Most new editing skills in 2026 target it | Larger older ecosystem |

Pick HyperFrames. Use Remotion only if you already work in React.

More motion kits:
- [heygen-com/hyperframes-launches](https://github.com/heygen-com/hyperframes-launches) (596): HeyGen's real launch-video compositions.
- [diffusionstudio/lottie](https://github.com/diffusionstudio/lottie) (5.6k): generates Lottie animations.
- [vibe-motion/skills](https://github.com/vibe-motion/skills) (1.3k) and [iart-ai/motion-skills](https://github.com/iart-ai/motion-skills) (799): motion design skill packs.
- [motion-canvas](https://github.com/motion-canvas/motion-canvas) (19.3k), [theatre-js](https://github.com/theatre-js/theatre) (12.8k): for hand-built animation.

## 15. Captions

**Winner: HyperFrames `embedded-captions`** (vendored). It has 35 caption identities. Most text runs on a verbatim lower-third "rail", and the peak word is embedded behind the subject. It's face-safe, refuses to caption Whisper hallucinations over silence, and composites preview frames in about 2 seconds so you can check before a full render.

| Option | Verdict |
|---|---|
| embedded-captions | Best looking and best guarded |
| ghost-editor | Word-timed, face-safe captions for reels |
| remotion-dev/skills `remotion-captions` | Best if you're on Remotion |
| [francozanardi/pycaps](https://github.com/francozanardi/pycaps) (224) | CSS-styled animated captions in plain Python |
| [6missedcalls/video-editing-skill](https://github.com/6missedcalls/video-editing-skill) (42) | Hormozi-style captions in Bash, FFmpeg and Whisper |
| [smacke/ffsubsync](https://github.com/smacke/ffsubsync) (7.9k) | Fixes the sync of existing SRT files |

## 16. Sound effects

**Winner: hassancs91 `suggest-sfx`** (vendored). It analyzes beats and narration, proposes SFX cues in a declarative `sfx-plan.json`, draws from a shared library that grows over time, and renders an audition mix. HyperFrames `media-use` (vendored) resolves SFX and BGM into local files.

| Option | Verdict |
|---|---|
| suggest-sfx | Best workflow. Beat-synced, review-first. |
| krusemediallc `sound-design` | Best mix recipe: generates ElevenLabs SFX, drops the third that come out near-silent, peak-normalizes to -3dB, and matches the music bed to a reference by BPM. Unlicensed. |
| [hkchengrex/MMAudio](https://github.com/hkchengrex/MMAudio) (2.3k) | Best open video-to-audio model. Generates Foley that matches the picture. |
| [HunyuanVideo-Foley](https://github.com/Tencent-Hunyuan/HunyuanVideo-Foley) (1.1k), [ThinkSound](https://github.com/QwenAudio/ThinkSound) (1.4k) | MMAudio alternatives |

SFX libraries:

| Library | License | Notes |
|---|---|---|
| Sonniss GDC Game Audio Bundle | Royalty-free, commercial OK | Free yearly release, tens of GB of pro SFX |
| Freesound (API) | Per sound: CC0, CC-BY, CC-BY-NC | Huge, so filter by license |
| Kenney audio packs | CC0 | UI clicks, pops, interface sounds |
| ElevenLabs SFX | Commercial use on paid plans | Generate exactly the whoosh you need |
| BBC Sound Effects | RemArc, **non-commercial only** | Don't use it in client work |

## 17. Render

**Winner: HyperFrames CLI** (`hyperframes lint / preview / render`, vendored skills) for compositions, and **FFmpeg** for final assembly and encoding.

| Option | Verdict |
|---|---|
| HyperFrames | Deterministic HTML to MP4, built for agents |
| [Remotion](https://github.com/remotion-dev/remotion) | Strong. Lambda rendering scales. License caveat. |
| [FFmpeg](https://github.com/FFmpeg/FFmpeg) | Always the last step: concat, loudnorm, encode |
| [moviepy](https://github.com/Zulko/moviepy) (15k), [editly](https://github.com/mifi/editly) (5.5k) | Fine for simple programmatic edits |
| [mifi/lossless-cut](https://github.com/mifi/lossless-cut) (44.5k) | Trims without re-encoding, for raw footage prep |

## 18. Review gate

**Winner: krusemediallc `video-qa` + `video-review-canvas`** (clone script). Its rule is "verify pixels and dB, not intentions". The canvas is a frame.io-style review page with timestamped notes, version comparison and a beat map, and the agent reads your notes back before making the next cut.

Others:
- [OpenMontage](https://github.com/calesthio/OpenMontage) `skills/meta/reviewer.md` + `checkpoint-protocol.md` (AGPL): a gate between every stage, plus a post-render ffprobe, frame and audio-level review.
- Nate's kit: per-edit `VERIFY.md` and QA scripts (vendored).
- [Netflix/vmaf](https://github.com/Netflix/vmaf) (5.5k): checks encode quality, so you know a final export didn't degrade.

---

## All-in-one systems compared

| System | Stars | License | Best at | Skip if |
|---|---|---|---|---|
| [OpenMontage](https://github.com/calesthio/OpenMontage) | 67.9k | AGPL-3 | 12 production pipelines, 700+ skill files, widest scope | You only edit talking heads (too heavy) |
| [HyperFrames](https://github.com/heygen-com/hyperframes) | 62.6k | Apache-2 | Rendering and motion, with official skills | You need cutting logic (pair it with Nate's kit) |
| [video-use](https://github.com/browser-use/video-use) | 28.9k | MIT | Editing real footage by conversation | You can't use ElevenLabs |
| [hypit-ai/hypit](https://github.com/hypit-ai/hypit) | 21.9k | | Cloning viral video formats | |
| [FireRed-OpenStoryline](https://github.com/FireRedTeam/FireRed-OpenStoryline) | 3.5k | Apache-2 | Intent-driven editing through an MCP/web UI | Chinese-first docs |
| [chengfeng-videocut-skills](https://github.com/Agentchengfeng/chengfeng-videocut-skills) | 3.1k | Apache-2 | Very rigorous talking-head cutting (5-pass flub scan) | Chinese only |
| [veedstudio/open-edit](https://github.com/veedstudio/open-edit) | 1.6k | Apache-2 | Renders any HTML page frame-accurately, alpha output, measured cut points, VEED hand-off | You want no VEED account (rendering and cutting still work without one) |
| [nateherkai/hyperframes-student-kit](https://github.com/nateherkai/hyperframes-student-kit) | 1.4k | MIT | Talking-head to finished long and short form | |

**Recommended stack for a talking-head editor:** Nate's kit (cut, plan, motion) + HyperFrames `embedded-captions` (captions, roto, face safety) + hassancs91 `clean-audio` / `suggest-sfx` (audio) + krusemediallc `video-qa` (review) + flow-mcp (generated shots).

## Bridges to real editors (NLE)

| Tool | Stars | Use |
|---|---|---|
| [samuelgursky/davinci-resolve-mcp](https://github.com/samuelgursky/davinci-resolve-mcp) | 3.5k | Control DaVinci Resolve Studio from Claude |
| [hetpatel-11/Adobe_Premiere_Pro_MCP](https://github.com/hetpatel-11/Adobe_Premiere_Pro_MCP) | 680 | Premiere Pro via MCP |
| [AcademySoftwareFoundation/OpenTimelineIO](https://github.com/AcademySoftwareFoundation/OpenTimelineIO) | 2.0k | Timeline interchange format, so agent EDLs open in any NLE |
| auto-editor | 5.5k | Silence cut exported as a Premiere, Resolve or FCP timeline |
| open-edit `veed-project` / `veed-pull` | | Agent cut into VEED's editor as an editable project, and back |
| open-edit `render --transparent` | | ProRes 4444 alpha overlays for any NLE |
| krusemediallc `capcut-export` | | Hands the agent's cut off as a CapCut draft |

## Reference-style cloning (edit mine like this reel)

- krusemediallc `reel-style-clone`: frame-by-frame breakdown into a STYLE-GUIDE.md plus build directives.
- ghost-editor: reverse-engineers a reference edit and applies it.
- [edenfunf/reelmimic](https://github.com/edenfunf/reelmimic) (2.6k): generates new videos in a reference's style.

## Where to find more

- [zhuyansen/awesome-claude-video-skills](https://github.com/zhuyansen/awesome-claude-video-skills): 180 video skill repos, each security-graded. This is the best index.
- [heygen-com/hyperframes-community-skills](https://github.com/heygen-com/hyperframes-community-skills): community HyperFrames workflows.
- Creator-made kits worth watching: Nate Herk (YouTube), Hasan Aboul Hasan (YouTube), [Jakeschincariol/master-skills](https://github.com/Jakeschincariol/master-skills), [Melvynx/video-agent-skills](https://github.com/Melvynx/video-agent-skills).

## Install

```bash
# Standalone skills -> ~/.claude/skills (video-use, ghost-editor, rough cut, HyperFrames skills, digitalsamba skills)
./install-skills.sh

# Workspace kits: open Claude Code inside the folder, because their scripts use repo-relative paths
cd skills/02-full-edit-pipeline/nateherk-hyperframes-kit && npm install
cd skills/06-youtube-editor-audio-sfx/claude-youtube-editor && pip install -r requirements.txt

# Picks that can't be vendored (unlicensed, AGPL/GPL, or engines)
./clone-external.sh

# open-edit CLI (renderer, cut tools); the skill is in skills/08-render-any-html
npx --yes @veedstudio/openedit-cli init --workspace .
```

Most skills need `ffmpeg` and Node 22+. API keys are optional unless noted: ElevenLabs (video-use, Nate's default transcriber), Gemini (video-qa L3).

## License notes

- Everything under `skills/` is MIT or Apache-2.0 and keeps its upstream LICENSE.
- krusemediallc/video-editor-agent and GTAI-1/flow-mcp have **no license file**. You can use them, but you can't legally redistribute them, so they're clone-only.
- OpenMontage is AGPL-3 and video-analyzer-skill is GPL-3, so they're clone-only to keep this repo's licensing clean.
- Remotion requires a paid license for companies with more than 3 people.
