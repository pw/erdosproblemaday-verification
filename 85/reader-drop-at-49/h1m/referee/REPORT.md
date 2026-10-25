**VERDICT: HOLDS WITH FIXES.** I found no soundness defect in M1–M4, the enumeration, the cell encoding, the symmetry breaking or the coverage argument. The fixes are a campaign-runner bug that lets unverified cells count as done, and overclaims in README §2, §4 and §5.

(Hostile referee seat, Opus 5.5, briefed to refute, 2026-10-19 ~21:45–22:10Z. Saved verbatim by the 21Z seat from the
seat's final message — the harness blocked the seat from writing this file itself. Fix status at the end.)

Hostile pass, 2026-10-19 ~21:45–22:10Z. I read:
- h1k/README.md and h1m/README.md. The h1m README changed on disk at ~21:41Z; I quote the current text.
- menum.py, mcount.c and mcount_nod.c; h1mcell.py, diffed against h1cube2.py.
- fsenc.add_perm_sb, campaign.sh, sample_cells.sh, musub.py, classes_all.tsv and runs/*.
- The prior referee report.
- The authors' Lean (CapacityInventory, CapacityCover, BranchDeficitSymmetry) and their h1_orbit_inventory.compact.

All solver runs: nice 19, `ulimit -v 4000000`, timeout ≤ 900 s, at most 2 at a time.

## What held

**(a) M1–M4.** I re-derived each one.
- **M1:** z ∈ X has a neighbour in a non-paired Y ≠ X iff mu(z) ≠ Y, and then exactly one.
- **M2:** the edges between X and Y are one set, so M is symmetric.
- **M3:** a matched z misses one block outside {X, X'}; an unmatched z misses X. So the row sum is 2e(X).
- **M4,** derived from mu without going through Lemma D's steps:
  - A common neighbour of a ∈ X and b ∈ Y is a far vertex adjacent to both blocks.
  - z is adjacent to X iff z ∉ X' and mu(z) ≠ X.
  - Exactly 5 vertices miss X, and none of them lie in X'.
  - So m(X,Y) = 30 − (5 − M[Y'][X]) − (5 − M[X'][Y]).
  - Hence q = 25 − m = 5 − M[X'][Y] − M[X][Y'], by symmetry. This is M4 with the README's orientation.

Every constraint in menum.py and mcount.c is implied by the graph: non-negativity, symmetry, zero diagonal and paired positions, exact row sums, M4, and the bound min(rem[X], rem[Y]). So no H is excluded.

**(b) Independent enumeration** (`enum_indep.py` → `enum_indep.out`).
- **Method:** 2×2 blocks per pair of pairs, where M4 is local (two anti-diagonal sums ≤ 5). Tables are built by a numpy join over blocks, cross-checked by a counting DP over row-sum states.
- **Orbits:** counted by Burnside's lemma, not by orbit minima.
- **Groups:** brute force over S8 (pairing- and e-preserving).

| case | \|G\| (brute = menum, as sets) | w/o M4 matrices (enum = DP) | orbits | with M4 matrices | orbits |
|---|---|---|---|---|---|
| 0 | 24 | 16,692 | 842 | 16,677 | 839 |
| 1 | 12 | 31,512 | 2,700 | 31,458 | 2,693 |
| 2 | 16 | 70,070 | 4,801 | 69,321 | 4,717 |
| 3 | 48 | 169,668 | 3,662 | 167,748 | 3,617 |
| 4 | 384 | 449,358 | 1,536 | 442,518 | 1,485 |

Total 13,541 → 13,351; 190 removed. Against this enumeration, classes_all.tsv passes in every case:
- every row is admissible;
- rows are pairwise inequivalent (own canonical form);
- every orbit is hit;
- stabilisers (brute force) and orbit sizes are correct;
- the orbit sizes sum to the matrix count.

I rebuilt mcount and mcount_nod and got identical counts.

**(c) Identification with the authors.**
- Their table entry `highBranchMissCount(s,t) = #{a ∈ branch s : N(a) ∩ branch t = ∅}` (BranchDeficitSymmetry.lean:83) is our M[s][t].
- Their capacity filter is T[c][j^1] + T[j][c^1] ≤ 5, which is M4 by symmetry.
- Their CapacityCover proves `#commonPairs = 20 + T[a][b^1] + T[b][a^1]`, which is our 25 − q.

`rowmatch_authors.py` applies an explicit relabelling φ, because their profile a puts the (1,2) pairs first with the even block at e = 1. Under φ:
- their capacity test and our M4 agree on all 13,541 raw rows;
- their 13,351 kept rows equal classes_all.tsv as sets, case by case;
- their 190 removed rows are exactly the M4 failures.

**(d) Cell encoding and symmetry breaking.**
- **Stabiliser filter.** `MM[b X][b Y] == MM[X][Y]` is correct. On 200 cells (the 15 largest stabilisers per case plus 25 random), h1mcell's loop equals the brute-force stabiliser minus the identity, and its size equals the |stab| column.
- **Permutations preserve the cell.** All 5,952 permutations checked (pair maps, edge swaps, transpositions) preserve the blocks, pairing, e-pattern, internal edges, free-variable set and M.
- **One order, one direction.**
  - For every transposition in every case, h1cube2's row-lex comparison sequence is a subsequence of `add_perm_sb`'s sequence (X ≤lex X∘π over sorted(var)), with the same orientation.
  - Every extra element is the reversal of an earlier one, so the two predicates are identical.
  - Random assignments with forced equal prefixes agree.
  - Negative controls give mismatches (1,590 for descending columns, 3,200 for flipped direction, 1,061 for odd/even order), so the check can fail.
  - Edge-swap and pair SB both go through `add_perm_sb`. All SB is therefore lex-leader under one order and one direction, for permutations of a group that preserves the cell's solutions. That is jointly sound.
- **Edge counts.** `between(X,Y)` lists each cross pair once, so the exact count #edges(X,Y) = 5 − M[X][Y] is right.

**(e) Coverage, end to end** (`coverage_e2e.py`). I took Kissat models (several seeds) of the whole-case CNF: no M, no SB, `--drop-c4 --slots --ph`, Lemma D on. For each model I:
1. computed M from the graph and checked symmetry, row sums and M4;
2. canonicalised M and found the class in the tsv;
3. relabelled the graph and fed it as 600 unit clauses to the representative's cell (no SB): SAT;
4. fed the same graph to a different class's cell: UNSAT.

Case 4: 6/6. Case 0, which has oriented (2,1) pairs: 5/5.

**(f) Controls rerun.**
- `dropc4_stab128.out`: the j = 4 cell with |stab| = 128 (127 pair permutations), all flags, C4 dropped → SAT, recheck clean, pair-lex 0/127.
- `--check-only` mutation (pair-SB clauses withheld) → 8/127 violations, so the recheck discriminates.
- `stab128_solvers.out`: the same cell with C4 on → Kissat UNSAT in 36.6 s, CaDiCaL UNSAT in 19.0 s.

## Objections

**1. The §2 identification is drawn from counts.**
> "Our numbers WITHOUT M4 equal theirs in every entry (profile p = our case 4 - p), and M4 removes exactly 51 + 45 + 84 + 7 + 3 = 190 classes. So their H1 inventory is this miss-matrix cube, and their capacity inequality is Lemma D (M4) — derived here independently, from the graph, without reading their Lean. (Counts, not a row-by-row identification: their table format was not parsed.)"

*Problem.* Equal counts do not make two inequalities, or two inventories, the same object, so the "So" does not follow. The labelled sets are also equal only up to a relabelling: their (1,2) pairs come first with the even block at e = 1.

*Fix.* Base the identification on their definitions (T = highBranchMissCount = M; capacity = M4 by symmetry; CapacityCover's `20 + T[a][b^1] + T[b][a^1]` = 25 − q) and on referee/rowmatch_authors.py: agreement on 13,541/13,541 raw rows and set equality of the 13,351 kept rows.

**2. `campaign.sh` records unverified UNSAT cells as done.**
> "Resumable: a cell already in the output TSV (any verdict but UNKNOWN/ERROR) is skipped"

The done test is `$3 ~ /UNSAT|SAT/ && $3 !~ /UNKNOWN/ && $4 !~ /NOT VERIFIED/`.

*Problem.* If drat-trim prints no `s VERIFIED` / `s NOT VERIFIED` line, `v` becomes "none". That happens when:
- coreutils `timeout $((CAP*3))` kills it;
- it hits its own limit and prints `s TIMEOUT` (`-t` default 40000);
- it crashes or runs out of memory under the 4 GB limit.

"none" passes the `NOT VERIFIED` test, so the cell is skipped forever without a proof check. A `s SATISFIABLE` result is also silently "done", and no tally compares the output with the 13,351 classes.

*Fix.*
- Done ⟺ `$3=="s UNSATISFIABLE" && $4=="s VERIFIED"` in DRAT mode, and `$3=="UNSAT"` in Kissat mode.
- Treat any SAT as an alarm: stop, save the model, recheck it.
- Add a tally script that exits non-zero unless all 13,351 (j, M) keys have exactly one VERIFIED row with a CNF hash.
- Set drat-trim's `-t` explicitly, or log TIMEOUT as its own status.

**3. "Meets the bar" overstates what DRAT certifies.**
> "The certified pass alone meets the bar (solver + independent proof checker)"

*Problem.* drat-trim certifies only that each emitted CNF is UNSAT. It does not certify the emitter (h1mcell, h1cube2, pysat seqcounter), the soundness of the symmetry-breaking clauses, the reduction, Lemma D, M1–M4, the slots/PH constraints, the enumeration's completeness, or coverage. Those rest on proofs, code review and the referee tests.

*Fix.* Say so explicitly.

**4. The §4 positive controls overclaim the SB part.**
> "on three cells (j = 0, 2, 4): **SAT**, and the model rechecks clean — … transposition / pair / edge-swap lex order, PH … So the cells are not vacuous; C4-freeness is what empties them."

*Problem.* `dropc4_controls.out` shows pair-lex 0/0 for j = 0 and j = 2 (trivial stabiliser, so no pair SB at all) and 0/1 for j = 4. No mutation run shows the recheck can fail. The edge-swap recheck cannot discriminate as coded: `eslex` is computed only when edge-swap clauses are present. "The cells" generalises from three cells to all 13,351.

*Fix.* Cite referee/dropc4_stab128*.out (0/127 with clauses, 8/127 with `--check-only`). Add an edge-swap mutation. Say "these cells".

**5. A cited result has no artefact.**
> "First probes (j = 0, no edgeswap): 4/4 UNSAT, 42-150 s."

*Problem.* There is no file for this in runs/.

*Fix.* Add the file or drop the line.

**6. The §5 estimates have no uncertainty.**
> "13,351 cells x ~54 s ~= **200 Kissat CPU-hours**" / "on the order of **300 CPU-hours**"

*Problem.*
- 54 s is a wall-clock mean over n = 26 cells (5–6 per case, nice 19, load 14–18, encoding included). Per case: 50.1 / 62.6 / 45.7 / 41.3 / 67.5 s, max 166.9 s. The class-weighted mean gives ~188 h, so the centre is fine.
- The tail is unconstrained: the README's own 142–13,660 s spread for the authors' orbit CNFs shows ~100× variation, and 1% of cells at 1 h would add ~130 h.
- Cells that hit CAP = 3600 come back UNKNOWN, and their reruns are not in the estimate.
- The 300 h figure extrapolates from one cell (82 s, 27 MB).

*Fix.* Label the figures as sample means with n stated, give the per-case means, note the unconstrained tail, and plan a capped first pass plus a rerun queue.

**7. (minor) The §3 coverage sentence omits the symmetry-breaking step.**
> "g maps H to an H' in the representative's cell (same case, same fixed internal edges). So H1 is empty iff all 13,351 cells are UNSAT."

*Problem.* H' generally violates the cell's lex-leader clauses. The argument needs the lex-least member of H''s orbit under the cell group Γ_c (transpositions, edge swaps and Stab(M)). That member satisfies every SB clause only because all SB uses one order and one direction (referee/sb_order_check.py). The "iff" itself is correct by h1k §1, conditions (i)–(iii).

*Fix.* Add that sentence and cite the order check.

## Checked and fine (not objections)
- |G_j| = 384/48/16/12/24, and each G_j is the full pairing- and e-preserving group.
- The menum and mcount descriptions are accurate.
- The 26 sampled cells are all in classes_all.tsv and all UNSAT (19.3–166.9 s, mean 54.0 s, as stated). The truncated-prefix draw is disclosed.
- `--cov` and `--mu` are correctly marked as unused.
- In h1mcell the cell-membership and edge-swap results are added to the violation list before the recheck line is printed.

Files are in /home/exedev/MathDyad/erdos85/h1m/referee:
enum_indep.py, enum_indep.out · sb_order_check.py, sb_order_check.out · coverage_e2e.py, coverage_e2e_j4.out,
coverage_e2e_j0.out · rowmatch_authors.py, rowmatch_authors.out · dropc4_stab128.out, dropc4_stab128_checkonly.out,
dropc4_stab128_noedgeswap.out · stab128_solvers.out

## Fix status (21Z seat)
All seven applied 2026-10-19 ~22:2xZ:
1. README §2 rewritten on their definitions + rowmatch_authors.py (13,541/13,541 rows, 13,351 kept = classes_all as sets).
2. campaign.sh: done ⟺ exact `UNSAT` (kissat) / `s UNSATISFIABLE` + `s VERIFIED` (drat); drat-trim gets `-t`; any SAT
   writes runs/ALARM_SAT and halts dispatch; `tally.py` added (exit 0 only when all 13,351 keys done, 3 on SAT).
   Mutation test of the to-do logic: rows with `none`, `s TIMEOUT`, `s NOT VERIFIED`, `UNKNOWN`, `SAT…` stay to-do;
   an empty output file yields all keys.
3. README §5 states what DRAT does and does not certify.
4. README §4 now cites the |Stab| = 128 controls and the `--check-only` mutation; edge-swap mutation added
   (`--es-check-only`: 5 violations vs 0, runs/edgeswap_mutation.out); 'these cells', not 'the cells'.
5. runs/first_probes.txt added.
6. README §5: n = 26, per-case means, class-weighted ~190 h, unconstrained tail, capped first pass + rerun queue, the
   300 h DRAT figure labelled as a one-cell extrapolation.
7. README §3 coverage sentence now includes the lex-least-of-orbit step and cites sb_order_check / coverage_e2e.
