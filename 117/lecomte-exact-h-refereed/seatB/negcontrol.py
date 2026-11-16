# Negative control: with a deliberately lowered profile T'(n)=T(n)-1 the checker must flag violations,
# and an independent max-clique (networkx, on the noncommuting graph) must agree with the CP-SAT omega.
import solve, networkx as nx
solve_T = solve.T
solve.T = lambda n: solve_T(n) - 1
for g in solve.parse('controls.dat'):
    res = solve.analyse(g)
    idv = g['id']; V = [v for v in range(1, g['n']+1) if v != idv]
    NC = nx.Graph(); NC.add_nodes_from(V)
    for i, v in enumerate(V):
        for w in V[i+1:]:
            if w not in g['comm'][v]: NC.add_edge(v, w)
    om_nx = max(len(c) for c in nx.find_cliques(NC)) if g['n'] <= 36 or g['label'] in ('E3^1+4',) else None
    print(g['label'], res['omega'], om_nx, res['a'], solve.verdict(res))
