# (1) Erdelyi Thm 2.1 (arXiv:2608.00744v1): max|P|^2 >= n+1 + n^{1/3}/38 for degree n, i.e. >= N + (N-1)^{1/3}/38 at length N.
#     Compare with the exhaustive min sup|P| from mN_output.txt.
# (2) App. A.1: Dirichlet kernel D_q concentration on E = (-d,d): ratio int_E |D_q|^a / int_T |D_q|^a -> 1 for a > 1,
#     and the two printed bounds int_{T\E} <= sin(pi d)^-a, int_T >= (2/pi)^a q^(a-1).
# (3) App. A.2: a_j = 2^{j^2} (as printed on p.24; the seat prompt's "2^j" is a paraphrase -- checked too): (46) with K=2 and
#     uniform convergence of |sum a_j z^j|/sqrt(S_n) to 1. Exact integer/rational arithmetic where possible.
# (4) App. A.2: P = 1+z, z = 1, z' = i: |P(z)-P(z')| vs sigma|P(z)| + tau|P(z')|.
import math, sys
from fractions import Fraction
import numpy as np
print("(1) Erdelyi bound vs exhaustive minimum")
for line in open(sys.argv[1]):
    if 'example=' in line:
        N = int(line.split('N=')[1].split()[0]); lo = float(line.split('[')[1].split(',')[0])
        eb = N + (N-1)**(1/3)/38
        print(f"  N={N:2d}  min||P||^2={lo*lo:9.5f}  Erdelyi lower bound={eb:8.5f}  holds={lo*lo >= eb - 1e-9}  slack={lo*lo-eb:7.4f}")
print("(2) Dirichlet kernel concentration")
for d in (0.05, 0.2, 0.45):
    for a in (1.5, 2, 4):
        row = []
        for q in (10, 100, 1000):
            K = 1 << 21
            t = (np.arange(K) + 0.5) / K - 0.5              # midpoint grid on [-1/2,1/2)
            s = np.sin(np.pi * t)
            D = np.abs(np.sin(np.pi * q * t) / s)
            Da = D ** a
            tot = Da.mean(); inE = Da[np.abs(t) < d].mean() * (np.abs(t) < d).mean()
            out = tot - inE
            ok1 = out <= math.sin(math.pi*d)**(-a) + 1e-9
            ok2 = tot >= (2/math.pi)**a * q**(a-1) - 1e-9
            row.append(f"q={q}: ratio={inE/tot:.6f} [outside<=sin^-a:{ok1}, total>=(2/pi)^a q^(a-1):{ok2}]")
        print(f"  d={d} a={a}: " + "; ".join(row))
print("(3) a_j = 2^{j^2}: exact check of (46) with K=2 and of the printed inequalities")
bad = []
for n in range(1, 41):
    a = [None] + [2 ** (j*j) for j in range(1, n+1)]
    S = sum(a[j]**2 for j in range(1, n+1))
    rhs = Fraction(2, n*n) * sum(j*j*a[j]**2 for j in range(1, n+1))
    c46 = S <= rhs
    c1 = (n < 2) or Fraction(sum(a[j]**2 for j in range(1, n)), a[n]**2) <= Fraction(n-1, 2**(4*n-2)) <= 1
    c2 = S <= 2*a[n]**2 <= rhs
    c3 = (n < 2) or Fraction(sum(a[j] for j in range(1, n)), a[n]) <= Fraction(n-1, 2**(2*n-1))
    # uniform deviation bound sum_{j<n} a_j/sqrt(S) + |a_n/sqrt(S) - 1|
    if not (c46 and c1 and c2 and c3): bad.append(n)
    if n in (1, 2, 3, 5, 10, 20, 40):
        sq = math.isqrt(S)
        devbound = (sum(a[j] for j in range(1, n)) + abs(a[n] - sq)) / sq if True else None
        print(f"  n={n:2d}: (46) K=2 {c46}; printed bounds {c1},{c2},{c3}; uniform deviation bound ~ {devbound:.3e}")
print("  failures:", bad)
# brute check of sup | |P|/sqrt(S) - 1 | on the circle for small n
for n in (2, 3, 4, 6):
    a = np.array([2.0 ** (j*j) for j in range(1, n+1)])
    S = (a**2).sum()
    th = 2*np.pi*np.arange(1<<16)/(1<<16)
    P = sum(a[j-1]*np.exp(1j*j*th) for j in range(1, n+1))
    print(f"  n={n}: max | |P|/sqrt(S_n) - 1 | on circle = {np.abs(np.abs(P)/np.sqrt(S)-1).max():.3e}")
print("  (prompt's paraphrase a_j = 2^j, for contrast):")
for n in (5, 10, 20, 40):
    a = [2 ** j for j in range(1, n+1)]
    S = sum(x*x for x in a); rhs = Fraction(2, n*n) * sum((j+1)**2 * a[j]**2 for j in range(n))
    print(f"    n={n}: (46) with K=2 holds: {S <= rhs};  |P(1)|/sqrt(S_n) = {sum(a)/math.sqrt(S):.4f}  (-> sqrt(3), NOT flat)")
print("(4) P = 1+z, z=1, z'=i")
Pz, Pzp = 2, abs(1+1j); lhs = abs(2 - (1+1j))
cands = {(s, t): s*Pz + t*Pzp for s in (1, -1) for t in (1, -1)}
print(f"  |P(z)-P(z')| = {lhs:.6f};  sigma|P(z)|+tau|P(z')| in {sorted(round(v,6) for v in cands.values())};  any equal: {any(abs(v-lhs)<1e-12 for v in cands.values())}")
print("  endpoint-sign remark: flipping one coefficient changes P(z) by exactly 2|z|^k = 2 on |z|=1, two flips <= 4 -> 4/sqrt(N) normalized: OK")
