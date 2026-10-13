# QA gate: caption-vs-face collisions, horizontal centring, black/frozen frames, loudness, sync.
# Usage: qa.py <plan.json> <front.mov> <final.mp4>
import sys, json, subprocess, numpy as np, re
plan_p, front_p, final_p = sys.argv[1:4]
P = json.load(open(plan_p)); FPS = P["fps"]; OW, OH = 1080, 1920
blocks = [(c["a"], c["b"]) for c in P["cards"]] + [(P["loop"]["a"], P["loop"]["b"])]
inblock = lambda t: any(a <= t < b for a, b in blocks)
p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", front_p, "-vf", "scale=540:960", "-f", "rawvideo", "-pix_fmt", "rgba", "-"], stdout=subprocess.PIPE)
coll, offc, i = [], [], 0
while True:
    b = p.stdout.read(540 * 960 * 4)
    if len(b) < 540 * 960 * 4: break
    a = np.frombuffer(b, np.uint8).reshape(960, 540, 4)[..., 3] > 60
    t = i / FPS
    if not inblock(t) and a.any():
        fo = P["cam"][i].get("face_out")
        if fo:
            x0, y0, x1, y1 = [v // 2 for v in fo]
            # protect the face from brow to chin (exclude the hair band above the brow)
            y0 = y0 + int((y1 - y0) * 0.28)
            reg = a[max(y0, 0):max(y1, 0), max(x0, 0):max(x1, 0)]
            if reg.size and reg.mean() > 0.003: coll.append((round(t, 2), round(float(reg.mean()) * 100, 2)))
        ys, xs = np.nonzero(a[600:])  # caption band only (below y=1200 in full res)
        if len(xs) > 200:
            cx = (xs.min() + xs.max()) / 2 * 2
            if abs(cx - 540) > 30: offc.append((round(t, 2), int(cx)))
    i += 1
print(f"frames checked: {i}")
print(f"caption/face collisions: {len(coll)} frames", coll[:20])
print(f"off-centre caption-band frames (>30px): {len(offc)}", offc[:20])
r = subprocess.run(["ffmpeg", "-hide_banner", "-i", final_p, "-vf", "blackdetect=d=0.08:pix_th=0.08,freezedetect=n=0.002:d=0.6", "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
print("black:", re.findall(r"black_start:[\d.]+ black_end:[\d.]+", r))
print("freeze:", re.findall(r"freeze_start: [\d.]+", r))
print("loudness:", re.findall(r"I:\s+(-?[\d.]+) LUFS", r)[-1:], "peak:", re.findall(r"Peak:\s+(-?[\d.]+) dBFS", r)[-1:])
pr = json.loads(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,duration,width,height,r_frame_rate", "-of", "json", final_p]))
print("streams:", [(s["codec_type"], s.get("width"), s.get("height"), s.get("duration")) for s in pr["streams"]])
