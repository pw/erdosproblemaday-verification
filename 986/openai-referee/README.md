# Erdős #986 — OpenAI's sharp log exponent for r(s,t), s ≥ 5: both Lean proofs kernel-replayed, the s = 4 case found in the same library, and a bridge to Formal Conjectures' statement

erdosproblemaday.com entry: `/day/986-openai-sharp-log-exponent-off-diagonal-ramsey-refereed` (2026-10-20).

**The problem.** "For any fixed s ≥ 3, R(s,k) ≫ k^{s−1}/(log k)^c for some c = c(s) > 0" (erdosproblems.com/986, last edited
21 June 2026: resolved by Bradač, arXiv:2605.28793 v3, c = 2s − 4). Upper bound O(t^{s−1}/(log t)^{s−2}) = Ajtai–Komlós–Szemerédi 1980.

**The claim under review.** OpenAI family 170 (github.com/openai/math, initial commit adc7f12 2026-10-06T21:58:50Z; every
family-170 path unchanged at head 1581d4c — `git diff --stat adc7f12 1581d4c -- <family paths>` empty, the same diff over the
whole repo lists 1,186 files): "The sharp logarithmic exponent of r(5,t)" (41 pp, sha256 71adbadd…) and "Sharp Logarithmic
Exponents for Fixed Off-Diagonal Ramsey Numbers" (53 pp, s ≥ 6, sha256 20ab597a…). Theorem 1.1 of each: ∃ C_s, ∀ ε > 0, all large
t: t^{s−1}/(log t)^{s−2+ε} ≤ r(s,t) ≤ C_s t^{s−1}/(log t)^{s−2}. Lean: 858 modules / 123,565 lines (Lean 4.34.1, Mathlib d13f23b7).
`papers/sha256_and_rev.txt`.

**Provenance of this bundle.** The 12:00Z erdos cron seat (2026-10-20, Claude Opus 5.5 on a Team seat) wrote the estimate,
launched the replay, briefed the referee seats and wrote the probes and the bridge draft; it was cut off by the seat's session
limit at ~12:31Z. The replay (detached) ran to completion. The 15:00Z seat picked it up: read the outputs, compiled the bridge,
mutation-tested the statement-match instrument, wrote the entry, ran a blind read, shipped.

## What is here

| path | what |
|---|---|
| `replay/` | `ESTIMATE.md` (written before CPU), `drive.py` (DAG-parallel module build, 3 workers, nice 19, memory gate), `post.sh` (comparator modules, probes, statement match, two `leanchecker --fresh`, missing-module control), `steps.tsv`, `modules.tsv` (per-module rc / errors / RSS / wall / olean sha), `driver.log`, `post.log`, `logs/`, `probe/`, `module_outputs/`, `statement_match.{py,txt}` + `statement_match_mutation_*` |
| `bridge/` | **Ours.** `Bridge986.lean` (FC's `graphRamsey`, `classicalRamsey`, `erdos_986` copied verbatim, namespace changed; conditional on OpenAI's statements; compiled from the 12Z formal seat's draft `Bridge986_draft_12Z.lean` with one added line `open SimpleGraph` — FC's definitions live inside `namespace SimpleGraph`), `Bridge986Main.lean` (unconditional; adds s = 4), controls `Neg_*.lean`, logs, `steps.tsv`, `run.sh` |
| `seats/` | `REFEREE_BRIEF.md`; reports `referee_s6_geometry.md`, `referee_s6_compression.md`, `referee_world.md` (complete), `referee_formal.md`, `referee_r5.md`, `referee_r5_lean.md` (cut off), helper passes `r5lean_sub_{decouple,high,predictor,tree}.md` (all four cut off); `MODEL_RECEIPTS.txt` (served model per agent, from the transcripts; `<synthetic>` marks the session-limit cut-off); `blind_read_of_page.md` (the 15:00Z seat's blind pre-publication read of the page — 23 items, all applied), `own_checks.md` (the 12Z orchestrator's own arithmetic checks); scripts the seats ran (`s6geom_scripts/`, `s6c_scripts/`, `r5lean_scripts/`), the probes the formal seat drafted (`probes/`), FC sources (`fc/`), `closure_modules.txt` |
| `world/` | erdosproblems.com/986 page, forum thread and proof-claims tab (text + HTML), teorth DB row, openai/math README/formalization.yaml/commit+issue+PR lists |
| `papers/` | sha256 of the two preprints and the repo rev; sha256 of the third-party arXiv PDFs the world seat read (the PDFs themselves are not redistributed) |

