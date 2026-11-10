#!/usr/bin/env python3
# Higher-order calibration: for the fixed-depth sieve model z (truncated singular series S_z), compare its EXACT
# finite-n excess over Cramér (model.c) with its pair-only prediction; the ratio F_z measures the higher-order
# cumulants. Then calibrated HL = pair_full * F_19.  Heuristic (c).
import sys, math, re, numpy as np
exec(open('pair_check.py').read().split("def pair_delta")[0].split("g = 0.5772")[0])  # reuse S, C2 build (lines above D)
def Dfrom(Sarr):
    a = Sarr - 1.0; a[0] = 0.0; d = np.arange(HMAX + 1, dtype=float)
    A = np.cumsum(a); B = np.cumsum(d * a); Dz = np.zeros(HMAX + 1)
    Dz[2:] = np.arange(2, HMAX + 1) * A[1:HMAX] - B[1:HMAX]
    return Dz
Dfull = Dfrom(S.copy())
def Sz(z):
    out = np.ones(HMAX + 1); d = np.arange(HMAX + 1)
    for p in [p for p in (2,3,5,7,11,13,17,19) if p <= z]:
        div = (d % p == 0)
        out *= np.where(div, p / (p - 1.0), p * (p - 2.0) / (p - 1.0) ** 2)
    return out
D19 = Dfrom(Sz(19)); D5 = Dfrom(Sz(5))
def pair(n, Dz):
    s = math.isqrt(n); kmax = n // (s + 1); tot = 0.0; CH = 10_000_000; k0 = 1
    while k0 <= kmax:
        k = np.arange(k0, min(kmax, k0 + CH - 1) + 1, dtype=np.int64)
        aa = np.maximum(n // (k + 1), s); bb = n // k; H = bb - aa
        mid = 0.5 * (aa.astype(float) + bb.astype(float)) + 0.5; q = 1.0 / np.log(mid)
        lp0 = H * np.log1p(-q); use = (H > 0) & (lp0 > -80)
        Hu = H[use]; qq = q[use]; tot += float(np.sum(np.exp(lp0[use]) * (1 - np.exp(qq * qq * Dz[Hu])))); k0 += CH
    return tot
for e in map(int, sys.argv[1:]):
    n = 10 ** e; md = open(f'model_1e{e}.out').read(); hf = open(f'hfast_1e{e}.out').read()
    J = int(re.search(r' J=(\d+)', hf).group(1)); row = {l.split()[0]: float(l.split()[2]) for l in md.splitlines() if l.split() and (l.startswith('cramer ') or l.startswith('z='))}
    EC = row['cramer']; gap = J - EC
    pf = pair(n, Dfull); p19 = pair(n, D19); p5 = pair(n, D5)
    F19 = (row['z=19'] - EC) / p19; F5 = (row['z=5'] - EC) / p5
    print(f"1e{e}: gap={gap:.0f} pair_full={pf:.0f} ({pf/gap:.3f})  z19: exact {row['z=19']-EC:.0f} pair {p19:.0f} F19={F19:.4f}  z5: F5={F5:.4f}  calibrated pair_full*F19/gap={pf*F19/gap:.4f}", flush=True)
