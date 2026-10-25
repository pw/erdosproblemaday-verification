import re, sys, os
root = sys.argv[1]; start = sys.argv[2:]
seen=set(); order=[]; stack=list(start); ext=set()
def path(m): return os.path.join(root, *m.split('.')) + '.lean'
while stack:
    m=stack.pop()
    if m in seen: continue
    seen.add(m)
    p=path(m)
    if not os.path.exists(p): ext.add(m); continue
    src=open(p,encoding='utf-8').read()
    for imp in re.findall(r'^\s*(?:public\s+)?import\s+(?:all\s+)?([\w.]+)', src, re.M):
        if imp.startswith('Proofs'): stack.append(imp)
        else: ext.add(imp.split('.')[0])
    order.append(m)
print(len(order), 'project modules;', 'external roots:', sorted(set(e.split('.')[0] for e in ext)))
missing=[e for e in ext if e.startswith('Proofs')]
print('missing project modules:', missing)
open(os.environ.get('CLOSURE_OUT', '/dev/null'),'w').write('\n'.join(sorted(order)))
