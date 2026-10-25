# Dependency on the public frontier through 1500

The extension-only PMC induction starts from the exact public result
`f(1500)=44`. Its required bundle is `frontier-1500`, whose manifest is named
`erdos1109_manifest_2026-08-11.sha256` and has SHA-256:

```text
cbd71d674a96c46a40b1a2a2a6b3ac7d9a18e05d255f4c8033b5233894bda7e9
```

When this directory is copied to `verification/1109/frontier-2000`, the
expected public layout places that bundle at `../frontier-1500`. The quick
reproducer automatically verifies it when present, or accepts an explicit
`--base-dir PATH`. If neither is available, it still verifies the complete
extension bundle and reports the unresolved external dependency rather than
silently substituting another base.

The full primary C++ transcript starts from `N=1` and independently recomputes
the through-1500 values. The separate base dependency matters for the
extension-only PMC induction and for publication provenance: only the ten
records after 1500 are new relative to that already-public result.
