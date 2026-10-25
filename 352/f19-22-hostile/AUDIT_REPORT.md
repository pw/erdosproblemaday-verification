# Hostile audit: Erdős #352 lattice values at N=19,20,21

## Verdict

**PUBLISH.** The three proposed finite computational results are sound:

```text
f(19)=38, f(20)=39, f(21)=41.
```

No missing diameter orbit, lens point, no-high/fixed-high branch, repeated
triple, or incompatible same-color pair was found. These remain finite exact
values only; they neither prove `f(N)=O(N)` nor solve the continuous problem.

## Definition and exact predicate

A finite `S` in `Z^2` is `N`-avoiding when every triple `p,q,r` in `S`, with
repetition allowed, obeys

```text
|area(p,q,r)-N| > diameter(p,q,r).
```

Writing `A2` for twice the absolute area and `D2` for squared diameter, this is
equivalent to the exact integer predicate

```text
(A2-2N)^2 - 4D2 > 0.
```

The hostile checker uses the six-term shoelace formula for `A2` and the
polarization identity for `D2`, rather than the producer's based-vector area
and coordinate-difference distance formulas.

## Lower witnesses

The source JSON files were byte-compared with the unmodified public witness
repository at commit `09e5c5393943c881ab60118aa32fe5660539c8d5`. The producer's
embedded tuples agree point-for-point. Definition-level repeated-triple scans
give:

| N | points | repeated triples | minimum integer margin | diameter squared | point-list SHA-256 |
|---:|---:|---:|---:|---:|:---|
| 19 | 38 | 9,880 | 5 | 45 | `a9b18dac9346f907dde492bac513b8292b3397e633d1e2483001604f3778968b` |
| 20 | 39 | 10,660 | 21 | 52 | `3d6dd7bb906fe6a6f8c1e2d9ba79566b0eaaeac780d0e5af2260cf597050198a` |
| 21 | 41 | 12,341 | 5 | 52 | `471accfaed1d71f8102fed8055bd3b5f31f487acdfd7d64c68bb002c5b351a95` |

Thus these witnesses prove the three lower bounds. The report correctly makes
no priority claim for them.

## Completeness of the upper reduction

Applying the condition to `(p,p,q)` gives `|p-q|<N`. Translate a diameter pair
to `A=(0,0)` and use signed-coordinate and swap symmetries to normalize the
other endpoint as `B=(x,y)`, `x>=y>=0`. The hostile checker generates all raw
signed vectors first and then quotients by the full eight-element symmetry:

| N | raw nonzero vectors | normalized D4 classes |
|---:|---:|---:|
| 19 | 1,124 | 156 |
| 20 | 1,244 | 172 |
| 21 | 1,368 | 188 |

Orbit-size reconstruction agrees exactly in all three cases. Every further
point lies in the closed two-disc lens of the diameter pair, making the finite
integer box exhaustive. Every surviving point is either below or above the
forbidden area band, so every avoiding set occurs in the no-high branch or in
at least one branch with a fixed high point.

Within each branch, a genuine avoiding extension is a clique in the
pair-compatibility graph. Any proper coloring therefore bounds its size; no
chromatic optimality claim is needed.

## Independent C++ upper replay

`audit_352_upper.cpp` imports no producer code. It independently rebuilds the
geometry, branch pools, and pair graphs. It constructs both the producer's
static degree-order coloring and a dynamic DSATUR coloring. It then checks the
logically critical direction using full repeated-triple enumeration for every
pair occurring in either selected same-color partition, while also comparing
that full result against the optimized pair predicate.

The replay returned:

| N | directions | with high | fixed-high | all branches | pool memberships | max pool | full same-pair checks | upper | tight B |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|:---|
| 19 | 156 | 123 | 16,622 | 16,778 | 760,404 | 158 | 7,582,345 | 38 | `(6,3)` |
| 20 | 172 | 138 | 21,122 | 21,294 | 1,185,058 | 183 | 12,781,104 | 39 | `(6,4)` |
| 21 | 188 | 153 | 26,250 | 26,438 | 1,764,968 | 219 | 20,819,634 | 41 | `(5,5)`, `(6,4)` |

It reproduced the producer's reported same-color counts exactly:

```text
N=19  5,673,504
N=20  9,215,235
N=21 14,588,044
```

As a particularly strong transcript check, the independent implementation
serialized every reconstructed forced set, candidate pool, branch label, and
static color vector in the producer's canonical JSON format. SHA-256 over
those streams reproduced the producer digests byte-for-byte:

```text
N=19  2d8b6e3ef793869a9e6a05726e6e7b434efc7b3695d3307343e1b083a4e1822d
N=20  bafa932d0529410be48dd4fb8cbd31362ca00bb1188a41699107522f89588996
N=21  cd5c1d7f245d3412ee966bd4ffbf138f06f6d5213d57ab589b9563001ae9bca3
```

The C++ hostile replays took 4.84, 7.15, and 11.05 seconds, respectively, and
used under 4 MiB maximum resident memory.

## Public implementation and packaging checks

The public upper repository was fetched at commit
`7a4a19468771766cb4f20e10dfa5cf770cc2487b`. Its `exact_bound.py` is
byte-identical to the frozen reference source and has SHA-256
`2746c9c19326d2195aee926588ca4a796747d44efdc83d3907d42cab41abe790`.
Its frozen N=19,20,21 outputs agree on every diameter split, branch count,
global upper bound, and tight direction.

The three publication bundles' `SHA256SUMS` manifests pass. Their source
witness and public reference copies are byte-identical to the checked source
files, and their full producer logs have SHA-256:

```text
N=19  502e2890020256bc742bfd39f8c70c9e330bbf28f08616a75cff109b383731c4
N=20  8e246e8d969ec2ac319c89085f3c0ce5a6ec5902d0e8b72f5b741197c20772e1
N=21  99789bff3babb200e924a193f63fdc07f41550c8d16f77152a0ddbe7a0150382
```

The producer uses Python `assert`, so its documented invocation must remain
ordinary `python3`, never `python3 -O`. The hostile C++ checker uses explicit
failures and is not affected by Python optimization flags.

No publication-blocking correction is required.
