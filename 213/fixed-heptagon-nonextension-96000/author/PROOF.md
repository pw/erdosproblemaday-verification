# Exact bounded nonextension theorem

## Theorem

Let `H` be the seven-point planar integral set represented by the published
Kreisel-Kurz distance matrix in `heptagon_matrix.json`. There is no point `P`
in the Euclidean plane, distinct from the points of `H`, for which all seven
distances from `P` to `H` are positive integers at most 96000.

This is stronger than merely excluding general-position extensions of this
fixed heptagon, because no collinearity or concyclicity assumption is imposed
on `P`.

## Coordinate reduction

Use vertices 0 and 1 as anchors. Their distance is `d = 22270`; put them at
`(0,0)` and `(d,0)`. If a candidate point has anchor distances `a,b`, strict
triangle inequalities hold and `1 <= a,b <= 96000`. Define

```
F(d,a,b) = (d+a+b)(d+a-b)(d-a+b)(-d+a+b).
X(a,b)   = a^2-b^2+d^2.
```

Heron's formula gives `F = 16 Area^2`. Every nondegenerate triangle in one
planar integral point set has the same squarefree characteristic. The primary
paper states and proves this fact, and states that `H` has characteristic
`k = 2002`. Consequently every possible extension must satisfy

```
F(d,a,b) = k*S^2
```

for an integer `S`. Its two possible coordinates are exactly

```
( X(a,b)/(2d),  +/- S*sqrt(k)/(2d) ).
```

The existing seven vertices are reconstructed in the same scaled coordinate
system from their anchor distances. Vertex 2 fixes an upper half-plane. Each
remaining sign is uniquely forced by its published distance to vertex 2. Both
programs then recompute all 21 matrix entries from exact integers before the
extension scan starts.

For scaled coordinate pairs `(X,S)` and `(Y,T)`, squared distance is

```
((X-Y)^2 + k*(S-T)^2) / (4*d^2).
```

The candidate test requires this rational number to be a positive integer
square at most `96000^2` for all seven vertices. No floating-point geometric
predicate is used.

Candidates collinear with the two anchors are outside the characteristic
argument. Both programs enumerate them separately: the `d-1` points strictly
between the anchors and the `96000-d` possible integral positions beyond each
endpoint. Their scaled coordinates are tested against all seven vertices by
the same exact metric predicate.

## Exhaustive domains

`extend_heptagon.cpp` enumerates every unordered pair `a <= b` satisfying the
strict triangle inequalities and the distance bound. For every
characteristic-compatible triangle it restores both orders `(a,b),(b,a)` and
both sides of the anchor line.

`verify_semiperimeter.go` uses a decorrelated domain. It sets

```
u = a+b-d,  v = d+a-b,  w = d-a+b.
```

Then `v+w=2d`, `a=(u+v)/2`, `b=(u+w)/2`, and

```
F = u*v*w*(2d+u).
```

Taking `v <= w` is exactly `a <= b`. The Go program independently enumerates
`1 <= v <= d`, positive `u` of the required parity, and
`u <= 2*(96000-d)+v`; that last bound is exactly `b <= 96000` and implies the
bound on `a`. It uses a pure-integer Newton square root and arbitrary-precision
integer metric arithmetic. The C++ program instead scans anchor radii and
uses a long-double square-root estimate corrected and accepted only by exact
128-bit multiplication.

## Certified counts

Both independent paths return exactly:

```
unordered strict anchor triangles  1765966460
characteristic-2002 triangles             1017
ordered-and-oriented candidates           4068
collinear-anchor candidates             169729
complete integral extensions                  0
```

The first count includes all nondegenerate candidates before a characteristic
or distance-to-other-vertices filter. Agreement on all five counts is a useful
cross-check; either scanner alone is intended to be complete.

The complete 1017-row pre-orientation residue is frozen as
`characteristic_candidates.tsv`. During reproduction both scanners regenerate
that canonical sorted `(a,b,S)` list from their different loop orders, compare
the two byte-for-byte, and compare them with the frozen file. Thus the
agreement is on the exact surviving set, not only its cardinality.

`verify_matrix.py` is a third, definition-level route for the fixed input. It
loads the JSON rather than a compiled-in matrix, reconstructs the quadratic
coordinates, checks all 21 distances, checks characteristic 2002 for all 35
triangles, and checks the collinearity and concyclicity determinants for every
triple and quadruple. It does not participate in the 96000 extension scan.

## Honest scope

The theorem is about extending this exact seven-point metric. An arbitrary
eight-point configuration need not contain a subset congruent to this
heptagon. Therefore the computation gives no lower bound of 96001 for
`d_dot(2,8)` and does not settle any new cardinality in problem 213.
