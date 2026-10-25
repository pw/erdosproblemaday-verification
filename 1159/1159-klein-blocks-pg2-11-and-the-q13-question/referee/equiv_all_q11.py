"""Referee: every 21-point q=11 witness file in runs/ vs the cadical witness, by nauty certificate of the
coloured Levi graph (S-points | other points | lines). For prime q, collineation = projectivity."""
import json, os, sys, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rpg, pynauty
p = 11; HERE = os.path.dirname(os.path.abspath(__file__)); RUNS = os.path.join(HERE, '..', 'runs')
pts, idx, lines, inc = rpg.plane(p); n = len(pts)
adj = {i: [] for i in range(2 * n)}
for li, l in enumerate(inc):
    for j in l: adj[j].append(n + li); adj[n + li].append(j)
cert = lambda S: pynauty.certificate(pynauty.Graph(2 * n, adjacency_dict=adj, vertex_coloring=[set(S), set(range(n)) - set(S), set(range(n, 2 * n))]))
ref = cert({idx[rpg.norm(P, p)] for P in json.load(open(os.path.join(RUNS, 'witnesses_q11_c4.json')))['cadical']})
for f in sorted(glob.glob(os.path.join(RUNS, '*witness*q11*.json'))):
    d = json.load(open(f)); items = d.items() if isinstance(d, dict) else [('', d)]
    for k, v in items:
        if not v: print(os.path.basename(f), k, ": empty"); continue
        S = {idx[rpg.norm(P, p)] for P in v}
        print(os.path.basename(f), k, f"|S|={len(S)} equivalent to cadical witness:", cert(S) == ref)
