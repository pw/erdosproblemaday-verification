# Erdos Problem 168: exact-prefix checkpoint (2026-08-11)

## Verdict

**PASS (computational continuation):** the exact smooth-prefix frontier is extended
from the published endpoint `f(5000)=3335` through `f(5020)=3347`.  This adds
twelve new A004059 rows, ending at `3347 5019`; the following prefix is flat.

**GAP (the actual Erdos problem):** this does not determine the density constant
or prove its irrationality.  The upper bounds at flat prefix steps are zero-gap
SCIP 10.0 integer-MIP results, not proof-assistant or DRAT certificates.  The
bundled SCIP was compiled without exact-solve support; the exact diagnostic is
retained in `exact_mode_probe.txt`.

## Definition and reduction

Let `d_1 < d_2 < ...` be the positive integers of the form `2^a 3^b`, and let
`f(k)` be the largest subset of `{d_1,...,d_k}` containing no
`{n,2n,3n}`.  In exponent coordinates, the forbidden sets are exactly the
corners

```text
(a,b), (a+1,b), (a,b+1).
```

The original interval problem has

```text
alpha = (1/3) sum_{k>=1} (f(k)-f(k-1))/d_k.
```

This is the definition and reduction used by GSW77, the Erdos Problems page,
OEIS A057561/A004059/A386439, and Veselinov's 2026 paper.  The source audit and
immutable source hashes are in `PROVENANCE.md`.

## Exact frontier

```text
k       5000 5001 5002 5003 5004 5005 5006 5007 5008 5009 5010
f(k)    3335 3335 3336 3337 3337 3338 3338 3339 3340 3340 3341

k       5011 5012 5013 5014 5015 5016 5017 5018 5019 5020
f(k)    3341 3342 3342 3343 3344 3344 3345 3346 3347 3347
```

The A004059-format continuation is in `b004059_extension.txt`.  Full structured
results, all 21 independent-set witnesses, and solver logs are under `frontier/`.

### Proof chain

1. The complement of a corner-free set is a vertex cover of the 3-uniform
   corner hypergraph.  The binary ILP minimizes `sum z_i` subject to
   `z_i+z_j+z_l >= 1` for every corner.
2. At `k=5000`, SCIP reports primal=dual=1665, hence `f(5000)=3335`, independently
   reproducing the published endpoint.
3. SCIP was run only at the baseline and flat constructive steps.  It reports
   primal=dual, zero gap, at `k = 5000, 5001, 5004, 5006, 5009, 5011, 5013,
   5016, 5020`.
4. At every other step, a checked witness has size `f(k-1)+1`.  Since adding one
   vertex can increase an independence number by at most one, that witness proves
   the next exact value without another optimization call.

The flat-step solver summary is:

```text
k      cover  f(k)  nodes  seconds
5000   1665   3335      3    45.56
5001   1666   3335     23   145.06
5004   1667   3337     11    99.48
5006   1668   3338     41   193.94
5009   1669   3340     15    89.32
5011   1670   3341     43   198.26
5013   1671   3342     43   206.16
5016   1672   3344     43   186.23
5020   1673   3347     15   108.20
```

Runtime was Python 3.12.3, PySCIPOpt 6.2.1, SCIP 10.0, one worker, and about
1275 seconds total wall time.  `verify_frontier_artifacts.py` independently
regenerates the smooth prefix and all corners, checks every witness, checks the
Lipschitz proof chain, and checks the recorded SCIP primal/dual endpoints.

### Small structural witness

Color `(a,b)` by `a+2b mod 3`.  Every corner has all three colors.  At `k=5000`
the color counts are `[1667,1667,1666]`; deleting color 2 gives 3334 points.
The exchange

```text
remove: (121,1), (123,0)
add:    (121,2), (122,0), (123,1)
```

gives a corner-free set of size 3335.  `verify_boundary_exchange.py` checks the
color counts, membership, cardinality, and all 4875 corners.  This is a compact
lower-bound certificate, not a new asymptotic structural theorem.

## Density audit

The certified interval through `k=5020` is, with outward rounding,

```text
[0.800965755006558989090420326388082412550050284333018241510270,
 0.800965755006558989090420326388082413556073056215427773096417]
```

It still certifies the same 35 digits
`0.80096575500655898909042032638808241`; the short extension narrows the tail
but does not cross the next decimal boundary.

The OEIS A386439 program has an off-by-one in its claimed upper endpoint.  It
subtracts the `k=5001` tail term and only then breaks on `i+1 > max(inc)`.
The unjustified omission is

```text
d_5001 = 32404306009923374140013298899777224704
1/(3*d_5001) = 1/97212918029770122420039896699331674112
              < 1.0286698725510571749770e-38.
```

This does not change the 35 displayed common digits.  Exact rational endpoints,
outward decimals, and the reconstructed buggy endpoint are in
`frontier/density_interval.json`.

## Evidence limitation

`Model.enableExactSolving(True)` was tested directly.  The wheel's SCIP library
prints:

```text
[scip_exact.c:161] ERROR: SCIP was compiled without exact solve support:
cannot enable exact solving mode.
```

It then raises `Exception: 'SCIP: unspecified error!'`.  A direct CNF for
`f(5001) <= 3335` was also generated (37,544 variables, 341,469 clauses, SHA-256
`cd494a464f39609cb2997b11bea91b290f08b3b86d383f0aee162bdb1477a12c`).
Kissat 4.0.4 returned `UNKNOWN` at the 300-second bound after 3,440,818 conflicts.
A forced-new version (`z_5001=0`, SHA-256
`948536a7d846a24a072d6dd86ff993e4206a5e30601a4b3eeb8a9bce2bc6229b`)
remained `UNKNOWN` in both Kissat and CaDiCaL at 180 seconds.  Finally, forcing
cover cardinality exactly 1665 is sound here: any smaller cover avoiding the new
vertex can be padded with old vertices.  That strengthened CNF (72,114 variables,
778,727 clauses, SHA-256
`3c0d35335eee5317a0f8fcca28016787aa75ea3b091226a22f5b226c58437423`)
also remained `UNKNOWN` in both solvers at 240 seconds.  No SAT proof is claimed
or frozen.

## Reproduction

Run the lightweight, solver-free checks:

```bash
./reproduce.sh
```

To rerun the optimization from an empty output directory, install
`requirements.txt` into a Python 3.12 environment and run:

```bash
python certify_frontier_scip.py \
  --bfile sources/b004059.txt \
  --through 5020 \
  --seconds-per-flat 900 \
  --out-dir rerun_frontier
```

The script is resumable after every completed prefix.  The original run was
restricted to one SCIP thread.
