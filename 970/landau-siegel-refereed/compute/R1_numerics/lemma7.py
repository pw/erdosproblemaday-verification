"""Small exact checks for the paper's §4-§5 objects.
Elements of R=Z[a,b] (a^2=d, b^2=2) as 4-tuples (z1,z2,z3,z4) = z1+z2 a+z3 b+z4 ab.
1) greedy weighted retention of rows R_alpha (exact over K via Fractions)
2) Nm(Delta) exactly, as det of the 4M x 4M restriction-of-scalars integer matrix
3) compare v_p(Nm Delta) with 4*E_p, E_p = sum floor(alpha1/p), for primes of every Frobenius class
   (positive: admissible p; negative control: p with Frob = tau or id, where the paper does NOT claim it).
"""
import sys, itertools, math
from fractions import Fraction as F

def mk(d):
    def mul(x, y):
        x1,x2,x3,x4 = x; y1,y2,y3,y4 = y
        return (x1*y1 + d*x2*y2 + 2*x3*y3 + 2*d*x4*y4,
                x1*y2 + x2*y1 + 2*(x3*y4 + x4*y3),
                x1*y3 + x3*y1 + d*(x2*y4 + x4*y2),
                x1*y4 + x4*y1 + x2*y3 + x3*y2)
    return mul

def sig(z): return (z[0], -z[1], z[2], -z[3])
def tau(z): return (z[0], z[1], -z[2], -z[3])
def st(z):  return (z[0], -z[1], -z[2], z[3])
def add(x,y): return tuple(a+b for a,b in zip(x,y))
def sub(x,y): return tuple(a-b for a,b in zip(x,y))
def iszero(x): return all(c==0 for c in x)

def run(d, N, H, maxw_extra=None):
    mul = mk(d)
    one = (1,0,0,0)
    def pw(x, k):
        r = one
        for _ in range(k): r = mul(r, x)
        return r
    def norm(z):
        return mul(mul(z, sig(z)), mul(tau(z), st(z)))[0]
    def inv(z):  # z^{-1} in K as Fraction tuple
        c = mul(sig(z), mul(tau(z), st(z)))
        n = norm(z)
        return tuple(F(ci, n) for ci in c)
    E = list(itertools.product(range(N), repeat=4))
    M = len(E)
    th = [(n[0], n[1], n[2], n[3]) for n in E]
    # candidate indices by weight
    def row(al):
        return [mul(mul(pw(t, al[0]), pw(sig(t), al[1])), pw(st(t), al[2])) for t in th]
    # exact incremental echelon over K (Fractions)
    basis = []  # list of (pivot col, row as Fraction tuples normalized pivot=1)
    retained = []
    w = 0
    while len(retained) < M:
        cands = sorted([al for al in itertools.product(range(w+1), repeat=3)
                        if al[0] + H*al[1] + H*al[2] == w])
        for al in cands:
            r = [tuple(F(c) for c in e) for e in row(al)]
            for (pc, b) in basis:
                if not iszero(r[pc]):
                    f = r[pc]
                    r = [sub(ri, mulF(mul, f, bi)) for ri, bi in zip(r, b)]
            nz = [j for j in range(M) if not iszero(r[j])]
            if nz:
                pc = nz[0]
                iv = invF(mul, r[pc])
                r = [mulF(mul, iv, ri) for ri in r]
                basis.append((pc, r))
                retained.append(al)
                if len(retained) == M: break
        w += 1
    return mul, th, retained, M

def mulF(mul, x, y):
    # multiply Fraction tuples using integer mul via common denominators
    dx = math.lcm(*[c.denominator for c in x]); dy = math.lcm(*[c.denominator for c in y])
    xi = tuple(int(c*dx) for c in x); yi = tuple(int(c*dy) for c in y)
    z = mul(xi, yi)
    return tuple(F(c, dx*dy) for c in z)

def invF(mul, x):
    dx = math.lcm(*[c.denominator for c in x])
    xi = tuple(int(c*dx) for c in x)
    c = mul(sig(xi), mul(tau(xi), st(xi)))
    n = mul(xi, c)[0]
    return tuple(F(ci*dx, n) for ci in c)

