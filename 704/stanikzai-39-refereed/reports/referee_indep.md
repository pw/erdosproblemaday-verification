> Bundle copy, lightly cleaned on 13 Nov: two editing splices removed and scratch paths repointed to `referee_scratch/` (the referee's scripts and logs). Content unchanged. Every fix it asks for was made before publication; see the page.

# Hostile referee report: independent recomputation of α(J(13,5,3)) ≤ 33

Referee seat, 2026-11-13. Scope: `/home/exedev/MathDyad/erdos704/indep/` (ESTIMATE.md, tree.py, replay.py, clq2.c,
run2.py, track.py, test_clq.py, cpsat_full.py, runs/). I did not modify any of those files. All scratch work is in
`referee_scratch/`:
- `check3.py`: a third tree checker. Orbits are computed combinatorially, not by closure.
- `track_many.py`, `track33.py`: coverage controls.
- `diff_test.py`: clq2 compared against cliquer.
- `cliquer_all.py`: a second leaf solver.
- `mutate.py`: consistent mutations of the manifest.

Severity scale: **BREAKS** means the claim is false or unsupported as stated. **SERIOUS** means the claim survives,
but the write-up or evidence as it stands would mislead a reader or leaves an instrument untested. **NIT** means a
presentation or robustness problem.

## Summary of what I re-derived myself

- P1, P2 and P3 are correct mathematics. The off-by-one is right: τ0 = 34 − 2 = 32.
- `replay.py` passes when rerun (35 s): `REPLAY OK n=13 s=33 nodes=209 internal=104 leaves=105 solve=105`.
- My own checker passes by a different route: `CHECK3 OK nodes=209 internal=104 leaves_in_file=105 childless=105`.
  - Residuals come from the closed formula, not incrementally.
  - Orbits are the classes of 5-sets with the same block-intersection signature under the Young subgroup of the
    connected components of the transposition graph. No closure is computed.
  - "Γ preserves R" is checked as "R is a union of signature classes".
- Both checkers go red on consistent mutations, where the change is propagated into leaves.txt and its sha256:
  - Exclude one extra non-orbit vertex at node 9: replay says `orbit mismatch at node 9`; check3 says
    `orbit mismatch at 9`.
  - Add the cross-block generator (3 6) at node 9: replay says `generator does not preserve R at node 9`; check3 says
    `R not a union of signature classes at node 9`.
- The files clq2 actually read match the checked files:
  - The chunk files `c*.txt`, taken as a multiset, equal `leaves.txt`.
  - The result ids in `r*.txt` equal the 105 leaf ids, each exactly once, all `UNSAT`.
  - All 10 return codes are 0.
- A fresh `-O2` build of clq2.c reproduces the shipped binary's node counts exactly on the 6 smallest leaves, for
  example `162 UNSAT nodes=38680` and `188 UNSAT nodes=89082`.
- Coverage control 1 (my own code, not track.py): 300 random independent sets containing v and u (sizes 2–29,
  maximal and non-maximal) were carried down the s=33 tree with explicit ground permutations. Every one lands with
  its residual part inside a leaf residual; 75 distinct leaves were hit.
- Coverage control 2: 576 images of the paper's 33-set (3 random normalisations for each of the 192 ordered pairs
  meeting in 4) were carried down the s=33 tree.
  - Every image lands inside a leaf residual. The images hit exactly 16 leaves.
  - These are exactly the 16 leaves that are SAT in `runs/n13_s32_lg350`. The s=32 tree is the s=33 tree with every
    τ lowered by 1; I checked this line by line.
  - clq2 at τ−1 says SAT on all 16. Mutual consistency between the positive control and the coverage argument is
    complete.
- clq2 at τ−2 and τ−3 on 8 other leaves gives SAT on 943, 1743, 683, 1303, 1582 and 1583. No answer is
  non-monotone in τ: no leaf is SAT at τ−2 and UNSAT at τ−3.

---

## Findings

