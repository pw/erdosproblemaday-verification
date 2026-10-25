# Exhaustive check of the strict-cross geometry used in Prop 6.3 / 6.5 ((6.4), (6.5), Figure 2,
# the branch claims), over a 5x5 label grid plus one unseen label per coordinate.
import itertools
L = list(range(5)) + ['u']                      # 'u' = a label carried by no point
POINT = [(a, b) for a in range(5) for b in range(5)]
CENTER = [(a, b) for a in L for b in L]
def R(y): return {x for x in POINT if (x[0] == y[0]) != (x[1] == y[1])}
def bit(x, y):                                  # consistent bit, or None if inconsistent
    if x[0] == y[0] and x[1] != y[1]: return 1
    if x[1] == y[1] and x[0] != y[0]: return 0
    return None
def N(o1, o2, b):                               # nonshared-coordinate match of opposite endpoints
    return o1[1] == o2[1] if b == 1 else o1[0] == o2[0]

errs = []
# (6.4): two states in one row
for (a, b, b2) in itertools.product(L, L, L):
    if b == b2: continue
    I = R((a, b)) & R((a, b2))
    if I != {x for x in POINT if x[0] == a and x[1] not in (b, b2)}: errs.append(('6.4', a, b, b2))
    for y3 in CENTER:                            # third state outside the row
        if y3[0] != a and len(I & R(y3)) > 1: errs.append(('third', a, b, b2, y3))
# (6.5) and three pairwise-distinct states
for y1, y2 in itertools.product(CENTER, CENTER):
    if y1[0] == y2[0] or y1[1] == y2[1]: continue
    I = R(y1) & R(y2)
    exp = {x for x in [(y1[0], y2[1]), (y2[0], y1[1])] if x in POINT}
    if I != exp: errs.append(('6.5', y1, y2))
    for y3 in CENTER:
        if len({y1[0], y2[0], y3[0]}) == 3 and len({y1[1], y2[1], y3[1]}) == 3 and I & R(y3):
            errs.append(('three', y1, y2, y3))
    # Figure 2: with point states in I and centre states in {y1,y2}, equal bits force N at either base
    for base in (y1, y2):                        # centre base
        for x1, x2 in itertools.product(I, I):
            b1, b2 = bit(x1, base), bit(x2, base)
            if b1 is not None and b1 == b2 and not N(x1, x2, b1): errs.append(('fig2-centre', y1, y2))
    for base in I:                               # point base
        for c1, c2 in itertools.product((y1, y2), (y1, y2)):
            b1, b2 = bit(base, c1), bit(base, c2)
            if b1 is not None and b1 == b2 and not N(c1, c2, b1): errs.append(('fig2-point', y1, y2))
# row case: point in row a, centre in row a  =>  any consistent edge has bit 1
for a in L:
    for x in POINT:
        for y in CENTER:
            if x[0] == a and y[0] == a and bit(x, y) not in (None, 1): errs.append(('row-bit', x, y))
# singleton case at a point base: same centre state => equal bits and N
for x in POINT:
    for y in CENTER:
        b = bit(x, y)
        if b is not None and not N(y, y, b): errs.append(('singleton', x, y))
print("errors in paper's claims:", len(errs), errs[:3])

# CONTROL: if the point states were only known to lie in R(y1) UNION R(y2) (no intersection /
# no transfer), equal bits at a centre base would NOT force the nonshared-coordinate match.
ctrl = 0
y1, y2 = (0, 0), (1, 1)
U = R(y1) | R(y2)
for base in (y1, y2):
    for x1, x2 in itertools.product(U, U):
        b1, b2 = bit(x1, base), bit(x2, base)
        if b1 is not None and b1 == b2 and not N(x1, x2, b1): ctrl += 1
print("CONTROL (union instead of intersection): violating pairs =", ctrl, "(must be > 0)")

# tau bounds in Prop 6.5 (random measures meeting each case's hypothesis); control = a false bound
import random
random.seed(65)
def tau(nu):
    A, B = {}, {}
    for (a, b), w in nu.items(): A[a] = A.get(a, 0) + w; B[b] = B.get(b, 0) + w
    return sum(v * v for v in A.values()) + sum(v * v for v in B.values()) - 1
def mass(nu, S): return sum(w for x, w in nu.items() if x in S)
def rand_nu(conc_on, z):
    nu = {x: random.random() * z / 25 for x in POINT}
    s = sum(nu.values()); nu = {x: w * z / s for x, w in nu.items()}  # z spread everywhere
    # remaining 1-z spread over conc_on at random proportions
    ws = [random.random() for _ in conc_on]; t = sum(ws)
    for x, w in zip(conc_on, ws): nu[x] = nu.get(x, 0) + (1 - z) * w / t
    return nu
bad = {'single': 0, 'row': 0, 'third': 0, 'corner': 0, 'CTRL single>=-4z': 0}
for _ in range(20000):
    z = random.choice([1e-4, 1e-3, 1e-2, 0.05])
    y = (0, 0)
    nu = rand_nu(sorted(R(y)), z)                  # nu(R_y) >= 1 - z
    if tau(nu) < -0.5 - z - 1e-12: bad['single'] += 1
    if tau(nu) < -4 * z: bad['CTRL single>=-4z'] += 1
    I = R((0, 0)) & R((0, 1)); nu = rand_nu(sorted(I), 2 * z)
    if tau(nu) < -4 * z - 1e-12: bad['row'] += 1
    I3 = I & R((2, 3)); nu = rand_nu(sorted(I3), 3 * z)
    if tau(nu) < 1 - 12 * z - 1e-12: bad['third'] += 1
    Ic = R((0, 0)) & R((1, 1)); nu = rand_nu(sorted(Ic), 2 * z)
    if tau(nu) < -4 * z - 1e-12: bad['corner'] += 1
print("tau-bound violations (paper's four bounds must be 0; CONTROL must be > 0):", bad)
