# Witness test: ER(q) is a solution of fsenc.build(base+R1+R1b) with S = pairwise non-adjacent passants (highs).
# Descend it by violating class transpositions to the lex-leader side, then the FULL CNF (with SB) must accept it.
import itertools, sys
sys.path.insert(0,'/home/exedev/MathDyad/erdos85/fs')
import fsenc, c4cnf
from pysat.solvers import Cadical153
q=int(sys.argv[1]); nh=int(sys.argv[2])
pts=[]
for v in itertools.product(range(q),repeat=3):
    if v==(0,0,0): continue
    f=next(z for z in v if z); inv=pow(f,q-2,q); w=tuple(z*inv%q for z in v)
    if w not in pts: pts.append(w)
n=len(pts); dot=lambda u,v: sum(a*b for a,b in zip(u,v))%q
E=[(i,j) for i,j in itertools.combinations(range(n),2) if dot(pts[i],pts[j])==0]
adj={v:set() for v in range(n)}
for i,j in E: adj[i].add(j); adj[j].add(i)
deg=[len(adj[v]) for v in range(n)]
ab={i for i in range(n) if dot(pts[i],pts[i])==0}
passant=[x for x in range(n) if x not in ab and not (adj[x]&ab)]
S=[]
for x in passant:
    if all(x not in adj[y] for y in S) and len(S)<nh: S.append(x)
fixed=[e for e in E if e[0] in S or e[1] in S]
target={v:deg[v] for v in range(n) if v not in S}
cnf,var,F,adjS,st,cls=fsenc.build(n,S,fixed,target,highs=S,sb="all",r1=True,r1b=True,hdeg=q+1)
X={e for e in E if e[0] not in S and e[1] not in S}
def rows(X):
    a={u:set(adjS[u]) for u in range(n)}
    for u,w in X: a[u].add(w); a[w].add(u)
    return a
steps=0
while True:
    a=rows(X); moved=False
    for C in cls:
        for i,j in itertools.combinations(C,2):
            if [k in a[i] for k in range(n) if k not in (i,j)] > [k in a[j] for k in range(n) if k not in (i,j)]:
                sw=lambda v: j if v==i else i if v==j else v
                X={tuple(sorted((sw(u),sw(w)))) for u,w in X}; moved=True; steps+=1; break
        if moved: break
    if not moved: break
d2,mc=c4cnf.check_graph(n,fixed+list(X))
with Cadical153(bootstrap_with=cnf.clauses) as s:
    okfull=s.solve(assumptions=[var[e] if e in X else -var[e] for e in var])
    orig={e for e in E if e[0] not in S and e[1] not in S}
    okorig=s.solve(assumptions=[var[e] if e in orig else -var[e] for e in var])
print(f"ER({q}) n={n} highs={len(S)} classes={st['sb_classes']} r1={st['r1_clauses']} r1b={st['r1b_clauses']} descent_steps={steps} "
      f"descended_is_valid={all(d2[u]==deg[u] for u in range(n)) and mc==1} FULL_CNF_accepts_descended={okfull} (raw ER accepted={okorig})")
