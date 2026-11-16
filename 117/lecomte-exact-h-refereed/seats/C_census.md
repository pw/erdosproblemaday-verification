## Erdős #117 (arXiv:2611.15068): computation-seat report

**Result: no counterexample.** No group or bilinear map anywhere in my range violates a ≤ T(ω) or z ≤ (T(ω)−1)². Every positive answer carries a witness that was re-checked independently. The pipeline does flag the deliberately wrong table: with T′(7)=9 it reports exactly the two order-243 extraspecial groups. Everything is in `~/MathDyad/subs-1116/117/seatC/`. Each job ran under `ulimit -v 8000000`, `timeout` (at most 3600 s), `nice 19`. I never touched cadical PIDs 3026833/3026834 and never used `pkill -f`. I stopped only my own PIDs by number.

**How a, ω and z are computed.** GAP 4.12.1 / SmallGrp (`export.g`) builds, for each nonabelian group, the commutation matrix of the nontrivial cosets of Z(G), tested on a faithful permutation image. Elements with the same centraliser (identical rows) are merged; this merging preserves ω and χ, and it automatically puts x and 2x together for odd p. Then:
- **ω:** exact branch-and-bound clique search (Python, plus C `gtool.c` for the larger graphs), with the clique witness re-checked.
- **a:** a DSATUR colouring, then clique-seeded SAT (cadical195) down to the optimum, or an UNSAT certificate at a−1. Every colouring witness is re-checked for properness.
- **z:** [G : Z(G)].

### Task 1: SmallGroups census

**Scope:** all 7012 groups of order ≤ 255, plus all 56092 groups of order 256 (every group of that order, not just class 2). Exact ω and exact a for every group.

How exact a was certified:
- Order ≤ 255: 6473 by colouring size = clique size; 37 by a SAT colouring of size ω; 8 by SAT UNSAT at a−1.
- Order 256: 54785 / 1101 / 184 by the same three routes.
- All 192 UNSAT lower bounds were re-proved with glucose4: 0 mismatches.

**Violations:** none of either kind, in both ranges.

**Orders ≤ 255, by ω** (the (a,z) distribution is the number of groups at each pair):

| ω | groups | T(ω) | max a | max z | (T−1)² | (a,z) distribution |
|---|---|---|---|---|---|---|
| 1 | 494 | 1 | 1 | 1 | – | |
| 3 | 276 | 3 | 3 | 4 | 4 | (3,4):276 |
| 4 | 170 | 4 | 4 | 9 | 9 | (4,6):125, (4,9):45 |
| 5 | 496 | 5 | 5 | 16 | 16 | (5,8):381, (5,12):42, (5,16):73 |
| 6 | 343 | 6 | 6 | 25 | 25 | (6,10):67, (6,16):240, (6,20):32, (6,25):4 |
| 7 | 219 | 10 | 10 | 81 | 81 | (7,8):61, (7,12):154, (9,64):2 [128,2326/2327], (10,81):2 [243,65/66] |
| 8 | 86 | 10 | 8 | 42 | 81 | (8,14):49, (8,21):23, (8,42):14 |
| 9 | 885 | 17 | 9 | 56 | 256 | (9,16):843, (9,32):37, (9,56):5 |
| 10 | 134 | 17 | 10 | 72 | 256 | (10,18):62, (10,24):23, (10,27):32, (10,36):13, (10,72):4 |
| 11 | 673 | 33 | 11 | 32 | 1024 | |
| 12 | 371 | 33 | 12 | 110 | 1024 | |

- For ω from 13 to 68, max a = ω in every row except ω=24, where a=27.
- Only 8 groups of order ≤ 255 have a > ω:
  - [128,2326], [128,2327]: ω=7, a=9.
  - [243,65], [243,66]: ω=7, a=10.
  - [192,1333], [192,1334], [192,1337], [192,1338]: ω=24, a=27.
- Every nonabelian group with ω ≤ 6 has a = ω.

**Equality cases, orders ≤ 255:**
- a = T(ω), 1287 groups: all 276 + 170 + 496 + 343 groups with ω = 3, 4, 5, 6, plus at ω=7 only [243,65] and [243,66].
- z = (T(ω)−1)², 400 groups:
  - ω=3: all 276.
  - ω=4: 45 (including [27,3], [27,4], [81,*], [243,2], …).
  - ω=5: 73 (including [32,49], [32,50]).
  - ω=6: [125,3], [125,4], [250,10], [250,11].
  - ω=7: [243,65], [243,66].
- Max z at ω=8 is 42: [42,1], [84,1], [84,7], [126,1], [126,7], [168,1], [168,8], [168,10], [168,47], [210,1], [252,1], [252,7], [252,16], [252,28].

**Order 256:**
- ω=7: (7,8):129 and (9,64):7. The worst ratio is a/T = 0.90, at [256,55640].
- ω=9: (9,16):2923, (9,32):503, (9,64):9.
- ω=11: (11,16):2258, (11,32):3563, (12,64):30.
- For ω ≥ 9 the worst a/T(ω) is 0.53.
- The 1003 equality groups at order 256 all have ω ∈ {3,5,6}; there is no ω=4 at this order, and nothing at ω ≥ 7 reaches T(ω).

