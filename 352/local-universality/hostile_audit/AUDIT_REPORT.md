# Hostile audit: Erdős #352 local-universality lemma

## Verdict

**BLOCK the current frozen wording; PUBLISH after one required scope edit.**

The geometric lemma and its arithmetic-progression strengthening are correct.
The pigeonhole consequence is also correct for a single homomorphic coloring
used on **every oriented (unnormalized)** fixed-high branch.  Every inequality
is strict with room to spare, all signs of `d` are covered, and an independent
implementation materialized and checked 9,821,816 repeated triples.

The bundle must not suggest that the proof also rules out a single
homomorphic coloring common only to the **D4-normalized** branch
representatives used in the finite enumeration.  Its construction does not
make `B` normalized, and normalizing `B` can move the constructed difference
out of the coloring kernel.  The current phrases “all fixed-high
compatibility graphs” and “the missing uniform coloring lemma” are ambiguous
against the established normalized-branch convention.  The exact correction
is given below.

Subject to that correction, this is rigorous and site-worthy structural
partial progress.  It proves a genuine all-`N` local-universality/AP-clique
lemma and eliminates a natural but narrower strategy.  It does not solve
#352 or provide a uniform upper bound.

## Frozen source integrity and replay

The source manifest verified exactly:

```text
README.md: OK
REPORT.md: OK
check_local_universality.py: OK
CHECK_OUTPUT.txt: OK
```

The cold replay, with bytecode writes disabled and assertions enabled, matched
`CHECK_OUTPUT.txt` byte-for-byte.  It completed in 11.57 seconds at 64,608 KiB
maximum RSS and printed:

```text
deterministic_N=[100, 127, 251, 509, 1000, 4096, 10000] random_cases=10000
total_cases=47088 trace_sha256=28d54ac1155252a72369bfc30c633c661311246f5826b429785c0d2160926312
example_N100_d10={"N":100,"d":[1,0],"points":[[0,0],[25,-16],[25,0],[23,0],[24,0]],"diameter2":881,"high_twice_area":400,"min_margin":24700,"progression_clique_size":5}
ALL EXACT CHECKS PASSED
```

The replay output SHA-256 is
`d50863243ff73c0a52b36493c5d76923a176ba9deb6507d59aa4c93afbca1188`,
identical to the frozen output hash.

The unmanifested `__pycache__` directory is irrelevant generated state and
should simply be omitted from a public verification bundle.

## Independent audit

`independent_audit.py` imports no producer code.  It uses:

- a separate iterative signed Bézout routine;
- Euclidean `divmod` for the dot-product normalization;
- shoelace area rather than the producer's based-vector determinant;
- exact integer squared comparisons only;
- complete materialization of the progression for deterministic signed
  cases, including every point pair and every triple with repetition;
- endpoint/monotonicity checks on 50,000 larger pseudorandom cases through
  `N=10,000,000`.

It passed:

```text
endpoint_cases=51691
materialized_cases=1691
materialized_repeated_triples=9821816
hostile_trace_sha256=8d930d9cb8ab06a4a94647ba957f100f1bb01aea6100861379cd1000cdf32fa0
ALL INDEPENDENT CHECKS PASSED
```

The deterministic cases include all admissible vectors, in all four sign
quadrants and on both axes, for `N=100,101,127,199,251,509,997,2000`.
Special cases exercise primitive and imprimitive vectors and equality in
`100|d|=N`, including `(3,4)`, all its sign variants, `(6,8)`, and `(5,12)`.

## Proof audit

Let `d=(d_x,d_y) != 0`, `delta=|d|`, and
`g=gcd(|d_x|,|d_y|)>0`.  The argument below applies without any sign
restriction on either coordinate.

### 1. Bézout solution and normalization

Choose integers `a,b` with `a d_x+b d_y=g`.  If `t=kg` is the least positive
multiple of `g` at least `16 delta`, then

```text
v_0=(k b,-k a),             det(v_0,d)=t.
```

