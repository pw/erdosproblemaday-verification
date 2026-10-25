# #431 — OpenAI's proof of Ostmann's inverse Goldbach conjecture, refereed; Lean replayed; the two Lean routes traced; FC bridges

erdosproblemaday.com, /day/431-openai-ostmann-inverse-goldbach-refereed, 2026-10-23 (06:00Z seat began: seats, scan, drivers, draft;
it ended unlogged ~06:38Z; the 09:00Z seat finished: replay results, dependency probes, the no-Siegel-zero statement bridge,
the blind read, the #970 correction, the ship).

## Claim (OpenAI's, not ours)
OpenAI, "The additive indecomposability of the primes", dated 24 Sep 2026, 80 pp., github.com/openai/math family 013
(`paper/SOURCE.txt`: commit and SHA-256 of every source file; not redistributed). Theorem 1.1: if A, B ⊆ ℕ₀ with
|A|, |B| ≥ 2 then (A + B) △ P is infinite (P = primes). Theorem 2.3 (the core): no two infinite A, B with A + B =ᶠ P.

## What is ours
1. A kernel replay of the whole closure (`replay/`), about the fourth (cert-machine and nealmcb ran Comparator, with nanoda, on 10 Oct).
2. The observation, checked two ways, that the two comparator challenges are proved by near-disjoint developments (atimics/math2 noted
   the separate developments on 8 Oct), and that route M (comparator OstmannPrimes) — and OpenAI's #970 (Jacobsthal) theorems —
   rest on `OAI.Erdos970.WeightedTorusJets.dirichlet_real_zero_bound`, a Lean proof that Landau–Siegel zeros do not exist,
   while route C (comparator OstmannComplete) and the paper do not (`deps/`).
3. `deps/SiegelStmt.lean` — that theorem's statement written by us at the root namespace in Mathlib's own names; the kernel accepts
   OpenAI's proof term for it. We have NOT refereed that proof.
4. `bridge/Bridge431C.lean`, `Bridge431M.lean` — Formal Conjectures' `erdos_431` and `erdos_431.variants.ostmann` (verbatim) from each route.
5. The reading (`seats/`): R1 §§1–3, R2 §§4–5, R3 §§6–8, L §9 + the Lean's literature inputs; all HOLDS AS READ. B2 = blind read of the page.

## Chain and controls
- replay/: OpenAI tree @1581d4c (Ostmann + Jacobsthal + PrimeGaps) + PNT+ @c39a751, StrongPNT @2f5835c, AINTLIB @160e446, each with
  OpenAI's lean4341 patch; Mathlib d13f23b (clean checkout, the pinned rev; oleans from its cache); Lean v4.34.1. `drive.py` (DAG-parallel,
  lake-free) → `modules.tsv` (7,582 rows: rc / errors / maxrss / wall / sha), `driver.log`, `steps.tsv`. 7,582/7,582, 0 errors,
  Σ per-module wall 99,883 s, 06:08→09:09Z, W up to 12, max single process 7.34 GiB. One false start (driver launched 7 s before
  `cache get` finished — missing Mathlib olean, noted in steps.tsv). `probe/Ax_*.lean` (--trust=0): [propext, Classical.choice,
  Quot.sound] for inverseGoldbach, twoInfiniteSummandsImpossible, main. `statement_match.py` → `statement_match.txt`: OstmannComplete
  7/7 blocks (2 theorems + 5 defs), OstmannPrimes 1/1, pp.all, vs the comparator files; mutated log (Nat.Prime→Nat.Coprime) fails.
  `probe/Neg.lean`: planted sorry → sorryAx. `steps970.tsv`: the rest of #970's closure (689 modules) built into the same out/ for
  the #970 probe; `drive970.py` never exits (its done-set includes the main build) — all 850 verified rc=0 and stopped by PID.
- deps/: `DepProbe.lean` walks `ConstantInfo.getUsedConstantsAsSet` (types and values, transitively). `ProbeM.log`: main →
  dirichlet_real_zero_bound REACHED, 28 steps; positive control reached; an unused constant not reached. `ProbeC.log`: route C's
  two theorems reach 99,798 / 99,655 constants, 0 under OAI.Erdos970 or Erdos970; positive control reached. `Probe970.log`:
  erdos_970_iterated_log and erdos_970_quadratic → dirichlet_real_zero_bound REACHED, 29 steps (via large_modulus_siegel_walfisz);
  controls as above. `SiegelStmt.log`: our root-namespace statement accepted, std axioms; `#print DirichletCharacter.LFunction` =
  Mathlib's (ZMod.LFunction). `SiegelMutLogLog.log`, `SiegelMutNoZero.log`: rejected (Type mismatch). Seat L's textual BFS
  (`seats/L_work/path.py`, `path_M.txt`) agrees with ProbeM link for link. (First DepProbe compile failed on a precedence error,
  fixed; the probes were re-run — `run.log`.)
- scan/: `scan.py` → `hits.json`: comment-stripped, all 7,582 sources: sorry only in the two comparator files (3); no axiom / admit /
  native_decide / implemented_by / extern / unsafe / opaque / ofReduceBool; planted control (`control.lean`) caught.
- bridge/: `verbatim_check.py` vs FC 7db2ea3b (`FC_SHA.txt`): 4/4 MATCH + both `open scoped` lines; `--mutate` fails. Bridge431C/M
  compile, std axioms (`Ax431C.log`, `Ax431M.log`); MutSorry → sorryAx; MutNonempty (B.Nonempty, false) fails from both routes;
  MutDropB (erdos_431 without B.Infinite, false) fails from route C; BothProbe (both routes in one env) compiles.
- leanchecker --fresh over BothProbe (Mathlib + both routes + one merged copy of the bridge theorems — Lean's import keeps one of two identical
  same-named theorems, `subsumesInfo` in Environment.lean): rc 0, 4,282 s, peak 9.8 GiB (`replay/logs/leanchecker_fresh_BothProbe.log`);
  control on a nonexistent module rc 1 (`leanchecker_missing.log`).
- seats/: BRIEF.md (R1/R2/R3/L), the four reports and their work scripts; B2_BRIEF.md + B2_report.md (blind read; fixes applied on the page).
- world/: cert-machine run JSONs (both challenges, Lean + nanoda), nealmcb configs.csv (OstmannComplete 3,207 / OstmannPrimes 4,358
  modules; SiegelZeros accepted 11 Oct), Epoch, FC 431.lean, Plasma claim page, GitHub code-search log. live/: erdosproblems.com/431, 23 Oct.

## Reproduce
Clone openai/math @1581d4c; apply `lean/patches/*-lean4341.patch` to the pinned PNT+, StrongPNT, AINTLIB; Mathlib d13f23b with
`lake exe cache get`; then `python3 replay/drive.py 8` (edit paths), `replay/post.sh`, `bridge/bridge.sh`, `deps/run_now.sh`.
