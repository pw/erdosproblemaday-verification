# Erdős #174 — OpenAI family 172 "A classification of finite Euclidean Ramsey configurations" (23 Sep 2026; public 6 Oct), refereed 2026-10-21

Claim (Theorem 1.1): a finite A = {a_1,…,a_s} ⊂ ℝ^d, s ≥ 2, affine span ℝ^d, is Euclidean Ramsey (arbitrary colourings, congruent
copies at scale one) iff there is P ∈ Mat_{d+1}(F ⊗_ℚ F), F = ℚ(coordinates), with (p_i⊗1)ᵀP(1⊗p_i) = 0 ∀i and m_F(P_αβ) = δ_αβ on the
spatial block (p_i = (1, a_i)). Consequences §7: Cor 7.1–7.5, Props 7.3, 7.6, 7.7 (see the entry). The theorem, proofs and Lean are
OpenAI's. Graham's conjecture was refuted first by Pálvölgyi (arXiv 2609.23327, 20 Sep). The algebraic-coordinates corollary was first
stated in four AI-generated repositories (7–14 Oct; seats/W_report.md §3). Ours: the replay + controls, two bridges to Formal
Conjectures + controls, the readings, the decision procedure and what it found.
Entry: https://erdosproblemaday.com/day/174-openai-euclidean-ramsey-classification-refereed

Paper: `paper/SOURCE.txt` (sha256 of the PDF + TeX we read; openai/math @ 1581d4c; not redistributed). PRINTED sections: 1 problem ·
2 tensors/necessity · 3 lattice identity · 4 two scales · 5 paths → copies (5.1–5.3) · 6 permutations → endpoints (6.1–6.3) · 7 examples.

## replay/ — kernel replay of OpenAI's Lean (openai/math @ 1581d4c lean/, Lean v4.34.1, Mathlib d13f23b7)
- Closure `all_order.txt`: 65 modules (47 OAI/Combinatorics/EuclideanRamsey + 18 OAI/Combinatorics/SphericalRamsey), 9,589 lines, roots =
  the seven comparator solution modules. External: Mathlib only. `ESTIMATE.md` = the estimate written before spending CPU.
