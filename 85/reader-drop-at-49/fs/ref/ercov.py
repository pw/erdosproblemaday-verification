# Orbit coverage on ER(3) instance: enumerate ALL solutions w/o SB, union by class transpositions,
# enumerate ALL solutions WITH the SB CNF, check every orbit contains >=1 SB-CNF solution.
import itertools, sys
sys.path.insert(0,'/home/exedev/MathDyad/erdos85/fs')
import fsenc, c4cnf
from pysat.solvers import Cadical153
q=3
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
S=[next(x for x in range(n) if x not in ab and not (adj[x]&ab))]
fixed=[e for e in E if e[0] in S or e[1] in S]
target={v:deg[v] for v in range(n) if v not in S}
def enum(sb):
    cnf,var,F,adjS,st,cls=fsenc.build(n,S,fixed,target,highs=S,sb=sb,r1=True,r1b=True,hdeg=q+1)
    sols=set()
    with Cadical153(bootstrap_with=cnf.clauses) as s:
        while s.solve():
            m=set(l for l in s.get_model() if l>0)
            on=frozenset(e for e in var if var[e] in m); sols.add(on)
            s.add_clause([-var[e] if var[e] in m else var[e] for e in var])
    return sols,cls,var
allS,cls,var=enum(False); sbS,cls2,_=enum("all")
print("solutions w/o SB",len(allS),"with SB",len(sbS),"classes",[len(c) for c in cls2])
assert sbS<=allS
par={s:s for s in allS}
def find(a):
    while par[a]!=a: par[a]=par[par[a]]; a=par[a]
    return a
for s in allS:
    for C in cls2:
        for i,j in itertools.combinations(C,2):
            sw=lambda v: j if v==i else i if v==j else v
            t=frozenset(tuple(sorted((sw(a),sw(b)))) for a,b in s)
            assert t in allS
            par[find(s)]=find(t)
orb={}
for s in allS: orb.setdefault(find(s),[]).append(s)
cov=sum(1 for o in orb.values() if any(s in sbS for s in o))
print("orbits",len(orb),"covered by SB-CNF",cov)
# lex-min check: SB-CNF solutions vs lex_ok
bad=0
for s in allS:
    a={u:set(adj[u]) if u in S else set() for u in range(n)}
    for x in S:
        for u in adj[x]: a[u].add(x)
    for u,w in s: a[u].add(w); a[w].add(u)
    if fsenc.lex_ok(a,cls2,n)!=(s in sbS): bad+=1
print("lex_ok vs SB-CNF mismatches",bad)