### 1. P1, P2, P3: no objection
> "P1: a family of 5-subsets of [13] with all pairwise intersections ≤ 2 has at most ⌊C(13,3)/10⌋ = 28 members"

- **OK.** A triple inside two members would make them meet in at least 3. So 10·|F| ≤ 286, which gives |F| ≤ 28.
- Members of an independent set meet in {0,1,2,4}. A 34-set therefore has a pair meeting in exactly 4.

> "P2: Sym(13) acts transitively on ordered pairs of 5-sets meeting in exactly 4"

- **OK.** Explicit permutation for (A, B): send the elements of A∩B (sorted) to 0, 1, 2, 3; send A∖B to 4; send
  B∖A to 5; send the remaining 7 elements in order to 6..12. Permutations of [13] preserve intersection sizes, so they
  are automorphisms of J and map an independent 34-set to one containing v = {0..4} and u = {0,1,2,3,5}.

> "P3: then α ≤ 33 iff … no clique of size 32"

- **OK.** 34 = 2 + 32. R0 excludes v, u and their J-neighbours.
- In code, `tau0 = (s+1)-2 = 32`, and replay asserts `nodes[1]['tau'] == s-1 == 32`.
- |R0| = 851 was recomputed by replay and by check3.
- The complement graph has 647,361 edges = C(1287,2) − 1287·280/2, which is consistent.

### 2. Orbital-branching soundness: holds; the brief's specific worries do not bite
> "generators … each generator is checked to be an automorphism of J and to map the node's residual set onto itself"

- **OK.** A node's subproblem is exactly (Gbar[R], τ). F is already encoded in R because R ⊆ Nbar(f) for every
  f ∈ F.
- So Lemma 2.7 needs only Γ ≤ Aut(Gbar[R]). That follows from: each generator is a permutation of [13] (hence an
  automorphism of Gbar) and maps R onto R.
- The check in tree.py is therefore sufficient, and replay and check3 re-establish it independently.
- **{4,5} block that swaps v and u:** harmless. Γ need not fix v, u or F; v and u are not in R, and R0 is symmetric
  in v and u.
  - Note: the paper's §3.1(a) remark "The Young subgroup … fixes every forced vertex" is FALSE for our tree at nodes
    where {4,5} is still a block.
  - Do not port that sentence into our write-up. Soundness never used it.
- **Ancestors' excluded orbits:** the exclude child keeps the parent's group, so R∖O stays Γ-invariant.
- **Union-find:** produces the true orbits. At all 104 internal nodes, replay's closure and check3's
  signature-class computation both equal the recorded `excluded_orbit`.
- **Exclude child:** removes exactly the orbit, by the same equality.

### 3. SERIOUS: the n = 10 and n = 11 "route gates" never exercise the branching
> "Gates: our route gives α(J(10,5,3)) ≤ 12 and α(J(11,5,3)) = 18"

- At LEAFMAX = 350 the root is already a leaf: |R0| = 98 for n = 10 and 230 for n = 11, so the tree has 1 node.
  I reran `tree.py 10 12 350`, `tree.py 11 18 350` and `tree.py 11 17 350`; each gives `nodes 1 internal 0`.
- These gates therefore test P1–P3 plus clq2, and test P4 not at all.
- No artifacts for these gates exist in `indep/runs/`; only the CP-SAT gate files exist.
- **Evidence that P4 does pass a real gate (my rerun, in referee_scratch):**

  | Run | Tree | replay / check3 | clq2 result |
  |---|---|---|---|
  | n=11, LEAFMAX 60, s=18 | 27 internal, 28 leaves | both OK | 28/28 UNSAT |
  | n=11, LEAFMAX 60, s=17 | same | both OK | 13 SAT / 15 UNSAT; all 13 witnesses verified as 18-sets |
  | n=11, LEAFMAX 120, s=18 | 4 internal, 5 leaves | both OK | 5/5 UNSAT |

  The trivial gates also pass: n=10 s=12 UNSAT, n=11 s=18 UNSAT, n=11 s=17 SAT.
