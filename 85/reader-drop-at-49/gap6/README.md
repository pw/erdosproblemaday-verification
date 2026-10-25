# Gap 6 closed (2026-10-21, 03:00Z erdos seat)

Gap 6 of the published review: the DIMACS we render from the Lean definition
`orderFortyNineGeneratedH7SatCnf (representativeMasks t r)` (`t1rep0/EmitT1Rep0.lean`) did not hash to the module
headers' `source_cnf_sha256`, for any of the 13 H7 t ≥ 1 representatives.

Authors' explanation (Robb Walters, 2026-10-20): the header hash is of the file their Python encoder wrote through
pysat (`generate_h7_canonical_cnfs.py`, GitHub tag erdos85-paper-v1, not in the Zenodo zip). pysat's IDPool numbers
the edge variables by FIRST USE; the Lean definition numbers them lexicographically (`orderFortyNineEdgeIndex`).

Our test (`renumber.py`): take OUR Lean rendering, rename edge variables 1..1176 by first use over the whole file
(auxiliary variables > 1176 untouched), re-render, sha256.

- 13/13 representatives: the renamed file's sha256 equals the module header's `source_cnf_sha256` (`results.txt`).
- 307 of 1,176 edge variables move; the 315 leading clauses are unit clauses on variables 1..315 and all 307 moved
  variables are among them (checked separately on t1r0).
- Controls: a mutated CNF (`t1rep0/h7_t1_rep0_cnfmut.cnf`) renamed the same way does NOT match; t1r0 against t5r1's
  header does NOT match.
- The authors' renumbered hashes (Lean scheme) t1_rep0 = 4fc61de9…76d9 and t7_rep0 = e3c55d75…582c equal the sha256
  of our renderings `h7_t1_rep0.cnf` / `h7_t7_rep0.cnf` byte for byte.

Reproduce: `python3 renumber.py <our rendering .cnf> <header sha256>` for each representative.
