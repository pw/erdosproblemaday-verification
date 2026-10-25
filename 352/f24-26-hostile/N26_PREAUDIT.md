# Hostile audit: Erdős #352 lattice value at N=26

## Verdict

**PUBLISH.** Independent upper and lower evidence and the completed strict
producer certify `f(26)=52`. No definition, repeated-triple, strict-predicate,
diameter-reduction, branch-completeness, coloring-certificate, transcript, or
public-row discrepancy was found.

## Lower witness

The source has 52 distinct points. Its compact canonical point-list SHA-256 is

```text
b1cb2421471e2e832335e20db20a5f6013b0c2e0db54a844475e5a0f3cc1b70c.
```

All `C(54,3)=24,804` triples with repetition satisfy
`(A2-52)^2-4D2>0`. The exact minimum margin is 12, attained twice, at

```text
((0,0),(6,-1),(6,5))
((1,4),(2,-2),(7,4)).
```

The maximum squared diameter is 65 and maximum twice-area is 36. A separate
100-decimal literal-radical evaluation agrees in sign on every triple and has
minimum gap

```text
0.189750324093345605870277264240898586431694863351436699822756239809214411063272945574566947732995105.
```

The source witness SHA-256 is
`138562cf4f47f42c66af5f722524cf6a6fa9a7ef6ea06522d46fe361357e3a2f`.
Thus `f(26)>=52`.

## Independent C++ upper replay

The standalone checker imports no producer code. It independently rebuilds
the complete signed-vector/D4 census, diameter lenses, no-high and every
fixed-high branch, compatibility graphs, producer-style static coloring, and
a separate DSATUR coloring. For every pair sharing a selected color, it
compares the optimized coexistence predicate to full repeated-triple
enumeration and requires the pair to be incompatible.

```text
raw signed nonzero vectors        2108
normalized D4 directions           285
directions with high points        243
fixed-high branches              70850
all branches                     71135
pool memberships              10435095
maximum branch pool                412
producer same-color pairs     103499415
independent same-color pairs  110471024
full-vs-fast same-pair checks 170658509
producer global upper                52
producer tight B       (7,3),(7,4),(8,2),(8,3)
```

The separate DSATUR coloring improves `(8,2)` but still gives global upper
52, tight at `(7,3),(7,4),(8,3)`. Chromatic optimality is not asserted or
needed. The reconstructed canonical producer transcript has
SHA-256

```text
a0a09b5ebee6bcdae77c14f296b0172c2586a95af83250ab0f5237fddb0d827a.
```

The hostile replay took 102.31 seconds and 3,972 KiB maximum resident memory.

## Completed strict producer

The strict producer independently reports the same 285 diameter cases, 243
cases with high points, 70,850 fixed-high branches, 71,135 certificates,
10,435,095 pool memberships, maximum pool 412, 103,499,415 audited same-color
pairs, global upper 52, and tight vectors `(7,3),(7,4),(8,2),(8,3)`. Its
certificate digest matches the hostile prediction exactly. It completed with
exit status 0 after 9,988.56 checker seconds (2:46:28 wall) and 20,836 KiB
maximum resident memory. The frozen strict log SHA-256 is

```text
49c03044e0954e3e033e2a589d3952bb75c714cb75028e507f2f711a7f4103ab.
```

## Public reference comparison

The completed public reference SHA-256 is
`1067e1b342d27dda5c4268edbf90688af4c8eb7f626328e36ae69c1948595434`.
Every one of its 285 per-diameter rows agrees exactly with the independent
transcript on `B`, squared diameter, low/high counts, no-high upper,
high-side upper, and total case upper. The 70,850 high branches, 243 cases
with high points, global upper 52, and producer-tight list
`(7,3),(7,4),(8,2),(8,3)` all match.

No correction beyond finite exact lattice scope is required. This claim does
not imply `f(N)=O(N)` and does not solve the continuous problem.
