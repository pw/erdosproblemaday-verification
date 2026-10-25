#!/usr/bin/env python3
"""Finite check of the planar cover obstruction (paper Lemma 7.5 / Lean
PlanarCover.compact_open_cover_impossible) on discretised domains.

Discrete model (exact, integer arithmetic):
  domain = finite union of closed grid cells of side h (cell (i,j) = [i h,(i+1) h] x [j h,(j+1) h]);
  a "cover" = partition of the cells into pieces; each piece is the CLOSED union of its cells.
  multiplicity at a point = number of pieces containing it; only grid vertices can see >2 cells,
  so multiplicity <= m everywhere  <=>  every grid vertex sees <= m distinct pieces among its incident cells.
  mesh = max piece diameter; diameter of a union of closed squares = max corner-to-corner distance
  over pairs of its cells (exact, squared, in units of h).
A finite closed cover of order <= 2 and mesh <= D swells to an open cover of order <= 2 and mesh <= D+eta,
so whenever the domain contains a disk of radius > D the lemma predicts UNSAT for (m=2, D).
Conversely every open cover with mesh <= D and multiplicity <= 2 induces such a cell partition once h is
below its Lebesgue number (cell -> any member containing it), so the discrete problem is the faithful
finite shadow of the lemma.

Encoding: canonical representative form (no symmetry): r[c][d] = "cell c lies in the piece whose
minimum-index cell is d"; only d <= c with diam(c u d) <= D are candidates.
"""
import itertools, sys, time, threading, math
from pysat.solvers import Solver
from pysat.formula import IDPool

def corners(c):
    i, j = c
    return [(i, j), (i+1, j), (i, j+1), (i+1, j+1)]

def diam2(c, d):            # squared diameter of the union of closed cells c, d (units of h)
    return max((a[0]-b[0])**2 + (a[1]-b[1])**2 for a in corners(c) for b in corners(d))

def vertex_cells(cells):
    S = set(cells); V = {}
    for c in cells:
        for v in corners(c):
            V.setdefault(v, []).append(c)
    return V

def check_cover(cells, piece, D2, m):
    """Independent checker. piece: dict cell -> piece label. Returns list of violations."""
    bad = []
    for v, inc in vertex_cells(cells).items():
        k = len({piece[c] for c in inc})
        if k > m: bad.append(('multiplicity', v, k))
    groups = {}
    for c in cells: groups.setdefault(piece[c], []).append(c)
    for p, mem in groups.items():
        dm = max(diam2(a, b) for a in mem for b in mem)
        if dm > D2: bad.append(('diameter', p, math.sqrt(dm)))
    return bad

def encode(cells, D2, m):
    cells = sorted(cells); idx = {c: k for k, c in enumerate(cells)}
    pool = IDPool(); cl = []
    cand = {c: [d for d in cells if idx[d] <= idx[c] and diam2(c, d) <= D2] for c in cells}
    r = lambda c, d: pool.id(('r', c, d))
    for c in cells:
        lits = [r(c, d) for d in cand[c]]
        cl.append(lits)                                     # at least one representative
        for a, b in itertools.combinations(lits, 2): cl.append([-a, -b])   # at most one
        for d in cand[c]:
            if d != c: cl.append([-r(c, d), r(d, d)])       # representative represents itself
    members = {}
    for c in cells:
        for d in cand[c]: members.setdefault(d, []).append(c)
    for d, mem in members.items():                          # piece diameter <= D
        for a, b in itertools.combinations(mem, 2):
            if diam2(a, b) > D2: cl.append([-r(a, d), -r(b, d)])
    def eq(a, b):                                           # eq(a,b) -> same piece
        if idx[a] > idx[b]: a, b = b, a
        e = pool.id(('eq', a, b))
        if ('done', a, b) not in done:
            done.add(('done', a, b))
            common = [d for d in cand[a] if d in cand[b]]
            ys = []
            for d in common:
                y = pool.id(('y', a, b, d)); ys.append(y)
                cl.append([-y, r(a, d)]); cl.append([-y, r(b, d)])
            cl.append([-e] + ys)
        return e
    done = set()
    for v, inc in vertex_cells(cells).items():
        if len(inc) > m:                                    # among any m+1 incident cells two share a piece
            for sub in itertools.combinations(inc, m+1):
                cl.append([eq(a, b) for a, b in itertools.combinations(sub, 2)])
    return cells, cand, r, pool, cl

def solve(cells, D2, m, assume_piece=None, timeout=50, name='glucose4'):
    cells, cand, r, pool, cl = encode(cells, D2, m)
    assum = []
    if assume_piece is not None:      # force a given partition (canonical rep = min index cell)
        idx = {c: k for k, c in enumerate(cells)}
        rep = {}
        for c in cells:
            p = assume_piece[c]
            if p not in rep or idx[c] < idx[rep[p]]: rep[p] = c
        for c in cells:
            d = rep[assume_piece[c]]
            if d not in cand[c]: return 'UNSAT(assumption outside candidate set: piece too wide)', None, len(cl)
            assum.append(r(c, d))
    s = Solver(name=name, bootstrap_with=cl)
    timer = threading.Timer(timeout, s.interrupt); timer.start()
    t0 = time.time()
    res = s.solve_limited(assumptions=assum, expect_interrupt=True)
    timer.cancel()
    model = s.get_model() if res else None
    s.delete()
    if res is None: return 'TIMEOUT', None, len(cl)
    if not res: return 'UNSAT', None, len(cl)
    ms = set(l for l in model if l > 0); piece = {}
    for c in cells:
        ds = [d for d in cand[c] if r(c, d) in ms]; assert len(ds) == 1; piece[c] = ds[0]
    return 'SAT', piece, len(cl)

