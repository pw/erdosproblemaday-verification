# Erdős #352: local universality of fixed-high compatibility

This note records rigorous structural progress on the uniform obstruction.
It does **not** prove `f(N)=O(N)` and does not solve Erdős problem 352.

## The lemma

Let `d` be any nonzero vector in `Z^2`, put `delta=|d|`, and suppose

```text
100 delta <= N.                                                (1)
```

Then there are five lattice points

```text
O, B, H, P, Q
```

with all of the following properties.

1. The five-point set is `N`-avoiding: every triple, with repetitions,
   satisfies

   ```text
   |area - N| > diameter.
   ```

2. `O,B` are a diameter pair.
3. `H` is high relative to that pair:

   ```text
   area(O,B,H) > N + |B|.
   ```

4. `Q-P=d`.  In particular, `P,Q` form a compatible edge in the fixed-high
   branch with forced set `{O,B,H}`.

Moreover, this branch contains the arithmetic-progression clique

```text
H-d, H-2d, ..., H-Ld,       L=floor(N/(20 delta)) >= 5.      (P)
```

Here an *oriented fixed-high branch* has `O=0` and an arbitrary integral
diameter endpoint `B`; we do not quotient this family by D4. Thus the union,
over all oriented fixed-high branches, of compatible pair differences
contains every nonzero lattice vector in the disk of radius `N/100`.

## Explicit construction

Let `g=gcd(d_x,d_y)`.  Choose the least positive multiple `t` of `g` with

```text
t >= 16 delta.
```

Then

```text
16 delta <= t < 16 delta + g <= 17 delta.                     (2)
```

The equation `det(v,d)=t` has an integer solution.  Its solutions differ by
integer multiples of `d/g`, so choose one for which

```text
0 <= v dot d < delta^2/g.                                    (3)
```

The components of `v` parallel and perpendicular to `d` are respectively
less than `delta/g <= delta` and `t/delta < 17`.  Hence

```text
|v| < delta + 17 <= 18 delta.                                (4)
```

Now put

```text
M = floor(N/(4 delta)),
O = 0,
H = M d,
B = M d + v,
P = (M-2)d,
Q = (M-1)d.                                                   (5)
```

Condition (1) gives `M>=25`, so these are five distinct points.

## Proof of the lemma

Write `D=|B|`.  Condition (3) makes the squared function

```text
|r d + v|^2 = r^2 delta^2 + 2r(v dot d) + |v|^2
```

nondecreasing for `r>=0`.  It follows that all distances from `B` to the
four collinear points in (5) are at most `D`.  Their mutual distances are at
most `M delta <= D`.  Thus `O,B` are a diameter pair.  Moreover,

```text
D <= M delta + |v|
  < N/4 + 18 delta
  <= 0.43 N.                                                  (6)
```

Every triangle in the set is either collinear or consists of `B` and two of
the four collinear points.  In the latter case, if their coefficient gap is
`k`, its area is exactly `k t/2`.  The only possible positive gaps are

```text
1, 2, M-2, M-1, M.                                           (7)
```

For `k=1,2`, equations (1)-(2) give

```text
area <= t < 17 delta <= 0.17N < N-D.                         (8)
```

For `k>=M-2`, using `M delta > N/4-delta`,

```text
area >= (M-2)t/2
     >= 8(M-2)delta
      > 2N-24delta
     >= 1.76N
      > N+D.                                                  (9)
```

Collinear triples have area zero and diameter at most `D<N`.  The same
observation handles every repeated triple.  Equations (8)-(9) therefore
prove the strict `N`-avoiding inequality for every triple.  Taking `k=M` in
(9) proves that `H` is high.  Finally `Q-P=d`, proving the lemma.

For the strengthening (P), adjoin `(M-j)d` for every `1<=j<=L`.  The
diameter argument is unchanged.  Gaps within this near-`H` cluster are at
most `L`, whereas gaps from `O` to the cluster are at least `M-L`.  Since
`L delta<=N/20`, their areas respectively satisfy

```text
area < 17N/40 = 0.425N < N-D
```

and

```text
area >= (M-L)t/2
      >= 8(M-L)delta
       > 8(N/4-delta-N/20)
      >= 1.52N
       > N+D.
```

Thus the enlarged set is still `N`-avoiding.  After fixing `O,B,H`, its
remaining `L` points are pairwise compatible, proving (P).

## Consequence for periodic colorings

No single lattice-coset coloring with `O(N)` colors, used unchanged on every
oriented fixed-high branch at a given `N`, can properly color them all for all
sufficiently large `N`.

More precisely, fix `C`. Suppose for each `N` all oriented fixed-high
compatibility graphs were colored by the same coset map

```text
Z^2 -> Z^2/L_N,          [Z^2:L_N] <= C N.                   (10)
```

Take `K=ceil(sqrt(CN))`.  Among the `(K+1)^2` points of
`{0,...,K}^2`, two have the same coset.  Their nonzero difference `d` lies in
`L_N` and obeys

```text
|d| <= sqrt(2) K = O_C(sqrt N).
```

For all sufficiently large `N`, this is at most `N/100`.  The lemma then
constructs a fixed-high branch containing a compatible pair whose difference
is `d`.  That pair has the same color under (10), a contradiction.

The same argument covers every coloring obtained from a homomorphism
`phi_N:Z^2 -> G_N` with `|im(phi_N)|<=CN`; the target group itself need not be
abelian because the image automatically is. It also covers an affine
translate of such a coloring.

This does **not** rule out a homomorphic coloring common only to the chosen
D4-normalized representatives used by the finite search: transporting a
branch to the normalized wedge also transports the coloring kernel. Nor does
it rule out a lattice or affine coloring chosen adaptively from the particular
`B,H`, or any nonperiodic coloring.

## Exact audit

Run:

```text
python3 check_local_universality.py
```

The checker implements the construction without floating-point arithmetic,
checks that `O,B` are a diameter pair, evaluates all 35 triples with
repetition under the exact squared predicate, checks the strict high
inequality, and rechecks that `P,Q` are compatible in the forced branch.  It
also checks the two endpoint inequalities certifying the entire progression
clique (P), without materializing a large graph.  It
exhausts all admissible `d` for seven selected values of `N` through 10,000
and also checks 10,000 deterministic pseudorandom cases through `N=10^6`.

## Claim boundary

Proved here:

- local universality of compatible differences through radius `N/100`;
- explicit arithmetic-progression cliques of size `floor(N/(20|d|))`;
- failure of one `O(N)`-index lattice-coset or small-image homomorphic
  coloring used unchanged across every oriented branch at a fixed `N`.

Not proved here:

- an `O(N)` coloring or cover for fixed-high branches;
- failure of a common rule only on chosen D4-normalized representatives;
- failure of branch-adaptive periodic rules;
- any upper bound on `f(N)` beyond the already known finite computations;
- Erdős problem 352.
