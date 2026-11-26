"""Referee B: Section 5 checks.
(1) Remark 5.2 6+6 example has S_{2,2}; the n=1 4-cycle has S_{1,1}.
(2) Brute force: no S_{1,1} with |A|+|B|<=3 (|A|,|B|>=1); no S_{2,2} with |A|+|B|<=11 (|A|,|B|>=2).
(3) Lemma 5.1 stress test on random bipartite tournaments (LP game value) + a mutation control.
(4) The degenerate literal-definition counterexample to Theorem 1.5 (|A|=n, |B|=1)."""
import sys, random, itertools
import numpy as np
from scipy.optimize import linprog

def has_S(K, m, beats, n):
    """beats[b] = bitmask of a in A with b -> a (b in B). a -> b otherwise.
    S_{n,n}: every n-subset of A has b with b->all; every n-subset of B has a with a->all."""
    fullA = (1 << K) - 1
    for Y in itertools.combinations(range(K), n):
        y = sum(1 << i for i in Y)
        if not any(beats[b] & y == y for b in range(m)):
            return False
    for Z in itertools.combinations(range(m), n):
        # a dominates Z iff a not in beats[b] for all b in Z
        u = 0
        for b in Z:
            u |= beats[b]
        if u == fullA:
            return False
    return True


def game_value(K, m, beats):
    # payoff to B: P[b][a] = 1 if b->a. B maximizes. LP: max v s.t. sum_b x_b P[b][a] >= v for all a.
    P = np.array([[1.0 if (beats[b] >> a) & 1 else 0.0 for a in range(K)] for b in range(m)])
    c = np.zeros(m + 1); c[-1] = -1
    A_ub = np.hstack([-P.T, np.ones((K, 1))])
    b_ub = np.zeros(K)
    A_eq = np.hstack([np.ones((1, m)), np.zeros((1, 1))])
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=[1.0], bounds=[(0, None)] * m + [(None, None)], method='highs')
    return -res.fun

def nus(K, m, beats):
    nA = []
    for s in range(K + 1):
        best = m
        for Y in itertools.combinations(range(K), s):
            y = sum(1 << i for i in Y)
            c = sum(1 for b in range(m) if beats[b] & y == y)
            best = min(best, c)
        nA.append(best)
    fullA = (1 << K) - 1
    nB = []
    for s in range(m + 1):
        best = K
        for Z in itertools.combinations(range(m), s):
            u = 0
            for b in Z:
                u |= beats[b]
            best = min(best, K - bin(u).count('1'))
        nB.append(best)
    return nA, nB

