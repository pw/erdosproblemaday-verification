# Hostile audit addendum: Erdős #352 lattice value at N=23

## Verdict

**PUBLISH.** The finite computational claim

```text
f(23)=45
```

passes an independent upper replay, a definition-level lower-witness audit,
and the completed strict producer run. It does not imply `f(N)=O(N)` and does
not solve the continuous problem.

## Lower witness

The 45 source points are distinct. Their compact canonical JSON point-list
SHA-256 is

```text
550732380cedbbb007ca37da695a77c0da7aaa31d87e15a0c8d75855a33807fb.
```

All `C(47,3)=16,215` triples with repetition pass the exact predicate
`(A2-46)^2-4D2>0`. The minimum margin is 56, attained eight times, and the
witness diameter squared is 52. Independent 100-decimal evaluation of the
literal radical inequality found minimum gap
`0.928932188134524755991556378951509607151640623115259634116601310046337607689464805748062328361792136`
and no sign disagreement. Thus `f(23)>=45`.

## Independent C++ upper replay

The standalone `audit_352_upper.cpp` imports no producer code. It uses
six-term shoelace area, polarization distance, exhaustive signed-vector/D4
reduction, independently rebuilt lenses and branches, a reconstructed static
coloring and a separate DSATUR coloring. Every pair sharing a selected color
was checked both by the optimized predicate and full repeated-triple
enumeration; the results agreed and every such pair was incompatible.

```text
raw signed nonzero vectors       1648
normalized D4 directions          225
directions with high points       187
fixed-high branches             40566
all branches                    40791
pool memberships              3893476
maximum branch pool               291
producer same-color pairs     34861434
independent same-color pairs  36649281
full-vs-fast same-pair checks 53167259
global upper                        45
tight B                     (6,4),(6,5)
```

The hostile replay took 37.55 seconds and 4,040 KiB maximum resident memory.
Its canonical producer transcript SHA-256 is

```text
7ce7aaa06bfd68ad93f7ac06c79a6454337ba034efb81c9e1a0ffb1541d250f3.
```

## Strict producer and public reference

The completed strict producer independently reports the same 225 diameter
cases, 187 cases with high points, 40,566 fixed-high branches, 40,791
certificates, 3,893,476 pool memberships, maximum pool 291, 34,861,434
same-color pairs, global upper 45, and tight vectors `(6,4),(6,5)`. Most
importantly, its certificate digest matches the hostile prediction exactly.
It finished with exit status 0 after 3,140.50 checker seconds (52:20.57 wall)
and 20,560 KiB maximum resident memory. The frozen strict log SHA-256 is
`57d775799dd12333fb3e678d1cb852ab37876a90761202631b9f3285bf4033a2`.

The public reference SHA-256 is
`af87f2a7b2a43949c7847abc903dcf7d7c78d83e85566dd694ad2a978eb61421`
and agrees on the complete finite case census and upper result. No
publication-blocking correction is required.
