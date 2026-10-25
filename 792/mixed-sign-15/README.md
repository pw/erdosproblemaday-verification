# Erdős #792 — n = 15: every nonzero 15-set of integers contains a sum-free 7-subset (F*(15) = 7)

F*(n) = min over nonzero integer n-sets A of α(A), α = largest sum-free subset (a+b=c forbidden, a=b allowed).
The positive witness {1,2,3,4,5,6,8,9,10,18,100,200,10000,20000,1000000} has α = 7, so F*(15) ≤ 7. This bundle
is the lower bound: for every sign pattern (k negatives, k = 0..7; negation covers k = 8..14) the QF_LRA instance
"reals x_0<…<x_{n-1}, k of them negative, every 7-subset contains x_i + x_j = x_m" is UNSAT. Integers are reals
and scaling is a symmetry, so no integer 15-set has α ≤ 6.

## Two arms

**Direct (mixed792.py, z3, pruned atoms, one process per k).** `results_n15_12h.log` (12 h cap): k=0 (positive
case) UNSAT 2.0 h · k=1 UNSAT 4.5 h · k=2 UNSAT 5.4 h · k=3 UNSAT 8.6 h · k=4..7 TIMEOUT. `results_n15_long.log`
(36 h cap, `runjob15_long.sh`): k=4 UNSAT 52,386 s (14.6 h) · k=5 UNSAT 80,895 s (22.5 h) · k=6 UNSAT 86,658 s (24.1 h)
· k=7 UNSAT 84,155 s (23.4 h). So the direct arm alone closes every pattern; the cube arm is an independent second proof.

**Cube-and-conquer (cube792.py + cube_campaign.py, z3).** For k negatives, a_i = −x_i (a_0 > … > a_{k−1} > 0).
Give each negative i a slot r_i ∈ {k..n}: x_{r_i−1} ≤ a_i ≤ x_{r_i} (with x_{k−1} := 0 and x_n := +∞ sides free).
Because the inequalities are non-strict, the cubes COVER every real assignment (a tie lies in two cubes), so
"every cube UNSAT" ⇒ the pattern is UNSAT. Inside a cube the sign of each mixed sum x_i + x_j (i negative,
j positive) is known, so its atom set is pruned soundly: r_i ≤ j ⇒ x_i + x_j ≥ 0 ⇒ m ∈ [k, j); r_i > j ⇒
x_i + x_j ≤ 0 ⇒ m ∈ (i, k). The campaign fixes only the slots of the two OUTERMOST negatives (i = 0 and
i = k−1; the inner ones keep the plain prune rule), giving (17−k)(16−k)/2 cubes per k:

| k | cubes | UNSAT | min | median | max | CPU |
|---|-------|-------|-----|--------|-----|-----|
| 4 | 78 | 78 | 30 s | 884 s | 6,020 s | 29.1 h |
| 5 | 66 | 66 | 18 s | 659 s | 3,540 s | 15.6 h |
| 6 | 55 | 55 | 8 s | 472 s | 4,424 s | 13.4 h |
| 7 | 45 | 45 | 8 s | 332 s | 6,116 s | 12.6 h |

244 cubes, 244 UNSAT, 70.5 CPU-hours on 4 workers (nice 19), 2026-10-12 14:28Z → 2026-10-13 09:45Z. One cube
(k=7, `15,_,_,_,_,_,7`) hit the 2 h cap and returned UNSAT on the 8 h retry in 5,844 s; every cube line is in
`cube_campaign.log` (the `unknown` line and its retry are both kept). `logs/cube_k{4,7}_sample.log` are the
fine-cube timings (all C(15,k) slots fixed) that sized the campaign; `logs/cube_k7_partial_sample.log` the
partial-cube timings.

## Controls (`cube792.py --selftest --n 15`, output in the entry)
* cube count per k equals C(15,k) for the fine cubes (and the partial-cube pairs cover every fine cube's pair);
* for each k = 1..8 a hand witness with k negatives lands in a cube whose PRUNED atom set still contains every
  Schur relation the witness realises (missing_atoms = 0) — the pruning cannot discard a relation a real set uses;
* that cube is SAT at t = α(witness)+1 and the model re-checks exactly over the integers (sorted, nonzero, every
  t-subset covered, α computed by brute force).
The campaign itself is a one-sided (UNSAT) proof; a SAT cube would have been scaled to integers and re-checked
exactly before being believed (same code path as the n = 13 runs).

## Reproduce
    python3 cube792.py --selftest --n 15
    python3 cube_campaign.py --workers 4          # resume-safe; appends to cube_campaign.log
    ./runjob15_long.sh <k>                        # the direct arm, one k per process, 36 h cap
