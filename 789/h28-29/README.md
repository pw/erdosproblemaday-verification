# Erdős #789 — h(28) = h(29) = 5, h(n) ≤ 6 through n = 39, and the lemma that does not continue

> **Update 2026-10-24 (09:00Z erdos tick):** the (16,6) order-pruned z3 run (`runp.sh 16 6`, no time limit, `ulimit -v` 20 GB)
> logged `(m=16,k=6) engine=z3 patterns=78/231 clauses=8008 disjuncts=624624 -> unknown in 92229.6s` (ended 2026-10-14 ~12:36Z);
> z3's reason was not logged — with no timeout set, memory exhaustion is the likely cause. h(32) ≥ 6 is NOT certified by this route
> and the run was not relaunched. The (15,6) pruned run returned SAT after 233,729.6 s with the 15-set already in this bundle
> ({1..10,12,14,18,19,23}; its own every-6-subset re-check passes). Lines 58–59 and 72 below ("open and running") are history.

h(n) = the largest k such that every n-element set of integers contains a k-element subset in which equal subset
sums force equal subset sizes (admissible). Admissibility is tested literally with `hcheck.admissible` (all nonempty
S,T ⊆ B, sum(S)=sum(T) ⇒ |S|=|T|; 0 and negatives allowed), the same checker as the `h20-23-exact` bundle.

h is non-decreasing in n (drop an element). So one n-set with no admissible k-subset proves h(n') ≤ k−1 for every
n' ≤ n, and the lower bound h(n) ≥ 5 for n ≥ 20 is the `h20-23-exact` lemma (every ten positive reals contain an
admissible 5-subset + pigeonhole). This bundle supplies the sets.

## 1. Signed-window search (`signedsearch789.py N k m0`)
Pure SAT over y_v for v ∈ [−N, N]: one clause per ADMISSIBLE k-subset of the window ("not all chosen"), a totalizer
cardinality constraint |A| ≥ m, m raised until UNSAT (cadical via pysat). Every witness is re-checked exhaustively:
all C(|A|,k) subsets through `hcheck.admissible`. UNSAT at m means only "no such m-set inside this window".

k = 6 (`logs_signedsweep_6.log`), largest A ⊆ [−N,N] with no admissible 6-subset:

| N | ints | admissible 6-subsets | max |A| |
|---|------|----------------------|--------|
| 11 | 23 | 0 / 100,947 | 23 (the whole interval — reproduces H([−11,11]) = 5) |
| 12 | 25 | 2 / 177,100 | 23 |
| 14 | 29 | 16 / 475,020 | 27 (reproduces the h20-23-exact 27-point obstruction) |
| 17 | 35 | 222 / 1,623,160 | 29 |
| 20 | 41 | 2,044 / 4,496,388 | 29 |
| 23 | 47 | 14,654 / 10,737,573 | 29 |
| 26 | 53 | 83,788 / 22,957,480 | 29 |

The 29-set found in [−26,26] is symmetric: A = {0} ∪ ±{1,2,3,4,5,6,7,8,9,10,12,14,15,16}; none of its 475,020
six-subsets is admissible (exhaustive re-check, 3 s). **Hence h(28) = h(29) = 5.** Every window from [−17,17] up
returns UNSAT at m = 30, so no 30-set inside [−26,26] avoids an admissible 6-subset — evidence, not proof, that
h(30) = 6.

k = 7 (`logs_signedsweep_7.log`, `logs_signedsweep_7b.log`), largest A with no admissible 7-subset:

| N | ints | admissible 7-subsets | max |A| |
|---|------|----------------------|--------|
| 14 | 29 | 0 / 1,560,780 | 29 (the whole interval) |
| 17 | 35 | 6 / 6,724,520 | 33 |
| 20 | 41 | 90 / 22,481,940 | 37 |
| 23 | 47 | 616 / 62,891,499 | 39 |
| 26 | 53 | 2,746 / 154,143,080 | 41 |
| 29 | 59 | see `logs_signedsweep_7b.log` | 43 |
| 32 | 65 | 33,336 / 696,190,560 | 43 |
| 35 | 71 | 101,500 / 1,329,890,705 | 43 |

