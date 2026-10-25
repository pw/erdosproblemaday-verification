"""Seat T toy checks for printed Sections 5-6.

(A) s=2 end-to-end: a genuine pair of paths with EQUAL endpoint in the free group K and
    weight ratio 1/k, built by hand for A={0,1}; Lemma 5.3 synchronisation done exactly;
    then the Hales-Jewett realisation bookkeeping (Lemma 5.5 output simulated: every common
    column gets an arbitrary string, identical across roles) with exact distance check.
(B) s=3 equilateral triangle: synthetic weight-1/t paths with diagonal factors containing
    inverses; same bookkeeping, exact arithmetic.
(C) Negative controls: (i) a role-dependent string in a common column, (ii) using the
    weight-1/t' path with t' != t, (iii) unequal-endpoint pair fed to synchronisation.
All arithmetic is exact (sympy).
"""
import random, sys
import sympy as sp

random.seed(int(sys.argv[1]) if len(sys.argv) > 1 else 1)

# ---------- vectors in E = R^(N): tuples, canonicalised, trailing zeros stripped ----------
def canon(v):
    v = [sp.radsimp(sp.expand(x)) for x in v]
    while v and v[-1] == 0:
        v.pop()
    return tuple(v)

def vadd(a, b):
    n = max(len(a), len(b))
    a = list(a) + [0] * (n - len(a)); b = list(b) + [0] * (n - len(b))
    return canon([x + y for x, y in zip(a, b)])

def vscale(c, a):
    return canon([c * x for x in a])

def vsub(a, b):
    return vadd(a, vscale(-1, b))

def sqn(a):
    return sp.radsimp(sp.expand(sum(x * x for x in a)))

def key(v):
    return tuple(sp.srepr(x) for x in v)

# ---------- free group K on letters xi_z: reduced words of (vector, +-1) ----------
def fmul(*ws):
    out = []
    for w in ws:
        for (z, e) in w:
            if out and key(out[-1][0]) == key(z) and out[-1][1] == -e:
                out.pop()
            else:
                out.append((z, e))
    return tuple(out)

def finv(w):
    return tuple((z, -e) for (z, e) in reversed(w))

def gen(z):
    return ((canon(z), 1),)

def feq(a, b):
    a, b = fmul(a), fmul(b)
    return len(a) == len(b) and all(key(x[0]) == key(y[0]) and x[1] == y[1] for x, y in zip(a, b))

def fmap(w, f):  # endomorphism on letters
    return fmul(*[((f(z), 1),) if e == 1 else ((f(z), -1),) for (z, e) in w])

# ---------- paths ----------
# factor: ('diag', g)  or ('copy', (b_1..b_s), u)
def endpoint(path, s):
    co = [()] * s
    for f in path:
        if f[0] == 'diag':
            co = [fmul(c, f[1]) for c in co]
        else:
            co = [fmul(c, gen(f[1][i])) for i, c in enumerate(co)]
    return co

def weight(path):
    return sp.nsimplify(sum(f[2] for f in path if f[0] == 'copy'))

def check_path(path, A):
    """every copy factor must satisfy ||b_i-b_j||^2 = u ||a_i-a_j||^2"""
    s = len(A)
    for f in path:
        if f[0] == 'copy':
            b, u = f[1], f[2]
            for i in range(s):
                for j in range(s):
                    lhs = sqn(vsub(b[i], b[j])); rhs = sp.radsimp(sp.expand(u * sqn(vsub(A[i], A[j]))))
                    assert sp.simplify(lhs - rhs) == 0, ("bad copy factor", lhs, rhs)

def scale_path(path, c):
    out = []
    for f in path:
        if f[0] == 'diag':
            out.append(('diag', fmap(f[1], lambda z: vscale(c, z))))
        else:
            out.append(('copy', tuple(vscale(c, b) for b in f[1]), sp.nsimplify(c * c * f[2])))
    return out

