# #1186 — outside replay of Quana Labs' Lean proof (dreadpiratechan/erdos-1186 v1.0.0, 0b0155e)

- Build (Lean v4.27.0, Mathlib from its cache): exit 0, 19 Nov 2026 12:26Z (`steps.tsv`, `build_resume_tail.log`; the first
  build was stopped by our memory watchdog and resumed incrementally — see `steps.tsv`).
- `axioms_ours.lean` → `axioms_ours.log`: `Erdos1186Day.erdos_1186.variants.prs_conjecture : δ 3 = 117/2192` depends on
  [propext, Classical.choice, Quot.sound].
- Statement match (20 Nov): `statement_match.lean` copies FC's `monoCount`, `minMonoCount`, `δ` (FC main, commit 4beab72)
  into a fresh namespace and applies Quana's theorem to the fresh δ: accepted (`statement_match.log`). Control:
  `statement_match_control.lean` (k − 1 → k in the progression bound) is rejected with a type mismatch
  (`statement_match_control.log`).
- NOT YET DONE: a from-scratch kernel re-check of the closure. The v4.27.0 toolchain has no `leanchecker` binary (the 19 Nov
  step printed exit 1 for that reason, nothing was checked). We built lean4checker from leanprover/lean4checker tag
  v4.27.0 (`lean4checker_version.txt`; positive control `--fresh Init.Prelude` exit 0) and started
  `lean4checker --fresh Erdos.Proofs.P1186ExFinal` on 20 Nov 09:03Z (`checker.sh`). Its result will be added here and on the page.
