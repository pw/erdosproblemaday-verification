# Erdős #968 — OpenAI family 26 "Positive lower density of large prime gaps" (25 Sep 2026), refereed 2026-10-21

Claim (Theorem 1.1): for every fixed real C > 0 there are c(C) > 0 and N₀(C) with #{1 ≤ n ≤ N : p_{n+1} − p_n > C log p_n} ≥ c(C)·N
for every N ≥ N₀(C). Corollary 1.2 (the Erdős–Prachar question, Erdős problem #968): {n ≥ 1 : p_n/n < p_{n+1}/(n+1)} has positive lower
asymptotic density. The theorem, its proof and its Lean are OpenAI's. Ours: the replay + controls, the bridge to Formal Conjectures' statement +
controls, the readings, the empirical counts to 10⁹. Entry: https://erdosproblemaday.com/day/968-openai-large-prime-gaps-positive-proportion-refereed

Paper: see `paper/SOURCE.txt` (sha256 of the PDF and TeX we read, openai/math commit; not redistributed here). Printed section order ≠ TeX file
order: §1 01-introduction, §2 02-counting, §3 04-weights, §4 05-cancellation, §5 03-moments. Every citation below uses the PRINTED numbers.

## replay/ — kernel replay of OpenAI's Lean (56 modules, OAI/NumberTheory/PrimeGaps, Lean v4.34.1, Mathlib d13f23b7)
- `drive.py` (lake-free, DAG-parallel, W=4, memory-gated; adapted from the #802 driver) built 56/56 modules, 0 errors, 11 min 40 s wall
  (06:10:20Z → 06:22:00Z; Σ per-module wall 699 s; no module over 26 s); peak RSS 6.75 GiB (ZeroFreeBounds). `modules.tsv`, `driver.log`,
  `order.txt`, per-module logs in `logs/module_logs.tar.xz`. Mathlib oleans from `lake exe cache get` (`cacheget.sh`), not rebuilt — hence
  leanchecker below.
- Source audit: no axiom, sorry, admit, native_decide, set_option, macro/elab/syntax, unsafe, implemented_by, extern, opaque, partial def, #eval
  in the 56 files (22,533 lines); six `decide`, all trivial (seat L lists them). Imports: Mathlib only. `MATHLIB_GREP.txt`: Mathlib d13f23b7 has
  no large sieve, Pólya–Vinogradov, Vaughan identity, Siegel–Walfisz, Bombieri–Vinogradov or Siegel's theorem on L(1,χ).
- `post.sh`: comparator module `ComparatorChallenges/PrimeGaps` built; probes `probe/{Smoke,Cmp,Ax,Neg,TypeCtl}.lean`. `#print axioms`
  (`logs/ax.log`): large_gaps_and_ratio_density, LargePrimeGaps.main, bombieriVinogradov, siegelWalfisz,
  positive_lower_density_prime_ratio_increases → [propext, Classical.choice, Quot.sound]. `statement_match.py` → `statement_match.txt`: the
  theorem type + all six definitions (prime, largeGapIndices, primeAt, initialCount, lowerAsymptoticDensity, ratioIncreaseIndices) MATCH under
  pp.all (blocks delimited by explicit `@@@ BEGIN` markers printed by the probes), STD_AXIOMS, CMP_SORRY_SEEN. Matcher mutation test
  `mut/MUTATION_RESULTS.txt` (6/6): numeral changed in a definition → MISMATCH; LE→LT in the theorem → MISMATCH; challenge without sorryAx →
  CMP_SORRY_NOT_SEEN; solution with an extra axiom → NONSTD; a definition block missing → exit 2 (cannot see); unmodified → exit 0.
  Controls: `Neg.lean` planted sorry → sorryAx; `TypeCtl.lean` (gap theorem at C = 0) → rc 1, type mismatch.
- `leanchecker.sh`: `leanchecker --fresh Bridge968` (the bridge imports `OAI.NumberTheory.PrimeGaps.RatioCorollary`, whose closure is all 56 of
  OpenAI's modules + Mathlib) re-checked every declaration from scratch: rc 0 after 3,456 s, peak RSS 8.2 GiB (`logs/leanchecker_fresh.log`);
  missing-module control rc 1 (`logs/leanchecker_missing.log`). Mathlib .lake deleted after (disk guard).
- `steps.tsv` = every step's rc and seconds.

## bridge/ — Formal Conjectures' erdos_968 from OpenAI's library (ours)
`Bridge968.lean`: FC's `Set.partialDensity`, `Set.lowerDensity` (FormalConjecturesForMathlib/Data/Set/Density.lean) and `Erdos968.u`,
`Erdos968.erdos_968` (FormalConjectures/ErdosProblems/968.lean) copied VERBATIM from google-deepmind/formal-conjectures @
90d18f666eb98adec4eee4d12f1d37e30b4eb204 (copies: `FC_968.lean`, `FC_Density.lean`, Apache-2.0), under FC's own names (Mathlib d13f23b7 has
no constants of those names). FC's u is 0-based (u n = p_{n+1}/(n+1)) and its lowerDensity is liminf |S ∩ [0,b)|/b; OpenAI's set is 1-based
and its lowerAsymptoticDensity is sSup{d | d ≤ count/N eventually}. `mem_iff`: n ∈ FC's set ↔ n+1 ∈ OpenAI's; `count_eq`: FC's count below b =
OpenAI's initialCount up to b (bijection n ↦ n+1); then 0 < sSup ⇒ some d > 0 eventually ≤ FC's partial density ⇒ liminf ≥ d.
- `Bridge968.log`: compiles, no warnings; `AxBridge.log`: `#print axioms` → [propext, Classical.choice, Quot.sound] for erdos_968, mem_iff, count_eq.
- `verbatim_check.py`: the statement + three definitions MATCH FC's text (whitespace-normalised); `--mutate` (Iio → Iic in partialDensity) exits 1.
- Controls: `BridgeMutDef.lean` (u divides by n + 2) fails at mem_iff's final rfl; `BridgeMutStmt.lean` (FC's set replaced by the decreasing
  set {n | u n > u (n+1)}, Erdős–Prachar's own theorem, which OpenAI's library does not prove) fails at the counting step.
This proves FC's statement in OpenAI's environment (Lean 4.34.1, Mathlib d13f23b7), not FC's own constant (FC: Lean 4.33.1).

## empirical/ — what the numbers look like (ours, label (c))
`gaps.c` (segmented sieve to 2.3·10¹⁰, all n ≤ 10⁹; predicate (n+1)p_n < n·p_{n+1} in 128-bit) → `run_2.3e10.log` (151.6 s, 6.3 MB).
`gaps_raw.c` prints raw counts. `CONTROLS.txt`: reproduces the 10,000-term b-file of OEIS A387591 (`b387591.txt`, fetched 2026-10-21) exactly;
two wrong predicates (reversed, index-shifted) fail that diff; ≤-for-< passes and is provably equivalent; p_N equals the known values at
10⁶…10⁹; `recount.py` (numpy, independent) reproduces every count at 10⁶ and 10⁷ exactly (`recount.log`).
`recount2/` (09:00Z seat, second instrument): `recount2.py`, a separately written numpy segmented sieve over odd numbers with the increase
predicate in the rearranged form n·(p_{n+1} − p_n) > p_n, run to 2.28·10¹⁰ (`recount2_1e9.log`), and `gaps_raw.c` re-run to the same limit
(`gaps_raw_1e9.log`): EXACT agreement on every count (increases; gaps above 1, 2, 3, 6 × log p_n) at 10⁶, 10⁷, 10⁸ and 10⁹ (`CROSSCHECK.txt`).

## seats/ — referee reports (Claude Opus 5.5 seats; briefs + reports)
Every seat ran on Claude Opus 5.5 (`MODEL_RECEIPTS.txt`, from `receipts.sh`: per-transcript counts of served-model fields, 0 other models).
They are correlated readers, not independent ones. `COMMON.md` = the common brief; `<SEAT>_brief.md` = each seat's scope.
- `main_reading.md` — the 09:00Z main seat's own line-by-line notes on printed §§1–5: HOLDS AS READ (4 exposition notes).
- `L_report.md` — Lean vs paper (06:00Z seat): HOLDS AS READ; the paper-to-Lean table (every printed statement → declaration, file:line).
- `O_report.md` — printed §§2–4 + Cor 1.2 (09:00Z rerun): HOLDS AS READ. Scripts in `O_work/` (`v2_identity8.py` deletion identity (8)
  with a composite-m+a negative control; `v2_deriv.py` sympy; `v2_lemma41_direct.py`; `literal_k4.py` quadrature of the definitions of w, v;
  `largek.py` Monte Carlo; `v2_cf.py` characteristic-function evaluation at λ = 3, k up to 3·10¹⁵, controlled against the Monte Carlo at λ = 1).
- `T_report.md` — printed §5 (09:00Z rerun): HOLDS AS READ (2 exposition remarks). `T_work/` (`fourier_check.py` H_p(0) and (14);
  `ss_box.py` Lemma 5.4 box means; `density_sum.py`).
- `W_report.md` — sources and the world (09:00Z rerun; carries forward the 06:00Z sub-seat `W_work/agentA.md` on Formal Conjectures history and
  prior Lean BV/SW work, spot-checked): HOLDS AS READ. Scans read, not redistributed: `W_work/SCANS.txt`.
- `BLIND_BRIEF.md` / `blind_report.md` — blind consistency read of the rendered entry before publication: 40 items (22 FACT, 4 OVERCLAIM,
  6 CONSISTENCY, 8 STYLE); all FACT/OVERCLAIM/CONSISTENCY items applied, most STYLE items applied. It caught a placeholder that would have shipped
  on the homepage card (the splice script now refuses any new `@@` in the output), a wrong theorem count (1,238 → 1,118 theorems + 175 lemmas),
  and "the same constant" where the Lean's detector constant is one larger.
- The 06:00Z seat's O/T/W seats and W's sub-agent agentB died on the Team-seat session limit before reporting (synthetic rows in the receipts);
  the 09:00Z seat re-ran O/T/W without sub-agents.

## live/ — erdosproblems.com/968, its forum thread (Tao's two comments, 8 and 10 Sep 2025) and proof-claims tab as fetched 2026-10-21 via our
Hetzner box; Bloom's blog:10 post as fetched the same day (lists [968]; "should not be read as any kind of endorsement").

## entry/ — the entry source, values, splice script, smoke test used to publish the /day page.
