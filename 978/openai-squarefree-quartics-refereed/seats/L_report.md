# Seat L: the Lean formalization read as a source artefact (Erdős #978, OpenAI "Squarefree values of quartics…")

**Scope.** I read the source of the 63 files in `OAI/NumberTheory/PowerFree/*.lean`, the comparator challenge `ComparatorChallenges/PowerFreeValues.lean` with its JSON, `lakefile.lean`, `lake-manifest.json` and `lean-toolchain`, and the scope note `lean_doc_020.md`. I compared all of this against the paper (LaTeX and PDF text), the live #978 page and `fc_978.lean`.

**What I did not do.** I did not run lean or lake (per the brief). Everything below about the proof is a reading of the source. Whether it compiles, and which axioms it uses, is for the coordinator's kernel replay.

**Provenance.** All 67 files I read (the 63 Lean files, the challenge, lakefile, manifest, toolchain) are byte-identical to `git show HEAD:lean/<path>` at 1581d4c. None of them changed between adc7f1241, the commit FC links to, and HEAD. Size: 23,269 lines, 906 theorems/lemmas, and **zero comments or docstrings anywhere in the closure**. Because there are no comments, the file-to-paper mapping in §2 is by content, not by any cross-reference in the code.

## 1. Statement fidelity

`Model.lean`, definition by definition:

| def | Lean | Paper / intended meaning | Verdict |
|---|---|---|---|
| `PowerFree k a` | `∀ p prime, ¬ (p:ℤ)^k ∣ a` | k-power-free; negatives allowed; 0 excluded (`p^k ∣ 0`) | correct |
| `rho f q` | `#{a ∈ range q : (q:ℤ) ∣ f(a)}` | ρ_f(q) = #{a ∈ ℤ/qℤ : f(a) ≡ 0} | correct |
| `count f k X` | `#{n ∈ Icc 1 ⌊X⌋₊ : PowerFree k (f n)}` | S_{f,k}(X), inputs 1 ≤ n ≤ X | correct |
| `LocallyAdmissible f k` | `∀ p prime, rho f (p^k) < p^k` | (1.1). f(n) mod p^k depends only on n mod p^k, so ρ(p^k) < p^k ⇔ ∃ n, p^k ∤ f(n) ⇔ "no fixed p^k divisor". It uses the exponent d−2, not d−1, so it avoids the forum's X⁶+33X⁵+… trap. | correct |
| `localFactor`, `densityConstant` | `1 − ρ(p^k)/p^k`; `∏' p : Nat.Primes` | c_{f,k} | correct |
| `DensityStatement` | `Multipliable ∧ 0 < ∏' ∧ (count − c·X) =o[atTop] X` over real X | S = cX + o_f(X), c > 0 | correct, and guarded |

**The tprod trap is guarded.** If the family were not multipliable, `∏'` would silently be 1; the statement asserts `Multipliable` explicitly, which rules that out. There is a second trap: Mathlib's `Multipliable` also admits `HasProd f 0` (a product diverging to 0 counts as multipliable). That one is closed by the separate `0 < densityConstant` conjunct. Positivity is also proved for real, not assumed. `densityConstant_converges_pos` (Sieve.lean:168) gets it as `exp(∑ log)`, using:
- `localFactor_pos`, which follows from `LocallyAdmissible`;
- summability of ρ(p^k)/p^k, which comes from ρ(p^k) ≤ d for p ∤ Res(f, f′) (`rho_prime_pow_le_degree`, a Hensel argument) and k ≥ 2.

**The hypotheses are satisfiable, so the theorem is not vacuous. Worked instance: f = X⁴+2.**
- It is Eisenstein at 2 and monic, so it is irreducible in ℤ[X], and by Gauss irreducible over ℚ.
- natDegree = 4, so k = 2.
- LocallyAdmissible: f(0) = 2, and p² ≥ 4 does not divide 2. So ρ(p²) ≤ p² − 1 for every p.
- Numerical check using the Lean definitions literally (`L_work/sanity.py`):
  - ρ(4) = 0 and ρ(9) = 2; no prime p < 200 violates the condition.
  - The Euler product over p < 3·10⁵ gives c ≈ 0.75668.
  - The empirical proportion of squarefree n⁴+2 for n ≤ 20000 (sieving p² with p < 2·10⁴) is 0.75635.

  So the statement agrees with the data. The same argument works for X^d + 2 for every d ≥ 4.

**Against the paper.**
- `density` is Theorem 1.1. It carries the hypothesis d ≤ 8 but never uses it.
- `allDegrees` is Corollary 1.2, word for word in content: f irreducible over ℚ, d ≥ 4, k = d−2, no fixed prime k-th-power divisor, no primitivity or sign condition, and positive integer inputs.
- `DensityStatement` also asserts c > 0, as the paper does.

