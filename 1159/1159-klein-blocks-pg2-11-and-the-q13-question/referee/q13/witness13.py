import json,sys
from collections import Counter
from pg import plane, norm
q=13; pts,lines=plane(q)
W=json.load(open(sys.argv[1]))
if isinstance(W,dict):
    for k in ('points','S','witness','set'):
        if k in W: W=W[k]; break
S={norm(tuple(p),q) for p in W}
assert len(S)==len(W), 'duplicate/denormalised points'
assert all(p in set(pts) for p in S)
spec=Counter(len(S&s) for s in lines.values())
print('|S| =',len(S),' line-intersection spectrum {i: #lines}:',dict(sorted(spec.items())))
print('blocking (no 0-line):',spec.get(0,0)==0,' max intersection:',max(spec),' contains a line:',any(s<=S for s in lines.values()))
# count identities as an internal check of the spectrum
k=len(S); N=q*q+q+1
print('identities:',sum(spec.values())==N, sum(i*t for i,t in spec.items())==k*(q+1), sum(i*(i-1)*t for i,t in spec.items())==k*(k-1))
# minimality: does every point have a tangent?
tan=[p for p in S if any(len(S&s)==1 and p in s for s in lines.values())]
print('points with a tangent:',len(tan),'of',k)
