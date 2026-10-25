"""Referee: positive controls for the author's symmetry breaks ON THE ACTUAL CNF FILES.
For the Klein witness S we construct (with our own projective algebra) an image g(S) that satisfies
  (b1)  (0,0,1) in S, line x=0 tangent at it;
  (b2)  (1,0,0) in S, line z=0 tangent at it                        [model1159.py --break2]
  (cube) L1: y=0 is a max line through P0 with c1 further points, Q1=(1,0,0), M1: z=0 tangent at Q1,
         L2: y=x a second-max line with c2 further points, (1,0,1) in S if c1>=2   [cubes1159.py]
and then ask a SAT solver whether the CNF accepts the full assignment (all 133 point variables fixed).
A sound WLOG + correct encoding must answer SAT for at least one image / the matching cube."""
import json, os, sys, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rpg
from pysat.formula import CNF
from pysat.solvers import Solver
p = 11; HERE = os.path.dirname(os.path.abspath(__file__)); RUNS = os.path.join(HERE, '..', 'runs')
pts, idx, lines, inc = rpg.plane(p)
W = json.load(open(os.path.join(RUNS, 'witnesses_q11_c4.json')))
S = [idx[rpg.norm(P, p)] for P in W['cadical']]; Sset = set(S)
def meet(l1, l2):
    (a,) = inc[l1] & inc[l2]; return a
def line_through(a, b):
    (l,) = [li for li, l in enumerate(inc) if a in l and b in l]; return l
def image(g, Sidx):
    return {idx[rpg.norm(rpg.matvec(g, pts[i], p), p)] for i in Sidx}
tangents = {P: [li for li, l in enumerate(inc) if l & Sset == {P}] for P in S}
P0t, R0t, Q1t, Yt = (0,0,1), (0,1,0), (1,0,0), (1,1,1)
def cnf_accepts(cnf_path, Simg):
    order = [tuple(P) for P in json.load(open(cnf_path + ('' if cnf_path.endswith('.json') else '')))['points']] if False else None
    return None
def check_cnf(cnf_file, points_file, Simg):
    order = [tuple(P) for P in json.load(open(points_file))['points']]
    assert sorted(order) == sorted(pts), "point list differs from PG(2,11)"
    assum = [(k + 1) if idx[P] in Simg else -(k + 1) for k, P in enumerate(order)]
    cnf = CNF(from_file=cnf_file)
    with Solver(name='cadical153', bootstrap_with=cnf.clauses) as s:
        return s.solve(assumptions=assum)
# --- break2 image: P0 in S, L0 tangent at P0, Q1 in S\{P0}, M1 tangent at Q1, R = L0 & M1 ; frame (P0,Q1,R,any 4th) chosen so that targets are exact
P0 = S[0]; L0 = tangents[P0][0]; Q1 = S[1]; M1 = tangents[Q1][0]; R = meet(L0, M1)
# 4th frame point: any point off the three sides; map it to (1,1,1); the residual diagonal freedom is irrelevant for b2
X = next(i for i in range(len(pts)) if all(i not in inc[line_through(a, b)] for a, b in ((P0, Q1), (P0, R), (Q1, R))))
g = rpg.proj_from_frames([pts[P0], pts[Q1], pts[R], pts[X]], [P0t, Q1t, R0t, Yt], p)
Sb = image(g, S)
L0t = idx[(1,0,0)]; M1t = idx[(0,0,1)]  # line x=0 has coords (1,0,0); line z=0 has coords (0,0,1)
assert idx[P0t] in Sb and inc[L0t] & Sb == {idx[P0t]} and idx[Q1t] in Sb and inc[M1t] & Sb == {idx[Q1t]}
print("b2 image built; spectrum", rpg.spectrum(Sb, inc))
print("pg11_c4_b2.cnf accepts the image (expect True):", check_cnf(os.path.join(RUNS, 'pg11_c4_b2.cnf'), os.path.join(RUNS, 'pg11_c4_b2.cnf.points.json'), Sb))
print("pg11_c4.cnf  accepts the image (expect True):", check_cnf(os.path.join(RUNS, 'pg11_c4.cnf'), os.path.join(RUNS, 'pg11_c4.cnf.points.json'), Sb))
# negative control: drop one point of the image -> must be rejected
print("negative control, image minus a point accepted? (expect False):", check_cnf(os.path.join(RUNS, 'pg11_c4_b2.cnf'), os.path.join(RUNS, 'pg11_c4_b2.cnf.points.json'), Sb - {next(iter(Sb - {idx[P0t], idx[Q1t]}))}))
# --- cube image
def further(l, P): return len((inc[l] & Sset) - {P})
L1t, L2t = idx[(0,1,0)], idx[rpg.norm((1, p - 1, 0), p)]  # y=0 ; x-y=0
found = {}
for P0 in S:
    through = [li for li in range(len(inc)) if P0 in inc[li]]
    for L0 in tangents[P0]:
        rest = [l for l in through if l != L0]
        c1 = max(further(l, P0) for l in rest)
        for L1 in [l for l in rest if further(l, P0) == c1]:
            rest2 = [l for l in rest if l != L1]; c2 = max(further(l, P0) for l in rest2)
            for L2 in [l for l in rest2 if further(l, P0) == c2]:
                for Q1 in sorted((inc[L1] & Sset) - {P0}):
                    for M1 in tangents[Q1]:
                        R = meet(L0, M1)
                        X2 = meet(L2, M1)            # must go to (1,1,0)
                        others = sorted((inc[L1] & Sset) - {P0, Q1})
                        if c1 >= 2:
                            Q2 = others[0]; Y = meet(line_through(Q2, R), L2)   # -> (1,1,1)
                        else:
                            Y = next(i for i in inc[L2] if i not in (P0, X2))
                        g = rpg.proj_from_frames([pts[P0], pts[Q1], pts[R], pts[Y]], [P0t, Q1t, R0t, Yt], p)
                        Si = image(g, S)
                        ok = (idx[P0t] in Si and inc[idx[(1,0,0)]] & Si == {idx[P0t]} and idx[Q1t] in Si
                              and inc[idx[(0,0,1)]] & Si == {idx[Q1t]} and len((inc[L1t] & Si) - {idx[P0t]}) == c1
                              and len((inc[L2t] & Si) - {idx[P0t]}) == c2 and (c1 < 2 or idx[(1,0,1)] in Si))
                        if ok: found.setdefault((c1, c2), Si)
                    if found: break
                if found: break
            if found: break
        if found: break
    if found: break
for (c1, c2), Si in found.items():
    f = os.path.join(RUNS, f'cube_q11_c4_{c1}{c2}.cnf')
    print(f"cube image for (c1,c2)=({c1},{c2}); cube file {os.path.basename(f)} accepts it (expect True):",
          check_cnf(f, os.path.join(RUNS, 'cube_q11_c4.points.json'), Si))
    for other in ('11', '21', '31'):
        print(f"   cube {other} accepts it (expect False, wrong c1/c2):", check_cnf(os.path.join(RUNS, f'cube_q11_c4_{other}.cnf'), os.path.join(RUNS, 'cube_q11_c4.points.json'), Si))
