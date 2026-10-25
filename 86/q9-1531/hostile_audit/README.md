# Hostile audit bundle: Problem 86, Q9 = 1531

This read-only bundle independently audits the frozen V3 author package for
the exact finite claim

```text
ex(Q_9, C_4) >= 1531.
```

Verdict: **PASS** for that lower bound and the V3 claim boundary. See
`AUDIT_REPORT.md` for scope, hashes, diagnostics, provenance, and residual
limitations.

Run the complete offline replay from this directory:

```bash
./recheck_audit.sh
```

`MANIFEST.sha256` covers every regular file in this bundle except itself. The
manifest's own SHA-256 is the external trust anchor reported with the bundle.
The replay rejects missing or unlisted files, links, special files, hardlinks,
writable entries, and content mismatches. The `author_bundle/` directory and
its matching archive are byte-for-byte copies of the frozen V3 submission.
Dated network captures are under `evidence/`; no network access is required by
the replay.

This audit did not edit or deploy the site.