def int_det(A):
    # Bareiss fraction-free determinant over Z
    A = [r[:] for r in A]; n = len(A); sign = 1; prev = 1
    for k in range(n-1):
        if A[k][k] == 0:
            sw = next((i for i in range(k+1, n) if A[i][k] != 0), None)
            if sw is None: return 0
            A[k], A[sw] = A[sw], A[k]; sign = -sign
        for i in range(k+1, n):
            for j in range(k+1, n):
                A[i][j] = (A[i][j]*A[k][k] - A[i][k]*A[k][j]) // prev
        prev = A[k][k]
    return sign*A[n-1][n-1]

def mulmat(d, z):
    # 4x4 integer matrix of multiplication by z in basis 1,a,b,ab (columns = images of basis)
    mul = mk(d)
    basis = [(1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1)]
    cols = [mul(z, e) for e in basis]
    return [[cols[j][i] for j in range(4)] for i in range(4)]

def vp(n, p):
    n = abs(n); v = 0
    while n % p == 0: n //= p; v += 1
    return v

def legendre(x, p):
    r = pow(x % p, (p-1)//2, p)
    return -1 if r == p-1 else r

if __name__ == '__main__':
    d = int(sys.argv[1]); N = int(sys.argv[2]); H = int(sys.argv[3])
    mul, th, ret, M = run(d, N, H)
    W = [a[0] + H*a[1] + H*a[2] for a in ret]
    S1 = sum(a[0] for a in ret); S2 = sum(a[1]+a[2] for a in ret)
    U = N**(4/3)
    print(f"d={d} N={N} H={H} M={M} retained max weight={max(W)} bound 96H^(2/3)U={96*H**(2/3)*U:.1f}  S1={S1} S2={S2} max a1={max(a[0] for a in ret)}")
    # rows matrix over R (integer tuples), then restriction of scalars
    def pw(x,k):
        r=(1,0,0,0)
        for _ in range(k): r=mul(r,x)
        return r
    rows = [[mul(mul(pw(t,a[0]), pw(sig(t),a[1])), pw(st(t),a[2])) for t in th] for a in ret]
    big = [[0]*(4*M) for _ in range(4*M)]
    for i in range(M):
        for j in range(M):
            m = mulmat(d, rows[i][j])
            for r in range(4):
                for c in range(4):
                    big[4*i+r][4*j+c] = m[r][c]
    nm = int_det(big)
    print("Nm(Delta) != 0:", nm != 0, " log10|Nm| =", f"{math.log10(abs(nm)):.1f}" if nm else '-')
    # Hadamard check
    import cmath
    sq = math.sqrt(abs(d)); embs = []
    for sa in (1,-1):
        for sb in (1,-1):
            av = complex(0, sq*sa) if d < 0 else sa*sq
            bv = sb*math.sqrt(2)
            embs.append((av, bv))
    mx = max(abs(t[0]+t[1]*av+t[2]*bv+t[3]*av*bv) for t in th for av,bv in embs)
    had = 4*(M/2*math.log(M) + (S1+S2)*math.log(mx)) if mx>0 else 0
    print(f"log|Nm| = {math.log(abs(nm)):.1f} <= Hadamard {had:.1f}: {math.log(abs(nm)) <= had}")
    for p in [3,5,7,11,13,17,19,23,29,31,37,41,43]:
        if p <= 2 or abs(d) % p == 0: continue
        chi = legendre(d, p); two = legendre(2, p)
        frob = {(-1,1):'sigma',(-1,-1):'sigma*tau',(1,1):'id',(1,-1):'tau'}[(chi,two)]
        Ep = sum(a[0]//p for a in ret)
        adm = (chi == -1 and p > H)
        print(f"  p={p:3d} chi={chi:+d} (2/p)={two:+d} Frob={frob:9s} admissible={adm!s:5s} 4E_p={4*Ep:4d}  v_p(Nm)={vp(nm,p):4d}  "
              f"{'OK' if vp(nm,p) >= 4*Ep else 'v_p < 4E_p'}")
