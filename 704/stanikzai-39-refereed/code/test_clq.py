import random, subprocess, networkx as nx, sys, os
random.seed(int(sys.argv[1]) if len(sys.argv)>1 else 1)
def write(n, E, path):
    with open(path,'w') as f:
        f.write(f"p edge {n} {len(E)}\n")
        for a,b in E: f.write(f"e {a+1} {b+1}\n")
bad=0; runs=0
for trial in range(300):
    n=random.randint(5,60); p=random.choice([0.3,0.5,0.7,0.8,0.9])
    E=[(i,j) for i in range(n) for j in range(i+1,n) if random.random()<p]
    if random.random()<0.3 and n>12:   # plant a clique
        s=random.randint(5,min(n,18)); S=random.sample(range(n),s)
        Es=set(E)|{(min(a,b),max(a,b)) for a in S for b in S if a<b}; E=sorted(Es)
    G=nx.Graph(); G.add_nodes_from(range(n)); G.add_edges_from(E)
    w=max((len(c) for c in nx.find_cliques(G)), default=1)
    write(n,E,'/tmp/t704.col')
    for tau in [w-1,w,w+1]:
        if tau<1: continue
        out=subprocess.run(['./clq','/tmp/t704.col',str(tau)],capture_output=True,text=True).stdout.split()
        runs+=1
        exp = tau<=w
        got = out[0]=='SAT'
        if got:
            C=[int(x)-1 for x in out[1:]]
            ok = len(C)==tau and len(set(C))==tau and all(G.has_edge(a,b) for i,a in enumerate(C) for b in C[i+1:])
            if not ok: bad+=1; print('BAD WITNESS',n,tau)
        if got!=exp: bad+=1; print('MISMATCH',n,p,tau,w,out[:2])
print('runs',runs,'bad',bad)
