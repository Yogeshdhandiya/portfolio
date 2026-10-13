# Cinematic grade (reference "blue glow" look): purple-blue walls -> deep teal-blue, tamed saturation,
# warm bright skin, teal shadows / warm highlights, S-curve, vignette, fine grain.
# Colour math is baked once into a 7-bit 3D LUT (128^3), so a 1080x1920 frame grades in ~60 ms.
import numpy as np, cv2

def _colour(x):  # x: (...,3) float RGB 0..1
    hsv = cv2.cvtColor(x.reshape(-1, 1, 3).astype(np.float32), cv2.COLOR_RGB2HSV).reshape(x.shape)
    h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    blue = np.clip(1 - np.abs(h - 235) / 50, 0, 1) * np.clip(s * 1.6, 0, 1)
    skin = np.clip(1 - np.abs(((h + 180) % 360) - 203) / 28, 0, 1) * np.clip(s * 3, 0, 1)
    h = h - 30 * blue                                  # purple-blue -> teal-blue
    s = s * (0.95 - 0.12 * blue + 0.06 * skin)
    v = v * (1 - 0.42 * blue) * (1 + 0.07 * skin)      # deep dark walls, brighter skin
    hsv = np.stack([np.mod(h, 360), np.clip(s, 0, 1), np.clip(v, 0, 1)], -1)
    x = cv2.cvtColor(hsv.reshape(-1, 1, 3).astype(np.float32), cv2.COLOR_HSV2RGB).reshape(x.shape)
    y = (0.2126 * x[..., 0] + 0.7152 * x[..., 1] + 0.0722 * x[..., 2])[..., None]
    x = x + (1 - y) ** 2 * np.float32([-0.030, 0.014, 0.028]) + y ** 2 * np.float32([0.035, 0.010, -0.030])
    x = np.clip((x - 0.03) / 0.97, 0, 1)
    x = x + 0.20 * (x - 0.5) * (x * (1 - x)) * 4 * 0.5   # S-curve
    return np.clip(x, 0, 1)

_l = (np.arange(128, dtype=np.float32) * 2 + 1) / 255
_g = np.stack(np.meshgrid(_l, _l, _l, indexing="ij"), -1)          # r,g,b
LUT = (_colour(_g).reshape(-1, 3) * 255 + 0.5).astype(np.uint8)
_yy, _xx = np.mgrid[0:1920, 0:1080].astype(np.float32)
_r = np.sqrt(((_xx - 540) / 700) ** 2 + ((_yy - 860) / 1150) ** 2)
VIG = np.clip(1 - 0.45 * np.clip(_r - 0.45, 0, 1) ** 1.5, 0.58, 1).astype(np.float32)[..., None]
_rng = np.random.default_rng(7)
GRAIN = [_rng.normal(0, 2.6, (1920, 1080)).astype(np.float32)[..., None] for _ in range(6)]
_k = [0]

def grade(rgb_u8):
    q = rgb_u8 >> 1
    idx = (q[..., 0].astype(np.int32) << 14) | (q[..., 1].astype(np.int32) << 7) | q[..., 2]
    x = LUT[idx].astype(np.float32) * VIG + GRAIN[_k[0] % 6]; _k[0] += 1
    return np.clip(x + 0.5, 0, 255).astype(np.uint8)
