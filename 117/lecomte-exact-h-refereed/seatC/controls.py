"""controls.py -- every checker must accept a known-good object and reject a known-bad one.

1. witness checkers reject bad witnesses
2. exact clique (Python MCQ, C MCQ) vs networkx maximal-clique enumeration, random graphs
3. exact chi (DSATUR+SAT, cadical) vs independent brute force (plain backtracking), random graphs;
   named graphs with known (omega, chi)
4. twin reduction: census values (GAP export with twin reduction) == full noncentral-coset graph
   (GAP export without twin reduction) analysed by networkx + SAT with a DIFFERENT solver (glucose4)
   and no symmetry breaking, for all 586 groups of order <= 64
5. groups built independently in Python (no GAP): D8, Q8, S3, A4, S4, A5, D10, Heisenberg 3^{1+2},
   2^{1+4}+ = D8*D8, 2^{1+6}+, 3^{1+4} (F_9 trace model); omega, chi, z on the FULL element graph,
   compared against the census rows for the GAP ids.
"""
import random, itertools, sys, time
import networkx as nx
from pysat.solvers import Solver
from graphlib import (check_clique, check_colouring, max_clique, chromatic, dsatur, colour_sat,
                      c_clique, c_heurclique, c_dsatur, c_tabu, parse_rows)

FAILS = []


def ok(cond, msg):
    print(('PASS ' if cond else 'FAIL ') + msg)
    if not cond:
        FAILS.append(msg)


def nxg(n, adj):
    G = nx.Graph()
    G.add_nodes_from(range(n))
    for v in range(n):
        for u in range(v + 1, n):
            if (adj[v] >> u) & 1:
                G.add_edge(v, u)
    return G


def from_nx(G):
    nodes = list(G.nodes())
    idx = {v: i for i, v in enumerate(nodes)}
    n = len(nodes)
    adj = [0] * n
    for a, b in G.edges():
        adj[idx[a]] |= 1 << idx[b]
        adj[idx[b]] |= 1 << idx[a]
    return n, adj


def nx_omega(n, adj):
    """networkx's own branch-and-bound max clique (independent of graphlib/gtool)."""
    if n == 0:
        return 0
    C, wt = nx.max_weight_clique(nxg(n, adj), weight=None)
    assert check_clique(adj, C) and len(C) == wt
    return wt


def brute_chi(n, adj):
    """independent: plain backtracking, colours tried in order, no clique seeding."""
    if n == 0:
        return 0
    order = sorted(range(n), key=lambda v: -bin(adj[v]).count('1'))
    for k in range(1, n + 1):
        col = [-1] * n

        def bt(i):
            if i == n:
                return True
            v = order[i]
            used = set(col[u] for u in range(n) if (adj[v] >> u) & 1 and col[u] >= 0)
            mx = max(col) + 1
            for c in range(min(k, mx + 1)):
                if c not in used:
                    col[v] = c
                    if bt(i + 1):
                        return True
                    col[v] = -1
            return False
        if bt(0):
            return k


def sat_chi_plain(n, adj, lo, hi, solver='glucose4'):
    """chi by SAT with a different solver and NO symmetry breaking."""
    if n == 0:
        return 0
    k = hi
    while k > lo:
        kk = k - 1
        var = lambda v, c: v * kk + c + 1
        with Solver(name=solver) as s:
            for v in range(n):
                s.add_clause([var(v, c) for c in range(kk)])
            for v in range(n):
                for u in range(v + 1, n):
                    if (adj[v] >> u) & 1:
                        for c in range(kk):
                            s.add_clause([-var(v, c), -var(u, c)])
            if s.solve():
                m = set(l for l in s.get_model() if l > 0)
                col = [min(c for c in range(kk) if var(v, c) in m) for v in range(n)]
                assert check_colouring(n, adj, col)
                k = max(col) + 1
            else:
                return k
    return k


