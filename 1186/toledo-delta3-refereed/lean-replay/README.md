# #1186 — outside replay of Quana Labs' Lean proof (dreadpiratechan/erdos-1186 v1.0.0, 0b0155e)

- Build (Lean v4.27.0, Mathlib from its cache): exit 0, 19 Nov 2026 12:26Z (`steps.tsv`, `build_resume_tail.log`; the first
  build was stopped by our memory watchdog and resumed incrementally — see `steps.tsv`).
- `axioms_ours.lean` → `axioms_ours.log`: `Erdos1186Day.erdos_1186.variants.prs_conjecture : δ 3 = 117/2192` depends on
  [propext, Classical.choice, Quot.sound].
- Statement match (20 Nov): `statement_match.lean` copies FC's `monoCount`, `minMonoCount`, `δ` (FC main, commit 4beab72)
  into a fresh namespace and applies Quana's theorem to the fresh δ: accepted (`statement_match.log`). Control:
  `statement_match_control.lean` (k − 1 → k in the progression bound) is rejected with a type mismatch
  (`statement_match_control.log`).
- From-scratch kernel re-check (21 Nov): DONE, PASSED. The v4.27.0 toolchain has no `leanchecker` binary (the 19 Nov
  step printed exit 1 for that reason; nothing was checked then). We built lean4checker from leanprover/lean4checker tag
  v4.27.0 (`lean4checker_version.txt`: 7df74851c95d9bd1bbb8fc9b51aeb291304faaf6) and ran (`checker.sh`)
  `lean4checker --fresh Erdos.Proofs.P1186ExFinal`, which replays the module's whole environment (every imported
  declaration, Mathlib's included) into a fresh kernel: started 20 Nov 09:03Z, ended 14:28Z with exit 0 and NO error text (325 min;
  `lean4checker_fresh.log`, `steps.tsv`; the memory watchdog never fired on this run, `watchdog.log`).
- Controls for the checker: positive `--fresh Init.Prelude` exit 0 (`lean4checker_control.log`). Negative
  (`negative-control/`): `NegCtl/Bad.lean` adds `NegCtl.bad : False` with value `True.intro` through `addDecl` under
  `set_option debug.skipKernelTC true`; it builds and `#print axioms` reports no axioms; lean4checker REJECTS it
  ("(kernel) declaration type mismatch", exit 1, `ctl_bad_nonfresh.log`) and accepts the honest `NegCtl/Good.lean`
  (exit 0). Under `--fresh` (`ctl_bad_fresh.log`, 38 min, the whole Lean core replayed first) it PRINTS the same
  kernel error ("declaration type mismatch") but EXITS 0. So in --fresh mode the exit code cannot go red: the
  instrument is the log text. `lean4checker_fresh.log` for Quana's module contains no error, exception or mismatch
  line (6 lines: the module search, then the timing). `ctl_good_fresh.log`: the honest file under --fresh: no error text, exit 0 (54 min).
- One kernel only: the build and the replay both use Lean's kernel; no second kernel (nanoda) was run here (v4.27.0
  ships no `leanexport`).
