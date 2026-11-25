import sys, itertools
from ortools.sat.python import cp_model
def alpha(A):
    A=sorted(set(A)); S=set(A); n=len(A)
    m=cp_model.CpModel(); x=[m.NewBoolVar(f"x{i}") for i in range(n)]
    E=0
    for i in range(n):
        for j in range(i+1,n):
            if A[i]+A[j] in S:
                m.AddBoolOr([x[i].Not(),x[j].Not()]); E+=1
    m.Maximize(sum(x))
    s=cp_model.CpSolver(); s.parameters.num_workers=8; s.parameters.max_time_in_seconds=600
    r=s.Solve(m)
    return int(s.ObjectiveValue()), s.StatusName(r), E
A43=[-42,-26,-24,-22,-20,-18,-16,-14,-13,-12,-11,-10,-9,-8,-7,-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,16,18,20,22,24,26,42]
print("A43 len",len(A43), "contains -14..14", all(x in A43 for x in range(-14,15)))
P=list(range(1,11))+[12,14,16,18,30]
print("pos15", len(P), alpha(P))
F=A43; k=6
for step in range(7):
    a=alpha(F)
    print(k, len(F), k*k+3*k-11, a, "interval", all(x in set(F) for x in range(-(2*k+2),2*k+3)), flush=True)
    odds=[s*(2*j+1) for j in range(k+2) for s in (1,-1)]
    F=sorted(set(odds)|{2*x for x in F}); k+=1
