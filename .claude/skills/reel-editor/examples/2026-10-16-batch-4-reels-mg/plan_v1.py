# Video 1: "month of content on your hard drive" (single take, close-up at the desk)
import sys; sys.path.insert(0, "/home/user/portfolio/.claude/skills/reel-editor/scripts")
from planlib import Job
J = Job("analysis.json", "src/src.words.json", end=34.15, fixes={9.76: "clips."})
lw = J.lw
CUTS = [1.24, 4.02, 7.40, 9.98, 12.32, 14.28, 16.44, 19.98, 22.04, 24.82, 27.22, 29.96, 32.18, 33.0]
CARDS = [
    {"type": "grid", "a": 7.40, "b": 9.98, "lead": lw(7.40, 8.90), "big": "DOZENS OF CLIPS", "big_t": 8.96, "tiles_t0": 8.05, "tiles_t1": 9.45, "n": 12},
    {"type": "flow", "a": 16.44, "b": 19.98, "lead": [[16.48, "ai content system"]],
     "items": [["CREATE", "f:memo", 16.80], ["POST", "f:outbox_tray", 17.44], ["REPURPOSE", "f:recycling_symbol", 18.08], ["ANALYZE", "f:bar_chart", 19.04]]},
]
EMPH = [
    (0.00, 1.24, (0.00, 0.45), "FOUNDER", 0.48, (0.80, 1.24)),
    (2.16, 4.02, None, "A MONTH OF CONTENT", 2.20, (3.12, 3.98)),
    (10.40, 12.32, (10.40, 11.03), "GETTING THEM ALL OUT", 11.04, None),
    (14.32, 16.40, (14.32, 14.47), "AI-INTEGRATED", 14.48, (15.52, 16.40)),
    (22.08, 24.82, (22.08, 22.87), "FREEDOM", 22.88, (23.20, 24.82)),
    (24.88, 27.22, (24.88, 26.07), "ISN'T THE RIGHT ANSWER", 26.08, None),
    (27.28, 29.96, (27.28, 28.23), "WHAT YOU'RE CREATING", 28.24, (29.04, 29.96)),
    (32.24, 33.02, None, "FOLLOW ME", 32.24, (32.64, 33.02)),
]
MG = [
    {"type": "hero", "t0": 2.20, "t1": 3.98, "icon": "f:floppy_disk", "label": "sitting unused"},
    {"type": "icons", "t0": 4.10, "t1": 7.16, "items": [{"t": 4.24, "icon": "f:studio_microphone", "label": "podcast"}, {"t": 4.88, "icon": "l:youtube", "label": "youtube"},
                                                     {"t": 5.84, "icon": "f:telephone_receiver", "label": "client call"}, {"t": 6.72, "icon": "f:busts_in_silhouette", "label": "workshop"}]},
    {"type": "hero", "t0": 14.40, "t1": 16.20, "icon": "f:robot"},
    {"type": "ring", "t0": 20.05, "t1": 21.98, "tc": 20.32, "value": 80, "label": "of the repetitive work"},
    {"type": "bars", "t0": 24.90, "t1": 29.90, "rows": [{"t": 24.95, "label": "Create more content", "value": 34, "good": False},
                                                     {"t": 27.30, "label": "Get more out of it", "value": 94, "good": True}]},
    {"type": "follow", "t0": 30.40, "t1": 34.10, "tap": 32.28, "handle": "yog.visuals_", "sub": "AI content systems", "initials": "Y"},
]
SFX = [
    [2.20, "h_pop-reveal.mp3", -15, 0, "onset"],
    [4.24, "pop.mp3", -17, 0, "onset"], [4.88, "h_pop-reveal.mp3", -17, 2, "onset"], [5.84, "pop.mp3", -17, 2, "onset"], [6.72, "h_pop-reveal.mp3", -17, 4, "onset"],
    [7.40, "h_whoosh-soft.mp3", -13, 0, "peak"],
    [16.44, "whoosh-short.mp3", -14, -2, "peak"],
    [20.32, "h_pop-reveal.mp3", -15, -2, "onset"],
    [27.30, "h_whoosh-reverse.mp3", -16, 0, "peak"],
    [32.28, "h_ui-send.mp3", -12, 0, "onset"],
]
J.build(CUTS, CARDS, EMPH, MG, SFX, zooms=(1.2, 1.06), hook=(1.34, 1.06))
