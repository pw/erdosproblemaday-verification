# Full-scale check on the real h3_t1 cell: SB clauses (alone) accept X iff lex_ok(X), on random X and on
# lex-descended X (apply violating transpositions until none; each step strictly decreases X in lex order).
import itertools, random, sys
sys.path.insert(0,'/home/exedev/MathDyad/erdos85/fs')
import fsenc, c4cnf
from pysat.solvers import Cadical153
random.seed(7)
H,fixed,target,n0,np_,ns=fsenc.stratum(3,[(0,1,2)])
n=49
cnf0,var,F,adjS,st0,_=fsenc.build(n,H,fixed,target,highs=H,sb=False,r1=True,r1b=True)
cnf,var2,F,adjS,st,cls=fsenc.build(n,H,fixed,target,highs=H,sb="all",r1=True,r1b=True)
assert var==var2 and cnf.clauses[:len(cnf0.clauses)]==cnf0.clauses
sbc=cnf.clauses[len(cnf0.clauses):]
print("sb clauses",len(sbc),"classes",[len(c) for c in cls])
def adjof(X):
    a={u:set(adjS[u]) for u in range(n)}
    for (u,w) in X: a[u].add(w); a[w].add(u)
    return a
def descend(X):
    while True:
        a=adjof(X); moved=False
        for C in cls:
            for i,j in itertools.combinations(C,2):
                ri=[1 if k in a[i] else 0 for k in range(n) if k not in (i,j)]
                rj=[1 if k in a[j] else 0 for k in range(n) if k not in (i,j)]
                if ri>rj:
                    sw=lambda v: j if v==i else i if v==j else v
                    X={tuple(sorted((sw(u),sw(w)))) for u,w in X}; moved=True; break
            if moved: break
        if not moved: return X
mis=0; acc=0; tot=0
with Cadical153(bootstrap_with=sbc) as s:
    for trial in range(300):
        p=random.choice([0.05,0.15,0.5])
        X={e for e in var if random.random()<p}
        for Y in [X, descend(X)]:
            # also a single-flip neighbour of the descended one
            for Z in [Y, Y ^ {random.choice(list(var))}]:
                ok=fsenc.lex_ok(adjof(Z),cls,n)
                enc=s.solve(assumptions=[var[e] if e in Z else -var[e] for e in var])
                tot+=1; acc+=ok; mis+=(ok!=enc)
print("checked",tot,"accepted",acc,"mismatches",mis)
