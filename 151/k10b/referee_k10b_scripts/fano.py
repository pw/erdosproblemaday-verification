import sys, subprocess, numpy as np, networkx as nx
for n in range(7, int(sys.argv[1])+1):
    out = subprocess.run(['nice','-n','19','nauty-genbg','-q','-c','-d3:3','-D3:3',str(n),str(n)],capture_output=True,text=True).stdout.split()
    cs = np.arange(1<<n, dtype=np.int64); bad=[]
    for s in out:
        G = nx.from_graph6_bytes(s.encode())
        masks=[sum(1<<u for u in G[e]) for e in range(n,2*n)]
        ok=np.ones(1<<n,dtype=bool)
        for m in masks:
            x=cs&m; ok &= (x!=0)&(x!=m)
            if not ok.any(): break
        if not ok.any(): bad.append(s)
    print(f"n={n}: connected 3-uniform 3-regular hypergraphs {len(out)}; NOT 2-colourable: {len(bad)} {bad[:3]}", flush=True)
