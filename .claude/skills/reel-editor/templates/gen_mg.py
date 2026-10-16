# Build the overlay page for template_minimal.html + mg.js: gen_mg.py plan.json outdir fonts_dir mg_assets_dir
# mg_assets_dir holds fluent/<name>_3d.png (Microsoft Fluent 3D emoji, MIT) and logos/<name>.svg (simple-icons, CC0).
import json, os, re, shutil, sys
HERE = os.path.dirname(os.path.abspath(__file__))
P = json.load(open(sys.argv[1])); od, fonts, A = sys.argv[2:5]
BRAND = {"youtube": "#FF0000", "instagram": "#E4405F", "whatsapp": "#25D366", "linkedin": "#0A66C2", "spotify": "#1DB954",
         "applepodcasts": "#9933CC", "zoom": "#0B5CFF", "googlemeet": "#00897B", "tiktok": "#000000", "x": "#000000", "notion": "#000000", "googledrive": "#1FA463"}
os.makedirs(f"{od}/img/fluent", exist_ok=True); os.makedirs(f"{od}/img/logos", exist_ok=True)
shutil.copytree(fonts, f"{od}/fonts", dirs_exist_ok=True)
d = {k: P.get(k, []) for k in ("phrases", "cards", "mg")}
s = json.dumps(d, ensure_ascii=False)
for kind, name in set(re.findall(r'"(f|l):([a-z0-9_]+)"', s)) | {("f", "check_mark_button"), ("f", "cross_mark")}:
    if kind == "f": shutil.copy(f"{A}/fluent/{name}_3d.png", f"{od}/img/fluent/")
    else:
        svg = open(f"{A}/logos/{name}.svg").read().replace("<svg ", f'<svg fill="{BRAND.get(name, "#111")}" ', 1)
        open(f"{od}/img/logos/{name}.svg", "w").write(svg)
ig = open(f"{A}/logos/instagram.svg").read().replace("<svg ", '<svg fill="#E4405F" ', 1); open(f"{od}/img/instagram.svg", "w").write(ig)
shutil.copy(f"{HERE}/mg.js", od)
open(f"{od}/front.html", "w").write(open(f"{HERE}/template_minimal.html").read().replace("/*DATA*/", "const D=" + s + ";"))
missing = [n for k, n in re.findall(r'"(f|l):([a-z0-9_]+)"', s) if not os.path.exists(f"{od}/img/{'fluent' if k == 'f' else 'logos'}/{n}{'_3d.png' if k == 'f' else '.svg'}")]
print("ok", "missing:", missing)
