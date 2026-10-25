"""Host seat's own direct check of Prop 3.1: t(C4,G) - rho^3 + gamma*rho >= 0 on every
triangle-free graph on <= NMAX vertices (nauty-geng -t), exact rationals. hom density via trace(A^4).
Mutation control: with gamma' = 3/64 - 1/1000 the Clebsch graph (16 vertices) must VIOLATE, and
we also report the minimum of g over the enumeration and where it occurs."""
import sys, subprocess
from fractions import Fraction as F
import networkx as nx
GAMMA = F(3,64) + F(1,50_000_000_000)
def g_of(G, gamma=GAMMA):
    n = G.number_of_nodes(); A = nx.to_numpy_array(G, dtype=object)
    import numpy as np
    A2 = A.dot(A); A4 = A2.dot(A2)
    hom = F(int(sum(A4[i][i] for i in range(n))))
    t = hom / F(n)**4
    rho = F(2*G.number_of_edges()) / F(n)**2
    return t - rho**3 + gamma*rho, t, rho
NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 10
worst = (None, None, None)
total = 0
for n in range(1, NMAX+1):
    out = subprocess.run(['nauty-geng', '-t', '-q', str(n)], capture_output=True, text=True).stdout.split()
    for g6 in out:
        G = nx.from_graph6_bytes(g6.encode()); total += 1
        val, t, rho = g_of(G)
        if val < 0:
            print("VIOLATION", n, g6, val); sys.exit(1)
        if worst[0] is None or val < worst[0]:
            worst = (val, n, g6)
print(f"checked {total} triangle-free graphs on 1..{NMAX} vertices: all g >= 0")
print(f"min g = {worst[0]} = {float(worst[0]):.6e} at n={worst[1]} graph6={worst[2]}")
# named graphs incl. Clebsch (tight) and the C5 blow-ups
clebsch = nx.Graph()
# Clebsch = 5-regular folded 5-cube: vertices = even-weight 5-bit strings... use the standard: Z_2^4 with x~y iff x+y in {e_i} or all-ones
V = list(range(16)); E = []
gens = [1,2,4,8,15]
for x in V:
    for s in gens:
        y = x ^ s
        if x < y: E.append((x,y))
clebsch.add_edges_from(E)
assert nx.is_regular(clebsch) and clebsch.degree[0]==5 and sum(nx.triangles(clebsch).values())==0
for name, G in [("C5", nx.cycle_graph(5)), ("Petersen", nx.petersen_graph()), ("Clebsch", clebsch),
                ("K_{8,8}", nx.complete_bipartite_graph(8,8)), ("C5 blow-up x3", nx.Graph([(5*a+i,5*b+j) for a in range(5) for b in [(a+1)%5] for i in range(3) for j in range(3)]))]:
    val, t, rho = g_of(G)
    print(f"{name:14s} rho={rho} t(C4)={t} g={val} ({float(val):.3e})")
# mutation control
bad = g_of(clebsch, gamma=F(3,64) - F(1,1000))[0]
print("mutation control (gamma=3/64-1/1000) on Clebsch:", bad, "VIOLATES" if bad < 0 else "NOT DETECTED <- BAD")
assert bad < 0
