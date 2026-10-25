#!/usr/bin/env python3
"""Check 1a/1b: the digit encoding (3.5)-(3.8) and Lemma 3.3 (determinant obstruction),
end to end, with exact big-integer arithmetic.

Instance family 'd1': d = 1 (K = F_r), M = 3, T = 1, k = 2.  Label coordinates X(xi) = (1, xi, xi^2),
   N = Vandermonde det, decomposition (f_10, f_20, f_30) = (1*X_1, X_2, X_3).
Instance family 'T4' (synthetic, tests the matching (3.7) with T > 1): label coordinates
   y(xi) = (1, xi, xi^2, xi^3), the T = C(4,3) = 4 monomial triples p<q<s with coefficients c_a,
   P = sum_a c_a det[y_p; y_q; y_s], k = T^2 + 1 = 17.  c = (1,0,0,0) makes P = Vandermonde
   (nonzero for distinct labels) while still using all four slots (three with zero scalar,
   exactly as Lemma 3.1 allows); random c tests the identity gamma_{k-1} == P (mod r).

CHANGED vs the paper: L = r^2 (paper L = r^10); B = nextprime(100 k^2 L^3) so B - 1 >= 100 k^2 L^3
   still holds and L < B, r | L.  Everything else as written.

Checks for every sampled triple of columns (labels xi_1, xi_2, xi_3, fresh digits per column):
  I1  gamma_{k-1} == P(labels) (mod r)                    [the (3.7)+(3.3) identity]
  I2  |gamma_u| <= 6 k^2 L^3 for all u                      [(3.9)]
  I3  sum_{u<k} gamma_u B^u == det C (mod h)                 [S_C represents det C]
  OB  P(labels) != 0 (mod r)  ==>  det C mod h has no representative in [-tau, tau]   [Lemma 3.3]
  RL  repeated labels: how often det C mod h DOES have a representative in [-tau, tau]
Mutations (checker must REJECT):
  M1 d1: row-3 designated position moved 1 -> 0 (designated triple no longer sums to k-1)
  M2 d1: base inequality dropped (B = nextprime(L), so L < B still holds but B << 100k^2L^3)
  M3 T4: l_a = T^2 - T a (drops the '+1'); unmatched triples (0,a',a') now sum to k-1
  M4 T4: base inequality dropped
"""
import random, sys
from sympy import nextprime

def polymul(a, b):
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                out[i + j] += x * y
    return out

def polyadd(a, b, sgn=1):
    n = max(len(a), len(b)); out = [0] * n
    for i, x in enumerate(a): out[i] += x
    for i, y in enumerate(b): out[i] += sgn * y
    return out

PERMS = [((0, 1, 2), 1), ((1, 2, 0), 1), ((2, 0, 1), 1), ((0, 2, 1), -1), ((2, 1, 0), -1), ((1, 0, 2), -1)]

def det3_int(m):
    return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
            - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
            + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))

