"""Seat T toy checks for printed Section 6.

(D) Lemma 6.2 for s=3 (equilateral triangle, side 1): build the commutator correction
    z_a z_b z_a^{-1} z_b^{-1} EXPLICITLY as a right fraction u v^{-1} with u, v products of
    diagonal factors and GENUINE unit congruent triangles in E, following (24) literally,
    and check u v^{-1} = ([a,b], 1, 1) with [a,b] != 1.
(E) Lemma 6.3 membership step, depth 0 -> 1 (= s-2 for s=3): H = S_3 acting on R^3,
    Z = union of orbits; after the normalise-then-average step (27) on every orbit, every
    within-orbit difference must lie in N^(1) = [N,N].  Membership in [N,N] is tested exactly
    with Fox derivatives projected to Z[K/N] = Z[t,t^-1] (the relation-module embedding
    N/[N,N] -> (+)_z Z[t^{+-1}] is injective).  Negative controls: before averaging, and
    with a non-uniform product, the instrument must report NOT in [N,N].
(F) the pure group identities quoted in Lemma 6.1, (23), (24), (30), on random words.
"""
import random, itertools, sys
import sympy as sp

random.seed(int(sys.argv[1]) if len(sys.argv) > 1 else 7)

# ---- free group on hashable letters ----
def fmul(*ws):
    out = []
    for w in ws:
        for (z, e) in w:
            if out and out[-1][0] == z and out[-1][1] == -e:
                out.pop()
            else:
                out.append((z, e))
    return tuple(out)

def finv(w):
    return tuple((z, -e) for (z, e) in reversed(w))

def g(z):
    return ((z, 1),)

def tmul(*ts):  # tuples in K^s
    return tuple(fmul(*[t[i] for t in ts]) for i in range(len(ts[0])))

def tinv(t):
    return tuple(finv(x) for x in t)

def diag(x, s):
    return tuple(x for _ in range(s))

# ================= (D) explicit commutator right fraction for the triangle =================
def key(v):
    return tuple(sp.srepr(sp.nsimplify(x)) for x in v)

def tri(p, q, plane, sign=1):
    """third vertex of the unit equilateral triangle on p,q (vectors in R^8)."""
    m = [(a + b) / 2 for a, b in zip(p, q)]
    d = [b - a for a, b in zip(p, q)]
    # rotate d by 90 degrees inside `plane`
    perp = [0] * 8
    perp[plane[0]] = -d[plane[1]]
    perp[plane[1]] = d[plane[0]]
    h = sp.sqrt(3) / 2 * sign
    return [sp.nsimplify(mi + h * pi) for mi, pi in zip(m, perp)]

def dist2(p, q):
    return sp.simplify(sum((a - b) ** 2 for a, b in zip(p, q)))

def copy_factor(pts):
    """X_b for an ordered triple; asserts it is a unit congruent copy of the triangle."""
    for i in range(3):
        for j in range(3):
            if i != j:
                assert dist2(pts[i], pts[j]) == 1, "not a unit equilateral copy"
    return tuple(g(key(p)) for p in pts)

def demo_commutator():
    s = 3
    E = lambda *c: [sp.Integer(x) for x in c] + [0] * (8 - len(c))
    z, zp = E(0, 0), E(1, 0)                 # an edge in plane (0,1)
    w, wp = E(0, 0, 5, 0), E(0, 0, 6, 0)     # an edge in plane (2,3)
    a = fmul(g(key(z)), finv(g(key(zp))))      # a = xi_z xi_z'^-1  in N
    b = fmul(g(key(w)), finv(g(key(wp))))      # b = xi_w xi_w'^-1  in N
    # z_a in M, supported on {1,2}: copy with roles (1,3) = (z,z'), role 2 = completion; times Delta(xi_z'^-1)
    Xa = copy_factor([z, tri(z, zp, (0, 1)), zp])
    c_a = tmul(Xa, diag(finv(g(key(zp))), s))
    assert c_a[0] == a and c_a[2] == ()
    # z_b in M, supported on {1,3}: roles (1,2) = (w,w'), role 3 = completion
    Xb = copy_factor([w, wp, tri(w, wp, (2, 3))])
    c_b = tmul(Xb, diag(finv(g(key(wp))), s))
    assert c_b[0] == b and c_b[1] == ()
    # follow (24) literally for  c_a * c_b * c_a^{-1} * c_b^{-1}
    u, v = c_a, diag((), s)                               # c_a = c_a * 1^{-1}
    u, v = tmul(u, c_b), v                                # J={1,3}: v already trivial on J, aux=1
    u, v = u, tmul(v, c_a)                                # z = 1 * c_a^{-1}, J={1,2}, aux=1, t=v=1
    # z = 1 * c_b^{-1}, J={1,3}: need aux in M with (v aux)|_{1,3} = 1, v = c_a; aux = X_{(z',*,z)} Delta(xi_z^-1)
    Xaux = copy_factor([zp, tri(zp, z, (0, 1)), z])
    aux = tmul(Xaux, diag(finv(g(key(z))), s))
    t = tmul(v, aux)
    assert t[0] == () and t[2] == (), "aux does not trivialise v on J"
    u, v = tmul(u, aux), tmul(t, c_b)                     # (u aux c)(t d)^{-1} with c=1, d=c_b
    lhs = tmul(u, tinv(v))
    comm = fmul(a, b, finv(a), finv(b))
    assert lhs == (comm, (), ()), ("fraction != commutator at coordinate 1", lhs)
    assert comm != ()
    deg_u = 3; deg_v = 3   # u = Xa,Xb,Xaux ; v = Xa,Xaux,Xb (each a unit copy factor)
    return len(comm), deg_u + deg_v

