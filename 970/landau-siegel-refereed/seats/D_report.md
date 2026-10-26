# Seat D report — definitions audit + Mathlib-only statement bridge (family 003)
STATUS: DONE except the leanchecker replay (11:31Z). `leanchecker --fresh SeatD003.Bridge` (PID 4148147, started
09:51Z) is still running and the MAIN SEAT is watching it: it killed my rsscap wrapper (PID 4148143) to lift the 2 h cap,
and its watchdog /tmp/oaimath/003/lean/lc_watch.sh (log /tmp/oaimath/003/lean/lc_watch.log) now holds the 14 GB cap.
The lines "leanchecker_fresh 137" in D_work/steps.tsv and "leanchecker fresh rc=137" in D_work/logs/post_build.log
record that wrapper being killed. They are NOT a leanchecker verdict. The verdict will be leanchecker's own output +
the /usr/bin/time "maxrss_kb=… wall_s=…" line in D_work/logs/leanchecker_fresh.log.

## Verdicts per task
1. Textual scan (67-module closure): HOLDS AS READ — no soundness escapes; no macro/syntax/notation/elab/scoped
   declaration exists in the closure at all; 9 global instances, all on OAI-defined algebraic-geometry / MvPolynomial
   objects (8 Prop-valued), none on any type in the statement.
2. Rebuild: DONE — v4.34.1 + Mathlib d13f23b (cache) + all 67 closure modules compiled with plain `lean -o`,
   67/67 rc=0, 0 errors, 0 warnings (no "declaration uses sorry"), 09:17:52Z–09:48:05Z.
3. Mathlib-only bridge + mutants: HOLDS AS READ — `theorem SeatD003.bridge : SeatD003.NoLandauSiegel :=
   OAI.Erdos970.WeightedTorusJets.dirichlet_real_zero_bound` ACCEPTED, axioms [propext, Classical.choice, Quot.sound];
   the ≥-variant accepted; all 6 mutants REJECTED ("Type mismatch" at the term, i.e. by the intended route); the
   statement's elaborated Expr uses only Mathlib/Init constants (46 direct, 5,316 reachable through defs, 0 foreign),
   unchanged when re-audited inside the mixed environment; the 10-23 statement TEXT re-elaborated INSIDE the mixed
   environment gives an Expr identical to the Mathlib-only one (so the 10-23 loophole did not bite either).
   Independent re-check of every imported .olean (`leanchecker --fresh`): RUNNING, main seat watching.
4. Non-vacuity + meaning of LFunction: HOLDS AS READ — kernel-checked, std axioms; plus a kernel-checked proof that the
   "junk-value" reading (naive LSeries instead of LFunction) makes the statement FALSE.
