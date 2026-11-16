"""Seat A: symplectic-geometry checks for Lecomte arXiv:2611.15068 sections 3-4.

Checks
  (1) clique number of W(3,3) (pairwise nonorthogonal projective points of F_3^4) == 7   [Sec 3.1]
      positive control: plane F_q^2 gives q+1; negative control: the checker reports 8 is NOT attainable.
  (2) Lemma 3.1 p=2: max clique of standard binary symplectic form in dim 2r == 2r+1 (r=1..4),
      every maximum clique spans V and sums to zero (r<=3 exhaustively over max cliques).
  (3) Lemma 3.1 lower bound p*r+1 via orthogonal combination, p in {3,5}, r in {1,2,3}.
  (4) Lemma 4.3: for EVERY hyperplane e^perp, the printed recipe gives a clique of size p*r+1 meeting it once.
  (5) Sec 4.3: Ceria-De Beule-Pavese-Smaldore 13-point set in F_27^2 trace model over F_3 is a clique,
      and also the identity b(P_x,P_y) = c*Nm(1-y/x).  Max clique of W(5,3) computed if cheap.
  (6) Lemma 4.6 recipe on random alternating maps beta: V x V -> F_p^2 with a nondegenerate scalarization.
"""
import itertools, random, sys
import networkx as nx
from ortools.sat.python import cp_model

def std_form(p, r):
    def b(u, v):
        s = 0
        for i in range(r):
            s += u[2*i]*v[2*i+1] - u[2*i+1]*v[2*i]
        return s % p
    return b

def proj_points(p, n):
    pts = []
    for v in itertools.product(range(p), repeat=n):
        if any(v):
            first = next(x for x in v if x)
            if first == 1:
                pts.append(v)
    return pts

def max_clique_cpsat(n_vertices, nonadj_pairs, time_limit=600, lower=None):
    """max set of vertices with no pair in nonadj_pairs (i.e. clique in complement of those pairs)."""
    m = cp_model.CpModel()
    x = [m.NewBoolVar(f"x{i}") for i in range(n_vertices)]
    for (i, j) in nonadj_pairs:
        m.AddBoolOr([x[i].Not(), x[j].Not()])
    m.Maximize(sum(x))
    s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = time_limit; s.parameters.num_workers = 4
    st = s.Solve(m)
    return s.ObjectiveValue(), s.BestObjectiveBound(), st == cp_model.OPTIMAL, [i for i in range(n_vertices) if s.Value(x[i])]

def proj_clique_number(p, r, time_limit=600):
    b = std_form(p, r)
    pts = proj_points(p, 2*r)
    orth = [(i, j) for i in range(len(pts)) for j in range(i+1, len(pts)) if b(pts[i], pts[j]) == 0]
    return max_clique_cpsat(len(pts), orth, time_limit), pts

def check1():
    print("== (1) W(3,q) / plane clique numbers ==")
    # positive control: plane over F_q (q prime) -> q+1
    for p in (2, 3, 5, 7):
        (val, bnd, opt, _), _ = proj_clique_number(p, 1)
        print(f"  plane F_{p}^2: clique number {val} (bound {bnd}, optimal={opt}); expected {p+1}")
        assert opt and val == p+1
    (val, bnd, opt, sol), pts = proj_clique_number(3, 2)
    print(f"  W(3,3): clique number {val} (bound {bnd}, optimal={opt}); paper claims 7")
    assert opt and val == 7
    # negative control: ask CP-SAT for a clique of size 8 -> infeasible
    b = std_form(3, 2)
    m = cp_model.CpModel(); x = [m.NewBoolVar("") for _ in pts]
    for i in range(len(pts)):
        for j in range(i+1, len(pts)):
            if b(pts[i], pts[j]) == 0:
                m.AddBoolOr([x[i].Not(), x[j].Not()])
    m.Add(sum(x) >= 8)
    st = cp_model.CpSolver().Solve(m)
    print("  negative control: 8-clique in W(3,3) status:", cp_model.CpSolver().StatusName(st) if False else st, "(3 = INFEASIBLE)")
    assert st == cp_model.INFEASIBLE
    # W(3,5): Tallini bound q^2-q+1 = 21
    (val, bnd, opt, _), _ = proj_clique_number(5, 2, time_limit=300)
    print(f"  W(3,5): clique number {val} (upper bound {bnd}, optimal={opt}); Tallini bound 21")
    assert bnd <= 21 + 1e-9