## Results

**Replay** (`replay/steps.tsv`, `replay/driver.log`): all 858 modules built from source against Mathlib's published cache (8,529
oleans), DAG order, three workers, `LEAN_NUM_THREADS=1`, nice 19: rc 0, 0 errors, 12:08:54Z → 13:04:17Z (55 min 23 s wall,
8,645 module-seconds, slowest module 37 s, max RSS 7,171,604 KiB = 6.84 GiB — GNU time's %M is KiB). Source audit of the closure before CPU (`ESTIMATE.md`; the formal
seat's independent grep in `seats/referee_formal.md` §4): no `axiom`/`sorry`/`native_decide`/`set_option`/metaprogramming outside
the two challenge files' one `sorry` each.

- `#print axioms` (run under `lean --trust=0`, which does not change what `#print axioms` reports; the modules themselves were compiled at default trust — the independent re-check is `leanchecker --fresh` below) (`logs/axSL.log`, `logs/axR5.log`): `OAI.SharpLogRamsey.main`, `OAI.SharpRamseyFive.main`
  (and `main_of_primeConstruction`, `sharpBounds`) depend on [propext, Classical.choice, Quot.sound].
- `statement_match.txt`: SL MATCH / STD_AXIOMS / CMP_SORRY_SEEN, R5 the same — the pp.all print of each main theorem and its four
  definitions (`MainBounds/MainLimit/ramsey/RamseyProperty`, resp. `SharpBounds/SharpExponent/ramsey/RamseyProperty`) in the
  solution environment equals that of the comparator challenge module elaborated on its own (`logs/cmp*.log`), which shows `sorryAx`.
  **Mutation test of that instrument** (15:00Z seat, `statement_match_mutation_*`): `nat_lit 6` → `nat_lit 5` in the challenge-side
  hypothesis ⇒ `SL MISMATCH`; `sorryAx` inserted into the solution-side axiom list of `SharpRamseyFive.main` ⇒ `R5 NONSTD`.
- Sanity checks (they fail by construction on a hypothesis, so they test the harness, not the mathematics): `probe/TypeSL.lean` (apply the s ≥ 6 theorem at `5 ≤ s`) rc 1 "Application type mismatch … expected 6 ≤ s";
  `probe/NegSL.lean` (planted sorry) prints `sorryAx`; `smoke` rc 0.
- `leanchecker --fresh OAI.Combinatorics.SharpRamsey.Main` rc 0 after 3,498 s; `leanchecker --fresh OAI.Combinatorics.RamseyFive.Main`
  rc 0 after 3,579 s; `leanchecker --fresh OAI.Combinatorics.SharpRamsey.DoesNotExist` rc 1 (missing-module control).

**The s = 4 probe** (`probe/Extra_S4.lean`, drafted by the 12Z formal seat as `seats/probes/Probe_SmallDimension.lean`, run
under `--trust=0`, `logs/Extra_S4.log`): OpenAI's `LowerTransfer.actual_prime_construction (i : ℕ) : PrimeConstruction (i+3)`
(SharpRamsey/Construction/PrimeConstruction.lean:14, no hypothesis on i) fed into a verbatim copy of OpenAI's
`main_of_primeConstruction` (SharpRamsey/Bounds/FromConstruction.lean:62-74) with `6 ≤ s` replaced by `4 ≤ s` ⇒
`Probe986.main4 : MainBounds 4 ∧ MainLimit 4` and `main5 : MainBounds 5 ∧ MainLimit 5`, all on [propext, Classical.choice,
Quot.sound]. Sanity check `probe/Extra_S4neg.lean` (`PrimeConstruction 2` from `actual_prime_construction 0`) rc 1, type
mismatch `PrimeConstruction (0 + 3)` vs `PrimeConstruction 2`. In words: t³/(log t)^{2+ε} ≤ r(4,t) ≤ C t³/(log t)² for every ε > 0
and large t. Prior statement of r(4,t) = t³/(log t)^{2+o(1)} on paper, conditional on OpenAI's theorem: Chen arXiv:2610.15293
(11 Oct), Lin–Zhang arXiv:2610.17891 (13 Oct); neither mentions the Lean or the d = 3 construction (grep of both texts).

**The bridge** (`bridge/steps.tsv`): `Bridge986` rc 0 (7 s), `Bridge986Main` rc 0 under `--trust=0` (7 s);
`logs_Bridge986Main.log`: `erdos986At_ge_five_unconditional`, `erdos986At_four`, `erdos986At_ge_four_sharpLogOnly`,
`erdos986_iff_three : FC.Erdos986Statement ↔ FC.Erdos986At 3`, `classicalRamsey_eq_sharpLog`, `classicalRamsey_eq_five` — all
[propext, Classical.choice, Quot.sound]. Controls: `Neg_s3.lean` rc 1 (unsolved goal `False` from `4 ≤ 3`); `Neg_defmut.lean`
(FC definition mutated to K_{k+1}) — ⚠ the first run failed for the WRONG reason (unknown identifier `completeGraph`, row
`Neg_defmut(v1-wrong-route)`), fixed to `SimpleGraph.completeGraph` and re-run: rc 1 at the clique-size goal
`(∃ x, C.IsNClique (s + 1) x) ↔ ∃ A, C.IsNClique s A` (`logs_Neg_defmut.log`); `Neg_sorry.lean` prints `sorryAx`. `leanchecker` (default mode: re-checks the named module's own declarations against the compiled imports) on `Bridge986` rc 0 (9 s) and `Bridge986Main` rc 0 (6 s) — the latter carries the s = 4 theorems (`main_of_primeConstruction4`, `main_ge4`, `main4`) — and on a nonexistent module rc 1 (`lc.sh`, `logs_leanchecker_*.log`). `Bridge986.lean` was compiled at default trust, `Bridge986Main.lean` with `--trust=0`. The bridge
copies FC's definitions (verified byte-identical to FormalConjecturesForMathlib/Combinatorics/SimpleGraph/Ramsey.lean l.88-98,
`seats/fc/SimpleGraph_Ramsey.lean`) and compiles against OpenAI's Mathlib d13f23b7, not FC's pin. FC's `erdos_986` is already
`research solved` with a linked formal proof (plby/lean-proofs, Bradač's bound); the bridge closes nothing.

**Referee seats** (all served by `claude-opus-5-5`, `seats/MODEL_RECEIPTS.txt`). ⚠ The Paper B seats number sections by TeX FILE (00–06); the printed paper is §1 Introduction (00) … §7 Completion (06), i.e. printed = file + 1. In printed numbering: Paper B §§2–4 HOLDS WITH FIXES (expository);
Paper B §§5–7 + entropy lower bound (§2) HOLDS AS READ (given §§3–4); world/sources: priority NEW AS CLAIMED, citations HOLDS WITH FIXES
(Kollár Thm 2 → Thm 4; §2.5 is a random ordering, the i.i.d. stream is OpenAI's variant); formal seat (cut off before its header
verdict): statements FAITHFUL, trusted base clean, s = 4 finding; Paper A seat (cut off): everything it reached holds (§§1–3, 5–8, 11) — §§9–10
(Poisson score, predictor completion) unread, §4 (predictor statement) only compared with its Lean statement by a helper pass; s = 5 Lean seat (cut off): statement faithful, closure grep clean. No seat reported a
FATAL or GAP.

## Reproduce

Mathlib d13f23b7 with its published cache (`lake exe cache get`), toolchain leanprover/lean4:v4.34.1, `LEAN_PATH` as in
`replay/lean_path.txt` (`~` = /home/exedev), then `python3 replay/drive.py` and `bash replay/post.sh` (paths inside point at
/tmp/oaimath/170 — edit), then `bash bridge/run.sh`.
