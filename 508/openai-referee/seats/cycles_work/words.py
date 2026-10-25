#!/usr/bin/env python3
"""Exhaustive finite checks for Prop 8.2 (five-cycle), Lemma 8.3 (six-position words), Prop 8.5's
word step, plus the generalised one-orbit sign/palette model used for test (B). Controls included."""
import itertools, sys
fails = []
def chk(c, m):
    print(("  ok   " if c else "  FAIL ") + m)
    if not c: fails.append(m)

# ---------- One-orbit model (raw constraints, NOT the paper's derived index arithmetic) ----------
def orbit_model(k, ell, pmax=2, use_57=True, antipodal=True):
    """labels 0..k-1; cycle 0..ell-1 with edge j = {j, j+1 mod ell}; outsiders ell..k-1.
    Six orbit positions; signs s_j in {+1,-1}^ell with s_{j+3} = -s_j (antipodal) ;
    O = labels with no incident positive edge, I = labels with no incident negative edge (outsiders in both);
    palette P_j: 1<=|P_j|<=pmax, P_j meets O_j and I_j ((8.1)); P_j, P_{j+1} disjoint ((5.7)).
    Returns list of satisfying (signs, palettes) witnesses (first few) and count of sign triples with a solution."""
    labels = range(k)
    inc = {i: [j for j in range(ell) if i in (j, (j+1) % ell)] for i in labels}
    pals = [frozenset(c) for r in range(1, pmax+1) for c in itertools.combinations(labels, r)]
    def OI(s):
        O = {i for i in labels if all(s[j] < 0 for j in inc[i])}
        I = {i for i in labels if all(s[j] > 0 for j in inc[i])}
        return O, I
    signs = list(itertools.product((1, -1), repeat=ell))
    sat_triples, witness = 0, None
    for s0, s1, s2 in itertools.product(signs, repeat=3):
        if antipodal:
            S = [s0, s1, s2, tuple(-x for x in s0), tuple(-x for x in s1), tuple(-x for x in s2)]
        else:
            S = [s0, s1, s2, s0, s1, s2]
        cand = []
        for s in S:
            O, I = OI(s)
            cand.append([p for p in pals if p & O and p & I])
        if any(not c for c in cand):
            continue
        # cycle search over 6 positions
        found = None
        for p0 in cand[0]:
            frontier = {p0: [p0]}
            for j in range(1, 6):
                nf = {}
                for prev, path in frontier.items():
                    for q in cand[j]:
                        if (not use_57) or not (q & prev):
                            if q not in nf: nf[q] = path + [q]
                frontier = nf
            for last, path in frontier.items():
                if (not use_57) or not (last & p0):
                    found = path; break
            if found: break
        if found:
            sat_triples += 1
            if witness is None: witness = (S, found)
    return sat_triples, witness

print("== Prop 8.2: five-cycle, five labels, |P|<=2, (8.1), (5.7), antipodal sign reversal")
n, w = orbit_model(5, 5)
chk(n == 0, f"k=5, ell=5: sign triples admitting a consistent orbit = {n} (paper: none)")
print("   controls (the solver CAN say SAT):")
n, w = orbit_model(5, 5, use_57=False)
chk(n > 0, f"  drop (5.7): {n} sign triples admit an orbit (expected >0)")
n, w = orbit_model(5, 5, pmax=5)
print(f"   OBSERVATION (not a control): allowing any palette size (no Prop 5.6) still gives {n} -- the constraints are"
      " monotone (a sub-palette of a solution is a solution), so (5.12) is not needed in Prop 8.2")
# control: signs at the six positions chosen independently (no antipodal relation at all). Since each position may
# then use ANY sign pattern, the admissible palettes per position are the union over all patterns:
def union_pals(k, ell, pmax=2):
    labels = range(k); inc = {i: [j for j in range(ell) if i in (j, (j+1) % ell)] for i in labels}
    out = set()
    for s in itertools.product((1, -1), repeat=ell):
        O = {i for i in labels if all(s[j] < 0 for j in inc[i])}; I = {i for i in labels if all(s[j] > 0 for j in inc[i])}
        out |= {frozenset(c) for r in range(1, pmax+1) for c in itertools.combinations(labels, r) if set(c) & O and set(c) & I}
    return sorted(out, key=sorted)
