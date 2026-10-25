#!/usr/bin/env python3
"""Control for T0: if G has a (3,3)-free 2-edge-colouring c, then F = red(c) ∪ lone(G) is triangle-free and
every independent set of F is a free set of G (contains no maximal clique of size >= 2); hence beta(G) >= alpha(F).
Exhaustive over all graphs n <= 7 (every (3,3)-free colouring of every graph, by brute force over 2^m colourings)
and 300 random graphs n in 8..12 (one colouring found by CP-SAT).  Mutation: F = red only (lone edges may be blue)
must FAIL the independent-implies-free test somewhere; positive control: K6 has no (3,3)-free colouring."""
import itertools, random, subprocess
import networkx as nx
from ortools.sat.python import cp_model
def maximal_cliques(G): return [frozenset(c) for c in nx.find_cliques(G) if len(c)>=2]
def is_free(S, MC): return not any(C<=S for C in MC)
def beta(G):
    MC=maximal_cliques(G); V=list(G); best=0
    for k in range(len(V),-1,-1):
        if any(is_free(frozenset(c),MC) for c in itertools.combinations(V,k)): return k
def lone_edges(G): return {frozenset(e) for e in G.edges() if not set(G[e[0]])&set(G[e[1]])}
def check_colouring(G, red, MC, mutate=False):
    """red: set of frozenset edges. Returns (ok_tf, ok_free, alphaF, betaG_ge)."""
    F=nx.Graph(); F.add_nodes_from(G); F.add_edges_from(tuple(e) for e in red)
    if not mutate: F.add_edges_from(tuple(e) for e in lone_edges(G))
    tf = sum(nx.triangles(F).values())==0
    free_ok=True
    for I in (frozenset(c) for c in nx.find_cliques(nx.complement(F))):   # maximal independent sets of F
        if not is_free(I,MC): free_ok=False; break
    aF=max(len(c) for c in nx.find_cliques(nx.complement(F)))
    return tf, free_ok, aF
def all_good_colourings(G):
    E=[frozenset(e) for e in G.edges()]; tris=[frozenset(t) for t in nx.enumerate_all_cliques(G) if len(t)==3]
    tri_edges=[[frozenset(p) for p in itertools.combinations(t,2)] for t in tris]
    for mask in range(1<<len(E)):
        red={E[i] for i in range(len(E)) if mask>>i&1}
        if all(not(all(e in red for e in te) or all(e not in red for e in te)) for te in tri_edges): yield red
def one_good_colouring(G):
    E=[frozenset(e) for e in G.edges()]; idx={e:i for i,e in enumerate(E)}
    m=cp_model.CpModel(); x=[m.NewBoolVar(str(i)) for i in E]
    for t in (t for t in nx.enumerate_all_cliques(G) if len(t)==3):
        s=sum(x[idx[frozenset(p)]] for p in itertools.combinations(t,2)); m.Add(s>=1); m.Add(s<=2)
    sv=cp_model.CpSolver(); sv.parameters.num_search_workers=1; r=sv.Solve(m)
    if r==cp_model.INFEASIBLE: return None
    assert r in (cp_model.OPTIMAL,cp_model.FEASIBLE)
    return {E[i] for i in range(len(E)) if sv.Value(x[i])}
assert one_good_colouring(nx.complete_graph(6)) is None, "control: K6 arrows"
assert one_good_colouring(nx.complete_graph(5)) is not None
tested=cols=0; mut_fail=0; viol=0
for n in range(2,8):
    for s in subprocess.run(['nauty-geng','-q','-c',str(n)],capture_output=True,text=True).stdout.split():
        G=nx.from_graph6_bytes(s.encode()); MC=maximal_cliques(G); b=beta(G)
        if G.number_of_edges()>16: continue
        for red in all_good_colourings(G):
            tf,fo,aF=check_colouring(G,red,MC); cols+=1
            if not(tf and fo and aF<=b): viol+=1; print("VIOLATION",s,red)
            tfm,fom,_=check_colouring(G,red,MC,mutate=True)
            if not fom: mut_fail+=1
        tested+=1
print(f"exhaustive: {tested} connected graphs n<=7 (m<=16), {cols} (3,3)-free colourings, violations {viol}, mutation(red only) fails {mut_fail}")
assert viol==0 and mut_fail>0
random.seed(151); rt=0; rv=0
while rt<300:
    n=random.randint(8,12); G=nx.gnp_random_graph(n,random.choice([0.3,0.45,0.6]),seed=random.randrange(10**9))
    red=one_good_colouring(G)
    if red is None: continue
    MC=maximal_cliques(G); tf,fo,aF=check_colouring(G,red,MC); b=beta(G); rt+=1
    if not(tf and fo and aF<=b): rv+=1; print("VIOLATION",nx.to_graph6_bytes(G))
print(f"random: {rt} graphs n in 8..12 with a (3,3)-free colouring, violations {rv}")
assert rv==0
print("T0 CONTROLS PASS")