def check2():
    print("== (2) Lemma 3.1, p=2: maximum 2r+1, spans, sum zero ==")
    for r in range(1, 5):
        b = std_form(2, r)
        vecs = [v for v in itertools.product(range(2), repeat=2*r) if any(v)]
        orth = [(i, j) for i in range(len(vecs)) for j in range(i+1, len(vecs)) if b(vecs[i], vecs[j]) == 0]
        val, bnd, opt, sol = max_clique_cpsat(len(vecs), orth, 300)
        print(f"  r={r}: max clique {val} (optimal={opt}), expected {2*r+1}")
        assert opt and val == 2*r+1
        if r <= 3:
            # enumerate all maximum cliques: build graph of nonorthogonal pairs
            G = nx.Graph(); G.add_nodes_from(range(len(vecs)))
            for i in range(len(vecs)):
                for j in range(i+1, len(vecs)):
                    if b(vecs[i], vecs[j]) == 1:
                        G.add_edge(i, j)
            cnt = 0; bad = 0
            for c in nx.find_cliques(G):
                if len(c) == 2*r+1:
                    cnt += 1
                    s = tuple(sum(vecs[i][k] for i in c) % 2 for k in range(2*r))
                    # rank over F2
                    rows = [int(''.join(map(str, vecs[i])), 2) for i in c]
                    basis = []
                    for x in rows:
                        for y in basis:
                            x = min(x, x ^ y)
                        if x:
                            basis.append(x)
                    if any(s) or len(basis) != 2*r:
                        bad += 1
            print(f"     {cnt} maximum cliques enumerated, {bad} violate span/sum-zero")
            assert cnt > 0 and bad == 0

def combine(X, Y, p):
    y0 = Y[0]
    return [tuple((a + c) % p for a, c in zip(x, y0)) for x in X] + list(Y[1:])

def plane_clique(p, r, i):
    """p+1 vectors in plane i of F_p^{2r} (coords 2i,2i+1), one per line"""
    out = []
    for t in range(p):
        v = [0]*(2*r); v[2*i] = 1; v[2*i+1] = t; out.append(tuple(v))
    v = [0]*(2*r); v[2*i+1] = 1; out.append(tuple(v))
    return out

def is_clique(vs, b):
    return len(set(vs)) == len(vs) and all(b(u, v) != 0 for u, v in itertools.combinations(vs, 2))

def check3():
    print("== (3) Lemma 3.1 lower bound p*r+1 by orthogonal combination ==")
    for p in (2, 3, 5):
        for r in (1, 2, 3):
            b = std_form(p, r)
            X = plane_clique(p, r, 0)
            for i in range(1, r):
                X = combine(plane_clique(p, r, i), X, p)
            ok = is_clique(X, b)
            print(f"  p={p} r={r}: size {len(X)} (expected {p*r+1}), clique={ok}")
            assert ok and len(X) == p*r+1
    # negative control: a set containing two vectors on one line is rejected
    b = std_form(3, 1)
    assert not is_clique([(1, 0), (2, 0), (0, 1)], b)
    print("  negative control (two vectors on a line) rejected: OK")

def lemma43_clique(p, r, e, b):
    """printed recipe: f with b(e,f)=1, V0 = <e,f>^perp, D0 clique of size p(r-1)+1 in V0 ({0} if r=1)"""
    n = 2*r
    allv = list(itertools.product(range(p), repeat=n))
    f = next(v for v in allv if b(e, v) == 1)
    V0 = [v for v in allv if b(e, v) == 0 and b(f, v) == 0]
    if r == 1:
        D0 = [tuple([0]*n)]
    else:
        # find clique of size p(r-1)+1 in V0 greedily via CP-SAT
        nz = [v for v in V0 if any(v)]
        orth = [(i, j) for i in range(len(nz)) for j in range(i+1, len(nz)) if b(nz[i], nz[j]) == 0]
        m = cp_model.CpModel(); x = [m.NewBoolVar("") for _ in nz]
        for i, j in orth:
            m.AddBoolOr([x[i].Not(), x[j].Not()])
        m.Add(sum(x) == p*(r-1)+1)
        s = cp_model.CpSolver(); s.parameters.num_workers = 4
        st = s.Solve(m); assert st in (cp_model.OPTIMAL, cp_model.FEASIBLE)
        D0 = [nz[i] for i in range(len(nz)) if s.Value(x[i])]
    C = [tuple((d[k] + f[k]) % p for k in range(n)) for d in D0] + \
        [tuple((e[k] + t*f[k]) % p for k in range(n)) for t in range(p)]
    return C

def check4():
    print("== (4) Lemma 4.3: every hyperplane meets the recipe clique exactly once ==")
    for p, r in ((2, 1), (2, 2), (2, 3), (3, 1), (3, 2), (5, 1), (5, 2)):
        b = std_form(p, r)
        bad = 0; n = 0
        for e in proj_points(p, 2*r):
            C = lemma43_clique(p, r, e, b)
            meet = [c for c in C if b(e, c) == 0]
            n += 1
            if not (is_clique(C, b) and len(C) == p*r+1 and len(meet) == 1):
                bad += 1
        print(f"  p={p} r={r}: {n} hyperplanes, {bad} failures")
        assert bad == 0

