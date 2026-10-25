#!/usr/bin/env python3
"""EXACT verification of a config188 core (sympy, no floating point in any decision):
  * every point is rebuilt exactly from its provenance (lattice coords (a,b) in Z[w] and the word of
    rotations that produced it; rotation about a lattice point c by the angle with 2 d sin(th/2)=1,
    cos th = 1 - 1/(2 d^2), sin th = sqrt(4 d^2 - 1)/(2 d^2));
  * every pair clause is checked to be a pair at distance EXACTLY 1;
  * every run clause is checked to be collinear, unit-spaced, in order;
  * the core is re-solved as a propositional formula by a second solver (minisat22) -> must be UNSAT;
  * negative controls: dropping any single clause of the core -> SAT (minimality), and perturbing a
    point's lattice coordinate must break its pair's unit-distance check.
Prints a PASS/FAIL summary; exit 0 only on PASS."""
import sys, json
import sympy as sp
from pysat.solvers import Solver

W_RE, W_IM = sp.Rational(-1, 2), sp.sqrt(3)/2   # w = e^{2 pi i/3}

def lattice_pt(a, b):
    return sp.Matrix([a + b*W_RE, b*W_IM])

def rot_about(center, d, sign):
    d = sp.nsimplify(d) if not isinstance(d, sp.Basic) else d
    c = 1 - 1/(2*d**2)
    s = sign*sp.sqrt(4*d**2 - 1)/(2*d**2)
    Rm = sp.Matrix([[c, -s], [s, c]])
    cen = sp.Matrix(center)
    return lambda z: cen + Rm*(z - cen)

def exact_d(dfloat):
    # recover the exact d from its float: we only use d in {sqrt(N)} or integers; try N = round(d^2)
    N = round(dfloat*dfloat)
    assert abs(dfloat*dfloat - N) < 1e-9, dfloat
    return sp.sqrt(N)

