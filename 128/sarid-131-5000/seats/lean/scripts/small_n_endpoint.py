# Falsification test of the Lean ENDPOINT statement at small n (it has no n>=n0 side condition):
# for every triangle-free graph on n vertices (nauty geng -t, all graphs incl. disconnected),
# min over floor(n/2)-subsets S of e(S) must be <= (131/5000) n^2.
import sys, subprocess, itertools, numpy as np, networkx as nx
from fractions import Fraction as Q
def run(n):
    k = n//2
    out = subprocess.run(['nauty-geng','-t','-q',str(n)],capture_output=True,text=True).stdout.split()
    combos = list(itertools.combinations(range(n),k))
    M = np.zeros((len(combos),n),dtype=np.int32)
    for i,c in enumerate(combos): M[i,list(c)] = 1
    worst = -1; worstg=None; cnt=0
    B=[]
    def flush():
        nonlocal worst,worstg
        if not B: return
        T = np.array([b[1] for b in B],dtype=np.int32)          # g x n x n
        E = np.einsum('si,gij,sj->gs', M, T, M)//2              # g x subsets
        mins = E.min(axis=1)
        j = int(mins.argmax())
        if mins[j] > worst: worst=int(mins[j]); worstg=B[j][0]
        B.clear()
    for s in out:
        G = nx.from_graph6_bytes(s.encode())
        B.append((s, nx.to_numpy_array(G,dtype=np.int32,nodelist=range(n))))
        cnt+=1
        if len(B)>=4000: flush()
    flush()
    bound = Q(131*n*n,5000)
    return cnt, k, worst, worstg, bound
for n in range(int(sys.argv[2]) if len(sys.argv)>2 else 1,int(sys.argv[1])+1):
    cnt,k,worst,g,bound = run(n)
    print(f"n={n:2d} graphs={cnt:7d} k={k} max_G min_S e(S)={worst} bound=131n^2/5000={float(bound):.4f} holds={Q(worst)<=bound} witness={g}", flush=True)
