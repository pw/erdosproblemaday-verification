# Erdős 352 hostile replay for N=19,20,21,22,23

This completed evidence audits the finite claims `f(19)=38`, `f(20)=39`,
`f(21)=41`, `f(22)=44`, and `f(23)=45`. It does not claim a uniform bound or
solve the continuous problem. The N=22 and N=23 results are recorded in their
respective audit addenda.

Build and run from this directory:

```bash
g++ -std=c++20 -O3 -Wall -Wextra -Wpedantic audit_352_upper.cpp -o audit_352_upper
./audit_352_upper 19 38 n19_producer_stream.jsonl
./audit_352_upper 20 39 n20_producer_stream.jsonl
./audit_352_upper 21 41 n21_producer_stream.jsonl
./audit_352_upper 22 44 n22_producer_stream.jsonl
./audit_352_upper 23 45 n23_producer_stream.jsonl
sha256sum -c SHA256SUMS
```

The generated stream files are deliberately excluded from this compact bundle:
their SHA-256 values are the certificate digests listed in `AUDIT_REPORT.md`,
and they are reproduced in seconds by the checker. `cpp_n*.out` and
`cpp_n*.time` are the frozen completed transcripts.

A much slower optional Python replay was begun for additional redundancy but
was manually stopped after this independent C++ audit had completed. Its
partial outputs are not evidence and are not included.
