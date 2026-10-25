#!/usr/bin/env python3
# Import closure (OAI namespace) of ComparatorChallenges/JointDickman.lean in openai/math @1581d4c lean/
import sys,os,re
SRC=sys.argv[1]; root=sys.argv[2]
seen={}; order=[]; ext=set()
def path(m): return f"{SRC}/{m.replace('.','/')}.lean"
def imps(m):
    out=[]
    for line in open(path(m)):
        t=line.strip().split()
        if not t: continue
        if t[0] in ('import','public','meta') and len(t)>=2:
            out.append(t[-1])
        elif t[0] not in ('--','/-','module','prelude') and not line.startswith(' ') and t[0] not in ('import','public','meta'):
            if t[0].startswith(('namespace','open','noncomputable','section','set_option','theorem','lemma','def','variable','universe','@[','abbrev','structure','instance','/-!','--')): break
    return out
def visit(m):
    if m in seen: return
    seen[m]=1
    for d in imps(m):
        if d.split('.')[0] in ('OAI','ComparatorChallenges'):
            visit(d)
        else: ext.add(d.split('.')[0])
    order.append(m)
visit(root)
for m in order: print(m)
print('EXTERNAL', sorted(ext), file=sys.stderr)
