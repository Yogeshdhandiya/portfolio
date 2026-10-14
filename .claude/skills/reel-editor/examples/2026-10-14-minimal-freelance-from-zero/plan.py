# Job 2 plan (Minimal Clean style): camera, 1-2 word captions, condensed emphasis, white cutaway cards, blur dissolves, SFX.
import json, sys, re
import numpy as np

A = json.load(open("analysis.json"))
FPS = A["fps"]; F = A["frames"]; N = len(F)
PW, PH = 1296, 2304
OW, OH = 1080, 1920
TX, TY = 540, 790
words = json.load(open(sys.argv[1]))["words"]

CUTS = [4.171, 6.089, 8.467, 9.76, 13.597, 16.85, 18.727, 19.978, 21.73, 22.356, 22.898, 23.607, 24.066, 26.36, 29.279]
fr = lambda t: int(round(t * FPS))
cut_f = [fr(t) for t in CUTS]
shots = list(zip([0] + cut_f, cut_f + [N]))
def ease(x):
    x = min(max(x, 0.0), 1.0); return 4 * x ** 3 if x < 0.5 else 1 - (-2 * x + 2) ** 3 / 2

# white cutaway cards (blur-dissolve in/out)
CARDS = [
    {"type": "week",    "a": 6.089,  "b": 8.467},
    {"type": "reviews", "a": 13.597, "b": 16.85},
    {"type": "stack",   "a": 21.73,  "b": 24.066},
    {"type": "dm",      "a": 28.30,  "b": 30.20},
]
DIS = 0.20  # dissolve length

# camera: alternate wide/tight on every cut, strong slow push inside shots, hook settles from tight
cam = []
for si, (a, b) in enumerate(shots):
    fc = [F[i]["face"] for i in range(a, b) if "face" in F[i]]
    cx, cy = float(np.median([f["cx"] for f in fc])), float(np.median([f["cy"] for f in fc]))
    t0, t1 = a / FPS, b / FPS
    base = 1.06 if si % 2 == 0 else 1.19
    for i in range(a, b):
        t = i / FPS
        z = base + 0.05 * (t - t0) / max(t1 - t0, 1e-6)
        if si == 0: z = 1.26 + (1.06 - 1.26) * ease(t / 0.9) + 0.05 * t / t1
        g = 0.0
        for c in CARDS:
            if c["a"] - DIS <= t < c["a"]: g = max(g, (t - (c["a"] - DIS)) / DIS)
            elif c["a"] <= t < c["b"]: g = 1.0
            elif c["b"] <= t < c["b"] + DIS: g = max(g, 1 - (t - c["b"]) / DIS)
        cam.append({"i": i, "z": z, "cx": cx, "cy": cy, "blur": 0.0, "gblur": round(g, 3)})

def transform(i):
    c = cam[i]; k = (OW / PW) * c["z"]
    ax = min(max(c["cx"] * PW, TX / k), PW - (OW - TX) / k)
    ay = min(max(c["cy"] * PH, TY / k), PH - (OH - TY) / k)
    return k, ax, ay
def to_out(i, xn, yn):
    k, ax, ay = transform(i); return k * (xn * PW - ax) + TX, k * (yn * PH - ay) + TY
for c in cam:
    k, ax, ay = transform(c["i"]); c["k"], c["ax"], c["ay"] = k, ax, ay
    f = F[c["i"]].get("face")
    if f:
        x0, y0 = to_out(c["i"], f["x0"], f["y0"]); x1, y1 = to_out(c["i"], f["x1"], f["y1"])
        c["face_out"] = [round(x0), round(y0), round(x1), round(y1)]
        c["chin_out"] = round(to_out(c["i"], f["cx"], f["chin"])[1])

W = [dict(w) for w in words]
def ws(t0, t1): return [w for w in W if t0 - 0.005 <= w["start"] < t1 - 0.005]
def in_card(t): return any(c["a"] - DIS / 2 <= t < c["b"] + 0.02 for c in CARDS)

# emphasis phrases on the talking head: (t0, t1, lead_range, BIG text, big_t, tail_range)
EMPH = [
    (1.92, 3.52, (1.92, 2.60), "NOT BUILD A BRAND", 2.64, None),
    (8.467, 9.36, None, "NOT STUDYING,", 8.48, None),
    (9.36, 9.76, None, "MAKING.", 9.36, None),
    (10.56, 11.76, (10.56, 11.10), "REAL PEOPLE", 11.12, None),
    (18.72, 19.978, (18.72, 19.50), "AN OFFER", 19.52, None),
    (19.99, 21.73, (19.99, 20.62), "THE WHOLE GAME", 20.64, (21.18, 21.73)),
    (24.10, 26.36, (24.10, 25.00), "FIRST FREELANCE BUSINESS", 25.04, None),
    (30.20, 30.78, None, "THAT'S IT.", 30.24, None),
]
phrases = []
for (t0, t1, lead, big, bt, tail) in EMPH:
    lines = []
    if lead: lines.append({"kind": "lead", "words": [{"t": w["start"], "text": w["text"].lower()} for w in ws(*lead)]})
    lines.append({"kind": "big", "words": [{"t": bt, "text": big}]})
    if tail: lines.append({"kind": "tail", "words": [{"t": w["start"], "text": w["text"].lower()} for w in ws(*tail)]})
    phrases.append({"t0": t0, "t1": t1, "style": "big", "lines": lines})
