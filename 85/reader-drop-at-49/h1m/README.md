# H1 miss-matrix cube (2026-10-19, 21:00Z erdos seat) — our derivation reproduces the authors' 13,351-orbit inventory

Setting and notation: `../h1k/README.md` (reduction §1, Lemma D §2, five cases §3 — all refereed HOLDS AS READ).
H = G[F] on the 40 far vertices, 6-regular, C4-free, 8 blocks of 5 (block X = far neighbours of u_X), pairs X ~ X',
no edges between paired blocks, every vertex has <= 1 neighbour in each block (own block included). Blocks 0..7, pairs
(0,1),(2,3),(4,5),(6,7). Case j: pairs 0..j-1 have e = (2,2), pairs j..3 have e = (2,1) (first block of a pair has 2).
Every block's internal matching is fixed: local edges (0,1)(2,3) for e = 2, (0,1) for e = 1.

## 1. The miss matrix (label (a))
Each far z has 7 available blocks (all but its partner block) and degree 6, <= 1 neighbour per block, so it misses
exactly one available block, mu(z) (h1k Lemma D step 1). An unmatched z (no neighbour in its own block X) has
mu(z) = X; a matched z has mu(z) outside {X, X'}.

For distinct non-paired blocks X, Y put M[X][Y] = #{z in X : mu(z) = Y}.
- **M1.** z in X has a neighbour in Y iff mu(z) != Y, and then exactly one. So the H-edges between X and Y form a
  matching of size N[X][Y] = 5 - M[X][Y].
- **M2.** N[X][Y] = N[Y][X] (the same edge set) => **M is symmetric**.
- **M3.** Row sums: sum over Y of M[X][Y] = #matched vertices of X = 2 e(X) (4 or 2).
- **M4 (Lemma D in M form).** For non-paired X != Y: q(X,Y) = N[X'][Y] + N[X][Y'] - 5 = 5 - M[X'][Y] - M[X][Y'] >= 0,
  i.e. **M[X'][Y] + M[X][Y'] <= 5**. (q = #pairs (a,b) in X x Y with no common neighbour; h1k Lemma D.)

So every H in case j determines a symmetric non-negative integer 8x8 matrix M, zero on the diagonal and on the four
paired positions, with row sums 2e(X) and M4. The case's block group G_j (permute the (2,2) pairs with an optional swap
inside each, permute the (2,1) pairs with orientation fixed; |G_j| = 384, 48, 16, 12, 24 for j = 4..0) maps the case's
H's to the case's H's (it preserves e, the pairing and the fixed internal edges) and acts on M by relabelling blocks.

## 2. Enumeration (two programs)
| case j | matrices (with M4) | classes under G_j | matrices without M4 | orbits without M4 |
|---|---|---|---|---|
| 0 | 16,677 | 839 | 16,692 | 842 |
| 1 | 31,458 | 2,693 | 31,512 | 2,700 |
| 2 | 69,321 | 4,717 | 70,070 | 4,801 |
| 3 | 167,748 | 3,617 | 169,668 | 3,662 |
| 4 | 442,518 | 1,485 | 449,358 | 1,536 |
| total | | **13,351** | | 13,541 |
`menum.py` (Python, entry-by-entry recursion over the 24 free entries in row-major order; orbit closure asserted;
orbit x stabiliser = |G_j| asserted; orbit sizes sum to the matrix count asserted) and `mcount.c` (C, row by row over
columns in DESCENDING order, M4 checked only at complete matrices; `mcount_nod` = without M4) agree on every matrix
count. Classes: `classes_all.tsv` (j, 24 upper-triangle entries of the canonical rep in menum.PAIRS order, orbit size,
|stabiliser|).

**Match with the submission (row level; h1m referee, `referee/REPORT.md` (c)).** The authors' table entry
`highBranchMissCount(s,t) = #{a in branch s : N(a) ∩ branch t = ∅}` (BranchDeficitSymmetry.lean:83) is our M[s][t];
their capacity filter T[c][j^1] + T[j][c^1] <= 5 is M4 by symmetry; their CapacityCover's
`#commonPairs = 20 + T[a][b^1] + T[b][a^1]` is our 25 − q. Under an explicit relabelling (their profile a puts the (1,2)
pairs first with the even block at e = 1; profile p ↔ our case 4 − p) `referee/rowmatch_authors.py` finds their capacity
test and our M4 agreeing on all 13,541 raw rows, their 13,351 kept rows EQUAL to `classes_all.tsv` as sets case by
case, and their 190 removed rows exactly the M4 failures. So the inventory and the filter are the same objects — and
M1–M4 derive both from the graph in a paragraph, without their Lean. (The first referee's recount of their inventory,
`../referee/REPORT.md`, gave the same per-profile numbers.) The referee's own enumerator (2x2 blocks per pair of pairs,
counting DP, Burnside, groups by brute force over S8) agrees on every count and validates every row of classes_all.tsv.

## 3. One cell = one SAT call (`h1mcell.py`)
`h1mcell.py` = the refereed `../h1k/h1cube2.py` plus additions marked [M]:
- `--M <24 entries>`: exact cardinality #edges(X,Y) = 5 - M[X][Y] for all 24 non-paired pairs (seqcounter);
  row sums asserted against the case.
- pair-level SB restricted to the STABILISER of M in G_j (a lex-leader over a block map that moves the cell to another
  cell would be unsound inside a cube); within-block transposition SB unchanged (it fixes every block, hence M).
- `--edgeswap`: lex-leader (fsenc.add_perm_sb, the same row-major order as the pair SB) for (0 2)(1 3) inside each
  e = 2 block — the third generator of the block's internal group, which h1cube2 does not break. Preserves the fixed
  internal edges, every block, M, slots and PH.
