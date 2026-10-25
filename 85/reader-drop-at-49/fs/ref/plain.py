# independent plain CNF for C4-free with min degree d
import itertools, subprocess, sys
from pysat.card import CardEnc, EncType
from pysat.formula import CNF
d=int(sys.argv[1]); n=int(sys.argv[2]); cap=sys.argv[3]; extra=sys.argv[4] if len(sys.argv)>4 else ""
var={}
for a,b in itertools.combinations(range(n),2): var[(a,b)]=len(var)+1
X=lambda a,b: var[(min(a,b),max(a,b))]
cnf=CNF(); top=len(var)
for v in range(n):
    lits=[X(v,w) for w in range(n) if w!=v]
    e=CardEnc.atleast(lits=lits,bound=d,top_id=top,encoding=EncType.seqcounter); top=max(top,e.nv); cnf.extend(e.clauses)
    e=CardEnc.atmost(lits=lits,bound=d+1,top_id=top,encoding=EncType.seqcounter); top=max(top,e.nv); cnf.extend(e.clauses)
for a,b in itertools.combinations(range(n),2):
    o=[p for p in range(n) if p not in (a,b)]
    for p,q in itertools.combinations(o,2):
        cnf.append([-X(a,p),-X(b,p),-X(a,q),-X(b,q)])
# optional: number of degree-(d+1) vertices fixed via extra 'hN' : force vertices 0..N-1 high, rest low
if extra.startswith('h'):
    hh=int(extra[1:])
    for v in range(n):
        lits=[X(v,w) for w in range(n) if w!=v]
        e=CardEnc.equals(lits=lits,bound=(d+1 if v<hh else d),top_id=top,encoding=EncType.seqcounter); top=max(top,e.nv); cnf.extend(e.clauses)
path=f"/tmp/fsref/plain_d{d}_n{n}{extra}.cnf"; cnf.to_file(path)
out=subprocess.run(["timeout",cap,"nice","-n","19",str(__import__('pathlib').Path.home()/"MathDyad/tools/kissat/build/kissat"),"-q",path],capture_output=True,text=True).stdout
v="UNSAT" if "s UNSATISFIABLE" in out else "SAT" if "s SATISFIABLE" in out else "UNKNOWN"
print(v)
if v=="SAT":
    m=set(int(t) for l in out.splitlines() if l.startswith("v ") for t in l[2:].split() if int(t)>0)
    E=[e for e,i in var.items() if i in m]
    adj=[set() for _ in range(n)]
    for a,b in E: adj[a].add(b); adj[b].add(a)
    degs=[len(s) for s in adj]; mc=max(len(adj[a]&adj[b]) for a,b in itertools.combinations(range(n),2))
    print("degs",sorted(degs),"maxcodeg",mc)
    open(f"/tmp/fsref/plain_d{d}_n{n}{extra}.edges","w").write(repr(E))
