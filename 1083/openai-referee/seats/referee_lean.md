# Referee report — `lean`: hostile source-level audit of cadamcat/distinct-distances-lean4

Scope: PROMPTS.md § "lean". Clone `/tmp/oaimath/166/lean/repo` at HEAD `88919b8` (2026-10-11T02:42Z). No lake or lean was run. The kernel replay at `/tmp/oaimath/166/lean-build` had **not started** when this was written (2026-10-11T21:30Z): `steps.tsv` holds only `launch`, and `build.log` says "waiting: #181 replay still building". **Nothing here is a kernel result.** Every "VERIFIED" below means *verified by reading the source*.

Material fetched for this audit (all read-only):
- The full transitive OAI import closure at `openai/math@adc7f124`: **503 modules, 130,917 lines**, in `/tmp/oaimath/166/oai_lean/OAI/...`, with the dependency graph in `oai_lean/_closure.json`. That is 33 import levels, well past the two levels the brief asked for.
- OAI's `lakefile.lean`, `formalization.yaml` and `OAI.lean` (in `/tmp/oaimath/166/oai_meta/`).
- The `PrimeNumberTheoremAnd-lean4341.patch` and `StrongPNT-lean4341.patch` patches, plus the PNT files extracted from them (`/tmp/oaimath/166/oai_patches/`).
- Formal Conjectures at `660712921c`: `Metric.lean`, `1083.lean` and `Euclidean.lean` (`/tmp/oaimath/166/lean_audit/fc/`).
- Mathlib `d13f23b`: `PiL2.lean`.
- The JSP catalog entry at awards@`16877004`.
- The GitHub API commit list and the v1.0.0→HEAD compare.

Helper scripts are in `/tmp/oaimath/166/lean_audit_scripts/`.

---

## 0. Verdict for this scope

- **Statement fidelity: HOLDS AS READ.**
  - `DistinctDistances.jsp_000900` in `Challenge.lean` is Theorem 1.1 (constant factor, every d ≥ 3, every set of at least 2 points) plus the grid upper bound.
  - The metric is Mathlib's L² (`EuclideanSpace = PiLp 2`), the exponent is real `rpow` 2/d, and c and C are chosen before P and n.
  - The statement is not vacuous.
  - It strictly implies Formal Conjectures' `erdos_1083` right-hand side. The implication is short but **not formalized in the repo**.
- **Kernel bypasses at source level: NONE FOUND.** I scanned three bodies of code:
  - the project (757 `.lean` files);
  - the full OAI closure (503 modules);
  - the one patch-injected third-party file in the import cone (`PrimeNumberTheoremAnd/Erdos970/HadamardSupport.lean`, 6,805 lines).

  Across all three: zero `sorry`/`admit`/`axiom`/`native_decide`/`ofReduceBool`/`implemented_by`/`extern`/`unsafe`/`opaque`/`debug.*`/`addDecl`; zero `elab`/`macro`/`syntax`/`run_cmd`/`initialize` in the cone; no metric instance or notation overrides.
- **Kernel acceptance: COULD NOT CHECK.** The replay is queued and has not started.
- **"Follows the paper": PARTLY CONTRADICTED.** The Lean does **not** formalize the paper's planar input. Theorem B.12 (planar Ω(n/log n)), Corollary B.13 and the ruled-surface / two-rich-point machinery B.7–B.11 have **no Lean counterpart**. They are replaced by `TrackC.ci_weak_planar_distances`, which gives |Δ(X)| ≥ c·|X|^{3/4} in ℝ². That leads to plane occupancy ≤ C·M^{4/3} (`ci_planar_occupancy`) and a uniform flat cap with c₀ = 1/3 instead of the paper's 1/2.

  **Consequence for the paper (conditional on a green replay):** Theorem 1.1, including the d = 3 base, does not need Guth–Katz-strength planar distinct distances. Lemma 2.1's "Planes have the more precise bound B^{2+o(1)}" (p. 7) and Appendix B §B.4–B.7 (pp. 95–101) are off the critical path. A planar exponent of 3/4 suffices, and by my reading of the Lean's consumers any exponent > 2/3 would. Appendix B's Theorems B.2 (Szemerédi–Trotter), B.5 (higher-richness Guth–Katz) and Corollary B.6 (planar motions) **are** formalized and **are** consumed, by Theorem 7.1 and Proposition 2.2.
- **Provenance:**
  - The public repo is **one squashed 211,476-line commit** (`0e56d4c`, 2026-10-10T18:52Z) plus 5 comment/doc/audit commits. The full public span is 7 h 50 min.
  - The development history is private; the author says so in JSP PR #4994.
  - The code was written by AI coding agents. `formalization.yaml` says `review: agent-reviewed, reviewers: []` and "No independent human expert has reviewed the formalization."
  - The "independent check" and the Comparator + nanoda run are self-reported. The Comparator run was **not sandboxed** ("development stand-in for `landrun`").

---

## 1. Claim → source → verdict table

