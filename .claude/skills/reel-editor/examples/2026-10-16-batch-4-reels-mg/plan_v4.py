# Video 4: "you don't need a bigger team, you need a better system" (close-up at the desk, 58 s)
import sys; sys.path.insert(0, "/home/user/portfolio/.claude/skills/reel-editor/scripts")
from planlib import Job
J = Job("analysis.json", "src/src.words.json", end=58.50,
        fixes={20.24: "help", 39.44: "experience", 40.24: "becomes", 58.08: "bye-bye."})
lw = J.lw
CUTS = [1.18, 3.98, 6.52, 8.70, 10.54, 13.00, 16.90, 19.18, 22.44, 24.30, 26.70, 30.00, 30.70, 33.18, 38.62, 41.08, 43.58,
        46.62, 49.66, 52.04, 54.38, 56.14, 58.10]
CARDS = [
    {"type": "rows", "a": 3.98, "b": 6.52, "rows": [{"lead": lw(4.00, 4.79), "big": "BIGGER TEAM", "big_t": 4.80},
                                                  {"lead": lw(5.44, 6.15), "big": "BETTER SYSTEM", "big_t": 6.16}]},
    {"type": "flow", "a": 13.00, "b": 16.90, "lead": [[13.04, "what the system does"]],
     "items": [["CREATE", "f:memo", 13.60], ["EDIT", "f:clapper_board", 14.24], ["REPURPOSE", "f:recycling_symbol", 15.28], ["SCHEDULE", "f:spiral_calendar", 16.32]]},
    {"type": "flow", "a": 33.18, "b": 38.62, "lead": [[33.20, "the decisions i still make"]],
     "items": [["WHAT TO POST?", "f:thinking_face", 33.20], ["WORTH IT?", "f:gem_stone", 34.64], ["SOUNDS LIKE THEM?", "f:speech_balloon", 36.48]]},
]
EMPH = [
    (0.00, 1.18, (0.00, 0.39), "FOUNDER", 0.40, (0.64, 1.18)),
    (1.20, 3.96, (1.20, 1.75), "MANAGING CONTENT", 1.76, (2.96, 3.96)),
    (7.68, 10.52, (7.68, 8.71), "AI CONTENT SYSTEM", 8.72, None),
    (10.56, 13.00, (10.56, 12.23), "REPETITIVE WORK", 12.24, None),
    (22.48, 24.30, (22.48, 22.87), "HIGH LEVERAGE", 22.88, (23.52, 24.30)),
    (24.32, 26.70, (24.32, 25.67), "CONTENT ANYMORE", 25.68, None),
    (26.72, 27.66, (26.72, 27.03), "CREATE", 27.04, None),
    (30.00, 30.70, None, "BUT GUESS WHAT?", 30.00, None),
    (30.72, 33.16, (30.72, 31.51), "MOST IMPORTANT DECISIONS", 31.52, None),
    (38.64, 41.08, (38.64, 39.43), "EXPERIENCE", 39.44, (40.24, 41.08)),
    (43.60, 46.62, (43.60, 44.95), "GUIDE AI", 44.96, (45.68, 46.62)),
    (46.64, 49.66, (46.64, 47.99), "FOCUS", 48.00, (48.40, 49.66)),
    (52.08, 54.38, (52.08, 53.27), "COMPLETELY OFF THEIR PLATE", 53.28, None),
    (56.16, 56.78, None, "FOLLOW ME", 56.32, None),
]
MG = [
    {"type": "hero", "t0": 1.80, "t1": 3.76, "icon": "f:spiral_calendar", "label": "every single week"},
    {"type": "hero", "t0": 8.74, "t1": 10.50, "icon": "f:robot"},
    {"type": "icons", "t0": 17.02, "t1": 19.14, "items": [{"t": 17.04, "icon": "l:instagram", "label": "instagram"}, {"t": 17.36, "icon": "l:youtube", "label": "youtube"},
                                                       {"t": 17.68, "icon": "l:tiktok", "label": "tiktok"}, {"t": 18.00, "icon": "l:x", "label": "x"}]},
    {"type": "hero", "t0": 19.22, "t1": 20.20, "icon": "f:bar_chart", "label": "pull metrics"},
    {"type": "hero", "t0": 20.26, "t1": 22.40, "icon": "f:light_bulb", "label": "what to post next"},
    {"type": "hero", "t0": 22.52, "t1": 24.28, "icon": "f:high_voltage"},
    {"type": "chips", "t0": 27.80, "t1": 29.96, "items": [{"t": 27.92, "icon": "l:instagram", "text": "posted on instagram"}, {"t": 28.40, "icon": "l:youtube", "text": "posted on youtube"},
                                                       {"t": 28.80, "icon": "l:tiktok", "text": "posted on tiktok"}]},
    {"type": "counter", "t0": 42.40, "t1": 43.54, "tc": 42.70, "dur": 0.5, "from": 1, "to": 5, "suffix": " YEARS", "label": "editing & designing"},
    {"type": "hero", "t0": 44.98, "t1": 46.60, "icon": "f:compass", "label": "the right direction"},
    {"type": "chips", "t0": 49.62, "t1": 54.34, "items": [{"t": 49.68, "icon": "f:chart_increasing", "text": "client: scaling the business"},
                                                       {"t": 52.08, "icon": "f:gear", "text": "me: the content system"}]},
    {"type": "follow", "t0": 54.46, "t1": 58.45, "tap": 56.34, "handle": "yog.visuals_", "sub": "AI content systems", "initials": "Y"},
]
SFX = [
    [1.80, "h_pop-reveal.mp3", -16, 0, "onset"],
    [3.98, "h_whoosh-soft.mp3", -13, 0, "peak"],
    [8.74, "pop.mp3", -16, 0, "onset"],
    [13.00, "whoosh-short.mp3", -14, -2, "peak"],
    [17.04, "h_pop-reveal.mp3", -18, 2, "onset"], [18.00, "pop.mp3", -18, 4, "onset"],
    [19.22, "h_pop-reveal.mp3", -17, -1, "onset"], [20.26, "pop.mp3", -17, 1, "onset"],
    [22.52, "h_whoosh-reverse.mp3", -17, 0, "peak"],
    [27.92, "h_ui-send.mp3", -17, 0, "onset"], [28.80, "pop.mp3", -18, 3, "onset"],
    [30.00, "h_whoosh-soft.mp3", -16, 3, "peak"],
    [33.18, "h_whoosh-soft.mp3", -13, -1, "peak"],
    [42.96, "h_clock-tick-soft.mp3", -16, 0, "onset"],
    [44.98, "h_pop-reveal.mp3", -17, 2, "onset"],
    [49.68, "pop.mp3", -17, 0, "onset"], [52.08, "h_pop-reveal.mp3", -17, 3, "onset"],
    [56.34, "pop.mp3", -14, 0, "onset"],
]
J.build(CUTS, CARDS, EMPH, MG, SFX, zooms=(1.2, 1.06), hook=(1.34, 1.06))
