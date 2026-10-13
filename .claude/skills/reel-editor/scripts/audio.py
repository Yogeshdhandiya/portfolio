# Sound design: cue sheet -> SFX stem, music bed ducked under voice, 2-pass loudnorm to -14 LUFS.
# Usage: audio.py <source_video> <plan.json> <assets_dir> <out_mix.wav>
import sys, json, subprocess, os
src, plan_p, A, out = sys.argv[1:5]
P = json.load(open(plan_p)); IDX = json.load(open(f"{A}/audio_index.json"))
DUR = P["n"] / P["fps"]
cues = []  # (time, file, gain_db, semitones, align)
def cue(t, f, g, st=0, align="onset"): cues.append((t, f, g, st, align))

# --- hook
cue(0.00, "h_whoosh-wind.mp3", -12)                       # eased pull-back
cue(P["roto"]["a"], "typing.mp3", -11, 0, "peak")          # "5 THINGS" types on behind the head
cue(P["roto"]["a"] + 0.55, "sparkle.mp3", -15)
for j, st in enumerate([0, 2, 4, 5, 7]):                   # centred tiles, rising pitch
    cue(P["tiles"]["a"] + j * P["tiles"]["dt"], "pop.mp3", -12, st)
# --- section cards: varied whoosh + impact layers, label click, soft exit swish
CARD_SFX = [("whoosh-cinematic.mp3", -7, 0, "impact-bass-1.mp3", -8),
            ("whoosh.mp3", -7, 0, "h_impact-deep-soft.mp3", -8),
            ("h_whoosh-wind.mp3", -7, 0, "h_launch-thump.mp3", -9),
            ("whoosh-short.mp3", -6, -2, "impact-bass-2.mp3", -11),
            ("h_whoosh-soft.mp3", -6, 0, "h_impact-soft.mp3", -8)]
for c, (wf, wg, wst, imf, img) in zip(P["cards"], CARD_SFX):
    cue(c["a"], wf, wg, wst, "peak")
    cue(c["a"], imf, img, 0, "peak" if imf == "impact-bass-2.mp3" else "onset")
    cue(c["a"] + 0.22, "h_ui-click-soft.mp3", -10)
for j, c in enumerate(P["cards"]):
    cue(c["b"], "h_whoosh-reverse.mp3" if j % 2 == 0 else "whoosh-short.mp3", -15, 3 if j % 2 else 0, "peak")
# --- zoom-blur transitions
for tc, st in zip(P["zoom_transitions"], [2, 0, -1]):
    cue(tc, "whoosh-short.mp3", -9, st, "peak")
# --- emphasis words, rotated by style so nothing repeats back to back
ROT = {"glow": [("sparkle.mp3", -16, 0), ("ping.mp3", -19, 0), ("h_chime-magic.mp3", -17, 0)],
       "gold": [("h_chime-reward.mp3", -16, 0), ("h_pop-reveal.mp3", -14, -2), ("sparkle.mp3", -17, 3), ("h_chime-reward.mp3", -16, 2)],
       "white": [("h_stamp-hit.mp3", -11, 0), ("h_knock-solid.mp3", -11, 0), ("impact-bass-1.mp3", -14, 2)],
       "scramble": [("glitch-3.mp3", -11, 0), ("h_glitch-zap.mp3", -10, 0)],
       "chip": [("pop.mp3", -10, 0), ("h_ui-toggle-on.mp3", -9, 0), ("pop.mp3", -10, 3)]}
used = {k: 0 for k in ROT}
for ph in P["phrases"]:
    st = ph["style"]
    if st not in ROT: continue
    em = [L for L in ph["lines"] if L["kind"] == "emph"]
    if not em: continue
    f, g, s = ROT[st][used[st] % len(ROT[st])]; used[st] += 1
    cue(em[0]["words"][0]["t"], f, g, s)
cue(26.86, "h_scan-hum.mp3", -20)                          # tension under the slow creep
# --- loop card
cue(P["loop"]["a"], "h_riser-soft.mp3", -9, 0, "peak")
for (txt, t), st in zip(P["loop"]["items"], [0, 3, 5, 8]):
    cue(t, "click.mp3", -11, st)
# --- CTA
cue(P["cards"][0]["a"] * 0 + 41.416, "whoosh-short.mp3", -9, 1, "peak")
cue(41.70, "impact-bass-2.mp3", -11, 0, "peak")
cue(41.70, "sparkle.mp3", -15, 2)

# build SFX stem
ins, fl = [], []
for n, (t, f, g, st, al) in enumerate(cues):
    meta = IDX[f]; off = meta["peak"] if al == "peak" else meta["onset"]
    start = max(0.0, t - off)
    ins += ["-i", f"{A}/sfx/{f}"]
    ch = f"[{n}:a]aformat=channel_layouts=stereo,aresample=48000"
    if st: ch += f",asetrate={48000 * 2 ** (st / 12):.1f},aresample=48000"
    if any(k in f for k in ("impact", "launch-thump", "stamp", "knock")):
        g -= 4; ch += f",afade=t=out:st={off + 0.35:.2f}:d=0.55"
    ch += f",volume={g}dB,adelay={int(start * 1000)}|{int(start * 1000)}[s{n}]"
    fl.append(ch)
fl.append("".join(f"[s{n}]" for n in range(len(cues))) + f"amix=inputs={len(cues)}:normalize=0,apad=whole_dur={DUR}[sfx]")
subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", ";".join(fl), "-map", "[sfx]", "-t", f"{DUR}", "-ar", "48000", "sfx_stem.wav"], check=True)
json.dump([dict(t=t, file=f, gain=g, semitones=st, align=al) for t, f, g, st, al in cues], open("sfx_cues.json", "w"), indent=0)

# voice + music (ducked) + sfx
MUSIC = f"{A}/music/tech-pulse.mp3"
F = ("[0:a]highpass=f=80,acompressor=threshold=-20dB:ratio=3:attack=5:release=120:makeup=3dB,asplit=2[v][vk];"
     f"[1:a]atrim=0:{DUR},afade=t=in:d=0.4,afade=t=out:st={DUR - 1.4}:d=1.4,volume=-17dB[m];"
     "[m][vk]sidechaincompress=threshold=0.03:ratio=5:attack=25:release=350[md];"
     "[2:a]volume=0dB[s];[v][md][s]amix=inputs=3:normalize=0:duration=first")
meas = subprocess.run(["ffmpeg", "-hide_banner", "-i", src, "-i", MUSIC, "-i", "sfx_stem.wav", "-filter_complex", F + ",loudnorm=I=-14:TP=-1:LRA=9:print_format=json", "-f", "null", "-"],
                      capture_output=True, text=True).stderr
j = json.loads(meas[meas.rindex("{"):meas.rindex("}") + 1])
ln = f"loudnorm=I=-14:TP=-1:LRA=9:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-i", MUSIC, "-i", "sfx_stem.wav", "-filter_complex", F + "," + ln, "-ar", "48000", "-c:a", "pcm_s16le", out], check=True)
print(len(cues), "cues ->", out)
