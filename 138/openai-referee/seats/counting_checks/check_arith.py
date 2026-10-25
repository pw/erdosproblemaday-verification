"""Arithmetic of count:local (printed Lemma 3.4) and the size of the count:global / count:local quantities
at actual parameters (informational thresholds; the paper only claims 'sufficiently large k')."""
import math, mpmath
from math import comb
C0 = 9 * 16005 ** 2
C = 1
while C ** 3 < C0: C += 1                     # C = ceil(C0^(1/3)), absolute
print("C0 = 9*16005^2 =", C0, "  C = ceil(C0^(1/3)) =", C)
# (1) 9(16004Dh+1)^2 <= C0 (Dh)^2
assert all(9 * (16004 * D * h + 1) ** 2 <= C0 * (D * h) ** 2 for D in range(1, 30) for h in range(1, 300))
bad = [(D, h) for D in range(1, 5) for h in range(1, 5) if 9 * (16004 * D * h + 1) ** 2 > 9 * 16004 ** 2 * (D * h) ** 2]
print("(1) 9(16004Dh+1)^2 <= C0(Dh)^2 on D<30,h<300: OK;  CONTROL C0'=9*16004^2 violated at", len(bad), "of 16 pairs")
# (2) h^{D+1} [C0 (Dh)^2]^{2D} = C0^{2D} D^{4D} h^{5D+1} <= (CDh)^{6D}
ok = True
for D in range(1, 9):
    for h in range(1, 201):
        lhs = h ** (D + 1) * (C0 * (D * h) ** 2) ** (2 * D)
        assert lhs == C0 ** (2 * D) * D ** (4 * D) * h ** (5 * D + 1)
        ok &= lhs <= (C * D * h) ** (6 * D)
print("(2) identity and inequality <= (CDh)^{6D} for D<=8, h<=200:", ok)
c1 = [(D, h) for D in range(1, 9) for h in range(1, 201)
      if h ** (D + 1) * (C0 * (D * h) ** 2) ** (2 * D) > ((C - 1) * D * h) ** (6 * D)]
c2 = [(D, h) for D in range(1, 9) for h in range(1, 201)
      if h ** (D + 1) * (C0 * (D * h) ** 2) ** (2 * D) > (C * D * h) ** (5 * D)]
print("    CONTROL C-1 violates at", len(c1), "pairs (e.g.", c1[:2], ");  CONTROL exponent 5D violates at", len(c2), "pairs")

# (3) informational: where do the 'o(.)' statements that consume count:global/count:local actually bite?
mpmath.mp.dps = 30
c = mpmath.mpf(10) ** -5; delta = mpmath.mpf(1) / 10
def glob_terms(k):
    k = mpmath.mpf(k)
    D = mpmath.ceil(k ** (mpmath.mpf(1) / 10)); M = mpmath.ceil(mpmath.sqrt(k)); h0 = D * D
    loglam = h0 * mpmath.log(2 * M)                 # paper's bound log(lambda) <= h0 log(2M)
    logq = c * k / D * mpmath.log(k) + mpmath.log(2 * k * k)
    R = (D + 1) * logq + 1                          # R = log(1+q^{D+1}/2) <= (D+1)log q (+1 slack)
    logF = mpmath.log(k * k * mpmath.e ** loglam + 2 * (k * k * R + 1))
    logT = 2 * D * (mpmath.log(9) + 2 * (mpmath.log(3) + 2 * mpmath.log(k) + logF + mpmath.log(1 + mpmath.e ** (-logF))))
    first = mpmath.log(k) + logT - (delta * M - 1) / 32  # log of k T_glob e^{-(delta M-1)/32}
    return D, M, logT, first
print("(3) first-family exponent log(k T_glob) - (delta M - 1)/32 (paper's explicit T_glob bound, lambda bound):")
for ex in (20, 25, 28, 30, 35, 40, 50):
    D, M, logT, first = glob_terms(mpmath.mpf(10) ** ex)
    print(f"    k=1e{ex}: D={int(D)} log T_glob<={mpmath.nstr(logT,6)}  M={mpmath.nstr(M,6)}  exponent={mpmath.nstr(first,6)}")
print("    second-family per-label sum S(D)=sum_{h>D^2} (CDh)^{6D} e^{-h/64} with the explicit C:")
for D in (1000, 3000, 5000, 8000, 10000, 20000):
    f = lambda h: 6 * D * mpmath.log(C * D * h) - h / 64
    # terms decrease for h > D^2 once f' < 0: f'(h) = 6D/h - 1/64 < 0 iff h > 384 D
    h1 = D * D + 1
    if h1 > 384 * D:
        # geometric tail bound: sum <= exp(f(h1)) / (1 - exp(max ratio)), ratio exp(f(h+1)-f(h)) <= exp(6D/h1 - 1/64)
        r = 6 * D / mpmath.mpf(h1) - mpmath.mpf(1) / 64
        logS = f(h1) - mpmath.log(1 - mpmath.e ** r)
        print(f"      D={D}: log S(D) <= {mpmath.nstr(logS,6)}  (k = D^10 ~ 1e{int(10*math.log10(D))})")
    else:
        print(f"      D={D}: D^2 <= 384 D, terms not yet decreasing at h=D^2")
