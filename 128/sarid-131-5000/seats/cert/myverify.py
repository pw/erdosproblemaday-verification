#!/usr/bin/env python3
"""Seat CERT: independent exact verifier for Sarid's clebsch_tangent_certificate.json.

Written from scratch.  The author's script was read ONLY to learn the JSON
format (block names, the integer key convention that fixes coordinate order).
Nothing is imported from the downloaded tree.

Semantics (stated once, used everywhere): INJECTIVE sampling.  For a host H on
six labelled vertices, the coefficient of H in a density expression is the
probability under a uniformly random bijection [6] -> V(H) (equivalently a
uniformly random ordering of V(H)).  In a graphon W the six sample points are
a.s. distinct, so t(F,W) = sum_H p(H;W) * c_H(F) with p(H;W) the induced
6-vertex density (sampling WITH repetition from the step graphon of a graph).

Target  T_H = c_H(C4) - c_H(3K2) + gamma*c_H(K2) with
   c_H(C4)  = #C4-subgraphs(H) / 45     (8 injective homs per 4-cycle, 360 injective 4-tuples)
   c_H(3K2) = #perfect-matchings(H) / 15 (random ordering -> uniform perfect matching of K6)
   c_H(K2)  = e(H) / 15
Squares (all routes are subset sums, NOT 720-permutation loops):
   s0 : (1/20)  sum_{3-sets S} v[F(S)] v[F(V\\S)]
   s2 : (1/180) sum_{ordered (x,y) of root type m} sum_{2-sets P of rest} v[k(x,y,P)] v[k(x,y,rest\\P)]
   u4 : (1/15)  sum_{4-sets R of root type M} avg_{kappa in K(R)} v[prof(l1,kappa)] v[prof(l2,kappa)]
        where K(R) = ALL bijections [4]->R realising the block's labelled root mask
        (averaging over every canonical assignment; the author breaks ties
        lexicographically instead - the two agree, see REPORT.md).
"""
import itertools, json, subprocess, sys
from fractions import Fraction as Fr
from math import comb

CERT = '/tmp/erdos1800/claim/erdos-128-sparse-halves/clebsch_tangent_certificate.json'

# ---------------------------------------------------------------- graph6 (own parser)
def parse_g6(s):
    s = s.strip()
    n = ord(s[0]) - 63
    bits = []
    for ch in s[1:]:
        x = ord(ch) - 63
        bits += [(x >> (5 - k)) & 1 for k in range(6)]
    E = set(); t = 0
    for j in range(1, n):
        for i in range(j):
            if bits[t]: E.add((i, j))
            t += 1
    adj = [[0]*n for _ in range(n)]
    for i, j in E: adj[i][j] = adj[j][i] = 1
    return n, adj

def tri_free(adj):
    n = len(adj)
    return not any(adj[a][b] and adj[b][c] and adj[a][c]
                   for a, b, c in itertools.combinations(range(n), 3))

def canon6(adj):
    """canonical form: lexicographically smallest sorted edge tuple over all 720 relabellings"""
    n = len(adj); E = [(i, j) for i in range(n) for j in range(i+1, n) if adj[i][j]]
    best = None
    for p in itertools.permutations(range(n)):
        key = tuple(sorted(tuple(sorted((p[i], p[j]))) for i, j in E))
        if best is None or key < best: best = key
    return best

# ---------------------------------------------------------------- hosts, two routes
def hosts_geng():
    out = subprocess.run(['/usr/bin/nauty-geng', '-tq', '6'], capture_output=True, text=True, check=True).stdout.split()
    return [parse_g6(s)[1] for s in out]

# ---------------------------------------------------------------- key convention (from the JSON format)
def lexpairs(k):
    return [(i, j) for i in range(k) for j in range(i+1, k)]

def mask(adj, verts):
    return sum(1 << b for b, (i, j) in enumerate(lexpairs(len(verts))) if adj[verts[i]][verts[j]])

