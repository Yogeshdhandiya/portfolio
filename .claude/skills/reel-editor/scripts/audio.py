# Sound design: cue sheet -> SFX stem, music bed ducked under voice, 2-pass loudnorm to -14 LUFS.
# Usage: audio.py <source_video> <plan.json> <assets_dir> <out_mix.wav>
import sys, json, subprocess, os
src, plan_p, A, out = sys.argv[1:5]
P = json.load(open(plan_p)); IDX = json.load(open(f"{A}/audio_index.json"))
DUR = P["n"] / P["fps"]
cues = []  # (time, file, gain_db, semitones, align)
def cue(t, f, g, st=0, align="onset"): cues.append((t, f, g, st, align))

# --- SFX only on KEY moments (v3 rule: ~1 cue per 2.5 s, sitting well under the voice)
cue(P["roto"]["a"], "typing.mp3", -12, 0, "peak")                    # roto text types on
cue(P["tiles"]["a"], "pop.mp3", -13)                                  # tiles (one soft pop, not five)
CARD_W = [("whoosh.mp3", -1), ("whoosh.mp3", 0), ("h_whoosh-soft.mp3", 0), ("whoosh-short.mp3", -2), ("h_whoosh-wind.mp3", 0)]
for c, (wf, st) in zip(P["cards"], CARD_W):
    cue(c["a"], wf, -9, st, "peak")                                   # card in: whoosh only
cue(P["cards"][0]["a"], "h_impact-soft.mp3", -11)                     # one impact, first card only
for tc, st in zip(P["zoom_transitions"], [2, 0, -1]):
    cue(tc, "whoosh-short.mp3", -11, st, "peak")                      # zoom-blur cuts
chips = [ph for ph in P["phrases"] if ph["style"] == "chip"]
for ph, (f, st) in zip(chips, [("pop.mp3", 0), ("h_ui-toggle-on.mp3", 0), ("pop.mp3", 3)]):
    em = [L for L in ph["lines"] if L["kind"] == "emph"][0]
    cue(em["words"][0]["t"], f, -13, st)                              # chips
cue(27.40, "glitch-3.mp3", -13)                                       # "get lost faster" scramble
cue(P["loop"]["a"], "h_riser-soft.mp3", -12, 0, "peak")               # into the loop card
cue(41.70, "h_impact-deep-soft.mp3", -11)                       # CTA "BUILD"

# auto-level: each cue's loudest 0.4 s window lands at (voice speech level + rel_dB), rel_dB <= -9
import numpy as np
def _pcm(cmd): return np.frombuffer(subprocess.run(cmd, capture_output=True).stdout, np.float32)
def _peak_rms(a, w=6400):
    return max(20 * np.log10(np.sqrt(np.mean(a[i:i + w] ** 2)) + 1e-9) for i in range(0, max(len(a) - w, 1), w // 4))
_v = _pcm(["ffmpeg", "-v", "error", "-i", src, "-af", "highpass=f=80,acompressor=threshold=-20dB:ratio=3:attack=5:release=120:makeup=3dB", "-ac", "1", "-ar", "16000", "-f", "f32le", "-"])
_w = 6400; _vr = np.array([20 * np.log10(np.sqrt(np.mean(_v[i:i + _w] ** 2)) + 1e-9) for i in range(0, len(_v) - _w, _w)])
VOICE = float(np.median(_vr[_vr > -45]))
_pk = {}
for (t, f, g, st, al) in cues:
    if f not in _pk: _pk[f] = _peak_rms(_pcm(["ffmpeg", "-v", "error", "-i", f"{A}/sfx/{f}", "-ac", "1", "-ar", "16000", "-f", "f32le", "-"]))
cues = [(t, f, float(round(VOICE + g - float(_pk[f]), 1)), st, al) for (t, f, g, st, al) in cues]
print("voice speech level", round(VOICE, 1), "dB")

# build SFX stem
ins, fl = [], []
for n, (t, f, g, st, al) in enumerate(cues):
    meta = IDX[f]; off = meta["peak"] if al == "peak" else meta["onset"]
    start = max(0.0, t - off)
    ins += ["-i", f"{A}/sfx/{f}"]
    ch = f"[{n}:a]aformat=channel_layouts=stereo,aresample=48000"
    if st: ch += f",asetrate={48000 * 2 ** (st / 12):.1f},aresample=48000"
    if any(k in f for k in ("impact", "launch-thump", "stamp", "knock")):
        ch += f",afade=t=out:st={off + 0.35:.2f}:d=0.55"
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
