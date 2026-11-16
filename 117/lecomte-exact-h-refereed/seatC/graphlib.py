"""graphlib.py -- exact clique number, DSATUR colouring, exact chromatic number (SAT),
and independent checkers.  Graphs are (n, adj) with adj[v] an int bitset.

Every positive answer carries a witness that is re-checked by an independent checker:
  clique  -> list of vertices, checked pairwise adjacent       (check_clique)
  colouring -> list of colours, checked proper on every edge   (check_colouring)
Upper bounds on omega (MCQ branch and bound) and lower bounds on chi (SAT UNSAT)
are the only unwitnessed claims; both are cross-checked against brute force on
random graphs in controls.py.
"""
import sys
from pysat.solvers import Solver

sys.setrecursionlimit(10000)


def T(n):
    """The paper's claimed profile h(n)."""
    if n <= 2:
        return 1
    if n <= 6:
        return n
    if n <= 8:
        return 10
    return 1 + 2 ** ((n - 1) // 2)


def parse_rows(rows):
    """rows: list of 0/1 strings. Returns (k, adj) and checks symmetry/irreflexivity."""
    k = len(rows)
    adj = [0] * k
    for j, r in enumerate(rows):
        assert len(r) == k, "row length"
        b = 0
        for l, ch in enumerate(r):
            if ch == '1':
                b |= 1 << l
        adj[j] = b
    for j in range(k):
        assert not (adj[j] >> j) & 1, "loop"
        for l in range(k):
            assert ((adj[j] >> l) & 1) == ((adj[l] >> j) & 1), "asymmetric"
    return k, adj


def check_clique(adj, C):
    C = list(C)
    if len(set(C)) != len(C):
        return False
    for a in range(len(C)):
        for b in range(a + 1, len(C)):
            if not (adj[C[a]] >> C[b]) & 1:
                return False
    return True


def check_colouring(n, adj, col):
    if len(col) != n:
        return False
    for v in range(n):
        m = adj[v]
        while m:
            low = m & -m
            u = low.bit_length() - 1
            m ^= low
            if col[u] == col[v]:
                return False
    return True


def max_clique(n, adj):
    """Tomita-style MCQ branch and bound. Returns a maximum clique (list)."""
    if n == 0:
        return []
    # relabel: high degree first (bit 0 = highest degree)
    deg = [bin(a).count('1') for a in adj]
    order = sorted(range(n), key=lambda v: -deg[v])
    pos = {v: i for i, v in enumerate(order)}
    radj = [0] * n
    for v in range(n):
        m = adj[v]
        b = 0
        while m:
            low = m & -m
            u = low.bit_length() - 1
            m ^= low
            b |= 1 << pos[u]
        radj[pos[v]] = b
    best = [[]]

    def colour_sort(P):
        verts, bounds = [], []
        Q = P
        c = 0
        while Q:
            c += 1
            Qc = Q
            while Qc:
                low = Qc & -Qc
                v = low.bit_length() - 1
                Qc &= ~radj[v] & ~low
                Q &= ~low
                verts.append(v)
                bounds.append(c)
        return verts, bounds

    def expand(R, P):
        verts, bounds = colour_sort(P)
        for idx in range(len(verts) - 1, -1, -1):
            if len(R) + bounds[idx] <= len(best[0]):
                return
            v = verts[idx]
            NP = P & radj[v]
            R.append(v)
            if NP:
                expand(R, NP)
            elif len(R) > len(best[0]):
                best[0] = list(R)
            R.pop()
            P &= ~(1 << v)

    expand([], (1 << n) - 1)
    C = [order[v] for v in best[0]]
    assert check_clique(adj, C)
    return C


def dsatur(n, adj):
    col = [-1] * n
    sat = [set() for _ in range(n)]
    deg = [bin(a).count('1') for a in adj]
    for _ in range(n):
        v = max((u for u in range(n) if col[u] < 0), key=lambda u: (len(sat[u]), deg[u]))
        c = 0
        while c in sat[v]:
            c += 1
        col[v] = c
        m = adj[v]
        while m:
            low = m & -m
            u = low.bit_length() - 1
            m ^= low
            sat[u].add(c)
    assert check_colouring(n, adj, col)
    return col


def colour_sat(n, adj, k, clique=(), solver='cadical195'):
    """Is the graph k-colourable?  Returns colouring list, or None if UNSAT.
    Symmetry breaking: vertices of `clique` get colours 0,1,2,... (sound)."""
    if k <= 0:
        return None if n else []
    if len(clique) > k:
        return None
    var = lambda v, c: v * k + c + 1
    with Solver(name=solver) as s:
        for v in range(n):
            s.add_clause([var(v, c) for c in range(k)])
        for v in range(n):
            m = adj[v]
            while m:
                low = m & -m
                u = low.bit_length() - 1
                m ^= low
                if u > v:
                    for c in range(k):
                        s.add_clause([-var(v, c), -var(u, c)])
        for i, v in enumerate(clique):
            s.add_clause([var(v, i)])
        if not s.solve():
            return None
        model = set(l for l in s.get_model() if l > 0)
    col = []
    for v in range(n):
        cs = [c for c in range(k) if var(v, c) in model]
        col.append(cs[0])
    assert check_colouring(n, adj, col)
    return col


def chromatic(n, adj, clique=None, solver='cadical195'):
    """Exact chromatic number with witness colouring.
    Returns (chi, colouring, lower_bound_source)."""
    if n == 0:
        return 0, [], 'empty'
    if clique is None:
        clique = max_clique(n, adj)
    lo = len(clique)
    col = dsatur(n, adj)
    hi = max(col) + 1
    best = col
    src = 'clique=dsatur'
    while hi > lo:
        c = colour_sat(n, adj, hi - 1, clique, solver)
        if c is None:
            src = 'SAT-UNSAT(%d)' % (hi - 1)
            break
        best = c
        hi = max(c) + 1
        src = 'clique=SAT'
    return hi, best, src


# ---------------- wrappers around the C workhorse (witnesses re-checked here) -------------
import subprocess, os
GTOOL = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gtool')


def _graph_text(n, adj):
    lines = [str(n)]
    for v in range(n):
        lines.append(''.join('1' if (adj[v] >> u) & 1 else '0' for u in range(n)))
    return '\n'.join(lines) + '\n'


def _run(n, adj, args, timeout=7200):
    r = subprocess.run([GTOOL] + [str(a) for a in args], input=_graph_text(n, adj), capture_output=True, text=True, timeout=timeout)
    if r.returncode != 0:
        raise RuntimeError('gtool failed: %s' % r.stderr)
    return r.stdout.split()


def c_clique(n, adj, tlim=60.0, lb=0):
    """Exact search for cliques of size >= lb. Returns (clique or None, proven)."""
    out = _run(n, adj, ['clique', tlim, lb])
    assert out[0] == 'CLIQUE'
    sz, proven = int(out[1]), int(out[2]) == 1
    C = [int(x) for x in out[4:]]
    assert len(C) == sz
    if sz:
        assert check_clique(adj, C), 'C clique witness invalid'
        assert sz >= lb
        return C, proven
    return None, proven


def c_heurclique(n, adj, iters=200, seed=1):
    out = _run(n, adj, ['heurclique', iters, seed])
    C = [int(x) for x in out[4:]]
    assert check_clique(adj, C)
    return C


def c_dsatur(n, adj):
    out = _run(n, adj, ['dsatur'])
    col = [int(x) for x in out[2:]]
    assert check_colouring(n, adj, col)
    return col


def c_tabu(n, adj, K, iters=200000, seed=1):
    out = _run(n, adj, ['tabu', K, iters, seed])
    if out[0] == 'FAIL':
        return None
    col = [int(x) for x in out[2:]]
    assert check_colouring(n, adj, col) and max(col) < K
    return col
