# Check (outer:criterion): for l >= 100, given sum_{F in Gamma(E)} z_F <= l/500 and every z_F <= 1/2,
#   z_E prod (1-z_F) >= exp(-(1/32+2/500) l) >= 2 e^{-l/8},   z_E = e^{-l/32}.
# Exact rational part with Fraction; transcendental part with a rational certificate
# (e^x >= 1+x) and with mpmath at 60 digits.
import sys
from fractions import Fraction as Fr
import mpmath as mp
mp.mp.dps = 60

def margin(a_inc):
    # positive difference 1/8 - 1/32 - 2*a_inc  (a_inc = per-label incident weight bound)
    return Fr(1,8) - Fr(1,32) - 2*a_inc

def crit_holds(l, a_inc):
    # exp(-(1/32+2a)l) >= 2 e^{-l/8}  <=>  margin*l >= log 2
    return mp.mpf(margin(a_inc).numerator)/margin(a_inc).denominator*l >= mp.log(2)

def main():
    d = margin(Fr(1,500))
    print('1/8 - 1/32 - 2/500 =', d, '=', float(d), '; times 100 =', d*100)
    # rational certificate: e^{359/40} >= 1 + 359/40 > 2  => log 2 < 359/40
    cert = 1 + d*100
    print('certificate 1 + 100*margin =', cert, '> 2 :', cert > 2, '  (e^x >= 1+x)')
    l = 100
    lhs = mp.e**(-(mp.mpf(1)/32 + mp.mpf(2)/500)*l)
    rhs = 2*mp.e**(-mp.mpf(l)/8)
    print('l=100: exp(-(1/32+2/500)l) = %s ; 2e^{-l/8} = %s ; ratio = %s' % (mp.nstr(lhs,12), mp.nstr(rhs,12), mp.nstr(lhs/rhs,12)))
    assert lhs >= rhs
    assert all(crit_holds(L, Fr(1,500)) for L in range(100, 20001))
    print('criterion holds for every integer l in [100, 20000] (monotone in l)')
    lmin = next(L for L in range(1, 1000) if crit_holds(L, Fr(1,500)))
    print('smallest l at which the second inequality holds:', lmin)
    # log(1-z) >= -2z on [0,1/2]
    grid = [mp.mpf(i)/20000 for i in range(0, 10001)]
    assert all(mp.log(1-z) >= -2*z for z in grid)
    print('log(1-z) >= -2z on 10001-point grid of [0,1/2] incl. endpoints: True; at z=1/2:',
          mp.nstr(mp.log(0.5),10), '>= -1')
    zE = mp.e**(-mp.mpf(100)/32)
    print('z_E at l=100 = e^{-100/32} =', mp.nstr(zE, 10), '< 1/2:', zE < 0.5)
    # sharper worst case for the product given sum z_F = l/500 and each z_F <= zmax:
    # log(1-z)/z is decreasing, so the product is smallest when mass sits on z_F = zmax.
    for L in (100, 101, 150, 1000):
        S = mp.mpf(L)/500
        worst_prod = (1 - zE)**(S/zE)
        val = mp.e**(-mp.mpf(L)/32)*worst_prod
        print('  l=%d: worst-case z_E*prod = %s  vs  paper lower bound %s  vs  2e^{-l/8} = %s' %
              (L, mp.nstr(val,8), mp.nstr(mp.e**(-(mp.mpf(1)/32+mp.mpf(2)/500)*L),8), mp.nstr(2*mp.e**(-mp.mpf(L)/8),8)))
    print('--- CONTROLS (each must FAIL) ---')
    print('CONTROL l=7 (below lmin):', crit_holds(7, Fr(1,500)))
    print('CONTROL per-label incident weight 1/20 instead of 1/500: margin =', margin(Fr(1,20)),
          '; criterion at l=100:', crit_holds(100, Fr(1,20)), '; at l=10^6:', crit_holds(10**6, Fr(1,20)))
    print('CONTROL log(1-z) >= -2z at z=0.8:', mp.log(1-mp.mpf('0.8')) >= -2*mp.mpf('0.8'))
    return 0
sys.exit(main())
