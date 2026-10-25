# Hostile audit: Erdős Problem 80 at order nine

Verdict: **PUBLISH**.

This lean bundle independently audits the frozen producer bundle at
`/tmp/erdos80_n9`.  It does not contain or modify the producer artifacts.

Run:

```bash
./reproduce.sh /path/to/erdos80_n9
```

The audit verifies the producer's complete manifest, regenerates the entire
order-nine nauty stream, byte-compares it with the frozen stream, decodes and
scans all 274,668 unlabelled graphs with a separate bit-mask implementation,
checks the OEIS collision controls, and reconstructs all extremal witnesses.

See `AUDIT_REPORT.md` for the mathematical and provenance review.
