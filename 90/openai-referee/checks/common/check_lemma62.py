# Lemma 6.2 toy: exact P(G, X(p) notin U(q,theta)) under the joint law P_E(p,q) P(theta|q),
# maximised over ALL (q,theta)-measurable selection rules U (and events G), vs 8*eta.
# Floats with a 1e-12 tolerance that favours the ADVERSARY (admissibility is loosened).
import itertools, random
random.seed(62)
TOL = 1e-12

def analyse(X, Hh, E, nA, nB, k, eta, mode="paper", c_relax=None):
    nE = len(E)
    P = sorted({p for p, _ in E}); Q = sorted({q for _, q in E})
    nbr = {q: [] for q in Q}
    for p, q in E: nbr[q].append(p)
    dP = {}
    for p, _ in E: dP[p] = dP.get(p, 0) + 1
    mu = {p: dP[p] / nE for p in P}
    kap = {q: len(nbr[q]) / nE for q in Q}
    muH = {}
    for p in P: muH[Hh[p]] = muH.get(Hh[p], 0) + mu[p]
    nu = {h: {} for h in muH}
    for p in P:
        nu[Hh[p]][X[p]] = nu[Hh[p]].get(X[p], 0) + mu[p] / muH[Hh[p]]
    thr = 1 - 3 * eta ** 2 if c_relax is None else 1 - c_relax
    total = 0.0
    for q in Q:
        dq = len(nbr[q])
        nut = {}
        for p in nbr[q]:
            for x, w in nu[Hh[p]].items():
                nut[x] = nut.get(x, 0) + w / dq
        supp = sorted(nut)
        # candidate supports. Adding zero-nu~ states to a <=2-set only helps containment, so the
        # adversary's admissible <=2-sets may be taken inside supp(nu~_q).
        cands = [('row', a) for a in range(nA)] + [('col', b) for b in range(nB)]
        # any member x of an admissible <=2-set has nu~(x) >= thr - max nu~ (its partner is at most
        # the top atom), so only those atoms can occur; this prunes nothing admissible.
        top = max(nut.values())
        supp2 = [x for x in supp if nut[x] >= thr - top - TOL]
        cands += [('set', frozenset(S)) for r in range(3) for S in itertools.combinations(supp2, r)]
        excl = frozenset(X[p] for p in nbr[q])
        if mode == 'any':      # CONTROL: arbitrary subsets allowed
            cands.append(('set', frozenset(supp) - excl))
        if mode == 'rowsub':   # CONTROL: 'row' = any subset of a row
            for a in range(nA):
                cands.append(('set', frozenset(x for x in supp if x[0] == a) - excl))
        def member(x, U):
            t, v = U
            return x[0] == v if t == 'row' else (x[1] == v if t == 'col' else x in v)
        adm = [U for U in cands if sum(w for x, w in nut.items() if member(x, U)) >= thr - TOL]
        if not adm: continue
        hq = {}
        for p in nbr[q]: hq[Hh[p]] = hq.get(Hh[p], 0) + 1 / dq
        for theta in itertools.product(sorted(hq), repeat=k):
            pth = 1.0
            for h in theta: pth *= hq[h]
            # P(X(p) notin U | q, theta) computed from the joint law: the template is drawn from
            # k further iid neighbours, so given (q,theta) p is still uniform on nbr[q]
            best = max(sum(1 for p in nbr[q] if not member(X[p], U)) / dq for U in adm)
            total += kap[q] * pth * best
    return total

def build(nA, nB, nH, nP, nQ, skew):
    X = [(0, 0) if random.random() < skew else (random.randrange(nA), random.randrange(nB)) for _ in range(nP)]
    Hh = [random.randrange(nH) for _ in range(nP)]
    odd = [p for p in range(nP) if X[p] != (0, 0)]
    E = set()
    for q in range(nQ):
        pool = odd if (odd and random.random() < 0.5) else list(range(nP))
        for p in random.sample(pool, min(random.randint(1, 4), len(pool))):
            E.add((p, q))
    return X, Hh, sorted(E)

worst = (0, None); viol = 0
for trial in range(600):
    nH = random.randint(1, 3)
    X, Hh, E = build(3, 3, nH, random.randint(6, 18), random.randint(3, 9), random.choice([0.6, 0.8, 0.9, 0.97]))
    for eta in (0.01, 0.025, 0.05, 1 / 12, 1 / 9):
        v = analyse(X, Hh, E, 3, 3, 2, eta)
        if v > 8 * eta + 1e-12: viol += 1
        if v / eta > worst[0]: worst = (v / eta, (trial, eta, v))