def coords():
    """Coordinate order of every block, re-derived from first principles:
    keys = minimal lexicographic-pair mask over orderings of the UNLABELLED vertices."""
    C = {}
    # s0: 3-vertex triangle-free graphs = 0,1,2 edges; check key convention gives the same order
    keys3 = sorted({min(mask_labelled(m3, p, 3) for p in itertools.permutations(range(3)))
                    for m3 in range(8) if m3 != 7})
    assert keys3 == [0, 1, 3], keys3
    C['s0_root0'] = {0: 0, 1: 1, 2: 2}            # index = number of edges
    # s2: labelled 4-vertex triangle-free graphs, roots 0,1 fixed, key=min over swap(2,3)
    for m in (0, 1):
        ks = set()
        for m4 in range(64):
            if (m4 & 1) != m: continue
            adj = adj_from_mask(m4, 4)
            if not tri_free(adj): continue
            ks.add(min(m4, mask(adj, [0, 1, 3, 2])))
        C[f's2_root{m}'] = {k: i for i, k in enumerate(sorted(ks))}
    # u4: root types = minimal masks of triangle-free 4-vertex graphs; coordinates = independent sets of the root
    types = set()
    for m4 in range(64):
        adj = adj_from_mask(m4, 4)
        if tri_free(adj):
            types.add(min(mask(adj, list(p)) for p in itertools.permutations(range(4))))
    for M in sorted(types):
        adj = adj_from_mask(M, 4)
        ind = [p for p in range(16)
               if not any((p >> i & 1) and (p >> j & 1) and adj[i][j] for i, j in lexpairs(4))]
        C[f'u4_root{M}'] = {p: i for i, p in enumerate(sorted(ind))}
    return C

def adj_from_mask(m, k):
    adj = [[0]*k for _ in range(k)]
    for b, (i, j) in enumerate(lexpairs(k)):
        if m >> b & 1: adj[i][j] = adj[j][i] = 1
    return adj

def mask_labelled(m, p, k):
    adj = adj_from_mask(m, k)
    return mask(adj, list(p))

# ---------------------------------------------------------------- target, own route
def count_c4(adj):
    n = len(adj); c = 0
    for a, b, c_, d in itertools.combinations(range(n), 4):
        # the three 4-cycles on {a,b,c,d}: a-b-c-d, a-b-d-c, a-c-b-d
        for x, y, z, w in ((a, b, c_, d), (a, b, d, c_), (a, c_, b, d)):
            if adj[x][y] and adj[y][z] and adj[z][w] and adj[w][x]: c += 1
    return c

def count_pm(adj):
    def rec(rest):
        if not rest: return 1
        a = rest[0]; tot = 0
        for b in rest[1:]:
            if adj[a][b]: tot += rec([x for x in rest if x not in (a, b)])
        return tot
    return rec(list(range(len(adj))))

def edges(adj):
    n = len(adj); return sum(adj[i][j] for i in range(n) for j in range(i+1, n))

def target_parts(adj):
    return Fr(count_c4(adj), 45), Fr(count_pm(adj), 15), Fr(edges(adj), 15)

# ---------------------------------------------------------------- squares, own route
def three_set_index(adj, S):
    a, b, c = S
    return adj[a][b] + adj[a][c] + adj[b][c]

def s2_key(adj, x, y, P):
    return min(mask(adj, [x, y, P[0], P[1]]), mask(adj, [x, y, P[1], P[0]]))

def u4_type(adj, R):
    return min(mask(adj, list(p)) for p in itertools.permutations(R))