| # | Claim (where) | What the source shows | Verdict |
|---|---|---|---|
| 1 | "`jsp_000900` … every finite set P of at least two points … at least c\|P\|^{2/d} … some n-point set … at most C n^{2/d}" (README, Challenge.lean:42–52) | `Challenge.lean` lines 42–52 quantify `∀ d, 3 ≤ d → ∃ c C, 0<c ∧ 0<C ∧ (∀ P : Finset (EuclideanSpace ℝ (Fin d)), 2 ≤ P.card → c * (P.card:ℝ)^((2:ℝ)/(d:ℝ)) ≤ distinctDistances P) ∧ (∀ n, 2 ≤ n → ∃ P, P.card = n ∧ distinctDistances P ≤ C * n^((2:ℝ)/(d:ℝ)))`. This is the same text as `DistinctDistances/Main.lean` lines 14–20. | VERIFIED-AT-SOURCE (statement). Elaborated-type identity: NOT VERIFIABLE WITHOUT A BUILD (`check_target.py statement` / Comparator). |
| 2 | "definitions copied verbatim from Formal Conjectures … at commit 660712921c…; only the module-system wrappers are dropped" (Challenge.lean, Defs.lean, THIRD_PARTY) | Every docstring+def chunk of the BEGIN/END block occurs verbatim in FC `Metric.lean`@660712 (my script: `True` for all 4 chunks; preamble `open scoped Finset` and `variable {X : Type*} [MetricSpace X]` present). The Challenge and Defs blocks are identical. | VERIFIED-AT-SOURCE |
| 3 | "FC's `erdos_1083` asks for the weaker n^(2/d − o(1)) form" (THIRD_PARTY, yaml) | FC 1083.lean@660712: `∃ o : ℕ → ℝ, o =o[atTop] (1 : ℕ → ℝ) ∧ ∀ᶠ n, (minimalDistinctDistances (ℝ^d) n : ℝ) = (n:ℝ)^((2:ℝ)/(d:ℝ) − o n)`, with `ℝ^d` = `EuclideanSpace ℝ (Fin n)` (FC Euclidean.lean:22). | VERIFIED-AT-SOURCE. jsp ⟹ FC right-hand side (§2.3), not formalized; the converse is false. |
| 4 | "Points live in `EuclideanSpace ℝ (Fin d)`" — Euclidean distance | Mathlib d13f23b PiL2.lean:114–115 `abbrev EuclideanSpace (𝕜 …) (n …) := PiLp 2 fun _ : n => 𝕜`; :161–163 `theorem EuclideanSpace.dist_eq … dist x y = √(∑ i, dist (x i) (y i) ^ 2) := PiLp.dist_eq_of_L2 x y`. `Upper.lean:39` rewrites with this lemma. | VERIFIED-AT-SOURCE (L², not sup) |
| 5 | "`sorry_count: 0`" (yaml) | After stripping comments and strings, the only `sorry` token anywhere is `Challenge.lean:52`, which is intended. 0 in the 503 OAI modules, 0 in HadamardSupport. | VERIFIED-AT-SOURCE |
| 6 | "depends only on propext, Classical.choice and Quot.sound" (README, yaml, CITATION) | No `axiom` declaration and no `native_decide`/`ofReduceBool` anywhere in the cone (project + OAI closure + HadamardSupport). | Consistent at source. NOT VERIFIABLE WITHOUT A BUILD. |
| 7 | "The formal proof follows the paper" / "This repository formalizes the rest of the paper" (README, AUTHORS, yaml) | Thm B.12, Cor B.13 and Lemmas/Theorems B.7–B.11 have no counterpart. The Lean's labels cite classical-incidence.tex lines 6–376 and 808/858 only, and nothing cites lines ~377–807. `WeakPlanar.lean:1910` "/-- ci:weak-planar-distances, replacing CI:808–856. -/"; `:2056` "replaces the exponent in CI:858–874"; `:29` "Elementary circle geometry for the planar replacement; no paper counterpart." Lemma 2.1's c₀ = 1/2 becomes 1/3 (`FlatCaps.lean:458`). App. A's projective-bundle formula (Fulton) is re-derived by a Koszul/Hilbert route ("B13 redesign", TrackB/TripleRankRoute.lean). | CONTRADICTED (partially; see objections L1, L2) |
| 8 | "OpenAI's Lean library supplies the polynomial isolation interface … This repository formalizes the rest" (README, AUTHORS) | 63 OAI modules imported directly, 503 transitively (130,917 lines). About 209 distinct `OAI.*` declarations are named in the project, including the **definitions of affine degree, dimension and Hilbert polynomial** (`Foundations/Affine.lean`: `abbrev dimension … := OAI.QuarticPowerFree.affineDimension`, `abbrev degree … := OAI.QuarticPowerFree.affineDegree`), Hilbert–Serre/Lech, local Bézout, Bertini specialization, and Borsuk–Ulam (`OAI.BorsukNine.SimplicialChains.odd_sphere_dimension_bound`, used for polynomial bisection). yaml does say "alongside further OAI modules used by the geometric tracks". | CONTRADICTED as worded in README/AUTHORS; yaml accurate |
| 9 | "No OpenAI source is copied into this repository" (THIRD_PARTY, NOTICE) | True for the repo. But the OAI "compatibility" patch `PrimeNumberTheoremAnd-lean4341.patch` **adds 47 new files** to the third-party PNT package, among them `Erdos970/HadamardSupport.lean` (6,805 lines, imports Mathlib only). That file is in the cone via the OAI `Jacobsthal/Siegel` modules. | VERIFIED; trust-base note (L9) |
| 10 | "Mathlib commit d13f23b" (README) | Manifest pins the leanprover-community URL at that commit. The GitHub API returns that commit upstream (2026-09-24, "chore: bump toolchain to v4.34.1"). The 23 OAI patches contain **no mathlib patch**. | VERIFIED-AT-SOURCE (pristine pin); Mathlib oleans come from `lake exe cache get` and are re-checked only by `leanchecker --fresh` |
| 11 | "`Challenge.lean` imports only Mathlib" | `import Mathlib.Analysis.InnerProductSpace.PiL2`, `import Mathlib.Analysis.SpecialFunctions.Pow.Real` | VERIFIED |
| 12 | Frozen blob `21648f72…` = `v1.0.0:Challenge.lean` (verify.sh, docs) | `git hash-object Challenge.lean` at HEAD = `21648f72616ee8911640b58864ddd2f072ba4f9c`; GitHub contents API at `0e56d4c` gives the same SHA. | VERIFIED |
| 13 | v1.0.0 → HEAD changes nothing in the proof (implicit) | compare `0e56d4c...88919b8`: 5 commits. Every Lean hunk in 13 files is inside `/-! -/`, `/-- -/` or `--` comments (removes "lane …", "DESIGN.md", "NOTES", "research/planar-shortcut.md"). Also adds `Audit/NonVacuity.lean` and changes verify.sh's frozen check (commit `324083b` → blob id) and docs. | VERIFIED-AT-SOURCE |
| 14 | "Audit/IndependentRestatement.lean … restates the target without the copied definitions … proved equivalent" (README, yaml) | `theorem fc_to_indep (h : FCStatement) : Indep := h` — the equivalence is **definitional** (`Indep` is `FCStatement` with `distinctDistances` unfolded). | VERIFIED but trivial (L4) |
| 15 | "NonVacuity … computes distinctDistances on small sets … derives c n^(2/d) ≤ g_d(n) ≤ C n^(2/d) … minimum is attained" (docs) | Statements as described (`pair_distinct`, `triple_distinct`, `g_attained`, `theta_bounds`, `g_unbounded`, `lower_forces_one`). They are consequences of `jsp_000900`, not independent checks of it, and `g` is the repo's own `sInf` over ℝ, not FC's `minimalDistinctDistances`. | VERIFIED-AT-SOURCE (statements); proofs NOT VERIFIABLE WITHOUT A BUILD |
| 16 | "751 Lean modules with 7572 declarations, 5553 of them theorems; 10181 jobs; 1483 s" (docs) | 750 files under `DistinctDistances/` + `DistinctDistances.lean` = 751 ✓. My grep counts 5,761 `theorem`/`lemma` headers (including private). 743 of the 751 modules are in `Main`'s cone (208,847 lines); 8 are outside it (aggregator roots, `TrackB.NullRigidity`, `TrackC.CanonicalGradient`, `TrackD.Profiles.PartitionRegularization`, `TrackE.OuterLiftAux`). | Module count VERIFIED; decl/job/time counts NOT VERIFIABLE WITHOUT A BUILD |
| 17 | "Independent check of v1.0.0 on a 32-core node … leanchecker --fresh exit 0 (37 minutes)" (docs) | Self-reported by the author; no logs published. The Software Heritage snapshot `swh:1:snp:f64f8482…` exists and has `refs/heads/main = 0e56d4c…`, `refs/tags/v1.0.0 = 3c771f79…` (checked via the SWH API). | SWH VERIFIED; run results NOT VERIFIABLE |
| 18 | "Comparator check of v1.0.0 with two kernels … nanoda … Comparator exited with status 0" (docs, commit 88919b8) | Self-reported. The doc itself says: "The sandbox was comparator's development stand-in for `landrun`, so the run checked the statement match and kernel acceptance without isolating the build from the code it checks." | NOT VERIFIABLE; not isolated |
| 19 | "review: agent-reviewed, reviewers: []"; "AI coding agents wrote the Lean code" (yaml, AUTHORS) | As stated. | VERIFIED (self-description) |
| 20 | `CITATION.cff` v1.0.0, date-released 2026-10-10 | Root commit author date 2026-10-10T18:52:12Z; repo `created_at` 2026-10-10T18:55:27Z. | VERIFIED |

---

## 2. Statement fidelity

### 2.1 The target

