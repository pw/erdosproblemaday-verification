# Final hostile audit: public Erdos 174 pyramid package

Audit completed: 2026-08-11T20:19:54Z

Input work package:
`/home/exedev/erdos_scratch/erdos174_pyramid_public_20260811_work`

Corrected frozen package:
`/home/exedev/erdos_scratch/erdos174_pyramid_public_20260811_final`

Neither this audit nor the corrections edited `/home/exedev/ErdosProblemADay`.
The work package was preserved; corrections were made only in the new final
sibling.

## Verdict

**PASS for public packaging and reproduction.** The final sibling satisfies
all seven pre-public acceptance conditions. This is a packaging and independent
proof audit, not journal peer review and not a claim that Erdos Problem 174 is
fully solved.

The mathematical conclusion remains **PARTIAL**: Moore's arXiv:2608.09649v1
proves closure under adjoining a point outside the current affine hull and
resolves Ivan--Leader--Walters Conjecture 8. The general characterization in
Problem 174 remains open. No peer-reviewed version or journal reference was
located at the audit time.

## Defects found and corrected

The input work package passed its documented reproduction, but hostile checks
found four publication defects:

1. `SOURCES.md` incorrectly named Maria-Romina Ivan as "Barnabas Ivan".
2. `REPORT.md` referenced the absent private path `live/live_gate.txt` instead
   of the public `LIVE_GATE.txt`.
3. Manifest closure ignored every nested regular file named `MANIFEST.sha256`.
   An untracked `nested/MANIFEST.sha256` was therefore accepted.
4. The no-PDF check inspected only the filename suffix. A tracked PDF header in
   `fixtures/payload.bin` was therefore accepted and reported as `pdfs=0`.

The final sibling corrects the attribution and path, removes an unnecessary
absolute novelty adjective and a non-reproducible historical scratch claim,
labels the screenshots as private custody artifacts with hashes, and supplies
source page locations and explicit license URLs. The checker now excludes only
the root manifest from closure, validates canonical in-root manifest paths,
and rejects both `.pdf` suffixes and PDF magic in the first 1024 bytes.

The tamper harness permanently regression-tests both bypasses as well as extra
files, duplicate entries, and both forms of PDF detection.

## Seven-point acceptance matrix

### 1. No third-party PDFs: PASS

An independent scan found no `.pdf` filename and no PDF magic in any regular
file. `file(1)` identified every shipped file as Markdown/text, JSON, Python,
or shell. The package intentionally distributes no PDF bytes.

The checker independently scans every regular file by extension and magic.
A tracked `disguised.pdf` and a tracked `%PDF-` payload named `disguised.bin`
were rejected in normal, `-O`, and `-OO` modes.

### 2. Source custody metadata: PASS

`SOURCES.md` now records correct authorship, official record/DOI URLs, audited
versions, theorem and page locations, observed PDF hashes, and license status:

```
2a1f866a06e5a8452f8b8425e6e244706a23eb039bb427eac5a51ade028fd45e  Moore 2608.09649v1, CC BY 4.0
9e7a0da78ec6094bde530cf789c9ef58a680810ef2ac52feac49114c4c884f0e  Ivan--Leader--Walters 2606.13472v1, arXiv default license
f0ee8b166026281c106562102657a71a7be8a85db964e0b370244ddc4764fbfd  Behague 2510.15677v3, CC BY-SA 4.0
ac59b75ae71753073a99d689e60a8d52caa7a47216dd21d7d57026b8d281682a  EGMRSS 1973, reproduction rights reserved in inspected copy
e82f0e24babe4751e695fd90da2f46363e127544f53598ea9a2ae805a6eaba72  Frankl--Rodl 1990, downstream permission not established
```

Moore's theorem is located at p. 2 with proof on pp. 3--5; ILW Corollary 4 is
on p. 6 and Conjecture 8 on p. 9; EGMRSS Proposition 4 is on journal p. 343
and Theorem 20 on journal p. 357; Frankl--Rodl Theorem 5.1 is on journal p. 5.

### 3. Exact manifest closure: PASS

The root manifest lists ten paths, all unique. There are exactly ten non-root-
manifest regular files, and the sorted sets agree. Every listed path is a
regular non-symlink with the stated hash. There are no other filesystem objects
below the package except the three expected directories.

The final checker rejects missing, modified, duplicate, linked, non-canonical,
escaping, unlisted, and unexpectedly nested regular files. In particular, the
nested-manifest bypass accepted by the work package now fails with
`manifest is not exact filesystem closure` in all three modes.

### 4. Explicit runtime failures: PASS

Neither `verify_public_bundle.py` nor `audit_tamper_matrix.py` contains an
`assert` statement. Required conditions call `require`, which raises
`VerificationError` or `RuntimeError` independently of Python optimization.
The checker also validates that the root manifest itself is a non-symlink
regular file.

### 5. Normal, `-O`, and `-OO`: PASS

