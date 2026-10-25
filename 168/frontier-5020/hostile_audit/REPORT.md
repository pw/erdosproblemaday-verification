# Independent hostile audit: Erdos Problem 168 frozen bundle

Audit date: 2026-08-11 UTC

Frozen bundle audited, without modification:

`/home/exedev/erdos_scratch/frozen_erdos168_20260811`

Independent audit directory:

`/home/exedev/erdos_scratch/audit_erdos168_20260811_144602`

## Verdict

**PASS, conventional computational result.** I found no counterexample or semantic
error in the claimed continuation. An independently written verifier reconstructs
the smooth prefix and forbidden triples by different methods, checks all 21
witnesses, validates every propagation step, reproduces the density arithmetic,
and confirms every frozen hash. A separately written selected-set SCIP model,
with reversed variable creation, changed constraint order, and changed
randomization, independently reproduced all nine baseline/flat objectives.

**GAP, proof-carrying exactness.** The upper bounds are floating-MIP results from
SCIP. The installed SCIP 10.0.2 library was compiled without exact solving
support. Neither the original run nor this audit produced a DRAT/LRAT,
proof-assistant theorem, exact rational branch-and-bound certificate, or another
independently checkable upper-bound certificate. The word "exact" in the bundle
is justified only in the normal computational-MIP sense, not in the
proof-carrying sense.

**GAP, the actual Erdos problem.** The bundle does not determine the constant in
closed form and does not prove rationality or irrationality. The live problem
remains open.

## Material findings

1. **All nine upper-bound anchors depend on floating SCIP.** These are `k = 5000,
   5001, 5004, 5006, 5009, 5011, 5013, 5016, 5020`. The other twelve new rows have
   checked constructive witnesses and follow from the one-vertex Lipschitz bound,
   but their proof chain inherits the most recent floating-MIP anchor.

2. **The density enclosure additionally depends on all 3,335 historical OEIS
   A004059 rows.** The bundle pins and audits the OEIS program and b-file, and the
   current remote bytes match, but it does not freeze proof certificates for the
   historical computations. Thus the rational endpoint arithmetic is exact
   conditional on that b-file, while the overall mathematical enclosure is not
   proof-carrying.

3. **The SAT attempts are correctly described as UNKNOWN, but are not frozen.**
   The three reported CNF hashes and headers match files still present outside
   the bundle. The frozen bundle contains no CNF, solver log, or completed proof.
   The large `.drat` files outside the bundle are interrupted partial traces, not
   proofs. Independent five-second Kissat 4.0.4 and CaDiCaL 3.0.1 probes also
   timed out UNKNOWN.

4. **Minor reproducibility blemishes do not change the result.**
   `frontier/results.json` retains an absolute path into the author's earlier
   `fresh3_...` directory. The documented rerun command overrides it correctly.
   `requirements.txt` pins PySCIPOpt but does not provide a wheel hash or a
   hermetic Python/SCIP environment. The lightweight verifier is portable and
   passed as frozen.

## Current statement and provenance

