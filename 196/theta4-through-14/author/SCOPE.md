# Exact scope

## Computational claim

For n in [1,14], let theta_4(n) count permutations p of [n] for which there are no integers a and
d > 0 such that a, a+d, a+2d, a+3d all lie in [n] and their positions in p are strictly increasing
or strictly decreasing. The claimed values are exactly those in expected_counts.tsv.

This is an exhaustive-computation claim. It is conditional on the ordinary software and hardware
trust boundary: correct compilation, execution, integer arithmetic, and file integrity.

## Elementary claims

REPORT.md gives checkable proofs of:

1. The endpoint recursion visits every avoiding permutation once and rejects every forbidden one.
2. Value complementation pairs distinct ordered two-value prefixes and preserves avoidance.
3. The number of four-term AP subsets of [n] is q*n - 3*q*(q+1)/2 for q = floor((n-1)/3).
4. Total AP-permutation incidence is n! times that subset count divided by 12.

These statements do not depend on the numerical output through n = 14.

## Source-status claims

The live-page facts and local-source collision facts are snapshot claims dated 2026-08-11. Their raw
captures are frozen under provenance/. The literature statement that no matching exact table was
found is search-limited. It is not a proof that no earlier table exists.

## Explicit exclusions

- No solution of the singly infinite problem is claimed.
- No upper or lower asymptotic estimate for theta_4(n) is claimed.
- No implication from finite nonzero counts to an order of type omega is claimed.
- No publication novelty or OEIS absence theorem is claimed.
- No site source was edited or deployed by this work.

The 1977 construction already gives a doubly infinite AP-free order of the positive integers.
Restricting it gives a finite avoider for every n. The unresolved issue is obtaining a singly
infinite order: a coherent construction must control predecessor sets/order type, not only every
finite forbidden pattern.