def synchronise(P1, P2, n, s):
    """Lemma 5.3, literally: returns dict t -> path of weight 1/t, all with one endpoint."""
    lam, mu = weight(P1), weight(P2)
    rho = sp.nsimplify(mu / lam)
    assert rho < sp.Rational(1, n)
    alpha = {t: (sp.Rational(1, t) - rho) / (1 - rho) for t in range(1, n + 1)}
    pts = sorted(set([sp.Integer(0)] + list(alpha.values())))
    assert pts[0] == 0 and pts[-1] == 1
    intervals = [(pts[k], pts[k + 1]) for k in range(len(pts) - 1)]
    big, small = [], []
    for (lo, hi) in intervals:
        l = hi - lo
        assert l > 0
        c = sp.sqrt(l / lam)
        Pb, Ps = scale_path(P1, c), scale_path(P2, c)
        assert sp.simplify(weight(Pb) - l) == 0 and sp.simplify(weight(Ps) - rho * l) == 0
        assert all(feq(x, y) for x, y in zip(endpoint(Pb, s), endpoint(Ps, s)))
        big.append(Pb); small.append(Ps)
    out = {}
    for t in range(1, n + 1):
        path = []
        for k, (lo, hi) in enumerate(intervals):
            path += big[k] if hi <= alpha[t] else small[k]
        assert sp.simplify(weight(path) - sp.Rational(1, t)) == 0, (t, weight(path))
        out[t] = path
    ends = [endpoint(out[t], s) for t in out]
    for e in ends[1:]:
        assert all(feq(x, y) for x, y in zip(e, ends[0])), "synchronised endpoints differ"
    return out, ends[0]

# ---------- Hales-Jewett realisation bookkeeping ----------
def rand_string(dim):
    L = random.randint(0, 3)
    return [canon([sp.Rational(random.randint(-5, 5), random.randint(1, 4)) for _ in range(dim)]) for _ in range(L)]

def realise_line(w, paths, A, n, t, mutate=None):
    s = len(A)
    var = sorted(random.sample(range(n), t))
    fixed = {m: random.randrange(s) for m in range(n) if m not in var}
    # columns per role: ('common', label) or ('principal', z)
    cols = []
    for m in range(n):
        if m in fixed:
            cols.append(('common', ('psi', w[fixed[m]])))
        else:
            P = paths[mutate[1] if mutate and mutate[0] == 'wrongt' else t]
            for f in P:
                if f[0] == 'diag':
                    cols.append(('common', ('psi', f[1])))
                else:
                    cols += [('common', 'p'), ('principal', f[1]), ('common', 'p')]
    # group-level consistency: column product == word product in K, for every role
    for i in range(s):
        prod = ()
        for c in cols:
            if c[0] == 'common':
                prod = fmul(prod, c[1][1] if c[1] != 'p' else ())
            else:
                prod = fmul(prod, gen(c[1][i]))
        word = fmul(*[w[fixed[m]] if m in fixed else w[i] for m in range(n)])
        if not (mutate and mutate[0] == 'wrongt'):
            assert feq(prod, word), "column expansion does not multiply back to the word"
    # Lemma 5.5 output: common column -> one string for all roles; principal -> (z_i)
    dim = 4
    strings = [[] for _ in range(s)]
    for ci, c in enumerate(cols):
        if c[0] == 'common':
            st = rand_string(dim)
            for i in range(s):
                if mutate and mutate[0] == 'rolecommon' and ci == mutate[1] and i == 0:
                    strings[i] += rand_string(dim) or [canon([1])]
                else:
                    strings[i] += st
        else:
            for i in range(s):
                strings[i].append(c[1][i])
    lens = [len(x) for x in strings]
    if len(set(lens)) != 1:
        return 'lengths differ', lens
    # Phi: letter j into block j  =>  ||Phi(z)-Phi(z')||^2 = sum_j ||z_j - z'_j||^2  (19)
    D = {}
    for i in range(s):
        for j in range(s):
            D[i, j] = sp.radsimp(sp.expand(sum(sqn(vsub(x, y)) for x, y in zip(strings[i], strings[j]))))
    ok = all(sp.simplify(D[i, j] - sqn(vsub(A[i], A[j]))) == 0 for i in range(s) for j in range(s))
    return ok, D

# ================= (A) s = 2, A = {0, 1}: genuine equal-endpoint pair =================
def demo_two_point(n):
    A = [canon([0]), canon([1])]
    s = 2
    z, zp = canon([0]), canon([1])          # ||z - z'|| = 1 = ||a_1 - a_2||
    P1 = [('copy', (z, zp), sp.Integer(1))]
    k = n + 1                                # ratio 1/k < 1/n
    ys = [vadd(zp, vscale(sp.Rational(m, k), vsub(z, zp))) for m in range(k + 1)]
    P2 = [('diag', gen(zp))]
    for m in range(k):
        P2 += [('diag', finv(gen(ys[m]))), ('copy', (ys[m + 1], ys[m]), sp.Rational(1, k * k))]
    check_path(P1, A); check_path(P2, A)
    e1, e2 = endpoint(P1, s), endpoint(P2, s)
    assert all(feq(x, y) for x, y in zip(e1, e2)), "hand-built pair does not share an endpoint"
    assert weight(P1) == 1 and weight(P2) == sp.Rational(1, k)
    paths, w = synchronise(P1, P2, n, s)
    for t in paths:
        check_path(paths[t], A)
    res = []
    for t in range(1, n + 1):
        for rep in range(3):
            ok, D = realise_line(w, paths, A, n, t)
            assert ok is True, ("distance bookkeeping failed", t, D)
            res.append(t)
    return len(res)

