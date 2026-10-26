"""Try to break Lemma 3: A over K=Q(sqrt2,sqrt3), every coordinate functional of A killing a lattice direction,
most lopsided t allowed by (3.1): t=(t1, 3(N-1), 3(N-1)), t1 minimal. Rank of evaluation computed mod a prime P
split in K (mod-P rank = M certifies char-0 rank = M). Negative control: A with a RATIONAL kernel direction
(violates the hypothesis) must give rank < M by the same code."""
import itertools, sys, random
def find_P():
    P = (1<<61) - 1
    while True:
        P -= 2
        if all(P % q for q in range(3, 2000, 2)) and pow(2,(P-1)//2,P)==1 and pow(3,(P-1)//2,P)==1:
            if pow(5, P-1, P) == 1 and pow(7, P-1, P) == 1:
                return P
P = find_P()
def sqrtmod(x):
    # Tonelli-Shanks
    q, s = P-1, 0
    while q % 2 == 0: q//=2; s+=1
    z = 2
    while pow(z,(P-1)//2,P) != P-1: z += 1
    m, c, t, r = s, pow(z,q,P), pow(x,q,P), pow(x,(q+1)//2,P)
    while t != 1:
        i, tt = 0, t
        while tt != 1: tt = tt*tt % P; i += 1
        b = pow(c, 1 << (m-i-1), P); m, c, t, r = i, b*b%P, t*b*b%P, r*b%P
    return r
r2, r3 = sqrtmod(2), sqrtmod(3)
assert r2*r2 % P == 2 and r3*r3 % P == 3
def rank_mod(rows):
    rows = [r[:] for r in rows]; rk = 0; ncol = len(rows[0])
    piv_rows = []
    for col in range(ncol):
        pr = next((i for i in range(rk, len(rows)) if rows[i][col] % P), None)
        if pr is None: continue
        rows[rk], rows[pr] = rows[pr], rows[rk]
        inv = pow(rows[rk][col], P-2, P)
        rows[rk] = [x*inv % P for x in rows[rk]]
        for i in range(len(rows)):
            if i != rk and rows[i][col]:
                f = rows[i][col]; rows[i] = [(x - f*y) % P for x, y in zip(rows[i], rows[rk])]
        rk += 1
        if rk == len(rows): break
    return rk
def test(A, N, t, label):
    E = list(itertools.product(range(N), repeat=4)); M = len(E)
    pts = [tuple(sum(A[j][i]*n[i] for i in range(4)) % P for j in range(3)) for n in E]
    # evaluation matrix: rows = points, cols = monomials; rank via points x monomials (transpose rank same)
    # build incrementally by z1-degree to keep memory small: rank of [z1^k z2^i z3^j]
    base = [[pow(z2,i,P)*pow(z3,j,P) % P for i in range(t[1]+1) for j in range(t[2]+1)] for (_,z2,z3) in pts]
    # columns grouped: for k in 0..t1: z1^k * base ; stop once rank M reached
    cur = [[] for _ in range(M)]; rk = 0; k = 0
    z1p = [1]*M
    while k <= t[0]:
        for idx in range(M): cur[idx].extend(z1p[idx]*b % P for b in base[idx])
        z1p = [z1p[idx]*pts[idx][0] % P for idx in range(M)]
        k += 1
        if k % 8 == 0 or k > t[0]:
            rk = rank_mod(cur)
            if rk == M: break
            # compress: keep a basis? just continue (sizes are small)
    print(f"{label}: N={N} M={M} t={t} -> rank {rk} at z1-degree <= {k-1}  {'SURJECTIVE' if rk==M else 'NOT surjective'}")
    print("   distinct evaluation points:", len(set(pts)), "(rank upper bound)", flush=True)
    return rk
import builtins
_p = builtins.print
def print(*a, **k): k.setdefault('flush', True); _p(*a, **k)
for N in (2, 3):
    t1 = (4*N-3)**4 + 3*(N-1)  # minimal: (t1-3(N-1)+1) > (4N-3)^4
    t = (t1, 3*(N-1), 3*(N-1))
    s2, s3, s6 = r2, r3, r2*r3 % P
    # each row kills one coordinate direction; entries from {1, sqrt2, sqrt3, sqrt6}
    A = [[1, s2, s3, 0], [1, s3, 0, s6], [1, 0, s6, s2]]
    test(A, N, t, "hyp-A (K=Q(sqrt2,sqrt3))")
    # negative control: kernel contains rational direction e4 (column 4 zero) -> points collide
    Abad = [[1, s2, s3, 0], [s3, 1, s6, 0], [s6, s3, 1, 0]]
    tc = (min(t1, 64), t[1], t[2])
    test(Abad, N, tc, "control A with ker=C e4 (hypothesis violated), t1 capped")
