# (4,5) for large K via exhaustive difference-collision counting (no structural assumption):
# a 4-set B is bad iff >=2 (pair,pair) equalities among its 6 positive differences.
import sys, itertools, time; sys.path.insert(0,'/tmp/ref757')
from core import *
from collections import defaultdict, Counter
def bad_count(P):
    D=defaultdict(list)
    for i,j in itertools.combinations(range(len(P)),2): D[P[j]-P[i]].append((i,j))
    eq=Counter()
    for d,prs in D.items():
        for p,q in itertools.combinations(prs,2):
            U=frozenset(p)|frozenset(q)
            if len(U)==4: eq[U]+=1
            else:
                for x in range(len(P)):
                    if x not in U: eq[U|{x}]+=1
    return sum(1 for B,c in eq.items() if c>=2), len(eq)
# controls
assert bad_count([0,1,2,3])[0]==1 and bad_count([0,1,2,4])[0]==1 and bad_count([0,1,2,5])[0]==0
assert bad_count([0,10,20,30,47,61])[0]>=1
for K in [int(a) for a in sys.argv[1:]]:
    t=time.time(); sc=269**K; P=[int(x*sc) for x in SK(K)]
    print('K',K,'n',len(P),'(bad, 4-sets with >=1 equality)=',bad_count(P),f'{time.time()-t:.1f}s',flush=True)
