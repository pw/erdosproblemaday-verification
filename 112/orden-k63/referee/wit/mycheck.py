"""Seat O's own witness checker: bitmask based. Usage: mycheck.py file k"""
import sys, itertools, hashlib

def parse(path):
    out = {}
    for line in open(path):
        line = line.strip()
        if not line or line.startswith('#'): continue
        v, rest = line.split(':', 1)
        out[int(v)] = [int(t) for t in rest.split()]
    return out

def analyse(out, k, label):
    n = len(out)
    assert sorted(out) == list(range(n)), "vertex labels not 0..n-1"
    arcs = [(v, w) for v in out for w in out[v]]
    dup = len(arcs) - len(set(arcs))
    loops = sum(1 for v, w in arcs if v == w)
    rng = sum(1 for v, w in arcs if not (0 <= w < n))
    A = set(arcs)
    two = sum(1 for v, w in A if (w, v) in A) // 2
    OUT = [0] * n
    ADJ = [0] * n
    for v, w in A:
        OUT[v] |= 1 << w
        ADJ[v] |= 1 << w
        ADJ[w] |= 1 << v
    # transitive triangles x->y, y->z, x->z  <=> y in OUT[x], z in OUT[y] & OUT[x]
    tt = sum(bin(OUT[y] & OUT[x]).count('1') for x in range(n) for y in range(n) if OUT[x] >> y & 1)
    # independent k-sets: count all by recursion over non-neighbour bitsets
    NON = [((1 << n) - 1) & ~ADJ[v] & ~(1 << v) for v in range(n)]
    cnt = 0; first = None
    def rec(chosen, cand):
        nonlocal cnt, first
        if len(chosen) == k:
            cnt += 1
            if first is None: first = list(chosen)
            return
        c = cand
        while c:
            b = c & -c; v = b.bit_length() - 1; c ^= b
            # only higher-numbered vertices to avoid duplicates
            rec(chosen + [v], cand & NON[v] & ~((1 << (v + 1)) - 1))
    rec([], (1 << n) - 1)
    # brute-force cross-check of the count (different method) when cheap
    brute = None
    if n <= 30:
        brute = sum(1 for S in itertools.combinations(range(n), k)
                    if all(not (ADJ[a] >> b & 1) for a, b in itertools.combinations(S, 2)))
    od = sorted(set(bin(OUT[v]).count('1') for v in range(n)))
    idg = sorted(set(sum(1 for u in range(n) if OUT[u] >> v & 1) for v in range(n)))
    ok = loops == 0 and two == 0 and dup == 0 and rng == 0 and tt == 0 and cnt == 0
    print(f"[{label}] n={n} arcs={len(A)} dup={dup} loops={loops} out_of_range={rng} 2cycles={two} "
          f"TT(ordered x->y->z,x->z)={tt} indep{k}-sets: rec={cnt} brute={brute} first={first} "
          f"outdeg={od} indeg={idg} -> {'PASS' if ok else 'FAIL'}")
    return ok

def circulant(n, S):
    return {x: sorted((x + s) % n for s in S) for x in range(n)}

if __name__ == '__main__':
    path = sys.argv[1]
    print("sha256", hashlib.sha256(open(path, 'rb').read()).hexdigest())
    W = parse(path)
    analyse(W, 6, "witness k=6")
    analyse(W, 5, "witness k=5 (expect FAIL: alpha must be >=5 since r(I5,L3)=23)")
    # positive control: Kirtchakov's circulant and its relabelled form
    C1 = circulant(28, [3, 8, 10, 12, 17]); analyse(C1, 6, "Cay(Z28,{3,8,10,12,17}) k=6 expect PASS")
    C2 = circulant(28, [1, 4, 12, 15, 22]); analyse(C2, 6, "Cay(Z28,{1,4,12,15,22}) k=6 expect PASS")
    # negative control: circulant + isolated vertex (29 vertices)
    C3 = dict(C1); C3[28] = []; analyse(C3, 6, "Z28 circulant + isolated vertex, expect FAIL (indep)")
    # negative control: add a chord making a transitive triangle
    W2 = {v: list(ws) for v, ws in W.items()}
    adj = lambda a, b: b in W[a] or a in W[b]
    done = False
    for x in W:
        for y in W[x]:
            for z in W[y]:
                if z != x and not adj(x, z):
                    W2[x].append(z); done = (x, y, z); break
            if done: break
        if done: break
    analyse(W2, 6, f"witness + arc {done[0]}->{done[2]} (path {done}), expect FAIL (TT)")
    # negative control: add a reverse arc -> 2-cycle
    W3 = {v: list(ws) for v, ws in W.items()}; W3[W[0][0]].append(0)
    analyse(W3, 6, f"witness + reverse arc {W[0][0]}->0, expect FAIL (2-cycle)")
    # mutation: delete each arc in turn, count how many deletions create an independent 6-set
    crit = 0; tot = 0
    for v in W:
        for w in W[v]:
            W4 = {a: [b for b in bs if not (a == v and b == w)] for a, bs in W.items()}
            tot += 1
            import io, contextlib
            with contextlib.redirect_stdout(io.StringIO()):
                ok = analyse(W4, 6, "del")
            crit += (not ok)
    print(f"arc-deletion mutations: {crit}/{tot} single-arc deletions create an independent 6-set (detected)")
