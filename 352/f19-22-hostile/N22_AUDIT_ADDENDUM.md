# Hostile audit addendum: Erdős #352 lattice value at N=22

## Verdict

**PUBLISH.** The finite computational claim

```text
f(22)=44
```

passes an independent upper replay and a definition-level lower-witness
audit. It does not imply `f(N)=O(N)` and does not solve the continuous problem.

## Lower witness

The 44 source points are distinct and their canonical point-list SHA-256 is

```text
c58628d90ce038f181248cae108bfee7e199122958629284e8aed17b1ac2f1ca
```

All `C(46,3)=15,180` triples with repetition pass the exact integer predicate

```text
(A2-44)^2 - 4D2 > 0.
```

The minimum margin is 32, attained four times; the witness diameter squared
is 53. An independent 100-decimal comparison with the literal radical
inequality found a minimum literal gap of approximately `0.5968757625671513`
and no sign disagreement. Thus `f(22)>=44`.

## Independent C++ upper replay

The same standalone `audit_352_upper.cpp` used for N=19,20,21 was run at
N=22. It imports no producer code and uses shoelace area, polarization
distance, signed-vector orbit generation, independent lens reconstruction,
and explicit failures.

It obtained:

```text
raw signed nonzero vectors      1512
normalized D4 directions         207
directions with high points      170
fixed-high branches            33218
all branches                   33425
pool memberships             2705113
maximum branch pool              255
producer same-color pairs    23388468
full-vs-fast same-pair checks 34621947
global upper                      44
unique tight B                  (7,2)
```

Every selected same-color pair failed the full definition-level coexistence
test, and every full result agreed with the optimized pair predicate. Both the
reconstructed static coloring and a separate dynamic DSATUR coloring certify
the claimed upper bound.

The independent program serialized every reconstructed forced set, candidate
pool, branch label, and static color vector in the producer's canonical JSON
format. Its stream SHA-256 is exactly

```text
64858529dc55172b3d9abba0595768f3f7da04517be5129e51cb265f777f55d0
```

matching the producer. The hostile run took 19.17 seconds and 4,040 KiB
maximum resident memory.

The public reference output independently reports the same 207 diameter
cases, 170 cases with high points, 33,218 fixed-high branches, global upper
44, and unique tight direction `(7,2)`. The publication bundle's
`SHA256SUMS` manifest also passes.

No publication-blocking correction is required.
