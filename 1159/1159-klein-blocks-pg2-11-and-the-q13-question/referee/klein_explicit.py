"""Referee: build Klein's configuration from the EXPLICIT literature coordinates (Seceleanu, arXiv:1410.0312, §4.2:
roots c, cbar of t^2+t+2; 21 quadruple points = all coordinate permutations of (1:0:0),(1:+-1:0),(1:+-1:+-cbar);
28 triple points = permutations of (c:+-1:0),(1:+-1:+-1),(cbar^2:+-1:+-1); the 21 lines = permutations of
[1:0:0],[1:+-1:0],[1:+-1:+-c]) over F_q, q in {7,9,11,23,29,37,43,...}, and
 (i) test whether the 21 quadruple points Q form a set projectively equivalent to our q=11 witness;
 (ii) compute the spectrum of Q in PG(2,q) for each q (tests C4 '21q-98' and 'q in {9,11}' on actual configurations)."""
import itertools, json, os, sys
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class Field:
    def __init__(self, q):
        self.q = q
        if q in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 53):
            self.add = [[(a + b) % q for b in range(q)] for a in range(q)]
            self.mul = [[(a * b) % q for b in range(q)] for a in range(q)]
        elif q == 9:  # F_3[i]/(i^2+1), element a+3b <-> a + b i
            def enc(a, b): return a % 3 + 3 * (b % 3)
            def dec(x): return x % 3, x // 3
            self.add = [[enc(dec(x)[0] + dec(y)[0], dec(x)[1] + dec(y)[1]) for y in range(9)] for x in range(9)]
            self.mul = [[enc(dec(x)[0] * dec(y)[0] - dec(x)[1] * dec(y)[1], dec(x)[0] * dec(y)[1] + dec(x)[1] * dec(y)[0]) for y in range(9)] for x in range(9)]
        else:
            raise ValueError(q)
        self.neg = [next(y for y in range(q) if self.add[x][y] == 0) for x in range(q)]
        self.inv = [None] + [next(y for y in range(q) if self.mul[x][y] == 1) for x in range(1, q)]
        # field axioms sanity (assoc/distrib on all triples for small q)
        for a, b, c in itertools.product(range(q), repeat=3):
            assert self.mul[a][self.add[b][c]] == self.add[self.mul[a][b]][self.mul[a][c]]
            assert self.mul[self.mul[a][b]][c] == self.mul[a][self.mul[b][c]]
    def norm(self, v):
        for x in v:
            if x:
                iv = self.inv[x]; return tuple(self.mul[iv][y] for y in v)
        raise ValueError
    def dot(self, u, v):
        s = 0
        for a, b in zip(u, v): s = self.add[s][self.mul[a][b]]
        return s

def klein(q):
    F = Field(q)
    roots = [t for t in range(q) if F.add[F.add[F.mul[t][t]][t]][F.add[1][1]] == 0]
    if not roots: return F, None
    out = []
    for c in roots:
        cb = F.add[F.neg[c]][F.neg[1]]  # cbar = -1 - c
        one, m1 = 1, F.neg[1]
        def perms(vs):
            res = set()
            for v in vs:
                for pm in itertools.permutations(v): res.add(F.norm(pm))
            return res
        signs = [one, m1]
        Qp = perms([(1, 0, 0)] + [(1, s, 0) for s in signs] + [(1, s, F.mul[t][cb]) for s in signs for t in signs])
        Tp = perms([(c, s, 0) for s in signs] + [(1, s, t) for s in signs for t in signs] +
                   [(F.mul[cb][cb], s, t) for s in signs for t in signs])
        Lp = perms([(1, 0, 0)] + [(1, s, 0) for s in signs] + [(1, s, F.mul[t][c]) for s in signs for t in signs])
        out.append((c, Qp, Tp, Lp))
    return F, out

def plane(F):
    q = F.q
    pts = sorted({F.norm(v) for v in itertools.product(range(q), repeat=3) if any(v)})
    inc = [frozenset(i for i, P in enumerate(pts) if F.dot(P, L) == 0) for L in pts]
    assert all(len(l) == q + 1 for l in inc)
    return pts, {P: i for i, P in enumerate(pts)}, inc

res = {}
for q in (7, 9, 11, 23, 29, 37, 43):
    F, out = klein(q)
    if out is None:
        print(f"q={q}: t^2+t+2 has no root in F_q -> skip"); continue
    pts, idx, inc = plane(F)
    for c, Qp, Tp, Lp in out:
        Qi = {idx[P] for P in Qp}; Ti = {idx[P] for P in Tp}
        line_ids = {idx[L] for L in Lp}
        sp = dict(sorted(Counter(len(Qi & l) for l in inc).items()))
        # incidence check: each listed line through exactly 4 Q-points and 4 T-points?
        lq = Counter(len(Qi & inc[li]) for li in line_ids); lt = Counter(len(Ti & inc[li]) for li in line_ids)
        four = {li for li, l in enumerate(inc) if len(l & Qi) == 4}
        print(f"q={q} c={c}: |Q|={len(Qi)} |T|={len(Ti)} |Q&T|={len(Qi & Ti)} |lines|={len(line_ids)}; "
              f"Q-points per listed line {dict(lq)}, T-points per listed line {dict(lt)}; listed lines == 4-secants of Q: {line_ids == four}")
        print(f"      spectrum of Q (21 quadruple points) in PG(2,{q}): {sp}  blocking={0 not in sp}  21q-98={21*q-98}, lines met={sum(v for k, v in sp.items() if k)}")
        res[(q, c)] = (pts, idx, inc, Qp)

# (i) projective equivalence with our q=11 witness
import rpg
W = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'runs', 'witnesses_q11_c4.json')))
S = [rpg.norm(P, 11) for P in W['cadical']]
def find_frame(Sv):
    for quad in itertools.combinations(Sv, 4):
        if rpg.general_position(list(quad), 11): return list(quad)
for (q, c), (pts, idx, inc, Qp) in res.items():
    if q != 11: continue
    Qs = set(Qp); Fr = find_frame(S); cnt = 0
    for quad in itertools.permutations(sorted(Qs), 4):
        if not rpg.general_position(list(quad), 11): continue
        g = rpg.proj_from_frames(Fr, list(quad), 11)
        if all(rpg.norm(rpg.matvec(g, P, 11), 11) in Qs for P in S): cnt += 1
    print(f"q=11, c={c}: projectivities mapping our cadical witness onto Seceleanu's 21 Klein quadruple points: {cnt}")
