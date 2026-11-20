# Erdős #488 — reader submission dv8gfk (Alicien B., 19 Nov 2026): outside replay and review

**Claim.** (1) An elementary disproof of Formal Conjectures' `erdos_488`: A = the 256-smooth integers in [x, 2x),
x = 2^(8j) for some 1 ≤ j ≤ 3500 (pigeonhole), n = 256x, m = (2n)!·Q. (2) The inequality holds whenever |A| ≤ 2.
Both in Lean (github.com/Alicienn/erdos-488-lean, commit 96b5360; paper aiXiv 2611.02020, 19 Nov 2026).

**Verdict (20 Nov 2026): VERIFIED — correct, not new.** Theorem 1 is Gessel's 5 Sep 2026 argument with different
constants; Theorem 2 was already proved (Chojecki, 20 Mar 2026, up to three generators) and kernel-checked on Jig
(statements 2, 4, 7, 11, 1 Sep 2026, up to four). See `referee_report.md`, `world_report.md`.

## What we ran
- `lean/build.sh`: `lake exe cache get` + `lake build` (Lean 4.35.0-rc2, Mathlib v4.35.0-rc2 = 0653561, `lean/env.txt`)
  → exit 0 (`lean/build_tail.log`); `CheckAxioms.lean` → both theorems depend on [propext, Classical.choice,
  Quot.sound] (`lean/check_axioms.log`).
- FC bridge: `lean/fc_bridge.lean` pastes FC's `erdos_488` body (main, last changed 7db2ea3, 14 Oct; copy in
  `lean/fc_488_main_7db2ea3.lean`) as a Prop in a fresh namespace and proves its negation with the submitter's theorem
  → accepted, standard axioms. Controls: factor 2 → 3 (`fc_bridge_control_factor3.lean`) REJECTED (type mismatch);
  planted sorry (`fc_bridge_control_sorry.lean`) shows `sorryAx`. Elaborated with the repo's Mathlib, not inside an FC
  checkout.
- Second kernel: `lake env leanexport Solution -- Erdos488.not_erdos_488 Erdos488.erdos_488_card_le_two` (lean4export
  3.1.0; 856,222 lines, 45 MB, sha256 in `nanoda/export.sha256`) checked by nanoda_bin 0.4.17 (`nanoda/cfg.json`,
  permitted axioms propext/Classical.choice/Quot.sound): "Checked 10743 declarations with no typechecker errors"
  (`nanoda/nanoda.log`). Controls: Quot.sound not permitted → "unpermitted axiom" error (`nanoda_ctrl_axiom.log`);
  `nanoda/tamper.py` gives `erdos_488_card_le_two` the type of `not_erdos_488` → type checker panics on a failed
  definitional-equality assertion, exit 101 (`nanoda_ctrl_tamper.log`).
- `lean/checker.sh`: `leanchecker --fresh Solution` (whole closure, Mathlib included). Missing-module control exits 1.
  Its result is recorded in `lean/steps.tsv` when it finishes.
- `numbers_claude.log`: our exact recomputation of 54 primes, 5^3500·28009^53 < 6^3500, 216Q < 1280φ(Q).
- `smallA/smallA3.c`: exact decision procedure over every primitive A (sizes 1–5) — no violation for size 3 with
  max A ≤ 200 (1,169,324 sets), size 4 ≤ 70 (576,700), size 5 ≤ 40 (219,826); with 2 replaced by 19/10 it reports
  violations (positive control). `smallA/smallA_runs.log`. Method in the file header (periodicity + tail bound
  |B(y) − d·y| < 2^k − 1).
- `referee/ref_*.py`: the referee seat's scripts (Theorem 2 brute force to 400, small analogues, statement diff).
