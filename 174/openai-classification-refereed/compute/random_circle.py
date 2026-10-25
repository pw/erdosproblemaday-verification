#!/usr/bin/env python3
"""Random census: s points on the unit circle at parameters t_i = (a_i tau + b_i)/(c_i tau + d_i) (integer Moebius
images of one transcendental tau; some constant), decided exactly by criterion.py.  Usage: random_circle.py s n seed"""
import sys, random, sympy as sp
from criterion import criterion, tau
s, n, seed = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]); random.seed(seed)
def pt(t): return (sp.together((1 - t**2)/(1 + t**2)), sp.together(2*t/(1 + t**2)))
nh = nf = 0
for trial in range(n):
    while True:
        ts = []
        for i in range(s):
            if random.random() < 0.35: ts.append(sp.Rational(random.randint(-6, 6), random.randint(1, 4)))
            else:
                a, b, c, d = [random.randint(-3, 3) for _ in range(4)]
                if a*d - b*c == 0: a, b, c, d = 1, random.randint(-3, 3), 0, 1
                ts.append(sp.together((a*tau + b)/(c*tau + d)))
        if any(t.has(tau) for t in ts) and len(set(sp.simplify(t) for t in ts)) == s:
            # distinct points: distinct parameters (t -> p(t) injective on the projective line minus i)
            break
    ok = criterion([pt(t) for t in ts], name=f"s={s} trial {trial} ts={[str(t) for t in ts]}")
    nh += ok; nf += (not ok)
print(f"SUMMARY s={s}: HOLDS {nh} FAILS {nf}")
