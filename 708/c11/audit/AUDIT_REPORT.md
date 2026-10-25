# Hostile audit: integrated Erdos 708 `c_11` candidate

Date: 2026-08-11 UTC

## Verdict

**PASS for the corrected integrated candidate.**

The audited proof snapshot is

```text
6a49dabc87e9020446490ab6b1ce54215ce6f9c1fe2534e739d7b2eb1c9c4f6c  erdos708_c11_candidate.md
26b7ddb74cab0b3b78a39fd7e0369736548d96162b24a637e9faf9e19ab968dc  erdos708_c11_full_audit.py
```

The proof establishes `c_11<=2` from the published `c_10` inputs and the two
separately frozen eleven-edge companion audits.  The private-prime padding
construction establishes `c_11>=2`.  I found no remaining mathematical gap
in their integration.

This verdict supersedes neither companion audit: their exact frozen scope and
hashes remain part of the dependency chain.  Copies of their reports and the
audited source files are under `inputs/`.

The current companion prose has harmless post-audit edits.  The placement
note now has hash `af0730a4...`; relative to its frozen audited snapshot it
only repairs mathematical typography, updates scope wording, and spells out
the already-audited absent-`C_j` discard branch.  The new-kernel note now has
hash `0c9d22fa...`; its only substantive-looking addition is the elementary
sentence that both active bipartition classes have size at least two.  The two
checker changes only replace their final scope-status strings.  Direct diffs
found no changed certificate, inequality, classification row, or executable
check.

## Structural reduction and inherited cores

For an inclusion-minimal maximum-defect core, every component has positive
defect and every active vertex has degree at least two.  A positive-defect
simple bipartite component needs at least six edges, so at most eleven edges
permit only one component.  The bipartite edge bound on `e-q` active vertices
then gives exactly the ranges in the candidate; `q=4,e=11` forces
`K_(3,4)-e`, and larger defect is impossible.

The independent checker enumerated labelled graphs and tested every proper
edge subset directly.  It discovered, rather than copied, the inherited
classes:

```text
q=2: 2 classes at e=8, 2 at e=9, and 10 at e=10;
q=3: K3,3 at e=9, K2,5 at e=10, and 2 minimal K3,4-minus-two classes.
```

The labelled counts include 96 `q=2,e=9` graphs, 210 and 2,040 graphs in the
two `q=2,e=10` shapes, and 54 minimal `q=3,e=10` `K_(3,4)` deletions.  All
15,324 proper subsets of the discovered representatives passed.

## Joint Hall placement and the singleton collision

The multi-repair Hall bounds use exactly the thresholds

```text
(q,s)=(2,2): 10; (3,2): 9; (3,3): 10.
```

The strict open-interval count and the nine/ten-point progression lemmas
exclude all such deficient sets.  If a deficient set remains, it has the form
`R+{d}`, with `R` tight and `Z(d)\V` contained in `N(R)`.  Supermodularity
shows that two distinct repairs cannot each occur in a deficient set.  After
deleting the unique bad repair, Hall holds; contracting the tight set matches
all other items outside `N(R)`.

Choose `z` in the bad repair neighbourhood.  A perfect matching of `R` onto
`N(R)` makes `z` represent an outside edge `e_0`.  With
`g=gcd(d,a_(e0))`, the support condition supplies a sixth divisible label in
the only tight counting case, hence a fresh `g`-multiple `w`.  The identity

```text
lcm(d,a_(e0)) gcd(d,a_(e0)) = d a_(e0)
```

proves that `z*w` restores the complete product with no valuation loss.

An abstract exhaustion, independent of graph geometry, checked 39,663 small
set systems satisfying the edge-only and multi-repair Hall hypotheses.  Among
1,840 non-Hall families it checked 2,224 deficient singleton-repair tight sets;
all had a unique bad repair and all contractions satisfied Hall.

## Aligned robustness and midpoint avoidance

For every one of the 14 inherited fixed-block `q=2` classes and the three
relevant fixed-block `q=3` classes, the independent checker generated every
exceptional matching, every endpoint set `W`, and every deletion
`Y subset X intersect K[W]`.  It found support tuples satisfying the actual
level demand and

```text
|B union (E(K-v) minus X)| >= 5
```

for every block and vertex.  All 907 matchings on minimal cores passed.

The supplied checker's total is 954 because it deliberately includes 47
matchings on the redundant same-column `K_(3,4)` deletion, which contains a
proper `K_(3,3)` core.  Thus the count difference is fully explained and is
not a missing isomorphism class.

Strict counts for labels below `M`, the endpoint-safe fifth label, and the
extra forbidden point `b_0` make the singleton and collision arguments valid.
Every selected endpoint and repair point avoids `b_0`; adjoining `b_0` only
after covering `A_0` avoids the double-counting error from the original
aligned `c_10` draft.

## Exceptional kernels

For `K_(2,5)`, the strengthened Konig argument was re-enumerated in all 107
denominator profiles.  Every divisor capture has size at most two, including
the `(2,2,3,3)` equality profile.  All 608 aligned endpoint/deleted-matching
levels satisfy the order-statistic demand, and 3,125 capped column-valuation
vectors confirm that the gcd of triple products is the sum of the three
smallest column valuations.

For `K_(3,4)-e`, all 17 positive endpoint levels independently recover exactly
the 45 advertised admissible four-block tuples.  The separately frozen Rado
placement audit proves that one such tuple has four distinct outside
representatives.  The corrected integrated snapshot explicitly handles both
equal-column discard branches, including the case in which `C_j` was not one
of the three selected `C` blocks.

## Lower bound

The public padding verifier stops at `n=10`, so it is not itself an `n=11`
certificate.  `LOWER_BOUND_PROVENANCE.md` records the uniform PNT prime-choice
argument that makes the published construction approach ratio two for every
fixed number of private primes.  The independent code also constructs an
explicit seven-private-prime instance with 20,805 integer points and 15
valuation types; exact DP gives minimum cover 12.  The finite instance is
corroboration, not a replacement for the uniform argument.

## Reproduction and scope

Run:

```bash
./run_all.sh
```

The independent run additionally checked 231,000 concrete strict-progression
pairs.  The finite searches certify the graph and set-system interfaces; the
written Hall, progression, prime-power layer, gcd/lcm, and PNT arguments cover
arbitrary intervals and valuations.

Publication should preserve the corrected candidate hash above, publish or
link both companion audit bundles, and make the one-paragraph PNT
prime-selection step explicit near the lower-bound citation.  The supplied
padding verifier should also be extended from `r<=6` to `r=7` for consistency,
although that code change is not logically needed once the theorem is stated.
The candidate's line-5 status still says "pending an independent cold audit";
that status should be updated when this PASS is promoted.
