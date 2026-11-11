# Higher-resolution brackets  Hc(j) <= H(j) <= Hf(j)  (same knapsack construction as slowk.py) computed in
# float64 with an a-priori RIGOROUS relative-error envelope:
#   every pass is a recursive sum of nonnegative terms (column cumsum of length K) -> rel. error <= gamma_{K-1},
#   inputs already carry eps -> eps' = (1+eps)(1+gamma)-1 ; final cumsum over L terms adds gamma_{L-1}.
#   Lo(j) = Cc_float/(1+eps)(1+1e-12),  Hi(j) = Cf_float/(1-eps)(1+1e-12).
# Controls: exact H(0..4) must sit inside; at R=2048 the float values must match the exact-integer run
# (slowk_exact.out) to within eps.
import sys, time, numpy as np
from math import floor, ceil, log2
u = 2.0**-53
def gam(k): return k*u/(1-k*u)
def primes_below(n):
    s = bytearray([1])*n; s[0]=s[1]=0
    for i in range(2,int(n**.5)+1):
        if s[i]: s[i*i::i]=bytearray(len(s[i*i::i]))
    return [i for i in range(n) if s[i]]
S = [p for p in primes_below(257) if p != 2]
HEX = [1, 128, 9537, 397421, 10913534]          # exact, from pigeonhole.out (direct recursive count)
def dp(weights, B):
    c = np.zeros(B+1); c[0] = 1.0; eps = 0.0
    for w in weights:
        n = (B + 1 + w - 1)//w*w; K = n//w
        pad = np.zeros(n); pad[:B+1] = c
        c = pad.reshape(-1, w).cumsum(axis=0).reshape(-1)[:B+1].copy(); del pad
        eps = (1+eps)*(1+gam(K-1)) - 1
    c = np.cumsum(c); eps = (1+eps)*(1+gam(B)) - 1
    return c, eps
R = int(sys.argv[1]); J = int(sys.argv[2]); lo_k = int(sys.argv[3]) if len(sys.argv) > 3 else 95
t = time.time(); B = 8*J*R
Wf = [floor(log2(p)*R) for p in S]; Wc = [ceil(log2(p)*R) for p in S]
Cf, ef = dp(Wf, B); Hf = [Cf[8*j*R] for j in range(J+1)]; del Cf
Cc, ec = dp(Wc, B); Hc = [Cc[8*j*R] for j in range(J+1)]; del Cc
eps = max(ef, ec); f = 1 + 1e-12
Lo = [x/((1+eps)*f) for x in Hc]; Hi = [x*f/(1-eps) for x in Hf]
print(f"R={R} J={J} B={B} ({time.time()-t:.0f}s)  a-priori float envelope eps={eps:.3e}")
ok = all(Lo[j] <= HEX[j] <= Hi[j] for j in range(5))
print(f"  positive control exact H(0..4) inside [Lo,Hi]: {ok}")
if R == 2048:
    ex = {112: (19663756308570290306837490615260075346157744638482, 19741959316398740655319416052621348910058319709095),
          113: (29358925658528546454237452718394053975124129342927, 29475817255257223914252285401859861991526186093434)}
    for j,(c_ex,f_ex) in ex.items():
        print(f"  cross-check vs exact-int run j={j}: |Hc_float/Hc_exact-1|={abs(Hc[j]/c_ex-1):.2e}  |Hf_float/Hf_exact-1|={abs(Hf[j]/f_ex-1):.2e}  (both must be <= eps={eps:.1e})")
status = {}
for k in range(J):
    if 2*Hi[k+1] <= 3*Lo[k]: status[k] = "SLOW (certified)"
    elif 2*Lo[k+1] > 3*Hi[k]: status[k] = "fast (certified)"
    else: status[k] = "undecided"
fast = [k for k in range(J) if status[k].startswith("fast")]; slow = [k for k in range(J) if status[k].startswith("SLOW")]
print(f"  certified fast: 0..{max(fast)} contiguous={fast == list(range(max(fast)+1))}; first certified slow: {slow[0] if slow else None}; undecided: {[k for k in range(J) if status[k]=='undecided']}")
for k in range(lo_k, J):
    print(f"  k={k}: H(k+1)/H(k) in [{Lo[k+1]/Hi[k]:.6f}, {Hi[k+1]/Lo[k]:.6f}]  {status[k]}")
