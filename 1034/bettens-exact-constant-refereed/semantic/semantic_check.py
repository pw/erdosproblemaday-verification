"""Semantic check of identity (31) for Erdos #1034 (Bettens): evaluate every term as a graphon
integral on random 0/1 step graphons, exactly over Q(sqrt3). Shares no code with verify.py.
Usage: python3 semantic_check.py DEPOSIT_DIR SEED NTRIALS [mutate]
"""
import sys, json, gzip, random, itertools
from fractions import Fraction as Fr
import numpy as np

dep, seed, ntrials = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
mutate = sys.argv[4] if len(sys.argv) > 4 else None
model = json.load(open(dep + "/verification_model.json"))
cert = json.load(gzip.open(dep + "/certificate.json.gz"))

def K(p): return (Fr(p[0]), Fr(p[1]))            # a + b*sqrt3
def kadd(x, y): return (x[0] + y[0], x[1] + y[1])
def kmul(x, y): return (x[0]*y[0] + 3*x[1]*y[1], x[0]*y[1] + x[1]*y[0])
def kscale(x, r): return (x[0]*r, x[1]*r)
ZERO = (Fr(0), Fr(0))

def pairlist(n): return list(itertools.combinations(range(n), 2))
def mask_of(n, adj):  # adj(i,j)->0/1
    m = 0
    for b, (i, j) in enumerate(pairlist(n)):
        if adj(i, j): m |= 1 << b
    return m
def edges_of(n, mask): return {(i, j) for b, (i, j) in enumerate(pairlist(n)) if mask >> b & 1}
CAN = {}
def canon(n, k, mask):
    key = (n, k, mask)
    if key in CAN: return CAN[key]
    E = edges_of(n, mask); best = None
    for perm in itertools.permutations(range(k, n)):
        p = list(range(k)) + list(perm)
        m = mask_of(n, lambda i, j: (min(p[i], p[j]), max(p[i], p[j])) in E)
        best = m if best is None or m < best else best
    CAN[key] = best; return best

c_star = K(model["definitions"]["c_star"])
mats = [[[K(e) for e in row] for row in M] for M in cert["matrices"]]
lam = [K(e) for e in cert["scalar_multipliers"]]
slack = [K(e) for e in cert["graph_slacks"]]
if mutate == "slack":   # perturb the slack of the graph with most edges among nonzero slacks
    i = model["graph_slack_flags"].index(0); slack[i] = kadd(slack[i], (Fr(1, 10**6), Fr(0)))  # empty 7-vertex graph
if mutate == "matrix":
    M = mats[5]; M[0][1] = kadd(M[0][1], (Fr(1, 1000), Fr(0))); M[1][0] = M[0][1]
if mutate == "beta": lam[816] = kadd(lam[816], (Fr(1, 1000), Fr(0)))
if mutate == "cstar": c_star = kadd(c_star, (Fr(1, 1000), Fr(0)))

# blocks: flag-basis quadratic forms G = C^T Q C over canonical flags
blocks = []
for b, M in zip(model["matrix_blocks"], mats):
    k, smask = b["type"]; n = b["flag_order"]
    vecs = []
    for comb in b["basis"]:
        d = {}
        for fm, co in comb:
            cf = canon(n, k, fm); d[cf] = d.get(cf, 0) + Fr(co)
        vecs.append(d)
    G = {}
    for i, vi in enumerate(vecs):
        for j, vj in enumerate(vecs):
            q = M[i][j]
            if q == ZERO: continue
            for a, ca in vi.items():
                for bb, cb in vj.items():
                    G[(a, bb)] = kadd(G.get((a, bb), ZERO), kscale(q, ca * cb))
    blocks.append((b["kind"], k, smask, n, G))

# 7-vertex class table from the slack graphs, via all 5040 relabellings (numpy)
P7 = pairlist(7); pidx = {p: i for i, p in enumerate(P7)}
reps = np.array(model["graph_slack_flags"], dtype=np.int64)
table = np.full(1 << 21, -1, dtype=np.int32)
for perm in itertools.permutations(range(7)):
    out = np.zeros_like(reps)
    for b, (i, j) in enumerate(P7):
        t = pidx[(min(perm[i], perm[j]), max(perm[i], perm[j]))]
        out |= ((reps >> b) & 1) << t
    prev = table[out]
    assert np.all((prev == -1) | (prev == np.arange(1044))), "two slack graphs are isomorphic"
    table[out] = np.arange(1044)
assert np.all(table >= 0), "slack graphs do not cover all labelled 7-vertex graphs"
print("class table: 1044 classes cover all 2^21 labelled graphs", flush=True)

