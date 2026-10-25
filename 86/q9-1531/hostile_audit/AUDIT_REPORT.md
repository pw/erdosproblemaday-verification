# Cold hostile audit: Erdos Problem 86, Q9 with 1531 edges

Audit date: 2026-08-11 UTC

## Verdict

**PASS**, for this exact finite claim:

```text
ex(Q_9, C_4) >= 1531.
```

The frozen certificate is a 1531-edge C4-free subgraph of the
9-dimensional hypercube. It proves a lower bound only. It does not prove the
exact value, optimality, the nonexistence of a 1532-edge graph, the asymptotic
conjecture in Problem 86, or unconditional novelty/priority. V3 states those
boundaries correctly. No theorem-bearing gap or V3 narrative overclaim was
found.

## Frozen object and hashes

Audited author directory:

```text
/home/exedev/erdos_scratch/erdos86_q9_1531_20260811_v3
```

Key SHA-256 values:

```text
520b3c6ae7ced58c696dc8ccb7141e141d0e9db95bec56d1be7865353b88806f  author SHA256SUMS
ea8bb444fb03fd5ea24d43c2b94f9ff2803a3e4d2810fe05f045e56d1f31321b  deterministic author tar.gz
4592a484fcfa65ef9883843485a60ff7b8d3856e81b4a667ae9cf14536132a5a  canonical 1531 JSON
21c7c0ad8c24f2cd5e337722d41e606e3154e4fb3c43b503d4124dba3290bb61  preserved raw 1531 JSON
883919d0e3c7d571aadd920ad539667338dfdb74efa24e61808fb41754db573c  prior site 1506 JSON
0994be825ec39d115b65eb1436eace7c1be324448a6ec116d69c8a7e2a75d338  external public 1505 JSON
```

The author manifest has 21 unique, sorted, canonical relative paths and
covers every regular file except itself. Including the manifest, the author
snapshot has 22 files. The independent freeze checker found no symlink,
hardlink, special file, path traversal, unlisted regular file, writable entry,
archive/directory mismatch, non-root archive owner, or non-canonical archive
timestamp.

The hostile-audit bundle has its own strict exact-coverage manifest: 64 listed
files and 65 total regular files including the manifest. Its offline replay
rejects an unlisted or missing file, a hash mismatch, writable content, a
symlink, a hardlink, or any special filesystem entry. The external trust
anchor for that audit manifest is reported with the sealed bundle.

## Independent certificate proof

`independent_q9_audit.py` is clean-room code and does not import an author
module. Its parser rejects invalid UTF-8, malformed JSON, duplicate object
keys, NaN-style constants, JSON booleans masquerading as integers, malformed
rows, reversed rows, loops, duplicates, endpoints outside 0..511, and edges
outside an independently generated Q9 universe of exactly 2304 edges.

It established exactly 1531 valid, distinct rows. It then used two complete
routes:

1. It enumerated every choice of two coordinates and every assignment to the
   other seven coordinates: `C(9,2) * 2^7 = 4608` square faces. Occupancy was
   `0:0, 1:784, 2:8, 3:3816, 4:0`. Every simple 4-cycle in a hypercube is one
   of these faces: a simple closed four-step coordinate-flip sequence uses
   exactly two coordinates twice, in alternating order.
2. It enumerated all 7638 length-two paths by center and unordered endpoint
   pair. Separately, it intersected adjacency sets for all
   `C(512,2) = 130816` unordered vertex pairs. The common-neighbour
   distribution was `0:123178, 1:7638`; the maximum was one, and every count
   agreed with the independent cherry enumeration. Two common neighbours of
   one pair are exactly a 4-cycle in a simple graph.

Diagnostics for the candidate were:

```text
direction counts = 170,170,172,170,170,171,168,170,170
degree histogram = 5:16, 6:492, 7:2, 8:2
faces = 4608
complete faces = 0
cherries = 7638
repeated endpoint pairs = 0
```

The raw and canonical files have identical edge rows in identical order.
Removing `construction` and `meta` leaves identical JSON objects. Their
portable edge-set digest is also identical:

```text
579539ce372adf149f05b7952be793a84948d206086612f945b6b88cd274ac91
```

That digest is SHA-256 of sorted normalized ASCII lines `u v\n`; it is an
edge-set identity, not a raw-file hash.

## Exact predecessor comparisons

The independent parser also fully validated both predecessor graphs as Q9
C4-free certificates. Exact set comparisons are:

```text
candidate1531 vs site1506:   common=1084 candidate-only=447 site-only=422 net=25
candidate1531 vs public1505: common=1059 candidate-only=472 public-only=446 net=26
site1506 vs public1505:      common=1313 site-only=193 public-only=192 net=1
```