def main(path):
    core = json.load(open(path))
    gen_desc = core["gen_desc"]; iso_words = core["iso_words"]
    isos_f = core["isos"]
    # build exact isometries as functions
    def exact_iso(word):
        fs = []
        for gi in word:            # word is [h_last, ..., h_first] : k = h o g  => apply rightmost first
            cen, d, sign = gen_desc[gi]
            # centre is a lattice point given as floats; recover (a,b): b = 2y/sqrt3, a = x + b/2
            b = round(cen[1]/float(sp.sqrt(3))*2); a = round(cen[0] + b/2)
            assert abs(cen[0]-(a-b/2)) < 1e-9 and abs(cen[1]-b*float(sp.sqrt(3))/2) < 1e-9
            fs.append(rot_about(lattice_pt(a, b), exact_d(d), sign))
        def f(z):
            for g in reversed(fs): z = g(z)
            return z
        return f
    pts = {}
    for i, (gi, a, b) in core["tags"].items():
        f = exact_iso(iso_words[gi])
        z = f(lattice_pt(a, b))
        pts[int(i)] = sp.simplify(z)
        # cross-check against the float used in the search
        zf = [float(z[0]), float(z[1])]
        assert abs(zf[0]-core["points"][i][0]) < 1e-7 and abs(zf[1]-core["points"][i][1]) < 1e-7, (i, zf, core["points"][i])
    ok = True
    # pairs
    for (i, j) in core["pairs"]:
        d2 = sp.simplify(((pts[i]-pts[j]).T*(pts[i]-pts[j]))[0])
        if sp.simplify(d2 - 1) != 0:
            print("FAIL pair", i, j, d2); ok = False
    print(f"pairs exact-unit: {len(core['pairs'])} checked")
    # runs (G5a: every run clause must have exactly k literals)
    for ch in core["runs"]:
        if len(ch) != core["k"]:
            print("FAIL run clause has", len(ch), "literals, expected k =", core["k"], ch); ok = False
        u = pts[ch[1]] - pts[ch[0]]
        if sp.simplify((u.T*u)[0] - 1) != 0:
            print("FAIL run step not unit", ch); ok = False
        for t in range(2, len(ch)):
            if sp.simplify(pts[ch[t]] - pts[ch[t-1]] - u) != sp.zeros(2, 1):
                print("FAIL run not unit-spaced collinear", ch, t); ok = False
    print(f"runs exact (collinear, unit-spaced, length {core['k']}): {len(core['runs'])} checked")
    # units: a positive unit must be the origin (red, WLOG by translation); a negative unit (blue, WLOG by a
    # rotation about the red origin) must be a base-lattice point whose theta_d partner is at distance exactly 1,
    # i.e. any lattice point P with |P| = d where 2 d sin(theta_d/2) = 1 -- true for every d>1/2, so we only check
    # that P is a base-lattice point with |P|^2 a norm in Z[w] and |P| > 1/2 (so the partner exists).
    nblue = 0
    for (v,) in core["units"]:
        if v >= 0:
            if sp.simplify(pts[v]) != sp.zeros(2, 1):
                print("FAIL positive unit clause not the origin", v); ok = False
        else:
            i = -v - 1   # stored as -(index+1)
            nblue += 1
            z = pts[i]
            # exact test that the point is an Eisenstein integer a + b w (its provenance word may be a rotation about itself)
            bq = sp.nsimplify(2*z[1]/sp.sqrt(3)); aq = sp.nsimplify(z[0] + z[1]/sp.sqrt(3))
            if not (aq.is_integer and bq.is_integer):
                print("FAIL blue WLOG point is not a lattice point", i, z); ok = False
            else:
                a, b = int(aq), int(bq)
                d2 = a*a - a*b + b*b   # |a + b w|^2 for w = e^{2 pi i/3}
                if d2 == 0:
                    print("FAIL blue WLOG point is the origin", i); ok = False
                print(f"blue WLOG point: lattice point ({a},{b}) = {tuple(z)}, |P|^2 = {d2} (W2 applies for any |P| > 1/2: its theta_|P| partner is at distance exactly 1)")
    if nblue > 1:
        print("FAIL more than one blue WLOG assumption (only one rotation freedom)"); ok = False
    # G5b: the geometrically checked clauses must be EXACTLY the propositional core (as a multiset)
    cl = core["core_clauses"]
    geo = [sorted([-(i+1), -(j+1)]) for (i, j) in core["pairs"]] + [sorted(v+1 for v in ch) for ch in core["runs"]] \
        + [[(v+1 if v >= 0 else v)] for (v,) in core["units"]]
    if sorted(map(tuple, geo)) != sorted(tuple(sorted(c)) for c in cl):
        print("FAIL geometric clause set != core_clauses (coverage gap)"); ok = False
    else:
        print(f"coverage: all {len(cl)} core clauses were geometrically checked")
    # propositional re-check with a second solver
    with Solver(name='minisat22', bootstrap_with=cl) as S:
        r = S.solve()
    print("minisat22 on core:", "UNSAT" if r is False else "SAT")
    ok = ok and (r is False)
    # minimality: every single-clause deletion is SAT
    nmin = 0
    for t in range(len(cl)):
        with Solver(name='minisat22', bootstrap_with=cl[:t]+cl[t+1:]) as S:
            if S.solve() is True: nmin += 1
    print(f"minimality: {nmin}/{len(cl)} single deletions SAT")
    ok = ok and nmin == len(cl)
    # negative controls on the exact checker: (i) rebuild EVERY rotated point with the WRONG angle (d^2 -> d^2+1)
    # and require that at least one pair clause then fails the unit test (pairs whose other point is the rotation centre
    # stay unit under any angle, so the control counts failures over all pairs); (ii) a corrupted run must fail.
    def rebuild_wrong(i):
        gi, a, b = core["tags"][str(i)]
        fs = []
        for h in iso_words[gi]:
            cen, d, sign = gen_desc[h]
            bb = round(cen[1]/float(sp.sqrt(3))*2); aa = round(cen[0] + bb/2)
            fs.append(rot_about(lattice_pt(aa, bb), sp.sqrt(round(d*d) + 1), sign))
        z = lattice_pt(a, b)
        for g in reversed(fs): z = g(z)
        return z
    wrong = {i: rebuild_wrong(i) for i in pts}
    nfail = sum(1 for (i, j) in core["pairs"] if sp.simplify(((wrong[i]-wrong[j]).T*(wrong[i]-wrong[j]))[0] - 1) != 0)
    print(f"negative control (i): with the wrong rotation angle {nfail}/{len(core['pairs'])} pair clauses fail the unit test (need >= 1)")
    ctrl_ok = nfail >= 1
    ch = core["runs"][0]
    bad = [pts[v] for v in ch]; bad[-1] = bad[-1] + lattice_pt(1, 0)
    u = bad[1] - bad[0]
    still_run = all(sp.simplify(bad[t] - bad[t-1] - u) == sp.zeros(2, 1) for t in range(2, len(bad)))
    print("negative control (ii): corrupted run still reads as a run?", still_run)
    ctrl_ok = ctrl_ok and not still_run
    ok = ok and ctrl_ok
    print("RESULT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
