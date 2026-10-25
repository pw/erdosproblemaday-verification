# Seat I: random finite-law checks of the information identities used in Prop 7.1 (printed §7):
#  (I1) I(X;P|O) <= sum_a I(X;P_a|O) when P_1..P_m are i.i.d. given (O,X)       [transport step]
#  (I2) I(A;B|C,S) - I(A;B|C) = I(A;S|B,C) - I(A;S|C) <= H(S)                   [eq. before (7.9)]
#  (I3) (7.9): I(X; s,W | O) <= I(X'; W | O') + 2H(s) with X'=X+s, O'=O+s mod p  [bijection given s]
# Negative control for (I1): with P_a NOT conditionally independent the inequality can fail.
import itertools, math, random
import numpy as np

rng = np.random.default_rng(12345)

def H(p):
    p = p[p > 0]; return float(-(p*np.log(p)).sum())

def marg(J, keep):
    axes = tuple(i for i in range(J.ndim) if i not in keep)
    return J.sum(axis=axes) if axes else J

def Hs(J, idx):
    return H(marg(J, tuple(sorted(idx))).ravel())

def I(J, A, B, C=()):
    A, B, C = set(A), set(B), set(C)
    return Hs(J, A|C) + Hs(J, B|C) - Hs(J, A|B|C) - (Hs(J, C) if C else 0.0)

worst1 = -1e9; worst2 = -1e9; worst3 = -1e9; ctrl_fail = 0
for trial in range(300):
    nO, nX, nP, m = 2, 3, 3, 3
    pOX = rng.dirichlet(np.ones(nO*nX)).reshape(nO, nX)
    K = rng.dirichlet(np.ones(nP), size=(nO, nX))      # package law given (O,X)
    J = np.zeros((nO, nX) + (nP,)*m)
    for o, x in itertools.product(range(nO), range(nX)):
        for ps in itertools.product(range(nP), repeat=m):
            J[(o, x)+ps] = pOX[o, x]*np.prod([K[o, x, q] for q in ps])
    lhs = I(J, [1], range(2, 2+m), [0])
    rhs = sum(I(J, [1], [2+a], [0]) for a in range(m))
    worst1 = max(worst1, lhs - rhs)
    # negative control: packages identical copies (not cond. independent) -> lhs = I(X;P1|O), rhs = m*I
    # (that one still satisfies it); use instead P2 = f(X, P1) dependent coupling: lhs can exceed rhs
    J2 = np.zeros((nO, nX, nP, nP))
    for o, x, p1 in itertools.product(range(nO), range(nX), range(nP)):
        # P1 independent of X given O; P2 = (P1 + x) mod nP  => individually uninformative-ish, jointly informative
        pass
    # (I2) on random 4-variable law
    J4 = rng.dirichlet(np.ones(2*3*2*3)).reshape(2, 3, 2, 3)   # A,B,C,S
    d = I(J4, [0], [1], [2, 3]) - I(J4, [0], [1], [2])
    e = I(J4, [0], [3], [1, 2]) - I(J4, [0], [3], [2])
    worst2 = max(worst2, abs(d - e), d - Hs(J4, [3]))
    # (I3): X,O residues mod p=5, s in Z_5 (stand-in for residue of displacement), W word symbol
    p = 5
    J5 = rng.dirichlet(np.ones(p*p*p*3)).reshape(p, p, p, 3)   # O, X, s, W
    lhs3 = I(J5, [1], [2, 3], [0])
    Jp = np.zeros_like(J5)                                    # law of (O', X', s, W)
    for o, x, s, w in itertools.product(range(p), range(p), range(p), range(3)):
        Jp[(o+s) % p, (x+s) % p, s, w] += J5[o, x, s, w]
    rhs3 = I(Jp, [1], [3], [0]) + 2*Hs(J5, [2])
    worst3 = max(worst3, lhs3 - rhs3)

# explicit negative control for (I1): X uniform bit, P1 uniform bit indep of X, P2 = P1 xor X.
J = np.zeros((1, 2, 2, 2))
for x, p1 in itertools.product(range(2), range(2)):
    J[0, x, p1, p1 ^ x] = 0.25
ctrl_lhs = I(J, [1], [2, 3], [0]); ctrl_rhs = I(J, [1], [2], [0]) + I(J, [1], [3], [0])
print(f"(I1) max[I(X;P|O) - sum I(X;P_a|O)] over 300 random cond.-iid laws = {worst1:.2e} (<=0 expected)")
print(f"     negative control (P2 = P1 xor X, not cond. iid): lhs={ctrl_lhs:.4f} rhs={ctrl_rhs:.4f} -> "
      f"{'inequality FAILS as it should' if ctrl_lhs > ctrl_rhs + 1e-9 else 'did not fail'}")
print(f"(I2) max |identity defect| / max[(lhs) - H(S)] = {worst2:.2e} (<=~0 expected)")
print(f"(I3) max[I(X;s,W|O) - (I(X';W|O') + 2H(s))] = {worst3:.2e} (<=0 expected)")