class Encoding:
    def __init__(self, r, L, B, T, fvals, positions):
        """fvals(xi) -> list over a of (f1a, f2a, f3a) residues mod r;
        positions -> list over a of (i_a, j_a, l_a)."""
        self.r, self.L, self.B, self.T = r, L, B, T
        self.k = T * T + 1
        self.h = B ** self.k
        self.tau = B ** (self.k - 1) // 2
        self.fvals = fvals
        self.positions = positions
        # sanity: positions distinct within each row and inside [0,k-1]
        for row in range(3):
            ps = [p[row] for p in positions]
            assert len(set(ps)) == len(ps), "positions collide within a row"
            assert all(0 <= x < self.k for x in ps)

    def column(self, xi, rng):
        r, L, k = self.r, self.L, self.k
        res = [[0] * k for _ in range(3)]
        for a, (f1, f2, f3) in enumerate(self.fvals(xi)):
            ia, ja, la = self.positions[a]
            res[0][ia] = f1 % r; res[1][ja] = f2 % r; res[2][la] = f3 % r
        digits = [[0] * k for _ in range(3)]
        for i in range(3):
            for v in range(k):
                base = res[i][v] if res[i][v] != 0 else r   # representative in [1, r]
                t = rng.randrange(L // r)
                dgt = base + r * t
                assert 1 <= dgt <= L and dgt % r == res[i][v]
                digits[i][v] = dgt
        return digits

    def analyse(self, cols):
        """cols: three digit arrays.  Return gamma list, det C mod h centered, S_C."""
        B, k, h = self.B, self.k, self.h
        # F_ij(Y) = sum_v c_iv^(j) Y^v ; det over (i row, j column)
        F = [[cols[j][i] for j in range(3)] for i in range(3)]
        gamma = [0] * (3 * (k - 1) + 1)
        for perm, sg in PERMS:
            prod = polymul(polymul(F[0][perm[0]], F[1][perm[1]]), F[2][perm[2]])
            gamma = polyadd(gamma, prod, sg)
        ints = [[sum(cols[j][i][v] * B ** v for v in range(k)) for j in range(3)] for i in range(3)]
        detC = det3_int(ints) % h
        cen = detC if detC <= h // 2 else detC - h
        S = sum(gamma[u] * B ** u for u in range(k))
        return gamma, cen, S

def vandermonde_mod(xs, r):
    a, b, c = xs
    return ((b - a) * (c - a) * (c - b)) % r

def run(name, enc, Pfun, r, nsamp, rng, force_repeat_frac=0.5, mutation=False):
    k, L, tau, h = enc.k, enc.L, enc.tau, enc.h
    A0 = 6 * k * k * L ** 3
    stats = dict(samples=0, I1_fail=0, I2_fail=0, I3_fail=0, OB_tested=0, OB_fail=0,
                 RL_tested=0, RL_small=0)
    examples_RL = []; examples_OB = []
    for s in range(nsamp):
        if rng.random() < force_repeat_frac:
            x = rng.randrange(r); y = rng.randrange(r)
            pat = rng.randrange(3)
            xs = [x, x, y] if pat == 0 else ([x, y, x] if pat == 1 else [y, x, x])
        else:
            xs = [rng.randrange(r) for _ in range(3)]
        cols = [enc.column(xi, rng) for xi in xs]
        gamma, cen, S = enc.analyse(cols)
        P = Pfun(xs) % r
        stats['samples'] += 1
        if gamma[k - 1] % r != P: stats['I1_fail'] += 1
        if max(abs(g) for g in gamma) > A0: stats['I2_fail'] += 1
        if (S - cen) % h != 0: stats['I3_fail'] += 1
        small = abs(cen) <= tau   # centered rep is the min-abs rep; any rep in [-tau,tau] iff this
        if P != 0:
            stats['OB_tested'] += 1
            if small:
                stats['OB_fail'] += 1
                if len(examples_OB) < 3: examples_OB.append((xs, gamma[k - 1], cen))
        if len(set(xs)) < 3:
            stats['RL_tested'] += 1
            if small:
                stats['RL_small'] += 1
                if len(examples_RL) < 3: examples_RL.append((xs, gamma[k - 1], cen))
    tag = "MUTATION" if mutation else "POSITIVE"
    print(f"[{tag}] {name}: r={r} L={L} k={k} B={enc.B} tau=floor(B^(k-1)/2)")
    print("   ", stats)
    if examples_OB: print("    OB counterexamples (labels, gamma_{k-1}, centered det):", examples_OB)
    if examples_RL: print("    repeated-label small-det examples (labels, gamma_{k-1}, centered det):", examples_RL)
    return stats

def main():
    rng = random.Random(20261022)
    results = {}
    # ---------- d = 1 ----------
    for r, nsamp in ((3, 20000), (5, 12000), (7, 8000)):
        L = r * r
        k = 2
        B = nextprime(100 * k * k * L ** 3)
        assert B - 1 >= 100 * k * k * L ** 3 and L < B and L % r == 0
        fv = lambda xi, r=r: [(1, xi, xi * xi)]
        enc = Encoding(r, L, B, 1, fv, [(0, 0, 1)])
        P = lambda xs, r=r: vandermonde_mod(xs, r)
        results[('d1', r)] = run("d1 positive", enc, P, r, nsamp, rng)
        # M1: designated position of row 3 moved to 0
        encM1 = Encoding(r, L, B, 1, fv, [(0, 0, 0)])
        results[('d1M1', r)] = run("d1 M1 (row-3 position 1->0)", encM1, P, r, nsamp, rng, mutation=True)
        # M2: base inequality dropped
        Bsmall = nextprime(L)
        encM2 = Encoding(r, L, Bsmall, 1, fv, [(0, 0, 1)])
        results[('d1M2', r)] = run(f"d1 M2 (B={Bsmall} << 100k^2L^3)", encM2, P, r, nsamp, rng, force_repeat_frac=0.0, mutation=True)
    # ---------- synthetic T = 4 ----------
    T = 4
    triples = [(0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)]
    def ycoords(xi, r): return [1, xi % r, xi * xi % r, xi ** 3 % r]
    pos_paper = [(a, T * a, T * T - (T + 1) * a) for a in range(T)]
    pos_M3 = [(a, T * a, T * T - T * a) for a in range(T)]
    for r, nsamp in ((3, 3000), (5, 3000), (7, 2000)):
        L = r * r
        k = T * T + 1
        B = nextprime(100 * k * k * L ** 3)
        for cname, cvec in (("c=(1,0,0,0)", [1, 0, 0, 0]), ("c=random", [rng.randrange(r) for _ in range(4)])):
            def fv(xi, r=r, cvec=cvec):
                y = ycoords(xi, r)
                return [(cvec[a] * y[p], y[q], y[s]) for a, (p, q, s) in enumerate(triples)]
            def P(xs, r=r, cvec=cvec):
                ys = [ycoords(x, r) for x in xs]
                tot = 0
                for a, (p, q, s) in enumerate(triples):
                    m = [[ys[j][p] for j in range(3)], [ys[j][q] for j in range(3)], [ys[j][s] for j in range(3)]]
                    tot += cvec[a] * det3_int(m)
                return tot % r
            enc = Encoding(r, L, B, T, fv, pos_paper)
            results[('T4', r, cname)] = run(f"T4 positive {cname} c={cvec}", enc, P, r, nsamp, rng, force_repeat_frac=0.3)
            encM3 = Encoding(r, L, B, T, fv, pos_M3)
            results[('T4M3', r, cname)] = run(f"T4 M3 (l_a=T^2-Ta) {cname}", encM3, P, r, nsamp, rng, force_repeat_frac=0.3, mutation=True)
            Bsmall = nextprime(L)
            encM4 = Encoding(r, L, Bsmall, T, fv, pos_paper)
            results[('T4M4', r, cname)] = run(f"T4 M4 (B={Bsmall})", encM4, P, r, nsamp, rng, force_repeat_frac=0.0, mutation=True)
    # ---------- matching (3.7) exhaustively for several T ----------
    print("\nMatching (3.7) exhaustive check:")
    for TT in (1, 2, 3, 4, 5, 7, 10, 20):
        kk = TT * TT + 1
        bad = 0; matched = 0
        for a in range(TT):
            for a1 in range(TT):
                for a2 in range(TT):
                    s = a + TT * a1 + (TT * TT - (TT + 1) * a2)
                    if s == kk - 1:
                        if a == a1 == a2: matched += 1
                        else: bad += 1
        mbad = 0
        for a in range(TT):
            for a1 in range(TT):
                for a2 in range(TT):
                    s = a + TT * a1 + (TT * TT - TT * a2)
                    if s == kk - 1 and not (a == a1 == a2): mbad += 1
        print(f"  T={TT}: matched triples summing to k-1: {matched} (want {TT}); unmatched: {bad} (want 0); "
              f"MUTATION l_a=T^2-Ta unmatched: {mbad} (want >0 for T>=2)")
    # verdict summary
    print("\nSUMMARY")
    for key, st in results.items():
        print("  ", key, {x: st[x] for x in ('samples', 'I1_fail', 'I2_fail', 'I3_fail', 'OB_tested', 'OB_fail', 'RL_tested', 'RL_small')})

if __name__ == "__main__":
    main()
