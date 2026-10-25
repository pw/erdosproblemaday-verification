# Independent instrument: integer-only construction (no Fraction, no import of build.py), Sidon via DISTANCE collisions,
# max size via SAT + cardinality (pysat CaDiCaL 1.5.3, seqcounter). (No (4,5) check in this file: see check45.py.)
import sys, itertools
from pysat.card import CardEnc, EncType
from pysat.solvers import Solver
def construct(K):
    # integer coordinates on scale 269^K: x -> 101*269^K ... apply psi(y) = 101*269^K + 18*y/269 at scale (y integer at scale 269^K)
    s=269**K
    base=[x*s for x in (0,49,75,83,98,101,117,119,121,159,269)]
    P=set(base); cur=base
    for _ in range(K):
        nxt=[]
        for y in cur:
            assert (18*y)%269==0
            nxt.append(101*s+18*y//269)
        P|=set(nxt); cur=nxt
    return sorted(P)
def dist_conflicts(P):
    # sets {p,q,r,t} whose induced distances collide: |p-q| == |r-t| for pairs {p,q} != {r,t}
    by={}
    for p,q in itertools.combinations(P,2): by.setdefault(q-p,[]).append((p,q))
    C=set()
    for d,prs in by.items():
        for a,b in itertools.combinations(prs,2): C.add(tuple(sorted(set(a)|set(b))))
    return C
def sidon_ge(P,C,k):
    n=len(P); top=n
    enc=CardEnc.atleast(lits=list(range(1,n+1)),bound=k,top_id=top,encoding=EncType.seqcounter)
    with Solver(name='cadical153',bootstrap_with=enc.clauses) as s:
        for c in C: s.add_clause([-(P.index(x)+1) for x in c])
        r=s.solve()
        if r:
            m=s.get_model(); T=[P[i] for i in range(n) if m[i]>0]
            ds=[q-p for p,q in itertools.combinations(T,2)]
            assert len(ds)==len(set(ds)) and len(T)>=k
        return r
if __name__=='__main__':
    # controls: 4-AP has max Sidon 3; {0,1,4,6} is Sidon(4)
    P=[0,1,2,3]; C=dist_conflicts(P); assert sidon_ge(P,C,3) and not sidon_ge(P,C,4)
    P=[0,1,4,6]; C=dist_conflicts(P); assert sidon_ge(P,C,4)
    for K in range(int(sys.argv[1])+1):
        P=construct(K); C=dist_conflicts(P); m=7+5*K
        a=sidon_ge(P,C,m); b=sidon_ge(P,C,m+1)
        print(f'K={K} n={len(P)} conflicts={len(C)} sidon>={m}:{a} sidon>={m+1}:{b}',flush=True)
        assert a and not b
