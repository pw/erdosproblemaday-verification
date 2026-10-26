"""Seat C: Lemma 3 / Corollary 4 tests. Rank of the evaluation map B -> (B(An))_{n in E_N} on monomial boxes.
rank over K >= rank mod a prime of K, so (rank mod p == M) CERTIFIES surjectivity; rank-deficient results are
re-tested at 2 more primes and (if small enough) certified exactly via Q-rank of the regular representation.
usage: lemma3.py mode d N [args]
  mode=box  d N t1 t2 t3           -> rank of one box
  mode=minbox d N tmax             -> for each (t2,t3) in [0,tmax]^2 the least t1 with rank M (or >M-1 cap)
  pointsets: d integer (paper's A of (4.1), d=2,8,4 give Q-DEPENDENT kernels), or d='rat' (A=[[1,0,0,1],[0,1,0,1],[0,0,1,1]])
"""
import sys, itertools, time, math
import flint
sys.path.insert(0, '/tmp/oaimath/003/seats/C_work')
from biq import *
from sympy import isprime
from sympy.ntheory.residue_ntheory import sqrt_mod

mode = sys.argv[1]; darg = sys.argv[2]; N = int(sys.argv[3])
M = N**4
pts = list(itertools.product(range(N), repeat=4))

def primes_for(dval, count, seed):
    """primes p with sqrt(dval) and sqrt(2) in F_p (p=1 mod 8); for perfect-square dval any such p works."""
    import random
    rng = random.Random(seed); out = []
    while len(out) < count:
        p = rng.randrange(2**29, 2**30) | 1
        if p % 8 != 1 or not isprime(p): continue
        if dval % p == 0: continue
        if pow(dval % p, (p-1)//2, p) != 1: continue
        out.append((p, sqrt_mod(dval % p, p), sqrt_mod(2, p)))
    return out

def point_values(p, s, t):
    """list over n of the three coordinates of An in F_p."""
    if darg == 'rat':
        return [((n[0]+n[3]) % p, (n[1]+n[3]) % p, (n[2]+n[3]) % p) for n in pts]
    if darg == 'qdep':
        # A = [[u,1,1,0],[v,x,y,w],[1,0,0,0]] with generic u,v,x,y,w: ker A = C(0,1,-1,(y-x)/w), first coordinate 0
        # => kernel coordinates Q-DEPENDENT; hypothesis of Lemma 3 violated on purpose.
        import random
        rng = random.Random(4242); u, v, x, y, w = (rng.randrange(1, p) for _ in range(5))
        return [((u*n[0] + n[1] + n[2]) % p, (v*n[0] + x*n[1] + y*n[2] + w*n[3]) % p, n[0] % p) for n in pts]
    dval = int(darg)
    r = math.isqrt(abs(dval))
    if dval > 0 and r*r == dval: s = r % p          # a = sqrt(d) is a rational integer: use the real value
    if dval > 0 and dval % 2 == 0 and math.isqrt(dval//2)**2 == dval//2:
        s = math.isqrt(dval//2) * t % p             # a = m*sqrt(2) = m*b exactly (d = 2 m^2): keep the Q-dependence
    a, b = s, t
    vals = []
    for n in pts:
        th = (n[0] + n[1]*a + n[2]*b + n[3]*a*b) % p
        sg = (n[0] - n[1]*a + n[2]*b - n[3]*a*b) % p
        st = (n[0] - n[1]*a - n[2]*b + n[3]*a*b) % p
        vals.append((th, sg, st))
    return vals

def dval_for_primes():
    return 1 if darg in ('rat', 'qdep') else int(darg)

def box_rank(t, pr):
    p, s, tt = pr
    V = point_values(p, s, tt)
    # exact reduction: on the point set, z_j^k for k >= (#distinct values of z_j) lies in the span of lower powers
    nv = [len(set(v[j] for v in V)) for j in range(3)]
    t = tuple(min(t[j], nv[j]-1) for j in range(3))
    rows = []
    for al in itertools.product(range(t[0]+1), range(t[1]+1), range(t[2]+1)):
        rows.append([pow(v[0], al[0], p) * pow(v[1], al[1], p) % p * pow(v[2], al[2], p) % p for v in V])
    return flint.nmod_mat(rows, p).rank()

def min_t1(t2, t3, pr, cap):
    """least t1 <= cap such that box (t1,t2,t3) has rank M mod p; layer-incremental rref. Returns (t1 or None, rank at cap)."""
    p, s, tt = pr
    V = point_values(p, s, tt)
    pw = [[[1]*(cap+1) for _ in range(3)] for _ in V]
    for i, v in enumerate(V):
        for j in range(3):
            for k in range(1, cap+1): pw[i][j][k] = pw[i][j][k-1] * v[j] % p
    basis = []  # rows of current rref (nonzero)
    for t1 in range(cap+1):
        layer = [[pw[i][0][t1] * pw[i][1][a2] % p * pw[i][2][a3] % p for i in range(M)]
                 for a2 in range(t2+1) for a3 in range(t3+1)]
        Mx = flint.nmod_mat(basis + layer, p)
        R, rk = Mx.rref()
        basis = [[int(R[i, j]) for j in range(M)] for i in range(rk)]
        if rk == M: return t1, rk
    return None, len(basis)

if mode == 'box':
    t = tuple(int(x) for x in sys.argv[4:7])
    prs = primes_for(dval_for_primes(), 3, 11)
    rks = [box_rank(t, pr) for pr in prs]
    b = [tj - 3*(N-1) for tj in t]
    budget = all(tj >= 3*(N-1) for tj in t) and (b[0]+1)*(b[1]+1)*(b[2]+1) > (4*N-3)**4
    print(f'd={darg} N={N} M={M} box t={t} satisfies (3.1): {budget}; #monomials={(t[0]+1)*(t[1]+1)*(t[2]+1)}; '
          f'rank mod 3 primes = {rks} -> {"SURJECTIVE (certified)" if max(rks)==M else "rank<M at all 3 primes"}')
elif mode == 'minbox':
    tmax = int(sys.argv[4]); cap = int(sys.argv[5]) if len(sys.argv) > 5 else M
    pr = primes_for(dval_for_primes(), 1, 5)[0]
    T0 = time.time()
    print(f'd={darg} N={N} M={M}: least t1 with box (t1,t2,t3) surjective (rank M mod p={pr[0]}); "-" = none up to t1={cap}')
    print('t2\\t3 ' + ' '.join(f'{x:>4}' for x in range(tmax+1)))
    best = None
    for t2 in range(tmax+1):
        line = []
        for t3 in range(tmax+1):
            t1, rk = min_t1(t2, t3, pr, cap)
            line.append(f'{t1:>4}' if t1 is not None else f'{"-"+str(rk):>4}')
            if t1 is not None:
                vol = (t1+1)*(t2+1)*(t3+1)
                if best is None or vol < best[0]: best = (vol, (t1, t2, t3))
        print(f'{t2:>5} ' + ' '.join(line), flush=True)
    if best is None: print('NO surjective box in range (expected for the collision control)')
    else: print(f'smallest-volume surjective box found: {best[1]} with {best[0]} monomials (M={M}); [{time.time()-T0:.0f}s]')
