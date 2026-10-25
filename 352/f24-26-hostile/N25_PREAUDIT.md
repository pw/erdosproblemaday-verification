# Hostile audit: Erdős #352 lattice value at N=25

## Verdict

**PUBLISH.** Independent evidence and the completed strict producer certify
the finite claim `f(25)=52`. No definition, repeated-triple, diameter-reduction,
branch-completeness, strict-predicate, coloring-certificate, transcript, or
public-row discrepancy was found.

## Lower witness

The source has 52 distinct points, with canonical point-list SHA-256

```text
f6fb2cd93d56b4490532c63a1a174119c090321c6746b17d8748b3c12c2c9a24.
```

All `C(54,3)=24,804` triples with repetition satisfy
`(A2-50)^2-4D2>0`. The exact minimum margin is 25 (multiplicity 12),
the maximum squared diameter is 58, and the maximum twice-area is 35.
A separate 100-decimal literal-radical evaluation agrees in sign on every
triple and has minimum gap

```text
0.428932188134524755991556378951509607151640623115259634116601310046337607689464805748062328361792136.
```

The witness source SHA-256 is
`040775ecaaca5b6a004b4bceafddd3a57e0330fe88ca2d447ac62e5cb45ac419`.
Thus `f(25)>=52`.

## Independent C++ upper replay

The standalone checker imports no producer code. It independently rebuilds
the complete signed-vector/D4 direction census, lenses, no-high and every
fixed-high branch, compatibility graphs, the producer-style static coloring,
and a separate DSATUR coloring. It full-enumerates repeated triples for every
pair sharing a selected color, agrees with the optimized predicate every time,
and requires every such pair to be incompatible.

```text
raw signed nonzero vectors        1940
normalized D4 directions           263
directions with high points        222
fixed-high branches              58662
all branches                     58925
pool memberships               7476577
maximum branch pool                362
producer same-color pairs      70784474
independent same-color pairs   75177204
full-vs-fast same-pair checks 114194578
global upper                         52
unique tight B                    (7,3)
```

The reconstructed canonical producer transcript has SHA-256

```text
da9e4abb06fc00a51d58ff40e255889c7d9c3cafe502276e97d52260be3f5a3a.
```

The hostile replay took 64.04 seconds and 4,024 KiB maximum resident memory.

## Completed strict producer

The strict producer independently reports the same 263 diameter cases, 222
cases with high points, 58,662 fixed-high branches, 58,925 certificates,
7,476,577 pool memberships, maximum pool 362, 70,784,474 audited same-color
pairs, global upper 52, and unique tight vector `(7,3)`. Its certificate digest
matches the hostile prediction exactly. It completed with exit status 0 after
6,223.87 checker seconds (1:43:43 wall) and 20,836 KiB maximum resident
memory. The frozen strict log SHA-256 is

```text
bfde7e19bd04ed026ac65801a7d7d112ff08fdc1f8ccc6eff4a4f1f9294db08f.
```

## Public reference comparison

The public reference SHA-256 is
`dd50b6762bec5a69932856886ada7929b38422b3589c2b2474c792b5bb072aca`.
Every one of its 263 per-diameter rows agrees exactly with the rebuilt
certificates on `B`, squared diameter, low/high counts, no-high bound,
high-side bound, and total bound. The 58,662 high branches, 222 cases with
high points, global upper 52, and unique tight direction `(7,3)` all match.

No correction beyond the usual “finite exact lattice value” scope is needed.
This claim does not imply `f(N)=O(N)` and does not solve the continuous
problem. The separate N=24 `2x-y` fiber counterexample is an explicitly killed
heuristic and plays no role in this proof.
