# Erdős 757: four exact separated-union values

This directory certifies

```text
f(17)=10, f(24)=14, f(26)=15, f(28)=16
```

for the `(4,5)`-set/Sidon-subset formulation of Erdős problem 757. These are
finite corollaries and do not improve the asymptotic interval
`9/17 <= c_* <= 4/7`.

## Reproduce

Using ordinary Python 3 from this directory:

```bash
python3 -I verify_separated_values.py
python3 -I audit_separated_values.py
sha256sum -c SHA256SUMS
```

Both checkers use only the standard library and integer arithmetic. The
primary verifier constructs four scale-separated unions from the previously
verified 3-, 12-, and 14-point blocks. The independent audit hardcodes all
coordinates and does not import or call the construction code.

For every set, the programs check the literal live `|B-B| >= 11` predicate
on every four-subset, every distinct-element pair sum, every three-term AP,
the absence of mixed APs, exact component Sidon numbers, and a matching
full-sum Sidon witness. The independent audit additionally exhausts every
subset of the 17-point union.

The matching lower bounds are the arithmetic consequences of the named
Gyárfás–Lehel and Henning–Yeo theorems detailed in `REPORT.md`.

The checkers use assertions as fail-closed tests. Do not invoke them with
`python3 -O`.
