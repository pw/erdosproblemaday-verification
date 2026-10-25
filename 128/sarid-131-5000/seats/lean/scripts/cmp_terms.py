# Compare the Lean literal certificateTerms (Data.lean) with clebsch_tangent_certificate.json term-by-term (exact rationals).
import json, re, sys
from fractions import Fraction as Q
root=sys.argv[1]
d=json.load(open(root+'/clebsch_tangent_certificate.json'))
print('json statement:', d['statement']); print('json epsilon:', d['epsilon']); print('json terms:', len(d['terms']))
print('first json term keys:', list(d['terms'][0].keys()) if isinstance(d['terms'][0],dict) else type(d['terms'][0]))
src=open(root+'/lean/Erdos128/C4Certificate/Data.lean').read()
rat=r'\(\s*(-?\d+)\s*(?:/\s*(\d+))?\s*:\s*ℚ\s*\)'
terms=[]
for m in re.finditer(r'⟨\.(s0|s2 (?:true|false)|u4 \d+),\s*'+rat+r',\s*\[(.*?)\]⟩', src, re.S):
    blk=m.group(1); w=Q(int(m.group(2)), int(m.group(3) or 1))
    vec=[Q(int(a), int(b or 1)) for a,b in re.findall(rat, m.group(4))]
    terms.append((blk,w,vec))
print('lean terms parsed:', len(terms))
def jblock(t):
    return t
jt=d['terms']
print('json term[0] sample:', {k:(v if not isinstance(v,list) else v[:4]) for k,v in jt[0].items()})
print('json block names:', sorted(set(t['block'] for t in jt)))
mapping={}
mism=0
for i,((blk,w,vec),t) in enumerate(zip(terms,jt)):
    jw=Q(t['weight']); jv=[Q(x) for x in t['vector']]
    mapping.setdefault(blk,set()).add(t['block'])
    if jw!=w or jv!=vec:
        mism+=1; print('MISMATCH at',i,blk,t['block'],w,jw)
print('block name correspondence:',{k:sorted(v) for k,v in mapping.items()})
print('term-by-term (in file order) weight+vector mismatches:',mism)
