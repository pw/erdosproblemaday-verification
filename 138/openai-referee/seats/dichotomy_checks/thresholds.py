# Exact threshold scan for every "for sufficiently large k" inequality used in 05-dichotomy.tex,
# with the paper's parameters (02-setup.tex): D=ceil(k^(1/10)), M=ceil(k^(1/2)), h0=D^2, H=k^-2, eta=1/(1000D).
# All comparisons in exact rational arithmetic (Fraction); integer roots exact via isqrt / integer search.
from fractions import Fraction as F
from math import isqrt
import sys

def ceil_root(k, r):
    # least integer D with D^r >= k  (= ceil(k^(1/r)))
    lo, hi = 1, 2
    while hi**r < k: hi *= 2
    while lo < hi:
        mid = (lo+hi)//2
        if mid**r >= k: hi = mid
        else: lo = mid+1
    return lo

def params(k):
    D = ceil_root(k, 10); M = ceil_root(k, 2)
    return dict(D=D, M=M, h0=D*D, H=F(1, k*k), eta=F(1, 1000*D))

# Each inequality: (name, paper location, predicate(k, p)) ; h ranges handled by worst case (h=1 or h=2M).
INEQ = [
 ("I1  m*-1 >= k/(2M)  [via k/M - 1 >= k/(2M), i.e. k >= 2M]", "drift proof l.1", lambda k,p: k >= 2*p['M']),
 ("I2  2kH < 1", "affinity hyp. as used in drift", lambda k,p: 2*k*p['H'] < 1),
 ("I3  6MH/k < 1", "drift: |v-lam u|", lambda k,p: 6*p['M']*p['H']/k < 1),
 ("I4  (1-2MH)/(2M) > H", "path: incongruent=>distinct", lambda k,p: (1-2*p['M']*p['H'])/(2*p['M']) > p['H']),
 ("I4' (1-2MH_x)/(2M) > H_x (first system only, H_x<=H; checked as 4MH<1)", "path (sharp form)", lambda k,p: 4*p['M']*p['H'] < 1),
 ("I5  2H + 4MH/h < 1 for all h>=1", "heavy-width", lambda k,p: 2*p['H'] + 4*p['M']*p['H'] < 1),
 ("I6  4MH/h < 1/2 for all h>=1", "short-motion", lambda k,p: 4*p['M']*p['H'] < F(1,2)),
 ("I7  2H(k+1) < 1", "short: width < |w_i|", lambda k,p: 2*p['H']*(k+1) < 1),
 ("I8  4MH/k < eta", "longer: drift < eta", lambda k,p: 4*p['M']*p['H']/k < p['eta']),
 ("I9  D(4 eta + 1/h0) < 1/2", "regular-fraction", lambda k,p: p['D']*(4*p['eta'] + F(1,p['h0'])) < F(1,2)),
 ("I10 2MH_x/k <= H_x and 4MH/k <= H (k >= 4M)", "longer: eligibility (ii)", lambda k,p: k >= 4*p['M']),
 ("I11 2M/k <= 1/16", "longer: eligibility (iii)", lambda k,p: F(2*p['M'], k) <= F(1,16)),
 ("I12 k - 2M - k/10 >= 4k/5 (worst h=2M)", "longer: covering count", lambda k,p: k - 2*p['M'] - F(k,10) >= F(4*k,5)),
 ("I13 h0 < 2M < k", "setup (used: dilation lemma needs h<=2M)", lambda k,p: p['h0'] < 2*p['M'] < k),
 ("I14 heavy => m*>=2 (k/M >= 1)", "drift: h well defined", lambda k,p: k >= p['M']),
]

KMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 200000
for name, loc, pred in INEQ:
    last_fail = None
    for k in range(3, KMAX+1):
        if not pred(k, params(k)):
            last_fail = k
    print(f"{name:72s} | {loc:34s} | last failure k <= {KMAX}: {last_fail}")
# spot-check a few huge k (monotone regime) exactly
for k in [10**6, 10**8, 10**12, 10**20, 10**40]:
    p = params(k)
    bad = [n.split()[0] for n,_,pr in INEQ if not pr(k,p)]
    print(f"k=10^{len(str(k))-1}: D={p['D']} M={p['M']} failures={bad}")
