# Fast person matte: u2net_human_seg (320px) + guided-filter edge refinement on the full-res frame.
# Usage: roto_fast.py <video> <out_dir> <u2net_human_seg.onnx> <t0:t1> [...]
# Writes out_dir/m_<frameindex>.png (grayscale, 540 wide, SOURCE frame space). Skips frames that already exist.
# About 1 s/frame on 2 CPU threads (BiRefNet-portrait looks better but takes 40 s to 4 min/frame on CPU).
import sys, os, json, subprocess, numpy as np, onnxruntime as ort, cv2

src, out, model = sys.argv[1], sys.argv[2], sys.argv[3]
ranges = [tuple(map(float, r.split(":"))) for r in sys.argv[4:]]
os.makedirs(out, exist_ok=True)
so = ort.SessionOptions(); so.intra_op_num_threads = 2
sess = ort.InferenceSession(model, so, providers=["CPUExecutionProvider"]); iname = sess.get_inputs()[0].name
pr = json.loads(subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height,r_frame_rate", "-of", "json", src]))["streams"][0]
n, d = map(int, pr["r_frame_rate"].split("/")); fps = n / d
GW, GH = 1080, int(1080 * pr["height"] / pr["width"])       # guide resolution
OW, OH = 540, int(540 * pr["height"] / pr["width"])
mean = np.array([0.485, 0.456, 0.406], np.float32); std = np.array([0.229, 0.224, 0.225], np.float32)

def guided(I, p, r, eps):
    mI = cv2.boxFilter(I, -1, (r, r)); mp = cv2.boxFilter(p, -1, (r, r))
    cov = cv2.boxFilter(I * p, -1, (r, r)) - mI * mp; var = cv2.boxFilter(I * I, -1, (r, r)) - mI * mI
    a = cov / (var + eps); b = mp - a * mI
    return cv2.boxFilter(a, -1, (r, r)) * I + cv2.boxFilter(b, -1, (r, r))

for t0, t1 in ranges:
    f0, f1 = int(round(t0 * fps)), int(round(t1 * fps))
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", f"{f0 / fps:.5f}", "-i", src, "-frames:v", str(max(f1 - f0, 1)), "-vf", f"scale={GW}:{GH}",
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    k = f0
    while True:
        buf = p.stdout.read(GW * GH * 3)
        if len(buf) < GW * GH * 3: break
        if os.path.exists(f"{out}/m_{k:05d}.png"): k += 1; continue
        img = np.frombuffer(buf, np.uint8).reshape(GH, GW, 3)
        x = (cv2.resize(img, (320, 320), interpolation=cv2.INTER_AREA).astype(np.float32) / 255 - mean) / std
        y = sess.run(None, {iname: x.transpose(2, 0, 1)[None]})[0][0, 0]
        y = (y - y.min()) / (y.max() - y.min() + 1e-6)
        m = cv2.resize(y, (GW, GH), interpolation=cv2.INTER_CUBIC).clip(0, 1).astype(np.float32)
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY).astype(np.float32) / 255
        m = guided(gray, m, 15, 1e-3); m = guided(gray, m, 5, 2e-4)
        m = np.clip((m - 0.08) / 0.84, 0, 1)
        cv2.imwrite(f"{out}/m_{k:05d}.png", (cv2.resize(m, (OW, OH), interpolation=cv2.INTER_AREA) * 255).astype(np.uint8))
        k += 1
    print("range", t0, t1, "done", flush=True)
