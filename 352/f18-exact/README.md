# Erdős 352 / Koizumi lattice model: exact `f(18)=34`

This directory certifies the finite statement `f(18)=34`, where `f(N)` is
the largest size of a finite `N`-avoiding subset of `Z^2`: every triple,
with repetitions allowed, satisfies

```text
|area(p,q,r) - N| > diameter(p,q,r).
```

This does not prove `f(N)=O(N)` and therefore does not solve the original
continuous Erdős problem 352.

## Reproduce

With Python 3.10 or newer:

```bash
python3 erdos352_n18_matching_audit.py
python3 erdos352_n18_verify.py --min-n 18 --max-n 18 --json
python3 hostile_audit/audit_exception_exact_cover.py
python3 hostile_audit/audit_strict_predicate.py
python3 hostile_audit/audit_352_n18.py
sha256sum -c SHA256SUMS
```

The two checkers use assertions as fail-closed checks. Run them with ordinary
`python3`, never `python3 -O`.

The focused checker verifies the 34-point witness, reconstructs the sole
exceptional `B=(5,4)` no-high pool, audits its 57-edge incompatibility graph
and nine-edge matching, and checks all 512 matching-endpoint choices. The
full checker exhausts all 140 normalized diameter cases and 12,594 fixed-high
branches, independently audits 12,734 coloring certificates and 3,011,741
same-color pairs, and applies the focused refinement to the exceptional
branch.

`hostile_audit/` is a frozen independent reconstruction. It uses set-based
dynamic DSATUR and different geometry code, computes the exact minimum vertex
covers without trusting the supplied matching, and compares the integer
predicate against 100-decimal radicals. Its verdict is `PUBLISH`; see
`hostile_audit/AUDIT_REPORT.md`.

The full run took 216.13 seconds with 20,940 KiB maximum resident memory. Its
canonical audited certificate-stream digest is:

```text
b761add523bbe8a4f1d8f822268ddc28a893e9a1318ebc73807822d7ca09fea8
```

`reference_upper_n18.json` is output from the separate public upper-bound
implementation at commit
`7a4a19468771766cb4f20e10dfa5cf770cc2487b`. It independently finds 140
diameter cases, identifies `B=(5,4)` as the unique case with pair-relaxation
upper total 35, and bounds every other case by 34. The additional matching
audit in this bundle lowers that last case to 34.

The lower witness was posted previously by BorisAlexeev and appears in the
public witness repository at commit
`09e5c5393943c881ab60118aa32fe5660539c8d5`; the source JSON is included.
No priority claim is made for it.

## Certificate in one paragraph

All 7,140 witness triples have positive exact integer margin, with minimum
21. Pair coloring bounds every upper branch by 34 except `B=(5,4)`, whose
no-high pool has 42 candidates. Its incompatibility graph has 57 edges and a
matching of size nine. A compatible 33-subset would omit a nine-vertex cover,
so it must select exactly one endpoint of each matching edge. Exactly two of
the 512 endpoint choices cover all incompatibility edges; each surviving
33-set contains two forbidden triples, all of exact margin `-15`. Hence that
branch has at most 32 candidates, or 34 points including the diameter pair.
