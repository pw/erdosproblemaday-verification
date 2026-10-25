# Klein-type 21-point set at q=11 from coordinate permutations of (1,0,0),(1,±1,0),(1,±1,±cb), cb a root of t^2+t+2.
import itertools,json,sys
from pg import plane,norm
q=11; pts,lines=plane(q)
for cb in [r for r in range(q) if (r*r+r+2)%q==0]:
    base=[(1,0,0),(1,1,0),(1,q-1,0)]+[(1,s,t*cb%q) for s in (1,q-1) for t in (1,q-1)]
    S={norm(tuple(v[i] for i in perm),q) for v in base for perm in itertools.permutations(range(3))}
    spec=sorted({len(S&s) for s in lines.values()})
    print('cb',cb,'|S|',len(S),'intersection sizes',spec)
    if len(S)==21 and spec[0]>=1 and spec[-1]<=4: json.dump(sorted(S),open('klein11.json','w')); break
