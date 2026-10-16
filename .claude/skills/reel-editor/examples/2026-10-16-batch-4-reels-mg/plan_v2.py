# Video 2: "your job is not to manage content" (single take, close-up at the desk, 67 s)
import sys; sys.path.insert(0, "/home/user/portfolio/.claude/skills/reel-editor/scripts")
from planlib import Job
J = Job("analysis.json", "src/src.words.json", end=66.85,
        fixes={31.52: "carousels,", 35.28: "", 35.44: "works.", 39.68: "", 40.08: "position", 60.24: "business."})
lw = J.lw
CUTS = [1.48, 3.32, 5.96, 7.62, 9.72, 11.96, 14.44, 16.84, 20.10, 21.42, 23.70, 29.88, 33.075, 35.80, 37.08, 39.0, 40.70,
        44.36, 47.24, 49.66, 52.38, 55.80, 60.70, 63.24, 64.64, 66.14]
CARDS = [
    {"type": "flow", "a": 23.70, "b": 29.88, "lead": [[23.76, "before and after the record button"]],
     "items": [["NICHE", "f:bullseye", 24.24], ["SCRIPT", "f:memo", 25.12], ["EXECUTION", "f:clapper_board", 26.48],
               ["POST-PRODUCTION", "f:film_frames", 27.28], ["EDITING", "f:laptop", 28.16], ["SOCIAL MEDIA", "f:mobile_phone", 28.72]]},
    {"type": "rows", "a": 55.80, "b": 60.70, "rows": [{"lead": lw(56.60, 57.27), "big": "EDITOR", "big_t": 57.28},
                                                    {"lead": lw(59.28, 60.20), "big": "BUSINESS", "big_t": 60.24}]},
    {"type": "dm", "a": 63.24, "b": 64.64, "lead": lw(63.28, 63.75), "typing_t": 63.40, "msg_t": 63.80, "msg": "SYSTEM 🚀"},
]
EMPH = [
    (0.00, 1.48, (0.00, 0.47), "FOUNDER OR COACH", 0.48, None),
    (1.52, 3.32, (1.52, 2.15), "NOT TO MANAGE CONTENT", 2.16, None),
    (9.76, 11.96, (9.76, 10.71), "FORGET WHO THEY ARE", 10.72, None),
    (12.00, 14.44, (12.00, 12.87), "SOLVE PROBLEMS", 12.88, (13.84, 14.44)),
    (14.48, 16.84, (14.96, 15.99), "STUCK IN BETWEEN", 16.00, None),
    (20.16, 21.40, (20.16, 20.95), "EASY", 20.96, None),
    (21.44, 23.66, (21.44, 22.63), "BEFORE AND AFTER", 22.64, None),
    (35.84, 37.08, (35.84, 36.15), "HELL LOT OF WORK", 36.16, None),
    (37.12, 39.00, (37.12, 38.07), "ALL BY YOURSELF", 38.08, None),
    (39.04, 40.70, (39.04, 39.43), "WORST POSITION EVER", 39.44, None),
    (44.40, 47.24, (44.40, 45.43), "WHOLE MESS", 45.44, (46.16, 47.24)),
    (47.28, 49.66, (47.28, 47.75), "AI CONTENT SYSTEM", 47.76, None),
    (52.40, 55.10, (52.40, 53.27), "FREEDOM", 53.28, (53.68, 55.10)),
    (60.72, 63.20, (60.72, 61.51), "SPREADING IT EVERYWHERE", 61.52, None),
    (64.66, 66.12, None, "FREE AUDIT", 64.72, (65.28, 66.05)),
    (66.16, 66.85, None, "FOLLOW FOR MORE", 66.16, None),
]
MG = [
    {"type": "chips", "t0": 4.20, "t1": 5.94, "items": [{"t": 4.32, "icon": "f:chart_increasing", "text": "scale the business"}, {"t": 5.28, "icon": "f:handshake", "text": "help your client"}]},
    {"type": "hero", "t0": 7.66, "t1": 9.66, "icon": "f:rocket", "label": "jump into content"},
    {"type": "chips", "t0": 16.92, "t1": 20.06, "items": [{"t": 17.04, "icon": "f:cross_mark", "text": "clients get no results"}, {"t": 18.56, "icon": "f:cross_mark", "text": "content isn't even good"}]},
    {"type": "hero", "t0": 20.20, "t1": 21.38, "icon": "f:movie_camera", "label": "the easy part"},
    {"type": "icons", "t0": 29.96, "t1": 33.98, "items": [{"t": 30.96, "icon": "f:clapper_board", "label": "reels"}, {"t": 31.52, "icon": "f:card_index_dividers", "label": "carousels"},
                                                       {"t": 32.16, "icon": "f:framed_picture", "label": "posts"}, {"t": 32.64, "icon": "f:mobile_phone", "label": "stories"}, {"t": 33.12, "icon": "l:youtube", "label": "long-form"}]},
    {"type": "hero", "t0": 34.10, "t1": 35.76, "icon": "f:chart_increasing", "label": "what works"},
    {"type": "counter", "t0": 40.76, "t1": 42.50, "tc": 41.04, "dur": 0.7, "from": 0, "to": 5, "suffix": " YEARS", "label": "in the industry"},
    {"type": "icons", "t0": 42.56, "t1": 44.34, "items": [{"t": 42.64, "icon": "f:artist_palette", "label": "design"}, {"t": 43.28, "icon": "f:robot", "label": "AI"}, {"t": 43.92, "icon": "f:clapper_board", "label": "content"}]},
    {"type": "hero", "t0": 47.30, "t1": 49.60, "icon": "f:robot"},
    {"type": "ring", "t0": 49.70, "t1": 52.34, "tc": 50.64, "value": 80, "label": "of the repetitive work"},
    {"type": "icons", "t0": 61.40, "t1": 63.02, "items": [{"t": 61.52, "icon": "l:instagram", "label": "instagram"}, {"t": 61.84, "icon": "l:youtube", "label": "youtube"},
                                                       {"t": 62.16, "icon": "l:tiktok", "label": "tiktok"}, {"t": 62.64, "icon": "l:x", "label": "x"}]},
    {"type": "follow", "t0": 64.74, "t1": 66.85, "tap": 66.18, "handle": "yog.visuals_", "sub": "AI content systems", "initials": "Y"},
]
SFX = [
    [4.32, "pop.mp3", -17, 0, "onset"], [5.28, "h_pop-reveal.mp3", -17, 2, "onset"],
    [7.70, "h_whoosh-soft.mp3", -17, 3, "peak"],
    [17.04, "h_pop-reveal.mp3", -17, -2, "onset"], [18.56, "pop.mp3", -17, -1, "onset"],
    [20.24, "h_pop-reveal.mp3", -16, 1, "onset"],
    [23.70, "h_whoosh-soft.mp3", -13, 0, "peak"],
    [30.96, "pop.mp3", -18, 0, "onset"], [32.16, "h_pop-reveal.mp3", -18, 3, "onset"], [33.12, "pop.mp3", -18, 4, "onset"],
    [34.12, "h_pop-reveal.mp3", -16, -2, "onset"],
    [41.04, "h_clock-tick-soft.mp3", -16, 0, "onset"],
    [42.64, "pop.mp3", -18, 1, "onset"], [43.92, "h_pop-reveal.mp3", -18, 3, "onset"],
    [47.32, "h_pop-reveal.mp3", -16, 0, "onset"],
    [50.64, "pop.mp3", -16, -2, "onset"],
    [55.80, "whoosh-short.mp3", -14, -2, "peak"],
    [61.52, "h_pop-reveal.mp3", -18, 2, "onset"], [62.64, "pop.mp3", -18, 4, "onset"],
    [63.24, "h_whoosh-soft.mp3", -14, 2, "peak"], [63.80, "h_ui-send.mp3", -12, 0, "onset"],
    [66.18, "pop.mp3", -14, 0, "onset"],
]
J.build(CUTS, CARDS, EMPH, MG, SFX, zooms=(1.2, 1.06), hook=(1.34, 1.06))