def square_coeff(adj, block, vec, C):
    V = range(6)
    if block == 's0_root0':
        tot = Fr(0)
        for S in itertools.combinations(V, 3):
            T = tuple(v for v in V if v not in S)
            tot += vec[three_set_index(adj, S)] * vec[three_set_index(adj, T)]
        return tot / 20
    if block.startswith('s2_root'):
        m = int(block[7:]); idx = C[block]; tot = Fr(0)
        for x, y in itertools.permutations(V, 2):
            if adj[x][y] != m: continue
            rest = [v for v in V if v not in (x, y)]
            for P in itertools.combinations(rest, 2):
                Q = tuple(v for v in rest if v not in P)
                tot += vec[idx[s2_key(adj, x, y, P)]] * vec[idx[s2_key(adj, x, y, Q)]]
        return tot / 180
    if block.startswith('u4_root'):
        M = int(block[7:]); idx = C[block]; tot = Fr(0)
        for R in itertools.combinations(V, 4):
            kap = [p for p in itertools.permutations(R) if mask(adj, list(p)) == M]
            if not kap: continue
            # sanity: M must be the minimal mask of R's class (else R belongs to another block)
            assert u4_type(adj, R) == M
            l1, l2 = [v for v in V if v not in R]
            acc = Fr(0)
            for k in kap:
                p1 = sum(adj[l1][k[i]] << i for i in range(4))
                p2 = sum(adj[l2][k[i]] << i for i in range(4))
                acc += vec[idx[p1]] * vec[idx[p2]]
            tot += acc / len(kap)
        return tot / 15
    raise ValueError(block)

def square_matrix(adj, block, C):
    """bilinear-form matrix G with  square_coeff(v) = v^T G v ; same enumeration as square_coeff."""
    k = len(C[block]); G = [[Fr(0)] * k for _ in range(k)]
    V = range(6)
    if block == 's0_root0':
        for S in itertools.combinations(V, 3):
            T = tuple(v for v in V if v not in S)
            G[three_set_index(adj, S)][three_set_index(adj, T)] += Fr(1, 20)
        return G
    if block.startswith('s2_root'):
        m = int(block[7:]); idx = C[block]
        for x, y in itertools.permutations(V, 2):
            if adj[x][y] != m: continue
            rest = [v for v in V if v not in (x, y)]
            for P in itertools.combinations(rest, 2):
                Q = tuple(v for v in rest if v not in P)
                G[idx[s2_key(adj, x, y, P)]][idx[s2_key(adj, x, y, Q)]] += Fr(1, 180)
        return G
    M = int(block[7:]); idx = C[block]
    for R in itertools.combinations(V, 4):
        kap = [p for p in itertools.permutations(R) if mask(adj, list(p)) == M]
        if not kap: continue
        l1, l2 = [v for v in V if v not in R]
        for kk in kap:
            p1 = sum(adj[l1][kk[i]] << i for i in range(4))
            p2 = sum(adj[l2][kk[i]] << i for i in range(4))
            G[idx[p1]][idx[p2]] += Fr(1, 15 * len(kap))
    return G

def quad(G, v):
    return sum(v[i] * G[i][j] * v[j] for i in range(len(v)) for j in range(len(v)) if G[i][j])

class Expansion:
    """per-host target parts and Gram matrices, computed once"""
    def __init__(self, hosts, C):
        self.hosts = hosts; self.C = C
        self.parts = [target_parts(a) for a in hosts]
        self.G = [{b: square_matrix(a, b, C) for b in C} for a in hosts]

def check_fast(E, eps, terms, gamma0=Fr(3, 64)):
    ok = all(w > 0 for _, w, _ in terms); mins = None; need = Fr(0); worst = None
    for b, w, v in terms:
        if len(v) != len(E.C[b]): return False, None, None, 'dimension mismatch'
    for h in range(len(E.hosts)):
        c4, m3, rho = E.parts[h]
        T0 = c4 - m3 + gamma0 * rho
        sos = sum(w * quad(E.G[h][b], v) for b, w, v in terms)
        sl = T0 + eps * rho - sos
        if sl < 0: ok = False
        if mins is None or sl < mins: mins, worst = sl, h
        if rho: need = max(need, (sos - T0) / rho)
    return ok, mins, need, worst

# ---------------------------------------------------------------- main check
def load_cert(path=CERT):
    d = json.load(open(path))
    terms = [(t['block'], Fr(t['weight']), [Fr(x) for x in t['vector']]) for t in d['terms']]
    return Fr(d['epsilon']), terms

