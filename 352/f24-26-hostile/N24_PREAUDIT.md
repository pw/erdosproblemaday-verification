# Hostile audit: Erdős #352 lattice value at N=24

## Verdict

**PUBLISH.** Independent evidence and the completed strict producer certify
the finite claim

```text
f(24)=48.
```

No definition, repeated-triple, diameter-reduction, branch-completeness,
strict-predicate, coloring-certificate, transcript, or public-row discrepancy
was found.

## Lower witness

The source contains 48 distinct lattice points. Their compact canonical JSON
point-list SHA-256 is

```text
571adfd643a238c11e9261d81ef9c7b5732e85a9806352804138785858e77249
```

An independent scan checked all `C(50,3)=19,600` triples with repetitions.
Every triple satisfies

```text
(A2-48)^2 - 4D2 > 0.
```

The minimum exact integer margin is 25, attained twice, at

```text
((0,0),(2,5),(7,1))
((0,3),(5,-1),(7,4)).
```

The maximum squared diameter is 65 and maximum twice-area is 34. A separate
100-decimal literal-radical evaluation agrees in sign on every triple; its
smallest literal gap is

```text
0.428932188134524755991556378951509607151640623115259634116601310046337607689464805748062328361792136.
```

The witness source file SHA-256 is
`dded96cc806568ea1ac3924d1b412937a0849fa02536821c97a69a9e2cfd1adf`.
Thus `f(24)>=48`.

## Independent C++ upper replay

The standalone C++ checker imports no producer code. It independently builds
the signed-vector/D4 direction census, diameter lenses, no-high and every
fixed-high branch, pair-compatibility graphs, static producer-style colorings,
and separate DSATUR colorings. For every pair sharing a selected color it
compares the optimized coexistence predicate to full repeated-triple
enumeration, and requires the pair to be incompatible.

It obtained:

```text
raw signed nonzero vectors       1788
normalized D4 directions          243
directions with high points       204
fixed-high branches             48626
all branches                    48869
pool memberships              5341706
maximum branch pool               327
producer same-color pairs     49876704
independent same-color pairs  52657947
full-vs-fast same-pair checks 78060046
producer global upper               48
producer tight B        (7,2),(7,3),(7,4),(8,1)
```

The separate DSATUR coloring improves the `(8,1)` branch but still gives
global upper 48, tight at `(7,2),(7,3),(7,4)`. Chromatic optimality is neither
asserted nor needed: any proper coloring bounds clique size.

The reconstructed canonical producer transcript has SHA-256

```text
4bdd9d9f9bad728c22531e753711fe126971ce3eb29d52937c818add3b15202b.
```

The hostile replay took 48.31 seconds and 3,896 KiB maximum resident memory.

## Completed strict producer

The strict producer independently reports the same 243 diameter cases, 204
cases with high points, 48,626 fixed-high branches, 48,869 certificates,
5,341,706 pool memberships, maximum pool 327, 49,876,704 audited same-color
pairs, global upper 48, and tight vectors `(7,2),(7,3),(7,4),(8,1)`. Its
certificate digest matches the hostile prediction exactly. It completed with
exit status 0 after 4,094.44 checker seconds (1:08:14 wall) and 20,968 KiB
maximum resident memory. The frozen strict log SHA-256 is

```text
f0f34a1e2f07ae0b90cece61729f7d36fbb54ac83f8e640d41e35558baf26de3.
```

## Public reference comparison

The public reference file SHA-256 is
`50d008f68722eeda4709c957ba6ff59464a4efc357e3650719d7d70143469c38`.
Every one of its 243 rows was rebuilt from the independent transcript. Exact
equality holds for `B`, squared diameter, low count, high count, no-high
upper, high-side upper, and total case upper. The aggregate counts and tight
directions also agree.

No correction or qualification beyond “finite exact lattice value” is
required. The claim does not imply `f(N)=O(N)` and does not solve the
continuous version.
