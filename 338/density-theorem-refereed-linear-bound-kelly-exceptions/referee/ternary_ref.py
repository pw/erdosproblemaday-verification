"""Referee's independent brute force for Theorem B (CLAIMS.md section K).
Not a bitset knapsack: exact pair-count array r2[m] = #{b<c in A : b+c=m} built by enumerating pairs, then exact
per-n searches with inclusion-exclusion on the pairs that touch already-chosen elements; every positive answer is
backed by an explicit witness that is re-verified from scratch.
usage: ternary_ref.py N [variant]   variant in {base, drop12, drop1, shift4}
"""
import numpy as np, sys, time

N = int(sys.argv[1])
variant = sys.argv[2] if len(sys.argv) > 2 else 'base'
t0 = time.time()

def in_X_vec(v):
    """vectorised: all base-3 digits of v are 0 or 1"""
    v = v.copy(); ok = np.ones(len(v), bool)
    while True:
        nz = v > 0
        if not nz.any(): break
        ok &= (v % 3) != 2
        v //= 3
    return ok

xs = np.arange(0, N // 2 + 1, dtype=np.int64)
X = xs[in_X_vec(xs)]
odd = 2 * X + 1
if variant == 'shift4':
    ev = 4 * X + 4              # mutated: 4a -> 4a+4
else:
    ev = 4 * X[X >= 1]
A = np.unique(np.concatenate([odd, ev]))
A = A[(A >= 1) & (A <= N)]
if variant == 'drop12':
    A = A[A != 12]
if variant == 'drop1':
    A = A[A != 1]
inA = np.zeros(N + 1, bool); inA[A] = True
Aset = set(int(a) for a in A)
print(f"variant={variant} N={N} |X|={len(X)} |A|={len(A)}  first: {A[:16].tolist()}", flush=True)

# exact pair counts
r2 = np.zeros(N + 1, np.int32)
for i, a in enumerate(A):
    s = a + A[i + 1:]
    s = s[s <= N]
    if len(s) == 0: break
    r2[s] += 1          # indices unique for fixed a
print(f"r2 built ({time.time()-t0:.1f}s), max r2 = {r2.max()}", flush=True)

# (no full index array: memory)
# order 2 with repetition
half = np.zeros(N + 1, bool); half[0::2] = inA[: N // 2 + 1][: len(half[0::2])]
ord2 = inA | (r2 > 0) | half
miss_ord2 = np.nonzero(~ord2[1:])[0] + 1
print(f"order-2 (repetition allowed) misses in [1,N]: count {len(miss_ord2)} first {miss_ord2[:10].tolist()}")

le2 = inA | (r2 > 0)
exc2 = np.nonzero(~le2[1:])[0] + 1
print(f"not a sum of <=2 distinct: count {len(exc2)}; first {exc2[:12].tolist()}")

def verify(n, parts):
    assert len(set(parts)) == len(parts), (n, parts)
    assert all(p in Aset for p in parts), (n, parts)
    assert sum(parts) == n, (n, parts)

def find3(n):
    """explicit triple {a,b,c} distinct in A with sum n, or None (exhaustive)"""
    av = A[A < n]
    m = n - av
    cnt = r2[m].astype(np.int64)
    other = m - av
    okidx = (other >= 1) & (other <= N)
    sub = np.zeros(len(av), np.int64)
    sub[okidx] = (inA[other[okidx]] & (other[okidx] != av[okidx])).astype(np.int64)
    good = np.nonzero(cnt - sub >= 1)[0]
    if len(good) == 0:
        return None
    a = int(av[good[0]]); mm = n - a
    for b in A[A < mm]:
        b = int(b); c = mm - b
        if b < c and c in Aset and b != a and c != a:
            return (a, b, c)
    raise AssertionError("count said yes but no witness", n)

cand3 = np.nonzero(~le2[1:])[0] + 1
exc3 = []
for n in cand3:
    n = int(n)
    w = find3(n)
    if w is None: exc3.append(n)
    else: verify(n, w)
print(f"not a sum of <=3 distinct (N={N}): {exc3}  ({time.time()-t0:.1f}s)", flush=True)

def find4(n):
    av = A[A < n]
    for i, a in enumerate(av):
        a = int(a)
        bv = av[i + 1:]
        m = n - a - bv
        keep = m >= 3
        bv, m = bv[keep], m[keep]
        if len(bv) == 0: break
        cnt = r2[m].astype(np.int64)
        oa = m - a
        ca = np.zeros(len(m), np.int64)
        k = (oa >= 1) & (oa <= N); ca[k] = (inA[oa[k]] & (oa[k] != a)).astype(np.int64)
        ob = m - bv
        cb = np.zeros(len(m), np.int64)
        k = (ob >= 1) & (ob <= N); cb[k] = (inA[ob[k]] & (ob[k] != bv[k])).astype(np.int64)
        both = (m == a + bv).astype(np.int64)
        good = np.nonzero(cnt - ca - cb + both >= 1)[0]
        if len(good):
            b = int(bv[good[0]]); mm = n - a - b
            for c in A[A < mm]:
                c = int(c); d = mm - c
                if c < d and d in Aset and len({a, b, c, d}) == 4:
                    return (a, b, c, d)
            raise AssertionError("count said yes but no witness", n)
    return None

exc4 = []
wit4 = {}
for n in exc3:
    w = find4(n)
    if w is None: exc4.append(n)
    else:
        verify(n, w); wit4[n] = w
print(f"not a sum of <=4 distinct (N={N}): {exc4}  ({time.time()-t0:.1f}s)")
print("sample 4-witnesses:", {k: wit4[k] for k in list(wit4)[:6]})
pred = []; p = 2
while p <= N: pred.append(p); p *= 3
print("exc3 == {2*3^j <= N}:", exc3 == pred, "| count", len(exc3), "predicted floor(log3(N/2))+1 =", len(pred))