Thus "25-edge improvement" and "26-edge improvement" mean cardinality gains,
not that either predecessor is a subgraph of the candidate. The bundle does
not claim containment.

Portable predecessor edge-set SHA-256 values are:

```text
79c072cfefa05136862c1db6d902178744f15dc97118e89a470f301d2c6c7ed2  site1506
c65e13fdc2914553059cd8f95806a8635f617e65b376d22ac2724663e2b554b3  public1505
```

## Reproduction and tamper audit

The full read-only author `reproduce.sh` exited 0 in 9.19 seconds with peak
RSS 350668 KiB. It checked the manifest, verified both 1531 files, ran
negative controls, compared predecessors, rebuilt the C++20/OpenMP heuristic,
and reproduced the exact 1506 predecessor edge set with its one-thread seed-1
positive control.

Every author Python checker was separately run under normal, `-O`, and `-OO`:
the output was byte-identical in all modes. The independent checker and hostile
tamper harness were also byte-identical across all three modes. Neither audit
checker uses `assert` for correctness.

The author verifier rejected a same-count duplicate, a non-Q9 edge, a complete
face, and the same mutation via its common-neighbour route in every mode. The
independent checker additionally rejected duplicate JSON keys, NaN, and a JSON
boolean endpoint. It tested the face and common-neighbour routes separately.

Hardening note: Python's `bool` is an `int` subclass, and Python's default JSON
loader keeps the last duplicate object key. The author parser therefore
accepts a boolean endpoint that is numerically the same vertex and accepts a
shadowed duplicate root key. This is not theorem-bearing: all four frozen JSON
files are duplicate-key-free, use exact JSON integers, are hash-locked, and
pass the strict independent parser. It is still a parser-hardening opportunity.

## Generator review

The generator is provenance, not proof. Source review confirmed V3's disclosed
one-line difference from the earlier 1506 source: an explicit safe cast of
`seeds.size()` to suppress `-Wconversion`. The strict author build was clean.
An additional ASan+UBSan one-thread build reproduced the exact 1506 edge set
without a sanitizer finding.

The audit did not rerun the schedule-dependent 1531 search or treat either the
frozen 180-second 1532 miss or a disclosed later post-freeze 300-second miss as
evidence. The intermediate 1507..1530 history and timing narrative are not
independently certified by complete transcripts in V3. None of that bears on
the explicit lower-bound certificate, and V3 makes no optimality inference.

## Public provenance and site gate

Fresh same-day captures established:

- The identified external repository's `HEAD` and `main` still resolve to
  commit `74e84382cbbc20b32a2ac679bff977cad3ac5d24`. Its current Q9 file is
  byte-identical to the frozen 1505 file.
- The live Problem 86 page remains `OPEN - $100`, with zero claimed proofs,
  no current worker, and two comments. The forum's Q9 row remains 1505.
- OEIS A245762 still stops at `n=6` with `1,3,9,24,56,132`.
- arXiv `2603.29127v4` concerns Q6, Q7, and Q8, not Q9.
- The live Erdos Problem a Day page publishes the exact 1506 predecessor.
  Source and sitemap each contain exactly one Problem 86 article. Its
  certificate hash matches the bundled 1506 file. The predecessor was added
  in site commit `8648597d27e13aaa11409ee94b7bd9860db2173a` at
  `2026-08-11T16:47:17Z`.
- At capture time, the site update gate therefore said to update the one
  existing Problem 86 article rather than add a duplicate. This audit made no
  site edit or deploy. The offline replay labels this as a dated
  prepublication fact, so it does not claim the 1531 entry remains absent
  after publication.

Authenticated GitHub code search found zero hits for `q9_edges_1531` and zero
for the candidate hash. A broad three-term search produced one false positive:
the terms occur in different Problem entries in a large frontier-atlas JSON;
its Problem 86 entry contains no 1531 claim. Repository search found the known
external construction repository. These are dated search results, not a proof
of global novelty. V3 expressly disclaims unconditional priority over private,
unindexed, or simultaneous work, so its public-comparison wording is sound.

## Publication-safe statement

> The explicit certificate and exhaustive independent checks prove
> `ex(Q_9,C_4) >= 1531`. This is 25 edges above the site's earlier audited
> 1506-edge certificate and 26 edges above the identified external 1505-edge
> certificate. No exactness, optimality, asymptotic resolution, or
> unconditional priority claim is made.

## Residual limitations

- Online status and search results are frozen as of 2026-08-11 and can change.
- Negative search cannot rule out private or unindexed prior work.
- The heuristic history is provenance only; the explicit certificate is the
  proof.
- The author parser's two strict-JSON leniencies should be hardened for future
  untrusted inputs, although they do not affect these frozen files.

None of these limitations changes the PASS verdict for the finite lower bound.
