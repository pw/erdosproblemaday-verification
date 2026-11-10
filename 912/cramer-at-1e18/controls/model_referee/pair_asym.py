# continuous-t version of pair.py to see the n -> infinity behaviour of the pair-only HL correction
import math, numpy as np, sys
sys.argv=[sys.argv[0]]
exec(open('/tmp/ref912/pair.py').read().split('for e in map')[0])   # reuse Dfull table
Hs = np.arange(HMAX+1, dtype=float)
def D_of(H):
    out = np.interp(H, Hs, Dfull)
    big = H > HMAX
    out[big] = -0.5*H[big]*np.log(H[big]) - 0.2075*H[big]
    return out
for e in (12, 13, 15, 18, 30, 50, 100, 200, 400):
    L = e*math.log(10); LL = math.log(L); scale = math.exp(0.5*(e*math.log(10) - LL))
    t = np.linspace(1e-3, 60, 600001); dt = t[1]-t[0]
    lnk = math.log(scale) + np.log(t)                     # log k
    H = np.exp(e*math.log(10) - 2*lnk) / (1 + np.exp(-lnk))  # n/(k(k+1))
    logx = e*math.log(10) - lnk
    q = 1/logx
    p0 = np.exp(H*np.log1p(-q))
    g = np.sum(p0 * -np.expm1(q*q*D_of(H))) * dt
    print(f"1e{e}: pair-only gap/scale = {g:.6f}   x L/LL = {g*L/LL:.4f}   x L = {g*L:.4f}   sqrt(pi/2)(LL-2.2417) = {math.sqrt(math.pi/2)*(LL-2.2417):.4f}")