UP = union_pals(5, 5)
cyc = [p for p in itertools.product(UP, repeat=6) if all(not (p[j] & p[(j+1) % 6]) for j in range(6))]
chk(len(cyc) > 0, f"  independent signs at the six positions: {len(cyc)} consistent palette cycles, e.g. {[sorted(x) for x in cyc[0]]} (expected >0)")
print("   test (B): same one-orbit model for other (k, ell):")
for k, ell in [(5, 4), (5, 3), (6, 6), (6, 5), (6, 4), (6, 3)]:
    n, w = orbit_model(k, ell)
    print(f"     k={k}, ell={ell}: sign triples admitting an orbit = {n}" +
          (f"; e.g. palettes {[sorted(p) for p in w[1]]}" if w else ""))

# ---------- Lemma 8.3 / Prop 8.5 words ----------
X, U, V = "X", "U", "V"
Z6 = range(6)
def valid(w, antip=True):
    if any(w[j] == w[(j+1) % 6] for j in Z6): return False          # p(e) != p(Re)
    if antip and any(w[j] != X and w[(j+3) % 6] != X and w[j] != w[(j+3) % 6] for j in Z6): return False
    return True
def cross(w, v):   # a diagonal at any position of w cannot equal a diagonal at an adjacent position of v (and vice versa)
    for j in Z6:
        for d in (1, -1):
            a, b = w[j], v[(j+d) % 6]
            if a != X and b != X and a == b: return False
            a, b = v[j], w[(j+d) % 6]
            if a != X and b != X and a == b: return False
    return True
words = ["".join(t) for t in itertools.product("XUV", repeat=6)]
VW = [w for w in words if valid(w)]
print(f"== Lemma 8.3: {len(VW)} valid words (adjacent inequality + antipodal equality) out of 729")
chk(all(X in w for w in VW), "every valid word contains X")
mixed = [w for w in VW if {j % 2 for j in Z6 if w[j] == X} == {0, 1}]
perm3 = [w for w in VW if w[:3] == w[3:] and set(w[:3]) == {X, U, V}]
chk(set(mixed) == set(perm3), f"mixed-parity words = three-periodic permutation words: {sorted(mixed)}")
chk(all(w.count(X) == 2 for w in mixed), "mixed-parity words have exactly two X, antipodal")
for w in mixed:
    comp = [v for v in VW if cross(w, v)]
    chk(comp == [w], f"isolation of {w}: compatible valid words = {comp}")
    chk(w[1:] + w[:1] != w, f"{w} != its one-position shift {w[1:] + w[:1]}")
single = [w for w in VW if w not in mixed]
for w in single:
    par = {j % 2 for j in Z6 if w[j] == X}
    oth = [j for j in Z6 if j % 2 not in par]
    assert len(par) == 1 and all(w[j] != X for j in oth)
chk(True, f"{len(single)} single-parity valid words; their other-parity positions are all non-X")
print("== Prop 8.5 word step: cross-compatible valid words with different X-parity")
bad = 0; pairs = 0
for w in single:
    for v in single:
        hw = {j % 2 for j in Z6 if w[j] == X}; hv = {j % 2 for j in Z6 if v[j] == X}
        if hw != hv and cross(w, v):
            pairs += 1
            sw = {w[j] for j in Z6 if j % 2 not in hw}; sv = {v[j] for j in Z6 if j % 2 not in hv}
            if not (len(sw) == 1 and len(sv) == 1 and sw != sv): bad += 1
chk(pairs > 0 and bad == 0, f"{pairs} such ordered pairs; in all, selected entries constant per word and opposite: violations={bad}")
print("   controls:")
VW2 = [w for w in words if valid(w, antip=False)]
chk(any(X not in w for w in VW2), f"  drop antipodal equality: X-free words exist e.g. {[w for w in VW2 if X not in w][:2]} (expected)")
w = "XUVXUV"
comp_nocross = [v for v in VW if v != w]
chk(len(comp_nocross) > 0, f"  without the cross-word restriction {w} is not isolated ({len(comp_nocross)} other valid words)")
sh = lambda s: s[1:] + s[:1]
chk(sh("UVUVUV") != "UVUVUV" and sh(sh("UVUVUV")) == "UVUVUV", "  sanity: shift operator behaves (period-2 word fixed by double shift)")
print("RESULT:", "ALL CHECKS PASS" if not fails else f"{len(fails)} FAILURE(S): {fails}")
sys.exit(1 if fails else 0)
