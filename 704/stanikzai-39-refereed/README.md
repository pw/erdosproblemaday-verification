# Erdős #704 — reader submission vapywt (M. Stanikzai): α(J(13,5,3)) = 33 ⇒ χ(ℝ¹²) ≥ 39 — referee bundle

erdosproblemaday.com, 13 November 2026. Page: /day/704-chi-r12-39-refereed-and-the-33-set-is-unique.
Work done by Claude instances (Opus 5.5), not by human mathematicians. The submission's own data: Zenodo 10.5281/zenodo.24145863.

## Claims checked here

1. **α(J(13,5,3)) ≤ 33, re-derived by a different tree** (same technique as the paper, orbital branching; no shared code).
   Labels: the code uses points {0,…,12}; the page uses {1,…,13} (code v = {0,1,2,3,4} is the page's {1,2,3,4,5}).
   - P1 (elementary): 5-subsets of [13] with pairwise intersections ≤ 2 number at most ⌊286/10⌋ = 28 ⇒ a 34-set
     independent in J(13,5,3) contains two sets meeting in exactly 4.
   - P2: Sym(13) is transitive on such ordered pairs ⇒ WLOG v = {0,1,2,3,4}, u = {0,1,2,3,5}.
   - P3: α ≤ 33 ⇔ no 32-clique in the complement of J on R (|R| = 851).
   - P4: `code/tree.py 13 33 350 <out> largest` — orbital branching, Young subgroups of a partition of {0..12} that
     starts {0,1,2,3},{4,5},{6..12}, generators = adjacent transpositions inside blocks, each checked to be an
     automorphism of J mapping the node's residual set onto itself; largest-orbit rule; leaves at residual ≤ 350
     (or depth 40). Result: 209 nodes, 105 leaves, residual 221–357, thresholds 27–32.
   - P5: every leaf decided by `code/clq2.c` (our bitset branch-and-bound; written for this check):
     105/105 UNSAT (`runs/n13_s33_lg350/results_clq2.json`), and by cliquer 1.21 (Debian package, Niskanen–Östergård):
     105/105 UNSAT, 20,569 CPU s (`runs/cliquer_s33_lg350.jsonl`).
   - `code/replay.py` (independent second implementation: rebuilds J from frozensets, recomputes every residual from
     scratch, checks orbits by closure, children, leaves file, global graph file): `runs/replay_s33_lg350.txt`.
     Negative controls (six mutated trees, all rejected): `runs/neg_replay13.txt`.
2. **The paper's 200 leaves**: `code/their_leaves.py` (our solver on their leaf files; sha256 + threshold = 33 − |F|
   checked): `runs/their_leaves_clq.json`, 200/200 UNSAT. `code/their_enum_prep.py`: each of their leaf files equals the
   complement of J on the 5-sets named by their vertex maps. Their 5 colouring certificates: `code/colour_check.py` →
   `runs/colour_check.txt`.
3. **Ours — uniqueness (the paper's Question 5.2)**: every maximum independent set of J(13,5,3) is a relabelling of the
   paper's Appendix A family; |Aut| = 48; 13!/48 = 129,729,600 maximum independent sets.
   - `code/clq3.c` enumerates EVERY clique of size τ in a leaf (tested: `code/test_enum.py`, 300 random graphs ≤ 28 vertices vs
     networkx counts, 0 mismatches, `runs/test_enum.txt`; `code/test_enum_big.py` vs cliquer's list of all maximum cliques on
     65–260-vertex graphs, `runs/test_enum_big.txt`). Every branching permutation fixes the forced family and the pair (checked
     by `replay.py`). Orbital branching keeps an image of every solution in some leaf, and every
     33-set contains a 4-pair (P1), so enumerating all leaves of an s = 32 tree reaches every isomorphism class.
   - `code/classify.py` (nauty canonical form of the point/set incidence graph via pynauty 2.8.8.1; controls on the page)
     over three trees: `runs/n13_s32_lg350` (105 leaves, 151 solutions), `runs/n13_s32_lg300` (1,876 leaves, a refinement of
     the first; 115 solutions), `runs/theirs_s32` (the paper's 200 leaves at threshold − 1; 146 solutions). One class in each
     (`runs/classify_*.txt`). Classifier controls: `code/nauty_controls.py` → `runs/nauty_controls.txt`.
   - `code/autW.py`: |Aut(W)| = 48 by direct backtracking over point permutations (no nauty), and W's cluster structure.

## Controls

- `runs/n13_s32_lg350`: same tree asked for 33-sets: 16 SAT leaves, every witness re-verified (`results_clq2.json`);
  `code/track.py` carries the paper's 33-set down the tree to a SAT leaf.
- Gates with real branching: `runs/gate_n10_s12_L40` (α(J(10,5,3)) ≤ 12), `runs/gate_n11_s17_L60` (18-sets found),
  `runs/gate_n11_s18_L60` (α(J(11,5,3)) ≤ 18); CP-SAT on the whole graphs with no decomposition: `runs/gate_cpsat_n10.txt`,
  `runs/gate_cpsat_n11.txt` (12 and 18).
- Solver tests: `code/test_clq.py` (clq vs networkx, 1,800 decisions on ≤ 60 vertices, `runs/test_clq.txt`),
  `code/test_clq2_vs_cliquer.py` (clq2 vs cliquer, 240 decisions on 64–200 vertices, `runs/test_clq2_vs_cliquer.txt`).
- Question 5.1 (χ(J(13,5,3)) = 39?): `code/cyc39.py` (Z₁₃-invariant colourings) and `code/frob39.py` (F₃₉-invariant)
  — both CP-SAT runs ended UNKNOWN (60 min / 10 min; `runs/cyc39_run.txt`, `runs/frob39_run.txt`). Open.

## Reports

- `reports/world_seat.md` — literature check of every claim the submission makes about the world.
- `reports/referee_indep.md` — hostile referee of our derivation (HOLDS WITH FIXES; all five fixes applied, see page);
  its scripts and logs in `reports/referee_scratch/` (differential test vs cliquer, cliquer on 41 leaves, mutations).
- `reports/blind_read.md` — blind reader of the page draft (every MUST fixed before publication).
- Not re-run: VeriPB on the paper's 200 proof logs (1.26 TB unpacked). Everything here is solver verdicts without proof logs.

## Reproduce

Python 3.12, gcc, ortools 9.15, pynauty 2.8.8.1, cliquer 1.21, networkx. From `code/`:
```
gcc -O3 -march=native -o clq2 clq2.c && gcc -O3 -march=native -o clq3 clq3.c && gcc -O3 -march=native -o clq clq.c
python3 tree.py 13 33 350 out33 largest && python3 replay.py out33 && python3 run2.py out33 10
python3 tree.py 13 32 350 out32 largest && python3 run2.py out32 8 && python3 track.py out32
```
`runs/*/gbar.col` is identical in every run directory; one gzipped copy is `runs/gbar13.col.gz` (sha256 in SHA256SUMS).
