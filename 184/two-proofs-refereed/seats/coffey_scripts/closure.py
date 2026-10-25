import re, sys, os
root = sys.argv[1]  # formal dir
start = sys.argv[2]  # module name e.g. EG.Proof.Main
def path(mod):
    return os.path.join(root, *mod.split('.')) + '.lean'
seen = set(); stack=[start]
while stack:
    m = stack.pop()
    if m in seen: continue
    seen.add(m)
    p = path(m)
    if not os.path.exists(p): continue
    for line in open(p, encoding='utf-8'):
        mm = re.match(r'\s*(?:public\s+)?(?:meta\s+)?import\s+(?:all\s+)?([\w.«»]+)', line)
        if mm:
            dep = mm.group(1)
            if dep.startswith('EG'):
                stack.append(dep)
for m in sorted(seen):
    print(m)