def check(eps, terms, hosts, C, gamma0=Fr(3, 64), verbose=False, rows=None):
    """returns (ok, min_slack, eps_needed). rows: list to append per-host rows."""
    ok = True; mins = None; need = Fr(0)
    for b, w, v in terms:
        if w <= 0: ok = False
        if len(v) != len(C[b]): raise AssertionError(f'dim mismatch {b}: {len(v)} vs {len(C[b])}')
    for h, adj in enumerate(hosts):
        c4, m3, rho = target_parts(adj)
        T0 = c4 - m3 + gamma0 * rho
        T = T0 + eps * rho
        sos = sum(w * square_coeff(adj, b, v, C) for b, w, v in terms)
        sl = T - sos
        if sl < 0: ok = False
        if mins is None or sl < mins: mins = sl
        if rho: need = max(need, (sos - T0) / rho)
        if rows is not None:
            rows.append((h, adj, c4, m3, rho, T, sos, sl))
    return ok, mins, need

def g6_of(adj):
    n = len(adj); bits = [adj[i][j] for j in range(1, n) for i in range(j)]
    bits += [0] * (-len(bits) % 6)
    return chr(n + 63) + ''.join(chr(63 + int(''.join(map(str, bits[k:k+6])), 2)) for k in range(0, len(bits), 6))

def main():
    # --- hosts route 1: geng
    H1 = hosts_geng()
    assert len(H1) == 38 and all(tri_free(a) for a in H1)
    c1 = {canon6(a) for a in H1}; assert len(c1) == 38
    # --- hosts route 2: brute force over all 2^15 labelled graphs
    pairs = lexpairs(6); c2 = set()
    perms = list(itertools.permutations(range(6)))
    pidx = {(i, j): b for b, (i, j) in enumerate(pairs)}
    permbits = [[pidx[tuple(sorted((p[i], p[j])))] for (i, j) in pairs] for p in perms]
    seen = bytearray(1 << 15); ncls = 0; trifree_lab = 0
    for m in range(1 << 15):
        if seen[m]: continue
        adj = adj_from_mask(m, 6)
        orbit = set()
        for pb in permbits:
            mm = 0
            for b in range(15):
                if m >> b & 1: mm |= 1 << pb[b]
            orbit.add(mm)
        for mm in orbit: seen[mm] = 1
        if tri_free(adj):
            ncls += 1; trifree_lab += len(orbit)
            c2.add(canon6(adj))
    print('hosts: geng -t 6 gives', len(H1), '; brute force over 2^15 labelled graphs gives',
          ncls, 'classes (', trifree_lab, 'labelled triangle-free graphs)')
    assert c1 == c2, 'host lists disagree'
    print('hosts: the two routes give the SAME 38 isomorphism classes')
    C = coords()
    print('block dimensions:', {k: len(v) for k, v in C.items()})
    eps, terms = load_cert()
    print('epsilon =', eps, ' gamma =', Fr(3, 64) + eps, ' terms =', len(terms))
    rows = []
    ok, mins, need = check(eps, terms, H1, C, rows=rows)
    with open('/tmp/erdos1800/seats/cert/HOSTS.tsv', 'w') as fh:
        fh.write('host\tgraph6\tedges\tC4_subgraphs\tperfect_matchings\ttarget_coeff\tsos_coeff\tslack\tslack_float\ttarget_float\tsos_float\n')
        for h, adj, c4, m3, rho, T, sos, sl in rows:
            fh.write(f'{h}\t{g6_of(adj)}\t{edges(adj)}\t{count_c4(adj)}\t{count_pm(adj)}\t{T}\t{sos}\t{sl}\t{float(sl):.6e}\t{float(T):.12e}\t{float(sos):.12e}\n')
    for h, adj, c4, m3, rho, T, sos, sl in sorted(rows, key=lambda r: r[7]):
        print(f'host {h:2d} {g6_of(adj):5s} e={edges(adj):2d}  target={float(T): .15e}  sos={float(sos): .15e}  slack={float(sl): .3e}')
    print('ALL HOSTS DOMINATE:', ok)
    print('minimum slack:', float(mins), '(exact', mins, ')')
    print('epsilon needed by these squares:', float(need))
    print('needed < used:', need < eps, ' needed exact =', need)
    return ok

if __name__ == '__main__':
    sys.exit(0 if main() else 1)
