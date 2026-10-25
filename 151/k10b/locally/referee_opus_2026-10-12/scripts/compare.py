# Run BOTH searches on the same X / NMAX and compare canonical forms (nauty labelg).
import sys, importlib.util, time, subprocess, io, contextlib, networkx as nx
X=sys.argv[1]; NM=int(sys.argv[2]); which=sys.argv[3] if len(sys.argv)>3 else "both"
spec=importlib.util.spec_from_file_location("indep","/tmp/ref151/scripts/indep_search.py"); I=importlib.util.module_from_spec(spec); spec.loader.exec_module(I)
k,Xadj=I.make_X(X)
def canon(g6s):
    if not g6s: return []
    return sorted(set(subprocess.run(["nauty-labelg","-q"],input="\n".join(g6s)+"\n",capture_output=True,text=True).stdout.split()))
res={}
if which in ("both","indep"):
    t=time.time(); S=I.Indep(k,Xadj,NM); S.run()
    for g in S.out: assert all(I.link_is_X(g,v,k,Xadj) for v in range(len(g)))
    res['indep']=canon([I.to_g6(g) for g in S.out]); print(f"[indep] {X} NMAX={NM}: {len(res['indep'])} graphs, orders {[ord(c[0])-63 for c in res['indep']]}, nodes {S.nodes}, {time.time()-t:.1f}s", flush=True)
if which in ("both","locally"):
    sys.path.insert(0,"/home/exedev/MathDyad/erdos151/locally"); import locally
    XG=nx.Graph(); XG.add_nodes_from(range(k)); XG.add_edges_from((a,b) for a in range(k) for b in range(a+1,k) if (Xadj[a]>>b)&1)
    t=time.time(); L=locally.Search(XG, NM)
    with contextlib.redirect_stdout(io.StringIO()): L.run()
    res['locally']=canon([nx.to_graph6_bytes(G,header=False).decode().strip() for G in L.found]); print(f"[locally.py] {X} NMAX={NM}: {len(res['locally'])} graphs, orders {[ord(c[0])-63 for c in res['locally']]}, nodes {L.nodes}, {time.time()-t:.1f}s", flush=True)
if len(res)==2: print("AGREE" if res['indep']==res['locally'] else "DISAGREE", flush=True)
for c in res.get('indep',res.get('locally',[])): print("   ", ord(c[0])-63, c)
