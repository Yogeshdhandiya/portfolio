# Job 3 plan (same reference as job 2; wide 4K park shot, so PRESCALE=1.8 and punch-in cuts on sentence boundaries)
# Job 2 plan (Minimal Clean style): camera, 1-2 word captions, condensed emphasis, white cutaway cards, blur dissolves, SFX.
import json, sys, re, os
import numpy as np

A = json.load(open("analysis.json"))
FPS = A["fps"]; F = A["frames"]; N = int(42.08 * FPS)
PRE = float(os.environ.get("PRESCALE", 1.2)); PW, PH = int(1080 * PRE) // 2 * 2, int(1920 * PRE) // 2 * 2
OW, OH = 1080, 1920
TX, TY = 540, 790
words = json.load(open(sys.argv[1]))["words"]

CUTS = [2.544, 6.048, 7.508, 9.74, 14.78, 16.38, 18.78, 23.33, 24.775, 26.92, 31.64, 33.18, 35.58, 38.86, 40.12]  # real: 2.544 6.048 7.508 24.775
fr = lambda t: int(round(t * FPS))
cut_f = [fr(t) for t in CUTS]
shots = list(zip([0] + cut_f, cut_f + [N]))
def ease(x):
    x = min(max(x, 0.0), 1.0); return 4 * x ** 3 if x < 0.5 else 1 - (-2 * x + 2) ** 3 / 2

# white cutaway cards (blur-dissolve in/out)
CARDS = [
    {"type": "stack", "a": 11.02, "b": 14.78},
    {"type": "stack2", "a": 21.10, "b": 23.33},
    {"type": "rows",  "a": 27.90, "b": 31.64},
    {"type": "dm",    "a": 36.52, "b": 38.86},
]
DIS = 0.20  # dissolve length

# camera: alternate wide/tight on every cut, strong slow push inside shots, hook settles from tight
cam = []
for si, (a, b) in enumerate(shots):
    fc = [F[i]["face"] for i in range(a, b) if "face" in F[i]]
    cx, cy = float(np.median([f["cx"] for f in fc])), float(np.median([f["cy"] for f in fc]))
    t0, t1 = a / FPS, b / FPS
    base = 1.72 if si % 2 == 0 else 1.28
    for i in range(a, b):
        t = i / FPS
        z = base + 0.06 * (t - t0) / max(t1 - t0, 1e-6)
        if si == 0: z = 2.05 + (1.66 - 2.05) * ease(t / 0.9) + 0.05 * t / t1
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
    (0.00, 2.70, (0.00, 1.00), "$89", 1.04, (1.70, 2.60)),
    (3.76, 6.04, (3.76, 5.00), "$2,500", 5.04, None),
    (6.24, 7.508, (6.24, 6.63), "SKILL", 6.64, (7.00, 7.50)),
    (8.64, 9.74, (8.64, 8.95), "VIDEO EDITOR", 8.96, None),
    (16.40, 17.80, (16.40, 16.90), "EDITING", 16.96, (17.30, 17.80)),
    (18.80, 21.10, (18.80, 19.50), "ENTIRE CONTENT SYSTEM", 19.52, None),
    (23.33, 24.775, (23.33, 23.99), "JUST THE OUTPUT", 24.00, None),
    (31.68, 33.15, (31.68, 32.20), "SAME PERSON", 32.24, None),
    (33.20, 35.55, (33.20, 33.70), "OFFER", 33.76, (34.30, 35.55)),
    (35.60, 36.52, (35.60, 35.95), "POSITIONING", 36.00, None),
    (38.88, 40.12, (38.88, 39.60), "TIME.", 39.68, None),
    (40.16, 42.08, (40.16, 41.00), "CHANGES THE BUSINESS", 41.04, None),
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
    "stack": {"items": [["BRIEFS", 11.12], ["EDITS", 12.32], ["REVISIONS", 13.52]]},
    "stack2": {"type": "stack", "items": [["STRATEGIES", 21.20], ["HOOKS", 21.92], ["CALENDAR", 22.40]]},
    "rows": {"rows": [{"lead": [[w["start"], w["text"].lower()] for w in ws(27.95, 28.80)], "big": "MINUTES", "big_t": 28.88},
                      {"lead": [[w["start"], w["text"].lower()] for w in ws(29.70, 30.90)], "big": "OUTCOMES", "big_t": 30.96}]},
    "dm": {"lead": [[w["start"], w["text"].lower()] for w in ws(36.55, 37.50)], "typing_t": 36.95, "msg_t": 37.52, "msg": "okay, $2,500 works 🤝"},
}
for c in CARDS: c.update(CARD_DATA[c["type"]])

SFX = [  # [t, file, dB relative to voice speech level, semitones, align]
    [5.04, "h_pop-reveal.mp3", -14, 0, "onset"],
    [CARDS[0]["a"], "h_whoosh-soft.mp3", -13, 0, "peak"],
    [CARDS[1]["a"], "whoosh-short.mp3", -14, -2, "peak"],
    [CARDS[2]["a"], "h_whoosh-soft.mp3", -13, 2, "peak"],
    [CARDS[3]["a"], "whoosh-short.mp3", -14, 0, "peak"],
    [37.52, "h_ui-send.mp3", -11, 0, "onset"],
]
plan = {"fps": FPS, "n": N, "cuts": CUTS, "zoom_transitions": [], "cam": cam, "cards": CARDS,
        "loop": {"a": 0, "b": 0, "items": []}, "phrases": phrases, "sfx": SFX, "music": "docu-pluck.mp3", "music_db": -15}
json.dump(plan, open("plan.json", "w"))
for p in phrases:
    print(f'{p["t0"]:6.2f}-{p["t1"]:6.2f} y={p["y"]} {p["style"]:5s} ' + " | ".join(l["kind"] + ":" + " ".join(w["text"] for w in l["words"]) for l in p["lines"]))