print("PAPER hypothesis, 600 random instances x 5 etas: violations of <= 8 eta:", viol,
      "; max P/eta =", round(worst[0], 3), worst[1])

# Hand-made instance aimed at the Markov step: one history whose nu_h has mass 3eta^2 off the
# heavy state, all of it on the neighbours of a single centre.
for eta in (0.05, 0.1):
    N = 400; n_odd = int(N * 3 * eta ** 2)
    X = [(1, 1)] * n_odd + [(0, 0)] * (N - n_odd); Hh = [0] * N
    E = sorted([(p, 0) for p in range(n_odd)] + [(p, 1 + p) for p in range(n_odd, N)])
    v = analyse(X, Hh, E, 2, 2, 2, eta)
    print(f"hand-made eta={eta}: P(G,X notin U)={v:.4f} (= mu-mass of odd states {n_odd/N:.4f}); 8eta={8*eta:.2f}")

# Structured family aimed at the Markov step of the proof: "q-type" centres see a 3*eta fraction of
# neighbours whose history h1 has nu_h1(U^c) = eta, and ALL those neighbours are outside U={x0}.
def structured(eta, per=20, nq=5, frac_odd=None):
    n_odd = round(per * 3 * eta) if frac_odd is None else frac_odd
    X, Hh, E = [], [], []
    pid = 0
    for q in range(nq):
        for j in range(per):
            if j < n_odd: X.append((1, 1)); Hh.append(1)     # h1-points outside U, at q
            else:         X.append((0, 0)); Hh.append(0)     # h0-points in x0
            E.append((pid, q)); pid += 1
    # h1-points in x0, elsewhere, so that nu_h1(x1) = eta exactly
    n_in = round(nq * n_odd * (1 - eta) / eta)
    for j in range(n_in):
        X.append((0, 0)); Hh.append(1); E.append((pid, nq + j // 19)); pid += 1
    return X, Hh, sorted(E)
best = 0
for eta in (0.05, 0.1):
    for per in (20, 40, 100):
        X, Hh, E = structured(eta, per=per)
        v = analyse(X, Hh, E, 2, 2, 2, eta)
        best = max(best, v / eta)
        print(f"structured eta={eta} per={per}: P(G,X notin U)={v:.4f} = {v/eta:.3f} eta  (lemma: <= 8 eta)")
# random search over the structured family's free parameters (odd count, degrees)
for trial in range(300):
    eta = random.choice([0.02, 0.05, 0.08, 0.1])
    per = random.randint(10, 60)
    odd = random.randint(1, max(1, int(per * 0.5)))
    X, Hh, E = structured(eta, per=per, nq=random.randint(1, 6), frac_odd=odd)
    v = analyse(X, Hh, E, 2, 2, 2, eta)
    assert v <= 8 * eta + 1e-12, (eta, per, odd, v)
    best = max(best, v / eta)
print("max P/eta over structured family + 300 random parameter draws:", round(best, 3), "(lemma: 8)")

eta = 0.05
# CONTROL 1: hypothesis weakened to nu~_q(U) >= 1/2 -> conclusion fails
X = [(0, 0)] * 10 + [(1, 1)] * 10; Hh = [0] * 20
E = sorted([(p, 0) for p in range(10)] + [(p, 1) for p in range(10, 20)])
v1 = analyse(X, Hh, E, 2, 2, 2, eta, c_relax=0.5); v1p = analyse(X, Hh, E, 2, 2, 2, eta)
print(f"CONTROL 1 (mass >= 1/2 only): P={v1} vs 8eta={8*eta} -> conclusion FAILS: {v1 > 8*eta}; "
      f"paper hypothesis on same instance: P={v1p}")
# CONTROL 2: arbitrary supports (type restriction dropped), mass hypothesis kept
X = [(i // 20, i % 20) for i in range(400)]; Hh = [0] * 400
E = sorted((p, p // 2) for p in range(400))
v2 = analyse(X, Hh, E, 20, 20, 1, eta, mode='any'); v2p = analyse(X, Hh, E, 20, 20, 1, eta)
print(f"CONTROL 2 (arbitrary U): P={v2} vs 8eta={8*eta} -> FAILS: {v2 > 8*eta}; restricted types: P={v2p}")
# CONTROL 3: 'row' = any subset of a row
X = [(0, j) for j in range(400)]; Hh = [0] * 400
E = sorted((p, p // 2) for p in range(400))
v3 = analyse(X, Hh, E, 1, 400, 1, eta, mode='rowsub'); v3p = analyse(X, Hh, E, 1, 400, 1, eta)
print(f"CONTROL 3 (row-subsets): P={v3} -> FAILS: {v3 > 8*eta}; full rows: P={v3p}")