def disk_cells(R, h):          # cells fully inside the closed disk of radius R centred at the origin (a grid vertex)
    n = int(R/h) + 2
    return [(i, j) for i in range(-n, n) for j in range(-n, n)
            if all((x*h)**2 + (y*h)**2 <= R*R + 1e-12 for x, y in corners((i, j)))]

def rect_cells(W, H, h):
    return [(i, j) for i in range(round(W/h)) for j in range(round(H/h))]

def inradius_at_origin(cells, h):  # distance from origin to the complement of the union of cells
    S = set(cells); best = float('inf')
    for c in cells:
        i, j = c
        for (di, dj), seg in [((1,0), ((i+1,j),(i+1,j+1))), ((-1,0), ((i,j),(i,j+1))),
                              ((0,1), ((i,j+1),(i+1,j+1))), ((0,-1), ((i,j),(i+1,j)))]:
            if (i+di, j+dj) not in S:
                (x1,y1),(x2,y2) = seg
                # distance from origin to segment (axis parallel)
                xs = sorted([x1,x2]); ys = sorted([y1,y2])
                px = min(max(0, xs[0]), xs[1]); py = min(max(0, ys[0]), ys[1])
                best = min(best, math.hypot(px*h, py*h))
    return best

if __name__ == '__main__':
    part = sys.argv[1]
    TO = float(sys.argv[2]) if len(sys.argv) > 2 else 50
    solver_name = sys.argv[3] if len(sys.argv) > 3 else 'glucose4'
    def run(label, cells, h, m, D=2.0, assume=None, expect=None):
        D2 = round((D/h)**2)
        t0 = time.time()
        res, piece, ncl = solve(cells, D2, m, assume, timeout=TO, name=solver_name)
        line = f"{label}: cells={len(cells)} h={h} m<={m} mesh<={D} clauses={ncl} -> {res} ({time.time()-t0:.1f}s)"
        if piece is not None:
            viol = check_cover(cells, piece, D2, m)
            line += f"  pieces={len(set(piece.values()))} independent-checker violations={len(viol)}"
        if expect is not None: line += f"  [expected {expect}: {'OK' if res.startswith(expect) else 'MISMATCH'}]"
        print(line, flush=True)
        return piece
    if part == 'main':
        for (R, h) in [(3.0, 0.5)]:
            cells = disk_cells(R, h)
            print(f"disk R={R} h={h}: union of cells contains the disk of radius {inradius_at_origin(cells,h):.3f} about the origin")
            run(f"  MAIN   disk R={R}", cells, h, 2, expect='UNSAT')
            run(f"  CTRL-a disk R={R}, multiplicity<=3 allowed", cells, h, 3, expect='SAT')
            run(f"  CTRL-f disk R={R}, m<=2 but mesh<=2.4 (inradius 2.5 > 2.4: lemma still predicts UNSAT)", cells, h, 2, D=2.4, expect='UNSAT')
        h = 0.5
        strip = rect_cells(6.0, 1.5, h)
        run("  CTRL-b thin rectangle 6 x 1.5 (no disk of radius >2 inside)", strip, h, 2, expect='SAT')
        slabs = {c: c[0] // 2 for c in strip}
        print("  witness slabs on strip: checker violations (m<=2):", check_cover(strip, slabs, 16, 2))
        run("  CTRL-c strip + forced slab witness", strip, h, 2, assume=slabs, expect='SAT')
        cells = disk_cells(3.0, 0.5)
        brick = {c: (c[1] // 2, (c[0] + (c[1]//2) % 2) // 3) for c in cells}   # 1.5 x 1.0 bricks, rows offset by one cell
        vb2 = check_cover(cells, brick, 16, 2); vb3 = check_cover(cells, brick, 16, 3)
        print(f"  witness brick wall on disk: checker m<=2 violations={len(vb2)} (e.g. {vb2[:2]}), m<=3 violations={len(vb3)}")
        run("  CTRL-d disk + forced brick witness, m<=3", cells, h, 3, assume=brick, expect='SAT')
        run("  CTRL-e disk + forced brick witness, m<=2 (must reject: T-junctions)", cells, h, 2, assume=brick, expect='UNSAT')
        one = {c: 0 for c in cells}
        print("  checker negative control (whole disk as one piece):", check_cover(cells, one, 16, 2)[:1])
    elif part == 'fine':
        cells = disk_cells(2.75, 0.25)
        print(f"disk R=2.75 h=0.25: inradius {inradius_at_origin(cells,0.25):.3f}", flush=True)
        run("  MAIN-fine disk R=2.75", cells, 0.25, 2, expect='UNSAT')
    elif part == 'mid':
        h = 1/3
        for R in [2.6]:
            cells = disk_cells(R, h)
            print(f"disk R={R} h=1/3: inradius {inradius_at_origin(cells,h):.3f}", flush=True)
            run(f"  MAIN-mid disk R={R}", cells, h, 2, expect='UNSAT')
            run(f"  CTRL-a-mid disk R={R}, m<=3", cells, h, 3, expect='SAT')
    elif part == 'sweepR':
        for R in [1.25, 1.5, 1.75, 2.0, 2.25, 2.5]:
            cells = disk_cells(R, 0.5)
            run(f"  SWEEP-R disk R={R} (inradius {inradius_at_origin(cells,0.5):.3f}), mesh<=2", cells, 0.5, 2)
    elif part == 'sweepD':
        cells = disk_cells(3.0, 0.5)
        for D in [2.5, 3.0, 3.5, 4.0, 5.0]:
            run(f"  SWEEP-D disk R=3 (inradius 2.5), m<=2, mesh<={D}", cells, 0.5, 2, D=D)
