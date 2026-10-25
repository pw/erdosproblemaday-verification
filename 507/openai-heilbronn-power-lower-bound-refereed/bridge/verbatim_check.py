#!/usr/bin/env python3
# Asserts every declaration chunk between `-- VERBATIM BEGIN x` / `-- VERBATIM END x` in Bridge507.lean occurs verbatim
# (whitespace-normalised, docstrings/attribute lines/`public`/`@[expose]` stripped) in the Formal Conjectures sources
# FC_507.lean, FC_2d.lean, FC_Asymptotics.lean, FC_green77.lean (pinned in FC_SHA.txt) and BOS_Statement.lean (BOS_SHA.txt). Exit 0 all found; 1 a chunk missing; 2 no chunks.
import re, sys
def norm(t):
    t = re.sub(r"/--.*?-/", " ", t, flags=re.S)          # docstrings
    t = re.sub(r"/-.*?-/", " ", t, flags=re.S)           # block comments (licence)
    t = re.sub(r"(?m)^\s*--.*$", " ", t)                 # line comments
    t = re.sub(r"(?m)^\s*@\[[^\]]*\]\s*$", " ", t)       # attribute-only lines
    t = re.sub(r"@\[category[^\]]*\]", " ", t)
    t = re.sub(r"\bpublic\s+", " ", t)
    return re.sub(r"\s+", " ", t).strip()
src = sys.argv[1] if len(sys.argv) > 1 else "Bridge507.lean"
B = open(src).read()
FC = norm("\n".join(open(f).read() for f in ("FC_507.lean", "FC_2d.lean", "FC_Asymptotics.lean", "FC_green77.lean", "BOS_Statement.lean")))
blocks = re.findall(r"-- VERBATIM BEGIN (\S+)\n(.*?)-- VERBATIM END \1", B, flags=re.S)
if not blocks: print("NO VERBATIM BLOCKS"); sys.exit(2)
bad = 0; n = 0
for name, body in blocks:
    for chunk in re.split(r"\n\s*\n", body):
        c = norm(chunk)
        if not c: continue
        n += 1
        ok = c in FC
        bad += not ok
        print(("OK      " if ok else "MISSING ") + name + " | " + c[:110])
print(f"{n} chunks, {bad} missing")
sys.exit(1 if bad else 0)
