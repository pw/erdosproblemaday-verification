# Max Sidon subset via CP-SAT on ALL sum-collision conflicts (a<=b), brute-forced; no structure assumed.
import sys, itertools, time; sys.path.insert(0,'/tmp/ref757')
from core import *
from collections import defaultdict
from ortools.sat.python import cp_model
def maxsidon(P,tl=300):
    n=len(P); S=defaultdict(list)
    for i in range(n):
        for j in range(i,n): S[P[i]+P[j]].append((i,j))
    C={tuple(sorted(set(p)|set(q))) for v,ps in S.items() for p,q in itertools.combinations(ps,2)}
    m=cp_model.CpModel(); x=[m.NewBoolVar('') for _ in range(n)]
    for c in C: m.AddBoolOr([x[i].Not() for i in c])
    m.Maximize(sum(x)); s=cp_model.CpSolver(); s.parameters.max_time_in_seconds=tl; s.parameters.num_workers=8
    st=s.Solve(m); T=[P[i] for i in range(n) if s.Value(x[i])]
    sums=[a+b for i,a in enumerate(T) for b in T[i:]]; assert len(sums)==len(set(sums))
    return s.StatusName(st), len(T), int(s.BestObjectiveBound())
assert maxsidon([0,1,2,3])[1]==3 and maxsidon([0,1,3,7])[1]==4 and maxsidon([0,1,2,4,8])[1]==4
for K in [int(a) for a in sys.argv[1:]]:
    t=time.time(); sc=269**K; P=[int(x*sc) for x in SK(K)]
    print('K',K,'n',len(P),maxsidon(P),'claim',7+5*K,f'{time.time()-t:.0f}s',flush=True)
