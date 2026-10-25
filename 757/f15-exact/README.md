# Erdős 757: exact finite value `f(15)=9`

This directory certifies the finite statement

```text
f(15) = 9
```

for the `(4,5)`-set/Sidon-subset formulation of Erdős problem 757. It does
not determine the asymptotic constant, whose published interval remains
`9/17 <= c_* <= 4/7`.

The construction is

```text
0 136 200 243 246 249 272 286 298 323 400 528 596 1056 1057
```

It has largest Sidon subset size 9. The matching lower bound is the finite
arithmetic consequence of the named Gyárfás–Lehel and Henning–Yeo theorems
explained in `REPORT.md`.

## Reproduce

From this directory, using ordinary Python 3:

```bash
python3 -I verify_757_f15.py
python3 -I audit_757_f15.py
sha256sum -c SHA256SUMS
```

Both programs use only the Python standard library. The main verifier checks
all 1,365 four-subsets, 105 distinct-element pair sums, the complete AP
hypergraph, all 32,768 subsets by the direct Sidon sum predicate, and all
3,003 ten-subsets. The independent audit evaluates the live `|B-B| >= 11`
predicate literally and implements separate sum- and distance-based Sidon
checks.

The checkers use assertions as fail-closed tests. Do not run them with
`python3 -O`.

`full_output.txt` and `independent_audit_output.txt` are frozen successful
runs; `REPORT.md` is the complete mathematical and bibliographic report.

## Scope

This extends the exact finite table to

```text
(f(1),...,f(15)) = (1,2,2,3,4,4,5,5,6,6,7,7,8,8,9).
```

The first order at which a finite block could improve the asymptotic upper
bound is still 16: an `(4,5)`-set of order 16 with largest Sidon subset 9
would give `c_* <= 9/16 < 4/7`. No such set is claimed here.
