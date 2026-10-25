# Referee report — seat `cycles` — §8 of "The Euclidean plane is not five-colorable" (OpenAI, 23 Sep 2026)

Scope: §8 in full (PDF pp. 51–60): preamble, Lemma 8.1, Prop 8.2, §8.3 preamble, Lemma 8.3, Lemma 8.4, Prop 8.5,
§8.4 preamble, Lemma 8.6, Lemma 8.7, §8.5 / Lemma 8.8, (8.5) Moser spindle, (8.6) placement, Lemma 8.9, Prop 8.10,
proof of Theorem 1.4, §8.6 rational verification; tests (B) and (G) of the brief. All quotes below are from the rendered
PDF pages (read with `pages=`), not from the text extraction.

## Verdict for this scope

**HOLDS AS READ**, conditional on the inputs §8 imports from §§4–7 (taken as given here; other seats' scope):
Lemma 4.3 (unit pairs of typical points differ), Definition 5.1 (traces W_x, palettes P_x, typical circle samplings),
Lemma 5.2 (5.2) and its density assertion 2, Corollary 5.4 (5.7), Lemma 6.3, Lemma 6.4, Proposition 7.1.
Proposition 5.6 / (5.12) is cited once in §8 (Prop 8.2) and is NOT needed there (Objection 1, proved by enumeration).
I found no FATAL objection and no GAP in §8. Every finite claim in §8 was recomputed exactly; every exclusion claim of
the six-position word lemma was checked exhaustively; every check has a control that fails.

## Objections

1. **COSMETIC (observation; matters for test B).** Prop 8.2, p. 52: *"The palette size bound (5.12) and (8.1) imply
   that almost every palette is a pair, containing one vertex from each allowed set."* The bound (5.12) is not needed:
   the constraints of the five-cycle argument (palette meets O(e) and I(e); consecutive palettes on an R-orbit disjoint)
   are monotone under passing to a sub-palette, so one may pick one vertex from each allowed set and run the paper's
   index argument on that pair. Exhaustive check (`words.py`): with palettes of ANY size the one-orbit system is still
   unsatisfiable (0 of 32,768 sign triples). Consequence: inside §8 nothing depends on Prop 5.6 (8.3 and 8.4 never use
   (5.12)). Fix: replace "is a pair" by "contains a pair". Exposition only.
2. **COSMETIC.** Prop 8.2, p. 52: *"The two possible palettes are therefore D1 = {1, 3} and D4 = {4, 1}, whose indices
   differ by two modulo five."* 4 − 1 = 3 ≡ −2; "differ by ±2" is meant and is what is used. Correct.
3. **COSMETIC.** §8.3, p. 53: *"Lemma 6.3 now applies to these three represented groups."* Lemma 6.3 is a statement
   about TWO states A, B whose groups partition I \ {X}; it is applied twice (A = U-set, B = V-set and the reverse),
   each time needing σ(A) > 0, which the preceding sentence (*"We may therefore suppose that both diagonal states have
   positive angular measure."*) supplies. The conclusion F_D ∩ RF_D = ∅ follows from Lemma 6.3's "no pair at chordal
   distance one" (chord 1 ⇔ angle ±π/3). Correct; wording only.
4. **COSMETIC.** Prop 8.5, p. 54: *"Both of the open diagonal arcs in Lemma 8.4 would therefore contain three equally
   spaced projective positions. An open arc containing such three positions has length greater than 2π/3 … This
   contradicts the diagonal arc of length at most π/2."* Both arcs exceeding 2π/3 already contradicts their sum π, so
   the "≤ π/2" clause of Lemma 8.4 is never needed. (The Lean does not formalise Lemma 8.4 at all: Interfaces.lean
   l. 360–363, *"The three-direction quadratic moment replaces the source's projective arc length argument. No
   assumption about antipodal ray pairs or the collinear case is required"* — a different, shorter route.)
5. **COSMETIC.** Prop 8.10, p. 58: *"Choose ρ > 0 so that …"* reuses ρ, already the radius of Prop 7.1 which §8 is
   working inside. Harmless.

No other objection. In particular (test F, this scope): every exceptional null set in §8 is taken at the single fixed
centre x after the continua K_j, directions v_j and the finite set B are fixed; G is chosen after F_U, F_V; η after
their separation margin; the radii sequences in Lemma 8.1 / Lemma 8.6 are chosen from a conull set fixed beforehand and
the restriction holds "eventually along the entire sequence", so passing to a weak-* subsequence loses nothing;
compactness is used only for closed essential supports in S (compact); "connected" is used only for open polar
rectangles U′ and open arcs (connected). The hedge words in §8 ("the same argument" l.1 of Lemma 8.1's proof for the
inner strip; "similarly" for the rotated Moser triangles; "in the same way" for the second block in Lemma 8.3) were
each checked; each is literally correct.

## Line-by-line status

| item (PDF page) | status | note |
|---|---|---|
| §8 preamble (51) | VERIFIED LINE BY LINE | q_{j,n} from Prop 7.1 item 2 |
| Lemma 8.1 (51–52) | VERIFIED LINE BY LINE | identity checked symbolically; x+ρ′e′ with ρ′>1 has |·−x|>1, |·−q_{j,n}|<1 ⇒ ∈Δ(K_j); H_i∩Δ=∅ ⇒ A_i null on the open set Δ (σ-compact). Nonemptiness: only bites when ℓ=5 (no outsiders). (8.1): polar Fubini per arc, countable Lindelöf cover of S\B, radii from a conull set, weak-* trace in W_x with zero excluded coordinates and sum 1 |
| Prop 8.2 (52) | VERIFIED LINE BY LINE + EXHAUSTIVE | run structure (2+2+1+1>5), allowed sets = internal run vertices, options {D_a, D_{a±2}} invariant under sign reversal, D_a∩D_b=∅ ⇔ b−a=±1, three-step sums {±1,±3}, six equal steps ≠0 mod 5 |
| §8.3 preamble (52–53) | VERIFIED LINE BY LINE | split ⇔ ++−− cyclic; d(−e)=d(e); (8.2) from (5.7); one diagonal null ⇒ Lemma 6.4 (states X / V, R-alternating); Lemma 6.3 ⇒ F_D∩R^{±1}F_D=∅, compact ⇒ margin; cross-word restriction with η ≤ margin |
| Lemma 8.3 (53) | VERIFIED LINE BY LINE + EXHAUSTIVE | 34 valid words; every one contains X; mixed-parity words = the 6 three-periodic permutation words; each isolated under the cross-word restriction (also under the Lean's one-directional `FourWordCross`); shift ≠ word; chain argument on a dense κ-invariant G |
| Lemma 8.4 (54) | VERIFIED LINE BY LINE + GRID | 24⁴ ray configurations on a 15° grid: 576 split everywhere (528 two-line, 48 one-line), 0 violations of any assertion |
| Prop 8.5 (54) | VERIFIED LINE BY LINE + EXHAUSTIVE (word step) | 4 ordered cross-compatible opposite-parity word pairs, all with constant opposite selected diagonals; projective triples spaced by κ |
| §8.4 preamble (54–55) | VERIFIED LINE BY LINE | two of three signs agree, those two edges cover the triangle; unique outsider by (5.7) ⇒ binary s with s(Re)≠s(e) |
| Lemma 8.6 (55) | VERIFIED LINE BY LINE | F(r,θ), ∂_θF=√3 and (8.3) unit distances checked symbolically; 4-edge path, two colours alternate ⇒ c(q)=c(q+h); Fubini in (q,h); open/closed dichotomy on connected U′; radial traces ⇒ s locally constant |
| Lemma 8.7 (56) | VERIFIED LINE BY LINE + GRID | E_s closed, R-invariant, nonempty; each boundary orbit needs ≥2 of ≤3 projective classes of B, orbits disjoint ⇒ one orbit. Grid: 72³ triangle configurations, max qualifying orbits = 1 |
| §8.5 / Lemma 8.8 (56) | VERIFIED LINE BY LINE | triple-angle identities, sin(a−b)sin(a+b)=sin²a−sin²b, Jacobian sin(2δ) — sympy; (8.4) ⇔ opposite-sign sectors on 156,931 random points, 0 disagreements |
| (8.5) Moser spindle (57) | VERIFIED EXACTLY | 11 edges |·|²=1 in Q(√3,√11); 0 proper 3-colourings of 2187; 384 proper 4-colourings |
| (8.6), Lemma 8.9 (57–58) | VERIFIED EXACTLY, two independent ways | (i) exact field values + certified sign of P′−P, l, 4−l; (ii) literal replay of §8.6 |
| Prop 8.10 + proof of Thm 1.4 (58) | VERIFIED LINE BY LINE | common translation off seven null sets; edges preserved by rotation+translation |
| §8.6 (58–60) | VERIFIED (every displayed number) | residual numerators match exactly; Table 2 factors; both bound chains; P₊ < P′₋ in all rows |
| Figure 3 (57) | SKIMMED | caption's "eleven drawn edges have unit length" checked |

## Test (G) — the rational placement certificate

Recomputed from scratch in exact arithmetic over Q(√3, √11) (basis 1, √3, √11, √33, Fraction coefficients):
z_g = M(g + c), M = (35+12i)/37 (|M|² = 1 exactly), c = (−290+149i)/250. All 11 placed edges have |·|² = 1 as an
exact field identity. For each of the seven vertices, l = ξ²+υ², P = υ²(3ξ²−υ²)² and P′ = l³(1−l/4)(l−1)² were
computed as exact field elements and the signs of l, 4−l, P′−P certified by rigorous rational enclosures of √3, √11, √33
(isqrt at 10⁻⁴⁰). All seven: 0 < l < 4 and P < P′. Smallest certified margin: vertex B, P′−P ≥ 6.97·10⁻⁴ (B sits 0.84°
from the sector boundary ray at angle π, where P ≈ 0 — legitimately inside the open region). Independently (mpmath,
50 digits) sin 3(φ−δ) and sin 3(φ+δ) have opposite signs at all seven vertices. The paper's own §8.6 argument was
replayed literally: every residual numerator in the d_x/d_y table equals the exact value, all |numerators| < 35,520,000,
(47/37)ε + 0.00005 < h, every Table 2 inequality, both bound chains, P₊ < P′₋ in all seven rows.
Controls that FAIL as they must: vertex uT moved by +0.01 (three edges become non-unit, e.g. |T−uT|² = 10001/10000 −
(7/2220)√3 − (1/925)√33); non-edges 0T (|·|²=3) and A,uA (1/3); points 0, (3√3+3i)/4, 1, 2 rejected by the region test;
the placement without the rotation M (4 vertices outside); the placement shifted by 0.3M (5 outside); a wrong u (non-unit
edges); the §8.6 replay with one Table 1 entry changed (P′₋ for uT 12.9 → 13.5) exits 1 at exactly that row.
The Lean (Moser.lean) uses the identical region (`ThreeLabelRegion`), coordinates, centres and edge list.

## Test (B) — where "five" enters §8, and what breaks at six

The number of labels enters §8 ONLY through the number of outsiders 5 − ℓ:
- ℓ = 5 (Prop 8.2): no outsiders, so O(e), I(e) are disjoint sets of cycle labels. The one-orbit sign/palette system is
  unsatisfiable (0/32,768). With k = 6 the same one-orbit system is SATISFIABLE for ℓ = 6 (7,800 sign triples) and for
  ℓ = 5 with one outsider (6,280): the Prop 8.2 argument does not extend.
- ℓ = 4 (§8.3–Prop 8.5): exactly one outsider X, so the diagonals U, V partition I \ {X}, which is the hypothesis of
  Lemma 6.3 that produces the strict separation F_D ∩ RF_D = ∅ and hence the cross-word restriction; the word alphabet
  is {X, U, V}. With k = 6 there are two outsiders, U ∪ V ≠ I \ {X}, Lemma 6.3 does not apply and the cross-word
  restriction (the only non-local input of Lemma 8.3/Prop 8.5) is lost. (The one-orbit model alone is satisfiable even at
  k = 5, ℓ = 4 — e.g. word X V U X V U — which is why the paper needs the non-local isolation/shift argument; it has it.)
- ℓ = 3 (§8.4–8.5): exactly two outsiders X, Y: *"There cannot be two outsiders in such a palette, since (5.7) would leave
  no outsider at Re"* gives the BINARY state s; Lemma 8.6's 4-edge path forces c(q) = c(q+h) only because two colours
  must alternate; Lemma 8.8 removes both outsiders leaving three labels, and the Moser spindle (χ = 4) finishes. With k = 6
  there are three outsiders: no binary state, Lemma 8.6's alternation fails (three colours on the path), and the
  Lemma 8.8 analogue leaves four labels, on which the Moser spindle is colourable (384 proper 4-colourings); a 5-chromatic
  unit-distance graph would have to be placed inside a sector-defined region whose existence is itself not derived.
- Prop 5.6's "≤ 2" is not load-bearing anywhere in §8 (Objection 1).
So §8 does not prove too much; it breaks at six in Prop 8.2's analogue, at Lemma 6.3's hypothesis for four-cycles, and
at the binary state/Lemma 8.6/the Moser certificate for triangles. Sanity check on a REAL colouring (`hex7.py`): the
standard hexagonal 7-colouring (side 0.45, proper: 0 monochromatic unit pairs in 4·10⁵ samples; control side 0.55 gives
1,224) has, at a hexagon triple point, three boundary segments that are exactly Prop 7.1's data (a triangle of common
exclusion continua) with k = 7; Lemma 8.1's strip conclusion holds on it (0 violations), and the strips near the unit
circle carry all FOUR outsiders {1,4,5,6} — the configuration §8 kills at k = 5 genuinely exists at k = 7, and the only
thing that kills it at k = 5 is the two-outsider count, which is exactly where the paper uses it.

## Citation table (§8)

| cited | paper's claim | source (fetched) | verdict |
|---|---|---|---|
| [25] Sokolov–Voronov arXiv:2502.01958v1, Prop 9 | one-sided strips are "a counterpart of the complementary-color strips" | Prop 9: "the segment of this ray with endpoints at distances 1 and hδ from u is colored in colors 1, 2, 3"; then "in any neighborhood of a circle of radius 1, there exists an open strip colored in colors 1, 2, 3" (6-colour map-type setting, multicolour {4,5,6} at u) | MATCH (attribution, not an input) |
| [30] Voronov arXiv:2304.10163v3, §§3–5 | "related circle and complementary-arc arguments … for a positive interval of forbidden distances" | §3 "Colorings of the circle", §4 "Coloring of complementary arcs", §5 "Chromatic number of the bicycle"; title "…with an interval of forbidden distances is at least 7" | MATCH (attribution) |
| [28] Townsend 2005, Thms 1, 4 | "predecessor in Townsend's annulus argument" | jennysteve.net does not resolve from this box; no Wayback snapshot | COULD NOT FETCH (non-load-bearing) |
| [19] Moser & Moser 1961 | the 7-vertex graph is not 3-colourable | not fetched; the graph is verified directly (exact unit edges, 0 proper 3-colourings) | NOT NEEDED |

## Instrument notes (what went wrong in MY checks, and why it does not touch the paper)

- First version of `words.py` had two controls that I expected to come back SAT and that came back UNSAT:
  "allow |P| ≤ 3" and "replace antipodal sign reversal by s_{j+3} = s_j". Both were mis-designed: the constraints are
  monotone under sub-palettes (so larger palettes cannot help), and sign reversal preserves the option set (so
  s_{j+3} = s_j gives the same options). The first became Objection 1; both were replaced by a real control
  (independent signs at the six positions ⇒ 100 consistent palette cycles), which the solver does find.
- First version of `geometry.py` had an inverted assertion in the Lemma 8.8 control (it asserted agreement of the
  reversed predicate instead of disagreement); the printed numbers were already the right ones (reversed inequality
  disagrees on 156,931/156,931). Fixed; the final run is the one shown.
- Every verdict below is carried by an exit code (0 pass / 1 fail) and each script contains at least one input it must
  reject; the rejections are shown in the outputs.

## Finite checks — scripts verbatim and outputs

All scripts live in /tmp/oaimath/158/seats/cycles_work/; each run < 35 s, < 170 MB. No lean/lake run.

### moser_exact.py
```python
#!/usr/bin/env python3
"""Exact verification of the Moser placement certificate (paper eqs. 8.5, 8.6, 8.4; Lemma 8.9).
Field arithmetic: Q(sqrt3, sqrt11) with basis (1, s3, s11, s33); all coefficients Fractions.
Sign decisions: a linear form a + b*s3 + c*s11 + d*s33 with rational a..d is evaluated with
rigorous rational enclosures of s3, s11, s33 (math.isqrt at scale 10^40); the sign is certified
iff the enclosure excludes 0, otherwise the script reports UNDECIDED (never a pass).
"""
from fractions import Fraction as F
from math import isqrt
import itertools, sys

class Q:
    __slots__ = ("c",)
    def __init__(s, a=0, b=0, c=0, d=0):
        s.c = (F(a), F(b), F(c), F(d))
    def __add__(s, o):
        o = o if isinstance(o, Q) else Q(o); return Q(*[x+y for x, y in zip(s.c, o.c)])
    __radd__ = __add__
    def __neg__(s): return Q(*[-x for x in s.c])
    def __sub__(s, o): return s + (-(o if isinstance(o, Q) else Q(o)))
    def __rsub__(s, o): return Q(o) - s
    def __mul__(s, o):
        o = o if isinstance(o, Q) else Q(o)
        a1, b1, c1, d1 = s.c; a2, b2, c2, d2 = o.c
        # s3^2=3, s11^2=11, s33^2=33, s3*s11=s33, s3*s33=3*s11, s11*s33=11*s3
        a = a1*a2 + 3*b1*b2 + 11*c1*c2 + 33*d1*d2
        b = a1*b2 + b1*a2 + 11*(c1*d2 + d1*c2)
        c = a1*c2 + c1*a2 + 3*(b1*d2 + d1*b2)
        d = a1*d2 + d1*a2 + b1*c2 + c1*b2
        return Q(a, b, c, d)
    __rmul__ = __mul__
    def __eq__(s, o):
        o = o if isinstance(o, Q) else Q(o); return s.c == o.c
    def __repr__(s): return "Q(%s)" % ", ".join(str(x) for x in s.c)

S3, S11, S33 = Q(0, 1), Q(0, 0, 1), Q(0, 0, 0, 1)
assert S3*S3 == Q(3) and S11*S11 == Q(11) and S3*S11 == S33 and S33*S33 == Q(33)

SC = 10**40
def encl(n):  # rational lo < sqrt(n) < hi, certified by squaring
    r = isqrt(n*SC*SC); lo, hi = F(r, SC), F(r+1, SC)
    assert lo*lo <= n < hi*hi
    return lo, hi
E = [None, encl(3), encl(11), encl(33)]

def sign(q):
    lo = hi = q.c[0]
    for k in (1, 2, 3):
        a = q.c[k]; l, h = E[k]
        if a >= 0: lo += a*l; hi += a*h
        else: lo += a*h; hi += a*l
    if lo > 0: return 1, lo, hi
    if hi < 0: return -1, lo, hi
    if lo == hi == 0: return 0, lo, hi
    return None, lo, hi  # UNDECIDED

class C:  # complex number with Q parts
    def __init__(s, re, im=0):
        s.re = re if isinstance(re, Q) else Q(re); s.im = im if isinstance(im, Q) else Q(im)
    def __add__(s, o): return C(s.re+o.re, s.im+o.im)
    def __sub__(s, o): return C(s.re-o.re, s.im-o.im)
    def __mul__(s, o): return C(s.re*o.re - s.im*o.im, s.re*o.im + s.im*o.re)
    def n2(s): return s.re*s.re + s.im*s.im

half = F(1, 2)
A = C(S3*half, Q(half)); B = C(S3*half, Q(-half)); T = C(S3, 0)
u = C(Q(F(5, 6)), S11*F(1, 6))
V = {"0": C(0, 0), "A": A, "B": B, "T": T, "uA": u*A, "uB": u*B, "uT": u*T}
EDGES = [("0","A"),("0","B"),("A","B"),("T","A"),("T","B"),
         ("0","uA"),("0","uB"),("uA","uB"),("uT","uA"),("uT","uB"),("T","uT")]

def check_edges(P, edges, tag):
    ok = True
    for a, b in edges:
        d2 = (P[a]-P[b]).n2()
        good = (d2 == Q(1))
        ok &= good
        print(f"  [{tag}] |{a}-{b}|^2 = {d2}  -> {'UNIT (exact)' if good else 'NOT UNIT  <-- REJECT'}")
    return ok

def region(z):
    xi, up = z.re, z.im
    l = xi*xi + up*up
    P = up*up*(3*xi*xi - up*up)*(3*xi*xi - up*up)
    Pp = l*l*l*(1 - l*F(1, 4))*(l - 1)*(l - 1)
    s1, l1, h1 = sign(l); s2, l2, h2 = sign(4 - l); s3, l3, h3 = sign(Pp - P)
    ok = (s1 == 1 and s2 == 1 and s3 == 1)
    return ok, (s1, s2, s3), (float(l1), float(l3)), l, P, Pp

def check_region(P, tag):
    allok = True
    for g, z in P.items():
        ok, sg, (lval, gap), *_ = region(z)
        allok &= ok
        print(f"  [{tag}] {g:>2}: z~({float(sign(z.re)[1]):+.6f},{float(sign(z.im)[1]):+.6f})  l~{lval:.6f}  "
              f"P'-P >= {gap:.6g}  signs(l,4-l,P'-P)={sg}  -> {'IN REGION' if ok else 'OUTSIDE/UNDECIDED  <-- REJECT'}")
    return allok

print("== 1. Unplaced Moser graph (8.5): eleven edges exactly unit")
ok1 = check_edges(V, EDGES, "G")
print("   all unit:", ok1)

print("== 2. Moser graph has no proper 3-colouring (brute force 3^7), has a proper 4-colouring (control)")
names = list(V)
def colourings(k):
    return [f for f in itertools.product(range(k), repeat=7)
            if all(f[names.index(a)] != f[names.index(b)] for a, b in EDGES)]
n3, n4 = len(colourings(3)), len(colourings(4))
print(f"   proper 3-colourings: {n3}   proper 4-colourings: {n4}")

print("== 3. Placement (8.6): z_g = M (g + c), M=(35+12i)/37, c=(-290+149i)/250")
M = C(Q(F(35, 37)), Q(F(12, 37))); c = C(Q(F(-290, 250)), Q(F(149, 250)))
print("   |M|^2 =", M.n2(), "(exact)")
Z = {g: M*(z + c) for g, z in V.items()}
ok3 = check_edges(Z, EDGES, "placed")
print("   all placed edges unit:", ok3)
print("== 4. Region (8.4) + 0<l<4 for every placed vertex (exact field values, certified signs)")
ok4 = check_region(Z, "placed")
print("   all seven in region:", ok4)
print("   distinct vertices:", len({tuple(z.re.c + z.im.c) for z in Z.values()}) == 7)

print("== 5. CONTROLS (each must be REJECTED)")
Zp = dict(Z); Zp["uT"] = Z["uT"] + C(Q(F(1, 100)), 0)
c1 = check_edges(Zp, [("T", "uT"), ("uT", "uA"), ("uT", "uB")], "perturbed uT by +0.01")
print("   control 5a (perturbed vertex) edges all unit?", c1, "(expected False)")
c2 = check_edges(Z, [("0", "T"), ("A", "uA")], "non-edges")
print("   control 5b (non-unit pairs claimed as edges) all unit?", c2, "(expected False)")
c3 = check_region({"origin": C(0, 0), "1.5e^{i pi/6}": C(S3*F(3, 4), Q(F(3, 4))),
                   "unit-circle 1": C(1, 0), "radius 2": C(2, 0)}, "bad points")
print("   control 5c (points that must lie outside) all in region?", c3, "(expected False)")
Zc = {g: (z + c) for g, z in V.items()}   # translation only, no rotation
c4 = check_region(Zc, "no rotation")
print("   control 5d (placement without the rotation M) all in region?", c4, "(expected False)")
Zd = {g: M*(z + C(Q(F(-290, 250)), Q(F(149, 250))) + C(Q(F(3, 10)), 0)) for g, z in V.items()}
c5 = check_region(Zd, "shifted by M*0.3")
print("   control 5e (placement shifted by M*0.3) all in region?", c5, "(expected False)")
u_bad = C(Q(F(5, 6)), S11*F(1, 5))
Vb = dict(V); Vb["uA"], Vb["uB"], Vb["uT"] = u_bad*A, u_bad*B, u_bad*T
c6 = check_edges(Vb, [("T", "uT"), ("0", "uA")], "wrong u=(5/6)+i*sqrt11/5")
print("   control 5f (wrong rotation u) all unit?", c6, "(expected False)")
verdict = ok1 and n3 == 0 and n4 > 0 and ok3 and ok4 and not any([c1, c2, c3, c4, c5, c6])
print("VERDICT:", "CERTIFICATE VERIFIED, ALL CONTROLS REJECTED" if verdict else "FAILURE")
sys.exit(0 if verdict else 1)
```
Output (`moser_exact.out`):
```
== 1. Unplaced Moser graph (8.5): eleven edges exactly unit
  [G] |0-A|^2 = Q(1, 0, 0, 0)  -> UNIT (exact)
  [G] |0-B|^2 = Q(1, 0, 0, 0)  -> UNIT (exact)
  [G] |A-B|^2 = Q(1, 0, 0, 0)  -> UNIT (exact)
  [G] |T-A|^2 = Q(1, 0, 0, 0)  -> UNIT (exact)
  [G] |T-B|^2 = Q(1, 0, 0, 0)  -> UNIT (exact)
  [G] |0-uA|^2 = Q(1, 0, 0, 0)  -> UNIT (exact)
  [G] |0-uB|^2 = Q(1, 0, 0, 0)  -> UNIT (exact)
  [G] |uA-uB|^2 = Q(1, 0, 0, 0)  -> UNIT (exact)
  [G] |uT-uA|^2 = Q(1, 0, 0, 0)  -> UNIT (exact)
  [G] |uT-uB|^2 = Q(1, 0, 0, 0)  -> UNIT (exact)
  [G] |T-uT|^2 = Q(1, 0, 0, 0)  -> UNIT (exact)
   all unit: True
== 2. Moser graph has no proper 3-colouring (brute force 3^7), has a proper 4-colouring (control)
   proper 3-colourings: 0   proper 4-colourings: 384
== 3. Placement (8.6): z_g = M (g + c), M=(35+12i)/37, c=(-290+149i)/250
   |M|^2 = Q(1, 0, 0, 0) (exact)
  [placed] |0-A|^2 = Q(1, 0, 0, 0)  -> UNIT (exact)
  [placed] |0-B|^2 = Q(1, 0, 0, 0)  -> UNIT (exact)
  [placed] |A-B|^2 = Q(1, 0, 0, 0)  -> UNIT (exact)
  [placed] |T-A|^2 = Q(1, 0, 0, 0)  -> UNIT (exact)
  [placed] |T-B|^2 = Q(1, 0, 0, 0)  -> UNIT (exact)
  [placed] |0-uA|^2 = Q(1, 0, 0, 0)  -> UNIT (exact)
  [placed] |0-uB|^2 = Q(1, 0, 0, 0)  -> UNIT (exact)
  [placed] |uA-uB|^2 = Q(1, 0, 0, 0)  -> UNIT (exact)
  [placed] |uT-uA|^2 = Q(1, 0, 0, 0)  -> UNIT (exact)
  [placed] |uT-uB|^2 = Q(1, 0, 0, 0)  -> UNIT (exact)
  [placed] |T-uT|^2 = Q(1, 0, 0, 0)  -> UNIT (exact)
   all placed edges unit: True
== 4. Region (8.4) + 0<l<4 for every placed vertex (exact field values, certified signs)
  [placed]  0: z~(-1.290595,+0.187568)  l~1.700816  P'-P >= 0.522848  signs(l,4-l,P'-P)=(1, 1, 1)  -> IN REGION
  [placed]  A: z~(-0.633544,+0.941414)  l~1.287637  P'-P >= 0.0302224  signs(l,4-l,P'-P)=(1, 1, 1)  -> IN REGION
  [placed]  B: z~(-0.309219,-0.004532)  l~0.095637  P'-P >= 0.00069663  signs(l,4-l,P'-P)=(1, 1, 1)  -> IN REGION
  [placed]  T: z~(+0.347832,+0.749314)  l~0.682458  P'-P >= 0.00445644  signs(l,4-l,P'-P)=(1, 1, 1)  -> IN REGION
  [placed] uA: z~(-1.159756,+1.178971)  l~2.735008  P'-P >= 9.75105  signs(l,4-l,P'-P)=(1, 1, 1)  -> IN REGION
  [placed] uB: z~(-0.366595,+0.569960)  l~0.459246  P'-P >= 0.0230783  signs(l,4-l,P'-P)=(1, 1, 1)  -> IN REGION
  [placed] uT: z~(-0.235756,+1.561364)  l~2.493438  P'-P >= 0.448211  signs(l,4-l,P'-P)=(1, 1, 1)  -> IN REGION
   all seven in region: True
   distinct vertices: True
== 5. CONTROLS (each must be REJECTED)
  [perturbed uT by +0.01] |T-uT|^2 = Q(10001/10000, -7/2220, 0, -1/925)  -> NOT UNIT  <-- REJECT
  [perturbed uT by +0.01] |uT-uA|^2 = Q(371037/370000, 7/888, 7/4440, -1/1850)  -> NOT UNIT  <-- REJECT
  [perturbed uT by +0.01] |uT-uB|^2 = Q(369037/370000, 7/888, -7/4440, -1/1850)  -> NOT UNIT  <-- REJECT
   control 5a (perturbed vertex) edges all unit? False (expected False)
  [non-edges] |0-T|^2 = Q(3, 0, 0, 0)  -> NOT UNIT  <-- REJECT
  [non-edges] |A-uA|^2 = Q(1/3, 0, 0, 0)  -> NOT UNIT  <-- REJECT
   control 5b (non-unit pairs claimed as edges) all unit? False (expected False)
  [bad points] origin: z~(+0.000000,+0.000000)  l~0.000000  P'-P >= 0  signs(l,4-l,P'-P)=(0, 1, 0)  -> OUTSIDE/UNDECIDED  <-- REJECT
  [bad points] 1.5e^{i pi/6}: z~(+1.299038,+0.750000)  l~2.250000  P'-P >= -3.60406  signs(l,4-l,P'-P)=(1, 1, -1)  -> OUTSIDE/UNDECIDED  <-- REJECT
  [bad points] unit-circle 1: z~(+1.000000,+0.000000)  l~1.000000  P'-P >= 0  signs(l,4-l,P'-P)=(1, 1, 0)  -> OUTSIDE/UNDECIDED  <-- REJECT
  [bad points] radius 2: z~(+2.000000,+0.000000)  l~4.000000  P'-P >= 0  signs(l,4-l,P'-P)=(1, 0, 0)  -> OUTSIDE/UNDECIDED  <-- REJECT
   control 5c (points that must lie outside) all in region? False (expected False)
  [no rotation]  0: z~(-1.160000,+0.596000)  l~1.700816  P'-P >= -3.42565  signs(l,4-l,P'-P)=(1, 1, -1)  -> OUTSIDE/UNDECIDED  <-- REJECT
  [no rotation]  A: z~(-0.293975,+1.096000)  l~1.287637  P'-P >= -0.946036  signs(l,4-l,P'-P)=(1, 1, -1)  -> OUTSIDE/UNDECIDED  <-- REJECT
  [no rotation]  B: z~(-0.293975,+0.096000)  l~0.095637  P'-P >= 0.000122102  signs(l,4-l,P'-P)=(1, 1, 1)  -> IN REGION
  [no rotation]  T: z~(+0.572051,+0.596000)  l~0.682458  P'-P >= -0.112846  signs(l,4-l,P'-P)=(1, 1, -1)  -> OUTSIDE/UNDECIDED  <-- REJECT
  [no rotation] uA: z~(-0.714698,+1.491380)  l~2.735008  P'-P >= 18.4117  signs(l,4-l,P'-P)=(1, 1, 1)  -> IN REGION
  [no rotation] uB: z~(-0.161927,+0.658047)  l~0.459246  P'-P >= -0.029306  signs(l,4-l,P'-P)=(1, 1, -1)  -> OUTSIDE/UNDECIDED  <-- REJECT
  [no rotation] uT: z~(+0.283376,+1.553427)  l~2.493438  P'-P >= 1.63599  signs(l,4-l,P'-P)=(1, 1, 1)  -> IN REGION
   control 5d (placement without the rotation M) all in region? False (expected False)
  [shifted by M*0.3]  0: z~(-1.006811,+0.284865)  l~1.094816  P'-P >= -0.702349  signs(l,4-l,P'-P)=(1, 1, -1)  -> OUTSIDE/UNDECIDED  <-- REJECT
  [shifted by M*0.3]  A: z~(-0.349760,+1.038711)  l~1.201252  P'-P >= -0.497713  signs(l,4-l,P'-P)=(1, 1, -1)  -> OUTSIDE/UNDECIDED  <-- REJECT
  [shifted by M*0.3]  B: z~(-0.025435,+0.092765)  l~0.009252  P'-P >= 3.93451e-07  signs(l,4-l,P'-P)=(1, 1, 1)  -> IN REGION
  [shifted by M*0.3]  T: z~(+0.631616,+0.846611)  l~1.115689  P'-P >= -0.151781  signs(l,4-l,P'-P)=(1, 1, -1)  -> OUTSIDE/UNDECIDED  <-- REJECT
  [shifted by M*0.3] uA: z~(-0.875972,+1.276269)  l~2.396189  P'-P >= 10.0154  signs(l,4-l,P'-P)=(1, 1, 1)  -> IN REGION
  [shifted by M*0.3] uB: z~(-0.082811,+0.667257)  l~0.452090  P'-P >= -0.0556872  signs(l,4-l,P'-P)=(1, 1, -1)  -> OUTSIDE/UNDECIDED  <-- REJECT
  [shifted by M*0.3] uT: z~(+0.048028,+1.658661)  l~2.753463  P'-P >= -0.716375  signs(l,4-l,P'-P)=(1, 1, -1)  -> OUTSIDE/UNDECIDED  <-- REJECT
   control 5e (placement shifted by M*0.3) all in region? False (expected False)
  [wrong u=(5/6)+i*sqrt11/5] |T-uT|^2 = Q(421/300, 0, 0, 0)  -> NOT UNIT  <-- REJECT
  [wrong u=(5/6)+i*sqrt11/5] |0-uA|^2 = Q(1021/900, 0, 0, 0)  -> NOT UNIT  <-- REJECT
   control 5f (wrong rotation u) all unit? False (expected False)
VERDICT: CERTIFICATE VERIFIED, ALL CONTROLS REJECTED
```

### sec86_replay.py
```python
#!/usr/bin/env python3
"""Literal replay of the paper's own Section 8.6 proof of Lemma 8.9 (PDF pp. 58-60), every displayed
number checked as an exact rational statement. Run with --corrupt to inject one wrong table entry
(control: the replay must then FAIL)."""
from fractions import Fraction as F
import sys
D = lambda s: F(s)            # terminating decimals = exact rationals (paper's convention)
fails = []
def chk(cond, msg):
    print(("  ok   " if cond else "  FAIL ") + msg)
    if not cond: fails.append(msg)

corrupt = "--corrupt" in sys.argv
# Table 1
T1 = {"0": ("-1.2906", "0.1876", "0.90", "1.35"), "A": ("-0.6335", "0.9414", "0.095", "0.110"),
      "B": ("-0.3092", "-0.0045", "0.000002", "0.00065"), "T": ("0.3478", "0.7493", "0.023", "0.026"),
      "uA": ("-1.1598", "1.1790", "9.8", "19.0"), "uB": ("-0.3666", "0.5700", "0.0022", "0.024"),
      "uT": ("-0.2358", "1.5614", "12.65", "12.9")}
# residual numerators (d_x, d_y) over 710400000000
RES = {"0": (3840000, -23040000), "A": (-29520000, 10176000), "B": (-12240000, -22464000),
       "T": (25440000, 10752000), "uA": (32043244, -19212795), "uB": (4763244, -27212795),
       "uT": (32966488, -23385590)}
# Table 2: b_y, b_H, a, b
T2 = {"0": ("0.0353", "4.963", "1.70", "1.71"), "A": ("0.887", "0.319", "1.28", "1.29"),
      "B": ("0.000022", "0.287", "0.095", "0.096"), "T": ("0.562", "0.199", "0.682", "0.683"),
      "uA": ("1.391", "2.647", "2.73", "2.74"), "uB": ("0.326", "0.079", "0.459", "0.46"),
      "uT": ("2.44", "2.273", "2.493", "2.495")}
if corrupt:
    T1["uT"] = ("-0.2358", "1.5614", "12.65", "13.5")   # raise P'_- for uT above what is provable
    print("*** CONTROL RUN: Table 1 row uT P'_- changed 12.9 -> 13.5 ***")

print("1. radical bounds by squaring rational endpoints")
chk(D("1.73205")**2 < 3 < D("1.73206")**2, "1.73205 < sqrt3 < 1.73206")
chk(D("3.31662")**2 < 11 < D("3.31663")**2, "3.31662 < sqrt11 < 3.31663")
a_, b_, eps = D("1.732055"), D("3.316625"), D("0.000005")
chk(a_ == (D("1.73205")+D("1.73206"))/2 and b_ == (D("3.31662")+D("3.31663"))/2, "a*, b* are the midpoints")
pe = (a_+b_)*eps + eps*eps
chk(pe == D("0.000025243425") and pe < D("0.000026"), f"(a*+b*)eps+eps^2 = {pe} = 0.000025243425 < 0.000026")
chk(D("0.000026")/6 < eps, "0.000026/6 < eps")
chk(F(35+12, 37) == F(47, 37), "absolute row sum of (35+12i)/37 rotation = 47/37")

print("2. midpoint-substituted placed points and the displayed residuals")
s3, s11, s33 = a_, b_, a_*b_
g = {"0": (F(0), F(0)), "A": (s3/2, F(1, 2)), "B": (s3/2, F(-1, 2)), "T": (s3, F(0)),
     "uA": ((5*s3 - s11)/12, (s33 + 5)/12), "uB": ((5*s3 + s11)/12, (s33 - 5)/12),
     "uT": (5*s3/6, s33/6)}
cx, cy = F(-290, 250), F(149, 250)
DEN = 710400000000
for k, (x, y) in g.items():
    X, Y = x + cx, y + cy
    zx, zy = (35*X - 12*Y)/37, (12*X + 35*Y)/37
    x0, y0 = D(T1[k][0]), D(T1[k][1])
    dx, dy = (zx - x0)*DEN, (zy - y0)*DEN
    chk(dx == RES[k][0] and dy == RES[k][1], f"{k:>2}: residual numerators ({dx},{dy}) == table {RES[k]}")
    chk(abs(dx) < 35520000 and abs(dy) < 35520000, f"{k:>2}: |numerators| < 35520000")
chk(DEN/20000 == 35520000, "710400000000/20000 = 35520000")
h = D("0.00011")
chk(F(47, 37)*eps + D("0.00005") < h, f"(47/37)eps + 0.00005 = {float(F(47,37)*eps + D('0.00005')):.8f} < h = 0.00011")

print("3. Table 2 factors from squared-coordinate integers; bound chains; Table 1 order")
for k in T1:
    x0, y0, Pp, Pm = (D(s) for s in T1[k]); by, bH, a, b = (D(s) for s in T2[k])
    chk(abs(x0) > h and abs(y0) > h, f"{k:>2}: |xi0|,|ups0| > h")
    m, n = abs(x0)*10**5, abs(y0)*10**5
    chk(m.denominator == 1 and n.denominator == 1, f"{k:>2}: m, n integers ({m},{n})")
    xl, xu, yl, yu = ((m-11)**2/F(10**10), (m+11)**2/F(10**10), (n-11)**2/F(10**10), (n+11)**2/F(10**10))
    chk(xl == (abs(x0)-h)**2 and yu == (abs(y0)+h)**2, f"{k:>2}: (m+-11)^2/1e10 formulas agree with (|c|+-h)^2")
    ll, lu = xl + yl, xu + yu
    H = max(abs(3*xl - yu), abs(3*xu - yl))
    chk(yu < by, f"{k:>2}: y_u = {float(yu):.8g} < b_y = {by}")
    chk(H < bH, f"{k:>2}: H = {float(H):.8g} < b_H = {bH}")
    chk(a < ll <= lu < b, f"{k:>2}: a={a} < l_l={float(ll):.6f} <= l_u={float(lu):.6f} < b={b}")
    chk(0 < a and b < 4 and (b < 1 or a > 1), f"{k:>2}: (a,b) in (0,4) and avoids 1")
    chk(by*bH**2 < Pp, f"{k:>2}: b_y b_H^2 = {float(by*bH**2):.8g} < P+ = {Pp}")
    low = a**3*(1 - b/4)*min(abs(a-1), abs(b-1))**2
    chk(low > Pm, f"{k:>2}: a^3(1-b/4)min(|a-1|,|b-1|)^2 = {float(low):.8g} > P'_- = {Pm}")
    chk(Pp < Pm, f"{k:>2}: P+ < P'_-")
chk(D("2.44")*D("2.273")**2 < D("12.65"), "displayed example 2.44(2.273)^2 < 12.65")
chk(D("2.493")**3*(1 - D("2.495")/4)*D("1.493")**2 > D("12.9"), "displayed example (2.493)^3(1-2.495/4)(1.493)^2 > 12.9")
RAD = {"0": ("1.70","1.71"), "A": ("1.28","1.29"), "B": ("0.095","0.096"), "T": ("0.68","0.69"),
       "uA": ("2.73","2.74"), "uB": ("0.459","0.46"), "uT": ("2.49","2.50")}
for k in T2:
    chk(D(RAD[k][0]) <= D(T2[k][2]) and D(T2[k][3]) <= D(RAD[k][1]), f"{k:>2}: listed squared-radius interval {RAD[k]} contains (a,b)")
print("RESULT:", "ALL CHECKS PASS" if not fails else f"{len(fails)} FAILURE(S)")
sys.exit(1 if fails else 0)
```
Output (`sec86.out`):
```
1. radical bounds by squaring rational endpoints
  ok   1.73205 < sqrt3 < 1.73206
  ok   3.31662 < sqrt11 < 3.31663
  ok   a*, b* are the midpoints
  ok   (a*+b*)eps+eps^2 = 1009737/40000000000 = 0.000025243425 < 0.000026
  ok   0.000026/6 < eps
  ok   absolute row sum of (35+12i)/37 rotation = 47/37
2. midpoint-substituted placed points and the displayed residuals
  ok    0: residual numerators (3840000,-23040000) == table (3840000, -23040000)
  ok    0: |numerators| < 35520000
  ok    A: residual numerators (-29520000,10176000) == table (-29520000, 10176000)
  ok    A: |numerators| < 35520000
  ok    B: residual numerators (-12240000,-22464000) == table (-12240000, -22464000)
  ok    B: |numerators| < 35520000
  ok    T: residual numerators (25440000,10752000) == table (25440000, 10752000)
  ok    T: |numerators| < 35520000
  ok   uA: residual numerators (32043244,-19212795) == table (32043244, -19212795)
  ok   uA: |numerators| < 35520000
  ok   uB: residual numerators (4763244,-27212795) == table (4763244, -27212795)
  ok   uB: |numerators| < 35520000
  ok   uT: residual numerators (32966488,-23385590) == table (32966488, -23385590)
  ok   uT: |numerators| < 35520000
  ok   710400000000/20000 = 35520000
  ok   (47/37)eps + 0.00005 = 0.00005635 < h = 0.00011
3. Table 2 factors from squared-coordinate integers; bound chains; Table 1 order
  ok    0: |xi0|,|ups0| > h
  ok    0: m, n integers (129060,18760)
  ok    0: (m+-11)^2/1e10 formulas agree with (|c|+-h)^2
  ok    0: y_u = 0.035235044 < b_y = 353/10000
  ok    0: H = 4.9626444 < b_H = 4963/1000
  ok    0: a=17/10 < l_l=1.700517 <= l_u=1.701167 < b=171/100
  ok    0: (a,b) in (0,4) and avoids 1
  ok    0: b_y b_H^2 = 0.86948733 < P+ = 9/10
  ok    0: a^3(1-b/4)min(|a-1|,|b-1|)^2 = 1.3782193 > P'_- = 27/20
  ok    0: P+ < P'_-
  ok    A: |xi0|,|ups0| > h
  ok    A: m, n integers (63350,94140)
  ok    A: (m+-11)^2/1e10 formulas agree with (|c|+-h)^2
  ok    A: y_u = 0.88644108 < b_y = 887/1000
  ok    A: H = 0.31835803 < b_H = 319/1000
  ok    A: a=32/25 < l_l=1.287210 <= l_u=1.287903 < b=129/100
  ok    A: (a,b) in (0,4) and avoids 1
  ok    A: b_y b_H^2 = 0.090262007 < P+ = 19/200
  ok    A: a^3(1-b/4)min(|a-1|,|b-1|)^2 = 0.11139233 > P'_- = 11/100
  ok    A: P+ < P'_-
  ok    B: |xi0|,|ups0| > h
  ok    B: m, n integers (30920,450)
  ok    B: (m+-11)^2/1e10 formulas agree with (|c|+-h)^2
  ok    B: y_u = 2.12521e-05 < b_y = 11/500000
  ok    B: H = 0.28699876 < b_H = 287/1000
  ok    B: a=19/200 < l_l=0.095556 <= l_u=0.095694 < b=12/125
  ok    B: (a,b) in (0,4) and avoids 1
  ok    B: b_y b_H^2 = 1.812118e-06 < P+ = 1/500000
  ok    B: a^3(1-b/4)min(|a-1|,|b-1|)^2 = 0.00068384471 > P'_- = 13/20000
  ok    B: P+ < P'_-
  ok    T: |xi0|,|ups0| > h
  ok    T: m, n integers (34780,74930)
  ok    T: (m+-11)^2/1e10 formulas agree with (|c|+-h)^2
  ok    T: y_u = 0.56161535 < b_y = 281/500
  ok    T: H = 0.19895034 < b_H = 199/1000
  ok    T: a=341/500 < l_l=0.682174 <= l_u=0.682657 < b=683/1000
  ok    T: (a,b) in (0,4) and avoids 1
  ok    T: b_y b_H^2 = 0.022255762 < P+ = 23/1000
  ok    T: a^3(1-b/4)min(|a-1|,|b-1|)^2 = 0.02643365 > P'_- = 13/500
  ok    T: P+ < P'_-
  ok   uA: |xi0|,|ups0| > h
  ok   uA: m, n integers (115980,117900)
  ok   uA: (m+-11)^2/1e10 formulas agree with (|c|+-h)^2
  ok   uA: y_u = 1.3903004 < b_y = 1391/1000
  ok   uA: H = 2.646392 < b_H = 2647/1000
  ok   uA: a=273/100 < l_l=2.734663 <= l_u=2.735692 < b=137/50
  ok   uA: (a,b) in (0,4) and avoids 1
  ok   uA: b_y b_H^2 = 9.7461931 < P+ = 49/5
  ok   uA: a^3(1-b/4)min(|a-1|,|b-1|)^2 = 19.181859 > P'_- = 19
  ok   uA: P+ < P'_-
  ok   uB: |xi0|,|ups0| > h
  ok   uB: m, n integers (36660,57000)
  ok   uB: (m+-11)^2/1e10 formulas agree with (|c|+-h)^2
  ok   uB: y_u = 0.32502541 < b_y = 163/500
  ok   uB: H = 0.07865406 < b_H = 79/1000
  ok   uB: a=459/1000 < l_l=0.459090 <= l_u=0.459502 < b=23/50
  ok   uB: (a,b) in (0,4) and avoids 1
  ok   uB: b_y b_H^2 = 0.002034566 < P+ = 11/5000
  ok   uB: a^3(1-b/4)min(|a-1|,|b-1|)^2 = 0.024955648 > P'_- = 3/125
  ok   uB: P+ < P'_-
  ok   uT: |xi0|,|ups0| > h
  ok   uT: m, n integers (23580,156140)
  ok   uT: (m+-11)^2/1e10 formulas agree with (|c|+-h)^2
  ok   uT: y_u = 2.4383135 < b_y = 61/25
  ok   uT: H = 2.2716642 < b_H = 2273/1000
  ok   uT: a=2493/1000 < l_l=2.493176 <= l_u=2.493967 < b=499/200
  ok   uT: (a,b) in (0,4) and avoids 1
  ok   uT: b_y b_H^2 = 12.606331 < P+ = 253/20
  ok   uT: a^3(1-b/4)min(|a-1|,|b-1|)^2 = 12.994601 > P'_- = 129/10
  ok   uT: P+ < P'_-
  ok   displayed example 2.44(2.273)^2 < 12.65
  ok   displayed example (2.493)^3(1-2.495/4)(1.493)^2 > 12.9
  ok    0: listed squared-radius interval ('1.70', '1.71') contains (a,b)
  ok    A: listed squared-radius interval ('1.28', '1.29') contains (a,b)
  ok    B: listed squared-radius interval ('0.095', '0.096') contains (a,b)
  ok    T: listed squared-radius interval ('0.68', '0.69') contains (a,b)
  ok   uA: listed squared-radius interval ('2.73', '2.74') contains (a,b)
  ok   uB: listed squared-radius interval ('0.459', '0.46') contains (a,b)
  ok   uT: listed squared-radius interval ('2.49', '2.50') contains (a,b)
RESULT: ALL CHECKS PASS
```
Output (`sec86_corrupt.out`):
```
*** CONTROL RUN: Table 1 row uT P'_- changed 12.9 -> 13.5 ***
1. radical bounds by squaring rational endpoints
  ok   1.73205 < sqrt3 < 1.73206
  ok   3.31662 < sqrt11 < 3.31663
  ok   a*, b* are the midpoints
  ok   (a*+b*)eps+eps^2 = 1009737/40000000000 = 0.000025243425 < 0.000026
  ok   0.000026/6 < eps
  ok   absolute row sum of (35+12i)/37 rotation = 47/37
2. midpoint-substituted placed points and the displayed residuals
  ok    0: residual numerators (3840000,-23040000) == table (3840000, -23040000)
  ok    0: |numerators| < 35520000
  ok    A: residual numerators (-29520000,10176000) == table (-29520000, 10176000)
  ok    A: |numerators| < 35520000
  ok    B: residual numerators (-12240000,-22464000) == table (-12240000, -22464000)
  ok    B: |numerators| < 35520000
  ok    T: residual numerators (25440000,10752000) == table (25440000, 10752000)
  ok    T: |numerators| < 35520000
  ok   uA: residual numerators (32043244,-19212795) == table (32043244, -19212795)
  ok   uA: |numerators| < 35520000
  ok   uB: residual numerators (4763244,-27212795) == table (4763244, -27212795)
  ok   uB: |numerators| < 35520000
  ok   uT: residual numerators (32966488,-23385590) == table (32966488, -23385590)
  ok   uT: |numerators| < 35520000
  ok   710400000000/20000 = 35520000
  ok   (47/37)eps + 0.00005 = 0.00005635 < h = 0.00011
3. Table 2 factors from squared-coordinate integers; bound chains; Table 1 order
  ok    0: |xi0|,|ups0| > h
  ok    0: m, n integers (129060,18760)
  ok    0: (m+-11)^2/1e10 formulas agree with (|c|+-h)^2
  ok    0: y_u = 0.035235044 < b_y = 353/10000
  ok    0: H = 4.9626444 < b_H = 4963/1000
  ok    0: a=17/10 < l_l=1.700517 <= l_u=1.701167 < b=171/100
  ok    0: (a,b) in (0,4) and avoids 1
  ok    0: b_y b_H^2 = 0.86948733 < P+ = 9/10
  ok    0: a^3(1-b/4)min(|a-1|,|b-1|)^2 = 1.3782193 > P'_- = 27/20
  ok    0: P+ < P'_-
  ok    A: |xi0|,|ups0| > h
  ok    A: m, n integers (63350,94140)
  ok    A: (m+-11)^2/1e10 formulas agree with (|c|+-h)^2
  ok    A: y_u = 0.88644108 < b_y = 887/1000
  ok    A: H = 0.31835803 < b_H = 319/1000
  ok    A: a=32/25 < l_l=1.287210 <= l_u=1.287903 < b=129/100
  ok    A: (a,b) in (0,4) and avoids 1
  ok    A: b_y b_H^2 = 0.090262007 < P+ = 19/200
  ok    A: a^3(1-b/4)min(|a-1|,|b-1|)^2 = 0.11139233 > P'_- = 11/100
  ok    A: P+ < P'_-
  ok    B: |xi0|,|ups0| > h
  ok    B: m, n integers (30920,450)
  ok    B: (m+-11)^2/1e10 formulas agree with (|c|+-h)^2
  ok    B: y_u = 2.12521e-05 < b_y = 11/500000
  ok    B: H = 0.28699876 < b_H = 287/1000
  ok    B: a=19/200 < l_l=0.095556 <= l_u=0.095694 < b=12/125
  ok    B: (a,b) in (0,4) and avoids 1
  ok    B: b_y b_H^2 = 1.812118e-06 < P+ = 1/500000
  ok    B: a^3(1-b/4)min(|a-1|,|b-1|)^2 = 0.00068384471 > P'_- = 13/20000
  ok    B: P+ < P'_-
  ok    T: |xi0|,|ups0| > h
  ok    T: m, n integers (34780,74930)
  ok    T: (m+-11)^2/1e10 formulas agree with (|c|+-h)^2
  ok    T: y_u = 0.56161535 < b_y = 281/500
  ok    T: H = 0.19895034 < b_H = 199/1000
  ok    T: a=341/500 < l_l=0.682174 <= l_u=0.682657 < b=683/1000
  ok    T: (a,b) in (0,4) and avoids 1
  ok    T: b_y b_H^2 = 0.022255762 < P+ = 23/1000
  ok    T: a^3(1-b/4)min(|a-1|,|b-1|)^2 = 0.02643365 > P'_- = 13/500
  ok    T: P+ < P'_-
  ok   uA: |xi0|,|ups0| > h
  ok   uA: m, n integers (115980,117900)
  ok   uA: (m+-11)^2/1e10 formulas agree with (|c|+-h)^2
  ok   uA: y_u = 1.3903004 < b_y = 1391/1000
  ok   uA: H = 2.646392 < b_H = 2647/1000
  ok   uA: a=273/100 < l_l=2.734663 <= l_u=2.735692 < b=137/50
  ok   uA: (a,b) in (0,4) and avoids 1
  ok   uA: b_y b_H^2 = 9.7461931 < P+ = 49/5
  ok   uA: a^3(1-b/4)min(|a-1|,|b-1|)^2 = 19.181859 > P'_- = 19
  ok   uA: P+ < P'_-
  ok   uB: |xi0|,|ups0| > h
  ok   uB: m, n integers (36660,57000)
  ok   uB: (m+-11)^2/1e10 formulas agree with (|c|+-h)^2
  ok   uB: y_u = 0.32502541 < b_y = 163/500
  ok   uB: H = 0.07865406 < b_H = 79/1000
  ok   uB: a=459/1000 < l_l=0.459090 <= l_u=0.459502 < b=23/50
  ok   uB: (a,b) in (0,4) and avoids 1
  ok   uB: b_y b_H^2 = 0.002034566 < P+ = 11/5000
  ok   uB: a^3(1-b/4)min(|a-1|,|b-1|)^2 = 0.024955648 > P'_- = 3/125
  ok   uB: P+ < P'_-
  ok   uT: |xi0|,|ups0| > h
  ok   uT: m, n integers (23580,156140)
  ok   uT: (m+-11)^2/1e10 formulas agree with (|c|+-h)^2
  ok   uT: y_u = 2.4383135 < b_y = 61/25
  ok   uT: H = 2.2716642 < b_H = 2273/1000
  ok   uT: a=2493/1000 < l_l=2.493176 <= l_u=2.493967 < b=499/200
  ok   uT: (a,b) in (0,4) and avoids 1
  ok   uT: b_y b_H^2 = 12.606331 < P+ = 253/20
  FAIL uT: a^3(1-b/4)min(|a-1|,|b-1|)^2 = 12.994601 > P'_- = 27/2
  ok   uT: P+ < P'_-
  ok   displayed example 2.44(2.273)^2 < 12.65
  ok   displayed example (2.493)^3(1-2.495/4)(1.493)^2 > 12.9
  ok    0: listed squared-radius interval ('1.70', '1.71') contains (a,b)
  ok    A: listed squared-radius interval ('1.28', '1.29') contains (a,b)
  ok    B: listed squared-radius interval ('0.095', '0.096') contains (a,b)
  ok    T: listed squared-radius interval ('0.68', '0.69') contains (a,b)
  ok   uA: listed squared-radius interval ('2.73', '2.74') contains (a,b)
  ok   uB: listed squared-radius interval ('0.459', '0.46') contains (a,b)
  ok   uT: listed squared-radius interval ('2.49', '2.50') contains (a,b)
RESULT: 1 FAILURE(S)
```

### words.py
```python
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
```
Output (`words.out`):
```
== Prop 8.2: five-cycle, five labels, |P|<=2, (8.1), (5.7), antipodal sign reversal
  ok   k=5, ell=5: sign triples admitting a consistent orbit = 0 (paper: none)
   controls (the solver CAN say SAT):
  ok     drop (5.7): 1000 sign triples admit an orbit (expected >0)
   OBSERVATION (not a control): allowing any palette size (no Prop 5.6) still gives 0 -- the constraints are monotone (a sub-palette of a solution is a solution), so (5.12) is not needed in Prop 8.2
  ok     independent signs at the six positions: 100 consistent palette cycles, e.g. [[0, 2], [1, 3], [0, 2], [1, 3], [0, 2], [1, 3]] (expected >0)
   test (B): same one-orbit model for other (k, ell):
     k=5, ell=4: sign triples admitting an orbit = 352; e.g. palettes [[4], [1, 3], [0, 2], [4], [1, 3], [0, 2]]
     k=5, ell=3: sign triples admitting an orbit = 512; e.g. palettes [[3], [4], [3], [4], [3], [4]]
     k=6, ell=6: sign triples admitting an orbit = 7800; e.g. palettes [[1, 5], [0, 4], [1, 3], [2, 5], [1, 4], [0, 3]]
     k=6, ell=5: sign triples admitting an orbit = 6280; e.g. palettes [[5], [1, 4], [0, 3], [5], [1, 4], [0, 3]]
     k=6, ell=4: sign triples admitting an orbit = 4096; e.g. palettes [[4], [5], [4], [5], [4], [5]]
     k=6, ell=3: sign triples admitting an orbit = 512; e.g. palettes [[3], [4], [3], [4], [3], [4]]
== Lemma 8.3: 34 valid words (adjacent inequality + antipodal equality) out of 729
  ok   every valid word contains X
  ok   mixed-parity words = three-periodic permutation words: ['UVXUVX', 'UXVUXV', 'VUXVUX', 'VXUVXU', 'XUVXUV', 'XVUXVU']
  ok   mixed-parity words have exactly two X, antipodal
  ok   isolation of XUVXUV: compatible valid words = ['XUVXUV']
  ok   XUVXUV != its one-position shift UVXUVX
  ok   isolation of XVUXVU: compatible valid words = ['XVUXVU']
  ok   XVUXVU != its one-position shift VUXVUX
  ok   isolation of UXVUXV: compatible valid words = ['UXVUXV']
  ok   UXVUXV != its one-position shift XVUXVU
  ok   isolation of UVXUVX: compatible valid words = ['UVXUVX']
  ok   UVXUVX != its one-position shift VXUVXU
  ok   isolation of VXUVXU: compatible valid words = ['VXUVXU']
  ok   VXUVXU != its one-position shift XUVXUV
  ok   isolation of VUXVUX: compatible valid words = ['VUXVUX']
  ok   VUXVUX != its one-position shift UXVUXV
  ok   28 single-parity valid words; their other-parity positions are all non-X
== Prop 8.5 word step: cross-compatible valid words with different X-parity
  ok   4 such ordered pairs; in all, selected entries constant per word and opposite: violations=0
   controls:
  ok     drop antipodal equality: X-free words exist e.g. ['UVUVUV', 'VUVUVU'] (expected)
  ok     without the cross-word restriction XUVXUV is not isolated (33 other valid words)
  ok     sanity: shift operator behaves (period-2 word fixed by double shift)
RESULT: ALL CHECKS PASS
```

### geometry.py
```python
#!/usr/bin/env python3
"""Finite/symbolic checks for Lemma 8.1 identity, Lemma 8.4 (four split rays), Lemma 8.6 (eq. 8.3 and F(r,theta)),
Lemma 8.7 (one boundary orbit), Lemma 8.8 (polynomial region <-> opposite sectors), with controls."""
import itertools, sys, random
import numpy as np, sympy as sp, mpmath as mp
fails = []
def chk(c, m):
    print(("  ok   " if c else "  FAIL ") + m)
    if not c: fails.append(m)

print("== Lemma 8.1 / 8.6 / 8.8 symbolic identities (sympy)")
r, e1, e2, w1, w2 = sp.symbols('r e1 e2 w1 w2', real=True)
lhs = (e1 - r*w1)**2 + (e2 - r*w2)**2          # |x+e-q|^2 with q-x = r w, |e|=|w|=1
chk(sp.simplify((lhs - (1 + r**2 - 2*r*(e1*w1+e2*w2))).subs({e2**2: 1-e1**2, w2**2: 1-w1**2}).expand().subs({e2**2: 1-e1**2, w2**2: 1-w1**2})) == 0,
    "|x+e-q|^2 = 1 + r^2 - 2r(e.w) for unit e,w")
t, th = sp.symbols('t theta', real=True)
vp = sp.Matrix([sp.cos(th), sp.sin(th)]); Jvp = sp.Matrix([-sp.sin(th), sp.cos(th)])
m = t/2*Jvp + sp.sqrt(1 - t**2/4)*vp
chk(sp.simplify(m.dot(m)) == 1 and sp.simplify((m - t*Jvp).dot(m - t*Jvp)) == 1, "(8.3): q'+(t/2)Jv'+sqrt(1-t^2/4)v' is at unit distance from q' and q'+tJv'")
R_, TH = sp.symbols('R Theta', real=True)
F = (R_*sp.cos(TH) - 1)**2 + (R_*sp.sin(TH))**2 - 1
chk(sp.simplify(F - (R_**2 - 2*R_*sp.cos(TH))) == 0 and F.subs({R_: 1, TH: sp.pi/3}) == 0
    and sp.simplify(sp.diff(F, TH).subs({R_: 1, TH: sp.pi/3}) - sp.sqrt(3)) == 0, "F(r,th)=r^2-2r cos th, F(1,pi/3)=0, dF/dth(1,pi/3)=sqrt3")
xi, up = sp.symbols('xi upsilon', real=True)
l = xi**2 + up**2
phi = sp.atan2(up, xi)
# l^3 sin^2(3 phi) = up^2(3xi^2-up^2)^2 : verify via (xi+i up)^3
chk(sp.expand(sp.im(sp.expand((xi + sp.I*up)**3)) - up*(3*xi**2 - up**2)) == 0, "Im (xi+i ups)^3 = ups(3xi^2-ups^2)  [so l^3 sin^2 3phi = P]")
d = sp.symbols('delta', positive=True)
chk(sp.simplify(sp.expand_trig(sp.sin(3*d)) - sp.sin(d)*(4*sp.cos(d)**2 - 1)) == 0, "sin 3d = sin d (4cos^2 d - 1)")
a_, b_ = sp.symbols('a b', real=True)
chk(sp.simplify(sp.expand_trig(sp.sin(a_-b_)*sp.sin(a_+b_)) - (sp.sin(a_)**2 - sp.sin(b_)**2)) == 0, "sin(a-b)sin(a+b) = sin^2 a - sin^2 b")
a1, a2 = sp.symbols('alpha1 alpha2', real=True)
Jac = sp.Matrix([[-sp.sin(a1), -sp.sin(a2)], [sp.cos(a1), sp.cos(a2)]]).det()
chk(sp.simplify(Jac - sp.sin(a2 - a1)) == 0, "Jacobian of (a1,a2)->e^{ia1}+e^{ia2} is sin(a2-a1) (= sin 2delta)")

print("== Lemma 8.8: (8.4) <=> endpoints phi+-delta strictly in opposite-sign sin(3.) sectors (random test, n=200000)")
rng = np.random.default_rng(1)
N = 200000
z = (rng.uniform(-2, 2, N) + 1j*rng.uniform(-2, 2, N)); z = z[(abs(z) > 1e-3) & (abs(z) < 2 - 1e-9)]
X, Y = z.real, z.imag; L = X**2 + Y**2
P = Y**2*(3*X**2 - Y**2)**2; Pp = L**3*(1 - L/4)*(L - 1)**2
ph = np.angle(z); dl = np.arccos(np.abs(z)/2)
prod = np.sin(3*(ph - dl))*np.sin(3*(ph + dl))
summ = np.exp(1j*(ph - dl)) + np.exp(1j*(ph + dl))
chk(np.max(np.abs(summ - z)) < 1e-12, "unit directions phi-delta, phi+delta sum to z")
margin = np.abs(Pp - P) > 1e-9
agree = ((P < Pp) == (prod < 0))[margin]
chk(agree.all(), f"(P<P') == (sin3(phi-d) sin3(phi+d) < 0) on {margin.sum()} points with |P'-P|>1e-9: disagreements {np.sum(~agree)}")
bad = ((P > Pp) == (prod < 0))[margin]
chk(np.sum(~bad) > 0.4*margin.sum(), f"  control: the reversed inequality P>P' disagrees with the sector test on {np.sum(~bad)} of {margin.sum()} points (must be many) -> comparison not vacuous")
print(f"   fraction of the disk of radius 2 in the region: {np.mean(P[margin] < Pp[margin]):.3f}")

print("== Moser vertices: independent angular check with mpmath (50 digits) of opposite-sector endpoints")
mp.mp.dps = 50
s3, s11 = mp.sqrt(3), mp.sqrt(11)
A = (s3 + 1j)/2; B = (s3 - 1j)/2; T = s3 + 0j; u = (5 + 1j*s11)/6
G = {"0": mp.mpc(0), "A": mp.mpc(A), "B": mp.mpc(B), "T": mp.mpc(T), "uA": u*A, "uB": u*B, "uT": u*T}
Mrot = mp.mpc(35, 12)/37; c = mp.mpc(-290, 149)/250
for g, val in G.items():
    zz = Mrot*(val + c); rr = abs(zz); p_ = mp.arg(zz); dd = mp.acos(rr/2)
    s_minus, s_plus = mp.sin(3*(p_ - dd)), mp.sin(3*(p_ + dd))
    chk(0 < rr < 2 and s_minus*s_plus < 0, f"{g:>2}: |z|={mp.nstr(rr,8)}  sin3(phi-d)={mp.nstr(s_minus,6)}  sin3(phi+d)={mp.nstr(s_plus,6)}  opposite signs")

def ang_sign(e, v):  # sign of e.v for angles (degrees, integer grid) -- exact on the grid via sympy-free rule
    dd = (v - e) % 360
    if dd == 90 or dd == 270: return 0
    return 1 if (dd < 90 or dd > 270) else -1

print("== Lemma 8.4 grid check: four rays v_0..v_3 on a 15-degree grid (24^4 configurations, vectorised)")
step = 15; nd = 360//step
# exact sign of cos(angle) for e at half-steps (k+1/2)*step and v at j*step: angle difference is an odd multiple of step/2
def sgn_tab():
    T = np.zeros((nd, nd), dtype=np.int8)
    for k in range(nd):
        for j in range(nd):
            dd = ((j*step) - (k*step + step/2)) % 360
            T[k, j] = 1 if (dd < 90 or dd > 270) else -1     # never exactly 90/270 on this grid
    return T
ST = sgn_tab()
cfg = np.array(list(itertools.product(range(nd), repeat=4)), dtype=np.int16)        # (24^4, 4)
S = ST[:, cfg]                                                                        # (24 mids, Ncfg, 4)
split_all = np.all((S[:, :, 0] != S[:, :, 2]) & (S[:, :, 1] != S[:, :, 3]), axis=0)  # Lean's InterfaceFourSplit
good = cfg[split_all]
def diag(sv):
    for j in range(4):
        if sv[j] == 1 and sv[(j+1) % 4] == 1: return "U" if (j+1) % 2 == 0 else "V"
viol = []; n1 = n2 = 0
for v in good:
    v = [int(x)*step for x in v]
    svs = [tuple(int(ST[k, vi//step]) for vi in v) for k in range(nd)]
    ds = [diag(sv) for sv in svs]
    for vi in v:
        if v.count(vi) != v.count((vi+180) % 360): viol.append(("not antipodally paired", v))
    lines = {vi % 180 for vi in v}
    if len(lines) == 1:
        n1 += 1
        if len(set(ds)) != 1: viol.append(("one line but both diagonals", v))
        continue
    n2 += 1
    if len(lines) != 2: viol.append(("more than two lines", v))
    for j in range(4):
        if (v[j] + 180) % 360 != v[(j+2) % 4]: viol.append(("opposite directions not at opposite edges", v))
    proj = {}
    for k, dg in enumerate(ds): proj.setdefault((k*step + step/2) % 180, set()).add(dg)
    if any(len(x) > 1 for x in proj.values()): viol.append(("d(-e) != d(e)", v))
    seq = [next(iter(proj[key])) for key in sorted(proj)]
    if sum(seq[i] != seq[(i+1) % len(seq)] for i in range(len(seq))) != 2: viol.append(("not U-arc/V-arc", v))
    lenU = step*seq.count("U")
    if min(lenU, 180 - lenU) > 90: viol.append(("no arc <= pi/2", v))
chk(len(good) > 0 and not viol, f"configs split at every generic direction: {len(good)} ({n2} two-line, {n1} one-line) of {len(cfg)}; Lemma 8.4 violations: {len(viol)} {viol[:3]}")
chk(np.sum(np.all((S[:, :, 0] != S[:, :, 2]) | (S[:, :, 1] != S[:, :, 3]), axis=0)) > len(good),
    "  control: a weaker (wrong) split test admits strictly more configurations -> the detector discriminates")

print("== Lemma 8.7 grid check: three rays on a 5-degree grid; R-orbits all of whose consecutive pairs meet B (vectorised)")
def max_orbits(nrays, stp, sub=1):
    n = 360//stp; R = 60//stp; q = 90//stp
    cfg = np.array(list(itertools.product(range(0, n, sub), repeat=nrays)), dtype=np.int16)
    Bm = np.zeros((len(cfg), n), dtype=bool)
    rows = np.arange(len(cfg))
    for i in range(nrays):
        Bm[rows, (cfg[:, i] + q) % n] = True; Bm[rows, (cfg[:, i] - q) % n] = True
    cnt = np.zeros(len(cfg), dtype=np.int16)
    for e0 in range(R):
        orb = [(e0 + R*j) % n for j in range(6)]
        ok = np.ones(len(cfg), dtype=bool)
        for j in range(6): ok &= Bm[:, orb[j]] | Bm[:, orb[(j+1) % 6]]
        cnt += ok
    return len(cfg), int(cnt.max()), np.bincount(cnt)
N3, m3, h3 = max_orbits(3, 5)
chk(m3 <= 1, f"three rays, 5-degree grid: {N3} configs, max qualifying orbits = {m3}, histogram {h3.tolist()}")
N4, m4, h4 = max_orbits(4, 5, sub=3)
chk(m4 >= 2, f"  control: four rays (15-degree subgrid, {N4} configs): max qualifying orbits = {m4} (>=2 shows the detector can exceed 1)")
print("RESULT:", "ALL CHECKS PASS" if not fails else f"{len(fails)} FAILURE(S): {fails}")
sys.exit(1 if fails else 0)
```
Output (`geometry.out`):
```
== Lemma 8.1 / 8.6 / 8.8 symbolic identities (sympy)
  ok   |x+e-q|^2 = 1 + r^2 - 2r(e.w) for unit e,w
  ok   (8.3): q'+(t/2)Jv'+sqrt(1-t^2/4)v' is at unit distance from q' and q'+tJv'
  ok   F(r,th)=r^2-2r cos th, F(1,pi/3)=0, dF/dth(1,pi/3)=sqrt3
  ok   Im (xi+i ups)^3 = ups(3xi^2-ups^2)  [so l^3 sin^2 3phi = P]
  ok   sin 3d = sin d (4cos^2 d - 1)
  ok   sin(a-b)sin(a+b) = sin^2 a - sin^2 b
  ok   Jacobian of (a1,a2)->e^{ia1}+e^{ia2} is sin(a2-a1) (= sin 2delta)
== Lemma 8.8: (8.4) <=> endpoints phi+-delta strictly in opposite-sign sin(3.) sectors (random test, n=200000)
  ok   unit directions phi-delta, phi+delta sum to z
  ok   (P<P') == (sin3(phi-d) sin3(phi+d) < 0) on 156931 points with |P'-P|>1e-9: disagreements 0
  ok     control: the reversed inequality P>P' disagrees with the sector test on 156931 of 156931 points (must be many) -> comparison not vacuous
   fraction of the disk of radius 2 in the region: 0.500
== Moser vertices: independent angular check with mpmath (50 digits) of opposite-sector endpoints
  ok    0: |z|=1.3041534  sin3(phi-d)=0.126851  sin3(phi+d)=-0.837743  opposite signs
  ok    A: |z|=1.134741  sin3(phi-d)=-0.430816  sin3(phi+d)=0.0328592  opposite signs
  ok    B: |z|=0.30925243  sin3(phi-d)=-0.872883  sin3(phi+d)=0.912362  opposite signs
  ok    T: |z|=0.82611024  sin3(phi-d)=-0.0263787  sin3(phi+d)=0.531503  opposite signs
  ok   uA: |z|=1.6537858  sin3(phi-d)=-0.857792  sin3(phi+d)=0.55564  opposite signs
  ok   uB: |z|=0.6776769  sin3(phi-d)=0.380022  sin3(phi+d)=-0.626988  opposite signs
  ok   uT: |z|=1.5790622  sin3(phi-d)=-0.0381169  sin3(phi+d)=0.758523  opposite signs
== Lemma 8.4 grid check: four rays v_0..v_3 on a 15-degree grid (24^4 configurations, vectorised)
  ok   configs split at every generic direction: 576 (528 two-line, 48 one-line) of 331776; Lemma 8.4 violations: 0 []
  ok     control: a weaker (wrong) split test admits strictly more configurations -> the detector discriminates
== Lemma 8.7 grid check: three rays on a 5-degree grid; R-orbits all of whose consecutive pairs meet B (vectorised)
  ok   three rays, 5-degree grid: 373248 configs, max qualifying orbits = 1, histogram [313920, 59328]
  ok     control: four rays (15-degree subgrid, 331776 configs): max qualifying orbits = 2 (>=2 shows the detector can exceed 1)
RESULT: ALL CHECKS PASS
```

### hex7.py
```python
#!/usr/bin/env python3
"""Test (B) illustration on a REAL proper colouring: the standard hexagonal 7-colouring (side s=0.45).
At a triple point x the three hexagon-boundary segments are compact connected exclusion continua (Prop 7.1's data,
with k=7). Check (i) properness by sampling, (ii) Lemma 8.1's one-sided strip conclusion on this colouring, and
(iii) what replaces the binary outsider state s of Sec. 8.4 when there are four outsiders instead of two."""
import numpy as np, sys
s = 0.45; SQ3 = np.sqrt(3)
def colour(p):
    x, y = p[..., 0], p[..., 1]
    q = (SQ3/3*x - y/3)/s; r = (2/3*y)/s                     # pointy-top axial coordinates
    cx, cz = q, r; cy = -cx - cz
    rx, ry, rz = np.round(cx), np.round(cy), np.round(cz)
    dx, dy, dz = abs(rx-cx), abs(ry-cy), abs(rz-cz)
    m1 = (dx > dy) & (dx > dz); m2 = (~m1) & (dy > dz)
    rx = np.where(m1, -ry-rz, rx); rz = np.where(~m1 & ~m2, -rx-ry, rz)
    return ((rx + 3*rz) % 7).astype(int)
rng = np.random.default_rng(7)
fails = []
# (i) properness on random unit pairs (skip pairs within 1e-6 of a boundary by resampling noise: measure-zero)
P = rng.uniform(-20, 20, (400000, 2)); th = rng.uniform(0, 2*np.pi, 400000)
Qp = P + np.stack([np.cos(th), np.sin(th)], 1)
mono = np.sum(colour(P) == colour(Qp))
print(f"(i) monochromatic unit pairs among 400000 random pairs: {mono}")
if mono: fails.append("hex colouring not proper")
# control: side s=0.55 (diameter 1.1 > 1) must produce monochromatic unit pairs
s_save = s; s = 0.55; mono_bad = np.sum(colour(P) == colour(Qp)); s = s_save
print(f"    control s=0.55 (hexagon diameter > 1): monochromatic unit pairs = {mono_bad} (must be > 0)")
if mono_bad == 0: fails.append("control failed")
# (ii) triple point x = top vertex of hexagon (0,0): x = (0, s); edge directions from x: 90, 210, 330 degrees
x = np.array([0.0, s]); vdeg = [90.0, 210.0, 330.0]
eps = 1e-3
def side_colours(vd):
    v = np.array([np.cos(np.radians(vd)), np.sin(np.radians(vd))]); n = np.array([-v[1], v[0]])
    p = x + 0.1*v
    return int(colour(p + eps*n)), int(colour(p - eps*n))
edges = [side_colours(vd) for vd in vdeg]
tri = sorted({c for e in edges for c in e})
print(f"(ii) edges (label pairs) at x: {edges}; triangle labels {tri}; outsiders {sorted(set(range(7)) - set(tri))}")
B = sorted({(vd + 90) % 360 for vd in vdeg} | {(vd - 90) % 360 for vd in vdeg})
viol = 0; outer_cols = set(); inner_cols = set()
for ed in np.arange(0.25, 360, 0.5):
    if min(abs(((ed - b + 180) % 360) - 180) for b in B) < 1.0: continue
    e = np.array([np.cos(np.radians(ed)), np.sin(np.radians(ed))])
    sg = [np.sign(e @ np.array([np.cos(np.radians(vd)), np.sin(np.radians(vd))])) for vd in vdeg]
    O = set(range(7)) - {c for (pair, g) in zip(edges, sg) if g > 0 for c in pair}
    I = set(range(7)) - {c for (pair, g) in zip(edges, sg) if g < 0 for c in pair}
    for rho in (1.0005, 1.002, 1.005):
        c = int(colour(x + rho*e)); outer_cols.add(c); viol += c not in O
    for rho in (0.995, 0.998, 0.9995):
        c = int(colour(x + rho*e)); inner_cols.add(c); viol += c not in I
print(f"    Lemma 8.1 strip conclusion on this colouring: violations = {viol} (expect 0)")
if viol: fails.append("Lemma 8.1 conclusion violated on hex colouring")
print(f"(iii) colours met just outside / inside the unit circle about x: {sorted(outer_cols)} / {sorted(inner_cols)}")
print("     With k=7 the two-of-three-edges strip uses the FOUR outsiders, not two: the binary state s(e) of Sec. 8.4,")
print("     the two-colour alternation of Lemma 8.6, and the 3-label region of Lemma 8.8 all depend on k=5 (two outsiders).")
print("RESULT:", "OK" if not fails else fails)
sys.exit(1 if fails else 0)
```
Output (`hex7.out`):
```
(i) monochromatic unit pairs among 400000 random pairs: 0
    control s=0.55 (hexagon diameter > 1): monochromatic unit pairs = 1224 (must be > 0)
(ii) edges (label pairs) at x: [(2, 3), (0, 2), (3, 0)]; triangle labels [0, 2, 3]; outsiders [1, 4, 5, 6]
    Lemma 8.1 strip conclusion on this colouring: violations = 0 (expect 0)
(iii) colours met just outside / inside the unit circle about x: [1, 4, 5, 6] / [1, 4, 5, 6]
     With k=7 the two-of-three-edges strip uses the FOUR outsiders, not two: the binary state s(e) of Sec. 8.4,
     the two-colour alternation of Lemma 8.6, and the 3-label region of Lemma 8.8 all depend on k=5 (two outsiders).
RESULT: OK
```

### lean_cross.py
```python
import itertools
X="X"
def valid(w): return all(w[j]!=w[(j+1)%6] for j in range(6)) and all(not(w[j]!=X and w[(j+3)%6]!=X and w[j]!=w[(j+3)%6]) for j in range(6))
def cross1(w,u):  # Lean FourWordCross w u : forall j, w j != 0 -> u(j+1) != w j and u(j-1) != w j
    return all(w[j]==X or (u[(j+1)%6]!=w[j] and u[(j-1)%6]!=w[j]) for j in range(6))
W=["".join(t) for t in itertools.product("XUV",repeat=6) if valid("".join(t))]
mixed=[w for w in W if {j%2 for j in range(6) if w[j]==X}=={0,1}]
print("one-directional (Lean FourWordCross) isolation:", all([u for u in W if cross1(w,u)]==[w] for w in mixed))
```
Output (`lean_cross.out`):
```
one-directional (Lean FourWordCross) isolation: True
```
