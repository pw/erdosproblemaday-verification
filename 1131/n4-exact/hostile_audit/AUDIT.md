# Independent release audit: Erdos Problem 1131 v3

Audit date: 2026-08-11 UTC

Verdict: **PASS - no release blocker found.**

This is a generic independent audit record. It records checks performed against
the frozen public archive and does not imply review or endorsement by any named
person. This document is original audit documentation and embeds no third-party
paper, site snapshot, package, or other third-party content.

## Audited boundary

The sole release input was:

```text
audit_erdos1131_n4_exact_20260811_v3_public.tar.gz
SHA-256: 2563c7e927a5f038211716511719473ba713cc03bf3e486efe7ad68b7b5166b7
```

The archive was extracted into a fresh temporary directory. The author working
directory, earlier v1/v2 packages, and any website checkout were not trusted as
release inputs. All hostile mutations were made only in disposable copies of
the fresh extraction. The frozen archive, source directory, and site were not
modified.

## Archive and integrity

* The archive hash matched the supplied release anchor.
* It contained one top-level directory and 15 regular files, with unique
  relative paths and no absolute paths, traversal components, links, devices,
  FIFOs, duplicate members, or extended PAX headers.
* Archive ownership was normalized to UID/GID 0, all mtimes were
  2026-08-11 00:00:00 UTC, documents were mode 0444, and executable entry
  points and the root directory were mode 0555.
* The gzip header had zero mtime and no stored filename. Rebuilding with sorted
  POSIX ustar members, fixed ownership and mtime, and `gzip -n -9` produced a
  byte-identical archive.
* Extracted `MANIFEST.sha256` had SHA-256
  `d518ead8ded0a2962bc0330709042c6dfafbb7e9dcde80d297f2bea5e64bea8a`.
* Extracted `MANIFEST.sha256.pin` contained that manifest digest and had
  SHA-256
  `64a5ab12d1fc91bd4c9bb77c2375882396faea71cf7a7fe6a07ad932a1e8eab6`.
* GNU `sha256sum --strict -c` passed, and the isolated Python verifier reported
  `MANIFEST_CLOSURE=PASS members=15`.

## Reproduction environment

The replay used `/tmp/erdos1131-v2-release-venv/bin/python` as the explicitly
selected out-of-tree interpreter:

```text
Python 3.12.3
SymPy 1.14.0
mpmath 1.3.0
isolated=1 safe_path=True optimize=0
Linux 6.12.93 x86_64, glibc 2.39
Bash 5.2.21
GNU coreutils sha256sum 9.4
timezone=UTC
```

The environment contained the two versions pinned by the release requirements.
Exact replay and exact-plus-numeric replay both exited zero. The latter output
was byte-identical to the bundled `verification.log`.

## Hostile checks

Each failure below was required and observed:

| Case | Result |
| --- | --- |
| Every Python entry point under `-O` and `-OO` | exit 1 |
| Every Python entry point without isolated/safe-path mode | exit 1 |
| Direct and wrapper `PYTHONOPTIMIZE` cases, including an empty value | exit 1 |
| Multiword `PYTHON` selector | exit 1 |
| Extra regular file or directory | closure failure |
| Missing listed payload | preflight failure |
| Listed same-content symlink | preflight failure |
| Listed FIFO | exit 1 in approximately 11 ms |
| Listed directory in place of a payload | preflight failure |
| Mutated regular payload | digest failure |
| Symlinked manifest | bootstrap failure |
| FIFO in place of the pin | exit 1 in approximately 6 ms |
| Extra unlisted FIFO | exit 1 in approximately 49 ms |
| Self-deleting unlisted `hashlib.py` import shadow | closure failure; marker absent and payload remained |
| False symbolic coefficient with regenerated manifest and pin | exact identity failure |
| The same false checker under optimized Python | optimized-mode failure |

The timings are single-host observations used only to establish prompt
nonblocking rejection; they are not performance guarantees.

An AST scan found zero `assert` statements in the three Python files. All three
also compiled successfully with bytecode directed outside the extracted bundle.

## Mathematical and documentary checks

* Exact and numerical certificates reproduced the recorded critical parameter,
  node, minimum, Fejer value, Gram identity, affine derivative, Bernstein
  positivity, resultant, and rational root isolations.
* Independent integer evaluation gave discriminants `-20736` and
  `-19439210456064000000`. Therefore the proof sentence that each real cubic
  has exactly one real root is correct.
* No optimizer is distributed. Earlier numerical optimization and the optional
  numerical checker are explicitly identified as non-proof; the exact checker
  is identified as the certificate.
* The live Problem 1131 status and comment summary were checked without copying
  site content into this artifact. The release wording is conservative about
  claimed proofs, records the known 1997 numerical work, states that the full
  article and prior references remain unreviewed for an exact small-n theorem,
  and makes no novelty or priority claim.
* `LICENSE` and `NOTICE` limit MIT coverage to contributor-owned original code
  and documentation. The archive contains no paper, PDF, site snapshot,
  dependency, dependency license text, or other redistributed third-party work.

## Limitations

This audit validates the identified archive bytes, integrity workflow,
reproduction, hostile cases, proof identities, and claim boundaries. It is not
a formal proof-assistant certification, a legal opinion, or a complete
literature-priority review. The outer SHA-256 remains the release trust root,
as the in-archive manifest pin is not a signature.
