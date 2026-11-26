"""Test the audit's Lemma-9.2 conversion on NON-constant rows against a real tournament at small N:
for random tournaments T on N=10 vertices compute x_H (densities of the 456 classes over all C(10,7) 7-sets,
classified by brute-force canonical form) and compare sum_H a_H x_H (audit's eval code, wt with N=10)
with the direct value of sum_theta prod(factors) computed on T itself."""
import importlib.util, itertools, random, sys
from math import comb, lcm
from fractions import Fraction as F
spec = importlib.util.spec_from_file_location('aud', '/home/exedev/MathDyad/subs-1126/902/repo/proof/search/r11/audit_b320_independent.py')
aud = importlib.util.module_from_spec(spec); spec.loader.exec_module(aud)
s = 7; N = 10
reps = list(aud.build_classes_scratch(s)); repidx = {int(c): i for i, c in enumerate(reps)}
adjs = [aud.adj_matrix(c, s) for c in reps]
popc = [bin(i).count('1') for i in range(1 << s)]
wt = [F(comb(N, t), comb(s, t)) for t in range(s + 1)]
perms = list(itertools.permutations(range(s)))
def canon(A7):
    best = None
    for p in perms:
        c = aud.induced_code(A7, p)
        if best is None or c < best: best = c
    return best
def aH(r, sigma, expr):
    f = aud.parse_hyp_expr(expr); out = []
    for A in adjs:
        tot = F(0)
        for th in itertools.permutations(range(s), r):
            if r >= 2 and aud.induced_code(A, th) != sigma: continue
            o = [v for v in range(s) if v not in th]
            for msk, cnt in aud.eval_factor_poly_configs(A, th, o, f).items():
                tot += wt[r + popc[msk]] * cnt
        out.append(tot)
    return out
def direct(T, r, sigma, expr):
    f = aud.parse_hyp_expr(expr); n = len(T); tot = 0
    for th in itertools.permutations(range(n), r):
        if r >= 2 and aud.induced_code(T, th) != sigma: continue
        val = 1
        for kind, S, b in f:
            D = sum(1 for w in range(n) if w not in [th[i] for i in S] and all(T[w][th[i]] for i in S))
            if kind == 'ge': val *= D - b
            elif kind == 'le': val *= b - D
            else: val *= (D - b) * (D - b - 1)
        tot += val
    return tot
rows = [(1, 0, 'D(0,)>=3*D(0,)>=5'), (2, 0, 'D(0, 1)>=2'), (2, 1, 'int[D(0, 1),1]'), (3, 0, 'D(0, 1, 2)>=1*D(0,)>=4'),
        (3, 5, 'D(0, 1)>=1'), (2, 0, 'D(0, 1)>=2*D(1,)>=4*deg0<=6')]
coef = {rw: aH(*rw) for rw in rows}
rng = random.Random(5)
bad = 0
for trial in range(3):
    T = [[0] * N for _ in range(N)]
    for i in range(N):
        for j in range(i + 1, N):
            if rng.random() < 0.5: T[i][j] = 1
            else: T[j][i] = 1
    cnt = [0] * len(reps)
    for U in itertools.combinations(range(N), s):
        A7 = [[T[U[a]][U[b]] for b in range(s)] for a in range(s)]
        cnt[repidx[canon(A7)]] += 1
    x = [F(c, comb(N, s)) for c in cnt]
    for rw in rows:
        lhs = sum(a * xi for a, xi in zip(coef[rw], x)); rhs = direct(T, *rw)
        ok = lhs == rhs; bad += (not ok)
        print(f"trial {trial} row {rw}: via x_H = {lhs}  direct = {rhs}  {'OK' if ok else 'MISMATCH'}", flush=True)
print("MISMATCHES:", bad)
