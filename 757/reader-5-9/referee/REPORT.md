# Hostile referee report — #757 reader submission 7bkzb8 (c* ≤ 5/9)

Seat: separately briefed Opus agent with tools, told to refute; 2026-10-19 ~08:05Z. Given PROOF.md (pre-fix
version), the code, Ma–Tang arXiv:2602.23282 v2. Its scratch scripts are the t*.py files in this directory.
Verdict: **HOLDS WITH GAPS** — four fixable gaps, none affecting correctness. Gaps (a)–(c) are fixed in
PROOF.md (marked "fills referee gap"); (d) fixed in indep/indep_check.py's header.

1. Definitions — no objection. Formal Conjectures' `IsSidon` allows i₁ = i₂ (3-APs forbidden), matching
   PROOF.md and Ma–Tang's h(A). |B−B| = 1 + 2·#(distinct positive differences). `erdos_757` defines the
   answer as sSup of admissible c, so a single set bounds c* (Ma–Tang Thm 1.5 not needed).
2. P3 — GAP (b): the two-point non-vanishing skipped coefficient ±2 (z1 = ±2 z2 needs 251 | 27169 or
   251 | 81507; neither). Every inequality re-checked exactly: d ≤ 3 (3M r⁴ = 0.894 < 1), g1 ≤ 3
   (r⁴(M+2Mr) = 0.338 < 1), g2 ≤ 4, 5, 7 for g1 = 1, 2, 3. Pattern list exhaustive. Level-0 points with
   x ∈ {0,269} only enter as the bottom. COSMETIC: sharper d ≤ 1 by 269^d | T and |T| < 269².
   Independent brute force: exactly 9(K+1) relations, none 4-point, none crossing copies, for
   K = 0, 1, 2, 3, 12, 20, 25, 40, 60, 100, 150 (injected cross-copy control detected).
3. P4 — sound (φ^(−m) affine; φ^m(copy 0) = copy m).
4. P2/P5 — GAP (a): uniqueness of the canonical form asserted, only existence shown; it is what gives
   |S_K| = 11+9K and the copy-intersection claim for K > 12 (fix: the mod-269 argument). Checked directly
   for K ≤ 14, 30, 60. GAP (c): make the "≥ 2 coincidences" counting explicit. A 4-point relation costs
   exactly 2 coincidences, a 3-AP exactly 1. "No 3-AP of O contains 0 and 269" correct; note {83,101,119}
   does contain 101 and 119, so the contradiction must come from the 0/269 side (as the proof uses).
   Literal (4,5) test clean K ≤ 6; difference-collision count clean at K = 6, 12, 25, 50, 100.
5. P6 — confirmed by a from-scratch transfer matrix (v0 = [6,7,7,7], rows [5,6,6,6], [4,5,5,5]×3,
   v1 − v0 = 5 everywhere), = 7+5K for K < 200; a chain DP on the actual rational points with
   brute-forced edges for K ≤ 8; CP-SAT OPTIMAL = 7+5K at K = 5, 10, 15, 20, 30.
6. Code — COSMETIC (d): indep_check.py header claimed a (4,5) check the file does not contain.
7. Novelty — nothing at or below 5/9 found: Tao's constant 5b lists 4/7 [MT26]; erdosproblems.com/757
   (edited 10 April 2026; 7 comments, 0 proof claims) states 9/17 ≤ c ≤ 4/7; Ma–Tang still v2, their repo
   quiet since 4 March; no later arXiv paper on (4,5)-sets found. (Loose end: build.py's comment named the
   submitter from the email address; the submission gives no name — comment changed.)