5. Paper <-> Lean map: Lemma 2, Lemma 6, Lemma 7 and §6 follow the paper's proof (same constants: c0=(4·97²)^-1,
   C0=192, H ≥ 86,713,344 = 12·C0/c0, threshold 32, N ≥ 18,818 = 2·97²). Lemma 3 / Corollary 4 do NOT: the Lean
   proves Corollary 4 in its dual multiplicity-estimate form (the paper's Remark 5) by a long commutative-algebra /
   scheme-theoretic zero estimate (local lengths at torus primes, cotangent dimension, invariant derivations,
   logarithmic forms, generic normalization, Hilbert-polynomial degree bound). The paper's nearest-point /
   supporting-face / Lagrange proof of Lemma 3 is formalized nowhere in the 105-file tree. HadamardSupport is a proof
   (6,805 lines, Mathlib-only imports, no axiom/sorry), not an assumption.

## Task 1 — textual scan (D_work/scan.txt; script D_work/scan.py)
Comment-stripped (nested /- -/, doc comments, --, string-literal aware) scan of all 67 closure sources
(66 under /tmp/oaimath/013/repo/lean/OAI/NumberTheory/Jacobsthal/Siegel/ + PrimeNumberTheoremAnd/Erdos970/HadamardSupport.lean).
Closure is import-closed: every import of every closure file is either `Mathlib` or another closure module, in
file order (checked by script; no order violations).
- ZERO hits: axiom, sorry, admit, opaque, implemented_by, extern, unsafe, native_decide, ofReduceBool/reduceBool,
  `decide +kernel`/kernel:=true, debug.skipKernelTC, set_option (none at all), macro, macro_rules, syntax, elab,
  elab_rules, infix/infixl/infixr/prefix/postfix, unif_hint, default_instance, run_cmd/run_elab/run_meta,
  initialize/builtin_initialize, `import Lean`, export, open private, binop%/unop%, csimp, simproc, partial def,
  class (none), structure (none), mutual, instance priority.
- notation: 42, all `local notation` (e.g. "ZeroIndices", "DivisorIndices", "𝒜") — cannot leak.
- scoped: 276 hits, ALL are `open scoped …`; no `scoped` declaration exists, so `open scoped _root_.Erdos970` opens nothing.
- instances: 71 `attribute [local instance]` (file-local), 1 `local instance`, 1 `attribute [-instance] … in`
  (command-local), and 9 GLOBAL instances:
  DegreeMap:143 `degreePiece_finite : Module.Finite K (degreePiece I n)`;
  GenericNormalization:75/79/93 `IsIntegral (genericNormalization Y)`, `IsDominant (genericNormalizationMap Y)`,
  `IsIso (dominantFunctionFieldHom f)`; :194 `affineFunctionFieldAlgebra : Algebra A (Spec (CommRingCat.of A)).functionField`
  (data, defined AS Mathlib's own instance `AlgebraicGeometry.instAlgebraCarrierFunctionFieldSpec`); :447/:450
  `IsIntegral f.image`, `f.image.IsSeparated`; ParameterIdeal:52 `(parameterIdeal k).IsPrime`; DerivationJet:354
  `Module.Finite K (MvPolynomial σ K ⧸ rectangularIdeal k)`.
  None can fire on ℕ, ℝ, ℂ, ZMod q, MulChar (ZMod q) ℂ, or any class used in the statement (LE/LT/Mul/Sub/OfNat/NatCast/
  FunLike/NeZero/CommMonoidWithZero …). Moot anyway after task 3 (statement elaborated with none of this present).
- Other counts (not escapes): 46 `decide`, 16 `private`, 11 abbrev/@[reducible], 1 direct `Classical.choice`.

## Task 4 — non-vacuity and the meaning of LFunction (bridge/SeatD003/NonVacuity.lean, log logs/NonVacuity.log)
Mathlib-only, compiled to bridge/out/SeatD003/NonVacuity.olean, all four theorems `[propext, Classical.choice, Quot.sound]`:
- `hypotheses_satisfiable`: ∃ q, NeZero q, χ : DirichletCharacter ℂ q with 3 ≤ q ∧ IsPrimitive ∧ χ ≠ 1 ∧ ∀ a, (χ a).im = 0.
  Witness q=3, χ = (quadraticChar (ZMod 3)).ringHomComp (Int.castRingHom ℂ); χ(2) = −1 ⇒ χ ≠ 1; conductor | 3 and ≠ 1 ⇒
  conductor = 3.
- control `one_mod3_not_primitive`: the trivial character mod 3 is NOT primitive (IsPrimitive is not vacuous-true).
- `LFunction_unique`: for χ ≠ 1, ANY entire f with f(s) = LSeries (χ ·) s on Re s > 1 equals χ.LFunction everywhere
  (identity theorem on ℂ, from Mathlib's `LFunction_eq_LSeries` + `differentiable_LFunction`). So χ.LFunction β for
  β ∈ (0,1) is the analytic continuation of Σ χ(n) n^-s — no junk value. Mathlib types quoted (#check):
  `DirichletCharacter.LFunction_eq_LSeries : ∀ {N} [NeZero N] (χ : DirichletCharacter ℂ N) {s : ℂ}, 1 < s.re →
   LFunction χ s = LSeries (fun x => χ ↑x) s`;
  `DirichletCharacter.differentiable_LFunction : ∀ {N} [NeZero N] {χ}, χ ≠ 1 → Differentiable ℂ (LFunction χ)`;
  also `differentiableAt_LFunction`, `LFunction_apply_one_ne_zero : χ ≠ 1 → LFunction χ 1 ≠ 0`.
  `#print`: `LFunction χ s := ZMod.LFunction (⇑χ) s`; `IsPrimitive χ := χ.conductor = n`;
  `DirichletCharacter R n := MulChar (ZMod n) R` (reducible).
- `not_Mut_LSeries`: the mutant reading "zero" as `LSeries (fun n => χ n) β = 0` is FALSE (LSeries is 0 off its
  half-plane of absolute convergence, so every β ∈ (0,1) would count; refuted with q=3, β = 1 − min(1/2, c/(2 log 3))).
  This is the negative control showing that the choice LFunction vs LSeries is load-bearing and that the bridge uses
  the right one.

## Task 5 — paper ↔ Lean map (sources /tmp/oaimath/013/repo/lean/OAI/NumberTheory/Jacobsthal/Siegel/)
- Lemma 2 (p.2, (2.1)/(2.2)): SumLogPrimeFactors.`source_analytic_lemma` states (2.1) and (2.2) in the paper's form
  (C log q + C·δ(log X)²/log q; primes H<p, p∤2q, χ(p)=−1), strengthened to C ≥ log 4 in
  SumLogDivFilterDvdTwoMul.`source_good_prime_mass_with_chebyshev_constant`. Proof follows the paper: completed L-function
  (ConductorCompletedL), Hadamard product / divisor indexing (HadamardSupport `divisorZeroIndex₀`, Weierstrass factors),
  log-derivative identity (RealLogDerivConductorCompletedLDivisorTsum.`real_logDeriv_conductorCompletedL_eq_divisor_tsum`,
  `real_zero_le_conductorCompletedL_logDeriv` = keep only the β term), combined von Mangoldt series (E.lean),
  Mertens/Chebyshev and Σ_{p|q} log p/p (SumLogPrimeFactors). FOLLOWS PAPER.
- Lemma 3 + Corollary 4 (pp.3–5): Corollary 4's conclusion = InvariantJetLinearMap.`actual_biquadratic_rectangle_span`
  (span of rows with α_j ≤ 32·H^{2/3}N^{4/3}, 32·H^{-1/3}N^{4/3}), proved from
  TorusQuotientDimensionPosCotangentFinrankThree.`uniform_rectangular_multiplicity`: for c ∈ ℂ⁴ ℚ-independent and any
  basis v of ker(c·), a polynomial F of degree ≤ N−1 in each variable whose invariant jets (D_v^a F)(1,1,1,1) vanish on
  the rectangle is 0. Proof: by contradiction, a shared torus component q (`torus_rectangle_shared_component_data`),
  lower bound on the local length (`source_local_torus_rectangle_graded_length_gt`, via derivations / cotangent
  dimension / logarithmic forms `torus_prime_residue_logarithmicForm_ne_zero`, counting (4N)^k < Π(⌊T_j/4⌋+1)) vs upper
  bound `rectangleJetIdeal_length_le` (projective degree via Hilbert series, LocalLengthMulProjectiveClosureDegree,
  TorusRectangleJetIdealParametersProjectiveDegreeBound). 38 of the 66 closure files form the import cone of
  TorusQuotientDimensionPosCotangentFinrankThree and 37 of them are used ONLY there (ConeMap … TorusEvalOne,
  GenericNormalization, DominantFunctionFieldHom, ParameterIdeal, LogarithmicForm, FiniteTypeFieldModelEquiv, HilbertSeries, …). DIFFERENT PROOF (a Philippon-style multiplicity estimate, i.e. the Remark 5 dual); no nearest-point,
  supporting face, convex hull or Lagrange interpolation appears anywhere in the 105 files (grep: 0 hits).
  Lemma 3 as stated (surjectivity of evaluation on 𝒫_t with the (4N−3)^4 budget) is not itself a Lean statement.
- Lemma 6 (p.5–6, (4.4)): GlobalRectanglePivotBounds.`global_source_rectangle_pivot_bounds` (+ GreedyPivots,
  WeightedJetIndices, GreedyPivotsWeightLowSpan): S₁ ≥ M·H^{2/3}·U/(4·97²), S₂ ≤ 192·M·H^{-1/3}·U, for N ≥ 18818, H ≤ N.
  Same constants, same greedy weighted pivot selection. FOLLOWS PAPER.
- Lemma 7 (p.7, (5.5)) and (5.2)/(5.6)/(5.7): CharacterGlobalGreedyDeterminantFullLocalBounds /
  BiquadraticArithmeticFull (`exists_lower_triangular_replacement`, `replacement_row_expansion`,
  `weighted_interpolation_determinant_dvd_of_frobenius_choice`, `galois_derivative_determinant_mem_prime_power`) with
  Frobenius from SqrtPairFrobeniusDirections.`sqrtPair_frobenius_directions` (arithmetic Frobenius in 𝓞 of
  CyclotomicField(8q), restricted to B = ℚ(a,b)). Statement: Δ ∈ (p)^{Σ⌊α₁/p⌋} in 𝓞 B for p prime, H<p, p∤2q, χ(p)=−1.
  FOLLOWS PAPER (minor: works in the full ring of integers 𝓞 B rather than ℤ[a,b], Frobenius via Mathlib arithFrobAt
  rather than Euler's criterion). Archimedean bound (5.2) is the `harch` field, same shape.
- §6 (pp.8–9, (6.1)/(6.2)): DirichletRealZeroBound (by_contra), SumLogPrimeFactors.`exists_contrary_sequence`
  (q→∞ via `exists_gap_fixed_modulus` / `exists_gap_bounded_moduli`, as in the paper), NormalizedMasterBound
  (= (6.1)), RealZeroUniformMasterBound (H ≥ 86713344, q ≠ 8 i.e. Q(√d) ≠ Q(√2)), NotEventuallyMaster.
  `exists_fixed_parameters_not_eventually_uniform_bound` (13/16 + 1/16 < 1, γ chosen). FOLLOWS PAPER.
- HadamardSupport: a PROOF. 6,805 lines, `import Mathlib` only, 207 theorems/lemmas, zero axiom/sorry/admit/opaque;
  it is an OpenAI addition (untracked in PNT+ @c39a751, delivered by lean/patches/PrimeNumberTheoremAnd-lean4341.patch),
  compiled here from source and kernel-checked with the rest.
- Provenance: /tmp/oaimath/013/repo is openai/math @1581d4cbdd69 with a clean worktree (0 changes under
  lean/OAI/NumberTheory/Jacobsthal/Siegel); HadamardSupport.lean on disk is byte-identical to the new file (6,805 lines)
  added by the repo's lean/patches/PrimeNumberTheoremAnd-lean4341.patch. sha256: DirichletRealZeroBound.lean 9759549f…,
  HadamardSupport.lean a0f61289….
- The 39 Siegel files OUTSIDE the closure (list: D_work/outside_closure.txt): all hang off `Main.lean` (an aggregator
  importing 19 of them); unused alternatives / transport lemmas / restatements (e.g. Divisibility, PivotBounds,
  BiquadraticBasisGroupTransport, FractionEulerDerivation, TorusJetZeroSchemeInclusion, CompletedLAnalyticOrderNeTop,
  NormLogDerivLFunctionNegLogDerivZeta, SumCharacterPeriodZero, and `DirichletRealZeroBoundProof` which just re-exports
  the theorem under the comparator name). None is a nearest-point proof of Lemma 3. Not needed for the theorem.

## Task 2 — rebuild (logs under D_work/logs/)
- Guards observed: df / ≥ 30 GB before toolchain install (55 G) and cache get (51 G); every lean launch gated on
  MemAvailable ≥ 28 GB (8 for it + 20) and ran under rsscap.sh (12 GB RSS / 40 min), LEAN_NUM_THREADS=2, ≤2 lean at
  once, nice 19. Peak RSS 7.40 GB (HadamardSupport). No foreign process touched; kills only by own PID (none needed).
  Deviation: the python driver (drive_closure.py) was NOT wrapped in `ulimit -v` because the limit is inherited by its
  lean children and breaks olean mmaps; it is a thin scheduler.
- Toolchain: /tmp/oaimath/003/lean/home/.elan, `Lean 4.34.1 … commit 5045d0056413`. Mathlib: /tmp/erdos0300/lean/mathlib4
  at d13f23b723b8 (git status clean except LAKE_DELETED.txt), `lake exe cache get` 8,908 files, exit 0 at 09:16:31Z.
- Closure: 67/67 modules, closure-file order, `lean -DautoImplicit=false … -o`, results in D_work/modules.tsv
  (rc, errors, warnings, maxrss, olean sha256 prefix), per-module output D_work/logs/mods/<module>.txt.
- Sizes to delete after banking: /tmp/oaimath/003/lean/out 109M (OAI oleans), /tmp/oaimath/003/lean/home 3.4G
  (toolchain + 449M cache), /tmp/erdos0300/lean/mathlib4/.lake 7.1G, D_work 1.8M.

## Task 3 — the bridge (D_work/bridge/)
Order of operations: SeatD003/NoLSStatement.lean compiled at 09:16:58–09:17:27Z with LEAN_PATH = seat-D out dir +
Mathlib only (env_mathlib_only.sh) — before the OAI build even started (09:17:52Z) and with the OAI out dir never on
that path. olean sha256 b438663b990a4927… (source 1764c937…), identical after the bridge ran.
Statement (written from the TeX of Theorem 1, p.1, eq. (1.1)):
  `def NoLandauSiegel : Prop := ∃ c : ℝ, 0 < c ∧ ∀ (q : ℕ) [NeZero q], 3 ≤ q → ∀ χ : DirichletCharacter ℂ q,
   χ.IsPrimitive → χ ≠ 1 → (∀ a : ZMod q, (χ a).im = 0) → ∀ β : ℝ, (0 < β ∧ β < 1 ∧ χ.LFunction (β : ℂ) = 0) →
   c ≤ (1 - β) * Real.log q`
Clause map: "absolute constant c>0" = ∃ c, 0 < c, quantified before q, χ, β; "primitive … of conductor q" = χ mod q
with IsPrimitive (Mathlib: `χ.conductor = q`, conductor = least level through which χ factors), so q is the conductor;
"nonprincipal" = χ ≠ 1 (redundant for primitive χ with q ≥ 3, kept as in the paper); "real" = every value χ(a),
a ∈ ZMod q, has imaginary part 0; "real zero β ∈ (0,1)" = 0 < β < 1 ∧ LFunction χ β = 0 (analytic continuation, Task 4);
"q ≥ 3" = 3 ≤ q; "log" = Real.log (natural), of the cast (q : ℝ); "(1−β) log q ≥ c" = c ≤ (1−β)·log q.
Results:
- StatementAudit.lean (Mathlib-only; logs/StatementAudit.log, logs/StatementAudit.consts.txt): pp.all print of the
  value; 46 constants used directly, every one declared in Init.* or Mathlib.* (e.g. DirichletCharacter,
  DirichletCharacter.IsPrimitive, DirichletCharacter.LFunction [Mathlib.NumberTheory.LSeries.DirichletContinuation],
  MulChar.hasOne, MulChar.instFunLike, ZMod, ZMod.commRing, Complex.im, Complex.ofReal, Real.log
  [Mathlib.Analysis.SpecialFunctions.Log.Basic], Nat.cast/Real.instNatCast, Real.instLE/instLT/instMul/instSub,
  NeZero/Nat.instMulZeroClass, Complex.instField …); transitive closure through types + def bodies + constructors:
  5,316 constants = Mathlib 4,490 + Init 819 + Batteries 6 + the def itself; AUDIT CLEAN.
- Bridge.lean (logs/Bridge.log, olean bridge/out/SeatD003/Bridge.olean): `theorem SeatD003.bridge :
  SeatD003.NoLandauSiegel := OAI.Erdos970.WeightedTorusJets.dirichlet_real_zero_bound` ACCEPTED (rc 0);
  `#print axioms SeatD003.bridge` = [propext, Classical.choice, Quot.sound] (same for bridge_ge and for OpenAI's theorem).
  In the mixed environment: the statement re-audited CLEAN; `#seatD_same` reports the brief's statement text
  elaborates to an Expr IDENTICAL to the Mathlib-only stored value; `#seatD_deps` (types + values incl. proofs,
  expanding only OAI/PNT constants): 2,267 foreign constants in 66 modules = 65 Siegel modules + HadamardSupport
  (250 constants, e.g. Erdos970.Complex.CartanBound.*, Hadamard.*); the imported AuxiliarySqrtPairCharacterField
  contributes no constant; no `axiom` declaration reached. Run 1 (logs/Bridge.run1_with_type_audit.log) additionally
  audited the TYPE of OpenAI's theorem: its only non-Mathlib constant is the theorem itself (exit 1 by design; line
  removed so the file could produce an olean).
- Mutants (each its own file, logs/BridgeMut_<m>.log), all rc 1 with `error: Type mismatch` at the term:
  (i) beta_le_two (β < 1 → β ≤ 2); (ii) no_log (c ≤ 1 − β); (iii) drop_ne_one; (iv) re_not_im ((χ a).re = 0);
  (v) LSeries (zero of the naive LSeries — kernel-proved FALSE in NonVacuity.lean); (vi) drop_primitive.
  Note: (i), (iii), (vi) are mathematically implied by / equivalent to the theorem — their rejection shows the check is
  definitional (no unfolding can make different props equal), not that the variants are false; (ii) and (v) are the
  semantic discriminators ((v) is provably false, (ii) is open/far stronger).
- Controls on my own instruments: `#seatD_same` positive (SameControlPos: same text, Mathlib-only → SAME, rc 0) and
  negative (SameControlNeg: β < 1 → β ≤ 1 → DIFFERENT, rc 1); `#seatD_audit` negative (AuditNegControl: an OAI
  definition, rectangleThreshold → FOREIGN (6), rc 1).
- Olean trust (beyond the brief): `lean` does NOT re-check imported .oleans. Demonstrated in D_work/lcctl/: an olean
  carrying `bad : False := True.intro` (added with the kernel switched off) imported by a second file proves False with
  "does not depend on any axioms" (LcUseBad.log, rc 0). So neither the 10-23 check nor `#print axioms` alone excludes a
  tampered olean. Here: (a) every OAI olean was produced by our own `lean -o` from source, and the scan shows no
  set_option / run_cmd / elab / initialize / `import Lean` that could switch the kernel off, so each OAI declaration was
  kernel-checked at compile time; (b) Mathlib's oleans came from the cache and are covered only by (c)
  `leanchecker --fresh SeatD003.Bridge` (replays every declaration of the whole import closure in a fresh kernel).
  leanchecker controls: LcBad (ill-typed olean) → "leanchecker found a problem", rc 1; LcGood → rc 0; missing module →
  rc 1 (logs/leanchecker_missing_control.log). Fresh run: logs/leanchecker_fresh.log — RUNNING at hand-off (1 h 39 min wall / 1 h 36 min CPU at 11:30Z, RSS ~7.3 GB, no
  output yet). It is slower than earlier families' ~58 min, presumably because the box is at load ~14. Main seat reads the result.

## Objections (scope: definitions, statement, paper↔Lean correspondence)
- None of severity FATAL/GAP/FIXABLE against the statement: the Lean theorem says Theorem 1 (p.1, (1.1)) exactly, in
  Mathlib's own definitions, and nothing of OpenAI's could have changed that meaning (Task 3).
- COVERAGE (not an objection to the paper's mathematics; Rule 6): §1 p.2 says "The proof uses a dimension count, a
  nearest-point argument for an integer polytope, and Lagrange interpolation on a supporting face", and §3's proof of
  Lemma 3 (pp.3–5, (3.3)–(3.6), Figure 1) is that argument. The Lean does not formalize it: Corollary 4's conclusion is
  obtained by an independent multiplicity estimate (Task 5). Consequences: (a) the kernel-checked theorem does not
  depend on the correctness of the paper's §3 proof; (b) conversely the formalization provides NO evidence for that
  proof — a referee who finds a hole in Lemma 3's nearest-point argument has found a hole in the paper, not in the
  theorem. The paper makes no claim of formalization (grep "Lean|formaliz|verified": 0 hits).
- EXPOSITION: "nonprincipal" in Theorem 1 is redundant given "primitive of conductor q ≥ 3" (in Mathlib:
  conductor 1 ⇔ χ = 1). Harmless; kept in the bridge.

## What I checked and how (with controls)
- Scan: comment/string-aware stripper, 40+ patterns, every instance/notation hit classified (scan.txt). Control: the
  scan does find the 83 instance lines / 42 local notations / 276 `open scoped`, i.e. it is not blind.
- Statement provenance: compiled Mathlib-only before any OAI olean existed; constant-provenance audit (positive:
  CLEAN on the statement; negative: FOREIGN on an OAI def); text-identity check (positive SAME / negative DIFFERENT
  in the Mathlib-only env, then SAME in the mixed env).
- Kernel acceptance of OpenAI's term against the Mathlib-only Prop; 6 mutants rejected by "Type mismatch"; the
  ≥-variant accepted (the check is definitional, not textual).
- Non-vacuity and meaning (Task 4), all kernel-checked: satisfiable hypotheses; trivial character not primitive;
  uniqueness of continuation pinning LFunction; the LSeries reading proved false.
- Olean trust: leanchecker controls (ill-typed olean rejected, good accepted, missing module rc 1) and the fresh
  replay of the whole closure (still running at hand-off, main seat watching).
- Paper↔Lean map: read the Lean statements of the load-bearing theorems (listed in Task 5) against the TeX; import
  cone analysis by script; grep for any nearest-point/convex-hull/Lagrange formalization (0 hits in 105 files).

## What I could NOT check
- Lean's kernel itself and Mathlib's definitions beyond the four pins above: no independent kernel (lean4lean,
  nanoda) is installed on this box; leanchecker uses the same C++ kernel, so it removes olean-tampering and
  elaborator-level risk, not kernel bugs.
- Whether the paper's own §3 nearest-point proof of Lemma 3 is correct (not formalized; outside this seat).
- Whether the Lean's multiplicity estimate is the "right" mathematics: irrelevant to truth once kernel-checked, and
  not read line by line (≈15k lines).
- The 024 copy (/tmp/oaimath/024/repo/lean/OAI/NumberTheory/SiegelZeros/) was not built; only its comparator
  statement was read (it states the same proposition, curried, plus the uncurried `dirichletRealZeroBound_proof` form).

## Where a hole is most likely to hide in this scope, and whether it does
In a statement-faithfulness audit the classic holes are: a junk value standing in for the analytic object
(LSeries is 0 on 0<β<1 — the mutant that uses it is provably false, and the statement uses LFunction, pinned to the
continuation by Mathlib's LFunction_eq_LSeries + differentiable_LFunction); "modulus" passed off as "conductor"
(IsPrimitive is literally conductor = q); an instance/notation/coercion from the author's code silently re-meaning
`≤`, `*`, `log`, casts or `.im` (closed by elaborating the statement with none of their code present, and by the
SAME-Expr check in the mixed environment — the 10-23 text was never contaminated); and an imported .olean that was
never kernel-checked (shown to be a real gap for plain `lean`/`#print axioms`; closed for OAI's modules by compiling
them ourselves from sources that contain no way to switch the kernel off, and for everything by leanchecker --fresh,
result pending with the main seat). I found no hole. What remains is trust in the Lean kernel and in Mathlib. The consequence should be
stated plainly: if the leanchecker replay passes, a statement that is word-for-word Theorem 1 has a kernel-checked
proof with standard axioms, and that proof does not pass through the paper's §3 argument.
