# #551 — OpenAI family 189, "Cycle–clique Ramsey numbers": refereed + replayed (erdosproblemaday.com, 2026-10-20)

Page: https://erdosproblemaday.com/day/551-openai-cycle-clique-ramsey-refereed

**Claim (OpenAI, dated 25 Sep 2026; public 6 Oct 2026, openai/math adc7f12, unchanged at 1581d4c):** R(C_m, K_n) = (m−1)(n−1)+1 for all
m ≥ n ≥ 3 with (m,n) ≠ (3,3); R(C_3,K_3) = 6 (the Erdős–Faudree–Rousseau–Schelp conjecture, Erdős #551).
Paper: `paper/SOURCE.txt` (sha256 366fc1d94b08e498183f475b170db56c72c7c898a24f3d3f1106e637ef42209b, 41 pp; not redistributed here).

## replay/ — OpenAI's Lean (route A, the comparator's), kernel-replayed
- Source: openai/math @ 1581d4cb, `lean/OAI/Combinatorics/Ramsey/CycleClique/` (443 modules, 222.6 MB, 2.80 M lines; Lean 4.34.1,
  Mathlib d13f23b7; imports only Mathlib + itself). TWO routes: (A) `OAI.CycleClique.thm_main` in `MainTheorem.lean`, the comparator
  challenge's theorem — import closure 182 modules / 28.3 MB / 43,320 `decide`, DAG depth 32 (`order.txt`); (B) `Construction/`
  (261 further modules, 194.3 MB, per-k certificates) behind `Main.lean`'s `cycle_clique_main_unconditional` — NOT replayed here.
  Source audit (grep, all 443 modules): 0 axiom declarations (the single `axiom` hit is a docstring in Construction/PublishedInputs.lean) /
  0 sorry / native_decide / set_option / macro / elab / syntax / unsafe / implemented_by / extern / opaque / #eval / ofReduceBool /
  maxHeartbeats / Lean.Meta / IO; 443,867 `decide` tokens (whole tree).
- `ESTIMATE.md` written before CPU. `drive.py` = lake-free DAG-parallel driver (≤ 3 lean at once, nice 19, LEAN_NUM_THREADS=1, launch gate
  MemAvailable ≥ 27 GB); `modules.tsv` = per-module rc / errors / max RSS / wall / olean sha.
  Result: 182/182 rc 0, 0 errors, 21:06:15Z → 22:57:23Z (1 h 51 min wall; Σ module wall 19,251 s; peak RSS 8,211,088 KiB ≈ 7.8 GiB, Certificates039). Mathlib d13f23b7 `.lake` re-fetched by `cacheget.sh` (`lake exe cache get`, 21:04–21:05Z).
- `post.sh` probes (`probe/`, logs in `logs/`): comparator module compiled; `Cmp.lean`/`Ax.lean` print pp.all of `thm_main` and of
  `RamseyProperty`, `cycleCliqueRamsey` in the challenge and in the solution; `statement_match.py` → `statement_match.txt`.
  `statement_match.txt`: MATCH (thm_main 1182 chars, RamseyProperty 641, cycleCliqueRamsey 191 — identical), solution axioms exactly {propext, Classical.choice, Quot.sound} for thm_main, main, exceptional, ramsey_upper, finite_range_verified, ramsey_lower_counterexample (`ax.log`, run with --trust=0); comparator copy carries sorryAx. `mut/MUTATION_RESULTS.txt`: matcher flags Fin→Fim inside RamseyProperty's printed body (MISMATCH), sorryAx deleted from the challenge's list (CMP_SORRY_NOT_SEEN), Lean.ofReduceBool added to the solution's (NONSTD); unmutated → MATCH. Controls: `Neg.lean` planted sorry → sorryAx; `TypeCtl.lean` (thm_main at R(C4,K4) = 9) fails, rc 1, type (4−1)(4−1)+1; `Pos44.lean` (same term at the true value) rc 0.
- leanchecker --fresh OAI.Combinatorics.Ramsey.CycleClique.MainTheorem: started 22:58:34Z (post.sh, after PROBES_DONE); see `steps.tsv` row `leanchecker_fresh` + `logs/leanchecker_fresh.log` — rc 0 after 11486 s (Mathlib included, from scratch; ended 2026-10-21 02:10:00Z); missing-module control rc 1 (`logs/leanchecker_missing.log`).

## bridge/ — Formal Conjectures' statement from OpenAI's theorem (ours)
`Bridge551.lean`: FC's `SimpleGraph.graphRamsey` and both `erdos_551` statements copied verbatim (FC @ 90d18f666e, 20 Oct 20:20Z;
`FormalConjecturesForMathlib/Combinatorics/SimpleGraph/Ramsey.lean`, `FormalConjectures/ErdosProblems/551.lean`; only the enclosing
namespace differs), proved from `OAI.CycleClique.main` (route A). Compiled rc 0; `bridge.log`: `Bridge551.Erdos551.erdos_551` and `.variants.sufficiently_large` both on [propext, Classical.choice, Quot.sound]. Controls: `BridgeWrongShape.lean` (value (k−1)(n−1), no +1) fails at the `rw`; `BridgeMut.lean` (`cycleGraph (k+1)`) fails at `rfl`.
Not compiled in FC's own environment (different Lean/Mathlib pins): this checks a verbatim COPY of FC's statement, not FC's constant.

