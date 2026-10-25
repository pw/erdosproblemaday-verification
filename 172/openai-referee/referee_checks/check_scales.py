# Check (8.1)-(8.2): lambda_e > 0 for every pair at the pivot, and b'_{B0} = b_{B0};
# check Lemma 3.3 sign claim for e_j = 2^{N-j}; check Lemma 2.5 chain construction.
import itertools, random
from fractions import Fraction

def subsets(xs):
    for r in range(1, len(xs)+1):
        for c in itertools.combinations(xs, r):
            yield c

def blocks(n):
    for i in range(1, n+1):
        for T in subsets(range(1, i)):
            yield (T, i)

def EB(T, i):
    # E_B = {P u {j} : P nonempty < T < j < i}
    out = []
    for j in range(max(T)+1, i):
        for P in subsets(range(1, min(T))):
            out.append((P, j))
    return out

def check_82(n):
    p = {l: 2**(n-l) for l in range(1, n+1)}
    bad = 0; npairs = 0
    for i in range(1, n+1):
        targets = [(T, ii) for (T, ii) in blocks(n) if ii == i and EB(T, i)]
        for (T0, _) in targets:
            # exponent of k in kappa_l
            kap = {l: (p[l] if l < i else (-sum(p[t] for t in T0) if l == i else 0)) for l in range(1, n+1)}
            # leading index unchanged
            assert sum(kap[l] for l in T0) + kap[i] == 0
            for (C, _) in targets:
                U = set(C) | {i}
                for (P, j) in EB(C, i):
                    A = set(P) | {j}
                    lam = sum(kap[l] for l in A) - sum(kap[l] for l in U)
                    lam_formula = sum(p[l] for l in A) - sum(p[l] for l in C) + sum(p[l] for l in T0)
                    assert lam == lam_formula
                    npairs += 1
                    if lam <= 0: bad += 1
    return npairs, bad

for n in range(4, 10):
    print("n=%d pairs-checked=%d nonpositive-lambda=%d" % ((n,) + check_82(n)))

def check_33(N):
    e = {j: 2**(N-j) for j in range(1, N+1)}
    bad = 0; cnt = 0
    for (T, i) in blocks(N):
        for (P, j) in EB(T, i):
            A = set(P) | {j}; B = set(T) | {i}
            cnt += 1
            if sum(e[x] for x in A) - sum(e[x] for x in B) <= 0: bad += 1
    return cnt, bad
for N in range(4, 11):
    print("Lemma3.3 N=%d adding-pairs=%d bad=%d" % ((N,) + check_33(N)))

# chain condition: build chains as in Lemma 2.5 from random q_d >= 2
def chain_from_q(qs):
    m = len(qs); idx = iter(range(1, 10**6)); tails = []
    for q in qs:
        tails.append(tuple(next(idx) for _ in range(q-1)))
    piv = [next(idx) for _ in range(m)]
    return [(tails[d], piv[d]) for d in range(m)]
random.seed(1)
for trial in range(2000):
    m = random.randint(2, 5)
    qs = [2*random.randint(1, 4) for _ in range(m)]
    ch = chain_from_q(qs)
    for d in range(m):
        Td, id_ = ch[d]
        Ed = set((tuple(P), j) for (P, j) in EB(Td, id_)) if Td else set()
        for k in range(d):
            Tk, ik = ch[k]
            assert (tuple(Tk), ik) in Ed, (ch, k, d)
    # union sizes
    for J in subsets(range(m)):
        assert sum(len(ch[d][0]) + 1 for d in J) == sum(qs[d] for d in J)
print("Lemma 2.5 chain construction: 2000 random chains satisfy B_k in E_{B_d} for k<d and size additivity")

# Lemma 3.3 also: chained blocks k<d: ratio c_k/c_d in W^w N  <=> sum e over B_k > sum e over B_d
def check_chain_e(N, trials=500):
    e = {j: 2**(N-j) for j in range(1, N+1)}
    for _ in range(trials):
        m = random.randint(2, 3); qs = [2*random.randint(1, 2) for _ in range(m)]
        ch = chain_from_q(qs)
        if max(ch[-1][1], 0) > N: continue
        for k in range(m):
            for d in range(k+1, m):
                Bk = set(ch[k][0]) | {ch[k][1]}; Bd = set(ch[d][0]) | {ch[d][1]}
                assert sum(e[x] for x in Bk) > sum(e[x] for x in Bd)
    return True
print("chain e-sign:", check_chain_e(14))