**Against #978 (live page) and FC.**
- `allDegrees` strictly implies FC's `parts.ii`, `parts.iii` and `variants.sub_two`. Its hypotheses are weaker: no k ≠ 2^l, no positive leading coefficient, and irreducibility over ℚ only.
- Its conclusion is stronger: positive density rather than just infinitude.
- The bridge is routine but **it is not formalized anywhere**: FC's three statements are still `sorry`, and FC's `formal_proof` link points at a theorem with a different statement. The bridge needs four steps:
  1. `Irreducible f` in ℤ[X] with natDegree ≠ 0 gives `IsPrimitive` (`Irreducible.isPrimitive`), and then irreducibility of the ℚ-map (`IsPrimitive.Int.irreducible_iff_irreducible_map_cast`).
  2. FC's `∃ n:ℕ, ¬p^k ∣ f n` gives `LocallyAdmissible`, by reducing n mod p^k.
  3. c > 0 together with `count − cX = o(X)` means count is unbounded, so the set is infinite.
  4. FC's `Powerfree k m` (`x^k ∣ m → IsUnit x`) is equivalent to OAI's `PowerFree k m` for k ≥ 1. For `parts.iii`, `Squarefree (n^4+2)` in ℕ corresponds to `PowerFree 2` in ℤ via `Nat.squarefree_iff_prime_squarefree` and `Int.natCast_dvd_natCast`.

  Classification: **EXPOSITION** (an unformalized but trivial bridge).

## 2. Architecture

**Imports.** The closure is a single linear chain of 63 files: each imports exactly its predecessor. The base, `Model`, imports only `Mathlib`. No other package from the lakefile is imported.

**How `Main` is assembled.**
- `allDegrees` → `density_ge_four`.
  - If d ≥ 5 → `density_ge_five` (MediumDegree), which branches:
    - d ≥ 9 → `density_ge_nine` (HighDegree);
    - 5 ≤ d ≤ 8 → `medium_degree_dyadic_tail`.
  - If d = 4 → `quartic_dyadic_tail`.
- Every branch first normalizes f = a·g with g primitive and positive-leading (`exists_primitive_positive_normalization`). It then turns a power-saving bound on the dyadic tail of g into the density statement for f via:
  - `dyadic_tail_limit_of_power_saving`,
  - `global_tail_of_dyadic_tail` (halving),
  - `tailCount_scalar_eq` (for N ≥ |a|, the tail of a·g equals the tail of g),
  - the sieve `densityStatement_from_large_prime_tail` (Proposition 2.1 / Lemma 2.3). The local factors used are f's own.
- `dyadicTailCount f k M` is #{n ∈ (M, 2M] : ∃ prime p > M with p^k ∣ f(n)}. This is exactly the set in Proposition 1.4, and every branch gives a fixed δ (not one depending on f), stated in the next block.

**Does the Lean prove d ≥ 9 itself? Yes, without Browning or Xiao.** `density_ge_nine` uses the paper's own §11.1 device:
- The direct surface f(x) = y·z^k in ℤ³, covered by two weight boxes, (1, 2, 11/10) and (1, 13/10, 13/10). The case split is p ≤ X^{1.1} versus p > X^{1.1}, and `high_degree_two_boxes` needs d ≥ 9.
- Both boxes feed the Lean's own affine counting theorem, with surface thresholds √(b′η′/D) < 0.499.
- The result is a dyadic tail ≪ X^{1−1/2000}.
- There are no names Browning, Xiao, Heath-Brown, Hooley or Reuss anywhere in the code.

The power saving the Lean proves in each branch:

| Degree | Tail bound |
|---|---|
| d = 4 | X^{1−3/1000} |
| 5 ≤ d ≤ 8 | X^{1−3/1000} |
| d ≥ 9 | X^{1−1/2000} |

**Does the Lean follow the paper's route? Only partly. It is a shorter route through a subset of the paper.**

What it shares with the paper:
- Lemma 4.1: the balanced factorization α^kβ = μ(n−θ), with |N(α)| = p·N(𝔠) and unit balancing (`balanced_arithmetic`).
- A uniform affine counting theorem with adaptive auxiliary primes, of the same shape as Theorem 3.1: Hilbert-function input per subvariety, exponent ∑ E_h + ε.
- Weighted-Hilbert thresholds. For 2 ≤ h ≤ d it uses the paper's §7 "general" coefficient (kU+V)^{h−1}·min(U,V)/(U^hV^h), i.e. Ψ_h(U,V; min(U,V)).
- A quartic surface analysis and curve alternatives (§8 Proposition 8.1, §9 Lemma 9.1 and Proposition 9.2), but with **different alternatives**:
  - the surface bound uses min(2U,V)(2U+V)/(U²V²) or (V+4U)/(2UV²);
  - the curve slope is min(2/U, max(1/U, g/V)) with g = (d−1)(k−1) = 3 for d = 4, where the paper uses g = 4.

