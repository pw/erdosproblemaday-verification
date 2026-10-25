# analog pipeline: n=d*d, highs deg d+1, lows deg d; uses fsenc's build (patched only for the degree-8 assert)
import itertools, subprocess, sys, json
sys.path.insert(0,'/tmp/fsref')
sys.path.insert(0,"/home/exedev/MathDyad/erdos85/fs"); import fsenc, c4cnf
def stratum_d(d,h,T):
    n=d*d; H=list(range(h)); T=[tuple(b) for b in T]
    cov={frozenset(p) for b in T for p in itertools.combinations(b,2)}
    Pairs=[p for p in itertools.combinations(H,2) if frozenset(p) not in cov]
    r3={x:sum(x in b for b in T) for x in H}
    sing=[(x,) for x in H for _ in range(d+2-h+r3[x])]
    n0=n-h-len(T)-len(Pairs)-len(sing); assert n0>=0,n0
    blocks=T+Pairs+sing+[()]*n0
    fixed=[(x,h+i) for i,b in enumerate(blocks) for x in b]
    assert all(sum(1 for a,_ in fixed if a==x)==d+1 for x in H)
    return n,H,fixed,{v:d for v in range(h,n)},blocks
def run(d,h,T,cap,sb="all",r1=True,r1b=True,units=None,tag=""):

    n,H,fixed,target,blocks=stratum_d(d,h,T)
    cnf,var,F,adjS,st,cls=fsenc.build(n,H,fixed,target,highs=H,sb=sb,r1=r1,r1b=r1b,hdeg=d+1)
    if units:
        for e in units: cnf.append([var[e]])
    path=f"/tmp/fsref/ana_d{d}_h{h}_t{len(T)}{tag}.cnf"; cnf.to_file(path)
    out=subprocess.run(["timeout",str(cap),"nice","-n","19","/home/exedev/MathDyad/tools/kissat/build/kissat","-q",path],capture_output=True,text=True).stdout
    v="UNSAT" if "s UNSATISFIABLE" in out else "SAT" if "s SATISFIABLE" in out else "UNKNOWN"
    note=""
    if v=="SAT":
        m=[int(t) for l in out.splitlines() if l.startswith("v ") for t in l[2:].split()]
        E=fixed+c4cnf.decode(m,var); degs,mc=c4cnf.check_graph(n,E)
        adj={u:set() for u in range(n)}
        for a,b in E: adj[a].add(b); adj[b].add(a)
        note=f"degs={sorted(set(degs))} mc={mc} lex={fsenc.lex_ok(adj,cls,n)}"
    return v,st["sb_classes"],note
if __name__=="__main__":
    d,h=int(sys.argv[1]),int(sys.argv[2]); T=json.loads(sys.argv[3]) if len(sys.argv)>3 else []
    for sb in ["all",False]:
        print(d,h,len(T),"sb=",sb,run(d,h,T,int(sys.argv[4]) if len(sys.argv)>4 else 120,sb=sb),flush=True)