The [live page](https://www.erdosproblems.com/168), read through Bright Data on
2026-08-11 because direct HTTP returned 403, asks for

`lim_{N->infinity} F(N)/N`

where `F(N)` is the largest size of a subset of `[1,N]` containing no
`{n,2n,3n}`, and asks whether the limit is irrational. It reports zero claimed
proofs and no current worker. Its last edit remains 2026-03-23. The current
forum contains the September 2025 Eberhard correction to

`0.80096575500655898909042032638808241...`.

The current [Formal Conjectures transcription](https://github.com/google-deepmind/formal-conjectures/blob/main/FormalConjectures/ErdosProblems/168.lean)
has SHA-256
`06ead6c583e5d4a4a31668a876a7dbbf5ca9e6d32b40535c4d0069eebfa73827`
at file commit `c252a41054125b5fd9c8356e2137cd9b55337657` (2026-07-16).
It formalizes the interval question and the already-known existence variant; it
does not formalize the smooth-prefix reduction or this computation.

The original Graham-Witsenhausen-Spencer paper was independently downloaded
from the link now exposed by OEIS. The PDF has SHA-256
`bc7a6525edb522d4b6889e90595ab61b8b979c464cb5fdcb8d6b07ef021aa193`.
Its Section 4 explicitly performs the coprime-to-6 component decomposition,
defines `f(k)` on the ordered `2^a 3^b`, obtains the increment series, and asks
whether the density is irrational. Its printed small table contains the known
historical `f(30)` error already noted on OEIS A057561.

### OEIS snapshot

Current pages: [A004059](https://oeis.org/A004059),
[A057561](https://oeis.org/A057561), and
[A386439](https://oeis.org/A386439).

* A057561 is `f(k)`, the maximum configuration-free subset size among the first
  `k` 3-smooth numbers.
* A004059 gives the first prefix at which each successive value of `f` occurs.
* A386439 gives the decimal digits of the interval density constant.

The current A004059 b-file has 3,335 data rows, ends at `3335 5000`, and has
SHA-256 `bba41cd187052c20e638c539893f16f73d23956f9900caa882e06778256b15ea`.
The current remote bytes exactly match the frozen bytes. The current OEIS source
hashes also match the bundle:

```text
1e38d564f8e42ea7c26843186ca76c4077e797ebcac402a3de00b3f8df7e2529  A004059 Python/Sage source
92b08a0c6647f55851356f6f3f6f7c8435a19446d5237c0ab0a53a9357aaa25d  A386439 Python/Sage source
```

The independently downloaded synthesized A057561 b-file contains its published
69 terms and is exactly reconstructed from the corresponding A004059 first-hit
positions. The synthesized A386439 b-file contains exactly the 35 digits above.
Their audit snapshot hashes are respectively
`266e452f022fe6d79d1d2a5c02223de03626a87b925f2b8c370b904fafa98a49`
and `d1258df430b6a8fc9188ffbcda8a9ab2eef3be6a953a268ee383456960eea8e4`.

The bundle correctly identifies the numerical robustness issue in the A004059
program: `int(p.get_objective_value())` truncates a floating solver value rather
than rounding and checking tolerance. I found no evidence that it changed a
published row, but it is a real weakness.

## Mathematical reconstruction

Every positive integer has a unique factorization `m d`, where `(m,6)=1` and
`d=2^a 3^b`. Multiplication by 2 or 3 stays inside one fixed-`m` component. If
`d_1<d_2<...` are the 3-smooth numbers, the component ending at `d_k` contributes
`f(k)`. Writing `epsilon_k=f(k)-f(k-1)` and counting integers coprime to 6 gives

`alpha = (1/3) sum_{k>=1} epsilon_k/d_k`.

Inside one smooth component, `2^a3^b`, `2^(a+1)3^b`, and `2^a3^(b+1)` are exactly
`{n,2n,3n}`. I reconstructed the first 5,021 smooth numbers by sorting a finite
`256 x 192` exponent rectangle, with exact boundary inequalities proving the
rectangle complete. I then generated forbidden triples by integer multiplication,
not by the bundle's heap/corner code. The resulting triples agree exactly with
the exponent corners.

The complement of a corner-free set is a vertex cover of the 3-uniform corner
hypergraph, so `f(k)=k-tau(k)`. Also, adding one vertex gives

`f(k-1) <= f(k) <= f(k-1)+1`.

Therefore a checked witness of size `f(k-1)+1` proves an increasing row once
the preceding row is established. No nested family of optimal witnesses is
required. I also checked, for every prefix through 5,020, the stronger structural
claim from Veselinov: a newly added point `(a,b)` adds no edge when `b=0`, and
otherwise adds exactly the edge anchored at `(a,b-1)`.

## Frontier result

The reconstructed values are:

```text
k       5000 5001 5002 5003 5004 5005 5006 5007 5008 5009 5010
f(k)    3335 3335 3336 3337 3337 3338 3338 3339 3340 3340 3341

k       5011 5012 5013 5014 5015 5016 5017 5018 5019 5020
f(k)    3341 3342 3342 3343 3344 3344 3345 3346 3347 3347
```

Thus the twelve A004059 continuation rows `3336 5002` through `3347 5019`
are correctly formed, and `k=5020` is flat.

### Baseline dependency and witnesses

The b-file asserts the published endpoint `f(5000)=3335`; the computation does
not merely assume it. The color counts for `a+2b mod 3` at `k=5000` are exactly
`[1667,1667,1666]`. Deleting color 2 and making the stated exchange

```text
remove (121,1), (123,0)
add    (121,2), (122,0), (123,1)
```

gives a checked lower-bound witness of size 3335. The original SCIP transcript
reports a minimum cover of 1665, and the independent selected-set SCIP rerun
reports maximum size 3335. This anchors the propagation chain in the normal
floating-MIP sense.

All 21 frozen witness files have the claimed cardinality, contain no duplicate or
out-of-prefix point, and avoid every forbidden triple. The audit performed
102,585 per-row corner checks.

### Independent SCIP rerun

This audit used selected-set variables and `x_i+x_j+x_l <= 2`, whereas the bundle
uses complement cover variables and `z_i+z_j+z_l >= 1`. Variables and constraints
were created in reverse order; the random seed shift and permutation seed were
changed. Every row again terminated `optimal` with equal reported primal and dual
bounds and zero gap:

```text
k      claimed f   author nodes   audit nodes
5000       3335          3            15
5001       3335         23            41
5004       3337         11            23
5006       3338         41            45
5009       3340         15            17
5011       3341         43            55
5013       3342         43            37
5016       3344         43            47
5020       3347         15            15
```

This is a genuine independent code/formulation rerun, but not an independent
solver and not exact arithmetic: both runs use SCIP.

### CBC falsification attempts

CBC Devel, build 2026-03-23, was run for 300 seconds on every new flat step.
At a claimed flat step with previous optimum `q`, each direct selected-set model
forces the new vertex and requires at least `q+1` selected vertices. A feasible
solution would be a counterexample; infeasibility would reproduce the upper
bound. CBC found no counterexample, but every search retained open nodes and hit
the time limit:

```text
k      nodes    iterations   result
5001    1849      105182     UNKNOWN
5004    1470       92010     UNKNOWN
5006    1293      102607     UNKNOWN
5009    1526       97985     UNKNOWN
5011    1749      102824     UNKNOWN
5013    1332      112002     UNKNOWN
5016    1598      119372     UNKNOWN
5020    1548       93772     UNKNOWN
```

A direct `k=5000` CBC maximization accepted the independently reconstructed
3335-point start but timed out after 2,338 nodes with an upper bound of 3343.08.
CBC is also a floating MIP solver. None of these runs counts as upper-bound
evidence; they are retained as unsuccessful counterexample searches.

## Density arithmetic

Using exact `Fraction` arithmetic and

`sum_{a,b>=0} 1/(2^a3^b) = 3`, 

I independently reproduced the frozen 60-place outward interval through 5020:

```text
[0.800965755006558989090420326388082412550050284333018241510270,
 0.800965755006558989090420326388082413556073056215427773096417]
```

The exact width is

```text
117128852097886899905192010372849039263 /
116427635011404771702822091888321129375931223181685076181269488070775799808
```

The lower/upper rational strings in `frontier/density_interval.json`, their
directed decimal roundings, the count of known increments, and the last smooth
number all match independently. The interval fixes exactly 35 decimal places,
not 36.

The A386439 source off-by-one is real. Its loop subtracts the current tail term
before testing `i+1 > max(inc)`, so it removes the `k=5001` term and only then
breaks. Here

```text
d_5001 = 32404306009923374140013298899777224704
omitted = 1/(3*d_5001)
        = 1/97212918029770122420039896699331674112
```

Adding that exact fraction to the program's reconstructed buggy upper endpoint
gives the corrected published-5000 upper endpoint exactly. The omission is too
small to change the 35 displayed digits.

## Post-page paper

[Nikola Veselinov, arXiv:2604.15515v1](https://arxiv.org/abs/2604.15515) was
submitted 2026-04-16, after the live page's last edit. The current arXiv record
still has only v1. The current PDF matches the frozen hash
`68e3b58de8d2bf8f4e5fb48560f2c43e489d7979e7e0f8c44ed2ddf1c7adbb14`.

The paper proves, for `S={2,3}`, `f(k)=2k/3+O(sqrt(k))`, derives the density
series and explicit reciprocal-tail formula, proves that optimal prefix sets
cannot always be nested (Proposition 6.2), and proves the unique-new-corner
increment criterion (Proposition 6.3). It does not determine `alpha` and does not
settle irrationality. Its Proposition 1.4 only shows that some nonperiodic binary
reciprocal sequences have rational sums; it says nothing decisive about the
specific increment sequence here.

## Integrity and reproducibility

The frozen `SHA256SUMS` lists exactly all 46 other files in the bundle: no file
is omitted and no nonexistent file is listed. Every digest passes. The bundle's
own `./reproduce.sh` passes without modification.

The independent lightweight verification command is:

```bash
python3 independent_audit.py \
  --bundle /home/exedev/erdos_scratch/frozen_erdos168_20260811 \
  --online-sources sources \
  --summary verification_summary.json
```

It does not import or execute author code. The independent solver generators,
LP models, CBC logs, SCIP logs/results, exact-mode probe, source snapshots, and
solver summary are all retained in this audit directory. `AUDIT_SHA256SUMS`
freezes the audit artifacts themselves.

## Bottom line

No counterexample, indexing error, arithmetic error, witness defect, provenance
mismatch, or manifest defect was found. The continuation to `f(5020)=3347` is a
well-reproduced floating-MIP computation. It should not be represented as a
formal/exact certificate, and the density interval should be described as
conditional on the historical OEIS b-file plus the floating-MIP upper bounds.
