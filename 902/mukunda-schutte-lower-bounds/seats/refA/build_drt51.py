"""Build doubly regular tournaments on 51 vertices from scratch:
good matrices of order 13 (A skew-type, B,C,D symmetric circulant +-1)
-> Goethals-Seidel skew-Hadamard matrix of order 52 -> normalise -> core = DRT(51).
Writes several distinct ones to refA/own_drt51_<i>.npy (int8 adjacency).
No repository code is used.
"""
import itertools, sys
import numpy as np

m = 13
h = (m - 1) // 2  # 6


def circ(row):
    row = np.array(row)
    return np.array([np.roll(row, i) for i in range(len(row))])


def paf(row):
    row = np.array(row)
    return tuple(int(np.dot(row, np.roll(row, -s))) for s in range(1, h + 1))


skews = []
for bits in itertools.product([1, -1], repeat=h):
    r = [1] + list(bits) + [-bits[h - 1 - i] for i in range(h)]
    # r[j] = -r[m-j] for j=1..h
    assert all(r[j] == -r[m - j] for j in range(1, m))
    skews.append(r)
syms = []
for b0 in [1, -1]:
    for bits in itertools.product([1, -1], repeat=h):
        r = [b0] + list(bits) + [bits[h - 1 - i] for i in range(h)]
        assert all(r[j] == r[m - j] for j in range(1, m))
        syms.append(r)

pafS = [paf(r) for r in skews]
pafY = [paf(r) for r in syms]
cd = {}
for ic, c in enumerate(syms):
    for id_, d in enumerate(syms):
        key = tuple(x + y for x, y in zip(pafY[ic], pafY[id_]))
        cd.setdefault(key, []).append((ic, id_))
sols = []
for ia in range(len(skews)):
    for ib in range(len(syms)):
        need = tuple(-(x + y) for x, y in zip(pafS[ia], pafY[ib]))
        for ic, id_ in cd.get(need, []):
            sols.append((ia, ib, ic, id_))
print("good-matrix quadruples found:", len(sols))

R = np.array([[1 if (i + j) % m == m - 1 else 0 for j in range(m)] for i in range(m)])


def gs(a, b, c, d):
    A, B, C, D = circ(a), circ(b), circ(c), circ(d)
    H = np.block([
        [A, B @ R, C @ R, D @ R],
        [-B @ R, A, D.T @ R, -C.T @ R],
        [-C @ R, -D.T @ R, A, B.T @ R],
        [-D @ R, C.T @ R, -B.T @ R, A]])
    return H


def to_drt(H):
    n = H.shape[0]
    assert np.array_equal(H @ H.T, n * np.eye(n, dtype=int)), "not Hadamard"
    assert np.array_equal(H + H.T, 2 * np.eye(n, dtype=int)), "not skew"
    # normalise first row to all +1 by D H D with D=diag(d), d_0=1, d_j=H[0,j]
    dvec = np.array([1] + [H[0, j] for j in range(1, n)])
    Hn = (dvec[:, None] * H) * dvec[None, :]
    assert np.all(Hn[0, 1:] == 1)
    assert np.array_equal(Hn + Hn.T, 2 * np.eye(n, dtype=int))
    S = Hn[1:, 1:] - np.eye(n - 1, dtype=int)
    Adj = (S == 1).astype(np.int8)
    np.fill_diagonal(Adj, 0)
    return Adj


def canon_invariant(Adj):
    # cheap invariant for de-duplication: sorted triple-dominator distribution
    n = Adj.shape[0]
    inm = [sum(1 << w for w in range(n) if Adj[w, v]) for v in range(n)]
    hist = {}
    for i, j, k in itertools.combinations(range(n), 3):
        c = bin(inm[i] & inm[j] & inm[k]).count('1')
        hist[c] = hist.get(c, 0) + 1
    return tuple(sorted(hist.items()))


seen = {}
out = 0
for (ia, ib, ic, id_) in sols:
    H = gs(skews[ia], syms[ib], syms[ic], syms[id_])
    Adj = to_drt(H)
    inv = canon_invariant(Adj)
    if inv in seen:
        continue
    seen[inv] = (ia, ib, ic, id_)
    np.save(f"/home/exedev/MathDyad/subs-1126/902/refA/own_drt51_{out}.npy", Adj)
    print(f"saved own_drt51_{out}.npy from rows a={skews[ia]} b={syms[ib]} c={syms[ic]} d={syms[id_]}")
    print("   triple-dominator histogram:", inv)
    out += 1
    if out >= 4:
        break
print("distinct (by histogram) DRT(51) saved:", out)
