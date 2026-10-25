# Import closure of a target module inside openai/math lean/ @1581d4c, read via `git show` from the blob:none clone.
# Scans EVERY line (not just a leading block) for `import` / `public import` / `meta import` — the #371 seat lost 3 modules
# by stopping at a leading /- licence -/ comment.
import subprocess, sys, re, os
REPO='/tmp/oaimath/024/repo'; DST='/tmp/oaimath/021/repo/lean'
def show(path):
    r=subprocess.run(['git','-C',REPO,'show','HEAD:lean/'+path],capture_output=True,text=True)
    return r.stdout if r.returncode==0 else None
targets=sys.argv[1:]
seen=set(); order=[]; ext=set()
def visit(m):
    if m in seen: return
    seen.add(m)
    src=show(m.replace('.','/')+'.lean')
    if src is None: ext.add(m); return
    p=os.path.join(DST,m.replace('.','/')+'.lean'); os.makedirs(os.path.dirname(p),exist_ok=True); open(p,'w').write(src)
    for line in src.split('\n'):
        mm=re.match(r'^\s*(?:public\s+|meta\s+)*import\s+(\S+)',line)
        if mm:
            n=mm.group(1)
            if n.startswith('OAI') or n.startswith('ComparatorChallenges'): visit(n)
            else: ext.add(n)
    order.append(m)
for t in targets: visit(t)
open('/tmp/oaimath/021/closure_order.txt','w').write('\n'.join(order)+'\n')
print(len(order),'local modules;', len([e for e in ext if not e.startswith(('Mathlib','Init','Std','Lean','Batteries','Aesop','Qq','Plausible','ProofWidgets','ImportGraph','LeanSearchClient'))]),'non-std externals:',sorted(e for e in ext if not e.startswith(('Mathlib','Init','Std','Lean','Batteries','Aesop','Qq','Plausible','ProofWidgets','ImportGraph','LeanSearchClient'))))
