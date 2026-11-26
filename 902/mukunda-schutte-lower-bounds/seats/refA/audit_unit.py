"""Unit-test the audit script's configuration counting (Lemma 9.2 implementation) on rows whose
value is the same constant for EVERY tournament on N=52 vertices, so a_H must equal that constant*K
on all 456 classes:  r=1 '1' -> 52;  r=1 'D(0,)>=25' -> C(52,2)-25*52 = 26;  r=1 'deg0<=26' -> 26;
r=2 sigma=0 '1' -> C(52,2)=1326; r=1 'int[D(0,),25]' -> sum_v (d-25)(d-26), NOT constant (control: must vary).
Also a quadratic constant: r=1 'D(0,)>=0*D(0,)>=0' -> sum_v d^2, not constant (control)."""
import importlib.util, itertools, sys
from math import comb, lcm
spec = importlib.util.spec_from_file_location('aud', '/home/exedev/MathDyad/subs-1126/902/repo/proof/search/r11/audit_b320_independent.py')
aud = importlib.util.module_from_spec(spec); spec.loader.exec_module(aud)
s, N = 7, 52
reps = aud.build_classes_scratch(s)
adjs = [aud.adj_matrix(c, s) for c in reps]
popc = [bin(i).count('1') for i in range(1 << s)]
K = lcm(*[comb(s, t) for t in range(s + 1)])
wt = [comb(N, t) * (K // comb(s, t)) for t in range(s + 1)]
def row(r, sigma, expr):
    f = aud.parse_hyp_expr(expr); vals = set()
    for A in adjs:
        tot = 0
        for th in itertools.permutations(range(s), r):
            if r >= 2 and aud.induced_code(A, th) != sigma: continue
            out = [v for v in range(s) if v not in th]
            for msk, cnt in aud.eval_factor_poly_configs(A, th, out, f).items():
                tot += wt[r + popc[msk]] * cnt
        vals.add(tot)
    return sorted(v / K for v in vals)
print("classes:", len(reps))
for r, sg, e, exp in [(1, 0, '1', 52), (1, 0, 'D(0,)>=25', 26), (1, 0, 'deg0<=26', 26), (2, 0, '1', 1326), (2, 1, '1', 1326)]:
    v = row(r, sg, e); print(f"r={r} sigma={sg} '{e}': distinct a_H/K = {v[:3]}{'...' if len(v)>3 else ''} expected {exp}: {'OK' if v == [exp] else 'MISMATCH'}")
for r, sg, e in [(1, 0, 'int[D(0,),25]'), (1, 0, 'D(0,)>=0*D(0,)>=0')]:
    v = row(r, sg, e); print(f"control r={r} '{e}': {len(v)} distinct values (should be >1), range {v[0]:.3f}..{v[-1]:.3f}")
