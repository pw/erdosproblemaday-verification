# Check (outer:first-weight): k*T_glob*exp(-(delta*M-1)/32) = o(1), using exactly the bounds the
# paper displays: T_glob <= [9(3k^2F+1)^2]^{2D} (count:global), F = k^2*lambda + 2m,
# log lambda <= h0*log(2M) (setup:dilation), m = ceil(k^2 R) <= k^2 R + 1,
# R = log(1+1/(2alpha)) <= (D+1) log q, log q <= c k log k / D + log(2k^2) (setup:q-bounds).
# Reports the first k = 10^e at which the first-family total weight is <= 1/1000
# (half of the 1/500 incident budget). Everything in log space; D, M exact integers.
import math, sys

def iroot_ceil(n, r):
    # exact ceil(n^(1/r)) by binary search on integers
    lo, hi = 0, 1 << (n.bit_length()//r + 2)
    while lo < hi:
        mid = (lo + hi)//2
        if mid**r >= n: hi = mid
        else: lo = mid + 1
    return lo

def logaddexp(a, b):
    m = max(a, b); return m + math.log(math.exp(a-m) + math.exp(b-m))

def log_first_weight(e, Dpow=10, rowfun=None, lean=False):
    k = 10**e; L = e*math.log(10)
    D = iroot_ceil(k, Dpow); M = iroot_ceil(k, 2)
    c = 1e-5; delta = 0.1
    logM2 = math.log(2*M)
    log_lambda = D*D*logM2                       # paper's bound log(lambda) <= h0 log(2M)
    log_q = c*math.exp(L)*L/D + math.log(2) + 2*L
    R = (D+1)*log_q
    log_2m = math.log(2) + logaddexp(2*L + math.log(R), 0.0)
    logF = logaddexp(2*L + log_lambda, log_2m)
    log_inner = logaddexp(math.log(3) + 2*L + logF, 0.0)          # log(3k^2F+1)
    if lean: logT = 2*D*(math.log(16) + 6*log_inner)
    else:    logT = 2*D*(math.log(9) + 2*log_inner)
    rows = (delta*M - 1) if rowfun is None else rowfun(k)
    return L + logT - rows/32, logT, D, M

def first_ok(**kw):
    target = math.log(1/1000)
    hist = []
    for e in range(4, 260):
        v = log_first_weight(e, **kw)[0]
        hist.append((e, v))
    ok = [e for e, v in hist if v <= target]
    first = ok[0] if ok else None
    stays = first is not None and all(v <= target for e, v in hist if e >= first)
    return first, stays, hist

def main():
    first, stays, hist = first_ok()
    print('paper bounds: first k=10^e with first-family weight <= 1/1000: e =', first, '; stays below through e=259:', stays)
    for e in (20, 22, 23, 24, 26, 30, 45, 60):
        v, logT, D, M = log_first_weight(e)
        print('  e=%3d  D=%-8d  log T_glob <= %.4g   (deltaM-1)/32 = %.4g   log(k T e^{-(dM-1)/32}) = %.4g' % (e, D, logT, (0.1*M-1)/32, v))
    f2, s2, _ = first_ok(lean=True)
    print('Lean global-count base 16(3k^2F+1)^6: first e =', f2, '; stays:', s2)
    print('--- CONTROLS (each must FAIL) ---')
    f3, s3, h3 = first_ok(rowfun=lambda k: 0.1*iroot_ceil(k, 4) - 1)
    print('CONTROL rows of size delta*k^{1/4} instead of delta*M: first e =', f3, '; value at e=259: %.4g' % h3[-1][1])
    f4, s4, h4 = first_ok(Dpow=5)
    print('CONTROL D = k^{1/5} instead of k^{1/10} (log T_glob ~ D^3 log M vs M): first e =', f4, '; value at e=259: %.4g' % h4[-1][1])
    return 0
sys.exit(main())
