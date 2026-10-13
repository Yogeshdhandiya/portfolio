# Index SFX/music files: duration, onset and peak time (so cues can be peak-aligned to cuts).
# Usage: index_audio.py <assets_dir>  -> <assets_dir>/audio_index.json
import subprocess, numpy as np, json, glob, os, sys
A = sys.argv[1]; out = {}
for f in sorted(glob.glob(f"{A}/sfx/*.mp3")) + sorted(glob.glob(f"{A}/music/*.mp3")):
    a = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-ac", "1", "-ar", "8000", "-f", "f32le", "-"], capture_output=True).stdout, np.float32)
    if len(a) < 100: continue
    rms = np.sqrt(np.convolve(a * a, np.ones(80) / 80, "same"))
    out[os.path.basename(f)] = {"dur": round(len(a) / 8000, 3), "peak": round(float(np.argmax(rms)) / 8000, 3),
                                "onset": round(float(np.argmax(rms > 0.1 * rms.max())) / 8000, 3), "peak_db": round(float(20 * np.log10(abs(a).max() + 1e-9)), 1)}
json.dump(out, open(f"{A}/audio_index.json", "w"), indent=0)
print(len(out), "audio files indexed")
