# Erdős #112 — four new lower bounds for small k(n,m) (submission eqf2h6, Tyler Satchel Orden, 22 Nov 2026)

k(n,m) = least k such that every oriented graph on k vertices has n pairwise non-adjacent vertices or a transitive
tournament on m vertices (r(I_n, L_m) in the literature).

**Claim:** k(7,3) ≥ 39, k(8,3) ≥ 47, k(6,4) ≥ 78, k(3,6) ≥ 71, by explicit (bi)circulant oriented graphs on 38, 46,
77 and 70 vertices (Zenodo 10.5281/zenodo.24390891, 20 Nov 2026). Previous bounds he cites: 37, 46, 65, 68
(github.com/rsvaultpudgy-create/erdos-112-lower-bounds, 11 Nov 2026, described there as AI-generated and unrefereed).

**Verdict: VERIFIED** (22 Nov 2026). All four graphs are oriented (no loops, no 2-cycles), have no independent n-set
and no transitive m-tournament.

**Checks.**
- `python3 check_orden.py` → `check_orden.out`: our own checker, written from the connection sets in the submission
  text (not from his files or code). Bitset recursion for independent sets and for transitive tournaments (TT_m exists
  iff some vertex has TT_{m-1} inside its out-neighbourhood). Positive controls: Kirtchakov's Cay(Z_28,{3,8,10,12,17})
  for k(6,3) ≥ 29, the directed triangle for k(2,3) ≥ 4. Negative controls (must fail): the Z_19×2 graph asked for no
  independent 6-set, the Z_77 graph asked for no transitive triangle, the Z_70 graph with 69 added (2-cycles) and with
  64 dropped (independent 3-set appears). All behave as expected; exit 0.
- His arc-list files are identical to the graphs we rebuilt from the connection sets (check in the review log).
- His own `run_checks.sh` (C checker + Python counter) → `submitter_run_checks.out`: 15 PASS lines exit 0, his 7
  negative controls exit 1. `submitter/SHA256SUMS.txt` matches 22 of 23 listed files (the licence file was not copied).

**Not checked:** his Lean 4 proofs (github.com/Tyorden/erdos-112-small-bounds-lean) were not built. The second
k(3,6) witness on Z_69 was not re-checked by our code (it is implied by the Z_70 one).

**World (22 Nov 2026, erdosproblems.com not read):** DataCite lists no other record for these four cases; the only
earlier bounds we found are the rsvaultpudgy repository's. Upper bounds are not improved.

`submission_eqf2h6_frozen.json` is the submission as received (contact details removed).