Every integral solution of `det(v,d)=t` differs from `v_0` by an integral
multiple of the primitive vector `d/g`.  Adding `d/g` changes `v dot d` by
the positive integer `delta^2/g`.  Euclidean division therefore gives a
unique representative modulo this kernel with

```text
0 <= v dot d < delta^2/g.
```

This is valid for negative coordinates as written.  Minimality of `t` gives

```text
16 delta <= t < 16 delta+g <= 17 delta.
```

The parallel component of `v` has length less than `delta/g`, while its
perpendicular component has length `t/delta<17`.  Since
`delta>=g>=1`,

```text
|v| < delta+17 <= 18 delta.
```

No sign or irrational-rounding assumption is hidden here.

### 2. Distinctness and diameter

Put `M=floor(N/(4 delta))` and
`L=floor(N/(20 delta))`.  From `100 delta<=N`, `M>=25`, `L>=5`, and
`L<M`.  The nonzero determinant makes `B=Md+v` off the line spanned by
`d`; all points

```text
O=0, B, H=Md, H-d, ..., H-Ld
```

are therefore distinct.

Write `D=|B|`.  Because `v dot d>=0`,

```text
D^2=M^2 delta^2+2M(v dot d)+|v|^2 >= M^2 delta^2.
```

All non-`B` points have coefficients between `0` and `M`, so their mutual
distances are at most `M delta<=D`.  For a coefficient `c`, the squared
distance from `B` is

```text
|(M-c)d+v|^2=r^2 delta^2+2r(v dot d)+|v|^2,
```

where `0<=r<=M`.  This is nondecreasing in `r`, so it is at most its value
at `r=M`, namely `D^2`.  Hence `O,B` remain a diameter pair for the entire
progression, not merely for the original five points.

Finally,

```text
D <= M delta+|v| < N/4+18 delta <= 0.43N < N.
```

### 3. Every triple, including repetitions

Every point except `B` is collinear.  A triangle containing `B` and two
distinct collinear points whose coefficient gap is `k` has area exactly
`kt/2`.  The possible gaps in the enlarged set split exhaustively into:

- cluster gaps `k<=L`;
- gaps from `O` to the cluster, `k>=M-L`.

For the first kind,

```text
area <= Lt/2 < 17L delta/2 <= 17N/40 = 0.425N < N-D,
```

because `D<0.43N`.  For the second kind,

```text
area >= (M-L)t/2
     >= 8(M-L)delta
      > 8(N/4-delta-N/20)
      >= 1.52N
      > N+D.
```

All inequalities needed at the endpoints are strict.  A triple that is
collinear, or has a repeated point and hence zero area, has diameter at most
`D<N`, so it also passes `|area-N|>diameter`.  These cases exhaust all
triples with repetition.  In particular, the whole enlarged set is
simultaneously `N`-avoiding.

Taking coefficient gap `M` proves that `H` is high relative to `O,B`.
After fixing `O,B,H`, all `L` remaining points coexist simultaneously, hence
form a clique in the pair-compatibility graph.  Its first two points are
`Q=(M-1)d` and `P=(M-2)d`, with `Q-P=d`.

### 4. Pigeonhole consequence

Let `L_N` be any finite-index sublattice with index `m<=CN`, where `C` is
fixed independently of `N`, and set `K=ceil(sqrt(CN))`.  The `(K+1)^2`
points in `{0,...,K}^2` occupy at most `m` cosets, so two distinct points
share a coset.  Their difference is a nonzero `d in L_N` satisfying

```text
|d| <= sqrt(2) K <= sqrt(2)(sqrt(CN)+1).
```

For all sufficiently large `N` this is at most `N/100`.  The geometric lemma
then supplies an oriented fixed-high branch with a compatible pair differing
by `d`, so the coset coloring assigns the pair one color.

For a homomorphism `phi_N:Z^2 -> G_N`, the same proof needs only
`|im(phi_N)|<=CN`; `G_N` itself may be any group, finite or infinite.  The
image is automatically abelian, the kernel has index equal to the image
size, and equality of two grid images puts their difference in the kernel.
Thus the report's restriction to an abelian target is harmless but
unnecessary.  An affine translate of such a coloring is also covered.

