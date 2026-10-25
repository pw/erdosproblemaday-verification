# (e) Lemma 2.5: equal Gram matrices (u_i.u_j = w_i.w_j) => u_i -> w_i extends to S in O(d)
import numpy as np
rng = np.random.default_rng(2025)
d = 3
def random_O(d, det=None):
    Q, R = np.linalg.qr(rng.normal(size=(d, d))); Q = Q @ np.diag(np.sign(np.diag(R)))
    if det is not None and np.sign(np.linalg.det(Q)) != det: Q[:, 0] *= -1
    return Q
def extend_isometry(U, W, tol=1e-9):
    """U, W: d x k with U^T U == W^T W. Build S in O(d) with S U = W (via orthonormal bases of spans)."""
    G = U.T @ U
    assert np.allclose(G, W.T @ W, atol=1e-9)
    # well-definedness: kernel of U equals kernel of W
    nU = np.linalg.svd(U)[2]; r = np.linalg.matrix_rank(U, tol)
    ker = nU[r:].T                       # k x (k-r)
    welldef = np.abs(W @ ker).max() if ker.size else 0.0
    # orthonormal basis of span(U) and corresponding images
    Uu, s, Vt = np.linalg.svd(U, full_matrices=True)
    E = Uu[:, :r]                          # orthonormal basis of span U
    # E = U V_r diag(1/s); image F = W V_r diag(1/s)
    F = W @ Vt[:r].T @ np.diag(1/s[:r])
    orthoF = np.abs(F.T @ F - np.eye(r)).max()
    # complete both to orthonormal bases of R^d
    def complete(X):
        Qf, _ = np.linalg.qr(np.hstack([X, rng.normal(size=(d, d-X.shape[1]))]))
        Qf[:, :X.shape[1]] = X
        # re-orthonormalise the completion against X
        for j in range(X.shape[1], d):
            v = Qf[:, j] - Qf[:, :j] @ (Qf[:, :j].T @ Qf[:, j]); Qf[:, j] = v/np.linalg.norm(v)
        return Qf
    Ef, Ff = complete(E), complete(F)
    S = Ff @ Ef.T
    return S, welldef, orthoF
cases = []
for k in (1, 2, 3, 4, 5):
    U = rng.normal(size=(d, k)); cases.append((f"generic k={k}", U))
U = rng.normal(size=(d, 2)); cases.append(("dependent: u3=u1+2u2", np.column_stack([U, U[:, 0]+2*U[:, 1]])))
u1 = rng.normal(size=d); cases.append(("collinear: u2=-1.5u1, u3=3u1", np.column_stack([u1, -1.5*u1, 3*u1])))
U = rng.normal(size=(d, 2)); cases.append(("planar 4 vectors", np.column_stack([U, U @ rng.normal(size=(2, 2))])))
for name, U in cases:
    for det in (+1, -1):
        S0 = random_O(d, det)
        W = S0 @ U
        S, wd, oF = extend_isometry(U, W)
        print(f"{name:32s} det(S0)={det:+d}: kernel-preserved err {wd:.1e}, image basis orthonormal err {oF:.1e}, |S U - W| = {np.abs(S@U-W).max():.1e}, |S^T S - I| = {np.abs(S.T@S-np.eye(d)).max():.1e}, det S = {np.linalg.det(S):+.3f}")
# Gram-equal pairs NOT produced from an S0: construct W from the Gram matrix directly (Cholesky-type), check extension still exists
for k in (2, 3):
    U = rng.normal(size=(d, k)); G = U.T @ U
    L = np.linalg.cholesky(G)                       # G = L L^T, L k x k
    W = np.zeros((d, k)); W[:k, :] = L.T
    S, wd, oF = extend_isometry(U, W)
    print(f"Gram-built W, k={k}: |S U - W| = {np.abs(S@U-W).max():.1e}, |S^T S - I| = {np.abs(S.T@S-np.eye(d)).max():.1e}")
# negative control: unequal Gram => no isometry (assert fires)
U = rng.normal(size=(d, 2)); W = U.copy(); W[:, 1] *= 1.01
try:
    extend_isometry(U, W); print("NEGATIVE CONTROL FAILED")
except AssertionError:
    print("negative control: unequal Gram matrices correctly rejected")
# matches: x -> q + S(x - p) maps p -> q and p+u_i -> q+w_i
p, q = rng.normal(size=d), rng.normal(size=d); U = rng.normal(size=(d, 3)); S0 = random_O(d, -1); W = S0 @ U
S, _, _ = extend_isometry(U, W)
print("match check: max |q + S((p+u_i)-p) - (q+w_i)| =", np.abs((q[:, None] + S @ U) - (q[:, None] + W)).max())
