"""Generate tokens/fulala-tokens.css from tokens/fulala.tokens.json.
Run: python3 tokens/build_tokens.py"""
import json, os, re
D = os.path.dirname(os.path.abspath(__file__))
T = json.load(open(os.path.join(D, "fulala.tokens.json")))

def var(path):  # "color.cinnabar" -> var(--fulala-color-cinnabar)
    return "var(--fulala-" + path.replace(".", "-") + ")"

def val(v):
    if isinstance(v, str):
        return re.sub(r"\{([^}]+)\}", lambda m: var(m.group(1)), v)
    if isinstance(v, list):
        return ", ".join(f'"{x}"' if " " in x else x for x in v)
    return str(v)

out = ["/* Fulala design tokens v1.0, generated from fulala.tokens.json. Do not edit by hand. */",
       '@import url("https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,400;9..40,600;9..40,700&family=Grandstander:wght@600;700&display=swap");',
       "", ":root {"]
def walk(node, path):
    if "$value" in node:
        t, v = node["$type"], node["$value"]
        name = "--fulala-" + "-".join(path)
        if t == "shadow":
            out.append(f"  {name}: {v['offsetX']} {v['offsetY']} {v['blur']} {v['spread']} {val(v['color'])};")
        elif t == "typography":
            out.append(f"  {name}: {v['fontWeight']} {v['fontSize']}/{v['lineHeight']} {val(v['fontFamily'])};")
            out.append(f"  {name}-tracking: {v['letterSpacing']};")
        else:
            out.append(f"  {name}: {val(v)};")
        return
    for k, child in node.items():
        if not k.startswith("$"):
            if not path: out.append(f"\n  /* {k} */")
            walk(child, path + [k])
walk(T, [])
out.append("}\n")
out.append("/* Text style helpers */")
for k in T["typography"]:
    extra = " text-transform: uppercase;" if k == "eyebrow" else ""
    out.append(f".fulala-{k} {{ font: var(--fulala-typography-{k}); letter-spacing: var(--fulala-typography-{k}-tracking);{extra} }}")
open(os.path.join(D, "fulala-tokens.css"), "w").write("\n".join(out) + "\n")
print("wrote tokens/fulala-tokens.css")
