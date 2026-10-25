# Non-vacuity check of the HYPOTHESIS BCLEventual. Lean proves (BCLCertificate/Bridge.lean:60) that BCLEventual
# implies BCLCutCertificate H for EVERY nonempty finite triangle-free H, i.e. D2(H) <= (2/47)|H|^2 at every order.
# If some small triangle-free graph violated that, BCLEventual would be FALSE and the theorem vacuous.
# Here: exact D2 = min over bipartitions of internal edges, all triangle-free graphs n<=N (nauty geng -t).
import sys, subprocess, itertools, numpy as np, networkx as nx
from fractions import Fraction as Q
for n in range(int(sys.argv[2]), int(sys.argv[1])+1):
    out = subprocess.run(['nauty-geng','-t','-q',str(n)],capture_output=True,text=True).stdout.split()
    # all bipartitions with vertex 0 fixed in side X (WLOG)
    X = np.array([[1]+[ (b>>i)&1 for i in range(n-1)] for b in range(2**(n-1))],dtype=np.int32)
    Y = 1-X
    worst=Q(-1); wg=None; B=[]
    def flush():
        global worst,wg
        if not B: return
        T=np.array([b[1] for b in B],dtype=np.int32)
        I = (np.einsum('si,gij,sj->gs',X,T,X)+np.einsum('si,gij,sj->gs',Y,T,Y))//2
        d2 = I.min(axis=1)
        j=int(d2.argmax()); r=Q(int(d2[j]),n*n)
        if r>worst: worst=r; wg=(B[j][0],int(d2[j]))
        B.clear()
    for s in out:
        G=nx.from_graph6_bytes(s.encode()); B.append((s,nx.to_numpy_array(G,dtype=np.int32,nodelist=range(n))))
        if len(B)>=2000: flush()
    flush()
    print(f"n={n:2d} graphs={len(out):7d} max D2/n^2={worst} ({float(worst):.5f}) vs 2/47={2/47:.5f} vs 1/25={1/25:.5f} ok={worst<=Q(2,47)} witness={wg}",flush=True)
