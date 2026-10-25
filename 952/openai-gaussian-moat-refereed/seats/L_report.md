# Seat L (Lean) report: Erdős #952 / OpenAI "Bounded-Step Walks on Gaussian Primes"

**Scope.** I read the comparator statement, `Model.lean`, `Main.lean`, and the declarations that carry the argument across all 41 files under `OAI/NumberTheory/GaussianMoat/`. Everything was compared against the printed paper (`src/paper.txt`), the live problem page, and FC's `erdos_952`.

I did not compile anything; the kernel replay belongs to the coordinator. After I finished my own reading I looked read-only at the coordinator's logs, and I mark every place where I cite them:
- `driver.log`: `BUILD END 0 41 failed []`
- `statement_match.txt`: `ALL_MATCH_STD_SORRYSEEN, 6 MATCH / 0 MISMATCH`
- `ax_GaussianMoat.log`: axioms `[propext, Classical.choice, Quot.sound]`
- `leanchecker --fresh` was still running when I read the logs.

The Mathlib checkout `/tmp/erdos0300/lean/mathlib4` is at `d13f23b` (same as `lake-manifest.json`). It has no tracked modifications; the only untracked file is `LAKE_DELETED.txt`.

Provenance. FC's `erdos_952` cites `openai/math@adc7f12 …/Main.lean#L102`. In the repo, `adc7f12` is the "Initial commit" and the only commit that touches `lean/OAI/NumberTheory/GaussianMoat` or `ComparatorChallenges/GaussianMoat.lean`. HEAD is `1581d4c` and the worktree is clean. `Main.lean:102` is `theorem fullMain`. So FC links to exactly the code examined here.

---

## 1. Is the statement faithful?

### 1a. Comparator statement vs. solution model

`ComparatorChallenges/GaussianMoat.lean` and `OAI/NumberTheory/GaussianMoat/Model.lean` are identical apart from the `fullMain … := by sorry` line and one blank line (I checked with `diff`). Both files have `import Mathlib` and nothing else. Every other file in the chain imports the previous one (Model → LatticeComponents → … → SieveSmoothing → Main).

So no instance, notation or option defined later in the chain can change how the five definitions elaborate:
- `PrimeVertex`
- `primeGraph`
- `component`
- `MainEndpoint`
- `UniformEndpoint`

`fullMain : MainEndpoint ∧ UniformEndpoint` refers only to these definitions. The coordinator's pp.all match (6/6) is the mechanical confirmation of this.

### 1b. `MainEndpoint` against the problem page and FC

`Model.lean:25`:
```
∀ (D : ℝ) (z : ℕ → GaussianInt), (∀ t, Irreducible (z t)) → Function.Injective z →
  (∀ t, dist (z (t + 1) : ℂ) (z t : ℂ) ≤ D) → False
```
The page asks: "Is there an infinite sequence of distinct Gaussian primes x_1, x_2, … such that |x_{n+1} − x_n| ≪ 1?" `MainEndpoint` is exactly the negative answer:
- "distinct" is `Injective`;
- "≪ 1" is "some real D bounds every step", and D is universally quantified in front, so no sequence has bounded steps.

**D negative or D < 1.** For D < 0 the step hypothesis cannot hold, so the case is vacuous and harmless. For 0 ≤ D < 1 there is also no walk. The proof does not special-case either: `main_of_finiteSieve` (`LatticeComponents.lean:110`) applies the sieve at `max D 1`, which is legitimate monotonicity.

**Irreducible vs Prime.** In ℤ[i], Irreducible and Prime coincide, so "Gaussian prime" = `Irreducible` (paper §1: "A Gaussian prime is an irreducible element of Z[i]"). For FC's direction only the easy half is needed:
- `Prime.irreducible` (`Mathlib/Algebra/Prime/Defs.lean:152`) needs `[CommMonoidWithZero M] [IsCancelMulZero M]`, available through the EuclideanDomain → IsDomain instance.
- So `MainEndpoint`, whose hypothesis is weaker, implies the `Prime` version.
- The converse, `irreducible_iff_prime` (DecompositionMonoid/PID), is available and Mathlib already uses it for ℤ[i] in `QuadraticReciprocity.lean:75`, but it is not needed.