### Task 2: sharp examples

| object | z | ω | a | how a is certified |
|---|---|---|---|---|
| ES 2^{1+4} ± | 16 | 5 | 5 = T(5) | DSATUR colouring of size 5 = ω |
| ES 2^{1+6} ± ([128,2326/2327]) | 64 | 7 | 9 < T(7)=10 | α=7 gives a ≥ 63/7; tabucol 9-colouring; UNSAT at 8 |
| ES 2^{1+8} ± (GAP, order 512) | 256 | 9 (proven) | 17 = T(9) | α=15 gives a ≥ 255/15; tabucol 17-colouring |
| ES 2^{1+10} (random rank-10 forms, 5 maps) | 1024 | ≥ 11 (found, not proven max) | 33 = T(11) | α=31 proven; explicit F₃₂-spread colouring, verified |
| ES 3^{1+4}, exp 3 and 9 ([243,65/66]) | 81 | 7 (proven) | 10 = T(7) | α=4; UNSAT at 9 |
| F₉ trace model, built in Python from Tr(x₁y₂−x₂y₁) | 81 | 7 (C and Python searches both prove no 8-clique) | 10 | α=4; UNSAT at 9; the 10 F₉-lines give a proper colouring |
| ES 3^{1+6} (F₂₇ trace model) | 729 | ≥ 13 | ≤ 28 | verified F₂₇-line spread colouring |
| ES 5^{1+4} | 625 | 18 (proven) | 26 | α=6; spread colouring |
| ES 7^{1+4} | 2401 | ≥ 33 | 50 | α=8; spread colouring |

