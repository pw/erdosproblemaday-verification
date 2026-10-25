# Cold hostile audit: Erdos problem 86, Q9 with 1506 edges

Audit date: 2026-08-11 UTC

Auditor: fresh6, working independently of the author bundle

## Verdict

**PASS**, for the following exact finite claim only:

```text
ex(Q_9, C_4) >= 1506.
```

The certificate is a 1506-edge C4-free subgraph of the 9-dimensional
hypercube. This is a lower bound. It does not prove optimality, does not give
the exact value of `ex(Q_9,C_4)`, and does not advance or settle the asymptotic
conjecture in problem 86.

No mathematical or provenance gap was found. The only reproducibility nuance
is that the generator writes its input path into JSON metadata, so raw byte
identity requires the same relative input path used by `reproduce.sh`. The
supplied script does use that path. With a differently named but byte-identical
input, the edge set and all other JSON fields agree while the raw file hash
changes as expected.

## Frozen object audited

Author directory:

```text
/home/exedev/erdos_scratch/erdos86_q9_1506_20260811
```

Frozen archive and key SHA-256 values:

```text
ed504a1707478d5cf897b152b4db32bce9de0f8d84f621aa75093d755d137c59  erdos86_q9_1506_20260811.tar.gz
2878fa5ec38e7d52e056883f53dfbeb72c72a200ec6eb133402cbf620d890e3c  SHA256SUMS
883919d0e3c7d571aadd920ad539667338dfdb74efa24e61808fb41754db573c  q9_edges_1506.json
```

`sha256sum -c SHA256SUMS` accepted every listed file. Extracting the frozen
archive and comparing it recursively with the read-only directory produced no
difference. See `author_frozen_hashes.log`, `author_manifest_check.log`, and
the empty `tar_vs_directory_diff.log`.

## Independent certificate checks

The clean-room checker `verify_q9_independent.py` was written without using
the author verifiers. It strictly parsed the candidate and established:

```text
n=9
vertices=512
edge rows=1506
distinct normalized edges=1506
endpoint range=0..511
loops=0
non-hypercube edges=0
degree sum=3012
degree range=4..7
```

It then used two complete routes.

1. Coordinate-face route. It enumerated exactly
   `binom(9,2) * 2^7 = 4608` square faces. Their edge occupancy distribution
   was `0:6, 1:838, 2:82, 3:3682, 4:0`. Thus no square face was complete.
   Every simple 4-cycle in a hypercube is such a face: its four coordinate
   flips must use two coordinates twice, in alternating order.
2. Common-neighbour route. It built adjacency from scratch and enumerated all
   7426 length-two paths, keyed only by their unordered endpoint pair. No pair
   occurred twice. In any simple graph, two distinct common neighbours of the
   same endpoint pair are exactly a 4-cycle.

These routes are logically equivalent at the theorem level but use different
enumerations and data paths. `negative_mutation_test.py` also made a controlled
1506-edge mutation that completes a square; both routes detected a C4. Full
outputs are in `independent_q9_audit.log` and
`negative_mutation_test.log`.

`check_bundle_consistency.py` additionally used duplicate-key-rejecting JSON
parsing and confirmed that the 1506 plain-text rows exactly match the JSON
rows in the same order.

## Public 1505 comparison

The current public repository was freshly cloned from
<https://github.com/rafalwronapl/erdos86-hypercube-c4>. Its `main` and `HEAD`
both resolved to:

```text
74e84382cbbc20b32a2ac679bff977cad3ac5d24
```

That commit still lists Q9 at 1505 edges. Its Q9 certificate has SHA-256:

```text
0994be825ec39d115b65eb1436eace7c1be324448a6ec116d69c8a7e2a75d338
```

The independently checked set comparison is:

```text
public edges=1505
candidate edges=1506
intersection=1313
candidate-only=193
public-only=192
net improvement=1
```

