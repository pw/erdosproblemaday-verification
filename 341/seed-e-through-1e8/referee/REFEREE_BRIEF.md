# Hostile referee brief — Erdős #341, seed E = {1,4,8,10,11,12} (2026-10-15)

You are refereeing a `/day/` entry before it is published. Your job is to REFUTE it. Quote the sentence you object to.
Verdict vocabulary: HOLDS AS READ / HOLDS WITH FIXES (list them) / GAP AT … (fatal). Report to `REPORT.md` in this directory.

## What is claimed (read `../entry/body.html`, `../entry/summary.txt`, `../entry/title.txt`, `../README.md`)
The entry claims (d) a finite non-periodicity bound for the Dickson greedy from E through 10⁸, (d) a structural characterisation
(no rail mod m ≤ 400, a near-period ladder with agreement ≤ ~0.99, bounded discrepancy, polynomial factor complexity),
(c) a conjecture of aperiodicity, (d) a SAT census that Li's shield conditions are unsatisfiable for every doubling cycle at every
modulus below 49, (d) a controller census (2- and 4-rail controllers periodic), and (d) a certificate census of all seeds with max 13 / 14.

## The problem statement (erdosproblems.com/341, `../live/page.txt`)
"extend it to an infinite sequence by defining a_{n+1} for n ≥ k to be the least integer exceeding a_n which is not of the form
a_i + a_j with i, j ≤ n" — equal indices allowed (Dickson's rule). Check that `../fast341.c` and `../greedy341.c` implement exactly this
(in particular that a_n + a_n is excluded, and that sums involving the seed elements themselves are excluded from the first step).

## What to attack, in order
1. **The generator.** Read `../fast341.c` line by line against the statement. Does the inner-loop truncation at min(t, N−t) lose any
   sum that matters for a position ≤ N? Does the carry form (`prev>>(64-r)`) ever drop a bit? Is the elems array large enough?
   Run it yourself on small seeds and compare to a from-scratch Python implementation YOU write (set-based, no bitsets) for
   several seeds to a few thousand, under both rules. The July control: SHA-256 through 500,000 = 3a045efe…
2. **The period test.** `../analyze.py` (border array) and the C probe in `fast341.c`: do they test what the entry says
   ("no gap period ≤ P terms beginning at or before term S")? Is the inference from "smallest period of the suffix > half its length"
   to that statement correct? Write a periodic control (any seed the July report certifies) and confirm the test detects it.
3. **The structural numbers.** Rerun `python3 ../analyze.py ../F_E_eq_1e7_elems.u32` and compare every number in the entry's third
   paragraph with the log. Check the arithmetic in the near-period ladder (889 = 253 + 636 etc.) and whether "Fibonacci-like" and
   "rotation" are claims or readings (they must be labelled as readings). Is "bounded discrepancy" supported, or is the density fitted on
   the same window (it is — say whether that matters)? Is the complexity slope quoted correctly?
4. **The shield SAT.** Read `../shield/shield_sat_L.py` against Li's Lemma 3.1 as reproduced in
   `~/ErdosProblemADay-1015-0000/verification/341/queneau-variant-56-for-77/PROOF.md` (section "The shield") and in Li's paper
   (`~/ErdosProblemADay-1015-0000/verification/341/li-disproof-refereed/`, find the PDF/tex). Does the encoding capture exactly his
   conditions? Is the claim "no Li-type shield at any modulus below 49" over-stated — e.g. are there cycle shapes, carry patterns, or
   cover types (P+P mixed sums, D+D) the encoding forbids that Li's argument would allow? Is the enumeration of doubling cycles
   complete (`../shield/cycles_below_49.txt`)? Run a few instances yourself.
5. **The controller census.** `../shield/census2.c`: are the carries right (rail j with predecessor i reads block q − c_i)? Is the
   "every rail nonempty on q ≤ q0" restriction justified by Li's Lemma 5 hypothesis? Could an initial content with q0 > 1 be aperiodic
   where q0 = 1 is not (the entry says q0 ≤ 3 for two rails, q0 = 1 for four)? Does "periodic to Q = 65536 with period ≤ 8000" prove
   periodicity (it does not — check the entry does not say it does; a suffix period is evidence, not proof, unless certified).
6. **The seed census.** `../census13/census.py` + the patched `certify.py`: is the patch `L = max(L, M+1)` sound (what does the July
   lemma require when the proposed onset N is ≤ max seed)? Does the driver's escalation logic ever call a seed CERTIFIED without a
   passing certificate, or UNRESOLVED when a certificate would pass at a larger N? Read `census13_run1_buggy.tsv` vs the fixed run.
7. **The three classic holes.** A lemma assuming the conclusion; a citation not saying what is claimed (Calkin–Erdős on "no known
   method" — find the sentence: `https://www.math.clemson.edu/~calkin/Papers/calkin_erdos.pdf`; Green's Problem 7 in `../lit/green.txt`);
   "clearly" at the hard step.
8. **Scope and register.** Does any sentence claim more than its label? Does the title or summary promise a proof? Is "smallest seed on
   record that resists every finite test" supported (what about seeds in [13], [14] from the census — read the tsv)?

Tools: you have the shell. Everything is under `~/MathDyad/erdos341e/`. Do not modify files outside `referee/`; write your own
scripts in `referee/`. Be specific: file, line, number.

## Addendum (01:0xZ) — a new instrument was added after you started
`../spectrum.py` (logs `../spectrum_E_1e7.log`, `../spectrum_S13_1e7.log`): the power spectrum of the indicator on [N/5, N], its
sharp peaks, and a test of whether the peak frequencies lie on a rank-r Z-module generated by the r largest independent peaks.
The entry now claims (d): E's 14 largest peaks (77% of the variance) all lie on Z f1 + Z f2 (f1 = 0.4386726, f2 = 0.1383678) within one
bin, 34 of the 40 largest, 81% of the variance within one bin of the 70 module points; {3,5,8,10,13} needs rank 3. Attack it: is the
"chance per peak" estimate right (the module points with |coef| ≤ 6 number ~169, bin width 1.3e-7)? Does parabolic refinement of the
generators bias the test? Could a periodic set with a very long period produce the same spectral picture (yes — say what the test does
and does not exclude)? Is the phrase "model set / two-frequency quasicrystal" labelled as a reading (c) and not a theorem?
