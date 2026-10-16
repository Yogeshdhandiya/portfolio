# Style: "Minimal Clean" (reference: Meta contextual-targeting reel, snapgram gh58ifjfqtw9, 56 s)

Frame-level breakdown (8 fps sheets of the hook, white cards, emphasis words, profile card, ending + spectrogram).

## Global
- 9:16, 30 fps, -14.2 LUFS. Dark, neutral, desaturated talking head (black hoodie, dark slatted wall). The reference's own grade is cool-neutral and desaturated, but **don't copy it: use the blue-glow grade** (user-feedback rule 14).
- Camera: slow continuous push-in inside shots (about 4–6% per shot) plus a framing change on every jump cut. Opens tight and settles out on the first beat. No zoom-blur or RGB split.
- Sound: a quiet music bed (gaps between words sit about 2–6 dB under speech level, which means a bed or room tone is present). Almost no audible SFX.

## Captions
- **One or two words at a time**, replacing each other (no accumulating build). Lowercase, white, geometric sans (Poppins SemiBold look), small (about 48 px at 1080 wide), centred at chest/mic height (about 52–60% of the height), soft shadow. Quoted phrases keep their quotes ("targeting people").
- **Emphasis = big condensed uppercase** (Bebas Neue look, about 130–150 px, white on the talking head, black on white cards), entering with a heavy blur → sharp (about 0.25 s). A small lowercase lead line sits above it ("and so Meta had to / SHUT IT DOWN") and an optional small tail below builds word by word ("ONLY RELEVANT / to that audience").
- Emphasis roughly every 2–4 s.

## White cutaway cards (the signature element)
- Transition in: the talking head **blurs heavily, then cross-dissolves to pure white** (about 0.2 s). Out: white dissolves back through a blur into the talking head.
- Content builds in time with the words:
  - small black lowercase words appear one or two at a time ("a few" → "years ago" → "it's called...");
  - a brand logo blur-fades in (Meta), with a black condensed caption under it that updates per phrase ("GOT INTO" → "REALLY BIG TROUBLE");
  - a big black condensed headline reveals **letter by letter with blur** ("CONTEXTUAL / TARGETING"), with a small tail ("and it uses...");
  - UI mockups: testimonial/review cards (avatar, name, stars, quote) on white with soft shadow; an Instagram-style dark profile pill (avatar with gradient ring, follower counts) with a blue **Follow** button that flips to grey **Following**, and a red notification badge counting up.
- About 4–5 white segments per minute, 1–5 s each.

## On-screen motion graphics (added after rule 15)
Placed in the band between the Instagram header (y 150) and the top of the head; `planlib.py` computes `y`/`s` per graphic and lifts the face by 130 px while one is up.
- Look: white rounded tiles (radius 38) with soft dark shadows, Microsoft Fluent 3D emoji or brand logos (simple-icons, brand colours), Poppins labels with a dark text shadow, white pills for labels, accent `#FFC83D` (yellow) for progress fills and number badges (it pops against the blue-glow walls).
- Motion: pop with overshoot (scale 0.3-0.4 → 1, `eb`, 0.32-0.42 s), labels slide up 0.1 s later, items of a row arrive on their spoken word and the row re-centres as it grows, exits blur-fade in 0.18 s. Hero icons float (±6 px, ±2°).
- Types in `templates/mg.js`: `hero`, `icons`, `ring`, `counter`, `badge`, `bars`, `chips`, `notif`, `follow`; card types `grid`, `flow` (auto-sizes up to 6 nodes and fits labels).
- SFX for MGs: soft pops (pop.mp3 / h_pop-reveal.mp3 alternating, pitched up along a row) at -17/-18 dB, a tick for counters, ui-send for notifications and the follow tap. Never one pop per item on rows of 5: first, middle, last.
