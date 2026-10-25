# Referee report (lean seat): source-level audit of the Lean formalization of Erdős #181

Target: `github.com/cadamcat/hypercube-ramsey-lean4` at HEAD `35fa134` (cloned at `/tmp/oaimath/171/lean/repo`).
Dependencies read in place: `openai/math` @ `adc7f12` (`/tmp/oai-math/lean-build/repo/.lake/packages/OAI`), Mathlib `d13f23b`, and `fixed-point-theorems` @ `770940d` with OAI's patch applied.
Method: I read files, grepped, diffed, and queried the GitHub API. I did not run lake or lean. Two small Python scripts parse import lines, and they are kept outside the repo in `/tmp/oaimath/171/scratch_lean/`. FC sources I fetched are in `/tmp/oaimath/171/refs/fc/`. GitHub compare and log dumps are in `/tmp/oaimath/171/refs/lean_audit/`.

## VERDICT

**CLEAN AS READ.** I found nothing at the source level that would let a kernel-green build of `HypercubeRamsey.Main` mean anything other than "R(Q_n) ≤ C·2^n for an absolute C". That covers the target statement, vacuity, the kernel-bypass surface and the dependency integrity.

This is conditional on our replay reporting exactly `[propext, Classical.choice, Quot.sound]` for `Erdos181.erdos_181`. Our replay is `/tmp/oaimath/171/lean-build/run.sh`.

**COULD NOT CHECK:**
- **(a)** Whether the 530,539 lines of intermediate statements match the paper's lemmas. This does not matter for soundness, because the final theorem has no hypotheses. It does matter for the claim that the formalization "follows the paper".
- **(b)** The author's external records: the 8 Oct independent check, `leanchecker --fresh`, and Comparator plus nanoda. These are self-reported and were run on v1.0.0 `ad206e1`, not on HEAD.
- **(c)** Whether the Mathlib `.olean`s from `lake exe cache get` and the elan toolchain binary are genuine. Our `run.sh` does not run `leanchecker`. See F2.

## Findings

**F1 — none (statement fidelity confirmed).** `Challenge.lean:62-65` and `HypercubeRamsey/Main.lean:14-17` read:
`theorem erdos_181 : ∃ C > (0 : ℝ), ∀ n : ℕ, (diagonalGraphRamsey (hypercube n) : ℝ) ≤ C * 2 ^ n`.
- This is a text-identical copy of FC `FormalConjectures/ErdosProblems/181.lean:41-44` at `9d259649`. Only the line `@[category research open, AMS 5]` (FC:40) is dropped.
- FC current main (`fe7a1ce`) changes only the attribute, to `@[category research solved, AMS 5, formal_proof using lean4 at ".../ad206e1.../Main.lean#L14"]`, and adds an OpenAI reference. The statement is unchanged.
- The definitions block (`Challenge.lean:20-51`, which is byte-identical to `HypercubeRamsey/FormalConjectures.lean:20-51`) is text-identical to FC `Hypercube.lean:31-44` and FC `Ramsey.lean:79-93`, as checked with `diff`.
  - `hypercube`: `Adj u v := #{i | u i ≠ v i} = 1` on `Fin n → Bool`.
  - `graphRamsey`: `sInf { n : ℕ | ∀ (C : SimpleGraph (Fin n)), G.IsContained C ∨ H.IsContained Cᶜ }`.
  - `diagonalGraphRamsey G := graphRamsey G G`.
- The binder `∃ C > 0, ∀ n` puts C outside `∀ n`. C cannot depend on n.
- Neither the `[Fintype α]` argument nor any `Decidable` choice changes values. `graphRamsey`'s body never uses Fintype. The `#{…}` filter uses the genuine `instDecidableEqBool`, and there is no `open Classical` in the file.
- FC pins Mathlib `0df444a` (lean v4.33.1); the project pins `d13f23b` (v4.34.1). I fetched `Mathlib/Combinatorics/SimpleGraph/Copy.lean` at `0df444a`:
  - `structure Copy (A : SimpleGraph α) (B : SimpleGraph β) where toHom : A →g B; injective' : Injective toHom` (line 85).
  - `abbrev IsContained (A) (B) := Nonempty (Copy A B)` (line 239).
  - At `d13f23b` these are at `Copy.lean:84-87` and `:239`, identical apart from variable names.
