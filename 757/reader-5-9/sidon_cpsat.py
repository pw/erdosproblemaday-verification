# Exact max Sidon subset via CP-SAT. Sidon = all sums a+b (a<=b, a=b allowed) distinct.
import sys, itertools
from collections import defaultdict
from ortools.sat.python import cp_model
from build import S
def conflicts(s):
    idx={x:i for i,x in enumerate(s)}
    sums=defaultdict(list)
    n=len(s)
    for i in range(n):
        for j in range(i,n): sums[s[i]+s[j]].append((i,j))
    cl=set()
    for v,ps in sums.items():
        for p,q in itertools.combinations(ps,2):
            cl.add(tuple(sorted(set(p)|set(q))))
    return cl
def max_sidon(s, timeout=600, workers=4):
    cl=conflicts(s)
    m=cp_model.CpModel(); x=[m.NewBoolVar(f'x{i}') for i in range(len(s))]
    for c in cl: m.AddBoolOr([x[i].Not() for i in c])
    m.Maximize(sum(x))
    sv=cp_model.CpSolver(); sv.parameters.max_time_in_seconds=timeout; sv.parameters.num_workers=workers
    st=sv.Solve(m)
    T=[s[i] for i in range(len(s)) if sv.Value(x[i])]
    return sv.StatusName(st), int(sv.ObjectiveValue()), int(sv.BestObjectiveBound()), T, len(cl)
def is_sidon(T):
    sm=[a+b for i,a in enumerate(T) for b in T[i:]]
    return len(sm)==len(set(sm))
if __name__=='__main__':
    # controls: {0,1,3,7} Sidon (4); {0,1,2,3} max Sidon 3
    assert max_sidon([0,1,3,7])[1]==4 and max_sidon([0,1,2,3])[1]==3
    for K in range(int(sys.argv[1]),int(sys.argv[2])+1):
        s=S(K); st,obj,bd,T,nc=max_sidon(s)
        assert is_sidon(T) and len(T)==obj
        print(K,len(s),st,'max',obj,'bound',bd,'claim',7+5*K,'conflicts',nc,flush=True)
