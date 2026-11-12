import os, re, sys
root = sys.argv[1]
start = sys.argv[2]
seen = set(); stack = [start]
while stack:
    mod = stack.pop()
    if mod in seen: continue
    seen.add(mod)
    path = os.path.join(root, *mod.split('.')) + '.lean'
    if not os.path.exists(path): continue
    for line in open(path):
        mm = re.match(r'\s*import\s+(.*)', line)
        if mm:
            for t in mm.group(1).split():
                if t.startswith('Erdos708'): stack.append(t)
proj = sorted(s for s in seen if s.startswith('Erdos708'))
print(len(proj), "project modules in closure of", start)
for s in proj: print(s)