covered = [(p["t0"], p["t1"]) for p in phrases]
# plain 1-2 word chunks for everything else on the talking head
free = [w for w in W if not in_card(w["start"]) and not any(a - 0.01 <= w["start"] < b for a, b in covered)]
chunks, i = [], 0
while i < len(free):
    g = [free[i]]
    if i + 1 < len(free) and not re.search(r"[.,?!]$", g[0]["text"]) and free[i + 1]["start"] - g[0]["end"] < 0.18 \
            and len(g[0]["text"]) + len(free[i + 1]["text"]) <= 14:
        g.append(free[i + 1])
    chunks.append(g); i += len(g)
for j, g in enumerate(chunks):
    t0 = g[0]["start"]
    nxt = chunks[j + 1][0]["start"] if j + 1 < len(chunks) else g[-1]["end"] + 0.5
    t1 = min(nxt, g[-1]["end"] + 0.45)
    for (a, b) in covered + [(c["a"] - DIS / 2, c["b"]) for c in CARDS]:
        if t0 < a < t1: t1 = a
    phrases.append({"t0": t0, "t1": t1, "style": "plain", "lines": [{"kind": "plain", "words": [{"t": t0, "text": " ".join(w["text"] for w in g).lower()}]}]})
phrases.sort(key=lambda p: p["t0"])
for p in phrases:
    i0, i1 = fr(p["t0"]), min(fr(p["t1"]) + 1, N)
    chins = [cam[i]["chin_out"] for i in range(i0, i1) if "chin_out" in cam[i]]
    p["y"] = int(min(max(max(chins) + 70 if chins else 1100, 1040), 1300))

# white-card content timings
CARD_DATA = {
    "week": {"lead": [[w["start"], w["text"].lower()] for w in ws(6.10, 6.80)], "big": "FIRST WEEK", "big_t": 6.80,
             "tail": [[w["start"], w["text"].lower().rstrip(".")] for w in ws(7.5, 8.4)], "days_t0": 7.05, "days_t1": 8.25},
    "reviews": {"lead": [[w["start"], w["text"].lower().rstrip(",")] for w in ws(13.66, 14.6)], "cards_t": [14.16, 14.42],
                "big": "PROBLEMS", "big_t": 15.04, "tail": [[w["start"], w["text"].lower().rstrip(".")] for w in ws(15.7, 16.85)]},
    "stack": {"items": [["SKILL", 22.00], ["PROOF", 22.40], ["PROBLEM", 23.12], ["OFFER", 23.76]]},
    "dm": {"lead": [[w["start"], w["text"].lower().rstrip(",")] for w in ws(28.20, 29.2)], "typing_t": 28.62, "msg_t": 29.28,
           "msg": "can you do that for me? 🙏"},
}
for c in CARDS: c.update(CARD_DATA[c["type"]])

SFX = [  # [t, file, dB relative to voice speech level, semitones, align]
    [CARDS[0]["a"], "h_whoosh-soft.mp3", -13, 0, "peak"],
    [CARDS[1]["a"], "whoosh-short.mp3", -14, -2, "peak"],
    [CARDS[2]["a"], "h_whoosh-soft.mp3", -13, 2, "peak"],
    [CARDS[3]["a"], "whoosh-short.mp3", -14, 0, "peak"],
    [14.16, "h_page-flip.mp3", -15, 0, "onset"],
    [29.28, "h_ui-send.mp3", -11, 0, "onset"],
]
plan = {"fps": FPS, "n": N, "cuts": CUTS, "zoom_transitions": [], "cam": cam, "cards": CARDS,
        "loop": {"a": 0, "b": 0, "items": []}, "phrases": phrases, "sfx": SFX, "music": "docu-pluck.mp3", "music_db": -15}
json.dump(plan, open("plan.json", "w"))
for p in phrases:
    print(f'{p["t0"]:6.2f}-{p["t1"]:6.2f} y={p["y"]} {p["style"]:5s} ' + " | ".join(l["kind"] + ":" + " ".join(w["text"] for w in l["words"]) for l in p["lines"]))
