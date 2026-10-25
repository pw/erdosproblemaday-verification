# Erdős 352 hostile replay for `N=24,25,26`

This evidence independently audits the finite claims `f(24)=48`, `f(25)=52`,
and `f(26)=52`. It does not claim a uniform bound or solve the continuous
problem.

Build and run from this directory:

```bash
g++ -std=c++20 -O3 -Wall -Wextra -Wpedantic \
  audit_352_upper.cpp -o audit_352_upper
./audit_352_upper 24 48 n24_producer_stream.jsonl
./audit_352_upper 25 52 n25_producer_stream.jsonl
./audit_352_upper 26 52 n26_producer_stream.jsonl
sha256sum -c SHA256SUMS
```

The generated streams are deliberately excluded: their SHA-256 values are
the certificate digests recorded in the two audit reports, and the checker
regenerates them. `cpp_n*.out`, the strict producer logs, witness audits, and
public-reference comparisons are the frozen completed transcripts.

The report filenames retain the historical `PREAUDIT` suffix, but their
contents are the finalized PUBLISH verdicts after strict producer completion.
