# v2 plan: camera moves, phrases (captions), cards, rotoscope text, SFX cues.
# Inputs: analysis.json (face track + cuts), words json. Output: plan.json
import json, sys, math
import numpy as np

A = json.load(open("analysis.json"))
FPS = A["fps"]; F = A["frames"]; N = len(F)
SW, SH = A["src_w"], A["src_h"]          # 2160x3840
PW, PH = 1296, 2304                      # pre-scaled source used by compose.py (1.2x output: near 1:1 warps, no aliasing)
OW, OH = 1080, 1920
TX, TY = 540, 790                        # where the face centre sits in the output
words = json.load(open(sys.argv[1]))["words"]

CUTS = [3.086, 5.005, 10.093, 12.054, 16.308, 18.811, 21.897, 24.441, 28.820, 31.865, 34.326, 35.661, 37.538, 41.416]
fr = lambda t: int(round(t * FPS))
cut_f = [fr(t) for t in CUTS]
shots = list(zip([0] + cut_f, cut_f + [N]))

def ease(x):  # cubic in-out
    x = min(max(x, 0.0), 1.0)
    return 4 * x ** 3 if x < 0.5 else 1 - (-2 * x + 2) ** 3 / 2
def eout(x):
    x = min(max(x, 0.0), 1.0); return 1 - (1 - x) ** 3

# ---- camera: (shot index) -> list of zoom keys (t, z, dur) ; first entry = base
CAM = {
    0:  [(0.0, 1.30, 0), (0.05, 1.08, 1.05)],                 # hook: tight -> eased pull back
    1:  [(4.45, 1.22, 0)],
    2:  [(5.005, 1.06, 0), (5.78, 1.16, 0.42), (8.68, 1.24, 0.30)],
    3:  [(11.55, 1.20, 0), (11.58, 1.30, 0.14)],                # "nothing." snap
    4:  [(12.054, 1.06, 0), (14.30, 1.18, 0.55)],
    5:  [(17.95, 1.20, 0)],
    6:  [(18.811, 1.06, 0), (19.26, 1.16, 0.45)],
    7:  [(23.35, 1.20, 0)],
    8:  [(24.441, 1.06, 0), (26.86, 1.24, 1.10)],               # slow creep into "get lost faster"
    9:  [(30.55, 1.20, 0), (31.42, 1.29, 0.14)],                # "bad." snap
    10: [(31.865, 1.06, 0), (33.18, 1.16, 0.45)],
    11: [(34.326, 1.20, 0)],
    12: [(35.661, 1.08, 0), (36.30, 1.18, 0.45)],
    13: [(37.538, 1.18, 0)],
    14: [(41.416, 1.06, 0), (41.45, 1.15, 2.0)],
}
DRIFT = 0.022                       # slow push inside every shot
ZOOM_T = [5.005, 24.441, 34.326]    # zoom-blur + RGB split transitions on these cuts

def face_med(a, b):
    fc = [F[i]["face"] for i in range(a, b) if "face" in F[i]]
    return (np.median([f["cx"] for f in fc]), np.median([f["cy"] for f in fc]))

cam = []
for si, (a, b) in enumerate(shots):
    cx, cy = face_med(a, b)
    keys = CAM[si]
    t0, t1 = a / FPS, b / FPS
    for i in range(a, b):
        t = i / FPS
        z = keys[0][1]
        for (kt, kz, kd) in keys[1:]:
            if t >= kt:
                z = z + (kz - z) * (ease((t - kt) / kd) if kd > 0 else 1)
        z += DRIFT * (t - t0) / max(t1 - t0, 1e-6)
        extra, blur = 1.0, 0.0
        for tc in ZOOM_T:
            if tc - 0.13 <= t < tc:
                p = (t - (tc - 0.13)) / 0.13; extra = 1 + 0.12 * p ** 2; blur = p
            elif tc <= t < tc + 0.18:
                p = (t - tc) / 0.18; extra = 1.12 - 0.12 * eout(p); blur = 1 - eout(p)
        cam.append({"i": i, "z": z * extra, "cx": float(cx), "cy": float(cy), "blur": round(blur, 3)})

def transform(i):
    c = cam[i]; k = (OW / PW) * c["z"]
    ax, ay = c["cx"] * PW, c["cy"] * PH
    # clamp so the crop stays inside the source
    ax = min(max(ax, (TX) / k), PW - (OW - TX) / k)
    ay = min(max(ay, (TY) / k), PH - (OH - TY) / k)
    return k, ax, ay
def to_out(i, xn, yn):
    k, ax, ay = transform(i)
    return k * (xn * PW - ax) + TX, k * (yn * PH - ay) + TY