- `Mathlib.Data.Real.Basic` at `d13f23b` is a `deprecated_module` whose only import is `Mathlib.Basic.Real.Basic`, so the import swap is a no-op.
- Mathlib defines no `SimpleGraph.hypercube`, `graphRamsey` or `diagonalGraphRamsey`, so nothing clashes or shadows.

**F2 — GAP in the verification procedure (ours and theirs), not in the proof.** `scripts/verify.sh:21` runs `lake env lean --trust=0 scripts/Axioms.lean`, and `Axioms.lean:3` is `#print axioms Erdos181.erdos_181`.
- In Lean 4.34.1, `--trust=0` does **not** re-typecheck imported modules. The help text in `src/lean/Lean/Shell.lean:157-158` ("0 means do not trust any macro, and type check all imported modules") is a legacy string. `finalizeImport` (`Environment.lean:2307ff`) performs no kernel check.
- So `verify.sh` adds only an axiom walk over declarations that were already kernel-checked when each module was compiled.
- Mathlib's `.olean`s come from `lake exe cache get` and are never kernel-checked locally on this path.
- The real replay is `scripts/replay.sh:10` (`lake env leanchecker --fresh HypercubeRamsey.Main`). The repo has it and the author says it was run (`docs/verification.md:59`), but our `run.sh` does not run it.
- **Fix:** add `leanchecker --fresh HypercubeRamsey.Main`, and ideally Comparator with `enable_nanoda: true` (`Challenge.json` ships with `"enable_nanoda": false`).
- **Mathematical significance: none**, unless the toolchain or cache has been tampered with.

**F3 — UNCLEAR (provenance of the external checks).**
- `docs/verification.md:51` says commit hashes were "renumbered on 10 October 2026, when local file paths were removed from older commits". The 8 Oct check therefore ran on a commit hash that no longer exists, and only the tree hash `477b9a49` ties it to the current tag. I confirmed tag v1.0.0 = `ad206e1`, tree `477b9a49`.
- Both Comparator runs used "comparator's development stand-in for the `landrun` sandbox" (`verification.md:62,68`), so the build was not isolated from the code being checked.
- Mitigation I verified: `gh api compare ad206e1...35fa134` shows 8 commits. They modify 37 `.lean` files only in module docstrings and comments (I read every hunk: removed `research/blueprint/…` and `runs/lanes/…` paths, and stale "Each `sorry` below…" notes) and add `Audit/NonVacuity.lean`. HEAD's proof content therefore equals v1.0.0's, and our HEAD replay is the authoritative check.

**F4 — COSMETIC (`check_target.py` coverage).**
- `statement` mode (`check_target.py:70-72`, `110-121`) prints with `pp.all` the type of `Erdos181.erdos_181` and the bodies of six names (`NAMES`, line 23-24). It compares the Challenge context against the `import HypercubeRamsey.Main` context.
- Constants used transitively (`Finset.card`, `Finset.filter`, `SimpleGraph.Hom`, `Real.instLE`, `HPow` instances, …) are compared by **name only**. That is sound here because both runs load the same Mathlib build, and a project-level instance swap would show up in the `pp.all` output.
- The check cannot pass with a different statement unless Mathlib itself is altered. The Mathlib checkout is pristine `d13f23b`: `git status --porcelain` is empty, and batteries, aesop, Qq, plausible and proofwidgets are pristine too.
- It compares against the *copy* in `Challenge.lean`, not against FC under FC's own Mathlib pin. My F1 diff closes that gap.
- `verify.sh:14` runs `check_target.py defs` without an FC checkout, so the "verbatim in FC" branch is not exercised by `verify.sh`. I did that comparison by hand.
- Minor: against FC *main*, the `@[category` filter (`check_target.py:39`) would leave the attribute's second line (`formal_proof using …]`) in place and fail. This is irrelevant to the pinned check.