All three modes produced this byte-identical line:

```
PUBLIC_BUNDLE=PASS manifest_files=10 pdfs=0 text_markers=30 fixture_cases=3 geometric_equalities=239 abstract_colourings=27
```

The SHA-256 of that output line including its newline is:

```
44d4d8b2edd5b02fe6db8cd3273a5f5e42f0d6eac0bddb8fb2c35ae45265dde5
```

### 6. Tamper rejection: PASS

All nine required tracked-file combinations rejected independently:

- `REPORT.md` under normal, `-O`, and `-OO`;
- `SOURCES.md` under normal, `-O`, and `-OO`;
- `fixtures/geometric_cases.json` under normal, `-O`, and `-OO`.

Every run exited 1 with the corresponding manifest hash mismatch. The shipped
harness additionally rejected five structural mutations in all three modes:
an untracked regular file, an untracked nested manifest, tracked PDF magic
under a `.bin` name, a tracked `.pdf` name without PDF magic, and a duplicate
manifest entry. Its exact summary was:

```
TAMPER_MATRIX=PASS clean_modes=3 tracked_mutation_rejections=9 structural_rejections=15
```

### 7. Publication wording: PASS

The public report explicitly says:

- `PARTIAL` and independently audited;
- the live problem status is `OPEN`;
- ILW Corollary 4 already handles a subsoluble base;
- Moore removes that structural assumption and handles every finite Ramsey
  base;
- the source is arXiv v1 and no peer-reviewed version or journal reference was
  located;
- an empty base, if admitted, gives a Ramsey singleton directly;
- the theorem does not characterize all Ramsey sets, prove the spherical or
  subtransitive conjecture, handle same-affine-hull extensions, or provide an
  effective dimension bound.

No forbidden stale attribution, private live-gate path, or absolute "new
closure theorem" phrase remains in the public narrative.

## Mathematical fixture audit

The exact rational fixture checker remains faithful to the independently
audited construction. Across three cases it checks:

- affine rank `|C|-1` for `S = {(c_i,h e_i)}`;
- congruence of the auxiliary apices with `C`;
- every base-fibre distance;
- every apex-to-assigned-fibre distance;
- all Cartesian-product pair distances;
- the 27 abstract three-colour dichotomy assignments.

It reports 239 geometric equalities and 27 colourings. These tests audit the
finite algebraic gadget. They do not replace compactness, the EGMRSS product
theorem, the Frankl--Rodl simplex theorem, or the general induction proof.

## Reproduction

From the final package directory:

```bash
./reproduce.sh
```

The frozen run completed:

```
[1/3] Verify frozen hashes
[2/3] Verify under normal, -O, and -OO modes
[3/3] Run tracked-file and structural tamper matrices
PROBLEM 174 PUBLIC PACKAGE REPRODUCTION PASSED
```

All package data files are mode `0444`; the three executable scripts are mode
`0555`. Directories remain writable enough for the tamper harness to construct
isolated temporary copies. The package manifest is the cryptographic freeze;
its hash is externally anchored below.

## Frozen package identities

The final package manifest has SHA-256:

```
96d9a06c67206c4a7d22f00b41d21ead41314ecc87848e1990420ab1648ba9cf  MANIFEST.sha256
```

Its ten entries are:

```
2bc20973f4da9c81b12c1f940d6a44f9ad51518c856e087b6415cbfcbe853ff5  ./HOSTILE_AUDIT.md
30ff949246e6abbaeaf7fb9158f4cf720b025e3a8f043146a48c05f9f7fb17f2  ./LIVE_GATE.txt
eabfaf2e62efb15dc4938e72485a5d604ffe7ebe4f98d08048ddbc37c2d4c2d1  ./REPORT.md
c9f1af35297059dab714e18b6fcdbf7651f1f3e3296a6d897c83aa9e98f66a4d  ./SOURCES.md
0dea3a0bf19fd3662ce7dad59418d9bc6cae6bb09aef3e50e59d80a609cedf5f  ./audit_tamper_matrix.py
b4f666f2d48e0ff4e6780615e67ad7d6673dbb8498e791a101528c1009aa76fd  ./fixtures/geometric_cases.json
39b7ce96a5d105ed8d9398eb860b0764b46451fe67c8086246affb912c6a93bc  ./logs/tamper_matrix.log
44d4d8b2edd5b02fe6db8cd3273a5f5e42f0d6eac0bddb8fb2c35ae45265dde5  ./logs/verify.log
0b755bdb52e20e5a79a42ba59e15a85112726d3aa0909b2301ae4d9b9eeff536  ./reproduce.sh
45f3645c55ff4aab9af14dc24da5260e2208ebbd3ba61fd932614b1825caadc0  ./verify_public_bundle.py
```

The input work-package manifest, preserved for comparison, had SHA-256
`b01f21f5e5f2b28c99df43eae64949d862dc7cc0e82034dc5b8bc1ef03c55779`.