for c in cam:
    k, ax, ay = transform(c["i"]); c["k"] = k; c["ax"] = ax; c["ay"] = ay
    f = F[c["i"]].get("face")
    if f:
        x0, y0 = to_out(c["i"], f["x0"], f["y0"]); x1, y1 = to_out(c["i"], f["x1"], f["y1"])
        c["face_out"] = [round(x0), round(y0), round(x1), round(y1)]
        c["chin_out"] = round(to_out(c["i"], f["cx"], f["chin"])[1])
        c["top_out"] = round(y0)

# ---- words (display fixes; audio untouched)
FIX = {(12.88, "or"): "audit", (13.12, "did"): None, (20.08, "Already"): "already"}
DROP = [(19.66, 20.07)]
W = []
for w in words:
    key = (round(w["start"], 2), w["text"])
    if key in FIX:
        if FIX[key] is None: continue
        w = dict(w, text=FIX[key])
    if any(a <= w["start"] <= b for a, b in DROP): continue
    W.append(w)
def ws(t0, t1):
    return [w for w in W if t0 - 0.005 <= w["start"] < t1 - 0.005]

# ---- cards (hard cut in on the jump cut)
CARDS = [
    {"n": "01", "label": "The Next Step", "img": "ladder_3d.png", "a": 3.086, "b": 4.45},
    {"n": "02", "label": "Busy ≠ Progress", "img": "hourglass_not_done_3d.png", "a": 10.093, "b": 11.55},
    {"n": "03", "label": "Another Skill?", "img": "toolbox_3d.png", "a": 16.308, "b": 17.95},
    {"n": "04", "label": "Bad Direction", "img": "compass_3d.png", "a": 21.897, "b": 23.35},
    {"n": "05", "label": "Version 1", "img": "construction_3d.png", "a": 28.820, "b": 30.55},
]
LOOP = {"a": 38.92, "b": 41.416, "items": [["Build", 38.96], ["Get Feedback", 39.36], ["Iterate", 40.48], ["Repeat", 41.04]]}

# ---- phrases: (t_start, t_end, lead_words_range, emph_range, tail_range, style)
# each range = (t0, t1) over word starts; style in plain|glow|gold|white|scramble|chip
P = [
    (0.00, 0.80, None, None, (0.00, 0.80), "plain"),
    (0.80, 1.20, None, None, (0.80, 1.20), "plain"),
    (1.84, 3.086, (1.84, 2.40), (2.40, 3.00), None, "gold"),             # before I started / FREELANCING
    (4.45, 5.005, None, None, (4.39, 5.00), "plain"),                     # the next step.
    (5.10, 5.76, None, None, (5.10, 5.76), "plain"),                      # When you're stuck,
    (5.76, 7.34, (5.76, 6.00), (6.00, 6.50), (6.50, 7.34), "glow"),       # pick the / SMALLEST THING / that can help you
    (7.34, 8.16, None, None, (7.34, 8.16), "plain"),                      # move forward
    (8.16, 9.20, (8.16, 8.70), (8.70, 9.10), None, "chip"),               # and get you / [feedback]
    (9.20, 10.093, None, None, (9.20, 10.09), "plain"),                   # and repeat the cycle.
    (11.55, 12.054, None, (11.55, 12.0), None, "white"),                  # NOTHING.
    (12.10, 12.86, None, None, (12.10, 12.86), "plain"),                  # At the end of the day,
    (12.86, 13.66, None, None, (12.86, 13.66), "plain"),                  # audit the task
    (13.66, 14.30, None, None, (13.66, 14.30), "plain"),                  # that you have done
    (14.30, 16.308, (14.30, 15.26), (15.26, 16.2), None, "gold"),         # and understand what / MOVES THE BUSINESS
    (17.95, 18.811, None, (17.95, 18.7), None, "scramble"),               # ANOTHER SKILL
    (18.80, 19.26, None, None, (18.80, 19.26), "plain"),                  # Try selling
    (19.26, 21.897, (19.26, 20.0), (20.0, 20.7), (20.7, 21.89), "gold"),  # the skill you / ALREADY HAVE / before moving to another.
    (23.35, 24.441, (22.40, 23.50), (23.50, 24.3), None, "glow"),         # cannot fix / BAD DIRECTION
    (24.441, 25.18, None, None, (24.44, 25.18), "plain"),                 # So if you don't
    (25.18, 26.06, None, None, (25.18, 26.06), "plain"),                  # know what you're building,
    (26.06, 26.86, None, None, (26.06, 26.86), "plain"),                  # AI will just
    (26.86, 28.82, (26.86, 27.40), (27.40, 28.7), None, "scramble"),      # help you / GET LOST FASTER
    (30.55, 31.865, (30.55, 31.40), (31.40, 31.8), None, "white"),        # will always be / BAD.
    (31.865, 32.62, None, None, (31.86, 32.62), "plain"),                 # Do not spend
    (32.62, 33.18, None, (32.62, 33.18), None, "chip"),                   # [three weeks]
    (33.18, 34.326, (33.18, 33.74), (33.74, 34.3), None, "gold"),         # making something / PERFECT,
    (34.326, 35.60, (34.30, 34.78), (34.78, 35.6), None, "chip"),         # put it in / [front of people]
    (35.60, 36.30, None, None, (35.60, 36.30), "plain"),                  # and understand
    (36.30, 37.538, (36.30, 37.10), (37.10, 37.5), None, "glow"),         # what needs to be / IMPROVED.
    (37.538, 38.92, (37.55, 38.20), (38.20, 38.9), None, "white"),        # And that's basically / THE WHOLE GAME
    (41.416, 42.0, (41.42, 41.70), (41.70, 42.0), None, "cta"),           # comment / "BUILD"
    (42.0, 42.55, None, None, (42.0, 42.55), "plain"),                    # and I'll give you
    (42.55, 43.63, None, None, (42.55, 43.63), "plain"),                  # my starting checklist.
]
FORCE_EMPH_TEXT = {11.55: "nothing.", 17.95: "another skill", 23.50: "bad direction", 41.70: "“BUILD”",
                   22.40: None}