def section1():
    print('== 1. witness checkers reject bad witnesses')
    n, adj = 3, [0b110, 0b101, 0b011]   # K3
    ok(not check_colouring(n, adj, [0, 0, 1]), 'improper colouring of K3 rejected')
    ok(check_colouring(n, adj, [0, 1, 2]), 'proper colouring of K3 accepted')
    C5 = [0] * 5
    for i in range(5):
        C5[i] |= 1 << ((i + 1) % 5)
        C5[(i + 1) % 5] |= 1 << i
    ok(not check_clique(C5, [0, 2]), 'non-clique {0,2} in C5 rejected')
    ok(check_clique(C5, [0, 1]), 'edge {0,1} in C5 accepted as clique')
    ok(not check_clique(C5, [0, 0]), 'repeated vertex rejected')
    ok(not check_colouring(5, C5, [0, 1, 0, 1, 0]), 'improper 2-colouring of C5 rejected')


def section2(seed=11):
    print('== 2. exact clique vs networkx on random graphs')
    rnd = random.Random(seed)
    bad = 0
    cnt = 0
    for t in range(300):
        n = rnd.randint(5, 60)
        p = rnd.choice([0.1, 0.3, 0.5, 0.7, 0.85, 0.95])
        adj = [0] * n
        for v in range(n):
            for u in range(v + 1, n):
                if rnd.random() < p:
                    adj[v] |= 1 << u
                    adj[u] |= 1 << v
        w_nx = nx_omega(n, adj)
        w_py = len(max_clique(n, adj))
        Cc, proven = c_clique(n, adj, 30, 0)
        w_c = len(Cc) if Cc else 0
        h = len(c_heurclique(n, adj, 50, t))
        cnt += 1
        if not (w_nx == w_py == w_c and proven and h <= w_nx):
            bad += 1
            print('   mismatch', n, p, w_nx, w_py, w_c, proven, h)
        # lb semantics: asking for >= w+1 must return none, proven
        C2, pr2 = c_clique(n, adj, 30, w_nx + 1)
        if C2 is not None or not pr2:
            bad += 1
            print('   lb-semantics mismatch', n, p)
    ok(bad == 0, 'clique: python MCQ == C MCQ == networkx on %d random graphs; heuristic <= exact; lb=omega+1 proven empty' % cnt)


def mycielski(n, adj):
    # Mycielskian
    N = 2 * n + 1
    A = [0] * N
    for v in range(n):
        for u in range(n):
            if (adj[v] >> u) & 1:
                A[v] |= 1 << u
                A[v] |= 1 << (n + u)
                A[n + u] |= 1 << v
    for u in range(n):
        A[n + u] |= 1 << (2 * n)
        A[2 * n] |= 1 << (n + u)
    return N, A


def section3(seed=12):
    print('== 3. exact chi vs brute force; named graphs')
    rnd = random.Random(seed)
    bad = 0
    for t in range(150):
        n = rnd.randint(3, 12)
        p = rnd.choice([0.2, 0.4, 0.6, 0.8])
        adj = [0] * n
        for v in range(n):
            for u in range(v + 1, n):
                if rnd.random() < p:
                    adj[v] |= 1 << u
                    adj[u] |= 1 << v
        chi, col, src = chromatic(n, adj)
        b = brute_chi(n, adj)
        d = max(c_dsatur(n, adj)) + 1 if n else 0
        if chi != b or d < chi:
            bad += 1
            print('   mismatch', n, p, chi, b, d)
    ok(bad == 0, 'chi: DSATUR+SAT(cadical, clique-seeded) == brute-force backtracking on 150 random graphs; C DSATUR >= chi')
    named = []
    named.append(('C5', 5, [((1 << ((i + 1) % 5)) | (1 << ((i - 1) % 5))) for i in range(5)], 2, 3))
    P = nx.petersen_graph()
    named.append(('Petersen',) + from_nx(P) + (2, 3))
    n5, a5 = 5, [((1 << ((i + 1) % 5)) | (1 << ((i - 1) % 5))) for i in range(5)]
    gn, ga = mycielski(n5, a5)
    named.append(('Grotzsch', gn, ga, 2, 4))
    C7c = nx.complement(nx.cycle_graph(7))
    named.append(('complement(C7)',) + from_nx(C7c) + (3, 4))
    K6 = nx.complete_graph(6)
    named.append(('K6',) + from_nx(K6) + (6, 6))
    for name, n, adj, w, x in named:
        ww = len(max_clique(n, adj))
        xx = chromatic(n, adj)[0]
        ok(ww == w and xx == x, '%s: omega=%d (expect %d), chi=%d (expect %d)' % (name, ww, w, xx, x))
    # tabu control: finds a 3-colouring of Petersen, fails 2-colouring of C5
    n, adj = from_nx(P)
    ok(c_tabu(n, adj, 3, 20000, 1) is not None, 'tabucol finds 3-colouring of Petersen')
    ok(c_tabu(5, named[0][2], 2, 20000, 1) is None, 'tabucol reports FAIL for 2 colours on C5')
    ok(colour_sat(5, named[0][2], 2) is None, 'SAT reports UNSAT for 2 colours on C5')


