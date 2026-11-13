import random, subprocess, networkx as nx
random.seed(11); bad=0; tot=0
for t in range(300):
    n=random.randint(6,28); p=random.choice([0.5,0.7,0.85])
    E=[(i,j) for i in range(n) for j in range(i+1,n) if random.random()<p]
    G=nx.Graph(); G.add_nodes_from(range(n)); G.add_edges_from(E)
    w=max(len(c) for c in nx.find_cliques(G))
    exp=sum(1 for c in nx.enumerate_all_cliques(G) if len(c)==w)
    open('/tmp/e.col','w').write(f"p edge {n} {len(E)}\n"+''.join(f"e {a+1} {b+1}\n" for a,b in E))
    perm=list(range(n)); random.shuffle(perm)
    open('/tmp/e.txt','w').write(f"1 {w} {n} "+' '.join(str(i+1) for i in perm)+"\n")
    out=subprocess.run(['./clq3','/tmp/e.col','/tmp/e.txt'],capture_output=True,text=True).stdout.splitlines()
    sols=[frozenset(l.split()[2:]) for l in out if ' SOL ' in l]
    ok_cl=all(G.has_edge(int(a)-1,int(b)-1) for s in sols for a in s for b in s if a<b)
    tot+=1
    if len(sols)!=exp or len(set(sols))!=len(sols) or not ok_cl: bad+=1; print('MISMATCH',n,w,exp,len(sols))
print('enum tests',tot,'bad',bad)
