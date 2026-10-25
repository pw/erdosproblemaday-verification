# Independent hostile audit: Erdos Problem 174 pyramid closure

Audit completed: 2026-08-11T19:53:55Z

Audited bundle:
`/home/exedev/erdos_scratch/fresh10_erdos174_pyramid_20260811`

This audit did not edit the audited bundle or `/home/exedev/ErdosProblemADay`.

## Verdict

- **Mathematical result: PASS.** Moore's Theorem 1.2 has the advertised
  quantifiers and the reconstruction in `REPORT.md` is valid modulo the three
  cited inputs. No counterexample or circular dependency was found.
- **Scope statement: PASS.** This is a closure theorem and a resolution of
  Ivan--Leader--Walters Conjecture 8, not a characterization of all finite
  Euclidean Ramsey sets and therefore not a solution of Erdos Problem 174.
- **Internal frozen custody: PASS.** Every non-manifest regular file is listed
  exactly once, all eleven hashes verify, and the official current arXiv PDF
  for 2608.09649v1 is byte-identical to the frozen copy.
- **Public release of the bundle as-is: GAP.** Do not publish PDFs lacking a
  downstream redistribution license, and replace the assert-based verifier
  before describing the public checker as robust.

The mathematical PASS is not peer review. The source is a one-day-old arXiv
v1 preprint with no peer-reviewed version or journal reference located, and
the independent literature search cannot establish absolute priority or
exclude private, unindexed, or same-day work.

## Findings requiring action

### 1. Third-party PDF licensing (public-release blocker)

`sources/EGMRSSone.pdf` prints "All rights of reproduction in any form
reserved." `sources/frankl_rodl_1990.pdf` prints that license or copyright
restrictions may apply to redistribution. The official ILW arXiv page uses
arXiv's default nonexclusive-distribution license; that grants distribution
rights to arXiv.org, not a general downstream CC license. Keep all three files
in the private scratch custody bundle. A public package should contain official
citations, URLs, theorem/page locations, and the observed SHA-256 hashes, but
not those PDF bytes unless redistribution permission is established.

Moore uses CC BY 4.0. Behague v3 uses CC BY-SA 4.0. Those two may be
redistributed only with their respective attribution and license conditions;
omitting every third-party PDF is the simplest public-safe policy.

This does not affect the proof audit. The relevant statements were read in the
primary papers, and Crossref independently confirms both bibliographic records
and DOIs.

### 2. `assert` makes the verifier optimization-sensitive

Every substantive condition in `verify_bundle.py` is an `assert`. The command
`python3 -OO verify_bundle.py` printed the same final PASS as the documented
command even though Python removed the assertions. `PYTHONOPTIMIZE=1` has the
same defect. Replace assertions with an explicit check function that raises a
runtime exception or exits nonzero.

The documented unoptimized run itself passed:

```
manifest_files=11
pinned_files=7
geometric_equalities=239
abstract_colourings=27
PASS: identities, source markers, live transcript, and pyramid gadget
```

Also make the public checker reject duplicate manifest entries and unexpected
regular files. The current bundle happens to have neither problem, but the
current verifier does not enforce completeness.

### 3. Novelty scope should name the prior subclass

Ivan--Leader--Walters Corollary 4 already proves the pyramid conclusion for a
subsoluble base (and proves a subtransitivity statement for a transitive base).
Moore's new theorem removes that structural assumption and handles an arbitrary
Ramsey base. State this explicitly. Behague's background result that nearly all
known Ramsey examples are subsoluble further limits any claim that every
instance furnished by the theorem is a new configuration.

Moore nevertheless proves the full Conjecture 8 statement. This finding narrows
the novelty wording; it does not weaken the theorem.

### 4. Peer-review wording

The candidate calls the paper "unrefereed." Public metadata establishes that
no peer-reviewed version or journal reference was located; it cannot establish
whether the manuscript has ever privately entered a referee process. Prefer
the observable statement and say that the site treats the arXiv v1 claim as
unrefereed, rather than asserting unknowable private review history.

### 5. Two minor evidentiary/edge limitations

The historical claim that no matching scratch directory existed before bundle
creation is not reproducible from the finished bundle. It is non-load-bearing.
Likewise, the OEIS search result is summarized but its raw response is not
frozen. The rendered page itself has no related-OEIS line, and the theorem is
qualitative, so this does not affect the publication result.

The proof tacitly uses a nonempty base when it calls a monochromatic copy of
`P` a colour and chooses a point for isometry extension. This is the standard
meaning of a finite configuration. If the set-theoretic empty set is allowed as
a Ramsey set, handle it in one sentence: `B = empty` gives the Ramsey singleton
`{z}` directly.

## Exact live and site gate

At the independent check, the local site files still had the frozen hashes:

```
08e988d080d5317adf768ba827b4f21397699b30d28cc749807616b6753a3b76  src/index.js
9ad7647dcd9ee51b2e08233e77d0a0c21b1321033b923c13ac50a563c6a9c052  src/ledger_data.js
```

