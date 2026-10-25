# Erdős 789: h(n) = 5 for 20 ≤ n ≤ 27

This directory certifies the exact finite values

```text
h(20) = h(21) = … = h(27) = 5
```

for Erdős problem 789 (live-page definition: for a set A of integers, h(n) is the largest k such that
every n-element A ⊆ ℤ contains a k-element B in which equal subset sums force equal subset sizes).
It does not improve either asymptotic bound; (n log n)^{1/3} ≪ h(n) ≪ n^{1/2} stand.

## The chain

1. **Lemma (SMT, two solvers).** Every 10 distinct positive reals contain a 5-element subset B such that
   no two disjoint nonempty sub-subsets of different sizes have equal sums. For positive numbers this is
   exactly admissibility (cancel the common part; the smaller side cannot be empty since a nonempty set of
   positives has positive sum). Its negation — ten ordered positive unknowns, every one of the 252
   five-subsets satisfying one of its 65 "bad" linear equations — is a quantifier-free linear-real-arithmetic
   sentence. z3 5.1 returns `unsat` (602 s); cvc5 returns `unsat` independently (see `cvc5_10_5_output.txt`).
   Real UNSAT implies integer UNSAT. The exact instance is `lemma_10_5.smt2.gz` (SMT-LIB 2).
2. **Pigeonhole (elementary).** A 20-element integer set has at most one zero, hence at least ten nonzero
   elements of one sign; negating a set preserves admissibility. So every 20-set has an admissible
   5-subset: h(20) ≥ 5, and by monotonicity h(n) ≥ 5 for n ≥ 20.
3. **Obstruction (exhaustive, re-verified here).** H([−11,11]) = 5: the 23-element interval has an
   admissible 5-subset and no admissible 6-subset (`hint.py 11` checks all 100,947 six-subsets against the
   literal definition). So h(23) ≤ 5, and by monotonicity h(n) ≤ 5 for n ≤ 23.

4. **Obstruction, extended (exhaustive, `obstruction25.py`).** z3 found twelve positives with no admissible
   6-subset (`z3_12_6_output.txt`, 11,251 s): P = {1,3,4,5,6,8,9,10,12,14,15,17}. The symmetric set
   {0} ∪ ±P (25 integers) has an admissible 5-subset and none of its 177,100 six-subsets is admissible,
   so h(25) ≤ 5 (`obstruction25_output.txt`). Greedy symmetric extension (`greedy_extend.py`) adds ±2:
   {0} ∪ ±{1,2,3,4,5,6,8,9,10,12,14,15,17}, 27 integers, 0 of 296,010 six-subsets admissible
   (`obstruction27_output.txt`), so h(27) ≤ 5 and, by monotonicity, h(n) ≤ 5 for n ≤ 27. No single ±x ≤ 80
   extends it further (`greedy_extend_output.txt`).

## Controls (all in the logs)

- (m,k) = (6,4): `unsat` on both solvers — the known "every six positive integers contain an admissible
  four-subset" (our wave-w015 report proved it by exact hyperplane enumeration).
- (5,4): `sat`, witness {2,3,4,6,9} (z3) / {1,2,3,5,6} (cvc5), every 4-subset re-checked bad by the
  literal definition — the encoding can find counterexamples.
- (9,5): `sat`, witness {1,2,3,4,5,6,7,8,10} (every 5-subset re-checked bad) — the lemma is sharp: nine
  positives do not suffice, so the pigeonhole step genuinely needs n ≥ 20.

## Reproduce

```bash
python3 -I hint.py 11            # H([-11,11]) = 5
python3 lemma789.py 6 4          # unsat (control)
python3 lemma789.py 5 4          # sat + re-checked witness (control)
python3 lemma789.py 9 5          # sat + re-checked witness (sharpness)
python3 lemma789.py 10 5         # unsat  (~10 min, z3)
python3 lemma789_cvc5.py 10 5    # unsat  (cvc5, independent)
```
`pip install z3-solver cvc5`. The verdicts are solver outputs, labelled (d) computer-assisted; no proof
certificate is extracted (QF_LRA unsat cores are not independently checkable by a simple tool), which is
why two unrelated solvers are run on the same SMT-LIB instance.