The fixed constant `C`, “sufficiently large `N`,” and one map common to every
branch at that `N` are essential quantifiers.  The argument does not apply
when the map can depend on `B,H`.

## Required normalization-scope correction

The explicit construction does not generally put `B` into the finite
search's normalized wedge `B_x>=B_y>=0`.  For example, the frozen
construction gives

```text
N=10000, d=(1,-1), B=(1756,-1779).
```

The D4 map `(x,y) -> (-y,x)` normalizes this to
`B'=(1779,1756)` but sends the edge difference to `d'=(1,1)`.
For the index-`m` lattice

```text
L_m={(x,y): x+y == 0 (mod m)},       m>2,
```

the original `d=(1,-1)` lies in `L_m`, whereas `d'=(1,1)` does not.  Thus
normalizing the constructed branch does not preserve the monochromatic-edge
certificate for a fixed coloring kernel.  This is not a counterexample to a
normalized-family theorem; it shows that no such theorem was proved here.

Recommended replacement wording:

> Here an *oriented fixed-high branch* has `O=0` and arbitrary integral
> diameter endpoint `B`; we do not quotient the family by D4.  The union of
> compatible differences over these oriented branches contains every
> nonzero `d` with `100|d|<=N`.  Consequently, no single homomorphism with
> image of size `O(N)`, used unchanged on every oriented branch at that `N`,
> properly colors them all.

Add explicitly:

> This does not rule out a homomorphic coloring common only to the chosen
> D4-normalized representatives, because transporting a branch to the
> normalized wedge also transports the coloring kernel.  It also does not
> rule out any coloring chosen adaptively from `B,H`.

With those sentences, the claim boundary is exact and the bundle is fit to
publish as structural partial progress.

## Why the obvious D4 symmetrizations do not repair the stronger claim

Let `m=[Z^2:L]`.  Replacing `L` by its D4-invariant core

```text
L_sym = intersection_{U in D4} U(L)
```

does make normalization harmless, but destroys the needed scale.  The crude
index bound is `m^8`.  Since `-L=L`, there are at most four distinct images,
improving the crude bound only to `m^4`.  Pigeonhole/Minkowski then supplies a
nonzero vector merely of length `O(m^2)`, which is `O(N^2)` when `m=O(N)`,
far outside the proved `N/100` universality radius.  Equivalently, augmenting
the color by all D4-transformed colors uses as many as `m^4` colors rather
than `O(N)`.

This loss is real, not just a loose product bound.  For odd `m`, take

```text
L_m={(x,y):x+y == 0 (mod m)}.
```

Intersecting with its quarter-turn image also imposes `x-y==0 (mod m)`, so
the D4-invariant core is exactly `m Z^2`, of index `m^2` and shortest-vector
length `m`.  If `m` is comparable with `N`, it has no nonzero vector in the
disk of radius `N/100`.

Nor does selecting only the canonicalizer arising from the present
construction give a pigeonhole shortcut.  When `m` is odd and `m` is
comparable with `N`, every vector of `L_m` in the `N/100` disk satisfies
`x+y=0` as an integer equality, so it is `a(1,-1)`.  The current construction
has `B` in the same mixed-sign sector (for `a>0`, its normalized Bézout choice
is a scalar multiple of the displayed `d=(1,-1)` example), and its D4
canonicalizer sends the difference to `a(1,1)`.  This belongs to `L_m` only
when `m` divides `2a`, impossible for odd `m` and `0<2|a|<m`.

Therefore neither kernel intersection, tuple-color symmetrization, nor a
“choose the eventual canonicalizer” pigeonhole argument repairs the
normalized-family conclusion at linear color scale.  A different geometric
construction that realizes arbitrary small kernel differences while keeping
`B` normalized might still exist; this audit neither proves nor refutes it.