# ---------- F_27 arithmetic ----------
def gf27():
    # F_27 = F_3[t]/(t^3 - t - 1)  (t^3 = t + 1), irreducible over F_3
    els = list(itertools.product(range(3), repeat=3))  # (a0,a1,a2) = a0 + a1 t + a2 t^2
    def mul(a, b):
        c = [0]*5
        for i in range(3):
            for j in range(3):
                c[i+j] += a[i]*b[j]
        # reduce t^4 = t^2 + t, t^3 = t + 1
        c4 = c[4]; c[2] += c4; c[1] += c4; c[4] = 0
        c3 = c[3]; c[1] += c3; c[0] += c3; c[3] = 0
        return tuple(x % 3 for x in c[:3])
    def add(a, b):
        return tuple((x+y) % 3 for x, y in zip(a, b))
    def pw(a, n):
        r = (1, 0, 0)
        for _ in range(n):
            r = mul(r, a)
        return r
    def inv(a):
        return pw(a, 25)
    # check irreducible: field iff every nonzero has inverse
    for a in els:
        if any(a):
            assert mul(a, inv(a)) == (1, 0, 0), "not a field"
    return els, mul, add, pw, inv

def check5():
    print("== (5) Ceria et al. 13-point clique in the F_27 trace model over F_3 ==")
    els, mul, add, pw, inv = gf27()
    one = (1, 0, 0)
    def tr(a):
        s = add(add(a, pw(a, 3)), pw(a, 9)); assert s[1] == 0 and s[2] == 0; return s[0]
    def nm(a):
        s = pw(a, 13); assert s[1] == 0 and s[2] == 0; return s[0]
    neg = lambda a: tuple((-x) % 3 for x in a)
    sub = lambda a, b: add(a, neg(b))
    for c in (1, 2):
        cc = (c, 0, 0)
        X = [x for x in els if any(x) and nm(x) == 1]
        assert len(X) == 13
        # vector (a, b) in F_27^2 with a = x, b = c x^{-1}; F_3-bilinear form Tr(a b' - b a')
        pts = [(x, mul(cc, inv(x))) for x in X]
        def B(u, v):
            return tr(sub(mul(u[0], v[1]), mul(u[1], v[0])))
        ok = all(B(u, v) != 0 for u, v in itertools.combinations(pts, 2))
        # also check the identity b(P_x,P_y) = c Nm(1 - y/x) and = c Tr(x/y - y/x)
        ident = True
        for x, y in itertools.permutations(X, 2):
            lhs = B((x, mul(cc, inv(x))), (y, mul(cc, inv(y))))
            r1 = (c * tr(sub(mul(x, inv(y)), mul(y, inv(x))))) % 3
            r2 = (c * nm(sub(one, mul(y, inv(x))))) % 3
            if not (lhs == r1 == r2):
                ident = False
        print(f"  c={c}: 13 points, pairwise nonorthogonal={ok}, identity Tr=Nm holds={ident}")
        assert ok and ident
    # the trace form Tr(x1 y2 - x2 y1) on F_27^2 is a nondegenerate alternating F_3-form of dim 6
    basis = [(e, (0, 0, 0)) for e in ((1, 0, 0), (0, 1, 0), (0, 0, 1))] + [((0, 0, 0), e) for e in ((1, 0, 0), (0, 1, 0), (0, 0, 1))]
    def B(u, v):
        return tr(sub(mul(u[0], v[1]), mul(u[1], v[0])))
    M = [[B(u, v) for v in basis] for u in basis]
    # rank over F_3
    A = [row[:] for row in M]; rank = 0
    for col in range(6):
        piv = next((i for i in range(rank, 6) if A[i][col] % 3), None)
        if piv is None: continue
        A[rank], A[piv] = A[piv], A[rank]
        invp = 1 if A[rank][col] == 1 else 2
        A[rank] = [(v*invp) % 3 for v in A[rank]]
        for i in range(6):
            if i != rank and A[i][col]:
                f = A[i][col]; A[i] = [(a - f*b) % 3 for a, b in zip(A[i], A[rank])]
        rank += 1
    print(f"  trace form Gram rank over F_3 = {rank} (expected 6), alternating={all(M[i][i]==0 for i in range(6))}")
    assert rank == 6
    # clique number of W(5,3): 364 projective points; compute upper bound with time limit
    (val, bnd, opt, _), _ = proj_clique_number(3, 3, time_limit=240)
    print(f"  W(5,3) clique number: best found {val}, upper bound {bnd}, optimal={opt} (paper only needs >= 13)")
    assert val >= 13

