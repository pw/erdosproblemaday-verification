# Hostile audit: Erdős #352 lattice value at N=18

## Verdict

**PUBLISH.** The proposed computational-only finite result is sound:

\[
f(18)=34
\]

for Koizumi's N-avoiding lattice model, with repetitions allowed in the
triangle triple.

This audit found no missing diameter orbit, lens point, low/high branch,
fixed-high branch, pair condition, or 33-candidate survivor. The result is a
finite exact value only; it neither proves `f(N)=O(N)` nor solves the continuous
problem.

## Definition and exact predicate

A finite `S` in the integer lattice is N-avoiding when every triple `p,q,r` in
`S`, including repetitions, obeys

\[
|\operatorname{area}(pqr)-N|>\operatorname{diam}(pqr).
\]

If `A2` is twice the absolute area and `D2` the squared diameter, this is
equivalent to the exact integer test

\[
(A2-2N)^2-4D2>0.
\]

The independent 100-decimal radical audit compared the literal inequality and
the integer predicate on all 7,140 witness triples and all 26,680 raw base-lens
triples. Every sign agreed. The base-lens scan contains 96 exact zero-margin
triples, so strict `>` rather than `>=` is materially exercised.

## Completeness of the upper reduction

For a repeated triple `(p,p,q)`, the condition gives `|p-q|<18`. Hence every
nontrivial avoiding set has a diameter pair of squared length below 324.
Translation and the eight signed-coordinate/swap isometries put it at

```text
A=(0,0), B=(b_x,b_y), b_x >= b_y >= 0.
```

Independent signed-vector orbit accounting gives exactly 1,004 raw nonzero
vectors and 140 D4 classes.

Every other lattice point lies in the closed two-disc lens of the diameter
pair. Because the diameter is below 18, the finite coordinate box used by the
program is complete. Every base candidate passing the strict `A,B,q` test is
necessarily either below the forbidden area band or above it. Thus every
avoiding set occurs in either the no-high branch or at least one branch with a
fixed high point `H`.

Within a branch, candidates of a genuine avoiding extension form a clique in
the pair-compatibility graph. Any proper coloring therefore gives an upper
bound, even though compatibility of pairs is only a relaxation of compatibility
of all candidate triples.

## Full independent branch audit

The hostile implementation `audit_352_n18.py` does not import the producer. It
uses shoelace area, polarization distance, explicit triple loops, set-based
dynamic DSATUR coloring, and explicit exceptions rather than Python asserts.
It independently obtained:

```text
diameter directions       140
directions with high      108
fixed-high branches     12594
all branches            12734
pool memberships       446938
maximum branch pool       129
sole loose coloring   B=(5,4), no-high, 33 colors vs cap 32
global upper bound          34
tight B             (5,4),(6,3),(5,5),(7,1),(7,2)
```

Its independent branch and diameter transcript hashes are:

```text
branch    69e0a1d66b168707a9365f45d110986c8b9d45a79ba7e00f2f1b97740b3fd7e6
diameter  760ad48430895eb53b36af3415831bd722773a04a6526df2226b7e541a8b563b
result    616c7c69a8f61e9e948353970ace843f4355e62e21005f840527bce068d44d6a
```

The frozen producer was also rerun. It reproduced all canonical non-timing
fields, including 12,734 coloring certificates, 3,011,741 directly audited
same-color pairs, and certificate-stream hash

```text
b761add523bbe8a4f1d8f822268ddc28a893e9a1318ebc73807822d7ca09fea8
```

As a third implementation check, the unmodified public reference code at
commit `7a4a19468771766cb4f20e10dfa5cf770cc2487b` independently returned 140
diameter cases, 108 cases with high points, 12,594 fixed-high branches, and a
unique relaxed maximum of 35 at the no-high `B=(5,4)` branch. That public code
does not contain the new three-candidate closure, so 35 is exactly the expected
pair-relaxation output rather than a contradiction.

## Exceptional B=(5,4) branch

The branch has 42 low candidates and 57 incompatibility edges. The supplied
focused checker exhibits nine disjoint edges and tests all 512 choices of one
omitted endpoint from each edge.

The hostile checker goes further: it does not use the supplied matching. A
from-scratch branching algorithm computes the exact minimum vertex-cover size
of the full 42-vertex incompatibility graph. It finds cover number 9 and exactly
two minimum covers. Their complementary 33-sets are killed as follows:

```text
(1,-1), (1,4), (6,1)    margin -15
(1,-1), (1,4), (6,2)    margin -15

(-1,2), (4,0), (4,5)    margin -15
(-1,3), (4,0), (4,5)    margin -15
```

For every one of these triples, `A2=25` and `D2=34`, hence

\[
(25-36)^2-4(34)=-15.
\]

Therefore no 33-candidate avoiding extension exists. The branch has at most
32 candidates and at most 34 points after restoring `A,B`.

The two surviving-set hashes are:

```text
1f88d54ca7d7317d67ea0d319295cd1ba45bf068a47235d4262b577264ed7f0f
dd08b8214282512d1a0fd433ce9af08d88044cab9e31a979585d496eb8f7bb2a
```

## Lower bound

The 34 displayed points are distinct and agree exactly with the frozen public
witness record. All `C(36,3)=7,140` triples with repetition pass. The minimum
integer margin is 21, attained twice, and the witness diameter squared is 53.
The canonical point-list SHA-256 is

```text
a99d87d1774eecb35c358a056a6cb1c233e54c3ff65141b1cae600d155ce1bf9
```

Thus `f(18)>=34`; the exhaustive certificates give `f(18)<=34`.

## Scope, attribution, and packaging caveats

- The 34-point witness was previously posted by Boris Alexeev; the report
  correctly makes no priority claim for it.
- The public upper-bound repository currently reports exact values only
  through N=7. The finite N=18 upper certificate is new progress in this
  project, but no absolute novelty claim is needed.
- The producer and supplied focused checker use Python `assert`; certified
  invocations must use ordinary `python3`, never `python3 -O`.
- The report's computational-only label and explicit warning that no uniform
  bound follows are both necessary and accurate.

No publication-blocking correction is required.
