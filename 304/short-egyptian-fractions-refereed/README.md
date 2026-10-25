# Erdős #304 (+ #148, #293) — OpenAI family 25 "Short Egyptian fractions" (25 Sep 2026; public 6 Oct), refereed 2026-10-21

Claims: Theorem 1.1 — c₁ log log b ≤ N(b) ≤ c₂ log log b for b ≥ b₀ (Erdős #304: is N(b) ≪ log log b? yes). Corollary 1.2 — ck ≤ log log F(k) ≤ Ck
(#148). Corollary 1.3 — exp(exp(k/600)) ≤ v(k) ≤ 1 + k^(2^(k−1)) for large k, log 2/257 ≤ liminf log log v(k)/k ≤ limsup ≤ log 2 (#293).
The theorems, proofs and Lean are OpenAI's; Bloom–van Doorn's exposition (14 Oct) preceded us. Ours: the replay + controls, the kernel dependency
walk, three bridges to Formal Conjectures + controls, the readings, the small-case computations.
Entry: https://erdosproblemaday.com/day/304-openai-short-egyptian-fractions-refereed

Paper: `paper/SOURCE.txt` (sha256 of the PDF/TeX we read, the openai/math commit; not redistributed). Printed sections: 1 intro · 2 elementary ·
3 divisors · 4 residues(+random) · 5 descent · 6 counting · 7–8 prescribed. All citations below use PRINTED numbers.

## replay/ — kernel replay of OpenAI's Lean (openai/math @ 1581d4c lean/, Lean v4.34.1, Mathlib d13f23b7)
- Two developments sharing no imports: OAI/NumberTheory/ShortEgyptian (58 modules, 8,140 lines; `OAI.ShortEgyptian.main`) and
  OAI/NumberTheory/EgyptianFractions (290-module closure, 36,061 lines; nine `OAI.Problem337.*` theorems). `order.txt` = the 348-module closure.
- `drive.py` (lake-free, DAG-parallel, W=4, memory-gated; adapted from the #416 driver): 348/348, 0 errors, 15 min 55 s wall
  (18:08:35Z → 18:24:30Z), Σ per-module wall 3,260 s, peak RSS 6.70 GiB. `modules.tsv`, `driver.log`, per-module logs `logs/module_logs.tar.xz`.
  Mathlib oleans from `lake exe cache get` (`cacheget.sh`; a first attempt under `ulimit -v` aborted "failed to create thread", log kept).
- `post.sh`: both comparator modules built; probes `probe/{CmpSE,CmpEF,AxSE,AxEF,Neg,TypeCtl}.lean`. `#print axioms` with `--trust=0`
  (`logs/axSE.log`, `logs/axEF.log`): all ten theorems → [propext, Classical.choice, Quot.sound]. `statement_match.py` → `statement_match.txt`:
  ShortEgyptianFractions 4/4 MATCH (main + IsExpansion, minLength, maxMinLength), EgyptianFractions 20/20 MATCH (nine theorems + eleven defs),
  standard axioms on the solution, sorryAx seen on the comparator. Matcher mutation test `mut/MUTATIONS.txt` (6/6 as wanted).
  Controls: `Neg.lean` planted sorry → sorryAx; `TypeCtl.lean` (`exact_marker_padding` at length 2) → rc 1.
- `probe/Deps.lean` → `logs/deps.log`, `logs/deps_summary.txt`: walk of every OAI constant reachable from each of the ten theorems (types and
  values, theorem bodies included via `value? (allowOpaque := true)`), recording defining modules. ShortEgyptian.main uses all 58 of its modules.
  The nine Problem337 theorems use 233 of the 290; the 57 unused include every ThreePrime*, Vaughan*, MinorArc*, MajorArc*, Mangoldt* module.
  `quantitative_marked_length` (Prop 8.1, the 257/log 2 slope) is `CompositeSupply.quantitative_marked_length` (CompositeSupplyFinal.lean),
  "proved by the composite cube-free route without any prime-triple distribution premise" — not the paper's three-primes §8.1.
- `leanchecker.sh`: `leanchecker --fresh BridgeAll` (BridgeAll imports both bridges ⇒ all 348 OpenAI modules + Mathlib + bridges), then a
  missing-module control. `leanchecker --fresh BridgeAll` rc 0 after 3,543 s, peak RSS 8.2 GiB (`logs/leanchecker_fresh.log`);
  missing-module control rc 1 (`logs/leanchecker_missing.log`). Mathlib .lake deleted after (disk guard; `LAKE_DELETED.txt`).
- `steps.tsv` = every step's rc and seconds. `ESTIMATE.md` = the estimate written before spending CPU.

## bridge/ — Formal Conjectures from OpenAI's library (ours)
FC files copied verbatim from google-deepmind/formal-conjectures @ 2a315101d438a68c0ebdf22b7485ac731624efed (21 Oct 2026): `FC_304.lean`,
`FC_148.lean` (Apache-2.0; sha256 in `FC_SHA.txt`).
- `Bridge304.lean`: FC's `unitFractionExpressible`, `smallestCollection`, `smallestCollectionTo` and the statements of `upper_bound`,
  `erdos_304.variants.lower_1950` VERBATIM. `oai_sum_eq` (OpenAI's list sum, elaborated through the coercion List ℕ → List ℚ, = finset sum),
  `unitFractionExpressible_eq_oai` (finsets ↔ strictly increasing lists via `Finset.sort`), `smallestCollection_eq_minLength`,
  `smallestCollectionTo_eq_maxMinLength` (sSup of the image = `Finset.sup'`), then both theorems from `OAI.ShortEgyptian.main`.
- `Bridge148_293.lean`: FC's `Erdos148.F` VERBATIM; `F_eq_oai` (finsets ↔ strictly increasing `Fin k → ℕ` via `Finset.orderEmbOfFin`, `Set.ncard_congr`);
  OUR statement `erdos_148.variants.double_log_order` (log log F ≍ k, Θ) from `counting_double_log_order`. #293 (no FC file): OUR `Erdos293.v`
  (FC style), `v_eq_oai`, `erdos_293.variants.explicit_bounds` (exp(exp(k/600)) ≤ v k ≤ 1 + k^(2^(k−1)) eventually) and
  `erdos_293.variants.double_log_order` (Θ; the upper half by our estimate 1 + k^(2^(k−1)) ≤ 2^(4^k)).
- `Bridge148LB.lean` (imports `Bridge148_293`; kept separate so the running leanchecker over `Bridge148_293` is undisturbed — its source sha256 is
  unchanged since that olean was built): FC's `erdos_148.variants.lower_bound` (Konyagin's form, research solved, `sorry` in FC) VERBATIM, from
  `counting_double_log_order` with o := 0. `AxBridgeLB.log` → standard axioms. Mutant `Bridge148LBMutStmt` (k·log k for k/log k) fails.
- `AxBridge.log`: the eight theorems of the first two files → [propext, Classical.choice, Quot.sound]. Mutants (must fail, do — `build_bridge.out`): `Bridge304MutDef` (n > 0),
  `Bridge304MutStmt` (log log log b), `Bridge148MutDef` (1 ∉ S for 0 ∉ S), `Bridge293MutStmt` (≍ k²).
- `verbatim_check.py`: seven FC items + `open` lines MATCH (whitespace-normalised); `--mutate` / `--mutate148` / `--mutateLB` exit 1.
This proves FC's statements in OpenAI's environment (Lean 4.34.1, Mathlib d13f23b7), not FC's own constants.

## empirical/ — small cases (ours, label (d))
- `enum1.py` (route A: DFS on the remaining fraction, last two terms from divisors of q²) → `enum1_k6.log`, `enum1_k7.log`: F(1..7) = 1, 0, 1, 6, 72,
  2320, 245765; v(1..7) = 2, 2, 4, 11, 17, 103, 733; |D_7| = 83,231; Lean bounds n_i ≤ k^(2^(i−1)), F ≤ k^(2^k−1), v ≤ 1 + k^(2^(k−1)) checked on every
  expansion; max denominator = Sylvester s_k − 1. `enum2.py` (route B: plain Fraction recursion) → `enum2_k6.log`: identical F, |D_k|, v for k ≤ 6.
  Seat P's separately written enumerator (`seats/P_scripts/`) agrees through k = 7.
- `nab.py` → `nab_60.log`: exact N(b), b ≤ 60 (matches OEIS A097849; seat W matched b ≤ 40 independently). `nab2.py`: first b with N(b) = k
  (11, 17, 79 for k = 4, 5, 6 = OEIS A097048) and N(732,733) = 7. `nab3.py`: first b with N(b−1, b) = k: 11, 17, 103, 733 for k = 4..7 = v(4..7).
  The inequality v(k) ≤ min{m : N(m−1, m) ≥ k} is elementary (van Doorn–Tang's reduction; FC PR #4870); equality fails at k = 3.

## seats/ — referee reports (all Claude Opus 5.5; `MODEL_RECEIPTS.txt` from `receipts.sh`). Correlated readers, not independent ones.
- `BRIEF.md` common brief. `main_reading.md` — main seat's own reading of §2, §5, §6: HOLDS AS READ.
- `U_report.md` (§§2–5, upper bound): HOLDS AS READ; 3 exposition notes; checks in `U_checks/`.
- `P_report.md` (§§6–8): HOLDS AS READ; O1 structural (§8 independent of §§3–5), O2/O3/O5 exposition, O4 attribution; scripts `P_scripts/`.
- `L_report.md` (Lean vs paper vs problems): HOLDS AS READ; L3 = the §8.1 dependency point (confirmed by `replay/probe/Deps.lean`).
- `W_report.md` (citations, priority, world): HOLDS AS READ; omitted intermediate results (Price 24 Jul; van Doorn–GPT-6 Astra Pro 16 Sep);
  FC PR #6842's 681943 tuple mis-transcribed (144/1984 for 44/984; the forum tuple sums to exactly 1 — re-checked by the main seat).
- `B_report.md` — blind consistency read of the entry draft: 12 MUST-FIX + 36 OPTIONAL; all MUST-FIX and nearly all OPTIONAL applied
  (`entry/entry_draft.js.pre-blind` vs `entry_draft.js`, `mkvalues.py` vs `mkvalues2.py`). Item 6 led to `Bridge148LB.lean`.

## live/ — erdosproblems.com pages fetched 2026-10-21 via the Hetzner box (304/148/293 + threads + proof-claims tabs; #18 proof claims; Bloom's
8 Oct blog post `blog10.html`); `teorth_head.txt` = teorth/erdosproblems main at the time (302a00e).
## entry/ — entry_draft.js, values.json, mkvalues.py, apply304.py, smoke304.mjs; the FC issue draft (staged, not posted).
