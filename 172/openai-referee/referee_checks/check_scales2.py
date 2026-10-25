import itertools, random
def subsets(xs):
    for r in range(1, len(xs)+1):
        yield from itertools.combinations(xs, r)
def in_EB(A, B):
    # A = P u {j}, B = T u {i}: nonempty P < T < j < i
    T, i = B; P, j = A
    return len(P) > 0 and len(T) > 0 and max(P) < min(T) and max(T) < j < i
def pairs_at(n, i):
    out = []
    for T in subsets(range(1, i)):
        for j in range(max(T)+1, i):
            for P in subsets(range(1, min(T))):
                out.append((T, (P, j)))
    return out
def check_82(n):
    p = {l: 2**(n-l) for l in range(1, n+1)}
    bad = npairs = 0
    for i in range(1, n+1):
        prs = pairs_at(n, i)
        targets = sorted(set(T for T, _ in prs))
        for T0 in targets:
            kap = {l: (p[l] if l < i else (-sum(p[t] for t in T0) if l == i else 0)) for l in range(1, n+1)}
            assert sum(kap[l] for l in T0) + kap[i] == 0          # b'_{B0} = b_{B0}
            for C, (P, j) in prs:
                lam = sum(kap[l] for l in P) + kap[j] - sum(kap[l] for l in C) - kap[i]
                assert lam == sum(p[l] for l in P) + p[j] - sum(p[l] for l in C) + sum(p[l] for l in T0)
                npairs += 1; bad += (lam <= 0)
    return npairs, bad
for n in range(4, 10):
    print("(8.2) n=%d (target,pair) checks=%d nonpositive-lambda=%d" % ((n,) + check_82(n)), flush=True)
def check_33(N):
    e = {j: 2**(N-j) for j in range(1, N+1)}
    cnt = bad = 0
    for i in range(1, N+1):
        for T, (P, j) in pairs_at(N, i):
            cnt += 1
            bad += (sum(e[x] for x in P) + e[j] - sum(e[x] for x in T) - e[i] <= 0)
    return cnt, bad
for N in range(4, 11):
    print("Lemma 3.3 N=%d adding pairs=%d bad=%d" % ((N,) + check_33(N)), flush=True)
random.seed(1)
def chain_from_q(qs):
    idx = iter(range(1, 10**6)); tails = [tuple(next(idx) for _ in range(q-1)) for q in qs]
    piv = [next(idx) for _ in qs]
    return [(tails[d], piv[d]) for d in range(len(qs))]
for trial in range(5000):
    m = random.randint(2, 6); qs = [2*random.randint(1, 5) for _ in range(m)]
    ch = chain_from_q(qs)
    for d in range(m):
        for k in range(d):
            assert in_EB(ch[k], ch[d])
    N = ch[-1][1]; e = {j: 2**(N-j) for j in range(1, N+1)}
    for k in range(m):
        for d in range(k+1, m):
            Bk = set(ch[k][0]) | {ch[k][1]}; Bd = set(ch[d][0]) | {ch[d][1]}
            assert sum(e[x] for x in Bk) > sum(e[x] for x in Bd)   # c_k/c_d in W^w N
print("Lemma 2.5 / Lemma 3.3 chain checks: 5000 random chains OK", flush=True)
