# EXACT brackets Hc(j) <= H(j) <= Hf(j) (same knapsack construction as slowk.py) computed modulo word-size
# primes with int64 numpy (no overflow by construction: column sums < K*p < 2^63, final cumsum < (B+1)*p < 2^63),
# then reconstructed by CRT.  Usage:  slowk_crt.py job R J idx   (writes residues)   |   slowk_crt.py combine R J
import sys, json, numpy as np
from math import floor, ceil, log2, prod
def primes_below(n):
    s = bytearray([1])*n; s[0]=s[1]=0
    for i in range(2,int(n**.5)+1):
        if s[i]: s[i*i::i]=bytearray(len(s[i*i::i]))
    return [i for i in range(n) if s[i]]
S = [p for p in primes_below(257) if p != 2]
def is_prime(n): return n > 1 and all(n % d for d in range(2, int(n**.5)+1))
MODS = []; x = 2**31 - 1
while len(MODS) < 8:
    if is_prime(x): MODS.append(x)
    x -= 2
def dp_mod(weights, B, p):
    c = np.zeros(B+1, np.int64); c[0] = 1
    for w in weights:
        n = (B + 1 + w - 1)//w*w; K = n//w
        assert K*p < 2**63
        pad = np.zeros(n, np.int64); pad[:B+1] = c
        c = pad.reshape(-1, w).cumsum(axis=0).reshape(-1)[:B+1] % p; del pad
    assert (B+1)*p < 2**63
    return np.cumsum(c) % p
mode, R, J = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]); B = 8*J*R
out = f"/tmp/e488/referee_R/crt_R{R}_J{J}"
if mode == "job":
    i = int(sys.argv[4]); p = MODS[i]
    res = {}
    for name, W in (("f", [floor(log2(q)*R) for q in S]), ("c", [ceil(log2(q)*R) for q in S])):
        C = dp_mod(W, B, p); res[name] = [int(C[8*j*R]) for j in range(J+1)]; del C
    json.dump({"p": p, **res}, open(f"{out}_m{i}.json", "w"))
    print(f"modulus {i} p={p} done")
else:
    rs = [json.load(open(f"{out}_m{i}.json")) for i in range(8)]
    ps = [r["p"] for r in rs]; Mrec = prod(ps[:7])
    def crt(vals, mods):
        x, M = 0, 1
        for v, m in zip(vals, mods):
            t = ((v - x) * pow(M, -1, m)) % m; x += M*t; M *= m
        return x
    H = {}
    ok = True
    for name in ("f", "c"):
        H[name] = []
        for j in range(J+1):
            v = crt([r[name][j] for r in rs[:7]], ps[:7])
            if v % ps[7] != rs[7][name][j] or v.bit_length() > 200: ok = False
            H[name].append(v)
    print(f"R={R} J={J}: CRT from 7 moduli (product 2^{Mrec.bit_length()-1}), 8th-modulus consistency check: {ok}")
    HEX = [1, 128, 9537, 397421, 10913534]
    print("  positive control exact H(0..4) inside [Hc,Hf]:", all(H['c'][j] <= HEX[j] <= H['f'][j] for j in range(5)))
    if R == 2048:
        print("  equals object-int run at j=112,113:",
              (H['c'][112], H['f'][112], H['c'][113], H['f'][113]) ==
              (19663756308570290306837490615260075346157744638482, 19741959316398740655319416052621348910058319709095,
               29358925658528546454237452718394053975124129342927, 29475817255257223914252285401859861991526186093434))
    fast = [k for k in range(J) if 2*H['c'][k+1] > 3*H['f'][k]]
    slow = [k for k in range(J) if 2*H['f'][k+1] <= 3*H['c'][k]]
    print(f"  certified fast (exact): 0..{max(fast)} contiguous={fast == list(range(max(fast)+1))}; certified slow (exact): {slow}")
    for k in range(max(0, J-4), J):
        print(f"  k={k}: {H['c'][k]} <= H(k) <= {H['f'][k]}")
    for k in slow[:2]:
        print(f"  CERT k={k}: 2*Hf(k+1) = {2*H['f'][k+1]} <= 3*Hc(k) = {3*H['c'][k]}")
