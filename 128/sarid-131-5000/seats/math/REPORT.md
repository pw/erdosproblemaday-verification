# Seat MATH: report on Sarid, "Sparse halves in triangle-free graphs: a bound of 131/5000", Sections 2–4

## 1. VERDICT
**HOLDS AS READ.** Sections 2–4 reduce Theorem 1.1 correctly to two inputs: BCL Thm 2(a) (an explicit hypothesis) and the Prop 3.1 certificate (CERT seat's scope). I found no FATAL and no GAP. There are three exposition slips; none changes a verdict.

## 2. Findings, most severe first
No FATAL. No GAP. The three exposition slips are in §4.

Each task, with its verdict, how I checked it, and its label:

- **Lemma 2.1 (β ≤ β\*) — HOLDS AS READ (a).**
  - The pair shift is affine, or concave when {x,y} is an edge, so an endpoint is no worse than t = 0.
  - A minimiser exists because the domain is compact, so one with fewest fractional coordinates exists.
  - Mass n/2 with one fractional coordinate forces that coordinate to be 1/2 and n to be odd. Then |{f=1}| = ⌊n/2⌋ and e(S)/n² ≤ cost.
  - Odd n and the n/2-vs-⌊n/2⌋ mismatch are handled correctly.
  - Test: 400 random (graph, fractional half) pairs with n ≤ 13, rounded by the paper's procedure. 0 cost increases, 0 wrong set sizes (`sections234.py` → `sections234.log`).

- **Lemma 2.2 — HOLDS AS READ (a).**
  - Corollary 4.2 needs only the direction D₂(G(k)) ≥ k²D₂(G), and that is the direction the multilinearity argument proves. The ≤ direction is the trivial lift.
  - The β\*, ρ and hom(C₄) identities are proved correctly but unused downstream.
  - G(k) is triangle-free: two twins are non-adjacent, so a triangle would sit in three classes and project to a triangle of G.
  - k ≥ n₀/n is always achievable.
  - Test: brute force over 59 graphs at k = 2 and 26 graphs at k = 3. 0 violations of D₂, hom(C₄) or e scaling.
  - The quantifier reading of BCL ("for n large enough") does not matter (b). Even the weakest reading, D₂ ≤ (1/23.5 + o(1))n², gives D₂(G)/n² ≤ 2/47 for every G via G(k) with k → ∞. That in turn implies the Lean `BCLEventual` with N = 1.
  - Consistency check, not a proof (d): max D₂(G)/n² over all 12,172 triangle-free graphs on ≤ 10 vertices is 1/25 (C₅), below 2/47. Because the ratio is invariant under blow-up, a small graph above 2/47 would refute BCL outright.

- **Lemma 3.2 and the normalisation question — HOLDS AS READ (a).** No mismatch anywhere:
  - The paper defines t = hom/n⁴.
  - Lean has `c4Hom := trace((adjMatrix ℚ)^4)` (`lean/Erdos128/ExternalInputs.lean:36`). `C4FlagCertificate` is n²·H₄ ≥ 8m³ − 2γmn⁴, which is exactly t ≥ ρ³ − γρ.
  - The verifier's `target_coefficient` averages ab·bc·cd·da over the 720 orderings. That is the injective closed-walk density, which equals the hom density on graphons. The step graphon of G gives exactly hom/n⁴.
  - Clebsch: trace(A⁴) = 625 + 10·1 + 5·81 = 1040, so t = 65/4096 = ρ³ − (3/64)ρ, and equality holds. Under a 3× (Razborov-style) normalisation Clebsch would read 195/4096 and not be tight (`exact.log`).
  - Razborov's C₄ samples 4 points with repetition and asks for a graph isomorphic to C₄. That is 3t: the three labelled C₄'s are disjoint events, and triangle-freeness makes "subgraph" equal "induced". So his Prop 1.1, β ≤ ρ/8 − C₄/(12ρ), is exactly (3).
  - Identity (4) checked exactly, with Fractions, on every edge of 379 graphs with Δ < n/2. Identity (5), Σ e(N(u),N(v)) = ½·trace(A⁴), checked on all 379, degenerate walks included. 0 failures (`sections234.log`).
  - p ∈ [0,1] and ρ/2 − e(N(u),N(v))/n² ≥ 0 hold as stated.

- **Prop 3.3 — HOLDS AS READ (a, exact rationals; `exact.log`).**
  - γ < 293/6250, with a gap of 249999/5·10¹⁰.
  - 7/484 + 293/25000 = 79203/3025000 < 79255/3025000 = 131/5000.
  - The bound at 7/22 with the true γ is 633593750121/24200000000000 ≈ 0.0261816.
  - At ρ = 5/16 with γ = 3/64 the formula returns exactly 27/1024.
  - The Δ ≥ n/2 case and the decrease for ρ > 1/4 are both correct.

- **Lemma 4.3 — HOLDS AS READ (a), tested (d).**
  - (7) is right: e_x = p²R_xU_x.
  - The weights w_xR_x sum to 1; the left side of (8) averages to exactly σ; 2R³/(R²+1) − (2R−1) = (R−1)²/(R²+1); and 2 − σ ≥ σ.
  - Test on 207 weighted graphs: random bipartite, random blow-ups of C₅/Petersen/Clebsch with edge deletions, geng −t samples on ≤ 8 vertices, greedy random triangle-free graphs, Dirichlet weights, plus 7 regular graphs with uniform weights.
    - min over graphs of (max_x S_x − 4μ³) = −1.4·10⁻¹⁷, i.e. 0 up to rounding, at C₅ uniform.
    - min of max S/(4μ³) = 1.000000000000. Equality holds on every regular uniform graph tested (C₅, Petersen, Clebsch, Andrásfai 3/4, C₇, Möbius–Kantor).
  - **Mutation control:** with 4.01μ³ the test FAILS (−1.1·10⁻⁴). It also fails on every uniform regular graph above, where the slack is exactly 0.
  - The lemma does not use triangle-freeness: 0 violations on 300 random non-triangle-free weighted graphs (`lemma43_44.log`).

- **Lemma 4.4 — HOLDS AS READ (a), tested (d).**
  - (10) needs N(x) independent, which triangle-freeness gives.
  - The barycentric weights make the linear term, ψ included, cancel exactly. The average equals A(α) − t₊t₋S_x.
  - The three-case product formula and t₊t₋ ≥ L(α) are correct.
  - The α > 1/2 symmetry is legitimate: t₊(1−α) = t₋(α), and the product involves only the interval, not ψ.
  - d < 1 because x ∉ N(x) and w_x > 0.
  - Test: 14,800 (graph, α, ψ, admissible x) cases. Every admissible x was tried, not just one; α ∈ (0,1) included values near 0 and 1; ψ at scales 0.01, 1 and 100.
    - worst relative slack of (9): +9.1·10⁻⁹;
    - 0 profiles outside [0,1], 0 weighted-mean errors;
    - average identity error 4·10⁻¹⁵;
    - three-case formula error 4·10⁻¹⁶, for α on both sides of 1/2.
  - **Mutation control:** K₆,₆ uniform with α = 0.15 and ψ = 0 is an exact equality case (5.625·10⁻³ = 4Lμ³). Using 1.01·L FAILS.

- **§4.2 — HOLDS AS READ (a), tested end to end (d).**
  - Masses: n(1−s)/2 + a·n(1+s)/2 = n/2, and c(1+s) = 1.
  - (13) holds exactly, in Fractions, on 272 (graph, bipartition) pairs, using optimal and arbitrary bipartitions.
  - (12) and the edge mass of G[Y] being 4c²I_Y both check out.
  - The perturbed ambient halves are feasible and cost ≤ B_i − L(a)μ³/c². Minimum slack is 0, attained only at a = 0 where L = 0; for a > 0 it is +4.5·10⁻⁵ over 237 pairs (`sec42_detail.log`).
  - **Equality instance and mutation** (`sec42_mutation.log`): G[Y] = K₄,₄ with |X| = 5, so a = 3/16. The achieved saving divided by L(a)μ³/c² is 1.000000000000. Inflating it by 1% FAILS, and so does dropping the 1/(4c²) factor. The normalisation is exactly right.
  - Relaxing (ρ, I) to (ρ₀, I₀) is legitimate in both places:
    - in B₁, the coefficients a/2 ≥ 0 and c > 0;
    - in the domain, the true μ = 4c²I_Y ≤ 4c²I ≤ 4c²I₀, so the true (a, μ) lies in the relaxed domain;
    - B₂ and the saving do not involve ρ or I.

- **Lemma 4.5 — HOLDS AS READ (a/d), by an independent route (`lemma45.log`).**
  - Brute 2001×2001 grid over the true domain a ∈ [0, ½], μ ∈ [0, 4I₀c²]: max F = 0.0261658 at a = 0.2110, μ at its cap.
  - Exact-rational 201×201 grid: max 0.0261108.
  - scipy Nelder–Mead from 6 starts: **max F = 0.026170019100 at a = 0.21103118 (= 88/417), μ = cap**.
  - Exact value F(a\*, μ\*) = 137600613254398/5257948522194369 ≈ 0.0261700191, which is below 131/5000 by 3.0·10⁻⁵.
  - For 501 values of a, a dense 1-D search in μ puts the argmax within 4·10⁻⁷ of min(ν(a), 4I₀c²).
  - sympy confirms h′, g₁′, g₂′ and E₃′ symbolically (difference 0). Every displayed constant reproduces: 455/36696, 28/417, 2107/312500 < 7/1000, 17983/6250000 < 1/300, 256/2209, 48/2209, 18424/173889, 4606/173889 < 2649/100000, and the saving > 29/100000.
  - The intro claim |Y|/|X| = 417/241 at a\* is correct.

- **Edge cases and hidden hypotheses — none found (a).**
  - ρ > 0 is used only for ρ ≥ 7/22. n = 1 is trivial. Connectedness is never used.
  - X = ∅ (s = 1, a = c = ½) is fine.
  - a = 0 gives L = 0 and F ≤ I₀/2. μ = 0 gives F = 0.
  - d = 1 is impossible. The perturbation never leaves [0,1], because t± are defined as the exact feasible radii; 0 violations in tests.
  - The ρ ≤ 7/22 and ρ ≥ 7/22 branches overlap at 7/22, so every graph is covered.

## 3. What I recomputed, and by which route
- **Exact rationals** (`exact.py`): every constant in Prop 3.3 and Lemma 4.5; the Clebsch numbers; sympy derivative identities.
- **Independent maximisation** (`lemma45.py`): F over its domain by grid, exact grid and scipy. Balancing remark:
  - The crossing of the high-density bound and the low-density maximum is at **ρ = 0.3183491**, value **0.02617585** (also solved to 30 digits in `extras.py`).
  - Splitting at 7/22 costs 5.7·10⁻⁶. The total cost of stating 131/5000 is 2.4·10⁻⁵, matching the paper's "about 2·10⁻⁵".
- **Randomised tests with mutation controls** for Lemmas 2.1, 2.2, 3.2, 4.3, 4.4 and §4.2 (`lemma43_44.py`, `sections234.py`, `sec42_mutation.py`).
- **Decorrelated probe of Prop 3.1** in the hom normalisation (d, not a proof; `prop31_probe_ratio.log`):
  - Minimised (t − ρ³ + (3/64)ρ)/ρ over vertex weights (SLSQP, analytic gradient) for every triangle-free graph on ≤ 9 vertices and every connected one on 10 (≈ 12.2k graphs), plus Clebsch, Clebsch minus a vertex or an edge, Andrásfai 2–8, Möbius–Kantor, C₇/C₉/C₁₁ and Petersen.
  - The minimum is ≥ 0 everywhere, with equality only at uniform Clebsch. Next smallest: 6.6·10⁻⁴ at Clebsch minus a vertex, ρ = 0.3196.
  - Second-order weight perturbations of Clebsch increase g in both eigen-directions.
  - (My first run, minimising g itself, collapsed to the trivial ρ → 0 point and was uninformative. The g/ρ run replaces it; same sign for ρ > 0.)
- **Correction to the host's framing in COMMON.md:** the host says "the whole gain lives in the ρ < 7/22 branch". It does not. The ρ ≥ 7/22 branch also depends on new content.
  - Prop 3.1 (t ≥ ρ³ − (3/64)ρ) is **not** Razborov's Thm 3.1(a) (t ≥ ρ²/2 − (27/256)ρ in t units).
  - Their difference is ρ(16ρ−5)(16ρ−3)/256. Both are tight at Clebsch, but with slopes 63/256 vs 53/256.
  - Fed into Lemma 3.2, Razborov's inequality gives β\* ≤ 27/1024 for every ρ, which is above 131/5000 (`razborov_vs_prop31.log`).
  - So the new cubic certificate is load-bearing there. If both inequalities hold, the minimal-C₄ envelope has a corner at ρ = 5/16.
  - The paper never claims Prop 3.1 is Razborov's, so this is not a defect of the paper. It does mean the certificate deserves full CERT scrutiny.
  - Slack available: any γ ≤ 4(131/5000 − 7/484) ≈ 0.0469488 would still work, against 3/64 = 0.046875.

## 4. Exposition notes (none change a verdict)
1. **Lemma 4.5** (claim.txt:438; tex:630) — "the first exceeding the second for µ > ν(a) and the second exceeding the first for µ < ν(a)."
   - The directions are swapped. At μ = 0 the first quantity is P > 0 and the second is 0.
   - Numerically, at a = 0.15: μ = ν/2 gives 0.0428 vs 0.0128; μ = 1.5ν gives 0.0083 vs 0.0383.
   - The next sentence, "For µ ≤ ν(a), where the minimum equals µ/4", is correct. So the argument is unaffected.
2. **Lemma 3.2 remark** (claim.txt:197; tex:296) — "This is Proposition 1.1 of [12], stated there for β rather than for the relaxation β\*".
   - Razborov's β is itself the fractional relaxation: "A half in a graph G with n vertices is a function µ : V(G) → [0,1] such that Σµ(v) = n/2 … β(G) = min(β(G,µ) | µ is a half)" (razborov.txt:183–192).
   - So Prop 1.1 is literally the β\* statement. For odd n, Razborov's β ≥ the paper's integral β, so all comparisons stand.
3. **Balancing remark** (claim.txt:87; tex:142) — "Numerically that value is near 0.3184".
   - The crossing is 0.318349, which rounds to 0.3183. The value 0.026176 is right. Nit.
4. **Lemma 2.1 wording** — "If f_x, f_y ∉ {0,1}": this tacitly means x ≠ y. In Lemma 4.5, "we used L(a) ≤ 1/4 and (12)" also uses c ≤ 1. Both trivial.
5. **Intro claims checked by brute force** (`extras.log`):
   - β(C₅(k)) = 0, 1/50, 1/75, 1/50 for k = 1, 2, 3, 4, consistent with "1/50 whenever the blow-up factor is even".
   - β(Petersen(k)) = 1/50 for k = 1, 2.
   - The certificate has 34 terms, all with positive weights.

## 5. What I could not check, and why
- **BCL Theorem 2(a):** COULD NOT CHECK. The source is a 6-page extended abstract with a flag-algebra proof sketch, and it is a declared hypothesis. Recorded quote: "Let G be a triangle-free graph on n vertices. Then, for n large enough, (a) D₂(G) ≤ n²/23.5" (bcl.txt). §2 explains why its quantifier form is immaterial.
- **Prop 3.1 as a proof:** COULD NOT CHECK here; that is CERT's seat. I covered only the normalisation, which matches, and a numerical probe, which found no counterexample. Averaged-square semantics, flag indexing, and host-by-host domination are not checked by me.
- **The Lean build and axiom audit:** LEAN's seat. I read only the definitions of `c4Hom`, `C4FlagCertificate`, `BCLCutCertificate` and `BCLEventual`; each matches the paper.
