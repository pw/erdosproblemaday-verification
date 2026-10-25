# Cold hostile audit of the problem 213 candidate

Audit date: 2026-08-11 UTC.

## Verdict

**PASS**, with the exact scope below and the 70000-comparison wording caveat in
`WEB_RECHECK.md`.

> For the exact seven-point metric published by Kreisel and Kurz with diameter
> 22270, there is no distinct planar point whose seven distances to the
> heptagon are positive integers at most 96000.

This is a bounded nonextension theorem for one fixed heptagon. It is not a
lower bound for `d_dot(2,8)`, not a proof that the heptagon is globally
inclusion-maximal, not an eight-point construction, and not a solution of
Erdos problem 213.

## Frozen author bundle

Bundle: `fresh7_erdos213_20260811`.

- `MANIFEST.sha256` SHA-256:
  `8dc4ce03a4bc8e6e8873c314e11f2efefb9840bcb38b62f32d9b5ce2d979aa47`.
- All 22 manifest entries passed.
- A clean `./reproduce.sh` rebuilt both author scanners, regenerated the full
  candidate residue, matched all frozen outputs, and returned zero extensions.
- The C++ scanner was rerun under UBSan and produced the same candidate file
  and zero-extension summary with no diagnostic.

## Geometric reduction

Put anchor vertices at `(0,0)` and `(d,0)`, with `d=22270`. For nondegenerate
anchor distances `a,b`, Heron's product is

```text
F=(d+a+b)(d+a-b)(d-a+b)(-d+a+b).
```

The primary Kreisel-Kurz source defines triangle characteristic as the
squarefree part of `F`, states that all nondegenerate triangles in a planar
integral point set have the same characteristic, and states characteristic
`k=2002` for this heptagon. Thus every non-anchor-collinear extension must have
`F=k*s^2` for an integer `s`. Its only two positions for ordered `(a,b)` are

```text
((a^2-b^2+d^2)/(2d), +/- s*sqrt(k)/(2d)).
```

For scaled pairs `(X,S)`, squared distance is exactly

```text
((X-Y)^2+k(S-T)^2)/(4d^2).
```

The code requires the numerator to be nonzero, divisible by `4d^2`, the
quotient to be a perfect square, and its root to be at most 96000. These are
necessary and sufficient exact predicates; no floating-point geometry is
used.

The complete distance matrix determines its planar realization up to global
isometry. Anchor circles give each vertex two signs, and its distance to
vertex 2 uniquely fixes the sign. The reconstructed exact coordinates match
all coordinate rows in the primary source and all 21 distances.

## Domain completeness

The author C++ loop enumerates `(a,b)` directly with `a<=b`; the author Go loop
uses Heron semiperimeter factors. The audit's third loop instead uses
`sum=a+b` and `delta=b-a`. Its independent conditions are:

```text
d < sum <= 2B
0 <= delta < d
sum == delta (mod 2)
delta <= sum-2
delta <= 2B-sum
```

These are exactly positivity, strict triangle inequalities, integrality of
`a,b`, ordering, and `b<=B`. The independent analytic count and all three
loops agree on `1,765,966,460` unordered strict triangles. The audit traversal
regenerated the exact same sorted 1,017-row `(a,b,s)` residue byte-for-byte.
It restores both anchor orders and both half-planes, yielding 4,068 candidates.

All anchor-collinear candidates are also complete. Between the anchors they
are the integer positions `1..d-1`. Outside, positions run through distance
`B-d` on each side, inclusive. The count is
`(d-1)+2(B-d)=169729`. The two exterior extremes attain distance 96000, so
the inclusive endpoint was exercised. The anchor endpoints themselves are
forbidden coincidences.

A point collinear with any other pair but not the anchors still has a
nondegenerate anchor triangle and remains in the characteristic scan. No
collinearity or concyclicity filter is applied. Points coincident with the
five non-anchor vertices occur among the characteristic candidates and are
rejected only by the required positive-distance test; all seven original
vertices were exercised as negative controls.

## Independent exact result

`audit_metric.py` uses Python arbitrary-precision integers and `math.isqrt`,
loads the JSON matrix independently, reconstructs the exact quadratic
coordinates, validates the primary coordinate representation, and tests all
auditor-generated candidates. It reports:

```text
analytic_triangle_pairs=1765966460
characteristic_candidates=1017
oriented_candidates=4068
collinear_candidates=169729
raw_pairs_with_b_at_bound=22270
coincident_vertex_negative_controls=7
extensions=0
AUDIT_METRIC_PASS
```

## Arithmetic and square roots

The declared Heron bound is `18,282,807,705,600,000,000`, below
`2^64-1=18,446,744,073,709,551,615` by `163,936,368,109,551,615`.
The sharper maximum at `a=b=96000` is
`18,036,838,426,581,590,000`. Candidate coordinate differences are promoted
to signed 128-bit before squaring in C++; Go uses `big.Int` for the metric.

The C++ square-root estimate is accepted only after exact 128-bit correction
and multiplication. Its input root is at most about 94.9 million, so the cast
is in range. The Go Newton iteration uses only integer division; in this
bundle its squared inputs are below `9.01e15`, so neither the initial power of
two nor `x*x` can overflow `uint64`. The Go fixed-heptagon reconstruction's
signed Heron products have maximum `695,689,634,716,876,800`, below `int64`.
The audit scanner independently uses sum/difference factors and exact
post-correction; the final metric pass uses arbitrary-precision arithmetic.

## Primary source and public boundary

`audit_primary_source.py` parses the original arXiv TeX and verifies all 49
matrix entries, exact coordinate rows, characteristic 2002, the common
characteristic theorem, and the restricted general-position search bound
70000. The product `6469693230` is exactly divisible by 2002.

The live problem page remains open with seven as the best construction and no
claimed proof. OEIS still stops at seven. Current and recent literature checks
found no eight-point general-position construction and no prior instance of
this exact fixed-heptagon bounded computation. Novelty remains a negative
search claim, not a theorem.

The sole wording correction required before publication is that the 2008
70000 comparison applies to the overlapping **general-position** slice. The
new zero-extension computation itself genuinely includes nongeneral-position,
collinear, and concyclic placements of the eighth point.
