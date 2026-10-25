#!/usr/bin/env python3
# Multi-root import closure. usage: closure2.py ROOTMODULE  (roots hard-coded below)
import sys,os
ROOTS={'OAI':'/tmp/oaimath/024/repo/lean','ComparatorChallenges':'/tmp/oaimath/024/repo/lean',
 'PrimeNumberTheoremAnd':'/tmp/oaimath/012/src/pnt','StrongPNT':'/tmp/oaimath/012/src/strongpnt',
 'Architect':'/tmp/oaimath/024/architect'}
seen=set(); order=[]; ext=set(); missing=[]
def path(m): return f"{ROOTS[m.split('.')[0]]}/{m.replace('.','/')}.lean"
def imps(m):
    # robust header parse: strip nested /- -/ block comments and -- line comments, then take every import line
    src=open(path(m)).read()
    out=[]; i=0; depth=0; buf=[]
    while i < len(src):
        if src.startswith('/-', i): depth+=1; i+=2; continue
        if depth and src.startswith('-/', i): depth-=1; i+=2; continue
        if not depth: buf.append(src[i])
        i+=1
    text=''.join(buf)
    for line in text.split('\n'):
        line=line.split('--')[0].strip()
        if not line: continue
        t=line.split()
        if t[0] in ('import','public','meta') and len(t)>=2:
            if t[-1] != 'section': out.append(t[-1])
            continue
        if t[0] in ('module','prelude'): continue
        break
    return out
def visit(m):
    if m in seen: return
    seen.add(m)
    if not os.path.exists(path(m)): missing.append(m); return
    for d in imps(m):
        if d.split('.')[0] in ROOTS: visit(d)
        else: ext.add(d.split('.')[0])
    order.append(m)
for r in sys.argv[1:]: visit(r)
for m in order: print(m)
print('EXTERNAL',sorted(ext),'MISSING',missing,file=sys.stderr)
from collections import Counter
print(Counter(m.split('.')[0] for m in order),file=sys.stderr)