def section4():
    print('== 4. twin reduction check: census (reduced) vs full coset graph, orders <= 64')
    census = {}
    for line in open('census/census_le255.tsv'):
        if line.startswith('n\t'):
            continue
        f = line.rstrip('\n').split('\t')
        census[(int(f[0]), int(f[1]))] = (int(f[2]), int(f[4]), int(f[5]))
    bad = 0
    cnt = 0
    t0 = time.time()
    for line in open('census/exportFULL_le64.txt'):
        body = line.split('#')[0].split()
        n, i, z, k = map(int, body[:4])
        rows = body[4:]
        if k == 0:
            w, a = 1, 1
        else:
            kk, adj = parse_rows(rows)
            assert kk == z - 1, 'full export should have z-1 vertices'
            w = nx_omega(kk, adj)
            d = max(dsatur(kk, adj)) + 1
            a = sat_chi_plain(kk, adj, w, d)
        cnt += 1
        if census[(n, i)] != (z, w, a):
            bad += 1
            print('   mismatch', (n, i), census[(n, i)], (z, w, a))
    ok(bad == 0 and cnt == 586, 'twin-reduced census == full-graph (networkx omega, glucose4 chi, no symmetry breaking) on all %d groups of order <= 64 (%.1fs)' % (cnt, time.time() - t0))


# ---------------- groups built without GAP ----------------
def perm_mul(p, q):  # apply p then q
    return tuple(q[p[i]] for i in range(len(p)))


def closure(gens):
    idt = tuple(range(len(gens[0])))
    S = {idt}
    frontier = [idt]
    while frontier:
        nf = []
        for x in frontier:
            for g in gens:
                y = perm_mul(x, g)
                if y not in S:
                    S.add(y)
                    nf.append(y)
        frontier = nf
    return sorted(S)


def element_graph(elems, mul):
    """full noncommuting graph on noncentral elements; returns (z, n, adj)."""
    N = len(elems)
    comm = [[mul(a, b) == mul(b, a) for b in elems] for a in elems]
    centre = [i for i in range(N) if all(comm[i])]
    nonc = [i for i in range(N) if not all(comm[i])]
    idx = {v: j for j, v in enumerate(nonc)}
    n = len(nonc)
    adj = [0] * n
    for a in nonc:
        for b in nonc:
            if not comm[a][b]:
                adj[idx[a]] |= 1 << idx[b]
    assert N % len(centre) == 0
    return N // len(centre), n, adj


def heis_group(p, d, B):
    """elements (v, c), v in F_p^d (tuple), c in F_p; (v,c)(w,e) = (v+w, c+e+B(v,w))."""
    elems = [(v, c) for v in itertools.product(range(p), repeat=d) for c in range(p)]

    def mul(x, y):
        v, c = x
        w, e = y
        return (tuple((a + b) % p for a, b in zip(v, w)), (c + e + B(v, w)) % p)
    return elems, mul


