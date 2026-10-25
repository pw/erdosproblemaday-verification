# Erdős #792 — the mixed-sign residual at n = 13: F_*(13) = 6

**Question.** F_*(n) = min over nonzero integer n-sets A of alpha(A), alpha = size of the largest sum-free subset
(a+b=c forbidden inside the subset, a=b allowed). Our wave-7m report (`/report/792`) had F_*(13) ∈ {5, 6}: Bourgain's
theorem gives ≥ 5, the set {1,2,3,4,5,6,8,9,10,18,100,200,300} gives ≤ 6, and the POSITIVE case was settled (every positive
13-set has a sum-free 6-subset: z3 UNSAT, report §4). Left open: a 13-set with both signs reaching alpha = 5.

**Reduction.** Negation preserves Schur relations, so assume k ∈ {0,…,6} negatives. For each k, `mixed792.py k` asks:
do reals x_0 < … < x_12, exactly k negative (x_{k-1} < 0 < x_k = 1 after scaling), exist such that EVERY 6-subset contains
some x_i + x_j = x_m (i ≤ j, m ∉ {i, j})? QF_LRA; integers are reals and scaling is a symmetry, so UNSAT ⇒ no integer set.
A SAT model would be scaled to integers and re-checked exactly (`every_subset_covered` + brute-force alpha) before being
believed. Atoms are pruned by order+sign (`--prune`, default): positives sum above both, negatives below both, a negative
plus a positive lands strictly between. `--no-prune` keeps every (i ≤ j, m) — a second, independently coded encoding.

**Controls (`controls.log`).** k=0,t=6 (the known UNSAT) reproduces: z3 unsat 51.6 s. SAT controls at t=7 (alpha ≤ 6 is
attainable for every sign split): k=0 z3 → {60,…,480} alpha 6; k=3 z3 pruned → {−205,…,328} alpha 6; k=3 cvc5 unpruned →
{−73,−72,−36,4,8,12,16,20,24,32,36,40,72} alpha 6 — every model re-checked from the definition. (cvc5 unpruned on k=0,t=6
hit the 600 s control cap — slow, not wrong; the production cvc5 runs use the pruned encoding.)

**Runs (`jobs.txt`, `runjob.sh` → `logs/`, verdict lines in `results.log`).** k = 1..6 × {z3 pruned, z3 unpruned,
cvc5 pruned}, nice 19, 6-hour cap each, plus the next positive rung n=15, t=7 (z3 pruned). `ship792.py` refuses to publish
unless all six patterns are UNSAT on both z3 encodings, and prints cvc5's coverage.

**Reproduce.** `python3 -m venv v && v/bin/pip install z3-solver cvc5` then `v/bin/python mixed792.py 3 --t 6`
(≈5 min), `--engine cvc5`, `--no-prune`; controls: `mixed792.py 0 --t 6` (unsat), `mixed792.py 3 --t 7` (sat + witness).
z3 5.1.0 and the cvc5 Python wheel current on 2026-10-11 were used.

**cvc5 12-hour re-runs (2026-10-12, `jobs_cvc5_long.txt` → `logs/k<k>_cvc5_prune_long.log`, verdicts in `results_cvc5_long.log`).** The four patterns that hit the 6 h cap all returned UNSAT under a 12 h cap: k=2 33,980 s · k=4 31,622 s · k=5 29,968 s · k=6 34,039 s. With k=1 (4,579 s) and k=3 (16,520 s) from the first pass, cvc5 confirms all six patterns; z3 confirms all six on both encodings.