def evaluate(Kp, A, m):
    S = sum(m); parts = range(Kp)
    adj = lambda x, y: A[x][y]
    total = ZERO
    # rho = 1/2 * edge density
    total = kadd(total, (Fr(sum(m[a]*m[b]*A[a][b] for a in parts for b in parts), 2*S*S), Fr(0)))
    # D(x) numerator
    def dnum(x):
        return sum(m[y] for y in parts if A[x[0]][y] + A[x[1]][y] + A[x[2]][y] >= 2)
    for kind, k, smask, n, G in blocks:
        e = n - k
        roots_ok = lambda x: all((A[x[i]][x[j]] == 1) == bool(smask >> bb & 1) for bb, (i, j) in enumerate(pairlist(k)))
        acc = {}   # (f,g) -> Fraction weight (already includes (c*-D) handled below)
        accD = {}
        for x in itertools.product(parts, repeat=k):
            if not roots_ok(x): continue
            wx = 1
            for r in x: wx *= m[r]
            cnt = {}
            for ys in itertools.product(parts, repeat=e):
                verts = list(x) + list(ys)
                fm = mask_of(n, lambda i, j: A[verts[i]][verts[j]])
                w = 1
                for y in ys: w *= m[y]
                f = canon(n, k, fm); cnt[f] = cnt.get(f, 0) + w
            dn = dnum(x) if kind == "triangle_localizer_psd" else None
            for f, cf in cnt.items():
                for g, cg in cnt.items():
                    acc[(f, g)] = acc.get((f, g), 0) + wx * cf * cg
                    if dn is not None: accD[(f, g)] = accD.get((f, g), 0) + wx * cf * cg * dn
        den = S ** (k + 2 * e)
        val = ZERO
        for key, q in G.items():
            a = acc.get(key, 0)
            if kind == "triangle_localizer_psd":
                # (c* - D) * f*g : c* a/den - accD/(den*S)
                term = kadd(kscale(kmul(q, c_star), Fr(a, den)), kscale(q, Fr(-accD.get(key, 0), den * S)))
            else:
                term = kscale(q, Fr(a, den))
            val = kadd(val, term)
        total = kadd(total, val)
    # scalar localizers [[(c*-D) F_j]]_tau, F_j order-6 tau-flags
    sg = model["scalar_generators"]
    want = {}
    for j in range(816):
        assert sg[j][0] == "P_flag" and sg[j][1] == 6
        want[canon(6, 3, sg[j][2])] = j
    accS = {}
    for x in itertools.product(parts, repeat=3):
        if not (A[x[0]][x[1]] and A[x[0]][x[2]] and A[x[1]][x[2]]): continue
        wx = m[x[0]] * m[x[1]] * m[x[2]]; dn = dnum(x)
        for ys in itertools.product(parts, repeat=3):
            verts = list(x) + list(ys)
            f = canon(6, 3, mask_of(6, lambda i, j: A[verts[i]][verts[j]]))
            if f not in want: continue
            w = wx * m[ys[0]] * m[ys[1]] * m[ys[2]]
            a, ad = accS.get(f, (0, 0)); accS[f] = (a + w, ad + w * dn)
    for f, (a, ad) in accS.items():
        q = lam[want[f]]
        total = kadd(total, kadd(kscale(kmul(q, c_star), Fr(a, S**6)), kscale(q, Fr(-ad, S**7))))
    # rooted Bollobas: type K4 - 01, sector = common neighbours of roots 0,1
    B = Fr(0)
    for x in itertools.product(parts, repeat=4):
        ok = (A[x[0]][x[1]] == 0) and all(A[x[i]][x[j]] for i, j in [(0, 2), (0, 3), (1, 2), (1, 3), (2, 3)])
        if not ok: continue
        wx = m[x[0]] * m[x[1]] * m[x[2]] * m[x[3]]
        w = [Fr(m[y] * A[x[0]][y] * A[x[1]][y], S) for y in parts]
        X = sum(w)
        E = sum(w[y] * w[z] * A[y][z] for y in parts for z in parts)
        T = sum(w[y] * w[z] * w[u] * A[y][z] * A[y][u] * A[z][u] for y in parts for z in parts for u in parts)
        P = sum(w[y] * w[z] * w[u] for y in parts for z in parts for u in parts if A[y][z] + A[y][u] + A[z][u] == 2)
        B += Fr(wx, S**4) * (X**3 - 11 * X * E + 30 * T + 15 * P)
    total = kadd(total, kscale(lam[816], B))
    # constant
    total = kadd(total, kadd(lam[817], kscale(lam[818], Fr(-1))))
    # slacks: p(H;W) by iid 7-tuples
    mv = np.array(m, dtype=np.int64); Am = np.array(A, dtype=np.int64)
    tup = np.array(list(itertools.product(parts, repeat=7)), dtype=np.int64)
    mask = np.zeros(len(tup), dtype=np.int64)
    for b, (i, j) in enumerate(P7): mask |= Am[tup[:, i], tup[:, j]] << b
    wts = np.prod(mv[tup], axis=1)
    cls = table[mask]
    sums = np.bincount(cls, weights=None, minlength=1044)  # unused counts
    pH = {}
    for c, w in zip(cls.tolist(), wts.tolist()): pH[c] = pH.get(c, 0) + w
    for h, w in pH.items():
        total = kadd(total, kscale(slack[h], Fr(w, S**7)))
    return total, len(pH)

rng = random.Random(seed)
bad = 0
for t in range(ntrials):
    Kp = rng.choice([4, 5, 6])
    A = [[0] * Kp for _ in range(Kp)]
    for a in range(Kp):
        for b in range(a, Kp):
            A[a][b] = A[b][a] = rng.randint(0, 1)
    m = [rng.randint(1, 4) for _ in range(Kp)]
    tot, nh = evaluate(Kp, A, m)
    ok = tot == ZERO
    bad += not ok
    print(f"trial {t}: K={Kp} m={m} A={A} classes_hit={nh} residual={'0' if ok else (float(tot[0]), float(tot[1]))}", flush=True)
print("SEMANTIC", "PASS" if bad == 0 else f"FAIL ({bad}/{ntrials})", "mutate=" + str(mutate))
