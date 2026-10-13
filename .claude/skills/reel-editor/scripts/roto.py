# Person matte (rotoscope) with BiRefNet-portrait via onnxruntime, memory-safe (arena off).
# Usage: roto.py <video> <out_dir> <birefnet.onnx> <t0:t1> [<t0:t1> ...]
# Writes out_dir/m_<frameindex>.png (grayscale, 540 wide, SOURCE frame space).
import sys, os, json, subprocess, numpy as np, onnxruntime as ort
from PIL import Image

src, out, model = sys.argv[1], sys.argv[2], sys.argv[3]
ranges = [tuple(map(float, r.split(":"))) for r in sys.argv[4:]]
os.makedirs(out, exist_ok=True)
so = ort.SessionOptions(); so.enable_cpu_mem_arena = False; so.enable_mem_pattern = False; so.intra_op_num_threads = 4
sess = ort.InferenceSession(model, so, providers=["CPUExecutionProvider"])
iname = sess.get_inputs()[0].name
pr = json.loads(subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height,r_frame_rate", "-of", "json", src]))["streams"][0]
n, d = map(int, pr["r_frame_rate"].split("/")); fps = n / d
OW, OH = 540, int(540 * pr["height"] / pr["width"])
mean = np.array([0.485, 0.456, 0.406], np.float32); std = np.array([0.229, 0.224, 0.225], np.float32)
for t0, t1 in ranges:
    f0, f1 = int(round(t0 * fps)), int(round(t1 * fps))
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", f"{f0 / fps:.5f}", "-i", src, "-frames:v", str(f1 - f0), "-vf", "scale=1024:1024",
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    k = f0
    while True:
        buf = p.stdout.read(1024 * 1024 * 3)
        if len(buf) < 1024 * 1024 * 3: break
        if os.path.exists(f"{out}/m_{k:05d}.png"): k += 1; continue
        x = (np.frombuffer(buf, np.uint8).reshape(1024, 1024, 3).astype(np.float32) / 255 - mean) / std
        y = sess.run(None, {iname: x.transpose(2, 0, 1)[None]})[0][0, 0]
        y = 1 / (1 + np.exp(-y)) if y.min() < 0 or y.max() > 1 else y
        Image.fromarray((np.clip(y, 0, 1) * 255).astype(np.uint8)).resize((OW, OH), Image.LANCZOS).save(f"{out}/m_{k:05d}.png")
        k += 1
        if k % 10 == 0: print("frame", k, flush=True)
    print("range", t0, t1, "done", flush=True)