phrases = []
for (t0, t1, lead, emph, tail, style) in P:
    ph = {"t0": t0, "t1": t1, "style": style, "lines": []}
    def wl(rng):
        return [{"t": max(w["start"], t0), "text": w["text"]} for w in ws(*rng)]
    if lead:
        L = wl(lead)
        if lead == (22.40, 23.50): L = [{"t": t0, "text": "cannot fix"}]
        if L: ph["lines"].append({"kind": "lead", "words": L})
    if emph:
        E = wl(emph)
        txt = FORCE_EMPH_TEXT.get(emph[0])
        if txt or not E:
            E = [{"t": max(t0, emph[0]), "text": txt}]
        else:
            E = [{"t": E[0]["t"], "text": " ".join(e["text"] for e in E)}]
        if style != "cta":
            E[0]["text"] = E[0]["text"].rstrip(",")
        ph["lines"].append({"kind": "emph", "words": E})
    if tail:
        T = wl(tail)
        if T: ph["lines"].append({"kind": "tail" if (lead or emph) else "plain", "words": T})
    # face-aware anchor: below the lowest chin during the phrase
    i0, i1 = fr(t0), min(fr(t1) + 1, N)
    chins = [cam[i]["chin_out"] for i in range(i0, i1) if "chin_out" in cam[i]]
    ph["y"] = int(min(max(max(chins) + 78 if chins else 1100, 1060), 1330))
    phrases.append(ph)

# blocks during which talking-head captions are hidden
def in_block(t):
    return any(c["a"] <= t < c["b"] for c in CARDS) or LOOP["a"] <= t < LOOP["b"]
for ph in phrases:
    assert not in_block(ph["t0"] + 0.01), ph

# ---- rotoscoped hook text (behind the head)
i_roto = range(fr(1.30), fr(3.08))
tops = [cam[i]["top_out"] for i in i_roto if "top_out" in cam[i]]
ROTO = {"text": "5 THINGS", "a": 1.30, "b": 3.086, "type_dt": 0.07, "y_bottom": int(np.median(tops) + 40)}

# ---- tiles (centred)
TILES = {"a": 1.62, "b": 3.086, "dt": 0.075, "y": None}
i_t = range(fr(1.62), fr(3.08))
TILES["y"] = int(max(ph["y"] for ph in phrases if ph["t0"] == 1.84) + 230)

plan = {"fps": FPS, "n": N, "cuts": CUTS, "zoom_transitions": ZOOM_T, "cam": cam, "cards": CARDS, "loop": LOOP,
        "phrases": phrases, "roto": ROTO, "tiles": TILES}
json.dump(plan, open("plan.json", "w"))
for ph in phrases:
    print(f'{ph["t0"]:6.2f}-{ph["t1"]:6.2f} y={ph["y"]} {ph["style"]:8s} ' + " | ".join(l["kind"] + ":" + " ".join(w["text"] for w in l["words"]) for l in ph["lines"]))
print("roto", ROTO, "tiles", TILES)
zs = [c["z"] for c in cam]; print("zoom range", round(min(zs), 3), round(max(zs), 3))
