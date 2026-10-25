# Erdős 864: exact finite values through 117

This bundle certifies the 2026-08-12 finite extension

```text
F(101)=...=F(106)=16
F(107)=...=F(116)=17
F(117)=18
```

where `F(N)` is the largest cardinality of a subset of `{1,...,N}` having at
most one sum value with multiple unordered representations `a+b`, `a<=b`.

The main Python verifier and the independent C++ audit use distinct
implementations but enumerate the same complete reflected-core
classification. In particular, both include the easily missed core-size-14
case and mathematically exclude core size 13 at diameter 115.

## Reproduce

From this directory:

```bash
python3 verify_864.py
g++ -O3 -std=c++17 audit_864.cpp -o /tmp/audit_864
/tmp/audit_864
sha256sum -c SHA256SUMS
```

The Python verifier uses only the standard library plus the system C++
compiler for its optimized exhaustive kernel. Assertions are fail-closed;
do not run it with `python3 -O`.

`REPORT.md` gives the completeness argument and independent hostile audit.
The frozen successful transcripts are `verify_output.txt`,
`audit_output.txt`, and `audit_time.txt`.

## Scope

This is an exact finite computation. It does not settle the conjectured
asymptotic constant in Problem 864.
