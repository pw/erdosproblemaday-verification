#!/usr/bin/env python3
"""Case (b) of the K4-free core at k = 10 (Erdős #151, NOTES_k10b.md T6/T7): enumerate connected graphs on <= NMAX
vertices in which every vertex's induced neighbourhood is one of an allowed FAMILY of links, under budgets:
  - 'M8' (Wagner)                       : degree 8, deficit 0
  - N8.4, N8.5 (ours; 10 edges)         : degree 8, deficit 2        N8.6 (11 edges): deficit 1
  - N8.1 (10 e), N8.2 (11 e), N8.3 (12 e): degree 8, deficit 2/1/0, EXCEPTIONAL
  - every marked triangle-free 9-vertex graph without isolated vertex (marked9.g6): degree 9, EXCEPTIONAL, 'nine'
Budgets (necessary conditions from T6/T7, so pruning by them loses no core): nine <= 2, exceptional <= 3,
sum(deficit) <= sum over nine-links of (|E| - 13.5) + 2.5*(2 - nine)  (each still-unchosen nine-link adds at most
16 - 13.5 = 2.5; so with two nine-links of e1, e2 edges the deficit is at most e1 + e2 - 27, and a 9-vertex link with
<= 11 edges forces the other to have >= 16 - ... i.e. most low-edge 9-links die at once).  Final filter on a complete graph: nine == 2 and the
two degree-9 vertices adjacent, n >= 21 (F_e(3,3;4) >= 21), exact deficit inequality; then arrowing is tested outside.
Vertex 0 is taken locally M8 without loss of generality (at least n - 8 >= 13 vertices are).  Engine = locally.py's."""
import sys, itertools, time
import networkx as nx
from networkx.algorithms import isomorphism as iso
sys.setrecursionlimit(20000)
W = nx.circulant_graph(8,[1,4])
N8 = {'N8.1':'G?`F`w','N8.2':'G?bF`w','N8.3':'G?rF`w','N8.4':'G?q`qg','N8.5':'GCQb`o','N8.6':'GCR`r_'}
class Link:
    def __init__(self, name, X, deficit, exceptional, nine):
        self.name=name; self.X=nx.convert_node_labels_to_integers(X); self.k=self.X.number_of_nodes()
        self.Xadj=[set(self.X[i]) for i in range(self.k)]
        self.auts=[tuple(m[i] for i in range(self.k)) for m in iso.GraphMatcher(self.X,self.X).isomorphisms_iter()]
        self.deficit=deficit; self.exceptional=exceptional; self.nine=nine; self.edges=self.X.number_of_edges()
def family(marked9_file):
    F=[Link('M8',W,0,False,False)]
    for nm,g6 in N8.items():
        X=nx.from_graph6_bytes(g6.encode()); F.append(Link(nm,X,12-X.number_of_edges(),nm in ('N8.1','N8.2','N8.3'),False))
    for i,line in enumerate(open(marked9_file)):
        s=line.strip()
        if s: F.append(Link(f'L9.{i+1}:{s}',nx.from_graph6_bytes(s.encode()),0,True,True))
    return F
