# Erdős 172 — audit of OpenAI's "Monochromatic finite sums and products in the positive integers" (23 Sept 2026)

**Claim under audit (theirs, not ours):** Hindman's finite sums-and-products conjecture — for every finite colouring of ℕ
and every m there is an m-element set A ⊂ ℕ with FS(A) ∪ FP(A) monochromatic (Theorem 1.1, with a separation clause).
This closes the headline question of erdosproblems.com/172 under every reading of "sums and products of distinct
elements". Paper: openai/math, family 164; SHA-256 in `paper.sha256`. **Nothing mathematical in this directory is ours.**

## The chain of evidence, strongest first

1. **Kernel-checked formalization by a third party** — github.com/cadamcat/hindman-sums-products-lean4 (Yao Xu; v1.0.0
   7 Oct, HEAD `3064cac` 11 Oct). Statement = the conjecture (no separation clause); `audit/Erdos172.lean` derives the
   Formal Conjectures statement. Source audit in `lean_audit.md`: one `sorry` (the Comparator placeholder), no axioms.
   The Alignment Principle (§6–8 of the paper) is imported from OpenAI's own sorry-free library; Prediction (§3–5) is
   re-proved with Kravitz–Kuca–Leng concatenation and OpenAI's cyclic inverse theorem in place of Tao–Ziegler / GTZ.
   Author's report: `#print axioms` = propext, Classical.choice, Quot.sound; `leanchecker --fresh` and nanoda replays.
2. **Our independent replay** — `replay/` (build log, per-step exit codes, the `#print axioms` output under `--trust=0`),
   produced on exe.dev from the pinned sources in a scrubbed environment. Result: 11471 jobs built from the pinned sources at nice 19 on four threads in 8 h 21 min; `#print axioms` under `--trust=0` printed `[propext, Classical.choice, Quot.sound]`; `audit/NonVacuity.lean` ran clean. Caveat (found 11 Oct by the #181 Lean-audit seat): Lean 4.34's `--trust=0` does not re-check imported modules, so this run kernel-checked everything compiled from source here (the proof and OpenAI's library); Mathlib's `.olean`s came from the official cache. The `leanchecker --fresh HindmanSumsProducts.Main` pass over the full import closure (relaunched 2026-10-12T03:05:52Z with the toolchain `bin` on PATH, after the #181 driver's last step died rc=127 on a missing `lake` launcher) **exited 0 after 13,271 s (3 h 41 min)** — `replay/leanchecker_fresh.log` holds only Lake 'has local changes' warnings, no error line; `replay/leanchecker_fresh.rc` has the step line. Controls for reading that silence as a pass (`replay/leanchecker_controls.{sh,log}`, 2026-10-12, same build): NEG — a non-existent module exits 1 with 'Could not find any oleans'; POS — stopped by us (SIGTERM at 28 GB RSS with 16 GB free and no swap on a loaded box; see the rc in the log); the same leanchecker binary's POS control on the #181 and #1083 builds (`verification/181/openai-referee/replay/leanchecker_controls.log`, `/tmp/oaimath/166/lean-build/leanchecker_controls.log` → #1083 bundle) exited 0 printing nothing. Residual: rerun the POS control here when the box is quiet. Note the driver's `lake build -j 4` step exited 1 at once (`-j` is not a flag in this Lake); the real build ran inside `scripts/verify.sh`, see `build.log`.
3. **Hostile machine referee of the paper as written** — `referee_report.md` (Opus, tools, briefed to refute, every
   objection quoting the paper with line numbers of `paper.txt`-style extraction). Verdict: **HOLDS AS READ** — no FATAL, no REPAIRABLE; two COSMETIC (the Cauchy–Schwarz procedure described for (5.13) is not the one that yields it, though a one-step argument gives the same inequality with the same exponent; ⊂ written for ⊆) + one attribution note (Lemma 2.5's ordering is not Alweiss's; the proof stands alone). Skim list stated. Four further sectioned seats run by the parallel session (`seats/`: deduction / prediction / alignment / citations) all read HOLDS AS READ.
4. **Primary-source checks** — `sources.md`: verbatim statements, from the current arXiv versions, of Zorin-Kranich
   Cor 3.7, Tao–Ziegler Thm 1.23, the GTZ erratum, the Green–Tao erratum (equal-sides case), Alweiss Thm 1.3 / Prop 4.1.
5. **Exact controls** — `controls.py` / `controls.out`: identity (8.2) exhaustive for n ≤ 8; Corollary 1.2's separation
   argument on 3,000 random separated sets, with a negative control (unseparated sets) that produces collisions.

## Labels
Theorem: (d) computer-assisted — a Lean 4 kernel proof exists, and our own from-source replay printed the same three standard axioms (leanchecker --fresh over the whole import closure, Mathlib's cache included, exited 0 on 2026-10-12 06:47Z). Paper as written: (c) plausible/unverified by a human — five tool-equipped machine seats, each briefed to refute, each HOLDS AS READ with only cosmetic objections.
§2 deduction, citation checks, controls: (a)/(b), ours.

## Reproduce
- Controls: `python3 controls.py` (seconds).
- Replay: `git clone https://github.com/cadamcat/hindman-sums-products-lean4 && cd hindman-sums-products-lean4 &&
  lake update; scripts/apply-oai-patches.sh && lake exe cache get && lake build && LEAN_NUM_THREADS=4 scripts/verify.sh`
  (our exact driver: `replay/run.sh`; ~35 min on 32 cores, hours on a loaded 16-core box). Expected final line:
  `PASS: all axioms are in the permitted set.`
- Sources: fetch the arXiv ids in `sources.md`, `pdftotext -layout`, grep the quoted statements.

## World state at audit time (2026-10-11)
teorth DB: 172 OPEN (lu 2025-08-31). OpenAI CONTENTS.md: family 164, no Lean link; `lean/formalization.yaml` does not
list the paper. Bloom's 8 Oct post lists #172 among the 25 Erdős claims, no endorsement. Open Proof Network erdos-172:
open ("AlphaProof Nexus, Feb 2026: not solved"). No independent human proof found on arXiv (searched 11 Oct).
