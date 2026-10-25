# Erdos 196 finite-enumeration evidence bundle

Frozen on 2026-08-11 UTC. This directory is an audit artifact, not a site change.

The bundle supports one computational statement: for 1 <= n <= 14, the number theta_4(n) of
permutations of [n] with no monotone four-term arithmetic progression is the table in
expected_counts.tsv and REPORT.md. The endpoint-recursion argument and the complement involution
used by the optimized enumerator are proved in REPORT.md.

The bundle does not solve Erdos problem 196, establish an asymptotic estimate, or assert publication
priority for the finite table. SCOPE.md gives the exact claim boundary and the remaining gap.

## Reproduction

Run:

    ./reproduce.sh

The default run rebuilds the C++ program, recomputes n = 1 through 14, directly enumerates every
permutation through n = 10 with a separate predicate, runs the independent Python enumeration
through n = 9, checks the frozen site-collision snapshots, and compares the generated C++ table
with expected_counts.tsv. On the frozen VM the full run takes about two minutes.

For a shorter audit:

    ./reproduce.sh 12 9 16

Arguments are maximum n, direct-cross-check maximum n, and OpenMP thread count. All generated
files go to a new directory under /tmp. The script does not modify this bundle.

## Layout

- REPORT.md: proof, finite table, source audit, and exact infinite-problem gap.
- SCOPE.md: claim classifications and exclusions.
- PROVENANCE.md: acquisition details and source-inspection anchors.
- ENVIRONMENT.txt: frozen toolchain and host facts.
- expected_counts.tsv: machine-readable finite table.
- code/count_avoiders.cpp: endpoint recursion and direct factorial enumerator.
- code/independent_verify.py: separate exhaustive Python checker and incidence calculation.
- code/audit_site_collision.py: deterministic audit of the two frozen local-source snapshots.
- code/verify_count_log.py: compares a generated C++ log with the frozen table.
- logs/: captured reference executions.
- provenance/: rendered live-page captures and exact local-source snapshots.
- sources/: inspected primary PDFs, extracted text, and OCR derivatives for the scanned 1977 PDF.
- MANIFEST.sha256: hashes of every bundle file except the manifest itself.

The OCR text is a navigation aid and may contain recognition errors. Mathematical source claims
must be checked against the corresponding PDF image.
