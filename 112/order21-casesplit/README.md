# Erdős 112: the order-21 case split for k(3,4)

**Claim (pending the run):** no 21-vertex oriented graph is simultaneously free of independent triples
(I_3) and transitive 4-tournaments (L_4); with the known 20-vertex witnesses this gives k(3,4) = 21.

## The reduction (elementary)
Let v be any vertex of a hypothetical witness. N^+(v) and N^-(v) are (I_3, L_3)-free oriented graphs
(an L_3 inside N^+(v) plus v is an L_4; an I_3 inside is an I_3), so each has at most 8 vertices because
k(3,3) = 9. The non-neighbourhood N^0(v) is a tournament (two non-neighbours of v that are non-adjacent form
an I_3 with v) with no L_4, so it has at most 7 vertices (every 8-tournament contains a transitive 4-set).
As |N^+| + |N^-| + |N^0| = 20 and reversing all arcs lets us assume |N^+| ≥ |N^-|, the root profile is one of
(8,8,4), (8,7,5), (8,6,6), (7,7,6), (8,5,7), (7,6,7).

## The types (two independent enumerations agree)
`enum_types.py` enumerates, up to isomorphism, every (I_3,L_3)-free oriented graph on 3..8 vertices and every
L_4-free tournament on 3..7 vertices by SAT with orbit blocking; it asserts the two classical controls (none on
9 vertices; no L_4-free 8-tournament). Counts: oriented 5, 13, 25, 31, 7, **1** for n = 3..8; tournaments
2, 3, 3, 1, **1** for n = 3..7. `control_bruteforce.py` recounts n ≤ 5 / n ≤ 6 by exhaustive enumeration;
`types_control_geng.py` recounts n = 7, 8 by a different route (nauty-geng over underlying graphs with
α ≤ 2 and no K_4, then all cyclic-triangle orientations, canonical forms by permutation). Both agree.

## The cases
Fixing each neighbourhood of v = 0 to one labelled representative of each isomorphism type is lossless
(relabel inside each part). `cases112.py` writes one DIMACS CNF per (profile, type-triple):
3 + 21 + 31 + 49 + 25 + 217 = **346 cases**, each with every pair-state fixed inside the three parts and free
only across parts; the constraints are the definition (exactly-one state per pair, no independent triple,
no transitive 4-set) plus the valid redundant degree bounds.

## Positive control
`ORDER=20 python3 cases_any.py cases20` builds the same split at order 20, where witnesses exist; the run must
return SAT on some case and `check_any.py` must validate the model as a genuine 20-vertex (I_3,L_4)-free graph.
This is what shows the encoding is not over-constrained. (Result recorded in `control20_result.txt`.)

## Lossless symmetry breaking (for the hard tail)
Every automorphism σ of the fixed out-type (permuting the out-part's vertices), of the fixed in-type, and of the fixed
non-tournament extends to an automorphism of the whole case CNF: the definition-level constraints are vertex-symmetric,
arcs to the root are uniform within a part, and the other parts are untouched. So the solution set of a case is invariant
under G = Aut(N⁺) × Aut(N⁻) × Aut(N⁰), and adding the lex-leader constraints x ≤_lex σ(x) for every σ ∈ G, over the vector
of cross-part pair-state variables, keeps at least one solution of every orbit (Crawford–Ginsberg–Luks–Roy, KR 1996).
Hence UNSAT of the symmetry-broken CNF implies UNSAT of the case. `symbreak_case.py` verifies each σ against the fixed
arcs before using it, enumerates the full group (orders 3 to 7·24·21 = 3,528 across the 72 hard cases; the order-3,528 case is
p767_o6_i30_n0, an out-type with 7 automorphisms, an in-type with 24, and the Paley non-part), and writes `<case>_sb.cnf` + `<case>.sb.json` (group sizes, clause counts). Controls: the order-20 witness
case stays SAT under its group of order 21 and the model validates (`control20_symbreak.json`); the solved order-21 case
p884_o0_i0_n0 (group order 192) closes UNSAT in 26 s under symmetry breaking versus ~90 s plain on the same loaded box.
`rerun_sb.sh` races cadical/kissat on the `_sb` instances and replays the winner's DRAT with drat-trim; a verdict
obtained this way is recorded as `UNSAT-VERIFIED <secs> sb-<solver>` in the parent case's status line.

**Result of the symmetry-broken pass (2026-10-11):** all 72 cases that had timed out plain closed UNSAT-VERIFIED —
43 by cadical, 29 by kissat, mean 79 s, longest 418 s (p767_o6_i30_n0, group order 3,528); every winning DRAT replayed
by drat-trim. Per-case group sizes and clause counts are in `sb/<case>.sb.json`; verdicts and timings in `statuses.txt`
(the `sb-c`/`sb-k` suffix marks the 72).

**Orbit control (`sbcontrol.py`, log `sbcontrol.log`).** The lex-leader clauses are tested per case independently of
the problem constraints: for each of the 73 symmetry-broken CNFs (the 72 plus p884_o0_i0_n0, which had closed plain
in the meantime) the group G is recomputed by brute force, three random cross-part pair-state vectors are orbited under
it, and cadical is asked whether the appended clauses alone are satisfiable with the cross vector pinned to (a) the
lex-minimum of the orbit — must be SAT, or the clauses would be losing solutions — and (b) the lex-maximum and a random
other orbit member — must be UNSAT, or the clauses would be vacuous. 219 draws, 0 failures, orbit sizes equal to the
full group order throughout.

**Plain re-runs.** Four of the 72 symmetry-broken cases — `p776_o6_i6_n0` (group 147), `p767_o2_i13_n0` (21), `p767_o6_i26_n0` (147), `p767_o6_i29_n0` (588) — were re-run PLAIN (no symmetry clauses) with a four-hour budget as a decorrelated check: cadical returned UNSAT on all four in 15–21 minutes, and drat-trim replayed each plain proof to `s VERIFIED` (809 / 1,515 / 2,602 / 1,717 s; `<case>.plaincheck.verify`). The plain DRATs (0.5–0.6 GB each) are not shipped.

## The run
`run_cases.sh cases 10 1800`: cadical with DRAT proof logging per case, every UNSAT proof replayed by drat-trim
(`s VERIFIED`), any SAT model checked by `check_witness.py` against the definition. Per-case verdicts in
`statuses.txt`; proofs are not shipped (18 MB each) but are reproducible from the CNFs.
