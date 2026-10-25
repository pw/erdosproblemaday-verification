# Evaluate the Lean definitions C4FlagCertificate / edgeDensityQ / c4DensityQ / BCL-shape on concrete graphs, exact rationals.
from fractions import Fraction as Q
import networkx as nx, numpy as np, itertools
gamma = Q(3,64)+Q(1,50000000000)
def c4hom(G):
    A = nx.to_numpy_array(G, dtype=object, nodelist=sorted(G.nodes()))
    A = np.array([[int(x) for x in r] for r in A], dtype=object)
    A4 = A.dot(A).dot(A).dot(A)
    return sum(A4[i][i] for i in range(len(A)))
def slack(G):  # n^2*hom - (8m^3 - 2*gamma*m*n^4); Lean C4FlagCertificate <=> slack >= 0
    n=G.number_of_nodes(); m=G.number_of_edges(); H=c4hom(G)
    return Q(n**2*H) - (8*Q(m)**3 - 2*gamma*m*Q(n)**4)
def clebsch():
    G=nx.Graph(); V=list(range(16)); G.add_nodes_from(V)
    for u,v in itertools.combinations(V,2):
        w=u^v
        if bin(w).count('1') in (1,4): G.add_edge(u,v)
    return G
tests = {'K2':nx.complete_graph(2),'C5':nx.cycle_graph(5),'Petersen':nx.petersen_graph(),'Clebsch':clebsch(),
 'K_{5,5}':nx.complete_bipartite_graph(5,5),'K3 (NOT triangle-free, control)':nx.complete_graph(3),'K4 (control)':nx.complete_graph(4)}
for k,G in tests.items():
    tf = not any(nx.triangles(G).values())
    s = slack(G); n=G.number_of_nodes(); m=G.number_of_edges()
    r = Q(2*m, n*n); t = Q(c4hom(G), n**4)
    print(f"{k:32s} n={n:2d} m={m:3d} triangle-free={tf!s:5s} r={float(r):.6f} t(C4)={float(t):.6f} r^3-gamma r={float(r**3-gamma*r):.6f} slack={float(s):.6g} cert_holds={s>=0}")
