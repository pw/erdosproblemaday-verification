# Erdős problem 352: exact finite value `f(17)=32`

Date: 2026-08-12 (UTC)

## Scope and claim label

Let `f(N)` denote Koizumi's lattice quantity: the largest cardinality of a
finite set `S` of lattice points such that, for every triple `p,q,r` from `S`
with repetitions allowed,

\[
  \left|\operatorname{area}(\triangle pqr)-N\right|
      > \operatorname{diam}(\triangle pqr).
\]

The new finite result is

\[
                         \boxed{f(17)=32}.
\]

This is **[d: computational-only]**: a finite exhaustive proof with standalone
exact-integer checkers. It extends the earlier exact table through `N=16` by
one row. It does not prove `f(N)=O(N)` and hence does not solve the original
continuous Erdős problem 352, which remained open with no proof claims on the
live page when checked on 2026-08-12.

The 32-point lower witness was posted previously by BorisAlexeev and is
available in KentaKitamura's public witness repository. The contribution here
is the exhaustive upper bound; no priority claim is made for the witness.

## Exact predicate and lower bound

For lattice points define

\[
 A_2=|\det(q-p,r-p)|,
 \qquad
 D_2=\max(|p-q|^2,|p-r|^2,|q-r|^2).
\]

The avoiding condition is exactly the integer inequality

\[
                    (A_2-34)^2-4D_2>0.                 \tag{1}
\]

The witness is

```text
(0,0), (0,1),
(1,-1), (1,0), (1,1), (1,2), (1,3),
(2,-1), (2,0), (2,1), (2,2), (2,3),
(3,-1), (3,0), (3,1), (3,2), (3,3), (3,4),
(4,-1), (4,0), (4,1), (4,2), (4,3), (4,4),
(5,0), (5,1), (5,2), (5,3), (5,4),
(6,1), (6,2), (6,3).
```

The checker evaluates all
`binom(32+2,3)=5,984` triples with repetition. Every gap in (1) is positive;
the minimum is 5. Thus `f(17)>=32`.

## Exhaustive upper-bound reduction

Applying the condition to `(p,p,q)` shows that every pair has distance less
than 17. Choose a diameter pair, translate one endpoint to `A=(0,0)`, and use
a lattice-preserving dihedral symmetry to put the other at

\[
 B=(b_x,b_y),\qquad b_x\ge b_y\ge0,\qquad
 0<b_x^2+b_y^2<17^2.
\]

There are 125 such normalized vectors. Every other point lies in the finite
two-disc lens centered at `A,B` with radius `|A-B|`. The checker exhausts a
provably complete integer box, imposes both lens inequalities, and tests (1).

For each `B`, candidates are split according to whether
`area(ABq)<17-|A-B|` (low) or `area(ABq)>17+|A-B|` (high). The no-high branch
fixes `A,B`; every branch containing a high point is covered by trying each
possible high point `H` and fixing `A,B,H`. This gives 125 no-high branches and
9,414 fixed-high branches.

For each fixed set, form the compatibility graph on remaining candidates:
two vertices are adjacent exactly when they can coexist with the fixed points
and the chosen diameter. An actual avoiding extension is a clique. Therefore
any proper `k`-coloring bounds the extension by `k`; optimal coloring is not
needed. The checker constructs deterministic greedy colorings, then audits
every same-color pair with a second shoelace/dot-product implementation and a
full triple scan. Across all 9,539 certificates, it audits 1,534,917
same-color pairs. Every branch is thereby bounded by 32 except one: the
no-high branch with `B=(5,4)` has a 40-candidate pool and a pairwise relaxation
of 31 candidates, or 33 total points.

## The exceptional `B=(5,4)` certificate

Let `G` be the incompatibility graph on those 40 candidates: two candidates
are adjacent when they cannot coexist with `A=(0,0), B=(5,4)`. Exact
reconstruction gives 48 edges. The following nine edges are disjoint:

```text
(-1,2)--(4,0)    (-1,3)--(3,0)    (0,3)--(4,-1)
(0,4)--(2,-1)    (1,-1)--(4,5)    (1,4)--(6,1)
(1,5)--(5,1)     (2,5)--(5,0)     (3,5)--(6,2)
```

Hence a pairwise-compatible subset contains at most one endpoint from each
pair and has size at most `40-9=31`. If it has size 31, its omitted 9-set must
contain exactly one endpoint of every displayed edge and no unmatched vertex.
There are only `2^9=512` such choices. The checker audits all 512 against all
48 incompatibility edges. Exactly two are vertex covers:

```text
O1 = {(-1,2),(-1,3),(0,4),(1,-1),(1,5),(4,-1),(5,0),(6,1),(6,2)}
O2 = {(-1,2),(-1,3),(0,4),(1,5),(4,-1),(4,5),(5,0),(6,1),(6,2)}.
```

The complement of `O1` contains the triple

```text
(0,3), (3,-1), (4,5),
```

and the complement of `O2` contains

```text
(1,-1), (2,5), (5,1).
```

For each triple, `A_2=22` and `D_2=37`, so its exact gap is

\[
                    (22-34)^2-4\cdot37=144-148=-4.
\]

Thus neither 31-candidate set is avoiding. The exceptional branch contains at
most 30 candidates, hence at most 32 points after adjoining `A,B`. Combined
with every other audited branch, this proves `f(17)<=32` and therefore
`f(17)=32`.

## Audit totals and reproducibility

```text
normalized diameter cases       125
cases having high candidates     94
fixed-high branches           9,414
color certificates            9,539
candidate-pool memberships  260,479
same-color pairs audited   1,534,917
largest branch pool              106
matching choices audited         512
surviving 9-vertex covers          2
full certificate SHA-256
  dd1b957a56174169a95cc31fd68d77b47d51dd38745f6252059954b74aad78e2
```

The full standalone run took 113.40 seconds (`user=113.19`, `sys=0.08`) and
20,292 KiB maximum resident memory on the exe.dev VM. The 207-line focused
matching checker independently rebuilt the witness and exceptional branch in
0.09 seconds.

As a cross-implementation check, the public upper-bound code at commit
`7a4a19468771766cb4f20e10dfa5cf770cc2487b` independently reproduced all 125
diameter cases, all 9,414 high branches, and showed that `B=(5,4)` is the only
case whose pairwise relaxation exceeds 32. The public witness verifier at
commit `09e5c5393943c881ab60118aa32fe5660539c8d5` independently returned size
32, 5,984 triples, and minimum gap 5.

Reproduce from `verification/352/f17-exact`:

```bash
python3 erdos352_n17_matching_audit.py
python3 erdos352_n17_verify.py --min-n 17 --max-n 17 --json
```

PARTIAL: Exact exhaustive integer certificates prove `f(17)=32` in Koizumi's
equivalent lattice model. Erdős problem 352 remains open because no uniform
bound `f(N)=O(N)` is proved.
