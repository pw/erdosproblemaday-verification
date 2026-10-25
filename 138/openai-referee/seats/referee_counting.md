# Referee report — seat `counting` — 03-counting.tex (§3, printed pp. 7–9)

Paper: OpenAI, "Quantitative Superexponential Bounds for van der Waerden Numbers" (23 Sep 2026), PDF sha256 `042acea33a57b58d17600a9ec5e0d8d6f424787c5edf28b9d8d5f9bd9297bd18` (re-hashed, matches `/tmp/oaimath/160/paper.sha256`).
Text read: the TeX source `build/sections/03-counting.tex` in full (220 lines); for dependencies and consumers, `02-setup.tex` in full, `04-outer.tex` in full, `05-dichotomy.tex` in full, `06-perturbation.tex` lines 1–180, `01-introduction.tex` lines 60–192. I matched printed numbering against `paper.txt`: count:arrangement = **Lemma 3.1** (p. 7), count:global = **Lemma 3.2** (p. 7), count:eligible = **Definition 3.3** (p. 8), count:local = **Lemma 3.4** (pp. 8–9). Lean sources were **read as text only**: `Arrangement.lean`, `ComparisonOutputs.lean`, `GlobalLabelWords.lean`, `AnchoredPatternDefinitions.lean`, `AnchoredPatterns.lean`, `AdaptiveMesh.lean` (head), `AdaptiveMeshBreakpoints.lean` (statements). No lean or lake was run.

## Verdict for this scope: **HOLDS AS READ**

I checked every step of §3 by hand. Exact finite checks, each with a control that fails, agree with the arrangement bound, the scalar-word determination claim, the width-independence of the stationary count, and the final arithmetic. I found **no FATAL issue and no GAP**. The objections below are COSMETIC or provenance notes. The most useful thing for the other seats is **Objection 5**: the Lean formalization does **not** prove Lemma 3.1, 3.2 or 3.4 with the constants and exponents printed here. It proves weaker polynomial forms (exponent 14D instead of 6D in Lemma 3.4). Those weaker forms also suffice, so the theorem is unaffected. But "Lemma 3.4 as printed is Lean-verified" would be an overclaim.

## Status of every item in scope

| Item (TeX label / printed number / page) | Status |
|---|---|
| Opening paragraph and the Stanley citation (p. 7) | VERIFIED LINE BY LINE; citation checked against the source (see the citation table) |
| Lemma `count:arrangement` / Lemma 3.1 / eq. (3.1) `count:arrangement-bound`, p. 7 | **VERIFIED LINE BY LINE** (strict-region induction, the zero-sign case, both inequalities, the subset restriction); finite check A |
| Lemma `count:global` / Lemma 3.2 / eq. (3.2) `count:global-bound`, p. 7 | **VERIFIED LINE BY LINE** (3k²F lines, determination by signs incl. equality, independent-coordinates relaxation, F = \|U\|+\|V\|, every O(·) and the final o(M)); finite check B |
| eq. (3.3) `count:coordinate-periods` and the stationary/rotating paragraph, p. 8 | VERIFIED (uses `setup:dilation` = Lemma 2.1, whose proof I re-read: the full ℓ-primary part of h divides λ, so s ∈ {1} ∪ (h_0, ∞), t = 0 included) |
| Definition `count:eligible` / Def. 3.3 / eq. (3.4) `count:local-paths`, p. 8 | **VERIFIED LINE BY LINE**, every clause (see §3 below); compared clause by clause with Lean `EligibleRealization`: identical |
| Lemma `count:local` / Lemma 3.4 / eqs. (3.5) `count:local-bound`, (3.6) `count:anchored-scalar`, pp. 8–9 | **VERIFIED LINE BY LINE**; finite checks C and D |
| Dependencies from §2: `mesh:width` (L2.3), `mesh:neighbors` (L2.4), `mesh:truncated` (L2.5) | VERIFIED LINE BY LINE as used here (owned by the `setup` seat); numerically re-checked on a literal-formula surrogate mesh (check C(a),(b)) |
| Consumers: Prop `outer:coloring` (use of T_glob, Lemma 3.4); `dichotomy:main` longer-period case (membership in Def. 3.3); `perturb:signatures` (Lemma 3.1 with e = 3) | SKIMMED for interface only. The interfaces match: T_glob counts full-label words of all progressions; Lemma 3.4 counts (t, pattern) pairs, one second-family event each; Lemma 3.1 holds for every e |

## Line-by-line notes (what I checked and why it holds)

### 1. Lemma count:arrangement (Lemma 3.1)
- **Strict regions.** "when a new hyperplane is added, every region it splits meets that hyperplane in a different region of the induced arrangement, whose dimension is at most e−1. Induction on s and e, followed by Pascal's identity, gives the stated bound."
  - A region R of the old arrangement that meets the new hyperplane H is split into exactly two pieces, because R is open and convex.
  - The map R ↦ R∩H sends distinct split regions to distinct regions of the induced arrangement {H∩H′ : H′∩H a proper hyperplane of H}. That arrangement has ≤ s−1 members; a repeated copy of H, or an H′ parallel to H, contributes nothing.
  - So r(s,e) ≤ r(s−1,e) + r(s−1,e−1), with r(0,e) = r(s,0) = 1, and Pascal's rule gives Σ_{j≤e} C(s,j). This is exactly Stanley's Lemma 2.1 recurrence, read as an inequality.
  - "Repeated hyperplanes create no additional regions": correct, since a repeat splits no region.
  - "A strict sign set is convex … so each strict sign vector corresponds to one region": the set is an intersection of open half-spaces. It is convex, hence connected, and it is a union of regions, so it is exactly one region.
- **Zero signs.** Let Z be the zero set of a realized vector and A = ∩Z ≠ ∅, of codimension d.
  - The normals of Z span a d-dimensional space. Any d of them with independent normals cut out an affine subspace of codimension d that contains A, so that subspace equals A.
  - Every hyperplane containing A vanishes at the realizing point, so Z = {H : H ⊇ A}.
  - The map (chosen d-subset, strict sign vector on A of the hyperplanes not containing A) → sign vector is well defined and injective.
  - On A ≅ ℝ^{e−d}, a hyperplane not containing A either meets A in a hyperplane of A or misses A (constant sign; the text does not mention this case). So the strict count is ≤ Σ_{j≤e−d} C(s,j).
  - The first inequality of (3.1) follows by summing over d.
