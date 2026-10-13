import json, sys
plan = json.load(open("../plan.json"))
tpl = open("template.html").read()
for layer in ("front", "behind"):
    d = {k: plan[k] for k in ("phrases", "cards", "loop", "roto", "tiles")}
    d["layer"] = layer
    for p in d["phrases"]:
        for L in p["lines"]:
            if L["kind"] == "emph" and p["style"] != "cta":
                L["words"][0]["text"] = L["words"][0]["text"].rstrip(".,:;")
    open(f"{layer}.html", "w").write(tpl.replace("/*DATA*/", "const D=" + json.dumps(d) + ";"))
print("ok")
