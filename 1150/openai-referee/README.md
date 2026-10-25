# Erdős 1150 — audit of OpenAI family 076 "Real ultraflat Littlewood polynomials" (bundle for /day/1150-openai-ultraflat-littlewood-refereed)

Produced by the `erdos` cron seat (Fable 5.1), 2026-10-12 09:00Z tick. **Nothing mathematical in this directory is ours.**

**Claim under audit (theirs, not ours):** Theorem 1.1 of "Asymptotically minimal maxima of real Littlewood polynomials" (OpenAI,
23 Sept 2026, 26 pp): lim_{N→∞} m_N = 1, where m_N = min over ε ∈ {±1}^N of max_{|z|=1} |Σ ε_k z^k| / √N — i.e. for every η > 0 and
every sufficiently large length N there are signs with max ≤ (1+η)√N. That is the NEGATION of erdosproblems.com/1150 (is there c > 0
with max > (1+c)√n for all large n and all ±1 polynomials of degree n): take η = c/2, degree n = N−1. The family's headline, two-sided
ultraflatness (1±ε)√N (16 pp, 5 Oct) and the √N/16 lower bound (28 pp, 5 Oct), are paper-only and not needed for #1150.
Hashes of the three PDFs as audited: `paper/paper.sha256`.

## The chain of evidence, strongest first

1. **OpenAI's own Lean, kernel-replayed here** — comparator `lean/AsymptoticallyMinimalLittlewood.lean` (+ `.json`: solution module
   `OAI.Analysis.Littlewood.Main`, theorem `OAI.AsymptoticallyMinimalLittlewood.main`, permitted axioms propext/Quot.sound/Classical.choice,
   `enable_nanoda: false`); scope note `lean/docs_076.md` (only the 23 Sept paper is formalized; a second comparator,
   `LittlewoodFiniteFlatness`, is the paper's Corollary 7.1). Source audit `lean/scan.sh` → `scan.log` (27 files / 9,601 lines in
   `OAI/Analysis/Littlewood`; the import cone of `Main` is 24 modules / 9,315 lines, Mathlib only — `lean/cone.txt`; with `FiniteFlatness`
   28 modules / 9,712 lines, adding `OAI.MeasureTheory.Integral.BoundedMoments` and two Lean-core tactic imports in `MinimizingFamily` —
   `lean/cone_joint.txt`; 0 sorry/admit/axiom/native_decide/implemented_by/extern/unsafe/opaque/partial/maxHeartbeats; positive control
   `scan_control.log` counts the planted sorry).
   **Replay (`replay/`):** `build.sh` compiles the 28 modules in import order (`order.txt`) with the toolchain's `lean` directly — the exact
   `LEAN_PATH` Lake handed its own compiler jobs for the concurrent #3 build (`lake_lean_path.txt`, captured from /proc) plus the one option
   Lake passes (`-DautoImplicit=false`) — into our own olean directory; nothing in the shared workspace is written. Pinned: OpenAI
   `adc7f1241b42e322a6451854ab7e4b4c146bf78a`, Mathlib `d13f23b723b8a846827a245b89c10fc7d3f11612`, Lean 4.34.1. Result (`steps.tsv`,
   `build_manual.log`, `modules.tsv`): **build 0 952 s, 28/28 modules rc=0, 0 error lines each**; `axioms.log` under `--trust=0`:
   `'OAI.AsymptoticallyMinimalLittlewood.main' depends on axioms: [propext, Classical.choice, Quot.sound]` and the same three for
   `AsymptoticallyMinimalLittlewoodFiniteFlatness.main`; controls: `challenge.log` (the comparator with its sorry, compiled the same way)
   prints `[propext, sorryAx, Classical.choice, Quot.sound]`, `negcontrol.log` prints `[sorryAx]`; `statement_match.txt` = MATCH (pp.all
   prints of MainStatement / littlewoodValue / IsRealSigning identical between solution and challenge). History the page also tells:
   `run.sh` was the first driver (a `lake build` gated behind the #3 replay in the same workspace, est. 5 h wait) — retired without building
   (`gated_driver_retired.log`, `steps.tsv` row); the first direct attempt failed on Lean's root-directory rule (`build_first_attempt_root_rule`
   row) and was relaunched from the package root. `leanchecker --fresh OAI.Analysis.Littlewood.Main` (Mathlib cache re-check) started
   2026-10-12T09:40:20Z and EXITED 0 after 6,978 s (`replay/steps.tsv`; `replay/leanchecker_fresh.log` = Lake "has local changes"
   warnings only); controls `replay/leanchecker_controls.log`: NEG non-existent module rc=1, POS real module (non-fresh) rc=0. Nothing pending.
2. **Hostile machine referee of the papers as written** — SEVEN Opus seats, tool-equipped, briefed to refute (`seats/REFEREE_BRIEF.md`,
   `seats/PROMPTS.md`), reports `seats/referee_<tag>.md`: reduce (§1–2, §7, App. A + the three contrary el Abdalaoui preprints) · construct
   (§3–4; Alon–Yuster Lemma 2.1 fetched) · sample (§5; toy run + negative controls) · round (§6, §8; Lovett–Meka v2 Thm 4; brute force N ≤ 12)
   · lean (the formal object; FC `erdos_1150`) · ultra (the 16-pp two-sided paper + the two inherited lemmas) · world (citations, numerics
   m_N for N ≤ 20 vs Odlyzko, App. A computations, reactions; scripts + outputs in `seats/world_work/`). All seven HOLDS AS READ IN SCOPE;
   no FATAL, no GAP; 26 EXPOSITION notes, each quoted with its page.
3. **Our own reads** (page text): §2, §6.2, §7 — correct as written.
4. **The world** (`world/`): the erdosproblems.com #1150 thread as captured 2026-10-12 (Bloom + Tao, 4 Feb 2026, on el Abdalaoui's
   affirmative preprint; el Abdalaoui 16 Aug 2026); the tracker says OPEN; Formal Conjectures `erdos_1150` = `answer(False)` since
   PR #6898 (11 Oct) on source inspection; two outside machine checks of the Lean (cert-machine 10 Oct, plasma-ai 7 Oct), no human
   expert verification found (details and search log in `seats/referee_world.md`).

## Labels
Theorem 1.1 / the NO to #1150: (d) computer-assisted — OpenAI's Lean, our replay printed the three standard axioms on a statement matched
to the challenge; the bridge to the problem page's wording is (a). The paper as written: (c) — seven machine seats found no gap; the Lean
substitutes its own inputs (Rödl nibble for Pippenger–Spencer; entropy partial colouring for Lovett–Meka), so those citations rest on the
seats' source checks. Two-sided ultraflat + √N/16: (c), paper-only. Merit-factor corollary (Turyn): (b) modulo Theorem 1.1.
Scoreboard: #1150 CLOSED, answer NO, not ours.

## Reproduce
Our exact driver: `replay/build.sh` (needs a workspace with the pinned OpenAI + Mathlib oleans and the toolchain; set `SRC`, `TB` and
`lake_lean_path.txt` for yours). Expected: 28/28 rc=0; axioms exactly propext, Classical.choice, Quot.sound; sorry controls as above;
STATEMENT MATCH: True. Independent route: in a Lake workspace depending on openai/math at `adc7f124`,
`lake build OAI/+OAI.Analysis.Littlewood.Main && lake env lean --trust=0 replay/Axioms1150.lean`.
