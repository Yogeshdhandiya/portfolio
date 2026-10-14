import os
# Per-frame analysis of a talking-head source: jump cuts, face box/chin, hand boxes.
# Usage: analyze.py <video> <out.json> <models_dir>
# Coordinates are normalized 0..1 in SOURCE frame space.
import sys, json, subprocess, numpy as np, mediapipe as mp
from mediapipe.tasks import python as mpt
from mediapipe.tasks.python import vision

src, out, M = sys.argv[1], sys.argv[2], sys.argv[3]
probe = json.loads(subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
        "stream=width,height,r_frame_rate,nb_frames", "-of", "json", src]))["streams"][0]
W, H = 540, int(540 * probe["height"] / probe["width"]) // 2 * 2
num, den = map(int, probe["r_frame_rate"].split("/")); fps = num / den
face = vision.FaceLandmarker.create_from_options(vision.FaceLandmarkerOptions(
    base_options=mpt.BaseOptions(model_asset_path=f"{M}/face_landmarker.task"), running_mode=vision.RunningMode.VIDEO, num_faces=1))
hand = vision.HandLandmarker.create_from_options(vision.HandLandmarkerOptions(
    base_options=mpt.BaseOptions(model_asset_path=f"{M}/hand_landmarker.task"), running_mode=vision.RunningMode.VIDEO, num_hands=2))
p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", src, "-vf", f"scale={W}:{H}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
# Wide shots: the face is too small at 540 px, so detect it on a high-res crop (FACE_CROP="x0,y0,x1,y1" normalised).
FC = [float(v) for v in os.environ["FACE_CROP"].split(",")] if os.environ.get("FACE_CROP") else None
if FC:
    CW = 640; CH = int(CW * (FC[3] - FC[1]) * probe["height"] / ((FC[2] - FC[0]) * probe["width"])) // 2 * 2
    pc = subprocess.Popen(["ffmpeg", "-v", "error", "-i", src, "-vf", f"crop=iw*{FC[2]-FC[0]}:ih*{FC[3]-FC[1]}:iw*{FC[0]}:ih*{FC[1]},scale={CW}:{CH}",
                           "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
frames, prev, i = [], None, 0
CHIN, FOREHEAD = 152, 10
while True:
    buf = p.stdout.read(W * H * 3)
    if len(buf) < W * H * 3: break
    img = np.frombuffer(buf, np.uint8).reshape(H, W, 3)
    ts = int(i * 1000 / fps)
    mi = mp.Image(image_format=mp.ImageFormat.SRGB, data=img)
    rec = {"i": i, "t": round(i / fps, 4)}
    if FC:
        cimg = np.frombuffer(pc.stdout.read(CW * CH * 3), np.uint8).reshape(CH, CW, 3)
        fr = face.detect_for_video(mp.Image(image_format=mp.ImageFormat.SRGB, data=cimg), ts)
    else:
        fr = face.detect_for_video(mi, ts)
    if fr.face_landmarks:
        lm = np.array([[l.x, l.y] for l in fr.face_landmarks[0]])
        if FC: lm = np.array([FC[0], FC[1]]) + lm * np.array([FC[2] - FC[0], FC[3] - FC[1]])
        x0, y0 = lm.min(0); x1, y1 = lm.max(0)
        h = y1 - y0
        rec["face"] = {"x0": float(x0), "y0": float(y0 - 0.35 * h), "x1": float(x1), "y1": float(y1),
                       "cx": float((x0 + x1) / 2), "cy": float((y0 + y1) / 2), "chin": float(lm[CHIN, 1]), "brow": float(lm[FOREHEAD, 1])}
    hr = hand.detect_for_video(mi, ts)
    rec["hands"] = []
    for hl in hr.hand_landmarks:
        a = np.array([[l.x, l.y] for l in hl])
        rec["hands"].append([float(v) for v in (*a.min(0), *a.max(0))])
    g = img[::4, ::4].mean(2)
    rec["diff"] = float(np.abs(g - prev).mean()) if prev is not None else 0.0
    prev = g
    frames.append(rec); i += 1
d = np.array([f["diff"] for f in frames])
med = np.median(d[1:]) + 1e-6
cuts = [frames[k]["t"] for k in range(1, len(frames)) if d[k] > max(6 * med, 4.0) and d[k] > 2.5 * max(d[k-1], d[min(k+1, len(d)-1)] if k+1 < len(d) else 0)]
json.dump({"fps": fps, "src_w": probe["width"], "src_h": probe["height"], "cuts": cuts, "frames": frames}, open(out, "w"))
print("frames", len(frames), "fps", round(fps, 3), "cuts", cuts)
print("face found", sum("face" in f for f in frames), "median diff", round(float(med), 2))
