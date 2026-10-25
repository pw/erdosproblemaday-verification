# Positive control: ER(q) polarity graph, passant point(s) as 'highs' (R1/R1b true there), classes active.
import itertools, subprocess, sys
sys.path.insert(0,'/home/exedev/MathDyad/erdos85/fs')
import fsenc, c4cnf
q=int(sys.argv[1]); nh=int(sys.argv[2]); cap=sys.argv[3]
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
# pick nh pairwise non-adjacent passants
S=[]
for x in passant:
    if all(x not in adj[y] for y in S): S.append(x)
    if len(S)==nh: break
assert len(S)==nh, (len(passant),S)
for x in S: assert all(len(adj[v]&adj[x])==1 for v in range(n) if v!=x)   # R1+R1b true for x
fixed=[e for e in E if e[0] in S or e[1] in S]
F=[v for v in range(n) if v not in S]
target={v:deg[v] for v in F}
mode=sys.argv[4] if len(sys.argv)>4 else "all"
cnf,var,F,adjS,st,cls=fsenc.build(n,S,fixed,target,highs=S,sb=("all" if mode!="nosb" else False),r1=True,r1b=True,hdeg=q+1)
path=f"/tmp/fsref/er{q}_{nh}_{mode}.cnf"; cnf.to_file(path)
out=subprocess.run(["timeout",cap,"nice","-n","19","/home/exedev/MathDyad/tools/kissat/build/kissat","-q",path],capture_output=True,text=True).stdout
v="UNSAT" if "s UNSATISFIABLE" in out else "SAT" if "s SATISFIABLE" in out else "UNKNOWN"
note=""
if v=="SAT":
    m=[int(t) for l in out.splitlines() if l.startswith("v ") for t in l[2:].split()]
    ed=fixed+c4cnf.decode(m,var); d2,mc=c4cnf.check_graph(n,ed)
    a2={u:set() for u in range(n)}
    for i,j in ed: a2[i].add(j); a2[j].add(i)
    r1=all(all(len(a2[v]&a2[x])==1 for v in range(n) if v!=x) for x in S)
    note=f"deg_ok={all(d2[u]==deg[u] for u in range(n))} mc={mc} r1r1b={r1} lex={fsenc.lex_ok(a2,cls,n)}"
print(f"ER({q}) n={n} highs={S} free={len(F)} classes={st['sb_classes']} r1={st['r1_clauses']} r1b={st['r1b_clauses']} sb={st['sb_clauses']} -> {v} {note}")