What it does differently: **the Lean never performs an archimedean (Bombieri–Pila/Taylor) determinant cut.** It applies the counting theorem directly to the whole (d+1)-dimensional affine norm variety in ℤ^{2d}, with r = d+1:
- coordinates = the α- and β-coefficients in a fixed integral basis (`IntegralEmbeddingChart`);
- equations a_i^k b_i − a_0^k b_0 = θ_0 − θ_i;
- this requires a **top-dimensional threshold** at h = d+1, δ_{d+1} = (U^dV^d/(kU+V)^{d−1})^{1/(d+1)} (`norm_full_real_hilbert_uniform`, `quartic_full_*`). The paper never needs this threshold.

The parameters it uses:

| Degree | Boxes | Exponents U, V | Certificate | Exponent achieved |
|---|---|---|---|---|
| 5 ≤ d ≤ 8 | one box for all of η ∈ (1, d/k] | U = 1/3, V = 2/5 | envelope in CurveThresholds | .997 / .971 / .950 / .943 |
| d = 4 | 100 bins η ∈ [1+j/100, 1+(j+1)/100] | U = η₊/4, V = 1−η₋/2 | `QuarticComponents` (`decide`) | ≤ .995 (j < 60), ≤ .984 (j ≥ 60) |

I re-checked every certificate inequality exactly in Python (`L_work/cert.py`). All are true. The tightest full-threshold margin is 0.00059, at j = 0. For d = 5 the exponent sum lands at exactly 997/1000, which is allowed (the inequality is ≤).

Exceptional fibres are handled arithmetically:
- fixed n: at most one point;
- fixed α: at most |Q|·d + 1 points, using ρ(p^k) ≤ d and p^k > X;
- "radial" fibres α′ = cα: c must be rational, and prime norms force c = ±1 (`prime_norm_proportional_sign`).

**File → printed section map.**

| Lean files | Paper |
|---|---|
| Model | §1 statements (Thm 1.1, Cor 1.2) |
| Sieve | §2 (Prop 2.1 sieve transfer, Lemma 2.3 sign/content, dyadic summation of Prop 1.4) |
| NormalMonomials, HilbertGrowth, Jacobians, IntegralKernels, GenericCuts, PureCuts, DegreeBudgets, PointInterpolation, IntegerPatches, PatchBounds, AdaptiveRanks, PrimeBlocks, RegularBlocks, DeformedRoots, ResidueBounds, StoppingTrees, AdaptiveFibres, ResidueRelations, HilbertSimplex, WeightedRelations, PrimePools, DegreeSchedules, AffineCounting | §3 (Thm 3.1 → `physical_affine_count`; Lemma 3.2 patches; Lemma 3.3 residue cut; Lemma 3.4 deletion; counting tree). These 23 files are 8,452 lines, 36% of the code. |
| WeightedSlabs, WeightedHypersurfaces, ComplexValues, CurveAlternatives, SelectedPrimes, SurfaceCounting, HighDegree | weighted hypersurface Hilbert functions; Lemma 9.1 (rational-function values); §11.1 direct surface — **used only for d ≥ 9, replacing Browning/Xiao** |
| PairAlgebras … RootPairHilbert, NormHilbert, RationalCoordinates, WeightedFunctions, CurveThresholds, NormComponents, NormBoxes | analogue of the Lemma 5.1 bicone Hilbert polynomial (for the affine norm variety); §7 Prop 7.1 thresholds plus the new full-dimension threshold; Prop 9.2 curve alternatives; the d = 5..8 certificate |
| UnitBalancing, EmbeddingCharts | Lemma 4.1 balanced factorization (not Lemma 4.2) |
| MediumDegree | §11.2 for d = 5..8 |
| AffineHilbert, PoleCoefficients, ThreePoles, TwoPoles, QuarticSurfaces | analogue of §8 Prop 8.1 |
| QuarticComponents | analogue of §10 for d = 4 (100 bins) |
| QuarticBoxes, RadialFibres, Main | §11.2 for d = 4, a Lemma 6.3 substitute, and §11 completion |

