#!/usr/bin/env python3
"""A meaningful negative control for the labels/tau hypothesis (T3): at P=17, I={5,7}, replace tau by an
injection whose values all have 2-adic valuation <= 1 (so tau(iota(q)) != q for q = 4, 8, 16).
Then the classes at the levels 4, 8, 16 should lose their private integers.
(The control 'swap two tau values' in random_split.py is vacuous: it merely relabels the residues t.)"""
import random
from cover import check, ok
from split import Fpp_list, M_F, divisors, build, check_hyp
from random_split import rand_instance

P, I = 17, {5, 7}
trees, pad, iota, tau = rand_instance(random.Random(3), P, I)
cls = build(P, I, trees, pad, iota, tau)
r = check([(a, n) for a, n, _ in cls]); print("base instance:", {k: r[k] for k in ('covering', 'minimal', 'distinct', 'k')})
MFP = M_F(P, I)
low2 = [d for d in divisors(MFP) if d % 4]          # v_2(d) <= 1
QF = Fpp_list(P, I)
tau2 = [None] * P; tau2[0] = 1
for q in QF:
    if q % 4: tau2[iota[q]] = q
rest = [d for d in low2 if d not in set(tau2)]
for t in range(P):
    if tau2[t] is None: tau2[t] = rest.pop()
print("hypothesis check:", check_hyp(P, I, trees, pad, iota, tau2), " tau2 =", tau2)
cls = build(P, I, trees, pad, iota, tau2)
r = check([(a, n) for a, n, _ in cls])
print("tau with v_2 <= 1:", {k: r[k] for k in ('covering', 'minimal', 'distinct')}, "classes without a private integer:", r['no_private'])
print("=> minimal distinct covering:", ok(r))