`Challenge.lean` lines 42–52, verbatim:
```
theorem jsp_000900 :
    ∀ d : ℕ, 3 ≤ d →
      ∃ c C : ℝ, 0 < c ∧ 0 < C ∧
        (∀ P : Finset (EuclideanSpace ℝ (Fin d)), 2 ≤ P.card →
          c * (P.card : ℝ) ^ ((2 : ℝ) / (d : ℝ)) ≤ (distinctDistances P : ℝ)) ∧
        (∀ n : ℕ, 2 ≤ n → ∃ P : Finset (EuclideanSpace ℝ (Fin d)), P.card = n ∧
          (distinctDistances P : ℝ) ≤ C * (n : ℝ) ^ ((2 : ℝ) / (d : ℝ))) := by
  sorry
```

Clause-by-clause match to Theorem 1.1:

| Lean | Theorem 1.1 |
|---|---|
| `∀ d ≥ 3` | "for every integer d ≥ 3" |
| `∃ c` before `∀ P` | c_d depends only on d |
| `Finset`, `2 ≤ P.card` | "n ≥ 2 distinct points" |
| `distinctDistances P` = card of `P.offDiag.image (dist ·.1 ·.2)` | \|Δ(P)\|, Δ(P) = {\|p−q\| : p ≠ q} |
| `rpow` with exponent `(2:ℝ)/(d:ℝ)` | n^{2/d} |

The second clause is the grid remark. `Upper.lean:148–152` proves it for d ≥ 1 with an explicit `C = 8·d`, using `EuclideanSpace.dist_eq`.

**Nothing in the quantifier structure lets c depend on P or n.** Main.lean takes c from `lower_bound d hd` and C from `upper_bound d`, both outside the `∀ P`.

### 2.2 Non-vacuity and small n

`lower_bound` (`TrackE/Top.lean`) argues by strong induction on d and contradiction:
- `lowerBound_of_IH` starts `by_contra hfail` and gets a `Regime` from `failure_gives_regime`.
- `regime_excluded` gives a uniform `ε₀ > 0, N₀` such that `ε₀ · Ascale d N < Mcount P` for all P with `N₀ ≤ |P|`.
- These contradict each other.

There is no small-n case split that could produce c = 0; `0 < c` is part of the statement. I read OAI's `failure_gives_regime` (PolynomialIsolation.lean:59–112) line by line:
- If no c > 0 works, choose `P_k` with `|Δ(P_k)| < (1/(k+1))·N_k^{2/d}`.
- Since `|Δ| ≥ 1`, this forces `k+1 < N_k^{2/d} ≤ N_k`, so N → ∞ automatically.
- And `(1+|Δ|)/N^{2/d} < 2/(k+1) → 0`.

