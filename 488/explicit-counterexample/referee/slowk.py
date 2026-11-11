# Pin the slow step: float brackets at higher resolution, then an EXACT-integer certificate
# (Python ints via numpy object arrays) that 2*H(k+1) <= 3*H(k) for a specific k, and that
# 2*H(k+1) > 3*H(k) for every smaller k that can be certified.
import sys, time, numpy as np
sys.argv = sys.argv
exec(open('/tmp/e488/referee_R/pigeonhole.py').read().split('S = [p for p in primes_below')[0])   # helpers only
S = [p for p in primes_below(257) if p != 2]
from math import floor, ceil, log2
def dp_counts(weights, B, exact=False):
    c = np.zeros(B+1, dtype=object if exact else np.float64); c[0] = 1
    for w in weights:
        n = (B + 1 + w - 1)//w*w
        pad = np.zeros(n, dtype=c.dtype); pad[:B+1] = c
        pad = pad.reshape(-1, w).cumsum(axis=0).reshape(-1)
        c = pad[:B+1]
    return np.cumsum(c)
def brackets(R, J, exact):
    Wf = [floor(log2(p)*R) for p in S]; Wc = [ceil(log2(p)*R) for p in S]
    B = 8*J*R; Cf = dp_counts(Wf, B, exact); Cc = dp_counts(Wc, B, exact)
    return [(Cc[8*j*R], Cf[8*j*R]) for j in range(J+1)]
mode = sys.argv[1]; R = int(sys.argv[2]); J = int(sys.argv[3])
t = time.time(); br = brackets(R, J, mode == "exact")
fast = [k for k in range(J) if 2*br[k+1][0] > 3*br[k][1]]
slow = [k for k in range(J) if 2*br[k+1][1] <= 3*br[k][0]]
print(f"{mode} R={R} J={J} ({time.time()-t:.0f}s): certified fast k: 0..{max(fast)} (contiguous: {fast == list(range(max(fast)+1))}); certified slow k: {slow[:5]}")
if slow and mode == "exact":
    k = slow[0]; lo, hi = br[k]; lo1, hi1 = br[k+1]
    print(f"  k={k}: {lo} <= H(k) <= {hi}")
    print(f"         {lo1} <= H(k+1) <= {hi1}")
    print(f"  2*Hf(k+1) <= 3*Hc(k): {2*hi1 <= 3*lo}  => 2H(k+1) <= 3H(k) certified; T = 256^{k} = 2^{8*k}")
    print(f"  H(k) has {len(str(lo))} digits; 12*Hf(k)/... ratio bound H(k+1)/H(k) <= {hi1/lo:.5f}")
