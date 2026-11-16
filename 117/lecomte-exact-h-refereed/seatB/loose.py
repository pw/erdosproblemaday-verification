# Search for the Section 7 "loose case": class-2 binary group with z=64, a(G)=1+sqrt(z)=9 and an
# abelian subgroup whose image in G/Z(G) has order > 8 (here: forms vanishing on a fixed 4-space Y).
import random, sys
from class2 import rank2, form_val, comm_structure, solve_graph
rng = random.Random(int(sys.argv[1])); nu = 6; found = 0
for t in range(int(sys.argv[2])):
    e = rng.choice([2, 3, 4])
    Bs = []
    for _ in range(e):
        B = [0] * nu
        for i in range(nu):
            for j in range(i + 1, nu):
                if i < 4 and j < 4: continue          # Y = <e0..e3> totally isotropic
                if rng.random() < 0.5: B[i] |= 1 << j; B[j] |= 1 << i
        Bs.append(B)
    beta = comm_structure(Bs, nu); V = list(range(1, 64))
    if any(all(beta(v, 1 << j) == 0 for j in range(nu)) for v in V): continue
    om, ex, a, nmax = solve_graph(V, lambda v, w: beta(v, w) == 0, tl=30)
    if a <= 9:
        found += 1; print('a=%d omega=%d e=%d  (Y of order 16 is abelian)' % (a, om, e), Bs, flush=True)
        if found >= 3: break
print('done, found', found)
