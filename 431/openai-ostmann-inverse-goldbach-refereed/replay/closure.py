# Import closure for OpenAI family 013 (Ostmann, Erdős #431) at openai/math 1581d4c across every source root.
# Scans EVERY line for import / public import / meta import (#371 lesson). Post-order DFS from the TARGETS (#371 lesson:
# never count a build list as the closure). Prints any module it cannot locate.
import sys, re, os, json
E='/tmp/oaimath/013/ext'
ROOTS={'OAI':'/tmp/oaimath/013/repo/lean','ComparatorChallenges':'/tmp/oaimath/013/repo/lean',
 'PrimeNumberTheoremAnd':E+'/PrimeNumberTheoremAnd','StrongPNT':E+'/StrongPNT','AbsorptionCutoff':E+'/AbsorptionCutoff',
 'BernoulliRegular':E+'/AINTLIB/projects/FltRegularBernoulli','FltRegular':E+'/AINTLIB/projects/FltRegular','Common':E+'/AINTLIB/Common'}
STD=('Mathlib','Init','Std','Lean','Batteries','Aesop','Qq','Plausible','ProofWidgets','ImportGraph','LeanSearchClient','Lake')
targets=sys.argv[1:]
seen=set(); order=[]; ext=set(); missing=set()
sys.setrecursionlimit(100000)
def visit(m):
    if m in seen: return
    seen.add(m)
    top=m.split('.')[0]
    if top in STD: ext.add(m); return
    if top not in ROOTS: missing.add(m); return
    p=os.path.join(ROOTS[top],m.replace('.','/')+'.lean')
    if not os.path.exists(p): missing.add(m); return
    for line in open(p):
        mm=re.match(r'^\s*(?:public\s+|meta\s+)*import\s+(\S+)',line)
        if mm: visit(mm.group(1))
    order.append(m)
for t in targets: visit(t)
OUTP=os.environ.get('CLOSURE_OUT','/tmp/oaimath/013/closure_last.txt'); open(OUTP,'w').write('\n'.join(order)+'\n')
from collections import Counter
print(len(order),'modules to build;', dict(Counter(m.split('.')[0] for m in order)))
print('Ostmann subtree:', sum(1 for m in order if m.startswith('OAI.NumberTheory.Ostmann')), 'Jacobsthal:', sum(1 for m in order if '.Jacobsthal.' in m), 'PrimeGaps:', sum(1 for m in order if '.PrimeGaps.' in m))
print('MISSING:', sorted(missing))
print('std prefixes:', sorted(set(e.split('.')[0] for e in ext)))
