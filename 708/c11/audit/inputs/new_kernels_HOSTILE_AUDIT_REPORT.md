# Hostile audit: Erdos 708 full eleven-edge q2/q3 kernels

Date: 2026-08-11 UTC

## Verdict

**PASS, restricted to genuinely new full `e=11` Hall-deficit-two and
Hall-deficit-three kernels in the generic exact-difference case.**

This report does not certify inherited cores with outside edges, the aligned
case, or `c_11=2`.

The audited source is frozen as

```text
12891b1403377ba1917f7996e5e813d3b7bff0ff2997b3fc7e4e19bb2138a453  erdos708_c11_new_kernels.md
6e1654b06df6c8eb6bc5ecd67ba1c534ba2136872ac13ec8d7994f79f0039a35  erdos708_c11_new_kernels_audit.py
```

## Structural classification

Minimality gives minimum degree at least two and exact vertex counts
`11-q`.  The degree bound leaves only `4x5` for `q=2`, `3x5` or `4x4` for
`q=3`, and `K_(3,4)-e` for `q=4`.  At most six vertices support only nine
bipartite edges, excluding larger defect.

The independent checker enumerates every labelled eleven-edge graph and
constructs the complete permutation orbit of each displayed table row.  The
sets agree exactly:

```text
q=2, 4x5: 13,560 labelled graphs in 11 orbits
q=3, 3x5:    390 labelled graphs in  3 orbits
q=3, 4x4:  2,304 labelled graphs in  8 orbits
```

It also checks every proper edge subset of every representative directly.
Thus the row/column-induced test has not hidden a non-induced smaller kernel.

## Layer certificates

For every displayed representative, all `2^(left+right)` endpoint subsets
were checked.  At each induced level, the number of fully contained support
blocks is at least `max(0,|E|-|V|)`.  Since every prime-power level is exactly
one such endpoint subset, this is a complete arbitrary-height certificate,
not merely a capped valuation test.

The independent capped valuation smoke test covered 288,684 vectors.  The
support-union minima were:

```text
q2: every displayed pair actually has at least 8 union edges
q3: every pair has at least 6; every triple has at least 9
```

The q2 statement is stronger than the note's advertised lower bound of six.

## Placement

For q2, each factor divides five distinct labels, so it is at most `M/5` and
has at least nine interval multiples.  Trapping one factor in the nine kernel
vertices makes every vertex divisible and hence makes all eleven labels
divisible.  If the two outside sets fail Hall, their full union has at most
ten points.  The alleged union forces both divisors into `[2M/11,M/5]`; a
distinct reduced ratio has lcm at least `2M`, impossible even for two common
multiples.  Equality of the factors contradicts the support-union count.

For q3, each factor divides four labels and has at least seven multiples.  Any
seven of the eight vertices induce at least six labels: the exact minima are
six for `3x5` and seven for `4x4`.  This excludes a trapped singleton factor.
Pair Hall failures reduce to the published nine-point lemma.  A triple failure
puts every pair in a ten-point union.  Distinct divisors in
`[2M/11,M/4]` have lcm at least `8M/11`; four common multiples span more than
`2M`.  Thus all three factors coincide, and their nine-edge support union
requires at least seventeen multiples, a contradiction.

These arguments correctly supply two or three distinct outside repair points
for every full eleven-edge q2/q3 kernel.

## Reproduction

Run:

```bash
./run_all.sh
```

The independent program uses explicit permutation orbits rather than the
supplied canonical-form routine.  Its arithmetic sweep checked 6,586,259
possible reduced-divisor pairs through `M=2000` and 135,355 concrete phase
pairs.

## Scope boundary

Still outside this verdict are the inherited `e<11` q2/q3 kernels with one or
more remaining endpoint sets, the four-defect placement/certificate
integration, every aligned exceptional-layer and midpoint-avoidance step, and
the assembly of a complete `c_11<=2` proof.