The 43-set from [−29,29] is {0} ∪ ±{1,…,12,14,15,16,18,20,21,25,27,28}; none of its 32,224,114 seven-subsets is
admissible (exhaustive re-check, 194 s). **Hence h(n) ≤ 6 for all n ≤ 43.** The growth (29 → 33 → 37 → 39 → 41 → 43) then stops: [−32,32]
and [−35,35] (`logs_signedsweep_7c.log`, 1.6 h and 2.4 h to classify) both give 43 and are UNSAT at 44 — the same plateau the
6-subset search shows at 29. Evidence, not proof, that h(44) = 7.

## 2. The positive-reals lemma stops at m = 13 (`intsearch789.py N m k`, `logs_intsweep_14_6.log`, `logs_intceiling_6.log`)
The route that produced h(20..27) was: "every m distinct POSITIVE reals contain an admissible k-subset" (QF_LRA,
two solvers) + pigeonhole (an n-set has ≥ ⌈(n−1)/2⌉ nonzero elements of one sign) ⇒ h(2m) ≥ k. The next rung,
(m,k) = (14,6), ran 36 hours on z3 without a verdict. It is FALSE, and an integer SAT search finds the witness in
3 seconds: {1,2,3,4,5,6,7,8,9,10,11,14,15,16} ⊂ [1,17] has no admissible 6-subset (every one of its 3,003
six-subsets re-checked). So does a 15-set, {1,…,10,12,14,18,19,23} ⊂ [1,24]. No 16-set exists in [1,24], [1,28]
or [1,32] (UNSAT at m = 16, 24–200 s each). Consequently the pigeonhole route cannot certify h(30) ≥ 6 or h(31) ≥ 6
at all (it would need the false (15,6)); the first value it can still reach is h(32) ≥ 6 via (16,6), which is open
and running (`lemma789p.py`, the order-pruned encoding of §3). The symmetric closure of the 15-set,
{0} ∪ ±{1,…,10,12,14,18,19,23} (31 integers), does contain admissible 6-subsets (86 of 736,281, e.g.
{−23,−19,−14,−10,−6,3}), which is why the signed search, not the closure, gives the upper bounds above.

Controls for the integer search: the known (12,6), (13,6) and (9,5) witnesses are recovered; the proved lemma (10,5)
returns UNSAT in [1,22].

## 3. Order-pruned encoding (`lemma789p.py`)
For a k-subset with positions p_0 < … < p_{k−1}, a bad equation sum(S) = sum(T), |S| < |T|, is kept only if some
strictly increasing positive k-vector satisfies it (231 → 78 patterns for k = 6; 65 → 21 for k = 5). Dropping an
equation the order makes impossible is sound. Self-test: no known witness ((9,5), (12,6), (14,6)) satisfies a dropped
equation on any of its k-subsets, every subset is still covered by a kept pattern, and (6,4)/(5,4)/(9,5) reproduce.
Effect: (12,6) SAT in 116 s against 11,251 s for the unpruned encoding in `h20-23-exact`. Limits: pruned z3 still returned `unknown` on (14,6) at a 1 h cap (`lemma_14_6_pruned.log`) — the SAT side belongs to
the integer search; (15,6) and (16,6) pruned runs are open-ended and memory-capped.

## Reproduce
    python3 signedsearch789.py 26 6 27      # 29-set, exhaustive re-check
    python3 signedsearch789.py 23 7 29      # 39-set, exhaustive re-check
    python3 intsearch789.py 17 14 6         # the positive 14-set that refutes lemma (14,6)
    python3 intsearch789.py 32 16 6         # UNSAT: no positive 16-set in [1,32]
`pip install python-sat`; `hcheck.py` and `lemma789.py` are copied from `h20-23-exact`.