# ================= (B) s = 3 equilateral triangle, synthetic paths =================
def rot_embed(u, plane, cs, b0, A):
    """sqrt(u) * R a_i + b0, R = rotation (cos,sin)=cs into coordinate plane (p,q)."""
    c, s_ = cs
    out = []
    for a in A:
        x, y = (a + (0, 0))[:2]
        v = [0] * 8
        v[plane[0]] = c * x - s_ * y
        v[plane[1]] = s_ * x + c * y
        out.append(vadd(vscale(sp.sqrt(u), canon(v)), b0))
    return tuple(out)

def rand_word(dim, L):
    w = ()
    for _ in range(L):
        z = canon([sp.Rational(random.randint(-3, 3), 2) for _ in range(dim)])
        w = fmul(w, gen(z) if random.random() < .5 else finv(gen(z)))
    return w

def synthetic_path(A, total):
    parts = random.randint(1, 3)
    cuts = sorted(sp.Rational(random.randint(1, 9), 10) for _ in range(parts - 1))
    us = [b - a for a, b in zip([0] + cuts, cuts + [1])]
    us = [u * total for u in us if u > 0]
    P = []
    for u in us:
        P.append(('diag', rand_word(5, random.randint(0, 3))))
        plane = random.sample(range(8), 2)
        cs = random.choice([(sp.Rational(3, 5), sp.Rational(4, 5)), (sp.Rational(5, 13), sp.Rational(-12, 13)), (1, 0)])
        b0 = canon([sp.Rational(random.randint(-4, 4), 3) for _ in range(6)])
        P.append(('copy', rot_embed(u, plane, cs, b0, A), u))
    P.append(('diag', rand_word(5, random.randint(0, 2))))
    return P

def demo_triangle(n):
    A = [canon([0, 0]), canon([1, 0]), canon([sp.Rational(1, 2), sp.sqrt(3) / 2])]
    paths = {t: synthetic_path(A, sp.Rational(1, t)) for t in range(1, n + 1)}
    for t in paths:
        check_path(paths[t], A)
    # NB synthetic: endpoints differ across t, so only the distance bookkeeping is exercised;
    # w is taken as each t's own endpoint for the multiply-back check.
    cnt = 0
    for t in range(1, n + 1):
        w = endpoint(paths[t], 3)
        for rep in range(3):
            ok, D = realise_line(w, paths, A, n, t)
            assert ok is True, ("triangle bookkeeping failed", t, D)
            cnt += 1
    return cnt

# ================= (C) negative controls =================
def controls(n):
    A = [canon([0]), canon([1])]
    z, zp = canon([0]), canon([1])
    P1 = [('copy', (z, zp), sp.Integer(1))]
    k = n + 1
    ys = [vadd(zp, vscale(sp.Rational(m, k), vsub(z, zp))) for m in range(k + 1)]
    P2 = [('diag', gen(zp))]
    for m in range(k):
        P2 += [('diag', finv(gen(ys[m]))), ('copy', (ys[m + 1], ys[m]), sp.Rational(1, k * k))]
    paths, w = synchronise(P1, P2, n, 2)
    fails = {}
    # (i) role-dependent string in a common column -> must break distances or lengths
    got = []
    for rep in range(6):
        r = realise_line(w, paths, A, n, 2, mutate=('rolecommon', 0))
        got.append(r[0] is not True)
    fails['role-dependent common column detected'] = sum(got)
    # (ii) wrong path weight at variable positions -> distances must be off
    got = []
    for rep in range(6):
        r = realise_line(w, paths, A, n, 2, mutate=('wrongt', 1))
        got.append(r[0] is not True)
    fails['wrong-weight path detected'] = sum(got)
    # (iii) unequal endpoints must be caught by synchronise's endpoint assertion
    P3 = P2[:-1] + [('copy', (ys[k - 1], ys[k]), sp.Rational(1, k * k))]   # swapped roles in last factor
    try:
        synchronise(P1, P3, n, 2)
        fails['unequal-endpoint pair detected'] = 0
    except AssertionError:
        fails['unequal-endpoint pair detected'] = 1
    return fails

if __name__ == '__main__':
    for n in (1, 2, 3, 4):
        print('A  s=2 equal-endpoint pair, n=%d: %d line realisations exact' % (n, demo_two_point(n)))
    for n in (2, 3, 4):
        print('B  equilateral triangle, n=%d: %d line realisations exact' % (n, demo_triangle(n)))
    print('C  negative controls (n=3):', controls(3))