The worktree had an existing modification to `src/ledger_data.js`; no file was
changed by this audit. Robust scans for `problemNum: 174`, ledger key `n:174`,
the exact problem URL, `2608.09649`, Kenneth Moore, pyramid/Ramsey terminology,
and the defining Euclidean-Ramsey phrases found no target entry in either site
file. Incidental digit string `174` occurrences inside other entries are not
semantic matches.

A fresh Bright Data render at about 2026-08-11T19:47Z independently showed:

- status `OPEN`;
- page last edited 16 October 2025;
- four comments and zero claimed proofs;
- no current worker and no current formalizer;
- newest comment 15 February 2026, mentioning Behague only;
- no occurrence of Moore, the pyramid title, or arXiv:2608.09649.

This confirms the screenshot transcription. Site status is only a gate and is
not evidence that Moore's theorem is correct or novel.

## Primary arXiv custody

The official `https://arxiv.org/pdf/2608.09649` download at audit time and the
frozen `sources/moore2608.09649.pdf` had the identical SHA-256:

```
2a1f866a06e5a8452f8b8425e6e244706a23eb039bb427eac5a51ade028fd45e
```

The arXiv abstract page and API both identified exactly v1, Kenneth Moore,
title `A pyramid with a Ramsey base is Ramsey`, five pages and one figure,
submitted 2026-08-10T14:26:02Z. The API theorem summary matches the report.

The official current ILW and Behague PDFs were also byte-identical to the
frozen copies:

```
9e7a0da78ec6094bde530cf789c9ef58a680810ef2ac52feac49114c4c884f0e  Ivan--Leader--Walters 2606.13472v1
f0ee8b166026281c106562102657a71a7be8a85db964e0b370244ddc4764fbfd  Behague 2510.15677v3
```

Crossref independently confirms the classical metadata:

- EGMRSS, JCTA 14(3), 341--363 (1973),
  DOI `10.1016/0097-3165(73)90011-3`;
- Frankl--Rodl, JAMS 3(1), 1--7 (1990),
  DOI `10.1090/S0894-0347-1990-1020148-2`.

## Theorem and quantifier audit

Write `R^n ->_r T` when every map from `R^n` into at most `r` colours has a
monochromatic congruent copy of finite `T`. The required order is

```
for every r >= 1, there exists N = N(X,r),
for every r-colouring of R^N, there exists a monochromatic copy of X.
```

The reconstruction respects this order. For fixed `r >= 2`, induction first
chooses `d2` for `r-1`, compactness chooses finite `C`, the geometric gadget
chooses `S`, `P`, and `A`, Ramsey-ness of the now-fixed `P` chooses `n0` for
`r`, and only then is an arbitrary colouring of `R^N` considered.

### Compactness (Lemma 2.3)

Apply EGMRSS Proposition 4 with `B = R^d`, `A` the family of congruent copies
of finite `T`, and incidence given by membership. Every relation fibre is
finite because `T` is finite. The finite point set `B'` supplied by the
proposition is exactly a finite `C` satisfying `C ->_r T`. There is no appeal
to the desired pyramid theorem here.

### Affine normalization and codimension

Let `d1 = affdim(B)` and first restrict to `aff(B union {z})`. Since
`z notin aff(B)`, this space has dimension `d1+1`; an affine Euclidean isometry
sends `aff(B)` to `R^d1 x {0}` and sends `z` to `(u,h)` after rotating its
one-dimensional normal component, with `h > 0`. This justifies the report's
normal form even when the original ambient codimension is larger than one.

It also shows equivalence with ILW Conjecture 8: after replacing an inessential
ambient `R^d` by `aff(B)`, the base lies in a hyperplane and the apex is off it.

### Affine independence and imported Ramsey theorems

For `s_i = (c_i,h e_i)`, any affine relation has last block
`h sum_i lambda_i e_i = 0`, so every `lambda_i = 0`. Thus `S` is the vertex
set of a nondegenerate simplex. Frankl--Rodl Theorem 5.1 applies. EGMRSS
Theorem 20 then applies literally to the orthogonal-coordinate Cartesian
product `P = B x S`. Both inputs quantify over every finite number of colours.

### Congruences and apex distances

`c_i -> (u,c_i,0)` preserves every pairwise distance, so `A` is congruent to
`C`. Each fibre `B x {s_i}` is congruent to `B`, and

```
||(b,c_i,h e_i) - (u,c_i,0)||^2 = ||b-u||^2 + h^2
                                      = ||(b,0)-(u,h)||^2.
```

Together with the unchanged base distances, this proves that each fibre plus
its assigned apex is congruent to `X = B union {z}`. The exact rational checker
audited these identities and product distances in three independent examples;
the general displayed identity, not the examples, is the proof.

### Extension to an ambient isometry

A finite distance-preserving bijection `phi:P -> P'` extends even when `P`
does not affinely span `R^N`. After fixing `p0`, the pairwise distances recover
the Gram matrix of all differences `p-p0`. Equal Gram matrices give a
well-defined inner-product isometry between their spans. Extend orthonormal
bases of the spans to bases of `R^N`, then restore the translation. Hence the
same ambient isometry legitimately transports every auxiliary apex `a_i`.

