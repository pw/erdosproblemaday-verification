# Problem 531: reader submission 8a7svk — F(5) ≥ 1514 (Atakan Akbaba)

Reviewed 2026-10-29. Verdict: **VERIFIED** (as a certificate: F(5) ≥ 1514). Review text: REVIEW_published_2026-10-29.md
(= /submission/8a7svk). Same convention as u2udx4 (../reader-f4-397): A a set of distinct positive integers, all
nonempty subset sums in {1,…,N} (sum(A) ≤ N) and of one colour.

- `submitted/k5_w1513.txt` — the witness, byte-identical to nakata-app/erdos-531-folkman @ d6009ad
  (SHA-256 b620e7c0c5f4de1d172a1952226b120c40bdddfe93279fe7842c9e4aaf7d6cc1; 1513 × {0,1} + newline). We ran none of
  the submitter's code.
- `checks/` — OUR checkers. `fs_grow.c` (bitset grower, any K ≤ 6: `fs_grow FILE K [N]`), `fs5_direct.c` (nested
  loops a<b<c<d<e, explicit new-sum tests; `fs5_direct FILE [N] [count]`), `fs_extend.py` (last week's set-based Python
  grower + partition-DP eligible count). Build: `gcc -O2 -o fs_grow fs_grow.c` (same for fs5_direct). Exit 0 = no
  monochromatic K-set.
- `controls/` — `run_controls.sh` → `controls.txt` (all-zero = DP at N = 40/80/120; 36 random colourings, both
  checkers identical; fs_extend.py at N = 500; the 1514 wall; F(2)/F(3) known values); `flip_one.sh` → `flips.tsv`
  (pos, fs_grow count, fs5_direct count) for all 1,513 single flips: 0 disagreements; 18 flips leave it valid.
- `referee/` — hostile Opus referee seat (blind to checks/ and controls/): REPORT.md (HOLDS), its own checkers in src/,
  its one-defect flip census `defect_census.txt` — equal to our flips.tsv on all 1,513 positions (absent = 0).
- `known/` — the [8] and [53] colourings from our July report (F(2) = 9, F(3) = 54).
- Eligible five-sets with sum ≤ 1513: 537,964,268,950 (partition DP).
