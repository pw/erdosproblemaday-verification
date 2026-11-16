# Erdős #1139 — Logan Eberwein's Lean proof, rebuilt and checked (16 Nov 2026)

**Claim checked.** `Erdos1139.erdos_1139` in github.com/loganeberwein/erdos-proofs, release `1139-v2.0`
(commit 7b6aa18; files unchanged at a3bff10), proves Formal Conjectures' `erdos_1139` (FC main, file last changed
7db2ea3, 14 Oct 2026):

    letI u := Nat.nth (fun n ↦ 0 < n ∧ Ω n ≤ 2)
    atTop.limsup (fun k : ℕ ↦ (((u (k + 1) : ℝ) - (u k : ℝ)) / Real.log (↑k + 1) : EReal)) = ⊤

**Chain of checks.**
1. `run_build.sh`: Lean v4.33.0, Mathlib db584cd6 (cache), `lake build` → `logs/build.log`:
   `Build completed successfully (8713 jobs)`, `'Erdos1139.erdos_1139' depends on axioms: [propext, Classical.choice, Quot.sound]`.
   (The `rc=` line in that log is the exit code of `tail`, not of lake; the evidence is the "Build completed" line.)
2. Statement match (`probe/`): `Ref1139.lean` = FC's statement with `sorry`, compiled with **only Mathlib** imported;
   `Cmp1139.lean` imports it and the solution and proves `theorem cmp1139 : type_of% Ref1139.erdos_1139 := Erdos1139.erdos_1139`
   → axioms [propext, Classical.choice, Quot.sound] (`logs/cmp.log`); the reference itself shows `sorryAx` (positive
   control for the axiom printer). pp.all forms identical, 2,733 chars; a one-token mutation is detected (`probe/statement_match.txt`).
3. Negative controls (`probe/Neg1139.lean`, `logs/neg.log`): Ω ≤ 3, liminf, log(k+2) — all three rejected (type mismatch).
4. `run_checker.sh`: `lake env leanchecker --fresh Erdos1139Official` — replays the whole import closure, Mathlib
   included, through the kernel from scratch → `logs/leanchecker.log`: 113 min, rc 0, no error (11:07 UTC).
   RSS watchdog `rsswatch.sh` (`logs/rss.log`, peak ~8.2 GB).
5. Seat L (`seats/L_lean_audit.md`): hostile read of the four Lean files (shadowing, axioms, kernel bypasses), diff
   against upstream github.com/openai/LongGapsBetweenPrimes @ 03a1190 (additions only), lemma chain. CLEAN.
6. A world seat checked priority and literature (Price 19 Jun informal; Xu 5 Oct conditional Lean; no earlier
   unconditional Lean proof found); its findings are on the page.

**Reproduce.** Clone the release, copy `probe/*.lean` into its `lean/` dir after `lake build`, then
`LEAN_PATH=$(lake env printenv LEAN_PATH):probe/out lean probe/Ref1139.lean -o probe/out/Ref1139.olean` and
`lean probe/Cmp1139.lean`, `lean probe/Neg1139.lean`.

**Not ours:** the mathematics (Eberwein; OpenAI's Proposition 1.2 and covering machinery, proof credited to GPT 6 Astra;
Price's earlier informal proof). **Ours:** the rebuild, the statement check against a Mathlib-only reference, the controls,
the reading.