- GAP identifies the Python-built F₉ group as IdGroup [243,65] (exponent 3), the same as `ExtraspecialGroup(243,3)`.
- **ES 3^{1+6} is the one danger point.** The bound needs ω ≥ 11 here, because T(10)=17 < 28. A 13-clique (the paper's Ceria et al. count) was found and checked by evaluating the form directly on the vectors (listed in `logs/es3_6.log`). The exact search for a 14-clique did not finish before the 1500 s cap, so whether ω exceeds 13 is still open.
- **ES 5^{1+4}:** the exact ω=18 is well above the 11 the bound needs.
- **Extraction caveat:** in `paper.txt`, Lemma 3.1's "pr + 1" means p·r+1, not p^r+1. Lemma 3.2's "pr + 1" means p^r+1. The computed values (ω=7 for 3^{1+4}, a=10) fit only that reading.

### Task 3: bilinear-map probe and exhaustive enumerations

**Random and structured maps over F_p:** 1091 maps.
- Families: `random`, `formplusdeg` (a standard form plus rank-2 forms), `sum2` (a form and a rank-2 perturbation of it), `tracesub` (Tr(c·det) for an e-dimensional space of c), `directsum`.
- Ranges: p=2, d=4..10, e=1..4; p=3, d=3..6, e=1..2. Per-(p,d,e,family) counts are in `probe/summary_all.txt`.
- **Certification:** a verified colouring with a_ub ≤ T(ω_lb), where ω_lb comes from a verified clique (T is nondecreasing, so this is sound), and z ≤ (T(ω_lb)−1)². Escalation when needed: tabucol, then the explicit spread obtained by mapping a single form isometrically to the F_q trace model, then SAT.
- **Uncertified a: 0. Uncertified z: 0.**
- Worst a_ub/T(ω_lb):
  - 1.0 only in single-form (e=1) maps whose clique number is at most 8, plus the binary symplectic equality cases.
  - With e ≥ 2: at most 0.588 (p=3, d=4), at most 0.53 (p=2, d ≤ 6), and at most 0.17 for d ≥ 8. Adding even one rank-2 form pushes ω from 9 to 18 or more.
- Equality cases with ω ≥ 7 occur only in:
  - p=2, e=1, rank 8: ω=9, a=17 (22 maps).
  - p=2, e=1, rank 10: a=33 (5 maps).
  - p=3, e=1, rank 4: ω=7, a=10 (51 maps).
- No map with e ≥ 2 or odd p reached equality at ω ≥ 9. This is consistent with the paper's classification of the n ≥ 9 maximisers.

**Non-elementary central quotients** (`probe_zpk.py`, 284 maps): A = (Z/4)^k × (Z/2)^j with |A| ≤ 256, or (Z/9)^k × (Z/3)^j with |A| ≤ 729, e=1,2. 0 uncertified on either side.

**Exhaustive enumeration over every subspace W of alternating forms.** This covers every group with G/Z ≅ F_p^d and that commutator rank. Enumeration counts were asserted equal to the Gaussian binomials.

- **F₂⁴, all 2824 subspaces (e=1..6):** 0 violations. Equality only at (3,3,4) and (5,5,16), with (6,6,16) on the a side.
- **F₃⁴, all 56631 subspaces (e=1..6):**
  - e=1: (ω,a,z) ∈ {(4,4,9), (7,10,81)}.
  - e=2: (10,10,27), (10,10,81), (12,12,81), (16,16,81).
  - e ≥ 3: ω ≥ 13.
  - 0 violations. With z=81, ω ≤ 8 occurs only for the single form, so a=10 and z=81 are maximal there.
- **F₂⁵:**
  - e=1: all 1023.
  - e=2: every other subspace in enumeration order, 87126 of 174251. Values (9,9,32) and (11,11,32) agree with the order-128 census.
  - 0 violations.

### Task 4: controls

All passed; logs are in `logs/`.
- The colouring checker rejects an improper colouring and the clique checker rejects a non-clique.
- The Python search, the C search and networkx agree on clique number for 300 random graphs.
- Exact χ matches brute-force backtracking on 150 random graphs. C5, Petersen, Grötzsch, the complement of C7 and K6 give their known (ω, χ).
- Tabucol and SAT both fail to 2-colour C5, as they should.
- The census agrees with an independent recomputation on the full graph without twin merging (networkx clique, a second SAT solver):
  - all 586 groups of order ≤ 64, with no symmetry breaking;
  - a 265-group sample of orders 65–255, using clique-seeded SAT on the larger graphs.
- Census values on D8 (3), Q8 (3), S3 (4), A4 (5), S4 (10), A5 (21), D10 (6) and Heis(3) (ω=4, a=4) match groups built in Python without GAP.
- Wrong table T′(7)=9:
  - the census flags exactly [243,65] and [243,66] on both the a side and the z side;
  - the probe's certificate becomes False under T′ and True under the paper's T.

### What this evidence does not cover
- Groups of order above 256 that fall outside the families above. That includes nonsolvable and nonnilpotent groups, class ≥ 3, and nonabelian central quotients above 256.
- Elementary-abelian central quotients F₂⁶ with |G′| ≥ 8, F₂⁷ and larger, and F₃⁵ and larger, are covered only by random sampling. The samples are mostly generic maps far from extremal.
- Odd primes p ≥ 5 are covered only by the two extraspecial checks above.
- For d ≥ 8, the probe's ω and a are bounds, not exact values. The certificates are sound, but the reported numbers are not exact.
- No proof steps of the paper were checked.
- No DRAT certificates were produced; UNSAT results rest on cadical plus a glucose4 cross-check.
- ω(2^{1+10}) ≤ 11 and ω(3^{1+6}) = 13 were not proven computationally.
- The F₂⁵, e=2 enumeration ran on half the subspaces. I stopped the other half because it would have run past its time cap, and those groups are all already in the order-128 census.

### Reproduction (from `~/MathDyad/subs-1116/117/seatC`, each wrapped as `bash -c 'ulimit -v 8000000; exec nice -n 19 timeout 3600 …'`)
```
gcc -O2 -march=native -o gtool gtool.c
gap -q census/run_{A,B,C,D}.g ; gap -q census/run_256{a,b}.g < /dev/null
python3 analyze.py census/census_le255 census/export_{A,B,C,D}.txt
python3 analyze.py census/census_256 census/export_256{a,b}.txt
python3 analyze.py census/WRONGTABLE_le255 --wrong-table census/export_{A,B,C,D}.txt
gap -q census/run_full.g ; python3 controls.py            # sections 1-5
gap -q census/run_fullsample.g < /dev/null ; python3 fullsample_check.py
python3 recheck_unsat.py census/census_le255.tsv census/export_B.txt census/census_le255.tsv census/export_D.txt census/census_256.tsv census/export_256a.txt census/census_256.tsv census/export_256b.txt
gap -q sharp/export_es.g < /dev/null ; python3 sharp.py ; gap -q sharp/id_f9_perm.g < /dev/null
python3 es3_6.py 900 ; python3 esp.py 5 2 300 ; python3 esp.py 7 2 300
probe/run_jobs.sh probe/jobs.txt probe/small.jsonl logs/probe_small.log      # likewise jobs_big2/jobs_huge2/jobs_huge3
probe/run_zpk.sh ; python3 summarize_probe.py probe/{small,big,huge}.jsonl ; python3 probe_control.py
python3 exhaustive.py 2 4 1,2,3,4,5,6 ex/p2d4 ; python3 exhaustive.py 3 4 1,2,3,4,5,6 ex/p3d4
python3 exhaustive.py 2 5 2 ex/p2d5_e2_c0 0/2
```

Notes on reproducing:
- To regenerate `big.jsonl` / `huge.jsonl` exactly, also run the first lines of `jobs_big.txt` / `jobs_huge.txt`. Ten `big.jsonl` records and one `huge.jsonl` record came from an earlier version of the script that ran the exact clique search and α on every map; the certificate logic is the same.
- The F₂⁵, e=1 result is in `logs/ex_p2d5.log`. That run was stopped during e=2, so no summary file was written for it.