**F5 — COSMETIC (build-time code execution in a dependency).** OAI's `lean/lakefile.lean:263` is a `run_cmd` that executes `git clone/checkout/apply` at Lake configuration time, plus a `post_update` hook at `:279`. Its `unsafe env.evalConstCheck` is the only `unsafe` in the OAI tree. I read it: it only applies the `*-lean4341.patch` files. It has no bearing on the kernel, but it is arbitrary IO run by `lake`.

**F6 — COSMETIC (metaprogramming).**
- `S18/Nodes_sol_split_d18l_sol_d18l_cal_bounds.lean:13` defines `elab "sol_d18l_existing" … => Lean.Meta.mkConstWithFreshMVarLevels (Lean.mkPrivateNameCore …)` to refer to private lemmas in another module. This builds a constant reference that the kernel checks inside the enclosing theorem, so it is benign.
- Four tactic `macro`s in `S10/Split_opus_s10_tagged_sol_s10_d8_locality.lean:11,229,378,607` (with `set_option hygiene false`) are elaborator-only.

**F7 — COSMETIC (labels).**
- The §3 headers mislabel paper lemmas: `S03/ConditionalAvoidance.lean:1` says "# Lemma 3.4: conditional avoidance comparison" (paper: Lemma 3.5) and `S03/ScatteredMoments.lean:1` says "# Lemma 3.5: scattered moments" (paper: Lemma 3.6). The TeX counter is shared (`main.tex:20-24`), so paper 3.4 is a Definition.
- The §3 TeX line citations are offset by about 10–20 lines from `adc7f12`'s TeX: the clock-sampling citation reads "lines 771–1131", but the lemma starts at line 781.
- `S10.ClusterExclusion` imports one S14 module (`S10/Split_opus_s10_tagged_sol_s10_d7c.lean:2`). The import is only for a Jensen lemma (`exp_mean_le`), not Prop 14.1. It is tool reuse, not a §10→§14 logical dependency.

**F8 — a pointer for the §18 paper seat (not a Lean defect).** `HypercubeRamsey/S18/Nodes_sol_s18_1b.lean` is outside Main's import closure. It records a "sketch support gap" in TeX 18:195-204: Lemma 18.1's proof, in the paragraph "Broad prefixes and deletion kernels: Suppose Requirements 1 and 2 hold… Var_U H = O(b_*+e^4)".
- Docstring at :65: "Thus the missing variance premise is automatic on the reference support". The premise needed is that sketch labels lie in the support of the initial prior, because R2's moments (eq:source-26) are only stated there.
- `Obstruction.local_obstruction` (:282) is a finite model in which R1 and the supported R2 moments hold and the retention is 0. Its docstring at :90 says it "models the quantifier gap".
- `gated_initial_of_current_support` (:52) shows the premise does hold, because the gate rules out posterior fallback.
- Reading: an **exposition** gap (an unstated premise that is true) in §18. Severity for the paper: UNCLEAR, leaning COSMETIC/GAP-exposition.
- The other recorded "refutations" are of the formalizers' own blueprint statements, not the paper:
  - `S06/Reduction.lean:12-14`: L6_1a had `n₀ C₀` universally quantified; refuted with `n₀=0, C₀=1/4, n=2, N=1`.
  - `S06/ChunkGeometry.lean:13-16`: L6_1b was claimed for every α; refuted at α=1/2, while the paper takes α small (06:163).
  - Commit `e0e704f4` "Repair the refuted P10.1c and P10.1k statements".
  - `S18/Nodes_sol_s18_2i.lean:76-80`: a "scalar diagnostic for the frozen coefficient".

