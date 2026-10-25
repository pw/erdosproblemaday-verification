# Independent control for enum_types.py: brute-force count isomorphism classes of
# L4-free tournaments on n<=6 and (I3,L3)-free oriented graphs on n<=5 by exhaustive enumeration.
import itertools, json
def classes(n, states, ok):
    P = list(itertools.combinations(range(n), 2)); perms = list(itertools.permutations(range(n)))
    seen = set(); cnt = 0
    for assign in itertools.product(states, repeat=len(P)):
        st = dict(zip(P, assign))
        if not ok(st, n): continue
        k = None
        for p in perms:
            out = {}
            for (u, v), s in st.items():
                a, b = p[u], p[v]
                if a < b: out[(a, b)] = s
                else: out[(b, a)] = 0 if s == 0 else (3 - s)
            kk = tuple(out[q] for q in P)
            if k is None or kk < k: k = kk
        if k not in seen: seen.add(k); cnt += 1
    return cnt
def arc(st, u, v):
    if u < v: return st[(u, v)] == 1
    return st[(v, u)] == 2
def tt4free(st, n):
    for S in itertools.combinations(range(n), 4):
        for o in itertools.permutations(S):
            if all(arc(st, o[i], o[j]) for i in range(4) for j in range(i+1, 4)): return False
    return True
def i3l3free(st, n):
    for a, b, c in itertools.combinations(range(n), 3):
        if st[(a, b)] == 0 and st[(a, c)] == 0 and st[(b, c)] == 0: return False
        for o in itertools.permutations((a, b, c)):
            if arc(st, o[0], o[1]) and arc(st, o[0], o[2]) and arc(st, o[1], o[2]): return False
    return True
T = json.load(open("types.json"))
for n in (3, 4, 5, 6):
    c = classes(n, (1, 2), tt4free); print(f"T n={n}: brute {c} vs sat {len(T['T'][str(n)])}", "OK" if c == len(T['T'][str(n)]) else "MISMATCH")
for n in (3, 4, 5):
    c = classes(n, (0, 1, 2), i3l3free); print(f"N n={n}: brute {c} vs sat {len(T['N'][str(n)])}", "OK" if c == len(T['N'][str(n)]) else "MISMATCH")