**Paper material the Lean does not need:**
- Lemma 4.2 (paired boxes and analytic branches).
- All of §5: Prop 5.2 archimedean cuts, the Taylor determinant, the second cut on pure components.
- All of §6: Lemma 6.1, Prop 6.2 lattice boxes, Lemma 6.3.
- Prop 8.2 (the quintic critical-value discard) and the "+1_{d=4}" in g.
- Prop 10.1: the K₀ = 3000 grid, the 2124/1084/552/226/3 intervals, t_*, w, m, and the common-shift estimate (10.5).
- Appendix A and A.2.
- §11.1 for d ≤ 8.
- §12.
- Browning 2011 / Xiao 2017.

**Material the Lean needs that the paper never states:**
- the h = d+1 threshold;
- the radial-fibre argument via prime norms;
- the single-box d = 5..8 bound;
- the 100-bin quartic certificate;
- the d ≥ 9 surface argument (stated in §11.1, but only for d ≤ 8).

**Not formalized at all: Corollary 1.3** (separable products and simultaneous values). That corollary rests on the paper alone.

## 3. Hidden assumptions (grep over the full closure plus the challenge)

| Pattern | Hits |
|---|---|
| `sorry` | 1, at `PowerFreeValues.lean:42`, which is the challenge itself (expected) |
| `admit`, `axiom`, `opaque`, `implemented_by`, `extern`, `unsafe`, `partial def`, `native_decide`, `@[csimp]` | 0 |
| `set_option` | **0**: no maxHeartbeats, maxRecDepth, synthInstance or `debug.*` anywhere |
| `macro`/`elab`/`syntax`/`run_cmd`/`#eval`/`initialize`, `import Lean`/`Lean.` | 0 |
| `decide +kernel` | 5, all in `QuarticComponents`: ∀ j : Fin 100 over ℚ. These are pure kernel reductions with no extra axiom. |
| plain `decide` on ∀ j : Fin 100 over ℕ | 4 |
| other `decide` | trivial Fin facts |
| local instances | `attribute [local instance] Classical.propDecidable`, harmless |
| other instances | 5 ordinary instances (Fintype, DecidableEq, Module.Finite), all built via `inferInstanceAs` or real proofs |
| cited-result hypotheses ("published inputs") | **none**. `allDegrees` has exactly the 3 mathematical hypotheses; nothing is passed in as a Prop. |

**Build infrastructure, outside the proof closure.** `lakefile.lean` contains a top-level `run_cmd` that runs IO (`git clone`, `git apply`) and `unsafe env.evalConstCheck`, and it patches 24 dependencies for Lean 4.34.1. None of the patched packages is in this closure. Mathlib is pinned at d13f23b (manifest agrees) and is not patched. So this matters only for reproducibility, not for soundness.

**Comparator configuration.** Permitted axioms are {propext, Quot.sound, Classical.choice}. `enable_nanoda: false`, so there is only one kernel check.

## 4. Comparator

- I diffed `Model.lean` against the challenge. The definitions `PowerFree` … `DensityStatement` are identical apart from blank lines.
- The `allDegrees` signature is identical character for character: `diff` exits 0.
- The namespaces and `open`s are the same, and both files import the same Mathlib.
- FC's link `Main.lean#L144` is exactly `allDegrees`.

## Objections

- **L-1 (EXPOSITION; important for the panel).** The kernel-checked object certifies Theorem 1.1, Corollary 1.2 and #978 parts 2–3 by a different, shorter route. That route skips Lemma 4.2, §§5–6, Proposition 8.2, Proposition 10.1/Appendix A and Browning/Xiao.
  - If the replay passes, **referee findings in those sections cannot sink the theorem.**
  - Equally, **the Lean cannot rescue them**: it says nothing about those parts of the paper.
  - It also suggests that the paper's archimedean machinery is unnecessary for its main theorem: the paper's own Theorem-3.1-type count at r = d+1, plus Lemma 4.1 and §§7–9-type thresholds, appears to suffice. The paper should say so, or say why it does not.
- **L-2 (EXPOSITION).** Corollary 1.3 and §12 have no formal backing.
- **L-3 (EXPOSITION).** The FC bridge to `parts.ii`/`parts.iii`/`variants.sub_two` is routine but unformalized (steps in §1).
- **L-4 (EXPOSITION).** The paper's own §11.1 already covers d ≥ 9: φ_d(η) ≤ φ_d(1) = 2/d ≤ 2/9 < 0.2495 on all of [1, d/k]. Citing Browning in Xiao's form for Corollary 1.2 is unnecessary, and the Lean shows the case independently.

No FATAL issue and no GAP in the statement or the source hygiene.

VERDICT: HOLDS AS READ
