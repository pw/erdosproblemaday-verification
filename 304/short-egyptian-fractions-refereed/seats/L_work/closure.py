import re,sys,os
root=sys.argv[1]; start=sys.argv[2]
def path(m): return os.path.join(root, *m.split('.'))+'.lean'
seen=set(); stack=[start]; ext=set()
while stack:
    m=stack.pop()
    if m in seen: continue
    seen.add(m)
    for line in open(path(m)):
        mm=re.match(r'\s*import\s+(\S+)',line)
        if mm:
            x=mm.group(1)
            if x.startswith('OAI.'): stack.append(x)
            else: ext.add(x)
for m in sorted(seen): print(m)
print('COUNT',len(seen),file=sys.stderr); print('EXT',sorted(ext),file=sys.stderr)
