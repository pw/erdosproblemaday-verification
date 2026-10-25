# (c') further Section-2 bookkeeping: Lemma 2.1 rows, Prop 2.2 sums, constants c1 (2.3) and c4/C4/theta (2.9), Chernoff.
import math
from math import comb, factorial
from sympy import Rational as R
print("== Lemma 2.1 u=2 row: planar bound g_2(m) >= c m/log m and <= M-1 distances  =>  m <= C M log(2M) ==")
# claim used: m/ln m <= X (X >= 1)  =>  m <= max(e, 2 X ln X) ; check: X >= 2 ln X for all X > 0
print("  min_{X>0} (X - 2 ln X) =", round(2 - 2*math.log(2), 6), "> 0, so m = 2X ln X has m/ln m >= X; brute check:")
bad = 0
for X in [1.5*1.1**i for i in range(200)]:
    m = 3
    while m/math.log(m) <= X: m += max(1, m//1000)
    if m - 1 > max(math.e, 2*X*math.log(X)) + 1: bad += 1
print("  violations of (largest m with m/ln m <= X) <= 2 X ln X over 200 X in [1.5, 2.8e8]:", bad)
print("== Lemma 2.1 u>=3 rows: c_u m^(2/u) <= M  =>  m <= (M/c_u)^(u/2) = C_u M^(u/2);  c0 = 1/2 ==")
for d in range(3, 8):
    rows = []
    for u in range(1, d):
        e = 1 if u == 1 else (1 if u == 2 else R(u, 2))   # exponent of M (u=2: M^{1+o(1)})
        rows.append(f"u={u}: B^{2*e}{'+o(1)' if u == 2 else ''}")
    print(f"  d={d}: proper u-flats hold at most " + ", ".join(rows) + f"; N B^(-1/2) = B^{R(2*d-1,2)}; worst exponent {max(2, d-1)} < {R(2*d-1,2)}")
print("== Prop 2.2 rich-line discard: sum over dyadic t = 2^j H <= L_max of C(N^2/t^3 + N/t)(2t)^2 <= 8C(N^2/H + N L_max) ==")
for N, H, L in ((10**6, 10, 1000), (10**9, 50, 10**5), (10**12, 1000, 10**6)):
    s = 0.0; t = H
    while t <= L: s += (N**2/t**3 + N/t)*(2*t)**2; t *= 2
    print(f"  N={N:.0e} H={H} L_max={L}: dyadic sum / (N^2/H + N L_max) = {s/(N**2/H + N*L):.3f} (<= 8)")
print("== Prop 2.2 greedy: removed curves Y carry > K A deg(Y) disjoint partners  =>  sum deg Y < N/(KA) = o(N/A) when K -> oo ==")
print("== (2.3): |S| = sum_j #partners_j <= sum_j C a_j A^j,  H_S(D) >= c_d a_j D^j,  D = floor(A) >= A/2 (A >= 2) ==")
for d in (3, 4, 5):
    print(f"  d={d}: |S| <= d * C * 2^(d-1) * max_j a_j D^j <= (d C 2^(d-1)/c_d) H_S(D)  =>  c1 = c_d/(d C 2^(d-1)) = c_d/(C*{d*2**(d-1)})")
print("== (2.9) and the sample: H_{S_F}(D) >= max_h c a_h D^(s0+h) >= (c/C) max_h m_h A^(s0)(D/A)^(s0+h) >= c4 m A^s0 with c4 = c/(C (d+1) 2^(s0+d)) ==")
for d in (3, 4, 5):
    s0 = d*(d-1)//2
    C4 = 2*2**s0/factorial(s0)          # 2 * C(D+s0,s0) <= 2 (2A)^s0/s0!  for A >= s0
    worst = max(comb(A+s0, s0)/A**s0 for A in range(s0, 5000))
    print(f"  d={d}, s0={s0}: max_(A>=s0) C(A+s0,s0)/A^s0 = {worst:.4f} <= 2^s0/s0! = {2**s0/factorial(s0):.4f}: {worst <= 2**s0/factorial(s0)};  "
          f"theta < c4/C4 suffices (fixed: depends on d and the constants of Lemmas 2.4 and 3.6 only)")
print("== Chernoff + union bound: P(Bin(n,theta) < n theta/2) <= exp(-n theta/8); need N^2 exp(-theta delta(H)/8) -> 0 with delta(H) >> A^(d-1) ==")
for d in (3, 4, 5):
    for N in (10**3, 10**6, 10**9):
        A = N**(2/d); theta = 1e-3
        lg = 2*math.log(N) - theta*A**(d-1)/8
        print(f"  d={d} N={N:.0e}: A^(d-1) = N^{2*(d-1)/d:.3f} = {A**(d-1):.3e}; log(N^2 exp(-theta A^(d-1)/8)) with theta=1e-3: {lg:.3e}")