- `drive.py` (lake-free, DAG-parallel, W=4, memory-gated; copied from the #304 driver): 65/65, 0 errors, 21:05:07Z → 21:11:14Z
  (6 min 7 s wall), Σ per-module wall 608 s, peak RSS 6.70 GiB. `modules.tsv`, `driver.log`, per-module logs `logs/module_logs.tar.xz`.
  Mathlib oleans from `lake exe cache get` (`cacheget.sh`, `cacheget.out`).
- `post.sh`: the seven comparator modules compiled; probes `probe/Cmp_*.lean` (import the challenge) and `probe/Ax_*.lean` (import the
  solution, `--trust=0`), all printing `pp.all` blocks; `probes.json` lists the theorem + definition names per comparator.
  `statement_match.py` → `statement_match.txt`: ALL_MATCH_STD_SORRYSEEN — EuclideanRamsey 11/11, GrahamSpherical 13/13, Circle 4/4,
  Nine 5/5, Quadratic 8/8, Spherical 4/4, Transitive 4/4 (49 blocks); solution theorems on exactly [propext, Classical.choice,
  Quot.sound]; sorryAx seen on every challenge theorem. `Neg.lean`: planted sorry → sorryAx (`logs/neg.log`).
- Matcher mutation test `mutate_matcher.sh` → `mut/MUTATIONS.txt`: unmodified 0; def token, theorem numeral (5→6), Nine count (9→8),
  extra axiom, comparator without sorryAx → 1; missing block, missing log → 2. A mutation that does not change its input is REFUSED
  (the first version silently tested three unchanged inputs; caught, fixed, re-run).
- `leanchecker.sh`: `leanchecker --fresh LcAll` (LcAll imports Bridge174 + the seven solution modules ⇒ OpenAI's 65-module closure +
  Mathlib + our bridge), then a missing-module control. `leanchecker_fc.sh`: `leanchecker --fresh Bridge174Main` (imports Bridge174FC + OpenAI's Main; it replaced a Bridge174FC-only run that the seat killed after ~15 min as a strict subset — row `leanchecker_fresh_fc_REPLACED`). Results: `steps.tsv`
  RESULT Bridge174Main: rc 0 after 3,556 s, peak RSS 8.2 GiB (`logs/leanchecker_fresh_fc.log`).
  RESULT LcAll: rc 0 after 3,603 s, peak RSS 8.2 GiB (`logs/leanchecker_fresh.log`); missing-module control rc 1 (`logs/leanchecker_missing.log`).
  rows `leanchecker_fresh`, `leanchecker_missing_control`, `leanchecker_fresh_fc`; logs in `logs/`. Both landed after the first commit; results below.
- `steps.tsv` = every step's rc and seconds.

## bridge/ — ours
- `Bridge174.lean` (imports OpenAI's Quadratic + Spherical): `algebraic_spherical_fieldCriterion` (algebraic coordinates + sphere ⇒
  FieldCriterion: F finite-dimensional via `IntermediateField.finiteDimensional_adjoin`, formally unramified via
  `Algebra.FormallyUnramified.of_isSeparable`, Kähler ideal = (e) with e idempotent via `Ideal.isIdempotentElem_iff_of_fg` +
  `Ideal.cotangent_subsingleton_iff`, P = (1−e)·(h⊗1) with h from OpenAI's `sphere_field_quadratic`), `algebraic_spherical_ramsey`,
  `algebraic_ramsey_iff_cospherical`. `AxBridge.log`: standard axioms. Mutants (must fail; logs rc 1): `BridgeMutNoAlg` (drop the
  algebraic hypothesis), `BridgeMutNeg` (conclude ¬Ramsey), `BridgeMutNoSphere` (drop sphericity). (All mutants re-run with their real namespaces after B's S9: a first version renamed
  namespaces, which added an incidental `end` error; every log now shows only the genuine error at the mutated step.) NOT a first: the same statement is
  in JD-Jones-ASES/six-concyclic-lean (7 Oct, same theorem name), Rogerhu12/openai-math-extensions, atimics/math2, wstrinz/spherical-ramsey.
- `Bridge174FC.lean`: FC's `Erdos174.IsRamsey` and the statements of `erdos_174.variants.graham` (inside ¬(∀ …)) and
  `erdos_174.variants.spherical` VERBATIM from `FC_174.lean` (google-deepmind/formal-conjectures @ 2a315101, added 2026-10-20 in PR
  #7469; sha256 in `FC_SHA.txt`); `verbatim_check.py` (whitespace-normalised; `verbatim.log` rc 0, `--mutate` rc 1). `graham_false`
  from `OAI.GrahamSpherical.full_main`; `erdos_174.variants.spherical` from `OAI.EuclideanRamsey.ramsey_cospherical`;
  `dim_pos_of_congruent` (a copy of two distinct points cannot live in ℝ⁰). `AxBridgeFC.log`: standard axioms. Mutants (rc 1):
  `BridgeFCMutSmall` (refutation restricted to ≤ 5 points), `BridgeFCMutSub` (conclusion strengthened to Subsingleton),
  `BridgeFCMutDef` (IsRamsey changed).
- `Bridge174Main.lean` (imports Bridge174FC + OpenAI's Main): `erdos_174_criterion (n) : {A | IsRamsey A} = criterionAnswer n` — FC's
  left-hand side verbatim (`verbatim_check.py` item 3), FC's `answer := sorry` replaced by our explicit `criterionAnswer` (finite A that are
  subsingletons or congruent, by an explicit labelling, to a full-span configuration satisfying OpenAI's FieldCriterion), from OpenAI's
  `classification_nonempty`; `isRamsey_iff_oai` (FC's IsRamsey ⇔ OpenAI's Ramsey of any enumeration, two distinct points);
  `witness_not_mem_criterionAnswer` (non-vacuity: the twelve points are not in it). `AxBridgeMain.log`: standard axioms. Mutants (rc 1,
  failing inside the proof at the lines that use what was removed — a first version renamed the namespace and failed for the wrong
  reason, unknown `IsRamsey`; caught and re-run): `BridgeMainMutNoCrit` (criterion dropped), `BridgeMainMutNoSub` (subsingletons dropped).
  LRW's iff is not bridged: its "only if" needs LRW 2011 Cor 2, formalised nowhere we found.

## compute/ — ours (exact; label (d))
- `criterion.py`: decision procedure for F = ℚ(τ). B ⊂ ℚ(x,y); kernel of the evaluation map over ℚ(x,y) (sympy DomainMatrix);
  saturation at the prime (x − y) of the DVR B_p = ℚ[x,y]_(x−y); test I ∈ span of spatial blocks of the reduced basis at y = x.
  Exact both ways: a saturated basis spans K_p, so FAILS ⇒ no certificate; HOLDS lifts back to B by clearing a unit denominator.
  `criterion_controls.log`: three squares FAILS (kernel 0); two squares (transitive) HOLDS; kite HOLDS; five circle points HOLDS;
  collinear {0,1,τ} FAILS; seven rational circle points HOLDS.
- `rank_check.py` → `rank_check.log` (no sympy, Fractions): three squares rank 9/9 at five random rational (x0,y0); two squares rank 8;
  diagonal rank 4–5 (control); all 220 nine-point subsets rank 9 at (3/7, −11/5).
- `census.py k` → `census_k{6,7,8}.log`: orbits under the 8 symmetries of the twelve points (rotation by 90°, reflection y ↦ −y).
  k=6: 128/128 HOLDS; k=7: 104/104 HOLDS; k=8: 67 HOLDS, 5 FAILS.
- Spot check (NOT a second proof — seat B's M3): exact Fractions, no sympy, no saturation loop, at fixed rational τ (2/7, −5/3; 11/13 in
  minor_check8), taking the limit y → x there; agrees with the symbolic procedure for all but finitely many τ, and both rest on the same
  DVR reduction. Scripts: `minor_check.py` (kernel dim 1: cofactor vector, exact interpolation in h = y − x,
  least power stripped) → `minor_check8.log` (the 5 failing 8-sets: antisymmetric spatial limit at three x0) and `crosscheck8.log`
  (72/72 agree); `plucker_check.py` (any kernel dim: Plücker coordinates = complementary maximal minors, sign convention validated
  by M·u = 0 at a non-sample h, limit by interpolation, basis by Cramer) → `plucker_k6.log` 128/128, `plucker_k7.log` 104/104 agree.
- `derivation_cert.py` → `derivation_cert.log`: ⚠ tests only the SPECIAL CASE Σλ·D(p)pᵀ = 0 (Pálvölgyi Thm 1 / OpenAI (31)); for the square +
  rectangle it finds only λ = 0, and our first draft wrongly concluded "no derivation certificate exists". Seat B (B_work/) showed the general
  condition of Pálvölgyi's Lemma A.1 is Σλ·D(p)pᵀ SYMMETRIC. Re-checked by the main seat: `lemmaA1_cert.py` → `lemmaA1_cert.log` (square +
  rectangle: 1-dim, energy 16λ/(1+t²)²; two squares and a passing 7-set: none), `lemmaA1_five.py` → `lemmaA1_five.log` (all five failing
  8-orbits have a certificate; passing 8- and 7-point controls none), `weights_check.log` (the explicit weights −2u², −2v², 1: all moments
  vanish, mixed moment symmetric diagonal, energy 16/(1+t²)²). B's symbolic reduced block for the square + rectangle: seats/B_work/sqrect_reduced.py.
- `palvolgyi_check.py` → `palvolgyi_check.log`: Pálvölgyi's identities (2), (3) recomputed (moments vanish; Σλ‖D(p)‖²·R = −24).
- `nine_det.py` → `nine_det.log`: Prop 7.6 det at the paper's grid = 64; random rational points ≠ 0; diagonal control 0.
- `random_circle.py s n seed` → `random_s{6,7}.log`: one-parameter circle configurations (Möbius images of τ mixed with rational points).
  s = 6: 40/40 HOLDS (seed 6); s = 7: 40/40 HOLDS (seed 7).

## seats/
`BRIEF.md` (one brief, printed numbering); `O_report.md` (§§1–4), `T_report.md` (§§5–6), `L_report.md` (Lean vs paper), `W_report.md`
(sources + world) — all HOLDS AS READ; `main_reading.md` (the main seat's own line-by-line read, written before reading the seat reports);
`B_report.md` (blind read of the entry page against these files: 6 MUST-FIX — incl. the false "no derivation certificate" claim, missing
credit for wstrinz's one-parameter procedure, the spot-check wording, (c) not (b) for seat-read proofs, the "characterise" judgment, the private
repo — all applied) and `B_work/` (its scripts). Work files `O_work/`, `T_work/`, `L_scratch/`, `W_src/` (FC copies,
OpenAI CONTENTS entry, prior-work snippets; third-party PDFs not redistributed — `THIRD_PARTY_DOWNLOADS_NOT_REDISTRIBUTED.sha256`).
`receipts.sh` → `MODEL_RECEIPTS.txt`: served-model fields per seat transcript.

## live/
erdosproblems.com/174, its forum thread and proof-claims tab as fetched 2026-10-21 21:04Z via the Hetzner box (+ text extractions).

## entry/
`entry174.js` (the /day entry), `apply174.py` (splices it + OAI_CLAIMS / LEAN_LABEL / CLOSED_BY_LITERATURE / HEADLINES / a dated
pointer on the 11 Aug #174 entry), `make_bundle.sh` (this bundle).
