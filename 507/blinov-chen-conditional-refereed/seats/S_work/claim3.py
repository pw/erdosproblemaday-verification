# Seat S: exact (Fraction) bookkeeping for claim 3, derived from the parameter definitions, not from the
# coordinator's closed forms.  All exponents are exponents of r (B in (40000k^4 r^6, 80000k^4 r^6]).
# Usage: python3 -I claim3.py [mutation]   mutation: none | uminus1 | Xoff | etaoff
import sys
from fractions import Fraction as F
mut = sys.argv[1] if len(sys.argv) > 1 else "none"
def expo(k, kappa, gamma):
    """kappa = r-exponent of K = N/(hq).  Returns dict of r-exponents (constants and logs dropped)."""
    B = 6; h = 6*k; tau = 6*(k-1); q = 36*k; s_lb = 2*q - 2*h; M = 3       # s >= q^2/(8000 h^2)
    N = h + q + kappa
    a = gamma + F(3*N - tau, 2)                                           # a_r = r^g sqrt(N^3/tau)
    pr_old = 6*(h+q) - 3*N                                                # (hq)^6 N^-3
    pr_new = pr_old - M*k - s_lb                                          # claim 1: x M^-k s^-1
    tri = h - 3*N - 8                                                     # (log)^2 h/(N^3 r^8)
    return dict(X=a-gamma, a=a, pair=a+pr_new, pair_old=a+pr_old, triple=2*a+tri)
results = {}
for name, k in [("Blinov set", 408781), ("bt163 set", 356155), ("Wroblewski set", 275385)]:
    u = -(-(41*k+2)//3)
    if mut == "uminus1": u -= 1
    # gamma must be in (0,1) and is set to X/(X+1) after X is known (X does not depend on gamma)
    X = expo(k, 6*u, F(0))["X"]
    gamma = X/(X+1)
    e = expo(k, 6*u, gamma)
    eta = 2*gamma/(gamma + X)
    if mut == "Xoff": X = X + 1
    if mut == "etaoff": eta = F(2, X+1)
    ok_pair = e["pair"] < 0
    ok_tri = e["triple"] < 0
    claimed_X = 60*k + 9*u + 3
    print(f"{name}: k={k} u={u} 3u-(41k+2)={3*u-(41*k+2)} X={X} (formula 60k+9u+3={claimed_X}) "
          f"pair-exp={e['pair']} triple-exp={e['triple']} (x log^2)  eta=2/{F(2)/eta}  ~{float(eta):.6e}")
    results[name] = (k, u, X, eta, ok_pair, ok_tri)
    # u-1 under the SAME gamma: does the pair bound still decay?
    e1 = expo(k, 6*(u-1), gamma)
    print(f"   with u-1: pair-exp={e1['pair']}  (>=0 means the bound does not decay)")
    # finer lift box N = hq B^(u-1) r^j
    for j in range(0, 7):
        Xj = expo(k, 6*(u-1)+j, F(0))["X"]; gj = Xj/(Xj+1); ej = expo(k, 6*(u-1)+j, gj)
        if ej["pair"] < 0:
            print(f"   finer box N=hq B^(u-1) r^{j}: pair-exp={ej['pair']} X={Xj} eta=2/{F(2)*(gj+Xj)/(2*gj)} ~{float(2*gj/(gj+Xj)):.9e}")
            break
    sup = F(2, 183*k+8)
    print(f"   sup over continuous N, gamma->1: 2/(183k+8)=2/{183*k+8} ~{float(sup):.9e}; claimed eta < sup: {eta < sup}")
# assertions against the coordinator's stated numbers
exp = {"Blinov set": (5586675, 74806940), "bt163 set": (4867453, 65176382), "Wroblewski set": (3763596, 50395469)}
bad = []
for name, (k, u, X, eta, okp, okt) in results.items():
    U, den = exp[name]
    if u != U: bad.append(f"{name}: u={u} != {U}")
    if eta != F(2, den): bad.append(f"{name}: eta={eta} != 2/{den}")
    if X + 2 != den: bad.append(f"{name}: X+2={X+2} != {den}")
    if not okp: bad.append(f"{name}: pair term does not decay")
    if not okt: bad.append(f"{name}: triple term does not decay")
print("Blinov formula 2/(249k+5) at Wroblewski k:", F(2, 249*275385+5))
print("Chen 2/100866719 ~", 2/100866719)
if bad:
    print("FAIL:", *bad, sep="\n  "); sys.exit(1)
print("ALL CLAIM-3 ARITHMETIC CHECKS PASSED")
