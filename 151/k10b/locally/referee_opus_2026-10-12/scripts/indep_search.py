#!/usr/bin/env python3
"""Referee's independent enumeration of connected locally-X graphs with <= NMAX vertices.
Written from scratch (no code shared with locally.py).  Differences by design:
 - next vertex to complete = the OPEN vertex with the MOST decided neighbours (ties: lowest index), not index order;
 - Aut(X) computed by own permutation backtracker; orbit representative = lexicographically MAXIMAL map;
 - free positions filled in DECREASING position order; bitmask state;
 - every output graph re-verified (each link explicitly isomorphic to X) and deduplicated by nauty canonical form.
usage: indep_search.py XNAME NMAX [--dump=file]"""
import sys, itertools, time, subprocess
sys.setrecursionlimit(100000)

def make_X(name):
    k = None; E = []
    if name == 'K3': k=3; E=[(0,1),(1,2),(0,2)]
    elif name.startswith('C') and name[1:].isdigit(): k=int(name[1:]); E=[(i,(i+1)%k) for i in range(k)]
    elif name == 'M8': k=8; E=[(i,(i+1)%8) for i in range(8)]+[(i,i+4) for i in range(4)]
    elif name == 'Q3': k=8; E=[(a,b) for a in range(8) for b in range(a+1,8) if bin(a^b).count('1')==1]
    elif name == 'Petersen':
        P=[frozenset(c) for c in itertools.combinations(range(5),2)]; k=10
        E=[(i,j) for i in range(10) for j in range(i+1,10) if not (P[i]&P[j])]
    elif name == 'K33': k=6; E=[(a,b) for a in range(3) for b in range(3,6)]
    elif name == 'Rook33':  # K3 x K3 (3x3 rook graph)
        k=9; E=[(a,b) for a in range(9) for b in range(a+1,9) if (a//3==b//3) != (a%3==b%3)]
    elif name == 'Ico':
        import networkx as nx
        G=nx.icosahedral_graph(); k=12; E=list(G.edges())
    else: raise SystemExit("unknown X")
    adj=[0]*k
    for a,b in E: adj[a]|=1<<b; adj[b]|=1<<a
    return k, adj

def automorphisms(k, adj):
    res=[]
    perm=[-1]*k; used=[False]*k
    def bt(i):
        if i==k: res.append(tuple(perm)); return
        for x in range(k):
            if used[x]: continue
            if bin(adj[i]).count('1') != bin(adj[x]).count('1'): continue
            ok=True
            for j in range(i):
                if ((adj[i]>>j)&1) != ((adj[x]>>perm[j])&1): ok=False; break
            if ok:
                perm[i]=x; used[x]=True; bt(i+1); used[x]=False
        perm[i]=-1
    bt(0); return res

class Indep:
    def __init__(self, k, Xadj, nmax):
        self.k=k; self.X=Xadj; self.nmax=nmax; self.auts=automorphisms(k,Xadj)
        self.out=[]; self.nodes=0; self.t0=time.time()
    def maps(self, K, nb, non):
        """all injective phi: K -> positions with decided pairs respected; keep lexicographically MAX per Aut-orbit"""
        k=self.k; X=self.X; res=[]; phi=[]
        def bt(i, usedmask):
            if i==len(K): res.append(tuple(phi)); return
            u=K[i]
            for x in range(k-1,-1,-1):
                if (usedmask>>x)&1: continue
                ok=True
                for j in range(i):
                    w=K[j]; xa=(X[x]>>phi[j])&1
                    if (nb[u]>>w)&1 and not xa: ok=False; break
                    if (non[u]>>w)&1 and xa: ok=False; break
                if ok: phi.append(x); bt(i+1, usedmask|(1<<x)); phi.pop()
        bt(0,0)
        reps=[]
        for p in res:
            if all(tuple(s[x] for x in p) <= p for s in self.auts): reps.append(p)
        return reps
    def search(self, nb, non, closed):
        self.nodes+=1
        n=len(nb); k=self.k
        openv=[u for u in range(n) if not (closed>>u)&1]
        if not openv:
            self.out.append([nb[u] for u in range(n)]); return
        v=max(openv, key=lambda u:(bin(nb[u]).count('1'), -u))
        K=[u for u in range(n) if (nb[v]>>u)&1]
        if len(K)>k: return
        cand=[u for u in range(n) if u!=v and not (nb[v]>>u)&1 and not (non[v]>>u)&1 and not (closed>>u)&1]
        for phi in self.maps(K, nb, non):
            placed=dict(zip(phi, K))           # position -> vertex
            free=sorted((s for s in range(k) if s not in placed), reverse=True)
            self.fill(nb, non, closed, v, placed, free, 0, cand, 0)
    def fill(self, nb, non, closed, v, placed, free, i, cand, nnew):
        n=len(nb); X=self.X
        if i==len(free):
            self.apply(nb, non, closed, v, placed, nnew); return
        s=free[i]
        usedset=set(placed.values())
        for u in cand:
            if u in usedset: continue
            ok=True
            for t,w in placed.items():
                if w>=n: continue                 # new vertex: no prior relations
                xa=(X[s]>>t)&1
                if xa:
                    if (non[u]>>w)&1: ok=False; break
                    if (closed>>w)&1 and not (nb[u]>>w)&1: ok=False; break
                else:
                    if (nb[u]>>w)&1: ok=False; break
            if ok:
                placed[s]=u; self.fill(nb, non, closed, v, placed, free, i+1, cand, nnew); del placed[s]
        if n+nnew+1 <= self.nmax:
            placed[s]=n+nnew; self.fill(nb, non, closed, v, placed, free, i+1, cand, nnew+1); del placed[s]
    def apply(self, nb, non, closed, v, placed, nnew):
        k=self.k; X=self.X; n=len(nb)
        nb=list(nb)+[0]*nnew; non=list(non)+[0]*nnew
        verts=list(placed.items())
        def edge(a,b):
            if (nb[a]>>b)&1: return True
            if (non[a]>>b)&1 or (closed>>a)&1 or (closed>>b)&1: return False
            nb[a]|=1<<b; nb[b]|=1<<a
            return bin(nb[a]).count('1')<=k and bin(nb[b]).count('1')<=k
        def nonedge(a,b):
            if (nb[a]>>b)&1: return False
            non[a]|=1<<b; non[b]|=1<<a; return True
        for s,u in verts:
            if not edge(v,u): return
        for (s,u),(t,w) in itertools.combinations(verts,2):
            if (X[s]>>t)&1:
                if not edge(u,w): return
            else:
                if not nonedge(u,w): return
        if bin(nb[v]).count('1')!=k: return
        allm=(1<<len(nb))-1
        non[v]|= allm & ~nb[v] & ~(1<<v)
        for u in range(len(nb)):
            if u!=v and not (nb[v]>>u)&1: non[u]|=1<<v
        self.search(nb, non, closed|(1<<v))
    def run(self):
        k=self.k; n=k+1; nb=[0]*n; non=[0]*n
        for i in range(k):
            nb[0]|=1<<(i+1); nb[i+1]|=1
        for a in range(k):
            for b in range(a+1,k):
                if (self.X[a]>>b)&1: nb[a+1]|=1<<(b+1); nb[b+1]|=1<<(a+1)
                else: non[a+1]|=1<<(b+1); non[b+1]|=1<<(a+1)
        self.search(nb, non, 1)

def link_is_X(nbm, v, k, Xadj, auts_unused=None):
    N=[u for u in range(len(nbm)) if (nbm[v]>>u)&1]
    if len(N)!=k: return False
    # explicit isomorphism search N -> X
    perm=[-1]*k; used=[False]*k
    def bt(i):
        if i==k: return True
        for x in range(k):
            if used[x]: continue
            ok=True
            for j in range(i):
                if ((nbm[N[i]]>>N[j])&1) != ((Xadj[x]>>perm[j])&1): ok=False; break
            if ok:
                perm[i]=x; used[x]=True
                if bt(i+1): return True
                used[x]=False
        return False
    return bt(0)

def to_g6(nbm):
    n=len(nbm); bits=[]
    for j in range(1,n):
        for i in range(j): bits.append((nbm[i]>>j)&1)
    while len(bits)%6: bits.append(0)
    s=chr(n+63)
    for i in range(0,len(bits),6):
        val=0
        for b in bits[i:i+6]: val=(val<<1)|b
        s+=chr(val+63)
    return s

if __name__=="__main__":
    name=sys.argv[1]; nmax=int(sys.argv[2])
    dump=None
    for a in sys.argv[3:]:
        if a.startswith("--dump="): dump=a[7:]
    k,Xadj=make_X(name)
    S=Indep(k,Xadj,nmax)
    print(f"[indep] locally {name}: k={k} |Aut X|={len(S.auts)} NMAX={nmax}", flush=True)
    S.run()
    g6s=[]
    for g in S.out:
        assert all(link_is_X(g,v,k,Xadj) for v in range(len(g))), "output graph not locally X"
        g6s.append(to_g6(g))
    raw=len(g6s)
    canon=sorted(set(subprocess.run(["nauty-labelg","-q"],input="\n".join(g6s)+"\n",capture_output=True,text=True).stdout.split())) if g6s else []
    from collections import Counter
    sizes=Counter(ord(c[0])-63 for c in canon)
    print(f"[indep] DONE: {raw} labelled completions, {len(canon)} up to isomorphism; orders {dict(sorted(sizes.items()))}; search nodes {S.nodes}; {time.time()-S.t0:.1f}s", flush=True)
    for c in canon: print("   ", ord(c[0])-63, c)
    if dump:
        with open(dump,"w") as f: f.write("\n".join(canon)+"\n")
