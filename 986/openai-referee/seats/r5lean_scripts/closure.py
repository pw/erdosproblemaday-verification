import sys, os, re
root = sys.argv[1]
start = sys.argv[2]
seen = set(); stack=[start]
while stack:
    m = stack.pop()
    if m in seen: continue
    seen.add(m)
    p = os.path.join(root, *m.split('.')) + '.lean'
    if not os.path.exists(p): continue
    for line in open(p, encoding='utf-8'):
        mm = re.match(r'\s*import\s+(\S+)', line)
        if mm and mm.group(1).startswith('OAI'):
            stack.append(mm.group(1))
for m in sorted(seen):
    print(m)
