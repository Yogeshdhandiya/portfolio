# Video 3: "stop doing these 5 things manually" (listicle, close-up at the desk, 66 s)
import sys; sys.path.insert(0, "/home/user/portfolio/.claude/skills/reel-editor/scripts")
from planlib import Job
J = Job("analysis.json", "src/src.words.json", end=66.23,
        fixes={37.28: "carousel,", 42.48: "mogrts,", 43.20: "presets", 40.16: "", 40.40: "and", 46.64: "number", 47.20: "follow-ups.",
               47.76: "if", 51.52: "it's", 54.56: "lastly,", 57.36: "believe", 60.00: "it", 19.60: "explain"})
lw = J.lw
CUTS = [1.50, 3.02, 4.78, 7.34, 9.26, 11.62, 13.70, 19.98, 23.82, 25.18, 27.88, 31.74, 34.22, 36.10, 40.12, 43.168,
        46.62, 47.631, 49.98, 51.50, 54.52, 57.30, 60.00, 62.14, 64.46]
CARDS = [
    {"type": "flow", "a": 13.70, "b": 19.98, "lead": [[13.76, "create a list"]],
     "items": [["CREATORS", "f:star", 14.48], ["COMPETITORS", "f:eyes", 15.52], ["ARTICLES", "f:spiral_notepad", 16.32],
               ["NEWSLETTERS", "f:inbox_tray", 16.96], ["AI EXPLAINS", "f:robot", 19.20]]},
    {"type": "flow", "a": 27.88, "b": 31.74, "lead": lw(27.92, 28.50),
     "items": [["RESEARCH", "f:magnifying_glass_tilted_left", 28.56], ["QUALIFY", "f:check_mark_button", 29.68], ["OUTREACH", "f:outbox_tray", 31.04]]},
    {"type": "flow", "a": 57.30, "b": 60.00, "lead": [[57.36, "connect your workflows"]],
     "items": [["IDEAS", "f:light_bulb", 57.84], ["CLIENTS", "f:handshake", 58.16], ["EDITING", "f:clapper_board", 58.48], ["FOLLOW-UPS", "f:speech_balloon", 58.80]]},
]
EMPH = [
    (0.00, 1.48, (0.00, 0.63), "ONE-PERSON BUSINESS", 0.64, None),
    (1.52, 3.00, (1.52, 2.07), "5 THINGS", 2.08, (2.56, 3.00)),
    (3.04, 4.76, (3.04, 3.99), "WHAT TO POST", 4.00, None),
    (4.80, 7.34, (4.80, 5.59), "TWO HOURS", 5.60, (6.16, 7.34)),
    (9.28, 11.50, (9.28, 9.83), "SYSTEM", 9.84, (10.08, 11.50)),
    (20.40, 23.80, (20.40, 21.43), "2 HOURS", 21.44, (22.24, 23.80)),
    (23.84, 25.18, (23.84, 24.31), "FINDING CLIENTS", 24.32, None),
    (31.76, 34.22, (31.76, 32.23), "EDITING FROM SCRATCH", 32.24, None),
    (45.44, 46.62, None, "SPEED UP YOUR WORKFLOW", 45.68, None),
    (46.64, 47.74, (46.64, 47.19), "FOLLOW-UPS", 47.20, None),
    (50.00, 51.48, (50.00, 50.87), "BRAIN CELLS", 50.88, None),
    (54.56, 57.28, (54.56, 55.59), "CONNECTING ALL THE PIECES", 55.60, None),
    (60.00, 62.12, (60.00, 60.79), "HIRED AN EMPLOYEE", 60.80, None),
    (64.48, 66.23, (64.48, 65.11), '"VIDEO"', 65.12, (65.36, 66.23)),
]
MG = [
    {"type": "hero", "t0": 1.56, "t1": 2.98, "icon": "f:gear", "label": "stop doing it manually"},
    {"type": "badge", "t0": 3.06, "t1": 4.74, "num": "1"},
    {"type": "hero", "t0": 5.62, "t1": 7.30, "icon": "f:hourglass_done"},
    {"type": "hero", "t0": 11.68, "t1": 13.50, "icon": "f:thinking_face", "label": "what your audience thinks"},
    {"type": "hero", "t0": 20.44, "t1": 23.78, "icon": "l:instagram", "label": "endless scrolling"},
    {"type": "badge", "t0": 23.86, "t1": 25.16, "num": "2"},
    {"type": "counter", "t0": 25.24, "t1": 27.64, "tc": 26.08, "dur": 0.8, "from": 0, "to": 100, "suffix": "", "label": "profiles, one by one"},
    {"type": "badge", "t0": 31.80, "t1": 34.20, "num": "3"},
    {"type": "hero", "t0": 34.26, "t1": 36.08, "icon": "l:youtube", "label": "one video"},
    {"type": "icons", "t0": 36.12, "t1": 40.10, "items": [{"t": 36.16, "icon": "f:framed_picture", "label": "post"}, {"t": 36.72, "icon": "f:clapper_board", "label": "reel"},
                                                       {"t": 37.28, "icon": "f:card_index_dividers", "label": "carousel"}, {"t": 37.84, "icon": "l:x", "label": "thread"},
                                                       {"t": 38.72, "icon": "f:inbox_tray", "label": "newsletter"}]},
    {"type": "icons", "t0": 41.64, "t1": 45.40, "items": [{"t": 41.76, "icon": "f:clipboard", "label": "templates"}, {"t": 42.48, "icon": "f:sparkles", "label": "mogrts"},
                                                       {"t": 43.20, "icon": "f:artist_palette", "label": "presets"}, {"t": 44.08, "icon": "f:robot", "label": "AI tools"}]},
    {"type": "badge", "t0": 46.66, "t1": 48.90, "num": "4"},
    {"type": "hero", "t0": 50.02, "t1": 51.46, "icon": "f:brain"},
    {"type": "notif", "t0": 52.10, "t1": 54.46, "icon": "f:robot", "bg": "#e9ecff", "app": "Automation", "title": "Follow-ups sent", "body": "12 leads messaged, 3 replied"},
    {"type": "badge", "t0": 54.58, "t1": 57.02, "num": "5"},
    {"type": "hero", "t0": 60.06, "t1": 62.10, "icon": "f:robot", "label": "your new employee"},
    {"type": "hero", "t0": 62.20, "t1": 64.42, "icon": "l:youtube", "label": "full breakdown"},
    {"type": "notif", "t0": 64.50, "t1": 66.23, "icon": "l:instagram", "app": "Instagram", "title": "New comment", "body": "you commented: VIDEO 🔥"},
]
SFX = [
    [0.64, "h_whoosh-soft.mp3", -16, 2, "peak"],
    [3.06, "h_pop-reveal.mp3", -15, 0, "onset"], [5.62, "pop.mp3", -17, -2, "onset"],
    [13.70, "h_whoosh-soft.mp3", -13, 0, "peak"],
    [20.44, "h_pop-reveal.mp3", -17, 2, "onset"],
    [23.86, "pop.mp3", -15, 2, "onset"], [26.08, "h_clock-tick-soft.mp3", -16, 0, "onset"],
    [27.88, "whoosh-short.mp3", -14, -2, "peak"],
    [31.80, "h_pop-reveal.mp3", -15, 3, "onset"], [34.26, "pop.mp3", -17, 0, "onset"],
    [36.16, "h_pop-reveal.mp3", -18, 1, "onset"], [37.28, "pop.mp3", -18, 3, "onset"], [38.72, "h_pop-reveal.mp3", -18, 5, "onset"],
    [41.76, "pop.mp3", -18, 0, "onset"], [43.20, "h_pop-reveal.mp3", -18, 2, "onset"],
    [46.66, "pop.mp3", -15, 4, "onset"], [50.02, "h_whoosh-reverse.mp3", -17, 0, "peak"], [52.10, "h_ui-send.mp3", -14, 0, "onset"],
    [54.58, "h_pop-reveal.mp3", -15, 5, "onset"],
    [57.30, "h_whoosh-soft.mp3", -13, 2, "peak"],
    [60.06, "pop.mp3", -16, 0, "onset"], [62.20, "h_pop-reveal.mp3", -17, 0, "onset"], [64.50, "h_ui-send.mp3", -13, 2, "onset"],
]
J.build(CUTS, CARDS, EMPH, MG, SFX, zooms=(1.2, 1.06), hook=(1.34, 1.06))
