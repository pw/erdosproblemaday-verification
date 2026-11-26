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

# (1) Remark 5.2: b_j -> a_i iff j-th entry of i-th word is 1
words = ['111000', '110100', '100011', '010011', '001110', '001101']
beats = [sum(1 << i for i in range(6) if words[i][j] == '1') for j in range(6)]
print('Remark 5.2 example (6+6) has S_{2,2}:', has_S(6, 6, beats, 2))
# n=1: a1->b1->a2->b2->a1 ; A={a1,a2} (bits 0,1), B={b1,b2}: b1 beats a2, b2 beats a1
print('n=1 4-cycle has S_{1,1}:', has_S(2, 2, [1 << 1, 1 << 0], 1))

# (2) brute force (families of subsets S_b of A, multiset since b's are distinct vertices but sets may repeat)
def exists(n, total, Kmin):
    found = []
    for K in range(Kmin, total + 1):
        for m in range(max(Kmin, K), total - K + 1):  # WLOG K <= m (swap symmetry)
            for fam in itertools.combinations_with_replacement(range(1 << K), m):
                if has_S(K, m, list(fam), n):
                    found.append((K, m, fam))
                    return found
    return found
print('S_{1,1} with |A|,|B|>=1 and |A|+|B|<=3 exists?', bool(exists(1, 3, 1)))
cnt_checked = 0
ex = []
for K in range(2, 6):
    for m in range(K, 12 - K):
        for fam in itertools.combinations_with_replacement(range(1 << K), m):
            cnt_checked += 1
            if has_S(K, m, list(fam), 2):
                ex.append((K, m, fam)); break
print(f'S_{{2,2}} with 2<=|A|<=|B|, |A|+|B|<=11: {cnt_checked} families checked, examples found: {ex[:1]}')
# swap symmetry check on the 6+6 example (transpose roles)
beatsT = [sum(1 << j for j in range(6) if words[i][j] == '0') for i in range(6)]  # a_i -> b_j iff entry 0
print('6+6 example with sides swapped also S_{2,2} (symmetry sanity):', has_S(6, 6, beatsT, 2))

# (3) Lemma 5.1 stress test
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

random.seed(902)
viol = 0; mut = 0; trials = 0; tightA = 0
for t in range(3000):
    K = random.randint(1, 8); m = random.randint(1, 8)
    pr = random.choice([0.2, 0.35, 0.5, 0.65, 0.8])
    beats = [sum(1 << a for a in range(K) if random.random() < pr) for b in range(m)]
    v = game_value(K, m, beats)
    nA, nB = nus(K, m, beats)
    trials += 1
    for s in range(K):
        if nA[s + 1] > v * nA[s] + 1e-9: viol += 1
        if nA[s + 1] > v * v * nA[s] + 1e-9: mut += 1
        if abs(nA[s + 1] - v * nA[s]) < 1e-9 and nA[s] > 0: tightA += 1
    for s in range(m):
        if nB[s + 1] > (1 - v) * nB[s] + 1e-9: viol += 1
        if nB[s + 1] > (1 - v) ** 2 * nB[s] + 1e-9: mut += 1
print(f'Lemma 5.1 stress: {trials} random bipartite tournaments (K,m<=8): violations={viol}; '
      f'equality cases (A side)={tightA}; CONTROL (v^2 in place of v) violations={mut} (must be >0)')
# value of the Remark 5.2 example and its nu's
v = game_value(6, 6, beats); nA, nB = nus(6, 6, beats)
print(f'Remark 5.2 example: v={v:.6f}, nu^A={nA}, nu^B={nB}; '
      f'Lemma 5.1 A-side ok: {all(nA[s+1] <= v*nA[s]+1e-9 for s in range(6))}, B-side ok: {all(nB[s+1] <= (1-v)*nB[s]+1e-9 for s in range(6))}')

# (4) literal definition: |A|=n, |B|=1, b beats all of A
for n in range(2, 6):
    print(f'n={n}: |A|=n,|B|=1 (b->all A) satisfies the literal S_{{n,n}}: {has_S(n, 1, [(1 << n) - 1], n)}  '
          f'(order {n+1} < (n+1)2^n = {(n+1)*2**n}); |A|=|B|=1 vacuous: {has_S(1, 1, [1], n)}')
