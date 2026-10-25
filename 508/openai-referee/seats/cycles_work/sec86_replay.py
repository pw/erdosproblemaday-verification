#!/usr/bin/env python3
"""Literal replay of the paper's own Section 8.6 proof of Lemma 8.9 (PDF pp. 58-60), every displayed
number checked as an exact rational statement. Run with --corrupt to inject one wrong table entry
(control: the replay must then FAIL)."""
from fractions import Fraction as F
import sys
D = lambda s: F(s)            # terminating decimals = exact rationals (paper's convention)
fails = []
def chk(cond, msg):
    print(("  ok   " if cond else "  FAIL ") + msg)
    if not cond: fails.append(msg)

corrupt = "--corrupt" in sys.argv
# Table 1
T1 = {"0": ("-1.2906", "0.1876", "0.90", "1.35"), "A": ("-0.6335", "0.9414", "0.095", "0.110"),
      "B": ("-0.3092", "-0.0045", "0.000002", "0.00065"), "T": ("0.3478", "0.7493", "0.023", "0.026"),
      "uA": ("-1.1598", "1.1790", "9.8", "19.0"), "uB": ("-0.3666", "0.5700", "0.0022", "0.024"),
      "uT": ("-0.2358", "1.5614", "12.65", "12.9")}
# residual numerators (d_x, d_y) over 710400000000
RES = {"0": (3840000, -23040000), "A": (-29520000, 10176000), "B": (-12240000, -22464000),
       "T": (25440000, 10752000), "uA": (32043244, -19212795), "uB": (4763244, -27212795),
       "uT": (32966488, -23385590)}
# Table 2: b_y, b_H, a, b
T2 = {"0": ("0.0353", "4.963", "1.70", "1.71"), "A": ("0.887", "0.319", "1.28", "1.29"),
      "B": ("0.000022", "0.287", "0.095", "0.096"), "T": ("0.562", "0.199", "0.682", "0.683"),
      "uA": ("1.391", "2.647", "2.73", "2.74"), "uB": ("0.326", "0.079", "0.459", "0.46"),
      "uT": ("2.44", "2.273", "2.493", "2.495")}
if corrupt:
    T1["uT"] = ("-0.2358", "1.5614", "12.65", "13.5")   # raise P'_- for uT above what is provable
    print("*** CONTROL RUN: Table 1 row uT P'_- changed 12.9 -> 13.5 ***")

print("1. radical bounds by squaring rational endpoints")
chk(D("1.73205")**2 < 3 < D("1.73206")**2, "1.73205 < sqrt3 < 1.73206")
chk(D("3.31662")**2 < 11 < D("3.31663")**2, "3.31662 < sqrt11 < 3.31663")
a_, b_, eps = D("1.732055"), D("3.316625"), D("0.000005")
chk(a_ == (D("1.73205")+D("1.73206"))/2 and b_ == (D("3.31662")+D("3.31663"))/2, "a*, b* are the midpoints")
pe = (a_+b_)*eps + eps*eps
chk(pe == D("0.000025243425") and pe < D("0.000026"), f"(a*+b*)eps+eps^2 = {pe} = 0.000025243425 < 0.000026")
chk(D("0.000026")/6 < eps, "0.000026/6 < eps")
chk(F(35+12, 37) == F(47, 37), "absolute row sum of (35+12i)/37 rotation = 47/37")

print("2. midpoint-substituted placed points and the displayed residuals")
s3, s11, s33 = a_, b_, a_*b_
g = {"0": (F(0), F(0)), "A": (s3/2, F(1, 2)), "B": (s3/2, F(-1, 2)), "T": (s3, F(0)),
     "uA": ((5*s3 - s11)/12, (s33 + 5)/12), "uB": ((5*s3 + s11)/12, (s33 - 5)/12),
     "uT": (5*s3/6, s33/6)}
