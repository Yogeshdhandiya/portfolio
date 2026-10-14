import json
P = json.load(open("../plan.json"))
d = {k: P[k] for k in ("phrases", "cards")}
open("front.html", "w").write(open("template_minimal.html").read().replace("/*DATA*/", "const D=" + json.dumps(d, ensure_ascii=False) + ";"))
print("ok")
