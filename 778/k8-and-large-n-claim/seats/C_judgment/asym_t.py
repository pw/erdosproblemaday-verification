#!/usr/bin/env python3
"""Smooth (no-rounding) threshold equation for target density t, optimal multipliers:
   need  L/ln(1/t) - ln(l)/ln(1/t) >= 2L/ln3 + 3   (a ~ 2L/ln3 + 3 worst case, R ~ 1 + log_{1/t}(n/l) - 1)
   l ~ 2L/D(t).  Solve for L by fixed point; report argmin over t."""
import math
LN3 = math.log(3)
D = lambda t: t*math.log(1.5*t) + (1-t)*math.log(3*(1-t))
def L_of(t, extra=3.0):
    L = 50.0
    for _ in range(200):
        l = 2*L/D(t)
        g = 1/math.log(1/t) - 2/LN3
        if g <= 0: return float('inf')
        L = (math.log(l)/math.log(1/t) + extra) / g
    return L
best = min((L_of(t/10000), t/10000) for t in range(5800, 6666))
print("t=0.6:", round(L_of(0.6), 2), " best:", round(best[0], 2), "at t =", best[1])
