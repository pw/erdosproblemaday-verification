# Prop 5.3 exhaustive check at q=3 (S = full affine elliptic-quadric graph Gamma, 9 points, a cap).
import itertools, numpy as np
q = 3
nu = 2  # nonsquare mod 3
pts = list(itertools.product(range(q), repeat=3))
code = {p: i for i, p in enumerate(pts)}
S = [(x, y, (x*x - nu*y*y) % q) for x in range(q) for y in range(q)]
s = len(S)
mats = []
for e in itertools.product(range(q), repeat=9):
    M = np.array(e).reshape(3, 3)
    if round(np.linalg.det(M)) % q != 0: mats.append(M)
print("|GL3(F3)| =", len(mats))
Sarr = np.array(S).T  # 3 x s
def run(allowed):
    rows = []
    for G in mats:
        for a in allowed:
            V = (G @ ((Sarr + np.array(a).reshape(3, 1)) % q)) % q
            ind = np.zeros(27, dtype=np.int64)
            ind[[code[tuple(V[:, j])] for j in range(s)]] = 1
            rows.append(ind)
    Mx = np.array(rows)          # maps x 27
    nmaps = Mx.shape[0]
    cnt = np.zeros((27, 27, 27), dtype=np.int64)
    for t1 in range(27):
        cnt[t1] = (Mx * Mx[:, t1:t1+1]).T @ Mx
    W = (q**3 / s)**3 * cnt / nmaps
    return W
def classify(t):
    P = [np.array(pts[i]) for i in t]
    zero = any(not p.any() for p in P)
    A = np.stack(P, axis=1)
    def rank_mod(A):
        A = A.copy() % q; r = 0; rows, cols = A.shape
        for c in range(cols):
            piv = next((i for i in range(r, rows) if A[i, c] % q), None)
            if piv is None: continue
            A[[r, piv]] = A[[piv, r]]
            inv = pow(int(A[r, c]), -1, q); A[r] = (A[r] * inv) % q
            for i in range(rows):
                if i != r and A[i, c]: A[i] = (A[i] - A[i, c] * A[r]) % q
            r += 1
        return r
    rk = rank_mod(A)
    affi = rank_mod(np.stack([P[1]-P[0], P[2]-P[0]], axis=1)) == 2
    eq = len(set(t)) < 3
    return zero, rk, affi, eq
b_aff = 2 * q**9 / s**3 * s*(s-1)*(s-2) / (q**3*(q**3-1)*(q**3-q))
b_r2 = q**9 / (s*(q**3-1)*(q**3-q))
b_all = q**9 / (s**2*(q**3-1))
Sset=set(S)
for name, allowed in [("all shifts (0 may lie in V)", pts), ("shifts with 0 not in a+S (density %.3f)" % (len([a for a in pts if tuple((-x)%q for x in a) not in Sset])/27), [a for a in pts if tuple((-x)%q for x in a) not in Sset])]:
    W = run(allowed)
    worst = {"aff": 0, "r2": 0, "all": 0}; supp_bad = 0; exact_aff = set()
    for t in itertools.product(range(27), repeat=3):
        w = W[t]
        zero, rk, affi, eq = classify(t)
        if affi: worst["aff"] = max(worst["aff"], w / b_aff); exact_aff.add(round(w, 9))
        if rk >= 2: worst["r2"] = max(worst["r2"], w / b_r2)
        worst["all"] = max(worst["all"], w / b_all)
        if w > 0 and (zero or not (affi or eq)):
            supp_bad += 1
            if supp_bad <= 2: print("  support exception:", [pts[i] for i in t], "zero col" if zero else "")
    print(f"{name}: max W/bound: affine {worst['aff']:.4f}, rank>=2 {worst['r2']:.4f}, general {worst['all']:.4f}; support violations {supp_bad}; distinct affine W values {sorted(exact_aff)[:6]}")
print("uniform affine-group prediction for affine triples: W =", (q**3/s)**3 * s*(s-1)*(s-2)/(q**3*(q**3-1)*(q**3-q)))