def section5():
    print('== 5. groups built in Python (no GAP), full element graph vs census')
    census = {}
    for line in open('census/census_le255.tsv'):
        if line.startswith('n\t'):
            continue
        f = line.rstrip('\n').split('\t')
        census[(int(f[0]), int(f[1]))] = (int(f[2]), int(f[4]), int(f[5]))
    cases = []
    # dihedral D8 on square, Q8 via quaternion units as signed perms of 8 points, S3, A4, S4, A5, D10
    D8 = closure([(1, 2, 3, 0), (3, 2, 1, 0)])
    cases.append(('D8', (8, 3), D8, perm_mul))
    # Q8: left regular rep of quaternion group: elements +-1,+-i,+-j,+-k
    qmul = {}
    units = ['1', 'i', 'j', 'k']
    tab = {('1', x): (1, x) for x in units}
    tab.update({(x, '1'): (1, x) for x in units})
    tab.update({('i', 'i'): (-1, '1'), ('j', 'j'): (-1, '1'), ('k', 'k'): (-1, '1'),
                ('i', 'j'): (1, 'k'), ('j', 'k'): (1, 'i'), ('k', 'i'): (1, 'j'),
                ('j', 'i'): (-1, 'k'), ('k', 'j'): (-1, 'i'), ('i', 'k'): (-1, 'j')})
    Q8 = [(s, u) for s in (1, -1) for u in units]

    def q_mul(a, b):
        s, u = tab[(a[1], b[1])]
        return (a[0] * b[0] * s, u)
    cases.append(('Q8', (8, 4), Q8, q_mul))
    S3 = closure([(1, 0, 2), (1, 2, 0)])
    cases.append(('S3', (6, 1), S3, perm_mul))
    A4 = closure([(1, 2, 0, 3), (0, 2, 3, 1)])
    cases.append(('A4', (12, 3), A4, perm_mul))
    S4 = closure([(1, 0, 2, 3), (1, 2, 3, 0)])
    cases.append(('S4', (24, 12), S4, perm_mul))
    A5 = closure([(1, 2, 0, 3, 4), (0, 1, 3, 4, 2)])
    cases.append(('A5', (60, 5), A5, perm_mul))
    D10 = closure([(1, 2, 3, 4, 0), (0, 4, 3, 2, 1)])
    cases.append(('D10', (10, 1), D10, perm_mul))
    # Heisenberg mod 3: B(v,w) = v0*w1  (commutator v0w1 - w0v1 = det)
    el, mu = heis_group(3, 2, lambda v, w: v[0] * w[1])
    cases.append(('Heis(3) = 3^{1+2} exp 3', (27, 3), el, mu))
    # 2^{1+4}+ : B = v0w1 + v2w3 over F2 (commutator = symplectic form)
    el, mu = heis_group(2, 4, lambda v, w: v[0] * w[1] + v[2] * w[3])
    cases.append(('2^{1+4} (B=v0w1+v2w3)', None, el, mu))
    el, mu = heis_group(2, 6, lambda v, w: v[0] * w[1] + v[2] * w[3] + v[4] * w[5])
    cases.append(('2^{1+6} (B=v0w1+v2w3+v4w5)', None, el, mu))
    for name, gid, elems, mul in cases:
        t0 = time.time()
        z, n, adj = element_graph(elems, mul)
        if n <= 60:
            w = nx_omega(n, adj)
        else:   # many twins -> too many maximal cliques for enumeration; use exact C MCQ
            Cq, pr = c_clique(n, adj, 600, 0)
            assert pr
            w = len(Cq)
        # lower bound max(omega, ceil(n/alpha)), alpha = clique number of complement (exact C MCQ)
        full = (1 << n) - 1
        cadj = [(~adj[v]) & full & ~(1 << v) for v in range(n)]
        Ia, pr = c_clique(n, cadj, 600, 0)
        assert pr
        alpha = len(Ia)
        lo = max(w, -(-n // alpha))
        d = max(c_dsatur(n, adj)) + 1
        a = sat_chi_plain(n, adj, lo, d, solver='minisat22')
        msg = '%s: |G|=%d z=%d omega=%d a=%d [alpha=%d, lower bound %d, DSATUR %d] (full element graph, %d vertices, %.1fs)' % (name, len(elems), z, w, a, alpha, lo, d, n, time.time() - t0)
        if gid:
            ok(census[gid] == (z, w, a), msg + ' == census %s %s' % (gid, census[gid]))
        else:
            print('INFO ' + msg)
    return


if __name__ == '__main__':
    which = sys.argv[1:] or ['1', '2', '3', '4', '5']
    if '1' in which: section1()
    if '2' in which: section2()
    if '3' in which: section3()
    if '4' in which: section4()
    if '5' in which: section5()
    print('CONTROL FAILURES: %d' % len(FAILS))
    for f in FAILS:
        print('  ' + f)
