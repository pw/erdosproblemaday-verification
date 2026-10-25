# Proof reconstruction and scope

Audit date: 2026-08-11 UTC

## Statement

For a finite planar point set `A` and a distance `d > 0`, write

```text
mu_A(d) = #{ unordered pairs {x,y} in A : ||x-y|| = d }.
```

Clemen, Dumitrescu, and Liu prove that, if `A` consists of `n >= 5`
points in convex position, then `A` determines a distance `d` with
`0 < d < diam(A)` and `1 <= mu_A(d) <= n`.

The result is a literature-derived partial. It is not a solution of the
unrestricted problem and says nothing about whether the number of distances
of multiplicity at most `n` tends to infinity.

## Named inputs

Let `m` be the number of distinct interpoint distances. The proof uses the
Altman--Fishburn classification:

1. Every convex `n`-point set determines at least `floor(n/2)` distances.
2. For odd `n`, equality forces a regular `n`-gon, up to similarity.
3. For even `n >= 8`, equality forces either a regular `n`-gon or a regular
   `(n+1)`-gon with one vertex deleted.
4. For `n = 6`, the equality configurations have multiplicity vectors
   `(6,6,3)` or `(5,5,5)`.

These are published theorem inputs, not claims proved by the checker.
`SOURCES.md` gives exact source locations.

## Pair count

Suppose first that `m > floor(n/2)` and, for contradiction, that every
non-diameter distance occurs more than `n` times. There are then at least
`floor(n/2)` non-diameter classes, each containing at least `n+1` pairs. The
diameter contributes at least one more pair, so

```text
C(n,2) >= floor(n/2) * (n+1) + 1.
```

The right side exceeds `C(n,2)`: the excess is `n+1` when `n` is even and
`(n+1)/2` when `n` is odd. This contradiction handles every non-equality
case.

## Equality models

It remains to inspect `m = floor(n/2)`.

- A regular odd `n`-gon has `(n-1)/2` chord-step classes, each of
  multiplicity `n`.
- A regular even `n`-gon has `n/2-1` non-antipodal classes of multiplicity
  `n`, and one antipodal class of multiplicity `n/2`.
- Deleting one vertex from a regular odd `(n+1)`-gon removes two pairs from
  every chord-step class, leaving `n/2` classes of multiplicity `n-1`.
- At `n=6`, every entry in `(6,6,3)` and `(5,5,5)` is at most six.

Each model therefore has a non-diameter distance of multiplicity at most
`n`. This proves the convex-position theorem.

`verify_convex_proof.py` checks the pair-count gap for `5 <= n <= 10000`,
the regular-polygon models for `5 <= n <= 500`, the deleted-vertex models for
every even `8 <= n <= 500`, and the two hexagon vectors, using exact integers.
The finite limits test the formulas; the displayed argument proves them for
all `n`.

## Publication boundary

Safe claim:

> Clemen, Dumitrescu, and Liu proved the conjecture for convexly positioned
> point sets: every convex `n`-point set, `n >= 5`, has a non-diameter
> distance occurring at most `n` times.

Rejected claims include that Problem 132 is solved, that the theorem covers
arbitrary planar sets, or that it proves the stronger growth question.

On the audit date the live problem remained `OPEN`, with five informal
comments, zero registered or dedicated proof claims, and no current worker.
The informal comments are not used here.