- SAT recheck extended: cell membership (every N[X][Y]), edge-swap lex order, plus h1cube2's checks.
- `--cov`, `--mu`: experimental, NOT used for any result (cov = codegree-coverage counts, slowed Kissat 85 -> 140 s on
  cell #200; mu = second cube level fixing every mu(z): one of 16 sub-cells alone took 43 s, a net loss).
- `subtest.py` (experiment, NOT a result): cell #200 restricted to blocks {0..5} (degrees <=, exact cross counts and
  C4 inside the subset) is SAT at once; {0..6} is UNKNOWN at 300 s (harder than the full cell, which has PH/slots/exact
  degrees). The obstruction is global — no sub-pattern shortcut for the cube.
Coverage of the cube: every H in case j has an M; some g in G_j maps M to its class representative; g maps H to an H'
in the representative's cell (same case, same fixed internal edges). H' itself need not satisfy the cell's lex-leader
clauses, but the lex-least member of its orbit under the cell group Γ_c (within-block transpositions + edge swaps +
Stab(M)) does — because every SB clause is a lex-leader under ONE variable order and ONE direction (referee
`sb_order_check.py`, with three mutated orders failing). So H1 is empty iff all 13,351 cells are UNSAT (h1k §1 (i)–(iii)
for the iff; referee `coverage_e2e.py`: 11/11 graphs from whole-case models land SAT in their own cell, UNSAT in another).

## 4. Evidence (Kissat 4.0.4, nice 19, flags --pairsb --slots --ph --edgeswap, box at load ~14-18)
- Random sample, seed 20261019 (`sample_cells.sh`, single solver, no proof; the j = 0..3 draw came from a first
  enumeration run whose j = 3 output was truncated at 3,495 of 3,617 classes, so that draw is uniform over a prefix —
  the cells themselves are in classes_all.tsv; exact lists in runs/sample_list*.txt): 5 cells per case j = 0..3 + 6 for j = 4
  -> **26/26 UNSAT**, 19-167 s per cell incl. ~3 s encoding, mean 54 s (`runs/sample_j0-3.tsv`, `runs/sample.tsv`).
- First probes (j = 0, no edgeswap): 4/4 UNSAT, 3 timed at 42-150 s (`runs/first_probes.txt`).
- Positive controls `--drop-c4` (C4 clauses removed, everything else on) on three cells (j = 0, 2, 4): SAT with clean
  rechecks (`runs/dropc4_controls.out`) — but those cells have 0, 0 and 1 pair permutations, so they test little of the
  pair SB. The discriminating ones: the j = 4 cell with |Stab| = 128 (referee): SAT, pair-lex 0/127 with the clauses,
  8/127 with `--check-only` (clauses withheld); same cell with C4 on: UNSAT under Kissat 36.6 s and CaDiCaL 19.0 s
  (`referee/dropc4_stab128*.out`, `referee/stab128_solvers.out`). Edge-swap mutation: 0 violations with the clauses,
  5 with `--es-check-only` (`runs/edgeswap_mutation.out`). So THESE cells are not vacuous and the rechecks can fail; it
  says nothing about the other 13,348 cells beyond what the sample does.
- For scale: the authors' own orbit CNFs (12-orbit sample, our build of their emitter, hash-identical) took 142-13,660 s
  each under CaDiCaL (one census orbit UNKNOWN at 4 h under Kissat).

## 5. Cost of closing H1 independently (estimate written BEFORE any campaign)
Sample means, n = 26 Kissat cells (5–6 per case; nice 19, load 14–18, wall time incl. ~3 s encoding): per case
50.1 / 62.6 / 45.7 / 41.3 / 67.5 s (j = 0..4), max 166.9 s; class-weighted ≈ **190 Kissat CPU-hours** for all 13,351.
The TAIL IS UNCONSTRAINED: the authors' orbit CNFs on this box spread 142–13,660 s (~100×); 1% of cells at an hour each
would add ~130 h. Plan = a capped first pass (cap 3600 s) + a rerun queue for UNKNOWNs, sized after the first pass.
Certified pass (CaDiCaL binary DRAT → drat-trim, proof deleted): ONE test cell (j = 2) took 82 s total, 27 MB proof,
`s VERIFIED` (`runs/test_drat.tsv`) ⇒ order of 300 CPU-hours, extrapolated from one cell.
What DRAT certifies: that each emitted CNF is UNSAT — NOT the emitter (h1mcell / h1cube2 / pysat seqcounter), the SB
clauses' soundness, the reduction, Lemma D, M1–M4, slots/PH, the enumeration or the coverage. Those rest on the proofs
here and in h1k/, code review, and the two referee reports (h1k/referee*, h1m/referee).
On this box after the Lean replay ends (~05-08Z 10-20), ~10 free cores at nice 19 ⇒ ~20 h (Kissat) / ~30 h (DRAT)
before tail reruns. That is a SAT campaign (and #552's cadicals are running), so it is NOT started from a cron tick:
Patrick's call. Runner (ready, resumable, not launched): `campaign.sh` — done ⟺ exact UNSAT / UNSATISFIABLE+VERIFIED,
any SAT writes runs/ALARM_SAT and halts dispatch; `tally.py <mode>` exits 0 only when all 13,351 keys are done. The 1-cell
test caught an awk NR==FNR bug (fresh campaign would have done nothing) and the referee caught a done-test bug
(a drat-trim timeout would have counted as done); both fixed and mutation-tested (`/tmp/h1m_rt` recipe in the seat log).
