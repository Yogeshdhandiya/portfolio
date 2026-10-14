# Final compositor: face-anchored sub-pixel reframe + zoom-blur/RGB-split transitions + grade
# + rotoscoped "behind" layer + front overlay. Streams frames into ffmpeg (x264) with the audio mix.
# Usage: compose.py <source> <plan.json> <front.mov> <behind.mov> <matte_dir> <mix.wav> <out.mp4> [crf]
import sys, os, json, subprocess, numpy as np, cv2
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from grade import grade

src, plan_p, front_p, behind_p, matte_d, mix_p, out_p = sys.argv[1:8]
crf = sys.argv[8] if len(sys.argv) > 8 else "16"
P = json.load(open(plan_p)); FPS = P["fps"]; N = P["n"]
PRE = float(os.environ.get("PRESCALE", 1.2))  # raise for wide 4K sources so punch-ins up to PRE stay native
PW, PH, OW, OH, TX, TY = int(1080 * PRE) // 2 * 2, int(1920 * PRE) // 2 * 2, 1080, 1920, 540, 790
SRC_MATTE_W = 540  # matte pngs are 540 wide in source space

def reader(path, w, h, ch, vf=None):
    cmd = ["ffmpeg", "-v", "error", "-i", path] + (["-vf", vf] if vf else []) + ["-f", "rawvideo", "-pix_fmt", "rgb24" if ch == 3 else "rgba", "-"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=w * h * ch * 2)
    while True:
        b = p.stdout.read(w * h * ch)
        if len(b) < w * h * ch: return
        yield np.frombuffer(b, np.uint8).reshape(h, w, ch)

srcR = reader(src, PW, PH, 3, f"scale={PW}:{PH}:flags=lanczos")
frontR = reader(front_p, OW, OH, 4)
behindR = reader(behind_p, OW, OH, 4) if os.path.exists(behind_p) else iter(())
enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{OW}x{OH}", "-r", "24000/1001", "-i", "-",
                        "-i", mix_p, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "medium", "-crf", crf, "-pix_fmt", "yuv420p",
                        "-c:a", "aac", "-b:a", "320k", "-movflags", "+faststart", "-shortest", out_p], stdin=subprocess.PIPE)

# grade: gentle filmic S-curve, slightly lifted blacks, cooled shadows / warm highlights, vignette
x = np.arange(256) / 255.0
s = x + 0.10 * np.sin(2 * np.pi * (x - 0.5)) * -1 * 0.5  # mild S
s = 0.025 + 0.965 * np.clip(s, 0, 1)
lutR = np.clip((s + 0.015 * (x - 0.5)) * 255, 0, 255).astype(np.uint8)
lutG = np.clip(s * 255, 0, 255).astype(np.uint8)
lutB = np.clip((s - 0.012 * (x - 0.5)) * 255, 0, 255).astype(np.uint8)
LUT = np.dstack([lutR, lutG, lutB]).reshape(1, 256, 3)
yy, xx = np.mgrid[0:OH, 0:OW].astype(np.float32)
r = np.sqrt(((xx - OW / 2) / (OW * 0.62)) ** 2 + ((yy - OH * 0.45) / (OH * 0.62)) ** 2)
VIG = (1 - 0.28 * np.clip(r - 0.55, 0, 1) ** 1.6 / 0.45 ** 1.6).clip(0.7, 1).astype(np.float32)[..., None]

def warp(img, k, ax, ay, extra=1.0, interp=cv2.INTER_LINEAR):
    kk = k * extra
    M = np.float32([[kk, 0, TX - kk * ax], [0, kk, TY - kk * ay]])
    return cv2.warpAffine(img, M, (OW, OH), flags=interp, borderMode=cv2.BORDER_REFLECT101)

def comp(dst, rgba):
    a = rgba[..., 3]
    ys, xs = np.nonzero(a > 0)
    if len(ys) == 0: return dst
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    A = a[y0:y1, x0:x1, None].astype(np.float32) / 255
    d = dst[y0:y1, x0:x1].astype(np.float32)
    dst[y0:y1, x0:x1] = (rgba[y0:y1, x0:x1, :3].astype(np.float32) * A + d * (1 - A) + 0.5).astype(np.uint8)
    return dst

for i in range(N):
    f = next(srcR); fr = next(frontR, None); br = next(behindR, None)
    c = P["cam"][i]; k, ax, ay, blur = c["k"], c["ax"], c["ay"], c["blur"]
    if blur > 0.02:
        # radial zoom blur (average of slightly different zooms) + chromatic RGB split
        n = 7; acc = np.zeros((OH, OW, 3), np.float32)
        for j in range(n):
            acc += warp(f, k, ax, ay, 1 + 0.07 * blur * j / (n - 1))
        base = acc / n
        sp = 0.014 * blur
        rch = warp(f, k, ax, ay, 1 + sp)[..., 0].astype(np.float32)
        bch = warp(f, k, ax, ay, 1 - sp)[..., 2].astype(np.float32)
        base[..., 0] = base[..., 0] * 0.5 + rch * 0.5
        base[..., 2] = base[..., 2] * 0.5 + bch * 0.5
        base = np.clip(base, 0, 255).astype(np.uint8)
    else:
        base = warp(f, k, ax, ay)
    base = grade(base)
    gb = c.get("gblur", 0)
    if gb > 0.01:
        base = cv2.GaussianBlur(base, (0, 0), 2 + 30 * gb ** 1.4)
    if br is not None and br[..., 3].any():
        mp = f"{matte_d}/m_{i:05d}.png"
        if os.path.exists(mp):
            # temporal smoothing (0.25/0.5/0.25) against matte shimmer
            ms = [(cv2.imread(f"{matte_d}/m_{j:05d}.png", cv2.IMREAD_GRAYSCALE), w) for j, w in ((i - 1, .25), (i, .5), (i + 1, .25)) if os.path.exists(f"{matte_d}/m_{j:05d}.png")]
            m = (sum(a.astype(np.float32) * w for a, w in ms) / sum(w for _, w in ms)).astype(np.uint8)
            sc = PW / SRC_MATTE_W
            M = np.float32([[k * sc, 0, TX - k * ax], [0, k * sc, TY - k * ay]])
            m = cv2.warpAffine(m, M, (OW, OH), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE).astype(np.float32)[..., None] / 255
            under = comp(base.copy(), br)
            base = (base.astype(np.float32) * m + under.astype(np.float32) * (1 - m) + 0.5).astype(np.uint8)
        else:
            base = comp(base, br)
    if fr is not None:
        base = comp(base, fr)
    enc.stdin.write(base.tobytes())
    if i % 100 == 0: print("frame", i, flush=True)
enc.stdin.close(); enc.wait()
print("done", out_p)