**F9 — UNCLEAR (production process; it informs how much weight the green build can carry).**
- 1,922 commits ran from `1baabc0e` (2026-10-06T23:31Z, about 1.5 h after `openai/math`'s single "Initial commit" `adc7f12` at 21:58Z) to v1.0.0 `ad206e1` (2026-10-08T07:33Z): about 32 h, peaking at about 164 commits/h.
- There are 584 lane-related messages. By filename tag, 344 files are `_sol_` (GPT-6.1 Sol), 128 `_q_`, 19 `_opus_`, 16 `_p_`.
- There are 39 commits titled "WIP before escalation (may not compile)". The last is `60c14b25` at 04:48Z on 8 Oct; v1.0.0 is "Pin OpenAI's library by git for the release", and no WIP state is the tag.
- `formalization.yaml:108,119` reads `status: "agent-reviewed"` … "No independent human expert has reviewed the formalization."
- Statements were "frozen with a hash of its elaborated type before any proof of it was attempted" (`formalization.yaml`, tool_setup). That only guards against drift; the kernel check is what carries the weight.

## Q2 — vacuity / sInf ∅ = 0
- **The upper-bound direction is the dangerous one,** since an empty set gives `sInf ∅ = 0`. It is closed.
  - OAI `Hypercube.lean:93-95`, `ramsey_set_nonempty`, gives the witness `2^(|V|+|V|)` via `finite_clique_ramsey` (proved at :24-71).
  - `Bridge.lean:19-36` proves `diagonalGraphRamsey (hypercube n) = ramseyNumber (cube n)` as an **equality of sets** (`congr 1; ext M`, both directions; the `→` direction derives `0 < M` from `h ⊥` into `Fin 0`).
  - `hypercube_eq_cube` (`Bridge.lean:15-17`) is `ext u v; rfl` against OAI `cube`'s `hammingDist x y = 1`. Mathlib has `hammingDist x y := #{i | x i ≠ y i}` at `InformationTheory/Hamming.lean:41`.
- `Audit/TargetProbes.lean:26-28` proves `2 ^ n ≤ diagonalGraphRamsey (hypercube n)`, and `:20-22` proves `R(Q_0)=1`.
- `Audit/IndependentRestatement.lean:24-28` defines `Indep : ∃ C, 0 < C ∧ ∀ n, ∃ M, (M:ℝ) ≤ C*2^n ∧ ∀ c : Fin M → Fin M → Bool, (∀ x y, c x y = c y x) → ∃ b f, Injective f ∧ ∀ u v, hammingDist u v = 1 → c (f u) (f v) = b`. It uses no FC or OAI definitions.
  - `fc_iff_indep` (:98) proves the target equivalent to `Indep`.
  - `Indep` asserts that *some* M ≤ C·2^n has the Ramsey property. "Every M ≥ C·2^n" follows by monotonicity, proved as `Audit/NonVacuity.lean:89-113 ramsey_monotone` and `:116-126 colouring_form`.
  - I read `Indep` as exactly Theorem 1.1, with non-induced copies; the diagonal of c is unused because f is injective.
- `IsContained` is the existence of an injective homomorphism, i.e. a non-induced copy (`Copy.lean:84-87,239`). The probe `IndependentRestatement.lean:115-117` confirms copies are non-induced.
- `Fin 0 → Bool` has exactly one element, so `Q_0` is one vertex.

## Q3 — kernel-bypass grep table

Project = `HypercubeRamsey/`, `Audit/`, `Challenge.lean`, `scripts/` (752 `.lean` files). OAI = the whole `lean/` tree at adc7f12. I also grepped the FPT package, Mathlib, batteries, aesop, Qq, plausible and the Lean core sources for `axiom`.

| pattern | project hits | reachable from erdos_181? | OAI tree hits | caught by `#print axioms`? |
|---|---|---|---|---|
| `^axiom` | 0 | — | 1 real: `ComparatorChallenges/HarmonicGrowth.lean:100 axiom mainStatement` (other 3 hits are prose) | yes |
| `sorry` | 3 (2 in comments; `Challenge.lean:65` by design, not imported) | no | 509, all in `ComparatorChallenges/` (challenge stubs) | yes (`sorryAx`) |
| `admit` | 13, all prose | no | — | yes |
| `native_decide` / `ofReduceBool` / `ofReduceNat` | 0 | — | 0 | yes (`Lean.ofReduceBool`) |
| `implemented_by` / `@[extern]` / `@[csimp]` | 0 | — | 0 | n/a: compiler-only; matters only via ofReduceBool |
| `unsafe` | 0 | — | 1 (OAI lakefile, F5) | kernel forbids safe→unsafe refs |
| `opaque` | 2, both in comments (`@[irreducible] def` at `S11/Core/Compatibility_q_s11_compat.lean:7`, `Classical.choose` def at `S05/History_sol_s05_1f_budgets.lean:16`) | yes, harmless | 21 (not imported) | not an axiom; cannot prove False |
| `partial def` | 1 (`Audit/Frontier.lean:25`, read-only `#eval` diagnostic, not imported by Main) | no | 6 | n/a |
| `set_option` | 708: maxHeartbeats 525, synthInstance.maxSize 76, `backward.isDefEq.respectTransparency false` 67, maxRecDepth 18, autoImplicit 12, hygiene false 4, linter 4; **`debug.skipKernelTC`: 0** | — | — | skipKernelTC would NOT be caught; absent; leanchecker would catch it |
| `import Lean` / `open Lean` / `Lean.Elab` / `modifyEnv` / `setEnv` / `addDecl*` / `run_cmd` / `initialize` / `evalConst` | 0 / 1 (`Audit/Frontier.lean:11`) / 0 / 0 / 0 / 0 / 0 / 0 / 0 | — | `import Lean` 240 (not imported) | env manipulation would NOT be caught; absent; leanchecker would catch it |
| `elab` / `macro` | 1 elab + 4 macros (F6) | yes, benign | — | output is kernel-checked |
| `include` | 23 (section-variable inclusion) | yes, harmless | — | n/a |

- **Import closure from Main.** Outside the project, Main reaches only `Mathlib.*`, `OAI.Combinatorics.Ramsey.Hypercube` (287 lines, `import Mathlib` only) and `FixedPointTheorems.kakutani` (the FPT package: 6 files, 3,170 lines).
  - OAI's sole real axiom is in `ComparatorChallenges/`, which is never imported.
  - FPT contains no axiom, sorry, native_decide or metaprogramming (only `axiomOfChoice` term names).
  - Mathlib, batteries and Lean core declare only the standard axioms. The `axiom` hits in `AesopTest`/`BatteriesTest` are test files, not imported.
- **Lakefiles.**
  - Project `lakefile.lean`: `leanOptions := #[⟨autoImplicit, false⟩]`, two `lean_lib`s. No `moreLeanArgs`, `weakLeanArgs`, `precompileModules` or plugins.
  - OAI lakefile: `autoImplicit false` plus the `run_cmd`/`post_update` patch hooks (F5). No odd args.
- **OAI patches** (`lean/patches/*-lean4341.patch`, 23 files). They touch only third-party packages' own files: none target `Mathlib/`, `Batteries/` or Lean core. The only patched package in the proof's closure is `fixed-point-theorems`.
  - Its working-tree diff is byte-identical to `fixed-point-theorems-lean4341.patch` (`git apply --check --reverse` OK).
  - The diff is 7 files, +78/−111: `Set.mem_setOf_eq→Set.mem_ofPred_eq`, `simpa … using!`, `import Mathlib`, docstrings. No logic or axiom changes; `kakutani.lean` itself is untouched.

## Q4 — structure / who proved what
- **(i) Import map.**
  - `Main → Interface → {Framework.PartC → Framework.Props → Framework.OneShot → … → Framework.Basic → OAI.Combinatorics.Ramsey.Hypercube → Mathlib}`.
  - `Interface → Assembly → Bridge → {FormalConjectures (Mathlib only), OAI Hypercube}`.
  - `Interface` also imports `S07.InitialDiscrepancy` (312 modules; reaches S03–S07), `S10.ClusterExclusion` (299; S03,S05,S06,S10,S14), `S11.Exports` (449; S03–S11,S14) and `S18.Exports` (463; S03,S05–S07,S09,S10,S12–S18).
  - The OAI import sites are `Framework/Basic.lean:1`, `Bridge.lean:2`, `S03/Height/Device.lean:2` and `S03/Height/Selection.lean:7`. The FPT import is `S03/Mixtures.lean:4`; Kakutani is used at `Mixtures.lean:400`, `S11/Core/Compatibility.lean:3149` and `S14/Profiles.lean:1285`.
  - The top-level chain (`Interface.lean:119-139`):
    - `linear_bound` is by contradiction: `badSeq_of_not_linear` → `no_badSeq`.
    - `no_badSeq` runs `exists_stabilizedOn (Stage.ofBadSeq S) FamB FamB_countable` (Lemma 3.2; `Framework/OneShot.lean:411`, for an arbitrary countable `Set PatchProp`).
    - It then takes `initial_discrepancy` (Cor 7.2), `remaining_deep_regime` (Cor 11.4) and `eventual_cluster_absence` (Cor 10.2), and feeds them to `partC_main` (§§12–18, `S18/Exports.lean`) → `False`.
  - `FamB` (`Framework/Props.lean:46-51`) is indexed by rational parameters only, and `FamB_countable` is proved. Patch properties are functions of `(n, N, E, A, B)` only (`Framework/Patch.lean:13`), so "intrinsic to supports" holds by construction.
- **(ii) What OAI supplies.** `cube`, `ramseyNumber`, finite clique Ramsey, `elementary_cube_bounds` (2^n ≤ R(Q_n) ≤ 2^(2^n+2^n)), cross-colourings, and `counterexample_sequence_of_not_linear` = Lemma 2.1 (`Hypercube.lean:244-254`).
  - That is the strongest hypercube statement in OAI. There is no Theorem 1.1, no Fox–Sudakov, no Conlon–Fox–Sudakov and no Tikhomirov bound.
  - OAI's `CONTENTS.md` entry #171 has no "([Lean](…))" link, unlike #172, and `lean/docs/` has no 171.md. OpenAI did not formalize Theorem 1.1.
- **(iii) Bridge.** `hypercube n = cube n` is a graph equality. `diagonalGraphRamsey (hypercube n) = ramseyNumber (cube n)` is an equality, proved both ways (`Bridge.lean:15-36`).
- **(iv) Size.**
  - Project: 744 modules / 532,237 lines. Main's closure: 718 modules / 530,539 lines, about 11,757 `theorem`/`lemma` and 4,856 `def`/`structure` lines by regex (approximate).
  - Imported third-party proof code: OAI 287 lines plus FPT 3,170 lines.
  - Per section (modules / lines): S03 58/50k, S04 23/23k, S05 125/57k, S06 56/52k, S07 25/15k, S08 29/31k, S09 24/37k, S10 48/33k, S11 26/25k, S12 16/12k, S13 17/13k, S14 8/19k, S15 48/37k, S16 24/32k, S17 17/19k, S18 124/62k, PartC 12/2.3k, Tools 19/6.9k.
  - 26 project modules (1,698 lines) are outside Main's closure (aggregators, Needs/Exports stubs, `S18/Nodes_sol_s18_1b` from F8, …).
- **Paper mapping.**
  - S03–S11 headers cite paper numbers: Lemmas 3.2–3.10 (mislabels in F7), 4.1, 5.1, 6.1, 7.1, Cor 7.2, 8.1, Cor 8.2, Def 9.1, Prop 9.2, Prop 10.1, Cor 10.2, Prop 11.1, Lemmas 11.2, 11.3, Cor 11.4.
  - S12–S18 cite TeX line ranges and blueprint node IDs (C12.K, C15.F, C18.F) rather than paper numbers. Matching file names against TeX environments places every Part C result:
    - 12.1 → DeepDiscrepancy, 12.2 → CenteredMoment, 12.3 → InteractionTails, 12.4 → ModerateMoment, 12.5 → HomogeneousPeeling, 12.6 → RowTrimming.
    - 13.1–13.4 → ResidualScales / ResidualBounds / Allocation / StableCleaning.
    - 14.1 → Construction, 14.2–14.3 → Profiles.
    - 15.1 → DirectNodes, 15.2–15.4 → ClusterNodes.
    - 16.1 → Geometry, 16.2 → ClusterDiagnostics, 16.3–16.4 → Calibrations/Producers, 16.6–16.7 → Comparisons.
    - 17.1–17.4 → S17 Nodes.
    - 18.1–18.6 → S18 Nodes/Endpoints.
  - Paper results I could **not** locate by an explicit citation: Corollary 12.1 and Lemmas 12.2–12.6, Definition 13.1, Lemma 13.2 and Proposition 13.3 (by name only), Proposition 15.4, Proposition 16.4, Lemma 17.1 and Proposition 17.4. For these I have only a topic-name match, not a statement-level check.

## Q5 — provenance
- `AUTHORS.md:7`: "Formalization and review used Claude Opus 5.5 …, GPT-6 Luna and GPT-6.1 Sol in Codex, and Gemini 3.8 Flash". The author "planned, dispatched and reviewed".
- `CITATION.cff` gives v1.0.0, 2026-10-08. `NOTICE` and `THIRD_PARTY.md` say no OAI source is copied and the only OAI module imported is `OAI.Combinatorics.Ramsey.Hypercube`; I confirmed both.
- Commits `1870de67` and `0d0bebc0` touch only `docs/verification.md`. They record:
  - 8 Oct: c4d-standard-32 VM, `lake build` exit 0 after 1483 s (9673 jobs), `verify.sh` 0, `leanchecker --fresh` 0 after 1334 s, Comparator `ca04cfc` with `lean4export` `076e8e5`: "Lean default kernel accepts the solution".
  - 10–11 Oct: Comparator with nanoda `3a24072`; nanoda accepted and rejected the sorry and altered-numeral controls.
  - Both runs were unsandboxed. I can corroborate neither (F3).
- `af093be6` adds `Audit/NonVacuity.lean` and docs.
- `scripts/freeze_list.py`, `list_decls.py` and `dup_names.py` are lane-management helpers (freeze-list resolver, declaration lister, duplicate-name check). None is used by `verify.sh`.
- Lane names `opus-s05-k1`, `sol-s10-d56`, `q-s05-j610` mean one agent lane per blueprint node per section, merged into main (F9).

## Q6 — other ways "kernel-green" could fail to mean Theorem 1.1
- **Wrong target:** no (F1).
- **Different graph:** no (Q_2 adjacency probes at `TargetProbes.lean:12-14`; `Indep` uses Mathlib `hammingDist`).
- **Trivialised constant:** no. C is existential with `C > 0`; `NonVacuity.constant_ge_one` shows any admissible C ≥ 1.
- **Modified Mathlib:** no. The checkout is pristine `d13f23b` and no patch touches Mathlib or batteries.
- **Residual trust:** the toolchain binary and the cached Mathlib oleans, which only `leanchecker --fresh` or nanoda remove (F2).

## Lines verified vs skimmed

Verified line by line:
- `Challenge.lean`, `FormalConjectures.lean` and `Main.lean`; FC 181/Hypercube/Ramsey at `9d25` and main; Mathlib `Copy.lean` at both pins.
- `Bridge.lean`, `Assembly.lean`, `Interface.lean`, `Framework/Basic.lean`, `Stage.lean`, `Patch.lean`, `Props.lean` and `PartC.lean`; the `OneShot.lean` statements at :37-86 and :411-420.
- OAI `Hypercube.lean` (all 287 lines).
- `Audit/IndependentRestatement.lean`, `TargetProbes.lean`, `NonVacuity.lean`, `FinalChecks.lean` and `Frontier.lean`.
- `scripts/check_target.py`, `check_axioms.py`, `verify.sh`, `replay.sh`, `Axioms.lean` and `apply-oai-patches.sh`.
- Both lakefiles, the FPT patch diff, all v1.0.0→HEAD `.lean` hunks, and the trust/import code in the Lean source.

Skimmed or grepped only:
- The 530k proof lines of S03–S18, PartC and Tools (headers, greps, closure computation).
- The other 22 OAI patches (grepped for kernel-relevant tokens only).
- The commit log (messages, plus 8 commits opened).
- `S18/Nodes_sol_s18_1b.lean` (read about 140 of 304 lines).