**Correct.** The `Regime` structure (`Framework/Regime.lean`) has **no rate field**. Its only asymptotic hypothesis is `ratio_tendsto : Tendsto (fun k => (1 + |Δ(P_k)|)/|P_k|^{2/d}) atTop (𝓝 0)`. So if the replay is green, the Lean proof uses no rate for M/A → 0. This is the brief's hazard (i), settled for the Lean's route (not for the paper's text).

### 2.3 Relation to FC's `erdos_1083`

FC Metric.lean@660712 defines:
```
noncomputable def minimalDistinctDistances (n : ℕ) : ℕ :=
  sInf {m : ℕ | ∃ points : Finset X, #points = n ∧ distinctDistances points = m}
```
It is defined through the same `distinctDistances`.

**jsp_000900 ⟹ the RHS of `erdos_1083` (answer `True`).** Fix d ≥ 3 and n ≥ 2, and write g(n) = `minimalDistinctDistances (ℝ^d) n`.
1. The set is nonempty (n distinct points exist), so the ℕ-`sInf` is attained.
2. The lower clause gives g(n) ≥ c n^{2/d} > 0. The upper clause gives g(n) ≤ C n^{2/d}.
3. Put o(n) := 2/d − log g(n)/log n for n ≥ 2. Then n^{2/d − o(n)} = g(n) exactly (rpow with positive base), and |o(n)| ≤ max(|log c|, |log C|)/log n → 0.

The converse fails: n^{2/d − o(1)} allows sub-polynomial losses. So the target is strictly stronger than FC's, as the repo says. **No Lean declaration in the repo mentions `minimalDistinctDistances` or `erdos_1083`**, so this implication is not formalized. NonVacuity's `g` is a separate `sInf` over ℝ, shown to be attained.

### 2.4 What the audit files prove

- **`Audit/TargetProbes.lean`.** `distanceSet ∅ = ∅`; singletons give ∅ and count 0; a pair of distinct points gives exactly 1; `one_le_distinctDistances` for card ≥ 2. These probe the definitions only.
- **`Audit/IndependentRestatement.lean`.** `FCStatement` and `Indep` differ only by unfolding `distinctDistances`/`distanceSet`. The "equivalence" is `fun h => h` (definitional) plus the boundary examples. It adds nothing beyond checking that unfolding gives what you see.
- **`Audit/NonVacuity.lean`.** Imports `DistinctDistances.Main`. It derives consequences of `jsp_000900`:
  - `hyps_joint`: both clauses applied in ℝ³;
  - `g_attained`, `theta_bounds`: two-sided Θ(n^{2/d}) for the minimum;
  - `g_unbounded`, `lower_forces_one`.

  It also computes `{0, e₀}` ↦ 1 and `{0, e₀, 2e₀}` ↦ 2 distances. These are sanity consequences, not independent evidence that the proof is right.

### 2.5 Comparator configuration

`Challenge.json` is `{"challenge_module":"Challenge","solution_module":"DistinctDistances.Main","theorem_names":["DistinctDistances.jsp_000900"],"definition_names":[],"permitted_axioms":["propext","Quot.sound","Classical.choice"],"enable_nanoda":false}`.
- `definition_names: []` means `distanceSet`/`distinctDistances` are compared by body, not treated as holes. That is correct.
- Both modules declare the root-namespace `distanceSet`/`distinctDistances`. They are never in one environment: `Main` never imports `Challenge`, and the lakefile has a separate `lean_lib Challenge`.
- The project contains **no** local instance or notation touching `Dist`, `MetricSpace`, `Norm`, `PiLp`, `WithLp` or `EuclideanSpace`. Instances found are all finiteness, `Membership` or graded-algebra.

So a wrong-metric elaboration in `Main` is not supported by the source. The pp.all comparison is the build-time check for it.

---

## 3. Kernel bypasses

### 3.1 Scan results

Scanner: `lean_audit_scripts/scan.py`. It strips nested block comments, line comments and string literals before matching.

| Construct | Project (757 files) | OAI closure (503 modules) | HadamardSupport.lean (PNT, patch-added, in cone) |
|---|---|---|---|
| `sorry` | 1 (`Challenge.lean:52`, intended) | 0 | 0 |
| `admit` (tactic) | 0 | 0 | 0 |
| `axiom` declaration | 0 | 0 | 0 |
| `native_decide` / `ofReduceBool` / `reduceBool` | 0 | 0 | 0 |
| `implemented_by` / `@[extern]` / `unsafe` / `opaque` / `partial def` / `@[csimp]` | 0 | 0 | 0 |
| `set_option debug.*` (incl. `debug.skipKernelTC`) | 0 | 0 | 0 |
| `addDecl` / `Kernel.` / `Environment.add` / `unsafeCast` | 0 | 0 | 0 |
| `elab` / `macro` / `syntax` / `run_cmd` / `#eval` / `initialize` | 0 | 0 | 0 |
| `import Lean` | 0 | 8 (6× `Lean.Elab.Tactic.Omega`, 2× `Lean`), none with meta code | 0 |
| notation | 0 | 34, all `local notation` abbreviations (e.g. `"E" => EuclideanSpace ℝ ν`) | 0 in HadamardSupport (5 `local notation`s exist in other Erdos970 files that are not in the cone) |
| `set_option` | 207: `maxHeartbeats` (≤ 5·10⁷), `backward.isDefEq.respectTransparency` true/false, `autoImplicit false`, linters, `synthInstance.maxHeartbeats` | 0 | 0 |
| `decide` | 68, all tiny (`(1 : Fin 2) ≠ 0`, `(0:ℚ) ≤ 1`, `Finset.univ (Fin 2) = {0,1}`) or `decide (p)` used as a Bool value | 83 (not reviewed individually; kernel-checked) | — |

The only `partial def` / `elab_rules` / `syntax` in the PNT patch are in `Erdos970/Tactic/AdditiveCombination.lean`, which is **not** imported by `HadamardSupport.lean` (that file imports `Mathlib` only).

### 3.2 What `#print axioms` (verify.sh step 5) catches, class by class

| Class | Caught by `#print axioms`? | Notes |
|---|---|---|
| `sorry` / `admit` | yes (`sorryAx`) | — |
| `axiom` declarations | yes (listed) | — |
| `native_decide` | yes (`Lean.ofReduceBool` or an auxiliary axiom) | — |
| `implemented_by` / `extern` | only via `native_decide` / `#eval`-in-proofs | The kernel ignores compiled code. |
| `unsafe` | n/a | The kernel rejects unsafe constants in safe declarations. |
| `opaque` / `partial` | n/a | Sound (needs an `Inhabited` witness); not an axiom. |
| `set_option debug.skipKernelTC true`, or meta code adding declarations without checking | **NO** | The declaration enters the environment unchecked and its term may cite only standard axioms. Caught only by `leanchecker --fresh` (in our `run.sh`) or Comparator/nanoda re-checking from export. Source scan: 0 occurrences of either in the cone. |
| Tampered or stale `.olean` (e.g. Mathlib from `lake exe cache get`) | **NO** | `#print axioms` reads stored terms and does not re-check them. Caught by `leanchecker --fresh`. |
| Notation or instance shadowing that changes the statement | **NO** | Caught by `check_target.py statement` (pp.all) and Comparator. Source: none present. |
| `maxHeartbeats`, `respectTransparency` | n/a | Elaborator resources and unification only. |
| Lakefile code execution: OAI's `lakefile.lean` has `run_cmd` with `unsafe env.evalConstCheck` and `IO.Process` git clone/apply | n/a | A build-environment supply-chain issue, not a kernel bypass. This is why landrun isolation matters, and the author's Comparator run lacked it. |

`check_forbidden.py` scans only the project and only for `sorry`/`admit`/`axiom`/`native_decide`/`implemented_by`/`extern`/`unsafe`. It does not look for `debug.skipKernelTC`, meta code, or anything in OAI or the patched packages. My scan above covers those.

### 3.3 `OuterPool.lean:1572` "admit"

Lines 1533–1573 are a calc proof of `hfinal : ((Filt \ G).card : ℝ) ≤ ρ' * (pool.S.card : ℝ) ^ 2`. Then comes a roughly 30-line comment of agent reasoning about whether `set`-bound `Filt`/`Sel` unfold definitionally. Line 1572 is:

`-- For now, admit final conversion via simpa (Filt = Sel.filter..., Sel = outerSelectedGraph)`

The next line, 1573, is the actual tactic `simpa only [hFiltdef, hSeldef] using hfinal`. **Nothing is admitted.** "admit" appears only in a comment, and the other 14 occurrences of "admit" in the project are the English word "admits". A `sorry`/`admit` would show as `sorryAx` anyway.

### 3.4 Patches (`*-lean4341.patch`)

The 23 patches target third-party packages pinned by OAI. **There is no Mathlib patch.** The only patched package in the cone is PrimeNumberTheoremAnd. Its patch:
- **adds 47 new files** (Erdos970/*, SiegelZeros/*, Catalan/*, ZetaFive/*);
- modifies `Fourier`, `SmoothExistence`, `Sobolev`, `Wiener`, `IEANTN/Mertens`, `PerronFormula`;
- in `lakefile.toml`, drops linter options and adds `leanOptions = { autoImplicit = false }` plus four new `lean_lib`s;
- bumps `lean-toolchain` v4.34.0 → v4.34.1.

None of the hunks I read sets a kernel-relevant option. The in-cone file `Erdos970/HadamardSupport.lean` scans clean. PNT is built from source (no cache), so the kernel checks it during `lake build`. I did not read the other 22 patches: no module of those packages is imported by the cone (the cone's import roots are `Lean`, `Mathlib`, `OAI`, and `PrimeNumberTheoremAnd.Erdos970.HadamardSupport` only).

---

## 4. Structure

### 4.1 Size and import graph

| Body | Modules | Lines |
|---|---|---|
| Project, all files | 751 | 209,786 |
| `DistinctDistances.Main` cone (`Main` → `Upper` + `TrackE.Top`) | 743 | 208,847 |
| OAI imported directly | 63 | — |
| OAI transitive closure | 503 | 130,917 |
| PNT `HadamardSupport` (patch-added) | 1 | 6,805 |

By namespace, the OAI declarations named in the project are: `QuarticPowerFree` (52), `PiExponentJets.W22/W24/W64/…` (~60), `ErdosDistinctDistances` (13), `Lech.*` (~15), `BorsukNine.SimplicialChains` (5), `MaximalSeshadri.BertiniIntegral` (5), `PiExponent.WeightedBezout` (5), `Erdos970.WeightedTorusJets` (6), `PiExponentSiegel.*`, `PermanentBorder.*`, `Nagata.*`, `ExactFourier`, `BoundaryOnly.…AnalyticReducedness`.

### 4.2 Tracks → paper sections

From the docstring `.tex` references:

| Track | Lines | Paper | `.tex` refs |
|---|---|---|---|
| Framework | 718 | §2.1 regime, asymptotic conventions | — |
| Foundations | 6,352 | variety model; degree/dimension are OAI's Hilbert invariants | — |
| TrackA | 32,151 | §3 (polynomial.tex: separators, interpolation, component Hilbert ranks, regularity, pooling, projection) | 79 |
| TrackB | 49,313 | App. A (concentration.tex) | 78 |
| TrackC | 30,733 | §7 (motions.tex) + App. B (classical-incidence.tex), with the planar replacement | 71 + 3 |
| TrackD | 34,910 | §4 (secants.tex) + §5 (profiles.tex) | 86 + 104 |
| TrackE | 50,600 | §2 (reduction.tex) + §6 (sparse-cones.tex, depth.tex = §6.3) + top | 119 + 178 + 41 |
| Bridges | 4,485 | glue | — |
| OAIInterface | 89 | wrappers | — |

### 4.3 Named paper results → Lean counterparts

| Paper | Lean declaration (file) | Notes |
|---|---|---|
| Thm 1.1 lower bound | `DistinctDistances.lower_bound` (TrackE/Top.lean) | strong induction on d ≥ 3 |
| Grid remark | `DistinctDistances.upper_bound` (Upper.lean), C = 8d | — |
| (2.1) regime | `Regime`, `failure_gives_regime` (Framework/Regime.lean); OAI `ErdosDistinctDistances.failure_gives_regime` | no rate field |
| Lemma 2.1 | TrackE/FlatCaps.lean: `card_inter_line_le` (≤ 2M−1), `card_inter_circle_le`, `card_inter_flat_le_of_IH` (3 ≤ u < d, C M^{u/2}), **`card_inter_plane_le` (C·M^{4/3}, not C M log 2M)**, `card_inter_proper_flat_le` (N·B^{−1/3}, **c₀ = 1/3, not 1/2**), `card_inter_proper_complex_flat_le`, `card_inter_flat_le_rpow` (B^{u+ε}, u ≥ 3) | "Planes have the more precise bound B^{2+o(1)}": **NOT FOUND** (replaced by C·B^{8/3}) |
| Prop 2.2 | `Reduction.exists_selection_directionCaps` (TrackE/Directions.lean:569), via `card_pairs_on_rich_lines`, `exists_greedy_family`, `exists_light_greedy_selection` (fixed H, K, from `sparse_cones`), `directionCaps_of_light_greedy` | finitary: ∃ c, C, ε, N₀ ∀ P |
| Prop 2.3 | `exists_selection_starRank`, `exists_selection_independentStars` (TrackE/Stars.lean:646, 734) | uses `TrackA.poly_envelope_projective_lower` |
| §2.3 graph + d = 3 deletion (2.4)–(2.5) | `Reduction.exists_retained_graph` (TrackE/Graph.lean:525) | isotropic cap C₀ A^{d−2}; d = 3 via `Request.RichMotions` |
| Lemma 2.4 | `Reduction.global_concentration` (TrackE/GlobalConcentration.lean:26), `global_rank_lower` (Concentration.lean:30) | — |
| Lemma 2.5 | `Reduction.local_concentration`, `local_concentration_ambient` (Concentration.lean:175, 485) | — |
| Prop 2.6 | `Reduction.main_contradiction` (Contradiction.lean:151) + `regime_excluded` (Top.lean) | fixed θ, Chernoff-type union bound `|W|·exp(−θ²δ/2) < 1/2` |
| Lemma 3.6 | `TrackA.poly_hilbert_lower`, `poly_hilbert_at_L`, `poly_hilbert_union_lower`, `poly_hilbert_projective_lower/at_L`, `poly_envelope_lower/projective_lower` (TrackA/Hilbert.lean) | `c·deg(F)·L^k ≤ H_F(L)` for F pure of dim k whose members are minimal primes of an ideal generated in degree ≤ L (`ComponentsDefinedInDegree`). No Chardin/Philippon/Walsh name appears anywhere in the project or the OAI closure: the inputs the paper cites are re-proved, by a route I did not audit. |
| Prop 4.3 | `TrackD.geo_terminal` (TrackD/Terminal.lean:33), finitary | hypotheses: `M ≤ ηA`, `RealFlatCap P c₀` for **any** fixed c₀ > 0 — no plane cap |
| Thm 6.1 (sparse cones) | `SparseCones.sparse_cones` (TrackE/SparseCones.lean) | finitary: ∃ η, δ₀, ε₀, N₀ such that, when deg C_p ≤ δ₀N/A, at least ηN² ordered pairs are covered in **neither** orientation (`uncoveredPairs`: `¬DirCovered C e.1 e.2 ∧ ¬DirCovered C e.2 e.1`). Families are irreducible curves spanning ≤ P² (`IsDirectionalFamily`). This is the either-endpoint form; the sequential form follows. |
| Thm 7.1 | `TrackC.mot_rich`, `mot_rich_deletion`, `very_rich_two_clouds` (TrackC/RichMotions.lean); `Bridges.rich_motions_rotated` | follows motions.tex parameters (r = t^{15/14}, etc.); uses `ci_rich_lines` (B.5) via Planar/MotionLocal |
| Thm A.1 | `TrackB.uniform_concentration`; `Bridges.uniform_concentration_bridge` (Bridges/UniformConcentration.lean:752) | stated for 1 ≤ h < e−1 (paper: 0 ≤ h < r; h = 0 is trivial). The projective-bundle Segre formula (Fulton) is **not** formalized; it is replaced by a Hilbert/Koszul identity `TrackB.triple_rank_identity` ("B13 redesign") |
| Thm B.2 (S–T) | `TrackC` `ci_st` (Incidence.lean:750, 1328); `Bridges.ci_st_rich_real`, `ci_st_affine` | — |
| Lemma B.3 (bisection) | `TrackC.polynomial_bisection_construct`, `ci_partition_dim`, `ci_partition` (Polynomial.lean:70–110) | uses OAI Borsuk–Ulam |
| Lemma B.4 (critical/flat lines) | `ci_flat(1)–(4)` (Polynomial.lean:656, 1003, 1069, 1302) | — |
| Thm B.5 (Guth–Katz, k ≥ 3) | `TrackC.ci_rich_lines` (Incidence.lean:3796): `R_k ≤ C(L^{3/2}/k² + L·B/k³ + L/k)`, k ≥ 3, plane cap B | matches the paper's B.5 shape |
| Cor B.6 | `ci:planar-motions` (TrackC/Planar.lean:1495, both orientations) | — |
| Lemma B.7, B.8, B.9; Thm B.10 (two-rich points); Lemma B.11 | **NOT FOUND** | no `ruled`/`regulus`/`flecnode`/`two-rich` theorem; the only "Two-rich" hit is a finiteness remark in RichLineTail.lean:11 |
| Thm B.12 (planar Ω(n/log n)) | **NOT FOUND**; replaced by `TrackC.ci_weak_planar_distances` (WeakPlanar.lean:1911): `∃ c > 0, ∀ X : Finset (E 2), 2 ≤ X.card → c · X.card^{3/4} ≤ |positiveDistances X|`. Proof: K_{3,2}-free count `three_point_incidence_bound` → circle partition → `ci_point_circle_incidence` (I ≤ K(n^{3/5} m^{4/5} + n + m) for n ≤ m) → `distance_circles`. | — |
| Cor B.13 | **NOT FOUND**; replaced by `ci_planar_occupancy` (≤ C M^{4/3}) and `planar_occupancy_sequence` (≤ B^{8/3}) | — |

### 4.4 Which planar bound the Lean uses, and where

There is exactly one planar distinct-distance input in the cone: `TrackC.ci_planar_occupancy`. It is consumed only through `Bridges.planar_occupancy_mcount` (→ `Request.PlanarOccupancy`) and `TrackE.FlatCaps.card_inter_plane_le`. The induction hypothesis covers only 3 ≤ u < d (`IH`), so **for d = 3 the weak planar bound is the only lower-dimensional input.**

The paper's three uses of the plane cap and their Lean replacements:
1. **p. 7, Lemma 2.1 (uniform c₀).** "Thus, for example, c₀ = 1/2 works after advancing along the sequence." Lean: `card_inter_proper_flat_le`, whose docstring says "with c₀ = 3 − 2·(4/3) = 1/3 after the planar shortcut … (For d = 3 the plane bound C M^{4/3} equals C N B^{−1/3} at M = A, so a small ε₀ is needed.)"
2. **p. 31, §4 (after (4.2)).** "The contribution of N/s to h_s F is at most CN B^{2+o(1)}(1 + log N)² = o(N²), using the plane cap and d ≥ 3." Lean: Track D's only flat hypothesis is `RealFlatCap P c₀` (`TrackD/Basic.lean:56`: every proper flat ≤ N·B^{−c₀}, any fixed c₀ > 0). No plane-specific cap occurs in TrackD.
3. **p. 47, §6.2.** "each lies in a proper flat containing at most B^{k+1+o(1)} sample points … B^{d−2k} B^{k+1+o(1)} = B^{d−k+1+o(1)} = o(n₀)". Lean `MOFlatAux.lean:331`: "Plane cap: |P ∩ H| ≤ C M^{4/3} ≤ C B^{8/3} ≤ B^{k+1+ε} (needs k ≥ 2)."
4. Also Prop 2.2, p. 9: "For a ≥ 2, Lemma 2.1 bounds the counted partners by O(A²)." Here C M^{4/3} ≤ C A^{4/3} = O(A²).

**My inference, not machine-checked for other exponents:** with planar |Δ| ≥ c n^β, use 1 needs 2/β < 3, use 3 needs 2/β ≤ 3 (with log room), and use 4 needs 2/β ≤ 4. So any β > 2/3 serves these consumers. β = 3/4 is what the Lean proves. Moser's n^{2/3} would make c₀ = 0 at d = 3 and fail.

**Theorem 7.1 does consume Guth–Katz higher-richness.** p. 62: "The incidence inputs are the Szemerédi–Trotter bound, Theorem B.2, and the higher-richness Guth–Katz bound, Theorem B.5." The Lean proves B.5 (`ci_rich_lines`) with polynomial partitioning, and B.6. So the part of App. B that *is* needed is B.1–B.6. The Lean does not need B.7–B.13, which hold the hardest, most compressed argument in the appendix (ruled surfaces → two-rich points B.10 → B.12).

### 4.5 What OAI supplies

**`OAI.Combinatorics.Distances.PolynomialIsolation` (392 lines).** The module provides:
- `distances` (off-diagonal image), `mem_distances`, `distance_pos`, `distances_mono`, `one_le_card_distances`;
- `failure_gives_regime` and `regime_precludes_bound`;
- `squaredDistancePolynomial` (deg ≤ 2), `separatorFactor`, `physicalSeparator` (deg ≤ 2|Δ|, value 1 at p and 0 at other points of P), `eval_physicalSeparator`;
- `isolationPolynomials` (deg ≤ 2|Δ|+1), `isolation_zero_iff` (common zeros = P), `linearIndependent_physicalSeparator`;
- `finrank_restrictDegree` ((L+1)^d);
- `elementary_card_bound` (|P| ≤ (2|Δ|+1)^d);
- `lengthFiber`, `equalLengthPairs`, `equalLengthPairs_lower_bound` (|S|² ≤ |Δ|·#equal-length pairs: Cauchy–Schwarz, cf. (2.4)).

All of this is elementary and clean.

**The rest of the OAI closure** (PiExponent/LocalAlgebra 113 files, AlgebraicGeometry/PlaneCurves 76, RingTheory/Multiplicity 71, NumberTheory/PowerFree 44, Algebra/Determinantal 42, FrobeniusObstruction 35, AlgebraicObstruction 29, Geometry/Borsuk 30, Seshadri/Bertini 9, Jacobsthal/Siegel 8, …) supplies:
- Hilbert polynomials and the very definitions of affine dimension and degree (`QuarticPowerFree.affineDimension`, `affineDegree`, `coordinateHilbert`);
- the projective Hilbert polynomial (`PiExponentJets.W22.actualHP`);
- Lech / Hilbert–Serre length theory, local and weighted Bézout, Bertini countable specialization;
- graded linear normalization, determinantal regular sections;
- Borsuk–Ulam (`odd_sphere_dimension_bound`, used for polynomial bisection).

**All 503 modules are complete at source:** 0 `sorry`, 0 `axiom`. Their soundness rests on the kernel replay like everything else.

---

## 5. Provenance

**Public history (GitHub API, paginated): 6 commits, all by "Yao Xu `<Xy2462381442@gmail.com>`".**

| sha | date (UTC) | message |
|---|---|---|
| 0e56d4c | 2026-10-10 18:52:12 | Formalize the higher-dimensional Erdős distinct-distances bound in Lean 4 — **root commit, no parents, +211,476/−0**; tag v1.0.0 (annotated `3c771f79`) |
| d90bdf2 | 20:51:12 | Record the independent check of v1.0.0 |
| d2610b8 | 22:43:43 | Add non-vacuity checks |
| 03a41f0 | 23:26:16 | Check the frozen Challenge.lean by its blob id |
| 7af0dff | 23:26:53 | Remove references to development notes from comments |
| 88919b8 | 2026-10-11 02:42:00 | Record a Comparator check of v1.0.0 with two kernels |

- The span is 7 h 50 min; repo created 18:55:27Z.
- **The development history is not public.** JSP PR #4994 says: "The repository was published as a single commit; the development history is not public."
- Lane names survive only in the comments removed by `7af0dff`: `lead-c`, `lead-d`, `m-b-hilb` ("B13 redesign (lane m-b-hilb, 2026-10-10)"), `m-b-part2`, `bridges-b`.
- The same comments name private files: `runs/lanes/lead-d/DESIGN.md`, `research/planar-shortcut.md`, `BLUEPRINT.md`, `NOTES`.
- `verify.sh` at v1.0.0 pinned `FROZEN=324083b`, a commit absent from the public history.
- The sibling repo `hypercube-ramsey-lean4` has a public commit "Merge lane opus-s05-k1" (2026-10-08). That is consistent with agent lanes, possibly Claude Opus; this is an inference.

**Author.** GitHub profile created 2023-08-31, bio "LLM inference on consumer hardware", 15 public repos. Same-pattern sibling repos: `hindman-sums-products-lean4` (#172), `hypercube-ramsey-lean4` (#181), `artin-primitive-roots-lean4`, `catalan-lean4`. The author also forks `TheJustinSunPrize/awards` and `formal-conjectures`.

**Bounty framing.**
- The JSP catalog entry at `16877004` (lines 1708–1724) records "Lean proof | No" and "Eligible to claim | No". Its review note reads: "Reports that for each fixed dimension d ≥ 3 every n-point set determines at least c_d n^(2/d) distinct distances … This records the higher-dimensional conjecture, not an exact leading constant." `Challenge.lean`'s docstring paraphrases this.
- The author opened **JSP PR #4994** (2026-10-10T20:53Z, open) claiming Lean-formalization credit for JSP-000900 at `0e56d4c`. It states the statement is a "proposed statement requiring review. I know of no maintainer-approved Lean statement for JSP-000900."
- FC issue #6905 (mo271, 2026-10-07, open) proposes marking `erdos_1083` true on the strength of the paper.

**Self-reported checks.** The 32-core "independent check" (`lake build` and `leanchecker --fresh` exit 0) and the Comparator + nanoda run are reported by the author with no logs. The Comparator run explicitly used a non-isolating sandbox stand-in.

**Not provenance problems in themselves:** AI-written code, a squashed history, and agent-only review. They do mean that **the only trust anchor is the kernel replay** together with the statement check in §2.

---

## 6. What could make a kernel-green build NOT mean Theorem 1.1

1. **Wrong target.** Ruled out at source (§2): same quantifiers, L² metric, real rpow, non-vacuous, definitions verbatim from FC. Residual: the elaborated-type identity between `Challenge` and `Main`, checked by `check_target.py statement` in our `verify.sh` step and by Comparator.
2. **Modified Mathlib.** No Mathlib patch exists. The manifest pins upstream `d13f23b`. Cached oleans are re-checked only by `leanchecker --fresh`, which our `run.sh` runs.
3. **Unchecked declarations** (`debug.skipKernelTC`, meta `addDecl`). Absent at source in project, OAI closure and HadamardSupport. `leanchecker --fresh` would catch them in any case.
4. **Trivialized constant.** Impossible: `0 < c` is in the statement.
5. **Patched dependencies.** Only the PNT patch reaches the cone, by **adding** `HadamardSupport.lean`. It is built from source, so it is kernel-checked, and it scans clean.
6. **What a green build would *not* certify:**
   - the paper's text (the Lean takes a different planar route and a different App. A degree computation, with finitary restatements throughout);
   - that the intermediate Lean definitions (degree, dimension, Hilbert function via OAI) match the paper's notions — they cannot affect the truth of the final statement;
   - FC's `erdos_1083` (not formalized; one short step, §2.3).

---

## 7. Objections

**L1 — README/AUTHORS overstate fidelity to the paper and understate OAI's share.**
- Location: README "How the proof is organized"; AUTHORS.md ¶2; yaml `project.description`.
- Quotes: "OpenAI's Lean library supplies the polynomial isolation interface (physical separators and isolation polynomials for the distance problem). This repository formalizes the rest of the paper" (README). Also "The formal proof follows the paper and takes the polynomial isolation interface … from OpenAI's Lean library" (AUTHORS).
- What is wrong:
  - (a) OAI supplies 503 modules / 130,917 lines, including the definitions of degree and dimension, Hilbert–Serre/Lech, local Bézout, Bertini and Borsuk–Ulam (§4.5).
  - (b) The repo does **not** formalize Theorem B.12, Corollary B.13 or B.7–B.11, nor the App. A projective-bundle formula. It replaces them (§4.3–4.4).
- Severity: COSMETIC for the theorem. A GAP in the provenance claim "follows the paper" — an exposition gap, not a mathematical one.
- Fix: state the planar replacement and the OAI dependency surface in the README.

**L2 — Finding about the PAPER: the full planar strength is not consumed.**
- Location: paper p. 7 (§2.1, Lemma 2.1); App. B pp. 95–101 (B.7–B.13); uses on pp. 9, 31, 47.
- Quotes: "We also use the planar result proved in Theorem B.12." / "Planes have the more precise bound B^{2+o(1)}." / "Thus, for example, c₀ = 1/2 works" (p. 7); "CN B^{2+o(1)}(1 + log N)² = o(N²), using the plane cap and d ≥ 3" (p. 31).
- What is wrong: nothing is false. The Lean route shows that |Δ| ≥ c n^{3/4} in the plane (Pach–Sharir-type point–circle incidences) suffices for every consumer, with c₀ = 1/3 and planes ≤ B^{8/3} (`WeakPlanar.lean:1911, 2058, 2168`; `FlatCaps.lean:426, 462`; `MOFlatAux.lean:331`; `TrackD/Basic.lean:56`).
- Severity for the paper: COSMETIC (over-strong input). For refereeing it is significant: **if the replay is green, App. B §§B.4–B.7 (two-rich points, ruled surfaces, n/log n) are off the critical path**, including at d = 3. B.2, B.5 and B.6 remain on it (Theorem 7.1, p. 62).
- This is conditional on the kernel replay.

**L3 — The FC implication is not formalized.**
- Location: repo-wide (no `minimalDistinctDistances`).
- Quote: "Formal Conjectures' `Erdos1083.erdos_1083` … asks for the weaker `n^(2/d - o(1))` form" (THIRD_PARTY).
- What is wrong: jsp ⟹ FC right-hand side is true (§2.3) but is left to the reader; NonVacuity's `g` is not FC's `minimalDistinctDistances`.
- Severity: COSMETIC (exposition).
- Fix: a ~30-line lemma deriving `erdos_1083`'s right-hand side from `jsp_000900`.

**L4 — The "independent restatement" is definitional.**
- Location: `Audit/IndependentRestatement.lean`.
- Quote: "`theorem fc_to_indep (h : FCStatement) : Indep := h`".
- What is wrong: it is equivalent by `rfl`; it is not an independent check of fidelity.
- Severity: COSMETIC.

**L5 — Squashed, private-history, agent-reviewed provenance.**
- Location: GitHub history; yaml `review`.
- Quotes: "The repository was published as a single commit; the development history is not public." (PR #4994); "No independent human expert has reviewed the formalization." (yaml).
- Severity: not a soundness issue. It means **all trust rests on the replay**.

**L6 — The second-kernel claim is unisolated and self-reported.**
- Location: docs/verification.md "Comparator check of v1.0.0".
- Quote: "The sandbox was comparator's development stand-in for `landrun`, so the run checked the statement match and kernel acceptance without isolating the build from the code it checks."
- What is wrong: OAI's lakefile executes `run_cmd` with `unsafe env.evalConstCheck` and `IO.Process` at configure time, so isolation matters.
- Severity: UNCLEAR (provenance).
- Fix: an independent Comparator + nanoda run under landrun. Our replay runs `leanchecker --fresh` but not Comparator/nanoda.

**L7 — Stale or misleading comments on proved declarations.**
- Location: `TrackB/Degree.lean:5776–5777`; `TrackE/Requests.lean:104–120`; `TrackD/Inputs.lean:55–66`; `OuterPool.lean:1544–1572`.
- Quotes: "This is the unresolved singular-base foundation, not an assumption in a data record." (Degree.lean, on the proved `triple_rank_identity`); "Placeholder for track C's `ci:planar-occupancy`." (proved by `exact Bridges.planar_occupancy_mcount`); "-- For now, admit final conversion via simpa".
- What is wrong: each is a real proof; the source contains no `sorry`/`admit`.
- Severity: COSMETIC.

**L8 — `check_forbidden.py` coverage gap.**
- Location: `scripts/check_forbidden.py`.
- Quote: "Scans every Lean source under DistinctDistances/, Audit/ and scripts/ … for `sorry`, `admit`, `axiom` declarations, `native_decide`, `implemented_by`, `extern` and `unsafe`."
- What is wrong: it does not scan OAI or the patched packages, and does not look for `debug.skipKernelTC` or meta code (the one class `#print axioms` cannot see).
- Severity: COSMETIC (my scan covers it; `leanchecker --fresh` backstops it).

**L9 — The OAI "compatibility" patch injects mathematics into a third-party package that sits in the trust base.**
- Location: `openai/math@adc7f124 lean/patches/PrimeNumberTheoremAnd-lean4341.patch`.
- Quote (patches/README.md): "Compatibility patches for third-party Lean dependencies."
- What is wrong: the patch adds 47 new files, among them `Erdos970/HadamardSupport.lean` (6,805 lines), which is in the cone.
- Severity: COSMETIC (kernel-checked from source; scans clean).

**L10 — The agent blueprint of App. A had a false intermediate statement; the Lean re-routed.**
- Location: `TrackB/MBPart2Aux.lean:1–17`; `TrackB/TripleRankRoute.lean:1–28`.
- Quotes: "The frozen statement, which quantifies over an arbitrary weight `w` and arbitrary `μ`, is false as stated; see `dehomogenize_instance_hyps` / `dehomogenize_rank_conclusion_false` for a machine-checked counterexample"; "no global regular sequences are claimed (they fail on non-Cohen–Macaulay bases)".
- What it means: this is about the agents' own intermediate statements, not the paper. The paper (App. A, p. 85) uses Fulton's projective-bundle formula and says "This formula applies equally to a vector bundle on a singular base [14, Sections 3.1–3.3]". The Lean does not formalize that formula; it proves a specialized Hilbert-function identity instead.
- Severity: UNCLEAR. It is a pointer for the App. A referee, not an objection to the paper.

**L11 — Thm A.1 analogue range.**
- Location: `Request.UniformConcentration` / `uniform_concentration_bridge`: `1 ≤ h → h < e − 1`. Paper: 0 ≤ h < r.
- Severity: COSMETIC. For h = 0, an irreducible V of dimension s₀ containing an s₀-dimensional flat equals that flat.

---

## 8. Citation table (this scope)

| Cited / referenced item | What the repo says it is | What the source says (quote) | Verdict |
|---|---|---|---|
| FC `FormalConjecturesForMathlib/Geometry/Metric.lean` @660712 | source of `distanceSet`, `distinctDistances` | "noncomputable def distanceSet (points : Finset X) : Finset ℝ := points.offDiag.image fun (pair : X × X) => dist pair.1 pair.2" / "noncomputable def distinctDistances (points : Finset X) : ℕ := #(distanceSet points)" | MATCH (verbatim) |
| FC `ErdosProblems/1083.lean` @660712 | weaker n^{2/d − o(1)} form | "∃ o : ℕ → ℝ, o =o[atTop] (1 : ℕ → ℝ) ∧ ∀ᶠ n : ℕ in atTop, (minimalDistinctDistances (ℝ^d) n : ℝ) = (n : ℝ) ^ ((2 : ℝ) / (d : ℝ) - o n)" | MATCH |
| FC `Geometry/Euclidean.lean` @660712 | (implicit) `ℝ^d` | "scoped[EuclideanGeometry] notation "ℝ^" n:65 => EuclideanSpace ℝ (Fin n)" | MATCH |
| Mathlib d13f23b `PiL2.lean` | Euclidean distance | "abbrev EuclideanSpace (𝕜 : Type*) (n : Type*) : Type _ := PiLp 2 fun _ : n => 𝕜"; "theorem EuclideanSpace.dist_eq … dist x y = √(∑ i, dist (x i) (y i) ^ 2)" | MATCH |
| JSP catalog @16877004, JSP-000900 | "review note reads the solution as … at least c_d n^(2/d) … with no exact leading constant" | "Reports that for each fixed dimension d ≥ 3 every n-point set determines at least c_d n^(2/d) distinct distances, matching the order of the lattice construction. This records the higher-dimensional conjecture, not an exact leading constant." | MATCH |
| OAI `PolynomialIsolation.failure_gives_regime` | "TOP.regime … restatement" (OAIInterface/Distances.lean) | statement at PolynomialIsolation.lean:59–68, as restated, with `distances` ≡ `distanceSet` (both `P.offDiag.image (dist ·.1 ·.2)`) | MATCH |
| Paper Thm B.12 (p. 101) | "replacing CI:808–856" | Paper: "Every finite set Q ⊂ R² of n ≥ 2 points determines at least cn/log(2n) distinct positive distances." Lean: `c * |X|^(3/4) ≤ |positiveDistances X|` | Replaced by a weaker statement (by design; L2) |
| Paper Thm B.5 (p. 93) | `ci_rich_lines`, "CI:214–336; no quadric cap" | Paper: "Let L be L distinct lines in R³, with at most B₀ in any affine plane. For every integer k ≥ 3, the number R_k of points lying on at least k lines satisfies R_k ≤ C(L^{3/2}/k² + LB₀/k³ + L/k). There is no assumption about lines on quadrics in this theorem." (read from the rendered PDF page 93). Lean: `FiniteCardBound (richPoints L k) (C * (L^{3/2}/k² + L·B/k³ + L/k))`, k ≥ 3, `planeCap L B`, "no quadric cap" | MATCH |

External mathematical citations (Chardin, Chardin–Philippon + erratum, Walsh, Guth–Katz, Tidor–Yu–Zakharov) are not imported or axiomatized in the Lean. Everything is proved inside the cone, so there is no citation dependence to check in my scope.

## 9. Constant-dependency table (Lean route; from statements read)

| Constant | Fixed where | Depends on | Used where | Independent of |
|---|---|---|---|---|
| c (lower clause) | `lower_bound d` (by_contra, non-constructive) | d | `Main.jsp_000900` | P, n (∃ before ∀ P) |
| C (upper) | `upper_bound`: `8 * d` | d | Main | n |
| ε₀, N₀ | `regime_excluded` = min(ε₁, ε₂, 1, θc₃/(4C)), max(N₁, N₂, 2) | d (via IH) | `lowerBound_of_IH` | P, sequence, rate |
| θ, C₁, s₀, κ, N₂ | Top.lean: θ = min(1, c₄/(4C₁)), C₁ = (1+s₀)^{s₀}, s₀ = C(d,2), κ = θ²c₃/2 | d | `main_contradiction` | P |
| c, ε₁, N₁ | `exists_selection_independentStars` | d (via `sparse_cones`, `poly_envelope_projective_lower`) | Top | P |
| H, K | `exists_light_greedy_selection` (∃ before ∀ P) | d | Prop 2.2 analogue | P |
| c₃, C₀, ε₂ | `exists_retained_graph` | d, c | Top | P, R |
| c₄ | `global_rank_lower` | d | Top | P, Q, W |
| C (local) | `local_concentration_ambient d C₀` | d, C₀ | Top | P, f |
| C_plane; c₀ = 1/3 | `ci_planar_occupancy` (absolute); `card_inter_proper_flat_le` | absolute; d | Lemma 2.1 analogue; Track D `RealFlatCap` | P |
| C_rich, K_rich | `mot_rich` | absolute | d = 3 deletion | P, congruent copy |
| η, δ₀, ε₀, N₀ | `sparse_cones` | d (via IH) | `exists_light_greedy_selection` | P, families C_p |

The kernel enforces these quantifier positions. No constant in a statement I read depends on the sequence or on a rate.

## 10. Read line by line vs skimmed

**Read line by line:**
- `Challenge.lean`, `Challenge.json`, `Defs.lean`, `Main.lean`, `lakefile.lean`, `lake-manifest.json`, `lean-toolchain`;
- all of `scripts/*`;
- README, AUTHORS, CITATION, THIRD_PARTY, NOTICE, `formalization.yaml`, `docs/verification.md`;
- `TrackE/Top.lean` (all 259 lines), `Framework/Regime.lean`, `OAIInterface/*.lean`;
- OAI `PolynomialIsolation.lean` lines 1–125 (incl. the `failure_gives_regime` proof), plus the remaining statements;
- `TrackE/SparseCones.lean`, `TrackE/Directional.lean`, `TrackE/Requests.lean`, `Bridges/CPlanar.lean`;
- `FlatCaps.lean` 400–480 and 795–830, `OuterPool.lean` 1500–1600;
- `Audit/IndependentRestatement.lean` (all), `MBPart2Aux` and `TripleRankRoute` headers;
- the full v1.0.0→HEAD compare diff;
- the PNT patch lakefile/toolchain hunks; OAI `lakefile.lean` 1–40 and 240–340;
- the FC `Metric.lean`/`1083.lean` files; the Mathlib `PiL2.lean` definitions; the JSP entry and PR #4994 body.

**Statements only (proofs not read; they rest on the replay):**
- WeakPlanar (`three_point_incidence_bound`, `circle_partition_estimate`, `ci_point_circle_incidence`, `distance_circles`, `ci_weak_planar_distances`, `ci_planar_occupancy`, `planar_occupancy_sequence`);
- `ci_rich_lines`, `ci_partition(_dim)`, `mot_rich`, `motion_scale_parameters`;
- `uniform_concentration_bridge`, `TrackA.poly_hilbert_lower/at_L/union_lower`;
- `geo_terminal`, `exists_selection_starRank/independentStars/directionCaps`, `exists_retained_graph`, `global_rank_lower`, `global_concentration`, `local_concentration(_ambient)`, `main_contradiction`, `upper_bound`;
- the NonVacuity theorems.

**Scanned mechanically, not read:** the remaining ~205k project lines, all 503 OAI modules (130,917 lines), and HadamardSupport (6,805 lines).

**Not done:** lake, lean, Comparator, nanoda. The kernel replay had not started at 2026-10-11T21:30Z.
