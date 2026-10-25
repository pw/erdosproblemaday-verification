# Publication copy notes

The original immutable author bundle is preserved separately at

```text
/home/exedev/erdos_scratch/erdos1109_exact_frontier_2026-08-11.tar.gz
```

with archive SHA-256

```text
ace7caef2f9d906fa72621b056c69a7f9121b63fbf2263ff42c239b95d52528d
```

Its 70 payload files and manifest are copied into this publication bundle
without alteration.  The original manifest remains
`erdos1109_manifest_2026-08-11.sha256`, whose SHA-256 is

```text
cbd71d674a96c46a40b1a2a2a6b3ac7d9a18e05d255f4c8033b5233894bda7e9
```

This version adds two separately frozen hostile audits under
`hostile_audit_1/` and `hostile_audit_2/`.  Both returned PASS for the exact
finite theorem and its dated novelty scope.  They independently reviewed the
graph reduction, incremental induction, primary clique recursion, all
witnesses, the 163 Cliquer decisions, the 163 PMC decisions, source and
binary provenance, sanitizers, and reproduction package.

The second audit identified one non-load-bearing provenance omission in the
author bundle: `/usr/bin/cliquer` is dynamically linked, while only the
executable hash was originally pinned.  It therefore freezes the loaded
`libcliquer.so.1` in `hostile_audit_2/`, SHA-256

```text
b1ccfac9465a0fc084b505d7415a8322da285705aaeb4f8f33f32cf926249c4e
```

The primary exhaustive verifier and source-pinned PMC replay already establish
the result independently of Cliquer, so this was not a mathematical gap.

The second audit's redundant scratch Git checkout of PMC is not included in
this repository copy. Its manifest-bound `pmc_src/` tree, rebuilt executable,
official source provenance, tests, and logs are all included; the omitted
checkout was not part of the audit evidence manifest.

The publication-level `SHA256SUMS` covers the complete recursive contents of
this version except itself, including the unchanged author manifest and both
audit evidence directories.