## finite/ — the finite stage, recounted and re-run (ours)
- `count_patterns.py` (+ `.out`): our own brute-force enumerator (multisets of reversal-normalised chain types; no code shared with
  either released checker) reproduces every row of the paper's Table 1 — 42 pairs, 3,099 patterns; negative control (budget + 1) → 5,735.
- `lean_pattern_lists.py` (+ `.out`): the pattern lists hard-coded in the Lean (`Patterns{k}x{t}.lean`, defs `patterns_k_t_i`) equal our
  enumeration as SETS for all 42 pairs, canonical form, no duplicates (3,099 total). Mutant (`lean_pattern_lists_MUT.py`, budget − 1)
  fails 38/42 pairs, rc 1 (the 4 pairs with t = k have budget 0 either way).
- `run1/` — both released checkers re-run UNMODIFIED via their `verify.py` (CPython 3.12.3, 197 s wall, 72 MB): original 50.5 s,
  independent 146.0 s, both stdout byte-identical to `expected-output.txt` (sha256 4cc194d9…), stderr empty, regenerated trace
  byte-identical to the shipped `certificates.jsonl` (sha256 a5646def…). `pristine.sha256` = hashes of the code/data as run.
- Seat F's mutation/validator work is in `seats/F_work/` (copies of OpenAI's checkers, Apache-2.0 — see NOTICE); `seats/F_work/artifacts/s6_initial_diff.py` (+ `.out`) regenerates the S6 figure: deleting Lemma 9.4's degree test changes 2,471 of 3,099 initial matrices in the original checker. Seat P's t = 8 control: `seats/seatP_work/model_t8.out` (169 violations).

## seats/ — readings
- `main_reading.md` — the main seat's own line-by-line reading of §2–§9: HOLDS AS READ.
- `seatP_proof.md` — hostile seat on §5–§8: HOLDS AS READ (E1–E5 exposition; model check t = 9..12, ~79 M systems, 0 violations; t = 8 control 169).
- `seatF_finite.md` (+ `F_work/`) — hostile seat on §9, Appendix A, the two checkers and the Lean finite stage: HOLDS AS READ (E1 Lemma 9.4's E = any subset; E2 verify.py should check matrices; third validator 3,099/3,099).
- `seatW_world.md` (+ `W/`) — sources, priority, Formal Conjectures, Bloom's side questions: HOLDS AS READ (exposition notes; Nikiforov Case 4.1 arithmetic confirmed on arXiv v1; DS1.18 Table Vb R(C8,K9) = 56 < 57).
- `blind_read.md` (+ `blind_work/`) — tool-equipped blind read of the rendered page before deploy: 43 findings (9 wrong, 7 overclaim, 6 unsupported, 17 unclear, 4 inconsistency), none touching the mathematics; all applied before deploy.
- `COMMON.md` — the shared brief. `MODEL_RECEIPTS.txt` — served-model counts per seat transcript.

## world/
`live_551.html` — erdosproblems.com/551 + proof-claims + thread, fetched 2026-10-20 ~21:02Z via the Hetzner box (no proof claims; Tao 1 Sep 2025).
`FC_551.lean`, `FC_Ramsey.lean` — Formal Conjectures files as bridged.

## Reproduce
Replay: `replay/drive.py 3` then `replay/post.sh` (paths are /tmp/oaimath/189/…; toolchain via elan v4.34.1; Mathlib d13f23b7 with
`lake exe cache get`). Finite: `python3 finite/count_patterns.py`; `python3 finite/lean_pattern_lists.py` (needs the openai/math checkout);
`python3 -I verification/code/verify.py --output /tmp/x` in the paper's directory.
