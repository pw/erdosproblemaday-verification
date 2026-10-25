# (f') EXHAUSTIVE over ALL isometries of R^3 (not only lattice ones) for the grid P = {0..t-1}^3 (t=3).
# An isometry g = (S,h) with a NON-collinear match set maps two independent difference vectors u1,u2 of P to
# difference vectors w1,w2 of P with the same Gram matrix; S is then [w1 w2 +-w1xw2][u1 u2 u1xu2]^-1.
# We enumerate every such S (deduplicated), then count matches k(S,h) for every translation h at once
# (histogram of y - S x over x,y in P).  Collinear match sets have k <= t < A and are irrelevant for k >= C*A.
import itertools, sys, numpy as np
t = int(sys.argv[1]) if len(sys.argv) > 1 else 3
P = np.array(list(itertools.product(range(t), repeat=3)), dtype=float); N = len(P); A = N**(2/3)
V = np.array([v for v in itertools.product(range(-(t-1), t), repeat=3) if any(v)], dtype=float)   # difference vectors
nrm = (V**2).sum(1).round().astype(int)
chunks = []
for a in range(len(V)):
    u1 = V[a]; W1 = V[nrm == nrm[a]]
    for b in range(a+1, len(V)):
        u2 = V[b]; cr = np.cross(u1, u2)
        if not cr.any(): continue
        Finv = np.linalg.inv(np.column_stack([u1, u2, cr]))
        W2 = V[nrm == nrm[b]]
        ii, jj = np.nonzero(np.abs(W1 @ W2.T - u1 @ u2) < 1e-9)
        w1, w2 = W1[ii], W2[jj]; wc = np.cross(w1, w2)
        for sgn in (1, -1):
            G = np.stack([w1, w2, sgn*wc], axis=2)            # columns w1, w2, +-w1xw2
            chunks.append((G @ Finv).reshape(-1, 9))
allS = np.concatenate(chunks)
_, first = np.unique(np.round(allS, 9), axis=0, return_index=True)
Ss = {i: allS[i].reshape(3, 3) for i in first}
print(f"  raw (u1,u2,w1,w2,sign) candidates: {len(allS)}")
print(f"t={t}: N={N}, A={A:.2f}; distinct orthogonal S mapping two independent difference vectors to difference vectors: {len(Ss)}")
assert all(np.allclose(S @ S.T, np.eye(3), atol=1e-9) for S in Ss.values())
ks = []; nlat = 0
for S in Ss.values():
    if np.allclose(S, np.round(S)): nlat += 1
    H = (P[None, :, :] - (P @ S.T)[:, None, :]).reshape(-1, 3)        # y - S x
    keys = np.round(H, 6)
    _, cnt = np.unique(keys, axis=0, return_counts=True)
    ks.append(cnt)
ks = np.concatenate(ks)
print(f"  of which signed permutations (lattice S): {nlat} (expected 48)")
print("  match-count distribution over all (S,h) with k>=4:", {int(k): int((ks == k).sum()) for k in np.unique(ks) if k >= 4})
for C in (0.5, 1.0, 2.0):
    sel = ks[ks >= C*A].astype(np.int64)
    print(f"  C_rich={C}: #motions with k >= {C*A:.1f}: {len(sel)}, sum k^2 = {int((sel**2).sum())}, / N^(10/3) = {(sel**2).sum()/N**(10/3):.4f}")
