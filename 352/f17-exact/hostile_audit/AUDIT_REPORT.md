# Hostile audit: Problem 352 lattice value at N=17

## Verdict

The proposed finite result is sound:

\[
f(17)=32
\]

for Koizumi's N-avoiding lattice model, with repetitions allowed in the
triangle triple.

The producer's final pinned N=17 run passed, and a standalone implementation
using different graph and geometry code independently reproduced every global
count.  A second, small certificate checker independently reconstructed the
sole loose branch, B=(5,4), from the lattice points themselves.

## Mathematical reduction checked

For a repeated triple (p,p,q), the avoiding inequality gives |p-q|<17.
Thus every nontrivial finite avoiding set has a diameter pair of squared
length below 289.  Translation and the eight signed-coordinate/swap
isometries put that pair at A=(0,0), B=(b_x,b_y), with
b_x >= b_y >= 0.  Independent signed-vector orbit accounting gives exactly
125 possible B.

Every further lattice point lies in the intersection of the two closed discs
centered at A and B with radius |A-B|.  Since that radius is below 17, the
integer coordinate box [-16,16]^2 is complete.  The exact predicate

\[
(A_2-34)^2-4D_2>0
\]

is equivalent to the literal strict inequality: A_2 is twice the area and
D_2 the squared triangle diameter.  This equivalence was cross-checked with
80-decimal radical arithmetic on 5,984 witness triples and 21,119 lens
triples.  There are 12 exact zero-margin lens triples, so using `>` rather
than `>=` is a real and tested boundary condition; the implementation gets it
right.

Each surviving lens point is below or above area 17.  Any avoiding set either
has no high point or contains a high point H.  Enumerating the no-high branch
and every possible fixed H is therefore exhaustive.  The independent run
found 94 directions with high candidates, 9,414 fixed-H branches, and 9,539
branches total.

Within a branch, the candidates of an actual extension form a clique in the
pair-compatibility graph.  A proper coloring therefore bounds their number,
even though triples of three candidates can make the true extension smaller.
The audit rebuilt every pair by a full triple scan of F union {p,q} and then
used dynamic DSATUR with Python sets, rather than the producer's static
degree-ordered bitset coloring.  All branches met the required cap except the
same single branch B=(5,4), no-high.

## Exceptional B=(5,4) branch

The independent reconstruction gives exactly:

- 40 low candidates;
- 48 incompatibility edges;
- a fixed matching of nine pairwise vertex-disjoint incompatibility edges;
- all 512 choices of one omitted endpoint per matching edge;
- exactly two choices that cover all 48 incompatibility edges.

A nine-edge matching proves that a pairwise-compatible set has at most 31
vertices.  A 31-set would omit exactly nine candidates, hence its omitted
vertices must be one of those two size-nine covers.  The two complementary
31-sets have canonical hashes

```text
a25169e82c060b4577a6c29a83aece3a1b5ed08e4ac8fcf911a3c65227d72236
8bbad78ce3238f685ffbdb068d074f4171732fc1cfb2182418fcb62880ed001a
```

and are respectively killed by the all-candidate triples

```text
(0,3), (3,-1), (4,5)
(1,-1), (2,5), (5,1)
```

For each triple, twice the area is 22 and the diameter squared is 37, so

\[
(22-34)^2-4(37)=144-148=-4.
\]

There is exactly one bad all-candidate triple in each 31-set.  Therefore an
avoiding extension contains at most 30 candidates, and with A,B at most 32
points.

The small checker used an alternative nine-edge matching from the producer;
it nevertheless found the same two covers and bad triples.  This decorrelates
the cover result from the matching choice.

## Lower bound

The 32 displayed lattice points are distinct.  All C(34,3)=5,984 triples with
repetition pass the strict exact predicate.  The minimum margin is 5, attained
once, and the witness diameter squared is 45.  Hence f(17)>=32.

## Global independent totals

```text
diameter directions       125
directions with high       94
fixed-high branches      9414
all branches             9539
pool memberships       260479
maximum branch pool       106
global upper bound         32
tight B             (5,3),(6,1),(5,4),(6,3)
```

These agree exactly with the producer.  The independent coloring choices are
different, but its deterministic branch and diameter manifests hash to

```text
branch    0a8e0e483ec7e279d3099d5689cb1b32c9b4d5ea5f3b57d0283dfa3302613fae
diameter  c3db96c807e553601f0d37115595f63edc89572a1f8b47c3f39e158a764d4857
```

## Attack findings and limitations

No missing diameter orbit, lens point, low/high branch, fixed-high branch,
pair condition, or 31-candidate survivor was found.  Strictness and
combinations-with-repetition were specifically tested.

The producer uses Python `assert` for its checks, so its certified invocation
must be ordinary `python3`, not `python3 -O`.  This is a packaging caveat, not
a flaw in the normal run or the mathematical result.  The standalone hostile
checker uses explicit exceptions for load-bearing checks.

The result is only the finite lattice value f(17).  It does not establish the
uniform f(N)=O(N) statement or solve the continuous Erdős problem.

Exact commands, hashes, resource usage, and canonical certificate hashes are
recorded in `AUDIT_LOG.txt`.
