"""Referee: second, independent stabilizer computation via nauty on the point-line incidence graph of PG(2,11)
with S coloured. Points and lines in DIFFERENT colour classes => automorphisms are collineations only
(PGammaL(3,11) = PGL(3,11) since 11 is prime). A second run puts S and its 4-secants in one class, which
admits correlations S <-> 4-secants (dualities), to separate collineations from dualities."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rpg, pynauty
p = 11; HERE = os.path.dirname(os.path.abspath(__file__))
pts, idx, lines, inc = rpg.plane(p); n = len(pts)
W = json.load(open(os.path.join(HERE, '..', 'runs', 'witnesses_q11_c4.json')))
adj = {i: [] for i in range(2 * n)}
for li, l in enumerate(inc):
    for i in l: adj[n + li].append(i); adj[i].append(n + li)
for key in ('cadical', 'cpsat'):
    S = {idx[rpg.norm(P, p)] for P in W[key]}
    four = {n + li for li, l in enumerate(inc) if len(l & S) == 4}
    # (1) collineations only
    g = pynauty.Graph(2 * n, adjacency_dict=adj, vertex_coloring=[S, set(range(n)) - S, set(range(n, 2 * n))])
    gens, grpsize1, grpsize2, orbits, norb = pynauty.autgrp(g)
    print(f"[{key}] nauty, colours (S | other points | lines): |Aut| = {grpsize1 * 10 ** grpsize2:.0f}")
    # (2) allow dualities mapping S <-> 4-secants
    A = S | four
    g2 = pynauty.Graph(2 * n, adjacency_dict=adj, vertex_coloring=[A, set(range(2 * n)) - A])
    gens2, s1, s2, orbits2, _ = pynauty.autgrp(g2)
    swaps = sum(1 for perm in gens2 if perm[next(iter(S))] >= n)
    print(f"[{key}] nauty, colours (S u 4-secants | rest): |Aut| = {s1 * 10 ** s2:.0f} ; generators swapping points<->lines: {swaps}")
    # (3) abstract configuration: 21 points + 21 four-lines (Levi graph), no colours
    Sl = sorted(S); Fl = sorted(four); m = len(Sl)
    adj3 = {i: [] for i in range(2 * m)}
    for a, P in enumerate(Sl):
        for b, L in enumerate(Fl):
            if P in inc[L - n]: adj3[a].append(m + b); adj3[m + b].append(a)
    g3 = pynauty.Graph(2 * m, adjacency_dict=adj3)
    _, t1, t2, orb3, _ = pynauty.autgrp(g3)
    g3c = pynauty.Graph(2 * m, adjacency_dict=adj3, vertex_coloring=[set(range(m)), set(range(m, 2 * m))])
    _, u1, u2, _, _ = pynauty.autgrp(g3c)
    print(f"[{key}] abstract (21_4) Levi graph: |Aut| = {t1 * 10 ** t2:.0f} (incl. dualities), {u1 * 10 ** u2:.0f} (points->points)")
    # (4) abstract configuration with the 28 three-secants too (49 lines)
    T = sorted(n + li for li, l in enumerate(inc) if len(l & S) >= 3)
    adj4 = {i: [] for i in range(m + len(T))}
    for a, P in enumerate(Sl):
        for b, L in enumerate(T):
            if P in inc[L - n]: adj4[a].append(m + b); adj4[m + b].append(a)
    g4 = pynauty.Graph(m + len(T), adjacency_dict=adj4, vertex_coloring=[set(range(m)), set(range(m, m + len(T)))])
    _, v1, v2, _, _ = pynauty.autgrp(g4)
    print(f"[{key}] abstract 21 points + 49 lines (3- and 4-secants): |Aut| = {v1 * 10 ** v2:.0f}")