`Irreducible` includes:
- all associates;
- 1+i;
- the axis primes 3, 3i, 7, … .

It excludes 0 and the units. This matches the paper's "includes primes on the coordinate axes".

**Coercion and distance.**
- `(p.val : ℂ)` elaborates through Mathlib's `instance : Coe ℤ[i] ℂ := ⟨toComplex⟩` (GaussianInt.lean:73), with `toComplex_def : (x : ℂ) = x.re + x.im * I`.
- The coordinator's pp.all log shows `@DFunLike.coe … (@RingHom GaussianInt Complex …) GaussianInt.toComplex`.
- `dist` is `@Dist.dist Complex (PseudoMetricSpace.toDist (SeminormedRing.toPseudoMetricSpace … instCommCStarAlgebraComplex))`, Mathlib's standard metric on ℂ.

The green build itself also certifies that this exact `dist` is Euclidean. Two lemmas, elaborated in an environment with no extra instances (LatticeComponents imports only Model), prove the identity `dist(z,w)² = Zsqrtd.norm (z − w) = (re Δ)² + (im Δ)²` for the instance in the statement:
- `norm_square_complex : (z.norm : ℝ) = ‖(z : ℂ)‖ ^ 2` (`LatticeComponents.lean:123`);
- `not_dvd_sub_of_dist_sq_lt` (`:159`), which rewrites `dist` to that norm via `dist_eq_norm` and `toComplex_sub`.

**FC's `.norm`.** In FC, `(x (n+1) − x n).norm` has no `GaussianInt.norm` definition to resolve to (only `GaussianInt.norm_*` theorems exist). It therefore resolves through the abbrev to `Zsqrtd.norm : ℤ`, which is re² + im² for d = −1. It is ℤ-valued, as `< C` with `C : ℤ` requires.

### 1c. `UniformEndpoint` against Theorem 1.1

