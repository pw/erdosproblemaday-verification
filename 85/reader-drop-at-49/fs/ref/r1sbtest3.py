import itertools, sys
sys.path.insert(0,'/tmp/fsref'); sys.path.insert(0,'/home/exedev/MathDyad/erdos85/fs')
import fsenc, c4cnf
from r1sbtest import enum
def case(h,blocks,tgt,label):
    n=h+len(blocks); S=list(range(h)); fixed=[(x,h+i) for i,b in enumerate(blocks) for x in b]
    target={v:tgt(v,blocks[v-h]) for v in range(h,n)}
    hdeg=sum(1 for a,_ in fixed if a==0)
    base,var,F,adjS=c4cnf.build(n,S,fixed,target)
    cnf,_,_,_,st,_=fsenc.build(n,S,fixed,target,highs=S,sb=False,r1=True,r1b=True,hdeg=hdeg)
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
    print(f"{label}: n={n} vars={len(var)} classes={[len(c) for c in cls2]} base={len(B)} R1R1b={len(R)} sem={len(sem)} eq={R==sem} SB={len(SB)} orbits={len(orb)} covered={cov} lexmis={lexmis}",flush=True)
c=lambda k: (lambda v,b: k)
import sys
which=int(sys.argv[1])
CASES=[
lambda: case(1,[(0,)]*4+[()]*4,lambda v,b: 3 if b else 2,"h1 D4 N3 out2"),
lambda: case(1,[(0,)]*4+[()]*8,lambda v,b: 4 if b else 3,"h1 D4 N4 out3"),
lambda: case(1,[(0,)]*4+[()]*8,lambda v,b: 4 if b else 2,"h1 D4 N4 out2"),
lambda: case(1,[(0,)]*6+[()]*6,lambda v,b: 3 if b else 2,"h1 D6 N3 out2"),
lambda: case(1,[(0,)]*6+[()]*6,lambda v,b: 3 if b else 3,"h1 D6 N3 out3"),
lambda: case(2,[(0,1)]+[(0,)]*3+[(1,)]*3,c(3),"h2 D4 d3 n0=0"),
lambda: case(2,[(0,1)]+[(0,)]*3+[(1,)]*3+[()]*2,lambda v,b: 3 if b else 2,"h2 D4 d3 +2 empties t2"),
lambda: case(2,[(0,1)]+[(0,)]*3+[(1,)]*3+[()]*3,lambda v,b: 3 if b else 2,"h2 D4 d3 +3 empties t2"),
lambda: case(3,[(0,1,2)]+[(0,)]*3+[(1,)]*3+[(2,)]*3,c(3),"h3 T=1 D4 d3"),
lambda: case(3,[(0,1),(0,2),(1,2)]+[(0,)]*2+[(1,)]*2+[(2,)]*2,c(3),"h3 pairs D4 d3"),
lambda: case(3,[(0,1),(0,2),(1,2)]+[(0,)]*2+[(1,)]*2+[(2,)]*2+[()]*2,lambda v,b: 3 if b else 2,"h3 pairs D4 +2e")
]
CASES[which]()
