# Multi-root import closure for OpenAI family 21 (Erdős #970). Scans EVERY line for import / public import / meta import
# (the #371 lesson: never stop at a leading /- licence -/ block). OAI + ComparatorChallenges read via `git show` from
# openai/math @1581d4c; external packages read from patched checkouts in /tmp/oaimath/021/ext.
import subprocess, sys, re, os
REPO='/tmp/oaimath/024/repo'; DST='/tmp/oaimath/021/repo/lean'; EXT='/tmp/oaimath/021/ext'
FS_ROOTS={'PrimeNumberTheoremAnd':EXT+'/PrimeNumberTheoremAnd','StrongPNT':EXT+'/StrongPNT','AbsorptionCutoff':EXT+'/AbsorptionCutoff'}
STD=('Mathlib','Init','Std','Lean','Batteries','Aesop','Qq','Plausible','ProofWidgets','ImportGraph','LeanSearchClient')
def src_of(m):
    top=m.split('.')[0]; rel=m.replace('.','/')+'.lean'
    if top in ('OAI','ComparatorChallenges'):
        r=subprocess.run(['git','-C',REPO,'show','HEAD:lean/'+rel],capture_output=True,text=True)
        if r.returncode: return None
        p=os.path.join(DST,rel); os.makedirs(os.path.dirname(p),exist_ok=True); open(p,'w').write(r.stdout); return r.stdout
    if top in FS_ROOTS:
        p=os.path.join(FS_ROOTS[top],rel)
        return open(p).read() if os.path.exists(p) else None
    return None
seen=set(); order=[]; ext=set(); missing=[]
sys.setrecursionlimit(100000)
def visit(m):
    if m in seen: return
    seen.add(m)
    top=m.split('.')[0]
    if top not in ('OAI','ComparatorChallenges') and top not in FS_ROOTS: ext.add(m); return
    s=src_of(m)
    if s is None: missing.append(m); return
    for line in s.split('\n'):
        mm=re.match(r'^\s*(?:public\s+|meta\s+|private\s+)*import\s+(\S+)',line)
        if mm: visit(mm.group(1))
    order.append(m)
for t in sys.argv[1:]: visit(t)
open('/tmp/oaimath/021/all_order.txt','w').write('\n'.join(order)+'\n')
from collections import Counter
print(len(order),'local modules by root:',dict(Counter(m.split('.')[0] for m in order)))
print('MISSING (local root, no file):',missing)
print('non-std externals:',sorted(e for e in ext if not e.startswith(STD)))
