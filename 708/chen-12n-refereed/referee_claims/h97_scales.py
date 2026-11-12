# Task 4: exact recomputation of Section 17 (sec:h97) window value and the 29 finite scales,
# from the paper's printed formulas only (Lemmas 17.x as printed: h97-5, h97-6, h97-7, h97-9).
from fractions import Fraction as Fr
from math import comb, floor
import time

H = Fr(1025, 1024); Gam = Fr(211, 210); K = Fr(8, 3); lam = Fr(51, 10)
rho = Fr(5, 4); D0 = Fr(47, 16); T = Fr(541, 100)
print("D0 + rho*T =", D0 + rho * T, "(paper: 97/10)")
wv = lam * (1 - 2 * Gam * H / K)
print("window value lam(1-2*Gam*H*/K) =", wv, "=", float(wv), "; paper 718539/573440:", wv == Fr(718539, 573440))
print("excess over 5/4 =", wv - Fr(5, 4), "(paper 1739/573440)", "; relative", float((wv - Fr(5,4)) / Fr(5,4)))
print("lam * 19/100 =", lam * Fr(19, 100), "(paper 969/1000)")

def A_r(r, a):
    v = floor(r * a / (r - 1))
    return Fr(v) - a, comb(v, r)

def eps(theta, s):
    a = (T - s) / theta
    best = None
    for r in range(2, floor(a) + 2):
        num, den = A_r(r, a)
        val = theta * num / den * (H / theta) ** r / Fr(__import__('math').factorial(r))
        if best is None or val < best: best = val
    return best

def exps_for(j, L):
    if L == 4: return [4]
    E = {L}
    h = 3
    while 2 ** h <= L:
        for a in range(4, 8):
            if (a * L) % (2 ** h) == 0:
                e = a * L // 2 ** h
                if e >= j: E.add(e)
        h += 1
    return sorted(E)

def polymul_trunc(P, exps, deg):
    # P * (1 + sum X^e)
    R = P[:]
    for e in exps:
        for i in range(0, deg + 1 - e):
            if P[i]: R[i + e] += P[i]
    return R

def A_jL(j, L):
    theta = Fr(j, L)
    exps = exps_for(j, L)
    deg = L + j
    Nmax = floor((K + 1) * L / j + 1)
    epsd = {d: eps(theta, 1 + Fr(d, L)) for d in range(1, j + 1)}
    G = [0] * (deg + 1); G[0] = 1          # G^N
    Gm = [0] * (deg + 1); Gm[0] = 1        # (G - X^j)^N
    exps_m = [e for e in exps if e != j]
    best = Fr(0); argN = 0
    for N in range(0, Nmax + 1):
        if N > 0:
            G = polymul_trunc(G, exps, deg); Gm = polymul_trunc(Gm, exps_m, deg)
        tot = Fr(0)
        for d in range(1, j + 1):
            D = G[L + d] - Gm[L + d]
            if D == 0: continue
            num = 1 - max(Fr(0), N * theta - 1 - Fr(d, L)) / K
            if num <= 0: continue
            tot += D * epsd[d] * num / max(Fr(d, L), N * theta - 1)
        if tot > best: best = tot; argN = N
    return best, argN, Nmax

t0 = time.time()
total = Fr(0)
a44, n44, _ = A_jL(4, 4)
print("A_{4,4} = %.9f (N*=%d)  paper bound < 0.024680" % (float(a44), n44), flush=True)
total += a44
paper = {8: 128711, 16: 25773, 32: 5665, 64: 1025, 128: 150, 256: 21, 512: 3}
for L in (8, 16, 32, 64, 128, 256, 512):
    sL = Fr(0); info = []
    for j in range(4, 8):
        v, nN, nmax = A_jL(j, L); sL += v; info.append((j, round(float(v), 9), nN, nmax))
    total += sL
    print("L=%4d sum_j A_{j,L} = %.9f  paper bound < %.6f  ok=%s  %s  (%.0fs)" % (L, float(sL), paper[L] / 1e6, sL < Fr(paper[L], 10**6), info, time.time() - t0), flush=True)
print("TOTAL 29 scales = %.12f ; 1e12*total in [%d, %d]; paper [186024001631,186024001632]; < 187/1000: %s"
      % (float(total), floor(total * 10**12), floor(total * 10**12) + 1, total < Fr(187, 1000)))