The public 1505 graph itself also passed the independent Q9 and C4 checks.
Thus the candidate is rigorously one edge larger than this specifically
identified current public explicit certificate. This does not prove that no
other public, unindexed, private, or unpublished 1506-edge graph exists.

## Reproduction audit

The full author `reproduce.sh` was run directly from the read-only bundle. It
rebuilt the C++20/OpenMP generator, ran both author verifiers and the public
comparison, reproduced the canonical witness byte for byte, checked the
portable edge list, and rechecked the manifest. It exited 0 in 15.93 seconds;
peak RSS was 348320 KiB, dominated by compilation.

The final generator source has SHA-256:

```text
ed54c9ea3ee2cdaf4bead26fab6005c44b886315051d64389882713038848e69
```

A separate rebuild in this audit produced binary SHA-256
`c3af0b2bba72cc89261e253bed631d82dec14646a58373549c0b8050b6b19eb1`.
With one thread, seed 1, 1,000,000 steps, and the canonical relative source
path, it regenerated witness SHA-256 `883919...573c` byte for byte in 0.01
seconds.

As a decorrelated search check, the rebuilt generator was run with 12 threads,
the same seed and step budget, and a differently named input copy. In 0.04
seconds it found a distinct 1506-edge graph with SHA-256
`f6995bca4340fd43f343f69bf799d0531028a53a374083876303d9245d41d65d`.
That graph independently passed all edge, square, and common-neighbour checks;
it shares 1325 edges with the canonical candidate. This rerun supports search
reproducibility but is not needed for the proof.

## Live and literature provenance

Fresh rendered captures of the problem page and forum show:

```text
status=OPEN - $100
claimed proofs=0
currently working=None
comments=2
```

The 2026-05-22 forum comment reports the explicit public Q9 certificate with
1505 edges and makes lower-bound-only claims. No 1506 update appears there.

OEIS A245762 currently contains exact values only for `n=1..6`:

```text
1, 3, 9, 24, 56, 132
```

It has no Q9 term. The current arXiv API resolves Minamo Minamoto's paper to
`2603.29127v4`; its abstract gives Q7 at least 304 and Q8 at least 680 and a
modern proof/reproduction of Q6=132. The frozen PDF is byte-identical to the
current v4 PDF and contains no Q9 construction.

Exact web and authenticated GitHub code searches for the witness hash,
`q9_edges_1506`, and 1506 together with Q9/C4-free hypercube terms returned no
relevant prior construction. This is only a documented search boundary, not a
proof of global novelty. The bundle's narrower phrase, "one-edge improvement
over the identified public explicit-certificate frontier," is supported.

The read-only site gate also passed for
`ErdosProblemADay/src/index.js` and `src/ledger_data.js`: no problem-86 record,
problem token, live URL, A245762 token, or same-framework C4-free-hypercube
text was found. The repository already had an unrelated modified
`src/ledger_data.js`; this audit did not edit the site.

## Claim-boundary audit

The top-level README and provenance consistently state only the finite lower
bound. They expressly deny exactness, optimality, and asymptotic resolution.
The `provenance/` subtree contains frozen files from the public 1505 project;
its broader Q9-through-Q15 `CLAIM_BOUNDARY.md` is clearly identified as
upstream source material, not as a claim of this 1506 bundle.

The publication-safe statement is therefore:

> The attached explicit certificate and exhaustive checks prove
> `ex(Q_9,C_4) >= 1506`. This improves the identified current public explicit
> 1505-edge certificate by one edge. No exactness, optimality, unconditional
> priority, or asymptotic claim is made.

## Residual risks

- Negative literature/code searches cannot rule out an unindexed or private
  earlier 1506-edge construction.
- The generator is heuristic provenance, not an optimality argument. The
  certificate verifier is the proof.
- The raw generator JSON hash records the input path. Reproduce with the
  bundled relative path for byte identity; compare edge sets if relocating the
  input.
- Online status can change after the frozen 2026-08-11 captures.

None of these risks affects the certified finite lower bound.
