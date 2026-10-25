# (6.7): c(rho)(rho^2+(1-rho)^2) - 2 rho(1-rho) >= lambda/2 for all rho in [0,1],
# delta = 1/100, lambda = delta^2/2, c = 1+lambda on |rho-1/2|<=delta else 1-lambda.
from fractions import Fraction as Fr
import sys

def make_c(delta, lam, inside=None, outside=None):
    inside = 1 + lam if inside is None else inside
    outside = 1 - lam if outside is None else outside
    return lambda r: inside if abs(r - Fr(1, 2)) <= delta else outside

def g(r, c):
    return c(r) * (r * r + (1 - r) ** 2) - 2 * r * (1 - r)

def check(delta, lam, c, N=200000, label=""):
    target = lam / 2
    worst = None
    pts = [Fr(i, N) for i in range(N + 1)]
    # exact boundary points and their neighbours
    for b in (Fr(1, 2) - delta, Fr(1, 2) + delta, Fr(1, 2)):
        for eps in (Fr(0), Fr(1, 10**12), -Fr(1, 10**12)):
            if 0 <= b + eps <= 1:
                pts.append(b + eps)
    for r in pts:
        v = g(r, c)
        # identity check
        ident = (2 * r - 1) ** 2 + (c(r) - 1) * (r * r + (1 - r) ** 2)
        assert v == ident, (r, v, ident)
        if worst is None or v < worst[1]:
            worst = (r, v)
    ok = worst[1] >= target
    print(f"{label}: min over {len(pts)} exact rationals = {float(worst[1]):.6e} at rho={float(worst[0]):.12f}; "
          f"lambda/2 = {float(target):.6e}; holds={ok}")
    return ok

delta = Fr(1, 100); lam = delta ** 2 / 2
ok1 = check(delta, lam, make_c(delta, lam), label="PAPER (delta=1/100, lam=delta^2/2)")
# analytic minima: inside, min of (2r-1)^2 + lam*(r^2+(1-r)^2) at r=1/2 -> lam/2 exactly
print("value at rho=1/2 (exact):", g(Fr(1, 2), make_c(delta, lam)), " = lam/2 =", lam / 2)
# just outside: (2delta)^2 - lam*(1/2 + 2 delta^2)
r = Fr(1, 2) + delta + Fr(1, 10**12)
print("just outside interval:", float(g(r, make_c(delta, lam))), " 4delta^2-lam =", float(4 * delta**2 - lam))
print("10 delta^2 < 1/4:", 10 * delta**2 < Fr(1, 4), "  margin lam/4 - 10delta^2 lam =", float(lam / 4 - 10 * delta**2 * lam))
print("Prop 5.5 constant 4d^2 lam/(2(1/4-d^2)) <= 10 d^2 lam:",
      4 * delta**2 * lam / (2 * (Fr(1, 4) - delta**2)) <= 10 * delta**2 * lam)

# CONTROLS that must FAIL:
# (i) reward 1 near balance (no +lambda bonus): value at 1/2 is 0 < lam/2
okc1 = check(delta, lam, make_c(delta, lam, inside=Fr(1)), label="CONTROL c=1 inside")
# (ii) penalty lambda too large outside: lam = 4 delta^2 kills the outside bound
lam2 = 4 * delta ** 2
okc2 = check(delta, lam2, make_c(delta, lam2), label="CONTROL lam=4delta^2")
print("controls rejected:", (not okc1) and (not okc2))
sys.exit(0 if (ok1 and not okc1 and not okc2) else 1)
