# Independent sanity check of R(C_m,K_n) = (m-1)(n-1)+1 for small m>=n>=3 and of the (3,3) exception.
# Encodes "graph G on N vertices with no C_m (as a subgraph, non-induced) and alpha(G) <= n-1" as SAT.
# Also verifies the lower-bound construction (n-1)K_{m-1} directly (no C_m, alpha = n-1).
import itertools, sys, time
from pysat.solvers import Cadical153
import networkx as nx

def var(i,j,N):
    if i>j: i,j=j,i
    return i*N - i*(i+1)//2 + (j-i-1) + 1

def cycles(N,m):
    # each m-cycle on vertex set as sequence starting at min vertex, second < last
    for S in itertools.combinations(range(N),m):
        a=S[0]
        for perm in itertools.permutations(S[1:]):
            if perm[0] < perm[-1]:
                seq=(a,)+perm
                yield [(seq[t],seq[(t+1)%m]) for t in range(m)]

def solve(N,m,n):
    s=Cadical153()
    for cyc in cycles(N,m):
        s.add_clause([-var(i,j,N) for i,j in cyc])
    for I in itertools.combinations(range(N),n):
        s.add_clause([var(i,j,N) for i,j in itertools.combinations(I,2)])
    r=s.solve(); model=s.get_model() if r else None; s.delete()
    return r, model

def check_witness(N,m,n,model):
    G=nx.Graph(); G.add_nodes_from(range(N))
    pos=set(x for x in model if x>0)
    for i,j in itertools.combinations(range(N),2):
        if var(i,j,N) in pos: G.add_edge(i,j)
    # verify no C_m by brute force over cycles and alpha <= n-1
    for cyc in cycles(N,m):
        if all(G.has_edge(i,j) for i,j in cyc): return False
    for I in itertools.combinations(range(N),n):
        if not any(G.has_edge(i,j) for i,j in itertools.combinations(I,2)): return False
    return True

def construction_ok(m,n):
    G=nx.disjoint_union_all([nx.complete_graph(m-1) for _ in range(n-1)])
    N=G.number_of_nodes()
    # no C_m: every component has m-1 < m vertices; check alpha = n-1 via complement clique number
    comp_ok = all(len(c) < m for c in nx.connected_components(G))
    alpha = max(len(c) for c in nx.find_cliques(nx.complement(G)))
    return N, comp_ok, alpha

pairs=[(3,3),(4,3),(5,3),(6,3),(4,4),(5,4),(6,4),(5,5)]
for m,n in pairs:
    f=(m-1)*(n-1)+1
    Nc,comp_ok,alpha=construction_ok(m,n)
    t=time.time()
    lo,mod=solve(f-1,m,n)
    wit = check_witness(f-1,m,n,mod) if lo else None
    hi,_=solve(f,m,n)
    extra=''
    if (m,n)==(3,3):
        hi6,_=solve(6,3,3); extra=f' | N=6 SAT? {hi6} (expect False: R(3,3)=6)'
    print(f'(m,n)=({m},{n}) formula={f} | construction (n-1)K_(m-1): N={Nc}, comps<m={comp_ok}, alpha={alpha} | N={f-1} SAT? {lo} (witness verified {wit}) | N={f} SAT? {hi}{extra} | {time.time()-t:.1f}s', flush=True)