- **Second inequality.** C(s,d)C(s,j) ≤ (s+1)^{d+j} ≤ (s+1)^e because d+j ≤ e. The number of pairs (d,j) with d+j ≤ e is (e+1)(e+2)/2 ≤ (e+1)².
- **Restriction to a subset.** Restricting the parameter space can only remove realized vectors. ✔
- **Finite check A** (exact Fourier–Motzkin oracle with strict, non-strict and equality constraints; 690 random arrangements with forced repeats, parallels and concurrencies; e = 1, 2, 3):
  - every count is ≤ B1 ≤ B2;
  - for e = 2 three independent methods agree on every instance (FM, exact face enumeration, Zaslavsky's V+E+R);
  - for e = 1 the count equals 2r+1.
  - Controls fail as they should:
    - the strict-only bound applied to ternary vectors (73 > 22);
    - (s+1)^e without the (e+1)² factor (73 > 49);
    - the e = 2 bound misapplied to a 3-parameter family (577 > B1(2,8) = 137; 1161 > 9·11² = 1089 at s = 10).

### 2. Lemma count:global (Lemma 3.2)
- **Setup of each scalar coordinate.** x_i and y_i = λx_i are homomorphisms, so the coordinate-i sample at n_j is (a + jb) mod 1 with a, b ∈ [0,1) the representatives of the value at n_0 and of the step d.
- **Range and comparisons.** a + jb ∈ [0, k). Comparing with every τ + z, −1 ≤ z ≤ k, places the real value between consecutive lifts of endpoints. Every U- and V-interval is a left-closed arc [τ_i, τ_{i+1}) in increasing circle order (the V convention puts 0 and the cut in the interval on their right), so the signs including equality fix the label.
- **Line count.** There are (k+2)·k·F ≤ 3k²F lines for k ≥ 1. The z = −1 and z = k comparisons are redundant but harmless.
- **Per-coordinate bound.** With e = 2, (e+1)² = 9, giving ≤ 9(3k²F+1)² words per scalar coordinate.
- **Product over coordinates.** Letting the 2D (start, step) pairs vary independently can only add words, so T_glob ≤ [9(3k²F+1)²]^{2D}. Using F = \|U\|+\|V\| as a common endpoint budget for both partitions is fine.
- **Orders of magnitude.**
  - \|U\| = k²λ and \|V\| = 2m = O(k³ log k) (mesh:width, via R ≤ (D+1) log q = O(k log k)).
  - Hence log F ≤ 2 log k + log λ + O(log k).
  - log T_glob ≤ 2D(log 9 + 2 log(3k²F+1)) = O(D(log k + log λ)).
  - With log λ ≤ h_0 log(2M) = D² log(2M): D log λ = O(k^{3/10} log k), and this is o(k^{1/2}) ≤ o(M). ✔
- **Finite check B** (exact face enumeration of the (a,b)-arrangement inside the half-open box, six tiny partitions with k ≤ 6, F ≤ 3):
  - the word is a function of the sign vector on all face points plus 3000 random points;
  - #words ≤ #sign vectors ≤ B1(2,s) ≤ 9(3k²F+1)².
  - **Control:** comparing only against τ (no integer lifts) does **not** determine the word (1713–3199 clashes per case). The k = 2, F = 1 case has one label, so it cannot clash; it is a trivial case, not a failed control.

### 3. Definition count:eligible (Def. 3.3) — every clause
- **Stationary vs rotating.** Stationary means s_i = 1, i.e. h \| λt_i, so the rational part of the Y-step is an integer. Rotating means s_i > h_0 (setup:dilation). This depends only on (h,t).
- **"Regular" with no rotating coordinates.** "if there are no rotating coordinates, every position is regular". Then the word has no ∗, and (i) demands that all h labels be distinct.
- **Regularity is read off the word.** It is visible from the ∗ positions, so different realizations of one word have the same regular set, and "the pattern" is well defined. "different realizations of one word do not define additional patterns" ✔.
- **Clause (i).** It supplies l(E) ≥ h/2 distinct labels to the second-family event. Since h > h_0 ≥ 1, it forces at least one regular position, so (iii) is never vacuous.
- **Clause (ii).** It gives absolute drift bounds where the mesh is uniform (U) or truncated (rotating V_η).
- **Why clause (iii) is relative to the interval width.** Stationary coordinates are not truncated, so their V-cells near the cut can be as small as ≈ Hα. An absolute bound \|v_i\| ≤ H would let a target sweep through ≈ log(H/α)/H cells, and α = q^{−(D+1)} would enter the count.
  - Check C(d) shows this directly. With \|b\| ≤ H, the reachable label count grows 335 → 557 → 889 as α = 2^{−20} → 2^{−30} → 2^{−45}. Under clause (iii) it stays at 3.
  - So (iii) is load-bearing for "independent of q", and it is stated correctly.
- **Deliberate enlargements (harmless).** The definition also omits y = λx, v = λu and gcd(t,h) = 1. The text says "an enlarged family".
- **Lean match.** Lean `EligibleRealization` (AnchoredPatternDefinitions.lean) has exactly these five fields: regular_many, regular_injective, first_drift, rotating_drift, and stationary_drift at every regular z.

### 4. Lemma count:local (Lemma 3.4)
- **Re-anchoring.** Y_z − Y_{z0} = ((z−z0)/h)(λt+v) mod 1, and similarly for X, so (3.6) is exact. Here \|z−z0\|/h ≤ (h−1)/h < 1. The anchor z0 carries β, so it is not ∗ and is therefore regular. The retained constraints are:
  - a lies in β's interval in that coordinate;
  - \|b\| ≤ H_x for the first system (from (ii));
  - \|b\| ≤ \|I\| for stationary coordinates (from (iii) at the regular z0);
  - \|b\| ≤ H for rotating coordinates (from (ii)).
  
  All of these are fixed by (β, h, t, z0).
- **First system.** For fixed z the target range is a real interval of length ≤ H_x + 2H_x = 3H_x. All lifts of U-endpoints form H_xℤ, because H_x^{−1} = k²λ ∈ ℤ. A closed interval of length 3H_x contains ≤ 4 lattice points, and those points decide the lattice cell, hence the U label. τ_z = (z−z0)t_i/h need not be an integer; that is irrelevant for a lattice. ✔
- **Stationary.**
  - τ_z = (z−z0)λt_i/h ∈ ℤ because h \| λt_i.
  - The target mod 1 is within distance < \|I\| of a point of I, so it lies in N(I).
  - N(I) is a closed arc of length 3\|I\| ≤ 6H < 1 (k ≥ 3) holding ≤ 49 endpoints (mesh:neighbors).
  - For a point of N(I), its label is decided by its position among the endpoints *inside* N(I). Consecutive such endpoints bound sub-arcs inside one cell, and the two end sub-arcs lie in the cells straddling the ends of N(I). The text says only "at most 49 mesh endpoints are relevant" and does not spell this out (Objection 2).
  - For fixed z the real range [lift(I) + τ_z ± \|I\|] has length < 1, so each circle endpoint has exactly one lift in it.
  - Check C(a) gives max 4 endpoints in N(I) on the surrogate. Check C(c) confirms determination by the lifted N(I)-endpoints for anchors from width 3·10⁻² down to 6·10⁻¹¹ (the cell next to the cut). The control with unlifted endpoints clashes.
- **Rotating.**
  - The range length is < 2H + 2H = 4H < 1.
  - mesh:truncated gives ≤ 16004D breakpoints of V_η on that arc, the value at a breakpoint included. Its proof checks out: ≤ 2 components of {ρ ≥ η}, spacing ≥ Hη/4, (16/η + 2) + 2 = 16000D + 4.
  - Each breakpoint has one lift because the length is < 1.
  - Check C(b): max 157 ≤ 16004 for D = 1. Check C(e): 114 outputs for every α, while the untruncated control grows with log(1/α). Check C(f): determination holds in exact 2D.
- **"magnitude of τ_z introduces no factor".** The lines are fixed per (t, z0, z), and how many there are does not depend on τ_z. ✔
- **Line count.** ≤ max(4, 49, 16004D)·h ≤ 16004Dh lines per coordinate. Lemma 3.1 with e = 2 gives 9(16004Dh+1)² ≤ 9·16005²(Dh)² = C_0(Dh)² with C_0 = 2,305,440,225.
- **"No additional regular-position mask is needed".**
  - Position z is ∗ ⇔ some rotating ρ < η ⇔ some rotating V_η output = ∗.
  - Otherwise the rotating outputs equal V(Y), and together with the U and untruncated stationary outputs they form L(X_z, Y_z).
  
  So the tuple of 2D scalar sequences determines the word. ✔
- **Product and final arithmetic.** The pattern lies in the image of a product of 2D sets of size ≤ C_0(Dh)² each. Adding h^D choices of t and ≤ h anchors gives:
  - h^{D+1}[C_0(Dh)²]^{2D} = C_0^{2D}D^{4D}h^{5D+1}, an identity, checked exactly for D ≤ 8, h ≤ 200;
  - this is ≤ (CDh)^{6D} with C = ⌈C_0^{1/3}⌉ = **1322**, using D, h ≥ 1.
  - Controls: C−1 fails at (D,h) = (1,1); exponent 5D fails.
- **Independence of the constant.** C does not depend on q, λ, β, D or r. ✔
- **Range of h.** The h-range h_0 < h ≤ 2M is never used in the proof; the bound holds for every h ≥ 1.

## Objections

1. **COSMETIC (exposition) — Lemma 3.1 proof, p. 7.** "Induction on s and e, followed by Pascal's identity, gives the stated bound." and "the remaining hyperplanes impose strict signs in dimension e−d."
   - Missing details: the base cases (s = 0 or e = 0: one region), and the case of a remaining hyperplane parallel to A (it misses A and has constant sign on A, so it is not a hyperplane of A).
   - Neither affects the bound. Fix: add one sentence each.
2. **COSMETIC (exposition) — Lemma 3.4, stationary case, p. 9.** "Modulo one every target belongs to N(I) from mesh:neighbors, and at most 49 mesh endpoints are relevant."
   - "Relevant" is undefined. The proof also needs the fact that a point's label in the closed arc N(I) is determined by comparisons with the endpoints *in* N(I) under the left-closed convention. That is true, by the sub-arc argument in §4 above, and the Lean proves it (`endpoints_determine_label`).
   - Also unstated: "3\|I\| < 1" uses \|I\| ≤ 2H = 2k^{−2} from mesh:width.
   - Fix: one sentence.
3. **COSMETIC — the printed PDF names every cross-reference "Theorem".** Examples on pp. 7–9: "so Theorem 3.1 bounds the number of scalar words", "By Theorem 2.1, a rotating coordinate", "Modulo one every target belongs to N(I) from Theorem 2.4", "Apply Theorem 2.5 to its image".
   - All of these point to Lemmas, and elsewhere to Definition 3.3 ("Theorem 3.3", p. 9) and Proposition 4.2 ("Theorem 4.2").
   - A reader looking for "Theorem 3.1" finds Lemma 3.1. This is a cleveref configuration issue. Fix: set the \crefname entries.
4. **COSMETIC — Lemma 3.2 proof, p. 7.** "comparisons with all τ+z for −1 ≤ z ≤ k" and "at most 3k²F lines".
   - The z = −1 and z = k comparisons are never needed, since a+jb ∈ [0,k).
   - The count (k+2)kF ≤ 3k²F needs k ≥ 1, which is not stated. Harmless.
5. **Provenance note (not a defect of the human proof; relevant to the `whole`/`sources` seats).** The Lean does **not** certify §3's printed constants or exponents:
   - `Arrangement.lean::card_realizedSigns_le` proves `(e + 2) ^ 2 * (s + 1) ^ (2 * (e + 1))` (Sauer–Shelah on a homogeneous lift), not (e+1)²(s+1)^e. For e = 2 that is 16(s+1)⁶ vs the paper's 9(s+1)².
   - `GlobalLabelWords.lean::exists_exact_word_family` proves `16 * (3 * k ^ 2 * card + 1) ^ 6` per scalar coordinate, vs the paper's 9(3k²F+1)².
   - `AnchoredPatterns.lean::card_through_le` proves `(16005 * D * h) ^ (14 * D)`, vs the paper's (CDh)^{6D}.
   
   The weaker forms still give o(1) in (outer:second-weight), since 14D log(CDh)/h ≤ 14 log(CD³)/D → 0. So the formal chain is fine. But Lemma 3.1 as printed, and the exponents 2 (Lemma 3.2) and 6D (Lemma 3.4), are human-proof-only. My hand check and finite checks A–D support them. Fix: none needed in the paper; just do not describe these lemmas as "formally verified as stated".
6. **UNCLEAR-but-harmless — scope of the statement of Lemma 3.4.** "for every h_0<h≤2M". The proof uses neither bound, and the rotating/stationary dichotomy s_i > h_0 is never used in the count; the lemma holds for all h ≥ 1. No fix needed. I note it because a reader may hunt for where h > h_0 enters; it enters only in §4–§5.

**No FATAL and no GAP objection in this scope.** Count of hedge phrases in 03-counting.tex: "standard" (l. 7: backed by the included proof and by Stanley) and "follow from" (l. 85: "The remaining bounds follow from setup:orders and M ≥ k^{1/2}"). I checked the second: D³ log(2M) = O(k^{3/10} log k) = o(k^{1/2}). There is no "clearly", "similarly" or "the same argument" in §3.

## Brief items (e), (i), (j) restricted to §3

**(e) Every "large k" inequality used in §3.** All hold for every k ≥ 3, given §2's facts:

| Where | Inequality | Holds from |
|---|---|---|
| Lemma 3.2 | (k+2)kF ≤ 3k²F | k ≥ 1 |
| Lemma 3.2 | log F = O(log k + log λ) | k ≥ 2 |
| Lemma 3.2 | O(D³ log M) = o(M) | asymptotic. With the paper's own explicit bound, the first-family exponent log(kT_glob) − (δM−1)/32 is still positive at k = 10²⁰ and negative by k = 10²⁵ (check E(3)) |
| Lemma 3.4, stationary | 3\|I\| ≤ 6H < 1 | k ≥ 3 |
| Lemma 3.4, rotating | 4H < 1 | k ≥ 3 |
| mesh:neighbors (used) | H ≤ 1/8 | k ≥ 3 |
| mesh:width (used) | α ≤ 1/4 and R ≥ 1 | q ≥ P > k ≥ 3 |
| Lemma 3.4 line count | 49 ≤ 16004D and 4 ≤ 16004D | D ≥ 1 |
| Lemma 3.4 arithmetic | h^{D+1}C_0^{2D}D^{4D}h^{4D} ≤ (CDh)^{6D} | all D, h ≥ 1 |

- None is reversed. None depends on r or on the progression.
- Informational: with the explicit C = 1322, the consumer bound Σ_{h>D²}(CDh)^{6D}e^{−h/64} < 1 first holds near D ≈ 2·10⁴, i.e. k ≈ 10⁴³ (check E(3)). K_0 is therefore astronomically large but finite and absolute. The paper only claims "sufficiently large".

**(i) Quantifiers.**
- C is a numerical constant (1322 works).
- Lemmas 3.1–3.4 have no hidden dependence on q, λ, β, D or r. q and λ enter only through F (inside a logarithm) in Lemma 3.2, and not at all in Lemma 3.4.
- The thresholds in §3 are finitely many and explicit.

**(j) Prove-too-much.**
- Nothing in §3 caps c: log T_glob depends on q only through log m ≈ log(k²(D+1) log q). With c = 1 Lemma 3.2 still gives O(k^{3/10} log k).
- Lemma 3.4 does not see q at all.
- The cap on c comes from §6 (2c − γ/80 < 0), outside this scope. §3 claims nothing beyond what it proves.

## Finite checks (scripts verbatim, outputs verbatim, controls)
All scripts are in `/tmp/oaimath/160/seats/counting_checks/`. They use exact `fractions.Fraction` arithmetic; mpmath at 60 digits is used only to evaluate the mesh formulas, which are then frozen as exact rationals. Measured runtimes (/usr/bin/time): 6.0 s, 15.0 s, 7.7 s, 22.7 s, 0.07 s; peak memory 15–23 MB.

One honest note on a discarded control. I first tried a control "C4": the lemma misapplied to non-affine `frac(a+jb)` vs τ comparisons, with a grid lower bound.
- That run took **72 s**, over the one-minute budget, and was **inconclusive**: lower bounds of 356 and 1990, below 9(s+1)² = 1521 and 9801 at k = 12 and 16.
- I deleted it rather than report a control that did not fail. The "no integer lifts" failure is instead shown as a determination failure in check B.

### Shared module: exact 2-D face enumeration
`/tmp/oaimath/160/seats/counting_checks/arr2d.py`
```python
"""Exact face enumeration for a line arrangement in a closed axis box (Fractions).
Lines are (A, B, C) meaning A*a + B*b = C.  Returns one rational sample point in the
relative interior of every face (vertex / edge / region) of the arrangement formed by
the given lines together with the 4 box lines, restricted to the closed box."""
from fractions import Fraction as Fr
from itertools import combinations

def norm_line(A, B, C):
    A, B, C = Fr(A), Fr(B), Fr(C)
    if A != 0:
        s = A
    elif B != 0:
        s = B
    else:
        raise ValueError("degenerate line")
    return (A / s, B / s, C / s)

def face_points(lines, box):
    x0, x1, y0, y1 = [Fr(v) for v in box]
    L = set(norm_line(*l) for l in lines)
    L |= {(Fr(1), Fr(0), x0), (Fr(1), Fr(0), x1), (Fr(0), Fr(1), y0), (Fr(0), Fr(1), y1)}
    L = sorted(L)
    inbox = lambda p: x0 <= p[0] <= x1 and y0 <= p[1] <= y1
    on = {i: set() for i in range(len(L))}
    verts = set()
    for i, j in combinations(range(len(L)), 2):
        A1, B1, C1 = L[i]; A2, B2, C2 = L[j]
        det = A1 * B2 - A2 * B1
        if det == 0:
            continue
        p = ((C1 * B2 - C2 * B1) / det, (A1 * C2 - A2 * C1) / det)
        if inbox(p):
            verts.add(p); on[i].add(p); on[j].add(p)
    pts = set(verts)
    for i, (A, B, C) in enumerate(L):
        vs = sorted(on[i], key=(lambda p: p[0]) if B != 0 else (lambda p: p[1]))
        for p, q in zip(vs, vs[1:]):
            m = ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)
            pts.add(m)
            eps = None
            for j, (A2, B2, C2) in enumerate(L):
                if j == i:
                    continue
                f = A2 * m[0] + B2 * m[1] - C2
                g = A2 * A + B2 * B
                if f == 0:
                    raise RuntimeError("midpoint on another line")
                if g != 0:
                    r = abs(f) / abs(g)
                    eps = r if eps is None or r < eps else eps
            eps = Fr(1) if eps is None else eps / 2
            for sgn in (1, -1):
                pt = (m[0] + sgn * eps * A, m[1] + sgn * eps * B)
                if inbox(pt):
                    pts.add(pt)
    return pts

def sgn(x):
    return (x > 0) - (x < 0)

def sign_vector(lines, p):
    return tuple(sgn(A * p[0] + B * p[1] - C) for (A, B, C) in lines)
```

### Check A — Lemma 3.1 sign-vector counts (FM oracle; e=2 cross-checked by faces and Zaslavsky; controls C1–C3)
`/tmp/oaimath/160/seats/counting_checks/check_arrangement.py`
```python
"""Check Lemma count:arrangement (printed Lemma 3.1, p.7):
#realized ternary sign vectors of s affine hyperplanes in R^e
   <= B1 = sum_{d=0}^e C(s,d) sum_{j=0}^{e-d} C(s,j) <= B2 = (e+1)^2 (s+1)^e.
Oracle 1: exact Fourier-Motzkin feasibility (strict/non-strict/equality), DFS over sign vectors.
Oracle 2 (e=2): exact face enumeration in a large box (arr2d.face_points).
Oracle 3 (e=2): Zaslavsky count  V + sum_L (v_L+1) + (1 + n + sum_p (t_p - 1))  over distinct lines.
Oracle 4 (e=1): 2r+1 for r distinct roots.
Controls that MUST fail are at the bottom."""
import random, sys, time
from fractions import Fraction as Fr
from math import comb
sys.path.insert(0, '/tmp/oaimath/160/seats/counting_checks')
from arr2d import face_points, sign_vector, norm_line

def B1(e, s): return sum(comb(s, d) * sum(comb(s, j) for j in range(e - d + 1)) for d in range(e + 1))
def B2(e, s): return (e + 1) ** 2 * (s + 1) ** e
def strict_only(e, s): return sum(comb(s, j) for j in range(e + 1))

# ---------- exact Fourier-Motzkin with strictness ----------
# constraint: (coef tuple, const, rel) meaning coef.x + const  rel 0, rel in '<','<=','=='
def feasible(cons, nvar):
    cons = [(list(c), Fr(d), r) for c, d, r in cons]
    # eliminate equalities
    while True:
        eq = next((k for k, (c, d, r) in enumerate(cons) if r == '=='), None)
        if eq is None:
            break
        c, d, r = cons.pop(eq)
        v = next((i for i in range(nvar) if c[i] != 0), None)
        if v is None:
            if d != 0:
                return False
            continue
        new = []
        for c2, d2, r2 in cons:
            if c2[v] != 0:
                f = c2[v] / c[v]
                c2 = [c2[i] - f * c[i] for i in range(nvar)]
                d2 = d2 - f * d
            new.append((c2, d2, r2))
        cons = new
    for v in range(nvar):
        pos = [x for x in cons if x[0][v] > 0]
        neg = [x for x in cons if x[0][v] < 0]
        zer = [x for x in cons if x[0][v] == 0]
        for cp, dp, rp in pos:
            for cn, dn, rn in neg:
                a, b = cp[v], -cn[v]
                c = [b * cp[i] + a * cn[i] for i in range(nvar)]
                zer.append((c, b * dp + a * dn, '<' if '<' in (rp, rn) else '<='))
        cons = zer
    for c, d, r in cons:
        if r == '<' and not d < 0: return False
        if r == '<=' and not d <= 0: return False
    return True

def count_signs_FM(H, e):
    """H: list of (normal tuple, const) for f(x)=n.x+c. Count realized sign vectors."""
    out = []
    def rec(i, cons, sig):
        if i == len(H):
            out.append(tuple(sig)); return
        n, c = H[i]
        for s in (-1, 0, 1):
            if s == -1: k = (n, c, '<')
            elif s == 0: k = (n, c, '==')
            else: k = (tuple(-x for x in n), -c, '<')
            if feasible(cons + [k], e):
                rec(i + 1, cons + [k], sig + [s])
    rec(0, [], [])
    return out

def rand_arr(e, s, rng, coef=2):
    H = []
    while len(H) < s:
        r = rng.random()
        if H and r < 0.15:                      # repeated hyperplane (possibly re-scaled / re-oriented)
            n, c = rng.choice(H); f = rng.choice([-2, -1, 2, 3])
            H.append((tuple(f * x for x in n), f * c)); continue
        n = tuple(Fr(rng.randint(-coef, coef)) for _ in range(e))
        if all(x == 0 for x in n): continue
        H.append((n, Fr(rng.randint(-coef, coef))))
    return H

def zaslavsky2(H):
    lines = sorted(set(norm_line(n[0], n[1], -c) for n, c in H))
    from itertools import combinations
    pts = {}
    for i, j in combinations(range(len(lines)), 2):
        A1, B1_, C1 = lines[i]; A2, B2_, C2 = lines[j]
        det = A1 * B2_ - A2 * B1_
        if det == 0: continue
        p = ((C1 * B2_ - C2 * B1_) / det, (A1 * C2 - A2 * C1) / det)
        pts.setdefault(p, set()).update((i, j))
    V = len(pts)
    E = sum(1 + sum(1 for p in pts if i in pts[p]) for i in range(len(lines)))
    R = 1 + len(lines) + sum(len(t) - 1 for t in pts.values())
    return V + E + R

def faces2(H):
    lines = [(n[0], n[1], -c) for n, c in H]
    # big box containing every vertex and the foot point of every line strictly inside
    from itertools import combinations
    big = Fr(1)
    for (A1, B1_, C1), (A2, B2_, C2) in combinations(lines, 2):
        det = A1 * B2_ - A2 * B1_
        if det != 0:
            big = max(big, abs((C1 * B2_ - C2 * B1_) / det), abs((A1 * C2 - A2 * C1) / det))
    for A, B, C in lines:
        nn = A * A + B * B
        big = max(big, abs(C * A / nn), abs(C * B / nn))
    big = 4 * big + 1
    pts = face_points(lines, (-big, big, -big, big))
    return len({sign_vector(lines, p) for p in pts if -big < p[0] < big and -big < p[1] < big})

rng = random.Random(20261015)
t0 = time.time()
worst = {}
ntests = 0
for e, s_list, reps in [(1, range(1, 9), 40), (2, range(1, 8), 40), (3, range(1, 7), 15)]:
    for s in s_list:
        for _ in range(reps):
            H = rand_arr(e, s, rng)
            cnt = len(count_signs_FM(H, e))
            assert cnt <= B1(e, s) <= B2(e, s), (e, s, cnt, H)
            if e == 1:
                roots = {-c / n[0] for n, c in H}
                assert cnt == 2 * len(roots) + 1, (cnt, roots)
            if e == 2:
                z = zaslavsky2(H); f = faces2(H)
                assert cnt == z == f, (cnt, z, f, H)
            ntests += 1
            worst[(e, s)] = max(worst.get((e, s), 0), cnt)
# general position extremes (maximal counts)
gp = {}
for e, s in [(2, 4), (2, 6), (3, 4), (3, 5)]:
    while True:
        H = [(tuple(Fr(rng.randint(-50, 50)) for _ in range(e)), Fr(rng.randint(-50, 50))) for _ in range(s)]
        if all(any(x != 0 for x in n) for n, c in H): break
    gp[(e, s)] = len(count_signs_FM(H, e))
    assert gp[(e, s)] <= B1(e, s)
print("random arrangements tested:", ntests, " (FM oracle; e=2 also vs face-enumeration and Zaslavsky; e=1 vs 2r+1)")
for (e, s), w in sorted(worst.items()):
    print(f"  e={e} s={s}: max realized={w:4d}  B1={B1(e,s):5d}  B2=(e+1)^2(s+1)^e={B2(e,s):6d}")
print("general position:", {k: (v, B1(*k), B2(*k)) for k, v in gp.items()})

# restriction to a subset: e=2, half-open box [0,1)^2 -- must be <= unrestricted count
for _ in range(20):
    H = rand_arr(2, 6, rng, coef=3)
    lines = [(n[0], n[1], -c) for n, c in H]
    pts = face_points(lines, (0, 1, 0, 1))
    rcnt = len({sign_vector(lines, p) for p in pts if 0 <= p[0] < 1 and 0 <= p[1] < 1})
    assert rcnt <= len(count_signs_FM(H, 2)) <= B1(2, 6)
print("restriction to [0,1)^2: 20 cases, restricted <= unrestricted <= B1: OK")

# ---------------- CONTROLS (each must report a violation) ----------------
print("\nCONTROLS (each line must show a VIOLATION):")
# C1: strict-region bound misapplied to ternary sign vectors
e, s = 2, 6; c = gp[(2, 6)]
print(f" C1 strict-only bound sum_j<=e C(s,j)={strict_only(e,s)} vs ternary count {c}: violated={c > strict_only(e,s)}")
# C2: dropping the (e+1)^2 factor
print(f" C2 (s+1)^e={(s+1)**e} vs ternary count {c}: violated={c > (s+1)**e}")
# C3: the e=2 count misapplied to a 3-parameter family (8 generic planes); see control_c3.py for s=10 vs 9(s+1)^2
H = [(tuple(Fr(rng.randint(-60, 60)) for _ in range(3)), Fr(rng.randint(-60, 60))) for _ in range(8)]
c3 = len(count_signs_FM(H, 3))
print(f" C3 e=2 count B1(2,8)={B1(2,8)} vs 8 generic planes in R^3: {c3}: violated={c3 > B1(2,8)};  correct e=3 bound B1(3,8)={B1(3,8)}: holds={c3 <= B1(3,8)}")
print("time %.1fs" % (time.time() - t0))
```
Output (`check_arrangement.out`):
```
random arrangements tested: 690  (FM oracle; e=2 also vs face-enumeration and Zaslavsky; e=1 vs 2r+1)
  e=1 s=1: max realized=   3  B1=    3  B2=(e+1)^2(s+1)^e=     8
  e=1 s=2: max realized=   5  B1=    5  B2=(e+1)^2(s+1)^e=    12
  e=1 s=3: max realized=   7  B1=    7  B2=(e+1)^2(s+1)^e=    16
  e=1 s=4: max realized=   9  B1=    9  B2=(e+1)^2(s+1)^e=    20
  e=1 s=5: max realized=  11  B1=   11  B2=(e+1)^2(s+1)^e=    24
  e=1 s=6: max realized=  13  B1=   13  B2=(e+1)^2(s+1)^e=    28
  e=1 s=7: max realized=  13  B1=   15  B2=(e+1)^2(s+1)^e=    32
  e=1 s=8: max realized=  13  B1=   17  B2=(e+1)^2(s+1)^e=    36
  e=2 s=1: max realized=   3  B1=    4  B2=(e+1)^2(s+1)^e=    36
  e=2 s=2: max realized=   9  B1=   11  B2=(e+1)^2(s+1)^e=    81
  e=2 s=3: max realized=  19  B1=   22  B2=(e+1)^2(s+1)^e=   144
  e=2 s=4: max realized=  33  B1=   37  B2=(e+1)^2(s+1)^e=   225
  e=2 s=5: max realized=  51  B1=   56  B2=(e+1)^2(s+1)^e=   324
  e=2 s=6: max realized=  73  B1=   79  B2=(e+1)^2(s+1)^e=   441
  e=2 s=7: max realized=  85  B1=  106  B2=(e+1)^2(s+1)^e=   576
  e=3 s=1: max realized=   3  B1=    4  B2=(e+1)^2(s+1)^e=   128
  e=3 s=2: max realized=   9  B1=   15  B2=(e+1)^2(s+1)^e=   432
  e=3 s=3: max realized=  27  B1=   42  B2=(e+1)^2(s+1)^e=  1024
  e=3 s=4: max realized=  65  B1=   93  B2=(e+1)^2(s+1)^e=  2000
  e=3 s=5: max realized= 131  B1=  176  B2=(e+1)^2(s+1)^e=  3456
  e=3 s=6: max realized= 211  B1=  299  B2=(e+1)^2(s+1)^e=  5488
general position: {(2, 4): (33, 37, 225), (2, 6): (73, 79, 441), (3, 4): (65, 93, 2000), (3, 5): (131, 176, 3456)}
restriction to [0,1)^2: 20 cases, restricted <= unrestricted <= B1: OK

CONTROLS (each line must show a VIOLATION):
 C1 strict-only bound sum_j<=e C(s,j)=22 vs ternary count 73: violated=True
 C2 (s+1)^e=49 vs ternary count 73: violated=True
 C3 e=2 count B1(2,8)=137 vs 8 generic planes in R^3: 577: violated=True;  correct e=3 bound B1(3,8)=697: holds=True
time 6.0s
```

### Check A′ — control C3 at the size where 9(s+1)² is exceeded
`/tmp/oaimath/160/seats/counting_checks/control_c3.py`
```python
"""Control C3 at a size where the misapplied bound is actually exceeded.
C3: 10 generic planes in R^3 (exact FM count incl. zero signs) vs the e=2 bound 9(s+1)^2.
"""
import sys, time, random
from fractions import Fraction as Fr
sys.path.insert(0, '/tmp/oaimath/160/seats/counting_checks')
# same exact Fourier-Motzkin oracle as check_arrangement.py, plus de-duplication of derived constraints
from math import comb
def feasible(cons, nvar):
    cons = [(list(c), Fr(d), r) for c, d, r in cons]
    while True:
        eq = next((k for k, (c, d, r) in enumerate(cons) if r == '=='), None)
        if eq is None: break
        c, d, r = cons.pop(eq)
        v = next((i for i in range(nvar) if c[i] != 0), None)
        if v is None:
            if d != 0: return False
            continue
        new = []
        for c2, d2, r2 in cons:
            if c2[v] != 0:
                f = c2[v] / c[v]; c2 = [c2[i] - f * c[i] for i in range(nvar)]; d2 = d2 - f * d
            new.append((c2, d2, r2))
        cons = new
    for v in range(nvar):
        pos = [x for x in cons if x[0][v] > 0]; neg = [x for x in cons if x[0][v] < 0]
        zer = [x for x in cons if x[0][v] == 0]
        for cp, dp, rp in pos:
            for cn, dn, rn in neg:
                a, b = cp[v], -cn[v]
                c = [b * cp[i] + a * cn[i] for i in range(nvar)]
                # normalise to cut duplicates
                zer.append((c, b * dp + a * dn, '<' if '<' in (rp, rn) else '<='))
        # dedupe after normalisation by max |coef|
        seen = {}
        for c, d, r in zer:
            m = max([abs(x) for x in c] + [Fr(0)])
            if m == 0:
                key = (tuple(c), d, r)
            else:
                key = (tuple(x / m for x in c), d / m, r)
            if key in seen and seen[key] == '<': continue
            seen[key] = r
        zer = [(list(k[0]), k[1], k[2]) for k in seen]
        cons = zer
    for c, d, r in cons:
        if r == '<' and not d < 0: return False
        if r == '<=' and not d <= 0: return False
    return True

def count_FM(H, e):
    n = [0]
    def rec(i, cons):
        if i == len(H): n[0] += 1; return
        nn, c = H[i]
        for s in (-1, 0, 1):
            k = (nn, c, '<') if s == -1 else ((nn, c, '==') if s == 0 else (tuple(-x for x in nn), -c, '<'))
            if feasible(cons + [k], e): rec(i + 1, cons + [k])
    rec(0, [])
    return n[0]

t0 = time.time()
rng = random.Random(7)
s = 10
H = [(tuple(Fr(rng.randint(-60, 60)) for _ in range(3)), Fr(rng.randint(-60, 60))) for _ in range(s)]
c3 = count_FM(H, 3)
gen = sum(comb(s, d) * sum(comb(s - d, j) for j in range(3 - d + 1)) for d in range(4))
print(f"C3: s={s} planes in R^3: exact realized={c3} (generic-position formula {gen});"
      f" misapplied e=2 bound 9(s+1)^2={9*(s+1)**2} -> violated={c3 > 9*(s+1)**2};"
      f" correct e=3 bound (e+1)^2(s+1)^e={16*(s+1)**3} holds={c3 <= 16*(s+1)**3}   [{time.time()-t0:.1f}s]")
```
Output (`control_c3.out`):
```
C3: s=10 planes in R^3: exact realized=1161 (generic-position formula 1161); misapplied e=2 bound 9(s+1)^2=1089 -> violated=True; correct e=3 bound (e+1)^2(s+1)^e=21296 holds=True   [14.6s]
```

### Check B — Lemma 3.2 scalar words: exact enumeration, determination by lifted comparisons; control: no lifts
`/tmp/oaimath/160/seats/counting_checks/check_global_words.py`
```python
"""Check Lemma count:global (printed Lemma 3.2, p.7), scalar step: for a circle partition with F endpoints
(half-open arcs [tau_i, tau_{i+1}) in increasing direction), the words (label((a+jb) mod 1))_{0<=j<k},
(a,b) in [0,1)^2, are determined by the ternary signs of a+jb-(tau+z), -1<=z<=k  (<= 3k^2F lines), hence
#words <= #realized sign vectors <= 9(3k^2F+1)^2.  Exact: every face of the arrangement (incl. box lines)
gets a rational sample point, so the realized word set is computed exactly.
Control (must FAIL): comparisons against tau only (z=0, no integer lifts) do NOT determine the word."""
import sys, time, random
from fractions import Fraction as Fr
from math import comb
sys.path.insert(0, '/tmp/oaimath/160/seats/counting_checks')
from arr2d import face_points, sign_vector

def label(x, taus):            # taus sorted in [0,1); arcs [tau_i, tau_{i+1}), last arc wraps
    f = x - (x.numerator // x.denominator)
    idx = -1
    for i, t in enumerate(taus):
        if f >= t: idx = i
    return idx % len(taus)     # f < taus[0] lies in the wrapping arc [tau_F, tau_1 + 1)

def B1(e, s): return sum(comb(s, d) * sum(comb(s, j) for j in range(e - d + 1)) for d in range(e + 1))

t0 = time.time()
rng = random.Random(3)
cases = [(2, [Fr(0)]), (3, [Fr(0), Fr(2, 5)]), (4, [Fr(0), Fr(1, 3), Fr(3, 4)]),
         (5, [Fr(0), Fr(1, 2)]), (4, [Fr(1, 7), Fr(5, 7)]), (6, [Fr(0), Fr(2, 3)])]
for k, taus in cases:
    F = len(taus)
    full = [(Fr(1), Fr(j), t + z) for j in range(k) for t in taus for z in range(-1, k + 1)]
    assert len(full) <= 3 * k * k * F
    pts = [p for p in face_points(full, (0, 1, 0, 1)) if 0 <= p[0] < 1 and 0 <= p[1] < 1]
    # add random rational points as extra probes of the determination claim
    pts += [(Fr(rng.randrange(10**6), 10**6), Fr(rng.randrange(10**6), 10**6)) for _ in range(3000)]
    words, sv2w, ok = set(), {}, True
    for p in pts:
        w = tuple(label(p[0] + j * p[1], taus) for j in range(k))
        words.add(w)
        sv = sign_vector(full, p)
        if sv2w.setdefault(sv, w) != w: ok = False
    nsv = len(sv2w)
    # control: no integer lifts (z = 0 only)
    nolift = [(Fr(1), Fr(j), t) for j in range(k) for t in taus]
    m, clash = {}, 0
    for p in pts:
        w = tuple(label(p[0] + j * p[1], taus) for j in range(k))
        sv = sign_vector(nolift, p)
        if m.setdefault(sv, w) != w: clash += 1
    s = len(full)
    print(f"k={k} F={F} taus={[str(t) for t in taus]}: lines={s} (3k^2F={3*k*k*F}) words={len(words)} "
          f"signvecs={nsv} B1(2,s)={B1(2,s)} 9(3k^2F+1)^2={9*(3*k*k*F+1)**2} "
          f"determined={ok}  CONTROL(no lifts) clashes={clash} -> determination fails={clash>0}")
    assert ok and len(words) <= nsv <= B1(2, s) <= 9 * (3 * k * k * F + 1) ** 2
print("time %.1fs" % (time.time() - t0))
```
Output (`check_global_words.out`):
```
k=2 F=1 taus=['0']: lines=8 (3k^2F=12) words=1 signvecs=5 B1(2,s)=137 9(3k^2F+1)^2=1521 determined=True  CONTROL(no lifts) clashes=0 -> determination fails=False
k=3 F=2 taus=['0', '2/5']: lines=30 (3k^2F=54) words=8 signvecs=54 B1(2,s)=1831 9(3k^2F+1)^2=27225 determined=True  CONTROL(no lifts) clashes=1713 -> determination fails=True
k=4 F=3 taus=['0', '1/3', '3/4']: lines=72 (3k^2F=144) words=69 signvecs=291 B1(2,s)=10441 9(3k^2F+1)^2=189225 determined=True  CONTROL(no lifts) clashes=2841 -> determination fails=True
k=5 F=2 taus=['0', '1/2']: lines=70 (3k^2F=150) words=28 signvecs=178 B1(2,s)=9871 9(3k^2F+1)^2=205209 determined=True  CONTROL(no lifts) clashes=2772 -> determination fails=True
k=4 F=2 taus=['1/7', '5/7']: lines=48 (3k^2F=96) words=16 signvecs=149 B1(2,s)=4657 9(3k^2F+1)^2=84681 determined=True  CONTROL(no lifts) clashes=2391 -> determination fails=True
k=6 F=2 taus=['0', '2/3']: lines=96 (3k^2F=216) words=43 signvecs=346 B1(2,s)=18529 9(3k^2F+1)^2=423801 determined=True  CONTROL(no lifts) clashes=3199 -> determination fails=True
time 7.7s
```

### Checks C/D — Lemma 3.4 on a literal-formula surrogate V-mesh (k=4, D=1): N(I) endpoints, V_η breakpoints, stationary/rotating exact 2-D determination, width-independence; controls: unlifted endpoints, absolute drift, no truncation
`/tmp/oaimath/160/seats/counting_checks/check_local.py`
```python
"""Check Lemma count:local (printed Lemma 3.4, pp.8-9) on a surrogate V-mesh built with the paper's literal
formulas (mesh:definition): R = log(1+1/(2 alpha)), m = ceil(k^2 R), a_l = alpha(e^{lR/m}-1), H = k^{-2},
eta = 1/(1000 D).  Surrogate: k = 4 (H = 1/16), D = 1, alpha in {2^-20, 2^-30, 2^-45}.  Endpoints are exact
rationals (60-digit decimal values of the formulas).
(a) mesh:neighbors: endpoints in N(I) <= 49, |J| >= |I|/16 for J meeting N(I)           [used by stationary case]
(b) mesh:truncated: V_eta breakpoints on any arc of length 4H <= 16004 D                  [used by rotating case]
(c) stationary case, exact 2D: a in I (half-open lift), |b| <= |I|, targets a + tau_z + (z-z0)/h * b with
    INTEGER tau_z: #distinct output sequences <= 9(49h+1)^2, and the output is a function of the signs
    against the lifted endpoints of N(I).  CONTROL: endpoints of I's closure only -> determination fails.
(d) width-independence: one target, max over ALL anchors I of #labels reachable, |b| <= |I| (clause (iii))
    vs CONTROL |b| <= H (absolute drift): the latter grows with log(1/alpha), i.e. with q.
(e) rotating case: one target, |b| <= H, truncated output V_eta: max #outputs is alpha-independent;
    CONTROL without truncation grows with log(1/alpha).
(f) rotating case, exact 2D for anchors with rho >= eta, h = 3."""
import sys, time, bisect, random
from fractions import Fraction as Fr
import mpmath
sys.path.insert(0, '/tmp/oaimath/160/seats/counting_checks')
from arr2d import face_points, sign_vector
mpmath.mp.dps = 60
HALF = Fr(1, 2)

def build_mesh(kk, alpha_exp):
    alpha = mpmath.mpf(2) ** (-alpha_exp)
    R = mpmath.log(1 + 1 / (2 * alpha))
    m = int(mpmath.ceil(kk * kk * R))
    a = [Fr(0)] + [Fr(mpmath.nstr(alpha * (mpmath.exp(l * R / m) - 1), 55)) for l in range(1, m)] + [HALF]
    assert all(x < y for x, y in zip(a, a[1:]))
    pts = set()
    for al in a:
        pts.add((-HALF + al) % 1); pts.add((HALF - al) % 1)
    E = sorted(pts)
    assert len(E) == 2 * m
    return E, Fr(mpmath.nstr(alpha, 55)), m

def arcs(E):   # list of (left, right) real lifts with left in [0,1), right = next endpoint (wrap +1)
    return [(E[i], E[i + 1] if i + 1 < len(E) else E[0] + 1) for i in range(len(E))]

def vlabel(x, E):
    f = x - (x.numerator // x.denominator)
    i = bisect.bisect_right(E, f) - 1
    return i % len(E)

def rho(x):
    f = x - (x.numerator // x.denominator)
    d = abs(f - HALF)
    return min(d, 1 - d)

def lifts_in(E, lo, hi):     # all reals e + n (e in sorted E, n integer) with lo <= e+n <= hi
    out = []
    n0 = lo.numerator // lo.denominator - 1
    for n in range(n0, n0 + int(hi - lo) + 3):
        i = bisect.bisect_left(E, lo - n)
        j = bisect.bisect_right(E, hi - n)
        out.extend(e + n for e in E[i:j])
    return sorted(out)

def count_in_closed_arc(E, lo, hi):   # endpoints (circle points) lying in closed real interval [lo,hi], length<1
    return len(lifts_in(E, lo, hi))

t0 = time.time()
KK, D = 4, 1
H = Fr(1, KK * KK); eta = Fr(1, 1000 * D)
meshes = {ae: build_mesh(KK, ae) for ae in (20, 30, 45)}
for ae, (E, alpha, m) in meshes.items():
    A = arcs(E)
    # (a)
    worstN, worstratio = 0, Fr(10**9)
    for (L, Rr) in A:
        w = Rr - L
        cnt = count_in_closed_arc(E, L - w, Rr + w)
        worstN = max(worstN, cnt)
    # |J| >= w/16 for J whose closure meets N(I): J ranges over arcs overlapping [L-w, R+w] (closed)
    widths = [r - l for l, r in A]
    n = len(A)
    for i, (L, Rr) in enumerate(A):
        w = Rr - L
        for di in range(-8, 9):
            j = (i + di) % n
            l2, r2 = A[j]
            for sh in (-1, 0, 1):
                if l2 + sh <= Rr + w and r2 + sh >= L - w:
                    worstratio = min(worstratio, (r2 - l2) / w)
    # (b) breakpoints of V_eta on arcs of length 4H, arcs starting at every breakpoint
    thr = [(HALF - eta), (HALF + eta) % 1]
    bps = sorted({e for e in E if rho(e) >= eta} | set(thr))
    worstB = 0
    ext = bps + [b + 1 for b in bps]
    for t_i, s0 in enumerate(bps):
        worstB = max(worstB, bisect.bisect_right(ext, s0 + 4 * H) - t_i)
    print(f"alpha=2^-{ae}: 2m={2*m} intervals; (a) max endpoints in N(I)={worstN} (<=49: {worstN<=49}), "
          f"min |J|/|I| over J meeting N(I)={float(worstratio):.4f} (>=1/16: {worstratio>=Fr(1,16)}); "
          f"(b) max V_eta breakpoints on a 4H arc={worstB} (<=16004D: {worstB<=16004*D})")
    assert worstN <= 49 and worstratio >= Fr(1, 16) and worstB <= 16004 * D

# (d) and (e): one target, z0 = 0, z = 1, h = 2 -> c = 1/2
print("(d)/(e) one target c=1/2, max over all anchor intervals of #distinct outputs reachable:")
for ae, (E, alpha, m) in meshes.items():
    A = arcs(E)
    rel = absd = rot_trunc = rot_full = 0
    for (L, Rr) in A:
        w = Rr - L
        # stationary, clause (iii): |b| <= w  -> target range [L - w/2, R + w/2] (R excluded only for b=0, harmless)
        rel = max(rel, count_in_closed_arc(E, L - w / 2, Rr + w / 2) + 1)
        # control: absolute drift |b| <= H
        absd = max(absd, count_in_closed_arc(E, L - H / 2, Rr + H / 2) + 1)
        # rotating: |b| <= H, truncated output (count breakpoints of V_eta in range, +1)
        lo, hi = L - H / 2, Rr + H / 2
        bp = [v for v in lifts_in(E, lo, hi) if rho(v) >= eta] + [v for v in lifts_in([HALF - eta, (HALF + eta) % 1], lo, hi)]
        rot_trunc = max(rot_trunc, len(set(bp)) + 1)
        rot_full = max(rot_full, count_in_closed_arc(E, lo, hi) + 1)
    print(f"  alpha=2^-{ae}: stationary |b|<=|I|: {rel:3d} (<=50: {rel<=50}) | CONTROL stationary |b|<=H: {absd:3d}"
          f" | rotating truncated: {rot_trunc:3d} | CONTROL rotating untruncated: {rot_full:3d}")
print("  (CONTROL columns must grow with log(1/alpha); the clause-(iii) and truncated columns must not)")

# (c) stationary exact 2D
E, alpha, m = meshes[30]
A = arcs(E)
rng = random.Random(11)
idx_cut = [i for i, (l, r) in enumerate(A) if l <= HALF + 0 and r > HALF or (l <= Fr(3, 2) and r > Fr(3, 2))]
picks = sorted(set(idx_cut + [0, len(A) // 4] + [rng.randrange(len(A)) for _ in range(2)]))
h = 4
for i in picks:
    L, Rr = A[i]; w = Rr - L
    for z0 in (0, 2):
        cz = {z: Fr(z - z0, h) for z in range(h)}
        tau = {z: 3 * (z - z0) for z in range(h)}          # integral translations (stationary case)
        lines, lines_ctl = [], []
        maxrel = 0
        for z in range(h):
            if z == z0: continue
            lo, hi = L + tau[z] - abs(cz[z]) * w, Rr + tau[z] + abs(cz[z]) * w
            rel = lifts_in(E, lo, hi)
            maxrel = max(maxrel, len(rel))
            lines += [(Fr(1), cz[z], e - tau[z]) for e in rel]   # a + tau_z + c_z b = e
            # control: the same circle endpoints but NOT lifted into the target range (representatives in [0,1))
            lines_ctl += [(Fr(1), cz[z], (e % 1) - tau[z]) for e in rel]
        pts = [p for p in face_points(lines, (L, Rr, -w, w)) if L <= p[0] < Rr]
        pts += [(L + w * Fr(rng.randrange(10**6), 10**6), w * Fr(rng.randrange(-10**6, 10**6 + 1), 10**6)) for _ in range(600)]
        outs, m1, ok, m2, clash = set(), {}, True, {}, 0
        for p in pts:
            o = tuple(vlabel(p[0] + tau[z] + cz[z] * p[1], E) for z in range(h))
            outs.add(o)
            if m1.setdefault(sign_vector(lines, p), o) != o: ok = False
            if m2.setdefault(sign_vector(lines_ctl, p), o) != o: clash += 1
        bound = 9 * (49 * h + 1) ** 2
        print(f"(c) anchor arc #{i} width={float(w):.3e} rho(left)={float(rho(L)):.3e} z0={z0}: relevant endpoints/target<= {maxrel}"
              f" lines={len(lines)} outputs={len(outs)} <= 9(49h+1)^2={bound}: {len(outs)<=bound}; determined={ok};"
              f" CONTROL(unlifted endpoints) clashes={clash}")
        assert ok and maxrel <= 49 and len(outs) <= bound and clash > 0

# (f) rotating exact 2D, h = 3, anchors with rho >= eta, |b| <= H, truncated outputs
h = 3
cnt = 0
for i in [0, len(A) // 3, 5, len(A) - 40]:
    L, Rr = A[i]
    if rho(L) < eta: continue
    for z0 in (0, 1):
        cz = {z: Fr(z - z0, h) for z in range(h)}
        tau = {z: Fr(7 * (z - z0), 3) for z in range(h)}   # arbitrary non-integral translation (lambda t_i/h)
        lines = []
        for z in range(h):
            if z == z0: continue
            lo, hi = L + tau[z] - abs(cz[z]) * H, Rr + tau[z] + abs(cz[z]) * H
            bp = [v for v in lifts_in(E, lo, hi) if rho(v) >= eta] + lifts_in([HALF - eta, HALF + eta], lo, hi)
            assert len(set(bp)) <= 16004 * D
            lines += [(Fr(1), cz[z], v - tau[z]) for v in sorted(set(bp))]
        if len(lines) > 90: continue
        pts = [p for p in face_points(lines, (L, Rr, -H, H)) if L <= p[0] < Rr]
        def out(p):
            r = []
            for z in range(h):
                x = p[0] + tau[z] + cz[z] * p[1]
                r.append('*' if rho(x) < eta else vlabel(x, E))
            return tuple(r)
        pts += [(L + (Rr - L) * Fr(rng.randrange(10**6), 10**6), H * Fr(rng.randrange(-10**6, 10**6 + 1), 10**6)) for _ in range(400)]
        m1, ok, outs = {}, True, set()
        for p in pts:
            o = out(p); outs.add(o)
            if m1.setdefault(sign_vector(lines, p), o) != o: ok = False
        cnt += 1
        print(f"(f) rotating anchor arc #{i} rho={float(rho(L)):.3f} z0={z0}: lines={len(lines)} outputs={len(outs)}"
              f" <= 9(16004Dh+1)^2: {len(outs) <= 9*(16004*D*h+1)**2}; determined={ok}")
        assert ok
print("time %.1fs" % (time.time() - t0))
```
Output (`check_local.out`):
```
alpha=2^-20: 2m=422 intervals; (a) max endpoints in N(I)=4 (<=49: True), min |J|/|I| over J meeting N(I)=0.8826 (>=1/16: True); (b) max V_eta breakpoints on a 4H arc=157 (<=16004D: True)
alpha=2^-30: 2m=644 intervals; (a) max endpoints in N(I)=4 (<=49: True), min |J|/|I| over J meeting N(I)=0.8826 (>=1/16: True); (b) max V_eta breakpoints on a 4H arc=157 (<=16004D: True)
alpha=2^-45: 2m=976 intervals; (a) max endpoints in N(I)=4 (<=49: True), min |J|/|I| over J meeting N(I)=0.8825 (>=1/16: True); (b) max V_eta breakpoints on a 4H arc=157 (<=16004D: True)
(d)/(e) one target c=1/2, max over all anchor intervals of #distinct outputs reachable:
  alpha=2^-20: stationary |b|<=|I|:   3 (<=50: True) | CONTROL stationary |b|<=H: 335 | rotating truncated: 114 | CONTROL rotating untruncated: 335
  alpha=2^-30: stationary |b|<=|I|:   3 (<=50: True) | CONTROL stationary |b|<=H: 557 | rotating truncated: 114 | CONTROL rotating untruncated: 557
  alpha=2^-45: stationary |b|<=|I|:   3 (<=50: True) | CONTROL stationary |b|<=H: 889 | rotating truncated: 114 | CONTROL rotating untruncated: 889
  (CONTROL columns must grow with log(1/alpha); the clause-(iii) and truncated columns must not)
(c) anchor arc #0 width=3.026e-02 rho(left)=5.000e-01 z0=0: relevant endpoints/target<= 2 lines=6 outputs=7 <= 9(49h+1)^2=349281: True; determined=True; CONTROL(unlifted endpoints) clashes=264
(c) anchor arc #0 width=3.026e-02 rho(left)=5.000e-01 z0=2: relevant endpoints/target<= 2 lines=6 outputs=7 <= 9(49h+1)^2=349281: True; determined=True; CONTROL(unlifted endpoints) clashes=611
(c) anchor arc #161 width=1.306e-06 rho(left)=2.158e-05 z0=0: relevant endpoints/target<= 2 lines=6 outputs=7 <= 9(49h+1)^2=349281: True; determined=True; CONTROL(unlifted endpoints) clashes=612
(c) anchor arc #161 width=1.306e-06 rho(left)=2.158e-05 z0=2: relevant endpoints/target<= 2 lines=6 outputs=7 <= 9(49h+1)^2=349281: True; determined=True; CONTROL(unlifted endpoints) clashes=253
(c) anchor arc #322 width=5.999e-11 rho(left)=0.000e+00 z0=0: relevant endpoints/target<= 2 lines=6 outputs=7 <= 9(49h+1)^2=349281: True; determined=True; CONTROL(unlifted endpoints) clashes=601
(c) anchor arc #322 width=5.999e-11 rho(left)=0.000e+00 z0=2: relevant endpoints/target<= 2 lines=6 outputs=7 <= 9(49h+1)^2=349281: True; determined=True; CONTROL(unlifted endpoints) clashes=602
(c) anchor arc #463 width=3.988e-07 rho(left)=6.191e-06 z0=0: relevant endpoints/target<= 2 lines=6 outputs=7 <= 9(49h+1)^2=349281: True; determined=True; CONTROL(unlifted endpoints) clashes=613
(c) anchor arc #463 width=3.988e-07 rho(left)=6.191e-06 z0=2: relevant endpoints/target<= 2 lines=6 outputs=7 <= 9(49h+1)^2=349281: True; determined=True; CONTROL(unlifted endpoints) clashes=257
(c) anchor arc #573 width=3.829e-04 rho(left)=5.944e-03 z0=0: relevant endpoints/target<= 2 lines=6 outputs=7 <= 9(49h+1)^2=349281: True; determined=True; CONTROL(unlifted endpoints) clashes=606
(c) anchor arc #573 width=3.829e-04 rho(left)=5.944e-03 z0=2: relevant endpoints/target<= 2 lines=6 outputs=7 <= 9(49h+1)^2=349281: True; determined=True; CONTROL(unlifted endpoints) clashes=610
(f) rotating anchor arc #0 rho=0.500 z0=0: lines=19 outputs=32 <= 9(16004Dh+1)^2: True; determined=True
(f) rotating anchor arc #0 rho=0.500 z0=1: lines=14 outputs=37 <= 9(16004Dh+1)^2: True; determined=True
(f) rotating anchor arc #604 rho=0.041 z0=0: lines=7 outputs=8 <= 9(16004Dh+1)^2: True; determined=True
(f) rotating anchor arc #604 rho=0.041 z0=1: lines=4 outputs=6 <= 9(16004Dh+1)^2: True; determined=True
time 22.6s
```

### Check E — final arithmetic of Lemma 3.4 and informational thresholds; controls: C−1, exponent 5D, C₀ too small
`/tmp/oaimath/160/seats/counting_checks/check_arith.py`
```python
"""Arithmetic of count:local (printed Lemma 3.4) and the size of the count:global / count:local quantities
at actual parameters (informational thresholds; the paper only claims 'sufficiently large k')."""
import math, mpmath
from math import comb
C0 = 9 * 16005 ** 2
C = 1
while C ** 3 < C0: C += 1                     # C = ceil(C0^(1/3)), absolute
print("C0 = 9*16005^2 =", C0, "  C = ceil(C0^(1/3)) =", C)
# (1) 9(16004Dh+1)^2 <= C0 (Dh)^2
assert all(9 * (16004 * D * h + 1) ** 2 <= C0 * (D * h) ** 2 for D in range(1, 30) for h in range(1, 300))
bad = [(D, h) for D in range(1, 5) for h in range(1, 5) if 9 * (16004 * D * h + 1) ** 2 > 9 * 16004 ** 2 * (D * h) ** 2]
print("(1) 9(16004Dh+1)^2 <= C0(Dh)^2 on D<30,h<300: OK;  CONTROL C0'=9*16004^2 violated at", len(bad), "of 16 pairs")
# (2) h^{D+1} [C0 (Dh)^2]^{2D} = C0^{2D} D^{4D} h^{5D+1} <= (CDh)^{6D}
ok = True
for D in range(1, 9):
    for h in range(1, 201):
        lhs = h ** (D + 1) * (C0 * (D * h) ** 2) ** (2 * D)
        assert lhs == C0 ** (2 * D) * D ** (4 * D) * h ** (5 * D + 1)
        ok &= lhs <= (C * D * h) ** (6 * D)
print("(2) identity and inequality <= (CDh)^{6D} for D<=8, h<=200:", ok)
c1 = [(D, h) for D in range(1, 9) for h in range(1, 201)
      if h ** (D + 1) * (C0 * (D * h) ** 2) ** (2 * D) > ((C - 1) * D * h) ** (6 * D)]
c2 = [(D, h) for D in range(1, 9) for h in range(1, 201)
      if h ** (D + 1) * (C0 * (D * h) ** 2) ** (2 * D) > (C * D * h) ** (5 * D)]
print("    CONTROL C-1 violates at", len(c1), "pairs (e.g.", c1[:2], ");  CONTROL exponent 5D violates at", len(c2), "pairs")

# (3) informational: where do the 'o(.)' statements that consume count:global/count:local actually bite?
mpmath.mp.dps = 30
c = mpmath.mpf(10) ** -5; delta = mpmath.mpf(1) / 10
def glob_terms(k):
    k = mpmath.mpf(k)
    D = mpmath.ceil(k ** (mpmath.mpf(1) / 10)); M = mpmath.ceil(mpmath.sqrt(k)); h0 = D * D
    loglam = h0 * mpmath.log(2 * M)                 # paper's bound log(lambda) <= h0 log(2M)
    logq = c * k / D * mpmath.log(k) + mpmath.log(2 * k * k)
    R = (D + 1) * logq + 1                          # R = log(1+q^{D+1}/2) <= (D+1)log q (+1 slack)
    logF = mpmath.log(k * k * mpmath.e ** loglam + 2 * (k * k * R + 1))
    logT = 2 * D * (mpmath.log(9) + 2 * (mpmath.log(3) + 2 * mpmath.log(k) + logF + mpmath.log(1 + mpmath.e ** (-logF))))
    first = mpmath.log(k) + logT - (delta * M - 1) / 32  # log of k T_glob e^{-(delta M-1)/32}
    return D, M, logT, first
print("(3) first-family exponent log(k T_glob) - (delta M - 1)/32 (paper's explicit T_glob bound, lambda bound):")
for ex in (20, 25, 28, 30, 35, 40, 50):
    D, M, logT, first = glob_terms(mpmath.mpf(10) ** ex)
    print(f"    k=1e{ex}: D={int(D)} log T_glob<={mpmath.nstr(logT,6)}  M={mpmath.nstr(M,6)}  exponent={mpmath.nstr(first,6)}")
print("    second-family per-label sum S(D)=sum_{h>D^2} (CDh)^{6D} e^{-h/64} with the explicit C:")
for D in (1000, 3000, 5000, 8000, 10000, 20000):
    f = lambda h: 6 * D * mpmath.log(C * D * h) - h / 64
    # terms decrease for h > D^2 once f' < 0: f'(h) = 6D/h - 1/64 < 0 iff h > 384 D
    h1 = D * D + 1
    if h1 > 384 * D:
        # geometric tail bound: sum <= exp(f(h1)) / (1 - exp(max ratio)), ratio exp(f(h+1)-f(h)) <= exp(6D/h1 - 1/64)
        r = 6 * D / mpmath.mpf(h1) - mpmath.mpf(1) / 64
        logS = f(h1) - mpmath.log(1 - mpmath.e ** r)
        print(f"      D={D}: log S(D) <= {mpmath.nstr(logS,6)}  (k = D^10 ~ 1e{int(10*math.log10(D))})")
    else:
        print(f"      D={D}: D^2 <= 384 D, terms not yet decreasing at h=D^2")
```
Output (`check_arith.out`):
```
C0 = 9*16005^2 = 2305440225   C = ceil(C0^(1/3)) = 1322
(1) 9(16004Dh+1)^2 <= C0(Dh)^2 on D<30,h<300: OK;  CONTROL C0'=9*16004^2 violated at 16 of 16 pairs
(2) identity and inequality <= (CDh)^{6D} for D<=8, h<=200: True
    CONTROL C-1 violates at 200 pairs (e.g. [(1, 1), (1, 2)] );  CONTROL exponent 5D violates at 1600 pairs
(3) first-family exponent log(k T_glob) - (delta M - 1)/32 (paper's explicit T_glob bound, lambda bound):
    k=1e20: D=100 log T_glob<=9.49506e+7  M=1.0e+10  exponent=6.37006e+7
    k=1e25: D=317 log T_glob<=3.75606e+9  M=3.16228e+12  exponent=-6.12606e+9
    k=1e28: D=631 log T_glob<=3.30933e+10  M=1.0e+14  exponent=-2.79407e+11
    k=1e30: D=1000 log T_glob<=1.40929e+11  M=1.0e+15  exponent=-2.98407e+12
    k=1e35: D=3163 log T_glob<=5.18822e+12  M=3.16228e+17  exponent=-9.83024e+14
    k=1e40: D=10000 log T_glob<=1.86979e+14  M=1.0e+20  exponent=-3.12313e+17
    k=1e50: D=100000 log T_glob<=2.33031e+17  M=1.0e+25  exponent=-3.12498e+22
    second-family per-label sum S(D)=sum_{h>D^2} (CDh)^{6D} e^{-h/64} with the explicit C:
      D=1000: log S(D) <= 151841.0  (k = D^10 ~ 1e30)
      D=3000: log S(D) <= 421087.0  (k = D^10 ~ 1e34)
      D=5000: log S(D) <= 591534.0  (k = D^10 ~ 1e36)
      D=8000: log S(D) <= 639132.0  (k = D^10 ~ 1e39)
      D=10000: log S(D) <= 526580.0  (k = D^10 ~ 1e40)
      D=20000: log S(D) <= -1.82231e+6  (k = D^10 ~ 1e43)
```

## Citation table (scope: §3)

| Cited result | What the paper says it gives | What the source says (quote; `refs/stanley2007_sp06.txt`, fetched from the bib URL https://www.cis.upenn.edu/~cis6100/sp06stanley.pdf) | Verdict |
|---|---|---|---|
| Stanley 2007, Lemma 2.1 | "the standard hyperplane-arrangement region count" (p. 7), i.e. the recurrence behind ≤ Σ_{j≤e} C(s,j) | "Lemma 2.1. Let (A, A′, A″) be a triple of real arrangements with distinguished hyperplane H0. Then r(A) = r(A′) + r(A″) …" Proof: "r(A) equals r(A′) plus the number of regions of A′ cut into two regions by H0 … R′ ∩ H0 ∈ R(A″)" | **MATCH**. This is the recurrence the paper's own proof uses, read as an inequality for counting |
| Stanley 2007, Proposition 2.4 | the general-position value of that count | "Proposition 2.4. (general position) Let A be an n-dimensional arrangement of m hyperplanes in general position. … In particular, if A is a real arrangement, then r(A) = 1 + m + C(m,2) + ··· + C(m,n)" | **MATCH**, with a caveat. Prop. 2.4 is an *equality for general position*. The *inequality for arbitrary* arrangements, and repeated hyperplanes (Stanley's arrangements are sets), come from the paper's own induction, which the paper supplies ("The elementary proof below also counts equality signs"). The numbering is checked in the sp06 notes, the version at the bib's own URL; the bib entry gives the IAS/Park City vol. 13 (2007) book version, pp. 389–496, which I did not fetch |

## Summary for this scope
Lemma 3.1 (the arrangement engine), Lemma 3.2, Definition 3.3 and Lemma 3.4 are correct as written, and I checked each line by line. Their constants are absolute and independent of q, λ, β, D and r. Exact finite checks with failing controls support every load-bearing step. The relative drift clause (iii) is what makes the stationary count independent of the anchor width: with an absolute drift the count grows like log(1/α), i.e. with q. The truncation V_η does the same job for rotating coordinates. Objections are cosmetic: unstated base cases and parallel case, an undefined "relevant", every cross-reference printed as "Theorem". There is one provenance note: the Lean proves only weaker exponents for §3 (14D instead of 6D), which suffice downstream. **Verdict: HOLDS AS READ.**