class Search:
    def __init__(self, F, nmax, dump=None, verbose=False):
        self.F=F; self.nmax=nmax; self.dump=dump; self.verbose=verbose; self.found=[]; self.nodes=0; self.t0=time.time()
        self.kmax=max(L.k for L in F)
    def embeddings(self, L, K, adj, non):
        out=[]
        def bt(i,phi,used):
            if i==len(K): out.append(tuple(phi)); return
            u=K[i]
            for x in range(L.k):
                if x in used: continue
                ok=True
                for j in range(i):
                    w=K[j]; ex=(phi[j] in L.Xadj[x])
                    if (w in adj[u] and not ex) or (w in non[u] and ex): ok=False; break
                if ok: phi.append(x); used.add(x); bt(i+1,phi,used); phi.pop(); used.discard(x)
        bt(0,[],set())
        return [phi for phi in out if min(tuple(s[x] for x in phi) for s in L.auts)==phi]
    def run(self):
        L0=self.F[0]; k=L0.k; n=k+1
        adj=[set() for _ in range(n)]; non=[set() for _ in range(n)]
        for i in range(k): adj[0].add(i+1); adj[i+1].add(0)
        for a in range(k):
            for b in range(a+1,k):
                if b in L0.Xadj[a]: adj[a+1].add(b+1); adj[b+1].add(a+1)
                else: non[a+1].add(b+1); non[b+1].add(a+1)
        self.rec(adj,non,{0:L0},1,{'nine':0,'exc':0,'def':0,'ninesum':0.0})
        return self.found
    def record(self, adj, links, budget):
        n=len(adj); G=nx.Graph(); G.add_nodes_from(range(n))
        for u in range(n):
            for w in adj[u]:
                if u<w: G.add_edge(u,w)
        nines=[v for v,L in links.items() if L.nine]
        ok = (len(nines)==2 and G.has_edge(*nines) and n>=21 and budget['def']<=budget['ninesum'])
        tag = "CORE-CANDIDATE" if ok else "family graph (fails final filter)"
        g6=nx.to_graph6_bytes(G,header=False).decode().strip()
        desc={v:L.name.split(':')[0] for v,L in links.items() if L.name!='M8'}
        print(f"  FOUND {tag}: n={n} edges={G.number_of_edges()} nine={nines} exceptional={budget['exc']} deficit={budget['def']} ninesum={budget['ninesum']} non-M8 links={desc}  graph6 {g6}  (nodes {self.nodes}, {time.time()-self.t0:.0f}s)", flush=True)
        if ok:
            for H in self.found:
                if H.number_of_nodes()==n and nx.is_isomorphic(G,H): return
            self.found.append(G)
            if self.dump:
                with open(self.dump,"a") as f: f.write(g6+"\n")
    def rec(self, adj, non, links, v, budget):
        self.nodes+=1
        if self.verbose and self.nodes%200000==0:
            print(f"  ... {self.nodes} nodes, {len(adj)} vertices, v={v}, budget={budget}, {time.time()-self.t0:.0f}s", flush=True)
        n=len(adj)
        if v==n: self.record(adj,links,budget); return
        K=sorted(adj[v])
        if len(K)>self.kmax: return
        U=[u for u in range(n) if u!=v and u not in adj[v] and u not in non[v]]
        for L in self.F:
            if len(K)>L.k: continue
            b=dict(budget)
            if L.nine: b['nine']+=1; b['ninesum']+=L.edges-13.5
            if L.exceptional: b['exc']+=1
            b['def']+=L.deficit
            # necessary: sum(def) <= sum over the (eventually two) nine-links of (|E|-13.5), each at most 16-13.5 = 2.5
            if b['nine']>2 or b['exc']>3 or b['def']>b['ninesum']+2.5*(2-b['nine']): continue
            if len(K)==9 and not L.nine: continue
            for phi in self.embeddings(L,K,adj,non):
                pos={K[i]:phi[i] for i in range(len(K))}
                slots=[s for s in range(L.k) if s not in set(phi)]
                self.fill(adj,non,links,v,L,pos,slots,0,{},U,0,b)
    def fill(self, adj, non, links, v, L, pos, slots, i, assign, U, newcount, b):
        n=len(adj)
        if i==len(slots): self.complete(adj,non,links,v,L,pos,assign,newcount,b); return
        s=slots[i]
        for u in U:
            if u in assign.values(): continue
            ok=True
            for w,pw in pos.items():
                if pw in L.Xadj[s]:
                    if w in non[u] or (w in links and u not in adj[w]): ok=False; break
                else:
                    if w in adj[u]: ok=False; break
            if ok:
                for s2,u2 in assign.items():
                    if u2<0: continue
                    if s2 in L.Xadj[s]:
                        if u2 in non[u]: ok=False; break
                    else:
                        if u2 in adj[u]: ok=False; break
            if ok:
                assign[s]=u; self.fill(adj,non,links,v,L,pos,slots,i+1,assign,U,newcount,b); del assign[s]
        if n+newcount+1<=self.nmax:
            assign[s]=-(newcount+1); self.fill(adj,non,links,v,L,pos,slots,i+1,assign,U,newcount+1,b); del assign[s]
    def complete(self, adj, non, links, v, L, pos, assign, newcount, b):
        n=len(adj); k=L.k
        adj=[set(a) for a in adj]+[set() for _ in range(newcount)]
        non=[set(a) for a in non]+[set() for _ in range(newcount)]
        links=dict(links)
        where=dict(pos)
        for s,u in assign.items():
            if u<0: u=n+(-u)-1
            where[u]=s
        def add_edge(a,c):
            if c in adj[a]: return True
            if a in links or c in links or c in non[a]: return False
            adj[a].add(c); adj[c].add(a)
            return len(adj[a])<=self.kmax and len(adj[c])<=self.kmax
        def add_non(a,c):
            if c in adj[a]: return False
            non[a].add(c); non[c].add(a); return True
        for u in where:
            if u not in adj[v]:
                if not add_edge(v,u): return
        Nv=list(where)
        for a,c in itertools.combinations(Nv,2):
            if where[c] in L.Xadj[where[a]]:
                if not add_edge(a,c): return
            else:
                if not add_non(a,c): return
        if len(adj[v])!=k: return
        links[v]=L
        for u in range(len(adj)):
            if u!=v and u not in adj[v]: non[v].add(u); non[u].add(v)
        self.rec(adj,non,links,v+1,b)
if __name__=="__main__":
    nmax=int(sys.argv[1]); m9=sys.argv[2]; dump=sys.argv[3] if len(sys.argv)>3 else None
    F=family(m9)
    print(f"family: {len(F)} link types ({sum(1 for L in F if L.nine)} nine-vertex), NMAX={nmax}", flush=True)
    S=Search(F,nmax,dump,verbose=True); found=S.run()
    print(f"DONE: {len(found)} core candidate(s): {[(G.number_of_nodes(),G.number_of_edges()) for G in found]}; search nodes {S.nodes}; {time.time()-S.t0:.1f}s", flush=True)