`Model.lean:30`:
```
∀ D : ℝ, ∃ B : ℕ, (∀ p : PrimeVertex, (component D p).Finite ∧ (component D p).ncard ≤ B) ∧
  (∀ n (z : Fin n → GaussianInt), (∀ i, Irreducible (z i)) → Injective z →
     (∀ i j : Fin n, j.val = i.val + 1 → dist (z j) (z i) ≤ D) → n ≤ B)
```
- **Graph.** `primeGraph D` has vertex type {z // Irreducible z} and `Adj p q := p ≠ q ∧ dist ≤ D`. This is the paper's G_D: all Gaussian primes, edges between distinct z, w with |z − w| ≤ D. `component D p` is the set of vertices reachable from p (reflexive–transitive closure of Adj), i.e. the vertex set of p's connected component.
- **`ncard` loophole.** `Set.ncard` of an infinite set is 0, so `ncard ≤ B` alone would be satisfiable vacuously by infinite components. The conjunction with `.Finite` closes this: finiteness is asserted separately, and on finite sets `ncard` is the true cardinality. **No loophole.**
- **Uniformity.** B is chosen after D and before p, so it is uniform over all components, including axis primes. This matches "independent of the starting prime".
- **Walk clause.** It quantifies over consecutive indices only (`j.val = i.val + 1`), with injectivity. It is the paper's "Consequently every sequence of distinct Gaussian primes whose successive distances are at most D has at most B_D terms". It is a corollary of the component bound and is proved that way (`finite_prime_walk_bound`, `LatticeComponents.lean:525`). The case n = 0 is trivial.
- **D < 1 and negative D.** The same B works; the proof again goes through `max D 1`.
- **Jordan–Rabung variant.** The forum version ("|γ_1| < M, |γ_j − γ_{j−1}| < M, lim|γ_j| = ∞", repeats allowed) also follows from `UniformEndpoint`. Such a sequence stays inside one finite component, so it is bounded.

### 1d. Bridge from `fullMain` to FC's `erdos_952`

```
¬ ∃ (x : ℕ → GaussianInt) (C : ℤ), Function.Injective x ∧ ∀ n, Prime (x n) ∧ (x (n+1) − x n).norm < C
```
Only `fullMain.1` is needed. Take D := (C : ℝ). The Lean facts required are:
1. `Prime.irreducible`, to turn `Prime (x n)` into `Irreducible (x n)`.
2. `dist (a:ℂ) (b:ℂ) ^ 2 = ((a − b).norm : ℝ)`. This comes from:
   - `dist_eq_norm`,
   - `GaussianInt.toComplex_sub`,
   - `GaussianInt.intCast_real_norm : (x.norm : ℝ) = Complex.normSq (x : ℂ)`,
   - `Complex.normSq_eq_norm_sq` (or `Complex.sq_norm`).

   Equivalently, use OAI's own `norm_square_complex` after `toComplex_sub`.
3. `GaussianInt.norm_nonneg` (GaussianInt.lean:138), giving `1 ≤ C` from `0 ≤ norm < C`. Then `norm ≤ C − 1 < C ≤ C²`, so `dist ≤ C`, using `dist_nonneg` and `abs_le_of_sq_le_sq`/`nlinarith`.

Uncompiled sketch (my own; the coordinator's `BRIDGE_DONE`/`bridge_compile rc=0` is their separate artefact):
```lean
example : ¬ ∃ (x : ℕ → GaussianInt) (C : ℤ),
    Function.Injective x ∧ ∀ n, Prime (x n) ∧ (x (n + 1) - x n).norm < C := by
  rintro ⟨x, C, hinj, h⟩
  refine OAI.GaussianMoat.fullMain.1 (C : ℝ) x (fun n => (h n).1.irreducible) hinj (fun t => ?_)
  have hN : ((x (t+1) - x t).norm : ℝ) < C := by exact_mod_cast (h t).2
  have h0 : (0:ℝ) ≤ (x (t+1) - x t).norm := by exact_mod_cast GaussianInt.norm_nonneg _
  have hC1 : (1:ℝ) ≤ C := by
    have : (0:ℤ) < C := lt_of_le_of_lt (GaussianInt.norm_nonneg _) (h t).2
    exact_mod_cast this
  have hsq : dist (x (t+1) : ℂ) (x t : ℂ) ^ 2 = ((x (t+1) - x t).norm : ℝ) := by
    rw [dist_eq_norm, ← GaussianInt.toComplex_sub, GaussianInt.intCast_real_norm,
        Complex.normSq_eq_norm_sq]
  nlinarith [dist_nonneg (x := (x (t+1) : ℂ)) (y := (x t : ℂ))]
```
FC's direction and indexing (x(n+1) − x n), injectivity and quantifiers all match `MainEndpoint`; nothing else is needed.

**Verdict on (1): faithful.** `MainEndpoint` is the problem page's question with a negative answer and is at least as strong as FC's `erdos_952`. `UniformEndpoint` is the paper's Theorem 1.1 plus its stated corollary. I found no weakening.

A minor EXPOSITION note: `GaussianMoat.json` has `"definition_names": []`. Protection of the five definitions therefore rests on the comparator's dependency check and on the coordinator's pp.all match of the five definitions, which `probes.json` does include.

---

## 2. Escape hatches: grep over all 41 files

| Pattern | Hits | Matters? |
|---|---|---|
| `sorry`, `admit` | 0 | – |
| `axiom`, `opaque`, `unsafe`, `partial`, `implemented_by`, `extern` | 0 | – |
| `native_decide`, `decide := true`, `Lean.ofReduceBool`, `trustCompiler` | 0 | – |
| `set_option` (any; incl. `maxHeartbeats 0`, `maxRecDepth`, `synthInstance`, `debug.skipKernelTC`) | **0** | – |
| `macro`, `macro_rules`, `elab`, `syntax`, `notation`/`infix*`/`prefix`/`postfix` (incl. `local notation`), `run_cmd`, `initialize`, `#exit`/`#eval` | 0 | – |
| `@[csimp]` | 0 | – |
| `import` other than the chain | only `Model.lean: import Mathlib` | – |
| `decide` (kernel `Decidable`, not native) | `WalkGeometry.lean:19,30,79,92,93` (`Fin 3` colour facts); `LatticeComponents.lean:76` (`(-1:ℤ) ≤ 0` for `Zsqrtd.norm_eq_of_associated`); `BackwardCoverage.lean:19,21,360`, `SignConcentration.lean:66` (the `decide` function inside terms) | no; kernel-checked |
| `attribute [local instance] Classical.propDecidable` | `FiniteLaw.lean:12` (file-local) | no |
| `open scoped … Classical` | many | no; it only adds a low-priority decidability instance inside proofs. Model.lean does not open it. |
| `@[reducible] def Cube` | `BooleanCube.lean:11` | no; a local type |

Instance declarations, all on local types or Prop-valued, none touching ℂ, `dist`, `MetricSpace`, `GaussianInt` arithmetic or `Irreducible`:

| Location | Instance | Kind |
|---|---|---|
| `BooleanCube.lean:14,17` | `Fintype`/`DecidableEq (Cube n)` | local type |
| `FiniteLaw.lean:131` | `CoeFun (FinLaw α)` | local structure |
| `ResidueQuotient.lean:34,36` | `Countable GaussianInt`, `Countable (ℤ[i] ⧸ multiples π)` | Prop, subsingleton |
| `WalkGeometry.lean:385,386` | `Module.Free ℤ GaussianInt`, `Module.Finite ℤ GaussianInt` | Prop |
| `SignConcentration.lean:12,17` | `IsProbabilityMeasure` | Prop |
| `SignedGeometry.lean:268`, `LatticeComponents.lean:224` | `Finite …` | Prop |
| `SignedResidues.lean:34` | `Fintype (s.Residue i)` on a quotient | used only in proofs |

None of them is visible to `Model.lean`. They could at worst cause elaboration failures, never unsoundness.

**Lakefile.** It contains `run_cmd`/`post_update` code that patches some git dependencies (iut, PNT+, carleson, …). It never patches Mathlib, and GaussianMoat imports only Mathlib. `leanOptions` is just `autoImplicit := false`.

**Verdict on (2): nothing found that matters.**

---

## 3. Mapping the Lean architecture to the paper

The Lean is a *certificate architecture*:
- `exists_sieveCertificate` (`Main.lean:9`) builds, for every D ≥ 1, a walk-independent `SieveCertificate D` (`SieveCertificate.lean:8`). Its fields are a schedule, the dyadic batches, a `BatchCertificate` for each batch, word lengths with divisibility, a smoothing error, and the final excess inequality.
- `SieveCertificate.sound` → `certificate_no_walk` (`BatchCertificate.lean:111`) refutes every avoiding walk.
- `finiteSieve_of_certificates` (`SieveCertificate.lean:52`) gives `FiniteSieveEndpoint`.
- `endpoints_of_finiteSieve` (`LatticeComponents.lean:550`) gives `fullMain`.

The table maps each paper item to its Lean counterpart. Stated relations are "same", "stronger", "weaker", or "different route".

| Paper | Lean | Relation |
|---|---|---|
| **Thm 1.2** | `FiniteSieveEndpoint` (`LatticeComponents.lean:41`): `∀ D, 1 ≤ D → ∃ s : SplitSieve, ∀ z, (∀ t, z t ∈ s.avoiding) → Injective z → (∀ t, dist … ≤ D) → False`. Here `SplitSieve` is a finite set of primes p ≡ 1 (mod 4), each with an irreducible factor of norm p, and `avoiding = {z | ∀ p, ¬ factor p ∣ z ∧ ¬ star (factor p) ∣ z}`. | **Same**: ∀D ≥ 1, ∃ a finite set, ∀ walks; A(P) excludes both conjugates. The choice of factor is immaterial, exactly as the paper says. |
| **Prop 2.1** | `prime_components_of_finiteSieve` (`:495`), with bound `B = period² + ncard (s.restored D)`, where `restored = exceptions ∪ ⋃ (avoiding-graph components of points within D of an exception)` (`:416`). Ingredients: König via `exists_seq_forall_proj_of_forall_finite` (`infinite_component_has_walk`, `:243`); translation invariance (`eq_of_finite_component_period`, `periodic_component_bound`, `:391`, giving ≤ Q² per avoiding component); exceptions finite (`exceptions_finite`). | **Same route, different explicit bound.** The Lean does not verify the paper's formula max{Q², \|E\| + (K_D − 1)\|E\|Q²}; I checked that formula by hand and it is correct. The paper's "D < 1 ⇒ B_D = 1" remark is not used; `max D 1` replaces it. The tail-deletion remark for the infinite-walk conclusion is `main_of_finiteSieve` (`:110`), the same. |
| **(3.1)** PNT in APs (Selberg) | **Not used.** `PrimeLogMass.eventually_prime_window_mass` (`PrimeMass.lean:360`) uses Mathlib's Dirichlet machinery (`LFunctionResidueClassAux`) plus a degree-~4000 positive polynomial window (`windowPolynomial`, `:112`). This gives c·X ≤ Σ_{p prime, p ≡ 1 (4), e^{1.001X} ≤ p ≤ e^{1.0499X}} 1/p. From it, `eventually_dense_split_bins` (`DenseBins.lean:203`): a positive proportion (c·X) of dyadic bins j with X ≤ j log 2 ≤ 1.05X have ≥ δ 2^j / log 2^{j+1} split primes. The upper bound is Chebyshev θ(x) ≤ x log 4 (`prime_log_mass_le_theta`). | **Different route, weaker input.** The paper needs every batch to satisfy k_T ~ T/(2 log T). The Lean uses only a positive-density subset of dyadic batches. |
| B > 2 geometric spacing, (6.5) | `thin_bins` (`BatchCertificate.lean:151`) keeps one residue class mod K of the dense bins, so the bins are K-separated (B ↔ 2^K). `precedingFactors_enum_cost` gives residueWeight(earlier batches) ≤ (4 log 4/(2^K − 1))·2^j ≤ c·2^j/10⁴. | Same idea. |
| Lemma 3.1 | `displacement_entropy_le` (`PointEnrichment.lean:25`), `ForwardKernel.displacement_entropy` (`Information.lean:92`): H(displacement) ≤ log 36 + 2 log(D·n). | Same, explicit. |
| Lemma 3.2 | `smoothing_condH` (`BackwardCoverage.lean:350`), `word_residue_smoothing` (`WalkWords.lean:195`): error 2h(a/(N+1)) + (a/(N+1))(log\|α\| + 2 log\|β\|), stated directly for the uniform offset. | Same; a slightly sharper constant on the word alphabet. |
| Lemma 3.3 | `FinLaw.short_list` (`FiniteLaw.lean:493`), `short_list_probability_deficit`. | Same. |
| Concavity of f_Z | `orderedEntropy_concave` (`FiniteEntropy.lean:269`), `signedEntropy_slope`. | Same. |
| **Lemma 4.1** | `walk_many_differences` (`DifferenceSampling.lean:142`): ∃ R ≥ W ≥ 1 with n ≤ 18RW, RW ≤ D²n², RW ≤ max(D, \|latticeBall(4D)\|)·\|E − E\|. Proof: `discrete_rectangle_sperner` (`WalkGeometry.lean:32`) → `path_difference_cover_general` (`:341`): every w is within 4D of v_i − u_j + s·a + t·b. | **Different route.** A discrete Sperner/tricolouring argument replaces the torus-degree argument (Hatcher); 4πD² becomes \|ball(4D)\|. Same statement shape. |
| **Lemma 4.2** | `SplitSieve.signed_rectangle` (`SignedGeometry.lean:601`): primes in [T, 2T], T ≥ 5, R ≥ W ≥ 1, 0 < d < 1/4, RW ≤ P^{1−d}, 1000 ≤ d³r ⇒ Pr_σ[nonzero multiple of the signed product in the rectangle] ≤ exp(−d³r/5120). Uses `cube_edge_isoperimetric` (`BooleanCube.lean:138`), Hoeffding (`sign_hoeffding`), line classes, `near_witnesses_collinear`. | **Same, with explicit constants** (C = 1, c = 1/5120, C₀ = 1000). |
| **Lemma 4.3** | `TimeLaw.step_enrichment` (`TimeLaw.lean:51`) and `TimeLaw.step_deficit` (`Information.lean:140`): if the fresh coordinate entropy is ≥ (1 − 30g)L*, the start has f(q) ≥ (1 − e)qL*, b ≤ gq, and displacement cost ≤ 8gqL*, then f_V(b) ≥ (1 − e/2 − 20g)bL*. Margins come from `EnrichmentMargins.from_scale`/`walk_fresh_lower`. | **Same, non-asymptotic.** O_D(g) becomes an explicit 20g, with the D-dependence moved into "scale ≫ log D, log\|ball(4D)\|" hypotheses. |
| (6.3)/(6.4) iteration and preservation | `deficit_iteration` (2^{−l} + 40g), `TimeLaw.geometric_band_entropy` (`MultiscaleSchedule.lean:367`): deficit (1/2)^l + 80g. `EntropyBand` (`EntropyBand.lean:205`) plus `EntropyBand.sound` (preservation to the later checkpoint via the `cost` field). | Same. |
| **Lemma 5.1** | `SplitSieve.signed_coverage_deficit` (`SignedResidues.lean:65`): average[log p − H(residue \| C)] ≤ eL* + E/b. | Same. |
| **Thm 5.2** | `FinLaw.lowResidues_backward` (`SignedResidues.lean:163`) → `backward_coverage_step` (`BackwardCoverage.lean:162`); walk instance `ForwardKernel.coverage_backward` (`EntropyBand.lean:153`). Hypotheses: τ ≤ 3/8, δ ≤ 1/64, next level at τ + 4δ; η′ + ε ≤ ηδ/2; data deficit e < ηδv/4; list bound b_i ≥ u′_i/δ; gain v ≤ log p − log b_i; p·exp(−nδ²u_i/(2p)) ≤ ε. Trials are i.i.d. conditional on the exact mixing value (`p.joint (q ω).iid n`). | **Same mechanism, generalized**: arbitrary exceptional thresholds u, u′, arbitrary list bound and gain v in place of p^{1−β}, p^{1−β′}, (β′/4) log T. |
| Lemma 6.1 | `windowSmoothing W m = ⌈exp(20·100^W·e^m)⌉` (`Smoothing.lean:86`); TV a/(N+1) through `smoothing_condH`; costs via `eventually_suffix_cost`, `commonSchedule_log_bound`. | Same role; the paper's specific "log(1 + S_V) ≤ 2gV" is not stated. |
| **Prop 6.2** | `CoverageDerivation` (`EntropyBand.lean:240`, inductive base/step) with `CoverageDerivation.sound` (`:262`), instantiated by `one_step_coverage` (`BatchParameters.lean:8`) and `coverage_from_scalar_guards` (`Smoothing.lean:227`). The **base** is the final "accurate" block (scale exp(e^m/20), grid g = e^{−m²}, 4m² iterations). It needs an *absolute* deficit ≤ e^{−100}/(512·640000) and gives fraction ≤ 1/640000 of coordinates with ≥ u′ = e^{−100}p/64 residues below τ′ = 5/16 (a *constant fraction of p*). **One** transfer step through the middle accurate block (scale ≈ T^{1/4}·e^{−8m⁴}) uses n = ⌈e^{X/100}⌉ repetitions and gain v = 100, needing absolute deficit + data cost < 1/256. Output: τ₀ = 1/4, η₀ = 1/100, exceptional sets < p·e^{−X/200} (X ≤ log p, so ≥ p^{199/200}). | **Different route.** No β_i/r_i/τ_i/η_i ladder (6.6)–(6.17) and no J = O(M) checkpoints. Prop 6.2 as printed is **not** formalized. The Lean proves only the terminal coverage that Prop 7.1 consumes. |
| **Prop 7.1** | `schedule_batch_information` (`InformationTelescope.lean:240`) ← `exists_batch_information` (`:10`) ← `averaged_batch_package_information` (`WalkPackage.lean:305`) ← `posterior_passing_information_lower` / `passing_information_lower` (`PassingInformation.lean:185/72`). Hypotheses: avoiding (`ha`), injective, (DL)² < p (single hit per package), smoothing L/(N+1) ≤ τ/(2p), list bound log(4e_i + p·e^{−n(Lτ/2p)/4}) ≤ log p − A, rate inequality n(Lr + 2(log 36 + 2 log D(…))) ≤ b(A(1 − 2η) − δL*) − E. Conclusion: ∃ signs σ, ordering π with r ≤ I(X′; W_L(t*) \| O′)/L. Favourable/unfavourable split at posterior 1/2, the 2η count, and conditional independence of packages given (O, X) via `conditionOn`/`mix` mirror (7.4)–(7.9). | **Same route.** Two packaging differences: (i) the bound is proved for an arbitrary set F of earlier factors with total log-norm ≤ E (not only the random selection), and (ii) the conclusion is existential (∃σ, π ≥ average), not E_C. Batch rate r = (topCoefficient a/4)/(10⁷ log 2^j), i.e. c₁/log T. |
| **Lemma 8.1** | `schedule_information_telescope` (`InformationTelescope.lean:218`) / `common_law_information_telescope` (`:151`): Σ_{j ≤ n} I(Q_{j+1}; W_{L_j} \| Q_j)/L_j ≤ log\|latticeBall D\| + n·ε, where ε bounds the explicit continuity error and L_j \| L_{j+1} (`batchWordLength j = 2^{⌊2j/5⌋}`, `batchWordLength_dvd`). | **Same**, non-asymptotic: o(1) becomes n·ε with ε = e^{−e^m}. |
| **Proof of Thm 1.2** | `certificate_no_walk` (`BatchCertificate.lean:111`) chooses nested factor sets F_j batch by batch with `greedy_finite_selection` (`:71`), sums the per-batch rates, and contradicts `excess : log\|ball D\| + last·error < Σ rates`. `exists_sieveCertificate` (`Main.lean:9`) supplies the certificate. | Same skeleton, different schedule (next row). |
| §6.1 schedule and windows | Windows at log-scale X_w = 100^w·e^m, w < W, each with its top band (g = topParameter = 10^{−6}, 20 iterations, scale a·2^j) and an accurate block (g = e^{−m²}). The window count W is **fixed**: W > (log\|ball D\| + 1)/rate, with rate = c·t/10500000. m → ∞ (eventually filters). | **Different route.** The paper uses X_m = 100^m for m ∈ [M/2, M] (growing count) and M → ∞. The Lean takes the number of windows depending only on D and lets the base scale grow. |

**The constants in `Main.lean`:**
- c = topCoefficient a/4 = (10^{−12})^{20}·a/4.
- The per-batch rate is c/(10⁷ log 2^j).
- Each window has ≥ t·X_w bins, each with log 2^j ≤ (21/20)·X_w. So a window contributes ≥ t·X_w·c/(10⁷·1.05·X_w) = c·t/10500000. Hence 10500000 = 1.05·10⁷, coming from the window width 21/20.
- E ≤ c·2^j/10000 is the budget for earlier-batch residues.
- `hcost'`: (#batches)·e^{−e^m} ≤ 1.

I re-did this arithmetic and it is consistent; the tight numeric lemmas `exp(−1.0499) < 0.35`, `exp(−1.001) > 11/30` and `2^{−20} + 9·10^{−5} ≤ 10^{−4}` also check numerically (`L_scratch/consts.py`).

### Quantifier order in the Lean (the order the brief flags)

1. Absolute constants first: topParameter = 10^{−6}, topIterations = 20, and (a, δ, t, K) from `exists_separated_parameters` (`SeparatedParameters.lean:183`). These have **no D-dependence**.
2. Then D.
3. Then c, rate, W (W depends on D through log\|ball D\|).
4. Then m. It is chosen from `∀ᶠ m` statements (`eventually_window_batch` for each w < W, `eventually_allBins_smoothing`) that are **uniform over all J, j ∈ J w, and E** (they are ∀-quantified inside the filter).
5. Then J (by `choose`), then the sieve `q.sieve`.
6. Only then is any walk introduced (`SieveCertificate.sound`), and the per-walk choices (σ, π, F_j) never feed back into the sieve. The sieve removes both conjugates, so the sign selection is irrelevant to it.

No constant is chosen after something it must precede. The paper's order "D, e₀, then l₀, g₀, c₀, then B, finally M" is respected, and in fact strengthened: the batch-level constants (paper's l₀, g₀, B) are D-independent in the Lean.

### What the Lean proves that the paper does not state

- D-independence of all batch-level constants: g = 10^{−6}, 20 iterations, the K-separation, a, δ, t. D enters only through W and the threshold for m.
- Explicit constants in Lemmas 4.2 and 4.3 and in the telescope.
- Theorem 5.2 for arbitrary threshold functions.
- A positive-density prime-batch lemma from Dirichlet L-function inputs alone. This shows the paper's appeal to the PNT in APs (3.1) is unnecessary.
- A single-step coverage derivation.

### Paper claims the Lean does not cover

None of these is needed for `fullMain`:
- (3.1) itself and Selberg's theorem;
- the torus-degree proof of Lemma 4.1 (an alternative proof is formalized);
- Lemma 6.1's 2gV bound;
- the β-ladder Prop 6.2 with (6.6)–(6.17);
- (6.10)–(6.11) as stated;
- the explicit B_D formula of Prop 2.1;
- the paper's base-B, M-window schedule.

The docs' "No explicit function of D is supplied" is accurate: B comes from `choose` and eventually filters, as the paper also says ("nonexplicit").

---

## 4. Objections (classified)

1. **EXPOSITION (important for other seats).** The formal proof does **not** follow the paper's §6.3–6.4 checkpoint ladder (β_i = 2^{−i}β₀, r_i, τ_i, η_i, J = O(M), Prop 6.2 as printed). It does not use the PNT in APs ((3.1), Selberg) or the homological-degree proof of Lemma 4.1 either. It replaces them with:
   - a constant-fraction base plus one transfer step, using extremely fine "accurate" bands with g = e^{−m²} so that absolute entropy deficits drop below 1/1024;
   - Dirichlet-L positive density of dyadic bins;
   - a discrete Sperner lemma.

   Consequence: if the replay is green, any GAP another seat finds *only* in §6.3–6.4, in Lemma 4.1's degree argument, in the use of (3.1), or in Prop 2.1's explicit bound is a defect of the paper's exposition, **not** of Theorem 1.1. A reader of the paper alone is not told that the verified route differs, and `docs/028.md` does not say so either.
2. **EXPOSITION.** `ComparatorChallenges/GaussianMoat.json` lists `"definition_names": []`. The five definitions under the theorem are protected only by the comparator's dependency check and the independent pp.all match, which the coordinator has run (6/6 MATCH, per their log).
3. **No ERROR or FATAL item on the Lean side.**
   - The statements are faithful to the page, to Theorem 1.1, and (via the short bridge in §1d) to FC's `erdos_952`.
   - There are no escape hatches: no sorry, axiom, native code, kernel-skipping option, or instance or notation that could affect the statement.
   - The `ncard`/`Finite` and negative-D cases are not loopholes.

VERDICT: HOLDS AS READ
