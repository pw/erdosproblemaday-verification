"""Seat G toy checks of the slab cap (Blinov patch, Lemma aux:cap / aux:random-set) at small odd primes q.

Checks, for random allowed shifts a and random G in GL3(F_q):
  (1) |S| = wq, S has no three collinear points (cap), V = G(a+S) has |S| points and 0 not in V;
  (2) no relation x1 u1 + x2 u2 + x3 u3 = 0 (x != 0 integer, |x| <= H) with u_i in V, unless
      sum(x) = 0 and the three columns are NOT affinely independent  (Lemma aux:random-set);
  (3) every line through the origin meets V in <= 2 points (used for the sharpened proportional-pair bound).
Toy constants: the lemma's proof only needs 3H < q and 3Hw < q/2 (the 1000/2000 constants only feed the
probability bound |A| >= q^3/2), so we take w with 3Hw < q/2.
Mutations (argv[1]):  square_nu  -> Q isotropic, cap must FAIL;
                      slab2      -> slab on coordinate 2 instead of 1, relation check must FAIL;
                      badshift   -> a1 not allowed, relation/zero check must FAIL.
"""
import sys, random, itertools

MUT = sys.argv[1] if len(sys.argv) > 1 else None
random.seed(20261022)

def is_square(t, q):
    return t % q == 0 or pow(t, (q - 1) // 2, q) == 1

def rand_gl3(q):
    while True:
        G = [[random.randrange(q) for _ in range(3)] for _ in range(3)]
        det = (G[0][0] * (G[1][1] * G[2][2] - G[1][2] * G[2][1])
               - G[0][1] * (G[1][0] * G[2][2] - G[1][2] * G[2][0])
               + G[0][2] * (G[1][0] * G[2][1] - G[1][1] * G[2][0])) % q
        if det:
            return G

def apply(G, v, q):
    return tuple(sum(G[i][j] * v[j] for j in range(3)) % q for i in range(3))

def norm_q(t, q):
    t %= q
    return min(t, q - t)

def projective(v, q):
    for c in v:
        if c:
            inv = pow(c, q - 2, q)
            return tuple(x * inv % q for x in v)
    return None

def run(q, H, w):
    nu = next(t for t in range(2, q) if not is_square(t, q))
    if MUT == "square_nu":
        nu = 4 % q  # a square: x^2 - 4 y^2 = (x-2y)(x+2y) isotropic
    Q = lambda x, y: (x * x - nu * y * y) % q
    if MUT == "slab2":
        S = [(x, y, Q(x, y)) for y in range(w) for x in range(q)]
    else:
        S = [(x, y, Q(x, y)) for x in range(w) for y in range(q)]
    assert len(set(S)) == w * q, "slab size"
    # (1) cap property of S: from each point, directions to other points must be pairwise distinct
    for p in S:
        seen = set()
        for o in S:
            if o == p:
                continue
            dvec = projective(tuple((o[i] - p[i]) % q for i in range(3)), q)
            assert dvec not in seen, f"three collinear points in S (q={q})"
            seen.add(dvec)
    # allowed shifts on coordinate 1
    allowed1 = [t for t in range(q) if all(norm_q(m * t, q) > 3 * H * w for m in range(1, 3 * H + 1))]
    assert allowed1, "no allowed shift"
    xs = [x for x in itertools.product(range(-H, H + 1), repeat=3)
          if any(x) and x[0] ** 2 + x[1] ** 2 + x[2] ** 2 <= H * H]
    for trial in range(1):
        a1 = random.choice(allowed1)
        if MUT == "badshift":
            a1 = (q - 1) % q  # -1: a1 + v1 = 0 for v1 = 1 < w
        a = (a1, random.randrange(q), random.randrange(q))
        if MUT == "slab2":
            a = (a1, 0, random.randrange(q))   # coord 2 carries the slab but is not shift-protected
        G = rand_gl3(q)
        V = [apply(G, tuple((a[i] + v[i]) % q for i in range(3)), q) for v in S]
        Vset = set(V)
        assert len(Vset) == len(S), "|V| != |S|"
        assert (0, 0, 0) not in Vset, "0 in V"
        # (3) lines through the origin
        cnt = {}
        for v in V:
            pv = projective(v, q)
            cnt[pv] = cnt.get(pv, 0) + 1
        assert max(cnt.values()) <= 2, "line through origin meets V in >= 3 points"
        # (2) short relations
        for u1 in V:
            for u2 in V:
                for x in xs:
                    x1, x2, x3 = x
                    if x3 % q == 0:
                        lhs = tuple((x1 * u1[i] + x2 * u2[i]) % q for i in range(3))
                        if lhs == (0, 0, 0):
                            # relation holds for every u3; lemma: impossible if x1+x2 != 0
                            assert x1 + x2 == 0 and u1 == u2, f"short relation x={x} (two columns)"
                        continue
                    inv = pow(-x3 % q, q - 2, q)
                    u3 = tuple((x1 * u1[i] + x2 * u2[i]) * inv % q for i in range(3))
                    if u3 in Vset:
                        msum = x1 + x2 + x3
                        assert msum == 0, f"short relation with nonzero sum, x={x}"
                        d1 = tuple((u2[i] - u1[i]) % q for i in range(3))
                        d2 = tuple((u3[i] - u1[i]) % q for i in range(3))
                        cross = ((d1[1] * d2[2] - d1[2] * d2[1]) % q, (d1[2] * d2[0] - d1[0] * d2[2]) % q,
                                 (d1[0] * d2[1] - d1[1] * d2[0]) % q)
                        assert cross == (0, 0, 0), f"short relation among affinely independent columns x={x}"
    return len(S)

def cap_only(q, w):
    # for w <= 2 the slab is a cap for ANY quadratic Q (a line with v1 != 0 meets <= w slab layers), so the
    # cap check inside run() is vacuous there; this sweep uses w >= 3 so the square_nu mutation can fail.
    nu = next(t for t in range(2, q) if not is_square(t, q))
    if MUT == "square_nu":
        nu = 4 % q
    S = [(x, y, (x * x - nu * y * y) % q) for x in range(w) for y in range(q)]
    for p in S:
        seen = set()
        for o in S:
            if o != p:
                dvec = projective(tuple((o[i] - p[i]) % q for i in range(3)), q)
                assert dvec not in seen, f"three collinear points in S (q={q}, w={w})"
                seen.add(dvec)

for (q, w) in ((31, 31), (101, 3), (101, 10), (103, 7), (127, 5)):
    cap_only(q, w)
print("cap-only sweep passed")

total = 0
for (q, H, w) in ((307, 2, 4), (401, 2, 2)):
    assert 3 * H < q and 2 * 3 * H * w < q and 3 * H * (6 * H * w + 1) < q
    total += run(q, H, w)
print("ALL TOY CAP CHECKS PASSED" + (f" (mutation {MUT} NOT detected!)" if MUT else ""), total)
