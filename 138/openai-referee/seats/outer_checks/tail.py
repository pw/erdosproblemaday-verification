# Check (outer:tail): for X ~ Bin(l,1/2), the bad event "some bit on strictly fewer than
# l/4 of l positions" = {X < l/4} U {l-X < l/4}; paper bounds it by the WEAK tails
# P(X-l/2 <= -l/4) + P(X-l/2 >= l/4) <= 2 e^{-l/8}.  Exact binomial tails (Fraction),
# exp via mpmath at 60 digits. Also checks E e^{+-(X-l/2)} = cosh(1/2)^l, cosh(1/2)<=e^{1/8},
# and (2j)! >= 2^j j!.
import sys, math
from fractions import Fraction as Fr
import mpmath as mp
mp.mp.dps = 60

def tails(l):
    tot = 2**l
    weak = sum(math.comb(l, j) for j in range(l+1) if 4*j <= l or 4*j >= 3*l)     # X<=l/4 or X>=3l/4
    strict = sum(math.comb(l, j) for j in range(l+1) if 4*j < l or 4*(l-j) < l)   # X<l/4 or l-X<l/4
    return Fr(strict, tot), Fr(weak, tot)

def check(bound_exp_den, L=600):
    worst = (0, None); first_fail = None
    for l in range(1, L+1):
        s, w = tails(l)
        assert s <= w
        b = 2*mp.e**(-mp.mpf(l)/bound_exp_den)
        r = mp.mpf(w.numerator)/w.denominator/b
        if r > worst[0]: worst = (r, l)
        if r > 1 and first_fail is None: first_fail = l
    return worst, first_fail

def main():
    worst, ff = check(8)
    print('claim  P <= 2e^{-l/8}, l=1..600: max ratio weak_tail/bound = %s at l=%d; first failure: %s'
          % (mp.nstr(worst[0], 8), worst[1], ff))
    # moment identity and cosh bound
    for l in (1, 2, 5, 17, 40):
        lhs = mp.fsum(mp.binomial(l, j)*mp.mpf(2)**(-l)*mp.e**(j - mp.mpf(l)/2) for j in range(l+1))
        lhs2 = mp.fsum(mp.binomial(l, j)*mp.mpf(2)**(-l)*mp.e**(-(j - mp.mpf(l)/2)) for j in range(l+1))
        assert abs(lhs - mp.cosh(0.5)**l) < mp.mpf(10)**-50 and abs(lhs2 - mp.cosh(0.5)**l) < mp.mpf(10)**-50
    print('E e^{+-(X-l/2)} = cosh(1/2)^l verified for l in (1,2,5,17,40) to 1e-50')
    print('cosh(1/2) =', mp.nstr(mp.cosh(0.5), 15), '<= e^{1/8} =', mp.nstr(mp.e**(mp.mpf(1)/8), 15), ':', mp.cosh(0.5) <= mp.e**(mp.mpf(1)/8))
    assert all(math.factorial(2*j) >= 2**j*math.factorial(j) for j in range(0, 300))
    print('(2j)! >= 2^j j! for j = 0..299: True')
    # strict vs weak: weak strictly larger exactly when some j hits l/4 or 3l/4 (4 | l)
    diff = [l for l in range(1, 41) if tails(l)[0] != tails(l)[1]]
    print('l in 1..40 where weak tail != strict tail:', diff)
    print('--- CONTROLS (each must FAIL) ---')
    worst7, ff7 = check(7)
    print('CONTROL claim P <= 2e^{-l/7}: first l where exact weak tail exceeds it =', ff7, '(max ratio %s at l=%d)' % (mp.nstr(worst7[0], 6), worst7[1]))
    print('CONTROL cosh(1/2) <= e^{1/9}:', mp.cosh(0.5) <= mp.e**(mp.mpf(1)/9))
    print('CONTROL (2j)! >= 3^j j! at j=1:', math.factorial(2) >= 3*math.factorial(1))
    print('CONTROL "weak tail <= strict tail" (reverse of the paper remark) at l=4:', tails(4)[1] <= tails(4)[0])
    kl = 0.75*math.log(1.5) + 0.25*math.log(0.5)
    print('true large-deviation rate KL(3/4||1/2) = %.6f  (> 1/8 = 0.125, < 1/7 = %.6f)' % (kl, 1/7))
    return 0
sys.exit(main())
