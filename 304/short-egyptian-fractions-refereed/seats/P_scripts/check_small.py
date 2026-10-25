# Small-case checks of every explicit inequality stated in Sections 6-8 / Cor 1.2-1.3.
import sys, pickle, math
from fractions import Fraction
PKL = sys.argv[1]
res = pickle.load(open(PKL, 'rb'))
KMAX = max(res)
public_F = {1:1, 2:0, 3:1, 4:6, 5:72, 6:2320, 7:245765, 8:151182379}
public_v = {3:4, 4:11, 5:17, 6:103, 7:733, 8:27539, 9:13856993}
# Sylvester s_1=2, s_{j+1}=s_j(s_j-1)+1
syl = [None, 2]
for j in range(1, 12): syl.append(syl[-1]*(syl[-1]-1)+1)
D = {}
fail = 0
for k in range(1, KMAX+1):
    exps = res[k]
    F = len(exps)
    assert F == public_F[k], (k, F)
    Dk = set()
    for t in exps:
        Dk.update(n for n in t if n >= 2)
        # Cor 1.2 proof: n_i <= k^(2^(i-1)), P_i <= k^(2^i - 1)
        P = 1
        for i, n in enumerate(t, start=1):
            if n > k**(2**(i-1)): print("FAIL n_i bound", k, t, i); fail += 1
            P *= n
            if P > k**(2**i - 1): print("FAIL P_i bound", k, t, i); fail += 1
        # Tang: n_k <= s_k - 1
        if max(t) > syl[k] - 1: print("FAIL Sylvester bound", k, t); fail += 1
    D[k] = Dk
    v = 2
    while v in Dk: v += 1
    ub = 1 + k**(2**(k-1))
    ok_ub = v <= ub
    ok_F = F <= k**(2**k - 1)
    ok_kF = v <= k*F + 2
    ok_syl = v <= syl[k]
    llv = math.log(math.log(v)) if v > math.e else float('nan')
    rhs = k*math.log(2) + (math.log(math.log(k)) if k >= 2 else float('nan'))
    print(f"k={k} F={F} |D_k|={len(Dk)} v(k)={v} (public {public_v.get(k)}) "
          f"v<=1+k^(2^(k-1)):{ok_ub} F<=k^(2^k-1):{ok_F} v<=kF+2:{ok_kF} v<=s_k({syl[k]}):{ok_syl} "
          f"maxden={max(max(t) for t in exps) if exps else None} loglogv={llv:.4f} <= k log2+loglogk={rhs:.4f}: {(llv<=rhs) if k>=2 and v>math.e else 'n/a'}")
    if k in public_v: assert v == public_v[k], (k, v)
    if not (ok_ub and ok_F and ok_kF and ok_syl): fail += 1
for k in range(3, KMAX):
    print(f"D_{k} subset D_{k+1}: {D[k] <= D[k+1]}")
    if not D[k] <= D[k+1]: fail += 1
# D_k contents for small k
for k in range(3, min(KMAX, 5)+1):
    print(f"D_{k} = {sorted(D[k])}")
# Cor 1.3 lower bound exp(exp(k/600)) at small k (claimed only for large k): just print
for k in range(1, KMAX+1):
    print(f"k={k} exp(exp(k/600))={math.exp(math.exp(k/600)):.3f}  exp(exp(k*log2/257))={math.exp(math.exp(k*math.log(2)/257)):.3f}")
print("TOTAL FAILS", fail)
