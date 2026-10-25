# Erdős #802 — OpenAI family 184 "A logarithmic independence bound for clique-free graphs" (25 Sep 2026), refereed 2026-10-21

Claim (Theorem 1.1): for every r ≥ 4 there is c_r > 0 such that every finite simple K_r-free graph with n vertices and average degree
d ≥ 2 has α(G) ≥ c_r·n·log d/d — the Ajtai–Erdős–Komlós–Szemerédi conjecture (Combinatorica 1981, Equation (3)), Erdős problem #802.
The theorem, its proof and its Lean are OpenAI's. Ours: the replay + controls, the bridge to Formal Conjectures' statement + controls,
the readings, the constant arithmetic. Entry: https://erdosproblemaday.com/day/802-openai-aeks-independence-refereed

Paper: see `paper/SOURCE.txt` (sha256 of both family-184 PDFs, openai/math commit; not redistributed here).

## replay/ — kernel replay of OpenAI's Lean (31 modules, OAI/Combinatorics/CliqueFree, Lean v4.34.1, Mathlib d13f23b7)
- `drive.py` (lake-free, DAG-parallel, W=4, memory-gated; adapted from the #551/#986 drivers) built 31/31 modules, 0 errors, 2 min 29 s wall
  (03:15:41Z → 03:18:10Z; Σ per-module wall 289 s); peak RSS 6.6 GiB (FiniteCoupling). `modules.tsv`, `driver.log`, per-module logs in
  `logs/module_logs.tar.xz`. Mathlib oleans from `lake exe cache get` (`cacheget.sh`), not rebuilt — hence leanchecker below.
- Source audit (ours + seat L): no axiom, sorry, admit, native_decide, decide, set_option, macro/elab/syntax, unsafe, implemented_by, extern,
  opaque, partial def, #eval in the 31 files (5,539 lines). Imports: Mathlib only.
- `post.sh`: comparator module `ComparatorChallenges/CliqueFreeLog` built; probes `probe/{Smoke,Cmp,Ax,Neg,TypeCtl}.lean`.
  `#print axioms` (`logs/ax.log`, `--trust=0`): logarithmic_independence_bound, maximum_degree_independence, exists_optimizer_triangle_bound
  → [propext, Classical.choice, Quot.sound]. `statement_match.py` → `statement_match.txt`: theorem type + `averageDegree` definition MATCH under
  pp.all, STD_AXIOMS, CMP_SORRY_SEEN. Matcher mutation test `mut/MUTATION_RESULTS.txt`: changed numeral in averageDegree → MISMATCH;
  challenge without sorryAx → CMP_SORRY_NOT_SEEN; solution with extra axiom → NONSTD. Controls: `Neg.lean` planted sorry → sorryAx;
  `TypeCtl.lean` (theorem applied with 3 ≤ r) → rc 1, type mismatch at hr.
- leanchecker --fresh over `Bridge802` (which imports OAI.Combinatorics.CliqueFree.Main ⇒ OpenAI's closure + Mathlib + our bridge):
  started 2026-10-21T03:28:17Z (`leanchecker.sh`): rc 0 after 3449 s (Mathlib + OpenAI's closure + the bridge, from scratch); missing-module control rc 1.
  Rows `leanchecker_fresh` + `leanchecker_missing_control` in `steps.tsv`; logs `logs/leanchecker_fresh.log`, `logs/leanchecker_missing.log`.
- `steps.tsv` = every step's rc and seconds.

## bridge/ — Formal Conjectures' erdos_802 from OpenAI's library (ours)
`Bridge802.lean`: FC's `SimpleGraph.averageDegree` (FormalConjecturesForMathlib/Combinatorics/SimpleGraph/Degrees.lean) and the statements
`erdos_802`, `erdos_802.variants.aeks`, `erdos_802.variants.r_eq_three` (FormalConjectures/ErdosProblems/802.lean) copied VERBATIM from
google-deepmind/formal-conjectures @ 90d18f666eb98adec4eee4d12f1d37e30b4eb204 (copies: `FC_802.lean`, `FC_Degrees.lean`, Apache-2.0).
FC's statement asks for every r and NO lower bound on the average degree t: t = 0 trivial (log 0 = 0, x/0 = 0); 0 < t < 2 via OpenAI's
`maximum_degree_independence` with Δ = 4 on the ≥ n/2 vertices of degree ≤ 2t (`degree_cutoff_card`), using log t/t < 1; r ≤ 3 via
`CliqueFree.mono` to r = 4; FC's ℚ-valued average degree = OpenAI's real 2|E|/|V| after the cast (handshake). `Core802.lean` = the core alone.
- `Bridge802.log`: compiles, `#print axioms` → [propext, Classical.choice, Quot.sound] for core, erdos_802, variants.aeks, variants.r_eq_three.
- `verbatim_check.py`: the three statements + the definition MATCH FC's text (whitespace-normalised); `--mutate` (≤ → <) exits 1.
- Controls: `BridgeMutDef.lean` (definition doubled) fails in `averageDegree_cast`; `BridgeMutStmt.lean` (n → n·n) fails in erdos_802.
This proves FC's statement in OpenAI's environment (Lean 4.34.1, Mathlib d13f23b7), not FC's own constant (FC: Lean 4.33.1).

## seats/ — referee reports (Claude Opus 5.5 seats; briefs + reports)
Main seat (the coordinator) read §§1–6 line by line. Hostile seats, each briefed by `COMMON.md` + its own brief, told to refute and quote:
- O (§2 + §6): HOLDS AS READ — `O_report.md`, scripts `O_work/` (Lemma 2.2 construction in exact rationals, 3,708 runs; Lemma 2.3 chain on 540
  instances; (6.2)/(6.3); the vacuity warning about brute-forcing (2.5); the K_{m,k} stationary point with ratio 374.7 > 144, 256 — `saddle.py`).
- T (§§3–5): HOLDS AS READ — `T_report.md`, scripts `T_work/` (5 negative controls in `negctl.py` + the K_{5,5} blow-up; 5 exposition notes).
- L (Lean vs paper): HOLDS AS READ — `L_report.md` (paper→Lean table §2, audit counts §3, route differences §5).
- W (world + sources): HOLDS AS READ — `W_report.md` (AKS 1980 + Shearer 1983 primary PDFs paywalled: secondary sources only).
- Blind read of the entry before deploy: `BLIND_BRIEF.md` → `blind_report.md` (41 items; applied to the entry except #6 and #36, which are
  site-template issues). All seats served by Claude Opus 5.5: `MODEL_RECEIPTS.txt`. Seats share one model — correlated, not independent, readers.

## constant/ — the c_r the printed constants give (ours)
`constant.py` → `constant.out`: c_4 ≈ 10^(−3.6·10^18); in general c_r = exp(−Θ(r^8 log² r)).

## live/ — erdosproblems.com/802, its forum thread and proof-claims tab as fetched 2026-10-21 (via our Hetzner box); Bloom's blog:10 post as
saved 2026-10-12 (lists [802], "should not be read as any kind of endorsement").

## entry/ — the entry source, values, splice script, smoke test and renderer used to publish the /day page.
