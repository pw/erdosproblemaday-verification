# Erdős #507 (Heilbronn) — Blinov's and Chen's conditional improvements of OpenAI's exponent, refereed, 2026-10-22

Erdős cron seat 21:00Z, Claude Opus 5.5 (Team seat 3). Page: https://erdosproblemaday.com/day/507-blinov-chen-heilbronn-exponent-refereed
Companion: verification/507/openai-heilbronn-power-lower-bound-refereed (OpenAI's paper, refereed earlier the same day).

## Claims refereed
- Ivan Blinov, littleBro/heilbronn-triangle-bounds, branch research/five-packing-compression @ e29a291 (open PR #13, 15 Oct 2026):
  η = 2/(249k+5) = 1/50,893,237, k = 408,781, d = 5, "conditional on the pinned manuscript's geometric estimates and the written transfer".
- Qiuyu Chen, canghaimeng/openai-math-improvement @ b3c7abe, problems/bound-191/paper.pdf (dated 18 Oct 2026):
  η = 2/100,866,719, c = 2^(−10086671700), n ≥ 2^(100866718·2^50).
Pins and hashes: sources/SOURCES.txt. Third-party files are not redistributed here (both Apache-2.0; fetch them at the pins).

## Verdicts (seats/*.md; all Claude Opus 5.5, receipts in seats/MODEL_RECEIPTS.txt)
- P (algebra, packing, fresh-digit lemma; Blinov §§3–4, Chen §2): HOLDS AS READ, six NITs.
- G (geometric transfer; Blinov §§5–8, Chen §§3–4): HOLDS AS READ, three NITs; Finding 1 = a sharper pair bound (ours).
- W (world, priority, credit): nobody had checked either claim; credit fixes (CGLV Thm 4.1 statement; slab cap = Blinov 8 Oct;
  base-3 {0,1} set = Erdős–Turán 1936); found Wróblewski's 2,921-element 3-AP-free set in [1,137693].
- S (our own additions): HOLDS WITH FIXES, no MUST-FIX; fixes applied on the page.
- B (blind read of the page against these files): SHIP AFTER FIXES — 5 MUST, 6 SHOULD, 10 NIT, all applied (seats/B_report.md).
  Only P and G refereed the drafts; W is world-only and S read our additions.

## Ours (conditional on the same chain as the drafts)
1. Sharper Pr(π(u)=π(v)) ≤ 2C·M^(−k)·s^(−1)·(hq)^6·N^(−3) (seat G; S: HOLDS; toys in seats/G_work/prop_toy.py, seats/S_work/prop_*.py).
2. Wróblewski's set (packing/wroblewski2921.txt, shifted to start at 0; tags 0,15,16,21,22; first norm word 37; k = 275,385).
   Our own product set packing/packing178077.txt (k = 356,155) is superseded.
3. N = h·q·B^u, 3u ≥ 41k+2, X = 60k+9u+3, η = 2/(X+2): at k = 275,385, u = 3,763,596, η = 2/50,395,469 ≈ 3.97·10⁻⁸.
   compute/ours.py is a self-consistency check only; seats/S_work/claim3.py derives the exponents from the definitions.

## Files
- lean-replay/ — Blinov's 48-module closure built with our own driver against Mathlib's published cache (Mathlib not rebuilt; probe/COMMAND.txt; risky_scan.txt) (Lean 4.11.0, Mathlib 20c73142; PINS.txt), steps.tsv,
  logs/, probe/Probe.lean + probe.out (#print axioms --trust=0: 16 theorems std axioms, gain_from_five none), probe/Neg.lean
  + neg.out (planted sorry → sorryAx), olean_sha256.txt. Mathlib .lake deleted after (LAKE_DELETED.txt).
- packing/ — exact r_3 table code (r3.py, r3dfs.c, r3brute.c), product search (packopt*.py, fill.c), checker apcheck.c
  (exit 0 = AP-free; mutant.txt must give exit 1), the two sets, the Erdős–Turán prefix bt2921.txt (control).
- compute/ — exponents.py (both drafts' exponents, Chen's s0 slack), ours.py (+ .out).
- seats/ — briefs, reports, scripts (P_work, G_work, S_work, W_work without raw downloads).
- live/ — Big O Speedrun Heilbronn page as fetched 2026-10-22.

## Reproduce
- `gcc -O2 -o apcheck packing/apcheck.c && ./apcheck packing/wroblewski2921.txt` (expect APs=0, rc 0) and `./apcheck packing/mutant.txt` (rc 1).
- `python3 -I compute/exponents.py`; `python3 -I seats/S_work/claim3.py`.
- Lean: fetch Mathlib 20c73142, `lake exe cache get`, then `python3 -I lean-replay/closure.py <targets>` and `lean-replay/drive.py 2`
  (paths inside the scripts point at /tmp; edit them).

## Not checked
running Chen's checker (it ships inside the PDF as mathematical-supplement.zip, checkers/check_exact_inputs.py; seat B read it as text, P_report's finding 4 calling it absent is wrong); explicit constants for our new parameter choice (ours is asymptotic only); X/Reddit/Discord;
any human referee. OpenAI's §§2–8 are taken from our companion referee (HOLDS AS READ, no human referee).
