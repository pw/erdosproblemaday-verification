# Hostile audit: Erdos problem 213 fixed-heptagon nonextension

Verdict: **PASS**, strictly for the bounded fixed-heptagon claim in
`AUDIT_REPORT.md`.

The audit owns a third full traversal in sum/difference coordinates, a separate
Python big-integer metric checker, and a parser for the original Kreisel-Kurz
arXiv source. To rerun it against the frozen author bundle:

```sh
./reproduce.sh ../fresh7_erdos213_20260811
```

The result is not a lower bound for `d_dot(2,8)`, does not establish an
eight-point construction, and does not solve problem 213.
