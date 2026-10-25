# Informational: smallest D at which the per-label second-family weight bound
#   S(D) = sum_{h > D^2} (C D h)^{6D} e^{-h/64}
# is <= 1/1000, with C = (9*16005^2)^{1/3} from the proof of count:local, versus the paper's
# sufficient route (each summand <= e^{-h/128}, needing 6 log(C D^3)/D <= 1/128).
# For D > 384, g(h) = 6D log(CDh) - h/64 is decreasing on h > D^2 with slope <= 6D/D^2 - 1/64,
# so S(D) <= exp(g(D^2+1)) / (1 - exp(6/D - 1/64)).
import math
C = (9*16005**2)**(1/3)
def logS_upper(D, a=6, C=C):
    slope = a/D - 1/64
    assert slope < 0
    return a*D*math.log(C*D*(D*D+1)) - (D*D+1)/64 - math.log(1 - math.exp(slope))
D = 400
while logS_upper(D) > math.log(1/1000): D += 1
print('true-sum route (paper C, 6D): S(D) <= 1/1000 from D =', D, '(k > (D-1)^10 ~ 10^%.1f)' % (10*math.log10(D-1)))
D = 2000
while logS_upper(D, a=14, C=16005) > math.log(1/1000): D += 1
print('true-sum route (Lean 16005, 14D): from D =', D, '(k ~ 10^%.1f)' % (10*math.log10(D-1)))
# CONTROL (must FAIL): at D = 5000 the per-label weight is astronomically large
print('CONTROL D=5000: log S(D) upper bound = %.4g (> log(1/1000) = %.3f)' % (logS_upper(5000), math.log(1/1000)))