def rand_alt(p, n):
    M = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            a = random.randrange(p); M[i][j] = a; M[j][i] = (-a) % p
    return M

def rank_mod(M, p):
    A = [r[:] for r in M]; n = len(A); m = len(A[0]); rk = 0
    for col in range(m):
        piv = next((i for i in range(rk, n) if A[i][col] % p), None)
        if piv is None: continue
        A[rk], A[piv] = A[piv], A[rk]
        iv = pow(A[rk][col], p-2, p)
        A[rk] = [(v*iv) % p for v in A[rk]]
        for i in range(n):
            if i != rk and A[i][col] % p:
                f = A[i][col]; A[i] = [(a - f*b) % p for a, b in zip(A[i], A[rk])]
        rk += 1
    return rk

def check6():
    print("== (6) Lemma 4.6 recipe on random 2-component alternating maps ==")
    random.seed(117)
    for p, r, trials in ((3, 2, 30), (3, 3, 15), (5, 2, 15), (2, 2, 20), (2, 3, 20), (2, 4, 10)):
        n = 2*r; done = 0; fails = 0; att = 0
        while done < trials and att < 5000:
            att += 1
            Mb = rand_alt(p, n); Mc = rand_alt(p, n)
            if rank_mod(Mb, p) != n:
                continue
            # independence of the two forms (values span W = F_p^2)
            if all(any((Mc[i][j] - s*Mb[i][j]) % p for i in range(n) for j in range(n)) for s in range(p)) is False:
                continue
            if all(Mc[i][j] == 0 for i in range(n) for j in range(n)):
                continue
            if any(all((Mc[i][j] - s*Mb[i][j]) % p == 0 for i in range(n) for j in range(n)) for s in range(p)):
                continue
            bf = lambda u, v, M: sum(u[i]*M[i][j]*v[j] for i in range(n) for j in range(n)) % p
            allv = list(itertools.product(range(p), repeat=n))
            # find v with Sv not in <v>:  c(v,.) not a multiple of b(v,.)
            def indep(v):
                rb = [bf(v, w, Mb) for w in allv]; rc = [bf(v, w, Mc) for w in allv]
                return not any(all((rc[k] - s*rb[k]) % p == 0 for k in range(len(allv))) for s in range(p))
            v = next(v for v in allv if any(v) and indep(v))
            vperp = [w for w in allv if bf(v, w, Mb) == 0]
            # quotient vperp/<v>: choose representatives: canonical rep = lexicographically minimal in w+F_p v
            def canon(w):
                return min(tuple((w[k] + t*v[k]) % p for k in range(n)) for t in range(p))
            reps = sorted(set(canon(w) for w in vperp))
            nzreps = [w for w in reps if w != canon(tuple([0]*n))]
            # need a clique of size p(r-1)+1 in quotient meeting ker c(v,.) exactly once: search CP-SAT
            kerc = [bf(v, w, Mc) == 0 for w in nzreps]
            m = cp_model.CpModel(); x = [m.NewBoolVar("") for _ in nzreps]
            for i in range(len(nzreps)):
                for j in range(i+1, len(nzreps)):
                    if bf(nzreps[i], nzreps[j], Mb) == 0:
                        m.AddBoolOr([x[i].Not(), x[j].Not()])
            m.Add(sum(x) == p*(r-1)+1)
            m.Add(sum(x[i] for i in range(len(nzreps)) if kerc[i]) == 1)
            s = cp_model.CpSolver(); s.parameters.num_workers = 4; st = s.Solve(m)
            if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
                fails += 1; done += 1; print("   no clique meeting kernel once found!", p, r); continue
            C = [nzreps[i] for i in range(len(nzreps)) if s.Value(x[i])]
            S = []
            for w in C:
                if bf(v, w, Mc) == 0:
                    S.append(w)
                else:
                    S += [tuple((w[k] + t*v[k]) % p for k in range(n)) for t in range(p)]
            ok = len(set(S)) == len(S) == p*p*(r-1)+1 and all(
                bf(a, bb, Mb) != 0 or bf(a, bb, Mc) != 0 for a, bb in itertools.combinations(S, 2))
            if not ok:
                fails += 1
            done += 1
        print(f"  p={p} r={r}: {done} random pairs, {fails} recipe failures (target size {p*p*(r-1)+1})")
        assert fails == 0

if __name__ == "__main__":
    which = sys.argv[1:] or ["1", "2", "3", "4", "5", "6"]
    for w in which:
        {"1": check1, "2": check2, "3": check3, "4": check4, "5": check5, "6": check6}[w]()
    print("ALL REQUESTED CHECKS PASSED")
