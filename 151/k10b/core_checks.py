#!/usr/bin/env python3
"""Controls for NOTES_k10b.md.
 (1) R(3,4) = 9 side used in T6: every triangle-free graph on 9 vertices has alpha >= 4 (geng -t 9, brute force alpha by hand,
     no networkx); and exactly 3 triangle-free 8-vertex graphs have alpha <= 3.
 (2) N8.i edge counts / degree sequences / alpha by a hand graph6 parser (second route for the table in T6(iv)).
 (3) T7 on every minimal (3,3)-Ramsey graph with <= 9 vertices, enumerated from scratch: arrowing by CP-SAT on every
     connected graph (geng -c), minimality = no proper subgraph arrows (delete each edge; isolated vertices never matter).
     Positive controls: the enumeration must return exactly {K6} on 6, {} on 7, {K3+C5} on 8, one graph on 9 (Bikov §1,
     Thm 2.4); each must satisfy #triangles >= #edges; and the minimal non-2-colourable sub-hypergraph of its triangle
     hypergraph must use every edge (we check the weaker, directly: deleting any edge makes it 2-colourable).
 (4) The deficit arithmetic: def(i) = 12 - |E(N8.i)|; Mantel bound 20 on 9 vertices (brute force over geng -t 9 edge counts).
Mutation: a non-minimal Ramsey graph (K6 plus a pendant edge) must be rejected by the minimality test."""
import itertools, subprocess, sys
from ortools.sat.python import cp_model
def g6(s):
    b=[ord(c)-63 for c in s]; n=b[0]; bits=''.join(format(x,'06b') for x in b[1:]); E=[]; k=0
    for j in range(1,n):
        for i in range(j):
            if bits[k]=='1': E.append((i,j))
            k+=1
    return n,E
def alpha(n,E):
    adj=[0]*n
    for a,b in E: adj[a]|=1<<b; adj[b]|=1<<a
    best=0
    for mask in range(1<<n):
        ok=True; m=mask
        while m:
            v=(m&-m).bit_length()-1; m&=m-1
            if adj[v]&mask: ok=False; break
        if ok: best=max(best,bin(mask).count('1'))
    return best
def geng(args): return subprocess.run(['nauty-geng','-q']+args,capture_output=True,text=True).stdout.split()
# (1)
t9=geng(['-t','9']); a9=[alpha(*g6(s)) for s in t9]
print(f"(1) triangle-free 9-vertex graphs: {len(t9)}; min alpha = {min(a9)}  (must be >= 4; R(3,4)=9)")
assert min(a9)>=4
t8=geng(['-t','8']); r348=[s for s in t8 if alpha(*g6(s))<=3]
print(f"    triangle-free 8-vertex graphs: {len(t8)}; with alpha<=3: {len(r348)} {r348}"); assert len(r348)==3
print(f"(4) Mantel on 9 vertices: max edges over triangle-free 9-vertex graphs = {max(len(g6(s)[1]) for s in t9)} (must be 20)")
assert max(len(g6(s)[1]) for s in t9)==20
# (2)
N8=['G?`F`w','G?bF`w','G?rF`w','G?q`qg','GCQb`o','GCR`r_','GCrb`o']
for i,s in enumerate(N8,1):
    n,E=g6(s); deg=[0]*n
    for a,b in E: deg[a]+=1; deg[b]+=1
    print(f"(2) N8.{i} {s}: edges={len(E)} degs={sorted(deg)} alpha={alpha(n,E)} deficit={12-len(E)}")
# (3)
from pysat.solvers import Glucose3
def arrows(n,E):
    """G -> (3,3)^e  iff  the 2-colouring CNF (each triangle not all-red, not all-blue) is UNSAT.  pysat/Glucose3."""
    tris=[(a,b,c) for a,b,c in itertools.combinations(range(n),3) if (a,b) in Es and (a,c) in Es and (b,c) in Es]
    if not tris: return False
    idx={e:i+1 for i,e in enumerate(E)}
    with Glucose3() as sv:
        for a,b,c in tris:
            v=[idx[(a,b)],idx[(a,c)],idx[(b,c)]]; sv.add_clause(v); sv.add_clause([-t for t in v])
        return not sv.solve()
def arrows_cpsat(n,E):   # second instrument for the arrowing test, used on the hits + controls only
    tris=[(a,b,c) for a,b,c in itertools.combinations(range(n),3) if (a,b) in Es and (a,c) in Es and (b,c) in Es]
    if not tris: return False
    idx={e:i for i,e in enumerate(E)}; m=cp_model.CpModel(); x=[m.NewBoolVar(str(i)) for i in E]
    for a,b,c in tris:
        s=x[idx[(a,b)]]+x[idx[(a,c)]]+x[idx[(b,c)]]; m.Add(s>=1); m.Add(s<=2)
    sv=cp_model.CpSolver(); sv.parameters.num_search_workers=1; r=sv.Solve(m)
    assert r in (cp_model.OPTIMAL,cp_model.FEASIBLE,cp_model.INFEASIBLE); return r==cp_model.INFEASIBLE
def is_minimal_ramsey(n,E):
    global Es
    Es=set(E)
    if not arrows(n,E): return False
    for e in E:
        E2=[f for f in E if f!=e]; Es=set(E2)
        if arrows(n,E2): return False
    return True
def ntri(n,E):
    S=set(E); return sum(1 for a,b,c in itertools.combinations(range(n),3) if (a,b) in S and (a,c) in S and (b,c) in S)
Es=set()
K6=g6('E~~w'); assert is_minimal_ramsey(*K6); Es=set(K6[1]); assert arrows_cpsat(*K6) and not arrows_cpsat(5,[e for e in K6[1] if 5 not in e])
K6p=(7,K6[1]+[(0,6)]); assert not is_minimal_ramsey(*K6p), "mutation: K6 + pendant edge is Ramsey but not minimal"
found={}
for n in range(6,10):
    gs=geng(['-c',str(n)]); hits=[]
    for s in gs:
        nn,E=g6(s)
        if len(E)<15: continue      # a (3,3)-Ramsey graph has >= 15 edges (K6 is the smallest); cheap prefilter
        if is_minimal_ramsey(nn,E): hits.append(s)
    found[n]=hits
    for s in hits:
        nn,E=g6(s); Es=set(E); assert arrows_cpsat(nn,E), "second instrument (CP-SAT) disagrees on a hit"
        print(f"(3) n={n}: minimal (3,3)-Ramsey {s}: edges={len(E)} triangles={ntri(nn,E)}  T7 {'OK' if ntri(nn,E)>=len(E) else 'VIOLATED'}  (arrowing confirmed by CP-SAT)", flush=True)
        assert ntri(nn,E)>=len(E)
    print(f"(3) n={n}: {len(gs)} connected graphs scanned, {len(hits)} minimal (3,3)-Ramsey", flush=True)
assert len(found[6])==1 and len(found[7])==0 and len(found[8])==1 and len(found[9])==1, found
print("ALL CONTROLS PASS")
