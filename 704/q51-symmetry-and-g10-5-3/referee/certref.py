# Referee: re-verify cert_X9 / cert_Y121 and that the 1600 rows are copies of W (structural reconstruction, own code).
import numpy as np, re
from itertools import combinations
V = [frozenset(c) for c in combinations(range(13), 5)]
M = np.load('../copies_rows.npy')[:1600].astype(np.int64)
assert M.shape == (1600, 1287) and set(np.unique(M)) <= {0, 1}
def build(inf, a, b, S12, S13, S23):
    B = [{a[0], b[0]} | S12 | S13, {a[1], b[1]} | S12 | S23, {a[2], b[2]} | S13 | S23]
    out = set()
    for Bk in B: out |= {frozenset(Bk - {x}) for x in Bk}
    out |= {frozenset({inf, *a, s}) for s in S12 | S13 | S23}
    out |= {frozenset({inf, *b, y}) for y in range(13) if y not in {inf, *b}}
    return out
def is_copy(F):
    deg = [sum(1 for s in F if x in s) for x in range(13)]
    if sorted(deg) != [12]*9 + [14]*3 + [15]: return False
    inf = deg.index(15); b = [x for x in range(13) if deg[x] == 14]
    c6 = [s for s in F if inf in s and not set(b) <= s]
    if len(c6) != 6: return False
    core = frozenset.intersection(*c6)
    if len(core) != 4: return False
    a = sorted(core - {inf}); rest = [s for s in F if inf not in s]
    blocks = []
    for ai in a:
        U = frozenset().union(*[s for s in rest if ai in s]); blocks.append(U)
    if any(len(Bk) != 6 for Bk in blocks): return False
    bb = []
    for Bk in blocks:
        t = [x for x in b if x in Bk]
        if len(t) != 1: return False
        bb.append(t[0])
    S12, S13, S23 = blocks[0] & blocks[1], blocks[0] & blocks[2], blocks[1] & blocks[2]
    if not all(len(S) == 2 for S in (S12, S13, S23)): return False
    return build(inf, a, bb, set(S12), set(S13), set(S23)) == F
rows_ok = all(is_copy({V[c] for c in range(1287) if M[r, c]}) for r in range(1600))
# negative control: a non-copy (swap one set) must fail
F0 = {V[c] for c in range(1287) if M[0, c]}; s0 = next(iter(F0)); t0 = next(x for x in V if x not in F0)
print('all 1600 rows are copies of W:', rows_ok, '| control (one set swapped) rejected:', not is_copy((F0 - {s0}) | {t0}))
def load(fn): return np.array([int(t) for t in re.findall(r'-?\d+', open(fn).read())], dtype=object)
X, Y = load('../cert_X9.txt'), load('../cert_Y121.txt'); assert len(X) == len(Y) == 1600
Mo = M.astype(object)
tx = X.dot(Mo); ty = Y.dot(Mo)
e = np.zeros(1287, dtype=object); e[0] = 1
print('S = coordinate 0 =', sorted(V[0]))
print('sum X_i C_i == 3 e_S mod 9:', all(((tx - 3*e) % 9) == 0), '| sum Y_i C_i == 11 e_S mod 121:', all(((ty - 11*e) % 121) == 0))
print('controls: X gives e_S mod 9?', all(((tx - e) % 9) == 0), '| X gives 3e_S mod 27?', all(((tx - 3*e) % 27) == 0))
