# Problem 552: the first missing finite value

This package independently audits the unreviewed candidate theorem

```text
R(C4, K1,39) = 46.
```

The lower bound was already known. The candidate proof at frozen Git commit
`86a1c5055eea5e3891b2eeaea6c7ee1b3977bd33` supplies the upper bound. The
hostile audit reconstructs the 45-vertex lower witness, the universal
46-vertex structural reduction, the exact spectral moments, and a rational
dual certificate. Its dependency-free checker does not use the candidate's
uncertified SAT result lines.

Run `./reproduce.sh` for the manifest check and exact standard-library audit.
`./run_audit.sh` additionally exercises the upstream project and requires its
pinned Python dependencies.

Classification: **PARTIAL** for Problem 552. This closes one finite Ramsey
value but does not settle the asymptotic problem. The candidate is public and
independently audited, but not peer reviewed; this package makes no priority
claim.