# ================= (E) Lemma 6.3 membership, Fox-derivative test =================
def exp_sum(w):
    return sum(e for _, e in w)

def fox(w):
    """projected Fox derivatives: letter -> {power: coeff} in Z[t,t^-1]"""
    D = {}
    p = 0
    for (x, e) in w:
        d = D.setdefault(x, {})
        if e == 1:
            d[p] = d.get(p, 0) + 1
        else:
            d[p - 1] = d.get(p - 1, 0) - 1
        p += e
    return {x: {k: c for k, c in d.items() if c} for x, d in D.items() if any(d.values())}

def in_NN(w):
    return exp_sum(w) == 0 and fox(w) == {}

def act(perm, x):
    return tuple(x[perm[i]] for i in range(len(x)))

def demo_averaging(skip_orbit=None, nonuniform=False):
    H = list(itertools.permutations(range(3)))
    seeds = [(1, 2, 3), (1, 1, 2), (4, 4, 4), (0, 7, 7)]
    orbits = []
    for sd in seeds:
        orbits.append(sorted(set(act(h, sd) for h in H)))
    Z = [x for O in orbits for x in O]
    W = {x: g(x) for x in Z}        # w_x = xi_x, degree 1
    deg = 1
    before = all(in_NN(fmul(W[x], finv(W[y]))) for O in orbits for x in O for y in O)
    for oi, O in enumerate(orbits):
        if oi == skip_orbit:
            continue
        x0 = O[0]
        c = finv(W[x0])
        W = {x: fmul(W[x], c) for x in Z}                       # diagonal right factor
        assert all(exp_sum(W[x]) == 0 for x in O)               # values on O now in N
        Hs = H[:-1] if nonuniform else H
        W = {x: fmul(*[W[act(h, x)] for h in Hs]) for x in Z}   # (27)
        deg *= len(Hs)
    after = {}
    for oi, O in enumerate(orbits):
        after[oi] = all(in_NN(fmul(W[x], finv(W[y]))) for x in O for y in O)
    maxlen = max(len(W[x]) for x in Z)
    return before, after, deg, maxlen

# ================= (F) pure identities on random words =================
def rw(L, alph=6):
    w = ()
    for _ in range(L):
        w = fmul(w, ((random.randrange(alph), random.choice((1, -1))),))
    return w

def rt(s, L=4):
    return tuple(rw(L) for _ in range(s))

def demo_identities(trials=200):
    s = 4
    for _ in range(trials):
        x, y = rw(5), rw(5)
        # Lemma 6.1: (x,y)^{-1} = (x^-1,x^-1)(y,x)(y^-1,y^-1)
        assert tinv((x, y)) == tmul((finv(x), finv(x)), (y, x), (finv(y), finv(y)))
        assert tmul((x, y), (finv(y), finv(y))) == (fmul(x, finv(y)), ())
        # (23): u v^{-1} g^[i] = (u a)(v b)^{-1}  when h^[i] = a b^{-1}, h = v_i^{-1} g v_i
        u, v, gg, i = rt(s), rt(s), rw(5), random.randrange(s)
        h = fmul(finv(v[i]), gg, v[i])
        hi = tuple(h if k == i else () for k in range(s))
        a = rt(s); bb = tmul(tinv(hi), a)                     # a bb^{-1} = h^[i]
        gi = tuple(gg if k == i else () for k in range(s))
        assert tmul(u, tinv(v), gi) == tmul(tmul(u, a), tinv(tmul(v, bb)))
        # (24): z supported on J, t = v b trivial on J  =>  u v^{-1} z = (u b c)(t d)^{-1}
        J = random.sample(range(s), 2)
        z = tuple(rw(4) if k in J else () for k in range(s))
        c = rt(s); d = tmul(tinv(z), c)                      # c d^{-1} = z
        b = tuple(finv(v[k]) if k in J else rw(3) for k in range(s))
        t = tmul(v, b)
        assert all(t[k] == () for k in J)
        assert tmul(u, tinv(v), z) == tmul(tmul(u, b, c), tinv(tmul(t, d)))
        # (30): A_j B_j^{-1} = (A_{j-1} (a_j b_j^{-1}) A_{j-1}^{-1}) (A_{j-1} B_{j-1}^{-1})
        As, Bs = [rw(4) for _ in range(5)], [rw(4) for _ in range(5)]
        A_, B_ = (), ()
        for aj, bj in zip(As, Bs):
            lhs = fmul(A_, aj, finv(fmul(B_, bj)))
            rhs = fmul(A_, aj, finv(bj), finv(A_), A_, finv(B_))
            assert lhs == rhs
            A_, B_ = fmul(A_, aj), fmul(B_, bj)
        # Prop 6.4: w_f^{-1} w_g = w_f^{-1} r^{-1} w_f with r = w_f w_g^{-1}
        wf, wg = rw(6), rw(6)
        r = fmul(wf, finv(wg))
        assert fmul(finv(wf), wg) == fmul(finv(wf), finv(r), wf)
    return trials

if __name__ == '__main__':
    L, cost = demo_commutator()
    print('D  triangle: ([a,b],1,1) = u v^{-1} with unit triangles; |[a,b]| =', L, ' cost =', cost)
    print('E  averaging (all orbits):', demo_averaging())
    print('E- control, orbit 1 skipped:', demo_averaging(skip_orbit=1))
    print('E- control, product over H minus one element:', demo_averaging(nonuniform=True))
    print('F  identities checked on', demo_identities(), 'random instances')