- **Fix:** publish the branching gate (n = 11 at LEAFMAX 60, s = 17/18), not the 1-node one, and save its
  artifacts.
- The only P4 positive control at n = 13 is the s=32 run. It is a good one (finding 0 above); keep it prominent.

### 4. SERIOUS: test_clq.py does not test clq2's multi-word code or its leaf indirection
> "P5: every leaf decided by our own bitset branch-and-bound clique solver clq2.c (same algorithm as clq.c; tested
> against networkx by test_clq.py)"

- test_clq.py runs `./clq`, not clq2, on n ≤ 60, which is a single 64-bit word.
- The real leaves have 221–357 vertices, which is 4–6 words.
- clq2's `main` is different code from clq.c's: the global graph plus the vs[]/orig[] indirection, and no bounds
  checks.
- `expand()` is byte-identical between the two files apart from comments. That is reassuring but untested above
  64 vertices.
- **My differential test:** random graphs with n in {40, 63, 64, 65, 66, 100, 127, 128, 129, 150, 191, 192, 193,
  220, 255, 256, 257, 300, 320, 350} and densities 0.5–0.85.
  - 60% of the graphs have a planted clique of size 8–40.
  - The leaf is a shuffled subset inside a larger global graph.
  - The reference ω comes from cliquer (Östergård's algorithm, the Debian binary) on the separately written induced
    graph.
  - Both the shipped `clq2` and a fresh build are queried at τ = ω−2, ω−1, ω, ω+1 and ω+2.
  - Results below.

`referee_scratch/diff_test.py`, seeds 11, 12 and 13, logs in `referee_scratch/log1{1,2,3}.txt`.

- **Graphs:** 107 random graphs completed. 13 were skipped because the cliquer reference took more than 60 s.
- **Coverage of the multi-word code:**
  - 91 graphs have n > 64.
  - 47 have n ≥ 192.
  - 2 have n = 350.
  - The tested n include every word boundary: 63, 64, 65, 127, 128, 129, 191, 192, 193, 255, 256, 257.
- **Queries:** each graph was queried at τ = ω−2 … ω+2 (values ≥ 1) on both the shipped `clq2` and a fresh build.
- **Result:** 0 mismatches, 0 bad witnesses, 0 non-zero exit codes.
- An earlier batch was aborted and discarded because its output was buffered and lost. It contributes nothing to
  these numbers.
- I read `expand()` line by line and found no bug:
  - The colour classes are greedy independent sets.
  - Only vertices with colour ≥ need are branched on.
  - What remains is (need−1)-colourable, so pruning is valid.
  - `col[i] < need` never fires and is redundant.
  - P is restored correctly between branches.
  - `found` and `csize` are reset for each leaf.
- **Fix:** point test_clq.py, or a copy of it, at clq2 with n up to about 360 and subset leaves; commit the result.

### 5. SERIOUS: one uncertified leaf solver, and the planned second solver never ran
> ESTIMATE.md: "(P5) leaves decided by (i) our own bitset branch-and-bound in C, (ii) OR-tools CP-SAT."

- `runs/cpsat_s33_lg350.log` and `runs/cpsat_samp24.log` are 0 bytes, and there is no `results_cpsat*.json`.
  `their_leaves.log` is also 0 bytes, and `runs/their_leaves_clq.json` does not exist.
- So all 105 UNSAT verdicts rest on one solver, with no proof log.
- That solver uses Tomita-style greedy-colouring bounds, the same family as MCQ/MaxCliqueDyn, which the submission
  also used. It is decorrelated in code, not in method.
- In the paper's own terms our recomputation is **uncertified**. That is fine for a corroboration, but it must be
  labelled as such.
- **What I added:** cliquer (Östergård "Russian doll" bound, a genuinely different method; also one of the
  submission's tools) on the real leaves, rebuilt from the 5-sets. Results below.

`referee_scratch/cliquer_all.py` and `cliquer_desc.py`; tally in `referee_scratch/cliquer_tally.json`.

cliquer 1.21 (Debian binary, Östergård's algorithm) ran on the induced leaf graphs, rebuilt from the 5-sets rather
than from gbar.col, for about 35 minutes on 2–4 cores at nice 19.

- **At τ: 41 of 105 leaves decided, all UNSAT, agreeing with clq2.**
  - These are the 40 smallest leaves (221–303 vertices) plus the largest leaf (leaf 181, 357 vertices, 232 s).
- **Positive controls at τ−1** on leaves hit by the 33-set images: 7 of 7 completed SAT. The leaf ids are 188, 186,
  156, 148, 66, 52 and 42. Every witness was re-verified as independent in J.
- **Disagreements with clq2:** 0.
- **Not reached in budget:** the remaining 64 leaves, of 303–350 vertices.
  - cliquer's time rises steeply: about 1–100 s at 260–300 vertices, with outliers up to 557 s (leaf 86, 295
    vertices).
  - Finishing all 105 leaves is a few core-hours. It is affordable and should be done before the word "recomputed"
    is used in public.
- **Fix:**
  - Say "uncertified; one solver" explicitly.
  - Delete the CP-SAT claim from ESTIMATE.md, or actually run it.
  - Ideally finish a second solver on all 105 leaves (cliquer over longer wall time, or mcqd/MoMC built from
    source) before calling it "recomputed".

### 6. NIT: "Leaves at residual size ≤ 350" is false for one leaf
- Leaf 181 has |R| = 357 at depth 40, because the DMAX = 40 depth cap forces leaves.
- Two leaves sit at depth 40.
- This is harmless: clq2 handles up to 1024 vertices, and the leaf is UNSAT. But the sentence is wrong.

### 7. NIT: docstring and description do not match the run
- tree.py's docstring says "Branch vertex = a max-degree vertex of the residual graph". The cited run uses
  `rule='largest'`, choosing the largest orbit first and breaking ties by degree.
- ESTIMATE.md P4 says "our own rule". The largest-orbit rule is the submission's rule (paper §3.1(3)(c)).

### 8. SERIOUS (presentation): "shares … no decomposition" overstates the independence
> "recomputed by a route sharing no code and no decomposition with the submission"

- The tree is different, and that is true and good:
  - The root is the pair reduction P1/P2, not a single vertex.
  - Generators are adjacent transpositions.
  - The stop rule is LEAFMAX 350.
  - There are 105 leaves against their 200, with different residuals.
- But the decomposition technique is the paper's own §3.1(3)(a)–(c): orbital branching over the Young subgroup of a
  partition refined by every forced set, with the largest-orbit rule. The soundness lemma is the same Lemma 2.7.
- The leaf solver is in the same family as MaxCliqueDyn.
- **Honest wording:** "a different branching tree (pair-fixed root, 105 leaves), built with the same standard
  orbital-branching technique, checked by two independent replays, with leaves decided by our own solver (code
  shared with nobody)".
- The shared ingredient, Lemma 2.7, is elementary, and I re-proved it above. So this does not weaken the
  mathematics, only the word "independent".

### 9. NIT (robustness): run2.py checks counts but not identity; clq2's parser is stream-based, not line-based
> run2.py: `missing = len(lines) - len(res)`

- **Demonstrated in referee_scratch on K6:** a leaf line with k = 4 but only 3 labels makes clq2 swallow the next
  line's id.
  - Output: `1 SAT 1 3 2 / 3 UNSAT nodes=1`, rc 0.
  - Leaf 2 is never answered, a phantom "leaf 3" is reported UNSAT, and `answered == leaves` still holds (2 == 2).
- **Also:** a label above GN (`1 2 2 1 7` on a 6-vertex graph) is read out of bounds silently and answered
  `UNSAT`, rc 0. An overlong line likewise produces phantom records, and a negative `missing` is not flagged.
- **This does not affect the published run.**
  - replay asserts `k == len(vs)` and the exact residual set for every line.
  - I checked that the chunk files equal leaves.txt and that the result ids equal the leaf ids, each once.
- **Fix:**
  - run2 should assert `sorted(result_ids) == sorted(leaf_ids)` and all rc == 0.
  - clq2 should parse one line at a time and bounds-check labels to 1..GN.

### 10. NIT: abandoned runs sit beside the cited one, and negative controls were not saved
- `runs/n13_s33_L350` (max-degree rule, 17,552 leaves) has no results; `run2_s33_L350.log` is 0 bytes.
- `runs/n13_s33_lg450` has no results.
- The "negative controls on replay.py (mutated manifests)" exist only as prose; there are no saved mutated manifests
  or rejection logs.
- **Fix:** label or remove the abandoned runs, and save the mutation logs (my `mutate.py` and its output can be
  reused).

---

## Differential test of clq2 (finding 4)

`referee_scratch/diff_test.py`, seeds 11, 12 and 13, logs in `referee_scratch/log1{1,2,3}.txt`.

- **Graphs:** 107 random graphs completed. 13 were skipped because the cliquer reference took more than 60 s.
- **Coverage of the multi-word code:**
  - 91 graphs have n > 64.
  - 47 have n ≥ 192.
  - 2 have n = 350.
  - The tested n include every word boundary: 63, 64, 65, 127, 128, 129, 191, 192, 193, 255, 256, 257.
- **Queries:** each graph was queried at τ = ω−2 … ω+2 (values ≥ 1) on both the shipped `clq2` and a fresh build.
- **Result:** 0 mismatches, 0 bad witnesses, 0 non-zero exit codes.
- An earlier batch was aborted and discarded because its output was buffered and lost. It contributes nothing to
  these numbers.

## Second solver on the real leaves (finding 5)

`referee_scratch/cliquer_all.py` and `cliquer_desc.py`; tally in `referee_scratch/cliquer_tally.json`.

cliquer 1.21 (Debian binary, Östergård's algorithm) ran on the induced leaf graphs, rebuilt from the 5-sets rather
than from gbar.col, for about 35 minutes on 2–4 cores at nice 19.

- **At τ: 41 of 105 leaves decided, all UNSAT, agreeing with clq2.**
  - These are the 40 smallest leaves (221–303 vertices) plus the largest leaf (leaf 181, 357 vertices, 232 s).
- **Positive controls at τ−1** on leaves hit by the 33-set images: 7 of 7 completed SAT. The leaf ids are 188, 186,
  156, 148, 66, 52 and 42. Every witness was re-verified as independent in J.
- **Disagreements with clq2:** 0.
- **Not reached in budget:** the remaining 64 leaves, of 303–350 vertices.
  - cliquer's time rises steeply: about 1–100 s at 260–300 vertices, with outliers up to 557 s (leaf 86, 295
    vertices).
  - Finishing all 105 leaves is a few core-hours. It is affordable and should be done before the word "recomputed"
    is used in public.

## Verdict

**HOLDS WITH FIXES.**

- No finding breaks the claim.
- The mathematics is correct: P1, P2, P3 and the orbital-branching lemma.
- The tree is sound by two checks that share no orbit or residual code: replay.py, and my signature-class check3.py.
- Coverage controls carry 876 sets into leaves, and the positive controls line up exactly (16 hit leaves = 16 SAT
  leaves).
- The leaf solver survived about 1,000 differential decisions across every word boundary. On the 41 real leaves
  that a decorrelated solver finished, it agrees, with 0 disagreements.
- **Required before publishing:**
  - (a) Call it an uncertified, single-solver recomputation, or finish cliquer on the other 64 leaves (finding 5).
  - (b) Replace the trivial n = 10/11 gates with the branching gate (finding 3).
  - (c) Replace "no decomposition" with "a different tree built by the same technique" (finding 8).
  - (d) Drop the CP-SAT claim from ESTIMATE.md (finding 5).
  - (e) Fix the false "≤ 350" line and the rule docstring (findings 6 and 7).

Final verdict line: **HOLDS WITH FIXES**