### Dimension monotonicity and colour dichotomy

For `N >= n0`, restricting any colouring of `R^N` to an embedded `R^n0`
proves `R^N ->_r P`. Embed `P union A` in the same `R^N` by taking
`N >= d1+d2+|C|`.

If the monochromatic copy of `P` is red and some transported apex is red, its
assigned red fibre gives red `X`. Otherwise every transported apex avoids red,
so the congruent copy of `C` uses at most the other `r-1` colours and its arrow
property gives a monochromatic `X`. Empty colour classes can be padded, so
"at most" causes no quantifier problem. This closes the induction.

### Iteration

If `z_i notin aff(B union {z_1,...,z_(i-1)})` for every `i`, each intermediate
finite union is Ramsey by the preceding theorem. Induction on finite `t` gives
the stated corollary. It makes no statement about an added point inside the
current affine hull.

## Counterexample and literature search

The standard necessary sphericality condition produces no counterexample. If
`B` has circumcentre `c` and radius `R` in its affine hull and `z=(u,h)`, a
sphere through the pyramid exists with centre `(c,t)`, where

```
t = (||u-c||^2 + h^2 - R^2) / (2h).
```

Thus the theorem is compatible with the known necessity that Ramsey sets are
spherical. Direct attempts to break the construction via dependent `C`, a
nonspanning `P`, a singleton base, extra ambient codimension, or unused colours
all reduce to the arguments above; none gives a counterexample.

At about 2026-08-11T19:50Z, arXiv API searches for the exact title,
`pyramid AND Ramsey`, `"affine hull" AND Ramsey`, `"adding a point" AND
Ramsey`, and `"Ramsey base"` returned Moore as the only relevant mathematical
record. An API listing of all sixteen math.CO submissions from Moore's
timestamp through the current index contained no later competing item. The
broader `"Euclidean Ramsey"` search located recent adjacent work but no other
paper asserting this closure theorem. DataCite's exact-title query returned
only Moore, Crossref concept queries exposed older surveys and adjacent
Euclidean Ramsey work but no competing pyramid theorem, and zbMATH's
`pyramid ramsey` query returned no record. DataCite registered the arXiv DOI
as version 1 on 2026-08-11. These are dated search results, not proof of
priority.

## Scope for Problem 174

Problem 174 asks for a characterization. Moore proves only closure under one
out-of-affine-hull point, and finite iteration under the same condition at each
step. He does not prove that every spherical set is Ramsey, that every
subtransitive set is Ramsey, either converse characterization, same-affine-hull
closure, or an explicit dimension bound. The site must remain `OPEN`, and a
publication entry must be labelled `PARTIAL`, literature-derived, arXiv v1,
with no peer-reviewed version located.

## Frozen identities

The audited bundle's manifest verified all eleven entries. Its independently
anchored SHA-256 is:

```
701facd01aa6f523d90a314676d357a0d42db8737ac695b819c83d5d62ba87c6  MANIFEST.sha256
```

Key file identities are:

```
0a8c89cb67e3baabdba2209674eb6e429202ab3c712ab324cbd1c18502593193  REPORT.md
102b93da48cbba7767449734ce18d5c4c09fd43a49dc5fb277eafe61d8d84cda  verify_bundle.py
7fa3dad5855a05335481d2106944e90aff96151644f8ec88b7dc49168316949e  gate_snapshot.txt
26dacfe820759166f07b4c0caf12e9c2a0296848638e46428d3e193b41fd3ee7  live/live_gate.txt
98f2e7fcf07fe8004a8b2646d55bbfa8f383ca0c4f01996a25e19a9b1f2c68a3  live/erdos174_live.png
f9911c644d635366a422f97713151a8e79582665626be514006c2be84e4f89af  live/erdos174_thread_live.png
```

## Public-package acceptance test

A repaired public package passes this audit only if all of the following hold:

1. The two restricted publisher PDFs and the default-license ILW PDF are
   absent from public version control. The simplest policy omits all PDFs.
2. Their citations, official URLs, theorem locations, observed hashes, and
   license status are preserved as source-custody metadata.
3. Every shipped regular file is present exactly once in the public manifest,
   and the manifest has no missing path, duplicate path, or stale hash.
4. The root checker uses explicit runtime failures, not `assert`, for required
   validation.
5. The unmodified package succeeds under `python3`, `python3 -O`, and
   `python3 -OO` with identical substantive counts.
6. After separately corrupting a manifest-tracked narrative file, a source
   metadata file, and a geometric fixture, each of those three Python modes
   exits nonzero. Restore from a clean copy between corruptions.
7. The public narrative names ILW Corollary 4, labels Moore's result `PARTIAL`
   and arXiv v1 with no peer-reviewed version located, and does not imply a
   full solution or peer-reviewed novelty.

Until that matrix is actually run against the assembled public tree, the
public-release verdict remains GAP even though the mathematics is PASS.
