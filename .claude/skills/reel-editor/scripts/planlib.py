# Shared planner for Minimal Clean reels with on-screen motion graphics.
# A job's plan.py is a short spec (cuts, cards, emphasis, mg, sfx) that calls Job(...).build(...).
import json, re, os
import numpy as np

PRE = float(os.environ.get("PRESCALE", 1.2))
PW, PH = int(1080 * PRE) // 2 * 2, int(1920 * PRE) // 2 * 2
OW, OH, TX, TY = 1080, 1920, 540, 790
DIS = 0.20
TOP_SAFE = 150  # Instagram header
MG_H = {"hero": 330, "icons": 230, "ring": 340, "bars": 280, "follow": 150, "notif": 170, "counter": 290, "badge": 300}


def ease(x):
    x = min(max(x, 0.0), 1.0); return 4 * x ** 3 if x < 0.5 else 1 - (-2 * x + 2) ** 3 / 2


class Job:
    def __init__(self, analysis, words, end=None, fixes=None):
        A = json.load(open(analysis))
        self.FPS, self.F = A["fps"], A["frames"]
        self.N = min(int(end * self.FPS), len(self.F)) if end else len(self.F)
        self.W = json.load(open(words))["words"]
        for w in self.W:  # ASR fixes, keyed by rounded start time
            k = round(w["start"], 2)
            if fixes and k in fixes: w["text"] = fixes[k]
        self.W = [w for w in self.W if w["text"]]  # a fix of "" drops a fumbled word from the captions

    def fr(self, t): return int(round(t * self.FPS))
    def ws(self, t0, t1): return [w for w in self.W if t0 - 0.005 <= w["start"] < t1 - 0.005]
    def lw(self, t0, t1, strip=""): return [[w["start"], w["text"].lower().rstrip(strip)] for w in self.ws(t0, t1)]

    def build(self, cuts, cards, emph, mg, sfx, zooms=(1.06, 1.2), hook=(1.32, 1.06), push=0.05, lift=130,
              music="docu-pluck.mp3", music_db=-15, out="plan.json"):
        FPS, F, N = self.FPS, self.F, self.N
        cut_f = [self.fr(t) for t in cuts]
        shots = list(zip([0] + cut_f, cut_f + [N]))
        # MG headroom: ease the face down by `lift` px while a top graphic is up
        def lift_at(t):
            v = 0.0
            for m in mg:
                if m.get("place", "top") != "top": continue
                a, b = m["t0"] - 0.35, m["t1"] + 0.05
                if a <= t < m["t0"]: v = max(v, ease((t - a) / 0.35))
                elif m["t0"] <= t < m["t1"]: v = 1.0
                elif m["t1"] <= t < b + 0.3: v = max(v, 1 - ease((t - m["t1"]) / 0.35))
            return v * lift
        cam = []
        for si, (a, b) in enumerate(shots):
            fc = [F[i]["face"] for i in range(a, b) if "face" in F[i]] or [f["face"] for f in F if "face" in f]
            cx, cy = float(np.median([f["cx"] for f in fc])), float(np.median([f["cy"] for f in fc]))
            t0, t1 = a / FPS, b / FPS
            base = zooms[si % 2]
            for i in range(a, b):
                t = i / FPS
                z = base + push * (t - t0) / max(t1 - t0, 1e-6)
                if si == 0: z = hook[0] + (hook[1] - hook[0]) * ease(t / 0.9) + push * t / t1
                g = 0.0
                for c in cards:
                    if c["a"] - DIS <= t < c["a"]: g = max(g, (t - (c["a"] - DIS)) / DIS)
                    elif c["a"] <= t < c["b"]: g = 1.0
                    elif c["b"] <= t < c["b"] + DIS: g = max(g, 1 - (t - c["b"]) / DIS)
                cam.append({"i": i, "z": z, "cx": cx, "cy": cy, "blur": 0.0, "gblur": round(g, 3), "lift": lift_at(t)})
        def transform(c):
            k = (OW / PW) * c["z"]
            ax = min(max(c["cx"] * PW, TX / k), PW - (OW - TX) / k)
            ay = min(max(c["cy"] * PH, TY / k), PH - (OH - TY) / k)
            ay = max(ay - c["lift"] / k, TY / k)
            return k, ax, ay
        for c in cam:
            k, ax, ay = transform(c); c["k"], c["ax"], c["ay"] = k, ax, ay
            f = F[c["i"]].get("face")
            if f:
                o = lambda xn, yn: (k * (xn * PW - ax) + TX, k * (yn * PH - ay) + TY)
                x0, y0 = o(f["x0"], f["y0"]); x1, y1 = o(f["x1"], f["y1"])
                c["face_out"] = [round(x0), round(y0), round(x1), round(y1)]
                c["chin_out"] = round(o(f["cx"], f["chin"])[1])
        self.cam = cam
        in_card = lambda t: any(c["a"] - DIS / 2 <= t < c["b"] + 0.02 for c in cards)
        phrases = []
        for (t0, t1, lead, big, bt, tail) in emph:
            lines = []
            if lead: lines.append({"kind": "lead", "words": [{"t": w["start"], "text": w["text"].lower()} for w in self.ws(*lead)]})
            lines.append({"kind": "big", "words": [{"t": bt, "text": big}]})
            if tail: lines.append({"kind": "tail", "words": [{"t": w["start"], "text": w["text"].lower()} for w in self.ws(*tail)]})
            phrases.append({"t0": t0, "t1": t1, "style": "big", "lines": lines})
        covered = [(p["t0"], p["t1"]) for p in phrases]
        free = [w for w in self.W if w["start"] < N / FPS and not in_card(w["start"]) and not any(a - 0.01 <= w["start"] < b for a, b in covered)]
        chunks, i = [], 0
        while i < len(free):
            g = [free[i]]
            if i + 1 < len(free) and not re.search(r"[.,?!:]$", g[0]["text"]) and free[i + 1]["start"] - g[0]["end"] < 0.18 \
                    and len(g[0]["text"]) + len(free[i + 1]["text"]) <= 14:
                g.append(free[i + 1])
            chunks.append(g); i += len(g)
        for j, g in enumerate(chunks):
            t0 = g[0]["start"]
            nxt = chunks[j + 1][0]["start"] if j + 1 < len(chunks) else g[-1]["end"] + 0.5
            t1 = min(nxt, g[-1]["end"] + 0.45)
            for (a, b) in covered + [(c["a"] - DIS / 2, c["b"]) for c in cards]:
                if t0 < a < t1: t1 = a
            phrases.append({"t0": t0, "t1": t1, "style": "plain", "lines": [{"kind": "plain", "words": [{"t": t0, "text": " ".join(w["text"] for w in g).lower()}]}]})
        phrases.sort(key=lambda p: p["t0"])
        for p in phrases:
            i0, i1 = self.fr(p["t0"]), min(self.fr(p["t1"]) + 1, N)
            chins = [cam[i]["chin_out"] for i in range(i0, i1) if "chin_out" in cam[i]]
            p["y"] = int(min(max(max(chins) + 70 if chins else 1100, 1040), 1320))
        warn = []
        for m in mg:  # place each top graphic in the band between the IG header and the top of the head
            i0, i1 = self.fr(m["t0"]), min(self.fr(m["t1"]) + 1, N)
            tops = [cam[i]["face_out"][1] for i in range(i0, i1) if "face_out" in cam[i]]
            top = min(tops) if tops else 560
            h = MG_H.get(m["type"], 92 * len(m.get("items", [])) + 20)
            band = top - 24 - TOP_SAFE
            m["s"] = round(min(1.0, band / h), 3)
            m["y"] = int(TOP_SAFE + band / 2)
            if m["s"] < 0.7: warn.append(f'mg {m["type"]}@{m["t0"]}: scale {m["s"]} (head top {top})')
            for c in cards:
                if m["t0"] < c["b"] and m["t1"] > c["a"] - DIS: warn.append(f'mg {m["type"]}@{m["t0"]} overlaps card {c["type"]}@{c["a"]}')
        plan = {"fps": FPS, "n": N, "cuts": cuts, "zoom_transitions": [], "cam": cam, "cards": cards, "mg": mg,
                "loop": {"a": 0, "b": 0, "items": []}, "phrases": phrases, "sfx": sfx, "music": music, "music_db": music_db}
        json.dump(plan, open(out, "w"))
        for p in phrases:
            print(f'{p["t0"]:6.2f}-{p["t1"]:6.2f} y={p["y"]} ' + " | ".join(l["kind"] + ":" + " ".join(w["text"] for w in l["words"]) for l in p["lines"]))
        for m in mg: print(f'MG {m["type"]:8s} {m["t0"]:6.2f}-{m["t1"]:6.2f} y={m["y"]} s={m["s"]}')
        for w in warn: print("WARN", w)
        return plan
