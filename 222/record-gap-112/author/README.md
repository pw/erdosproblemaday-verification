# Erdos 222 finite frontier bundle

Disposition: **PASS**.

The next record gap between integers that are sums of two squares is certified
at

```text
133858454292 .. 133858454404
```

The difference is 112, equivalently 111 consecutive interior integers are not
sums of two squares.  An exhaustive baseline verifies the previous global
maximum 107 through 99,951,600,400.  Three agreeing post-anchor scans, including
a separately written implementation, prove that the new 112 gap is maximal
through the represented endpoint 200,000,000,000.

Start with:

- `AUDIT_REPORT.md` for the exact statement and proof;
- `PROVENANCE.md` for the live, OEIS, literature, novelty, and collision audit;
- `verify_frozen_outputs.log`, `verify_gap_python.log`, and
  `verify_gap_pari.log` for the concise PASS records;
- `MANIFEST.sha256` for integrity.

No site files were edited or deployed.  The copies under `site_snapshot/` are
frozen evidence of the versions audited for collision.
