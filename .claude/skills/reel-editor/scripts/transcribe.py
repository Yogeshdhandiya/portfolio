# Word-level transcript with Parakeet TDT (sherpa-onnx). Usage: transcribe.py in.wav out.json
import sys, json, soundfile as sf, sherpa_onnx, numpy as np
M = "/tmp/claude-0/-home-user-portfolio/63ef4ede-eb2d-5b20-8c31-3f23cb3d0e7c/scratchpad/models/sherpa-onnx-nemo-parakeet-tdt-0.6b-v2-int8/"
rec = sherpa_onnx.OfflineRecognizer.from_transducer(
    encoder=M+"encoder.int8.onnx", decoder=M+"decoder.int8.onnx", joiner=M+"joiner.int8.onnx",
    tokens=M+"tokens.txt", model_type="nemo_transducer", num_threads=4)
audio, sr = sf.read(sys.argv[1], dtype="float32")
CH = 20 * sr  # chunk on 20s windows with word timestamps offset
words = []
for off in range(0, len(audio), CH):
    s = rec.create_stream(); s.accept_waveform(sr, audio[off:off+CH]); rec.decode_stream(s)
    r = s.result; base = off / sr
    cur = None
    for tok, t in zip(r.tokens, r.timestamps):
        if tok.startswith((" ", "▁")) or cur is None:
            if cur: words.append(cur)
            cur = {"text": tok.lstrip(" ▁"), "start": round(base + t, 3)}
        else:
            cur["text"] += tok
        cur["end"] = round(base + t + 0.08, 3)
    if cur: words.append(cur)
words = [w for w in words if w["text"]]
for a, b in zip(words, words[1:]):
    a["end"] = min(max(a["end"], a["start"] + 0.05), b["start"])
json.dump({"words": words, "text": " ".join(w["text"] for w in words)}, open(sys.argv[2], "w"), indent=1)
print(" ".join(w["text"] for w in words))
