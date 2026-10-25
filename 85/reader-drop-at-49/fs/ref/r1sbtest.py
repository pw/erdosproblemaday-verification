# Tiny instances with highs: (1) CNF(base+R1+R1b) solution set == {base solutions with every v!=x having exactly
# one nbr in N(x) for each high x}; (2) orbit coverage of SB-CNF over that set under the class group.
import itertools, sys
sys.path.insert(0,'/home/exedev/MathDyad/erdos85/fs')
import fsenc, c4cnf
from pysat.solvers import Cadical153
def enum(clauses,var,cap=200000):
    sols=set()
    with Cadical153(bootstrap_with=clauses) as s:
        while s.solve():
            m=set(l for l in s.get_model() if l>0)
            sols.add(frozenset(e for e in var if var[e] in m))
            s.add_clause([-var[e] if var[e] in m else var[e] for e in var])
            if len(sols)>cap: raise SystemExit("cap")
    return sols
def case(h,blocks,d):
    n=h+len(blocks); S=list(range(h)); fixed=[(x,h+i) for i,b in enumerate(blocks) for x in b]
    target={v:d for v in range(h,n)}
    hdeg=sum(1 for a,_ in fixed if a==0)
    base,var,F,adjS=c4cnf.build(n,S,fixed,target)
    cnf,var2,_,_,st,cls=fsenc.build(n,S,fixed,target,highs=S,sb=False,r1=True,r1b=True,hdeg=hdeg)
    cnfsb,_,_,_,st2,cls2=fsenc.build(n,S,fixed,target,highs=S,sb="all",r1=True,r1b=True,hdeg=hdeg)
    B=enum(base.clauses,var); R=enum(cnf.clauses,var); SB=enum(cnfsb.clauses,var)
    def adjof(s):
        a={u:set() for u in range(n)}
        for u,w in list(fixed)+list(s): a[u].add(w); a[w].add(u)
        return a
    sem={s for s in B if all(all(len(adjof(s)[v]&adjof(s)[x])==1 for v in range(n) if v!=x) for x in S)}
    par={s:s for s in R}
    def find(a):
        while par[a]!=a: par[a]=par[par[a]]; a=par[a]
        return a
    for s in R:
        for C in cls2:
            for i,j in itertools.combinations(C,2):
                sw=lambda v: j if v==i else i if v==j else v
                t=frozenset(tuple(sorted((sw(a),sw(b)))) for a,b in s)
                assert t in R, "class transposition not a symmetry"
                par[find(s)]=find(t)
    orb={}
    for s in R: orb.setdefault(find(s),[]).append(s)
    cov=sum(1 for o in orb.values() if any(x in SB for x in o))
    lexmis=sum(1 for s in R if fsenc.lex_ok(adjof(s),cls2,n)!=(s in SB))
    print(f"h={h} blocks={blocks} d={d} n={n} vars={len(var)} classes={[len(c) for c in cls2]} base={len(B)} R1R1b={len(R)} sem={len(sem)} eq={R==sem} SB={len(SB)} orbits={len(orb)} covered={cov} lexmismatch={lexmis}",flush=True)
cases=[
 (2,[(0,1),(0,),(0,),(1,),(1,),(),()],2),
 (2,[(0,1),(0,),(0,),(1,),(1,),(),(),()],3),
 (2,[(0,1),(0,),(1,),(),(),()],2),
 (2,[(0,1),(0,),(0,),(1,),(1,),(),(),(),()],3),
 (3,[(0,1,2),(0,),(1,),(2,),(),(),()],3),
 (3,[(0,1),(0,2),(1,2),(0,),(1,),(2,),(),()],3),
 (3,[(0,1,2),(0,),(0,),(1,),(1,),(2,),(2,),(),()],3),
 (1,[(0,),(0,),(0,),(),(),(),(),(),()],3),
 (1,[(0,),(0,),(0,),(0,),(),(),(),(),()],3),
]
if __name__=="__main__":
  for c in cases:
    try: case(*c)
    except AssertionError as e: print("assert",c,e)
