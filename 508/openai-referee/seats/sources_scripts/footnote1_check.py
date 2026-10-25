# Exact check of footnote 1 (p.2): on the unit circle, two points e^{ia}, e^{ib} are at distance 1
# iff a-b = +-pi/3 (mod 2pi). Work in units of pi/3, so the circle is [0,6) and "unit pair" means a-b in {+-1}+6Z.
# A set is a finite union of intervals given as (lo, hi, lo_closed, hi_closed) with rational endpoints.
from fractions import Fraction as Fr
from itertools import product

def diff_interval(I, J):
    # {a-b : a in I, b in J} is an interval with endpoints I.lo-J.hi, I.hi-J.lo
    (a1, b1, ca1, cb1), (a2, b2, ca2, cb2) = I, J
    lo, hi = a1 - b2, b1 - a2
    lo_closed = ca1 and cb2   # attained iff a=a1 and b=b2 both allowed
    hi_closed = cb1 and ca2
    return lo, hi, lo_closed, hi_closed

def contains(iv, x):
    lo, hi, lc, hc = iv
    return (lo < x < hi) or (lc and x == lo) or (hc and x == hi)

def unit_pairs(S):
    hits = []
    for I, J in product(S, S):
        d = diff_interval(I, J)
        for k in range(-3, 4):
            for t in (Fr(1) + 6*k, Fr(-1) + 6*k):
                if contains(d, t):
                    hits.append((I, J, t))
    return hits

def measure(S):  # in units of pi/3 (assumes disjoint intervals)
    return sum(hi - lo for lo, hi, _, _ in S)

cases = {
  "footnote arc [0,pi/3) (half-open)":            [(Fr(0), Fr(1), True, False)],
  "three alternating arcs [0,1)u[2,3)u[4,5)":      [(Fr(0),Fr(1),True,False),(Fr(2),Fr(3),True,False),(Fr(4),Fr(5),True,False)],
  "CONTROL closed arc [0,pi/3]":                  [(Fr(0), Fr(1), True, True)],
  "CONTROL arc [0,pi/2) (too long)":              [(Fr(0), Fr(3,2), True, False)],
  "CONTROL [0,1)u[2,3)u[4,5]  (last closed)":     [(Fr(0),Fr(1),True,False),(Fr(2),Fr(3),True,False),(Fr(4),Fr(5),True,True)],
}
for name, S in cases.items():
    h = unit_pairs(S)
    print(f"{name:45s} measure = {measure(S)}*(pi/3)   unit pair present: {bool(h)}" + (f"   e.g. difference {h[0][2]}*(pi/3)" if h else ""))

# numeric sanity: sample the half-open arc densely, max chord length must stay < 1
import math
N = 20000
pts = [i*(math.pi/3)/N for i in range(N)]   # t in [0, pi/3)
mx = max(2*math.sin(abs(pts[-1]-pts[0])/2), 0)
print("numeric: max chord in sampled half-open arc =", mx, "(<1:", mx < 1, ")")