cx, cy = F(-290, 250), F(149, 250)
DEN = 710400000000
for k, (x, y) in g.items():
    X, Y = x + cx, y + cy
    zx, zy = (35*X - 12*Y)/37, (12*X + 35*Y)/37
    x0, y0 = D(T1[k][0]), D(T1[k][1])
    dx, dy = (zx - x0)*DEN, (zy - y0)*DEN
    chk(dx == RES[k][0] and dy == RES[k][1], f"{k:>2}: residual numerators ({dx},{dy}) == table {RES[k]}")
    chk(abs(dx) < 35520000 and abs(dy) < 35520000, f"{k:>2}: |numerators| < 35520000")
chk(DEN/20000 == 35520000, "710400000000/20000 = 35520000")
h = D("0.00011")
chk(F(47, 37)*eps + D("0.00005") < h, f"(47/37)eps + 0.00005 = {float(F(47,37)*eps + D('0.00005')):.8f} < h = 0.00011")

print("3. Table 2 factors from squared-coordinate integers; bound chains; Table 1 order")
for k in T1:
    x0, y0, Pp, Pm = (D(s) for s in T1[k]); by, bH, a, b = (D(s) for s in T2[k])
    chk(abs(x0) > h and abs(y0) > h, f"{k:>2}: |xi0|,|ups0| > h")
    m, n = abs(x0)*10**5, abs(y0)*10**5
    chk(m.denominator == 1 and n.denominator == 1, f"{k:>2}: m, n integers ({m},{n})")
    xl, xu, yl, yu = ((m-11)**2/F(10**10), (m+11)**2/F(10**10), (n-11)**2/F(10**10), (n+11)**2/F(10**10))
    chk(xl == (abs(x0)-h)**2 and yu == (abs(y0)+h)**2, f"{k:>2}: (m+-11)^2/1e10 formulas agree with (|c|+-h)^2")
    ll, lu = xl + yl, xu + yu
    H = max(abs(3*xl - yu), abs(3*xu - yl))
    chk(yu < by, f"{k:>2}: y_u = {float(yu):.8g} < b_y = {by}")
    chk(H < bH, f"{k:>2}: H = {float(H):.8g} < b_H = {bH}")
    chk(a < ll <= lu < b, f"{k:>2}: a={a} < l_l={float(ll):.6f} <= l_u={float(lu):.6f} < b={b}")
    chk(0 < a and b < 4 and (b < 1 or a > 1), f"{k:>2}: (a,b) in (0,4) and avoids 1")
    chk(by*bH**2 < Pp, f"{k:>2}: b_y b_H^2 = {float(by*bH**2):.8g} < P+ = {Pp}")
    low = a**3*(1 - b/4)*min(abs(a-1), abs(b-1))**2
    chk(low > Pm, f"{k:>2}: a^3(1-b/4)min(|a-1|,|b-1|)^2 = {float(low):.8g} > P'_- = {Pm}")
    chk(Pp < Pm, f"{k:>2}: P+ < P'_-")
chk(D("2.44")*D("2.273")**2 < D("12.65"), "displayed example 2.44(2.273)^2 < 12.65")
chk(D("2.493")**3*(1 - D("2.495")/4)*D("1.493")**2 > D("12.9"), "displayed example (2.493)^3(1-2.495/4)(1.493)^2 > 12.9")
RAD = {"0": ("1.70","1.71"), "A": ("1.28","1.29"), "B": ("0.095","0.096"), "T": ("0.68","0.69"),
       "uA": ("2.73","2.74"), "uB": ("0.459","0.46"), "uT": ("2.49","2.50")}
for k in T2:
    chk(D(RAD[k][0]) <= D(T2[k][2]) and D(T2[k][3]) <= D(RAD[k][1]), f"{k:>2}: listed squared-radius interval {RAD[k]} contains (a,b)")
print("RESULT:", "ALL CHECKS PASS" if not fails else f"{len(fails)} FAILURE(S)")
sys.exit(1 if fails else 0)
