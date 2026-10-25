# Erdős 352 / Koizumi lattice model: exact `f(23)=45`

This directory certifies the finite statement `f(23)=45`, where every triple
in an `N`-avoiding subset of `Z^2`, with repetitions allowed, satisfies

```text
|area(p,q,r)-N| > diameter(p,q,r).
```

It does not prove the uniform estimate `f(N)=O(N)` and therefore does not
solve the original continuous problem.

## Reproduce

```bash
python3 erdos352_n23_verify.py --min-n 23 --max-n 23 --json
sha256sum -c SHA256SUMS
```

Run the assertion-based checker with ordinary `python3`, never `python3 -O`.

The embedded 45-point witness has 16,215 repeated triples; every exact integer
margin is positive and the minimum is 56. The upper checker exhausts all 225
normalized diameter cases and 40,566 fixed-high branches, reconstructs 40,791
coloring certificates, and directly audits 34,861,434 same-color pairs. The
global upper bound is 45, tight at `B=(6,4)` and `B=(6,5)`. Its
certificate-stream digest is:

```text
7ce7aaa06bfd68ad93f7ac06c79a6454337ba034efb81c9e1a0ffb1541d250f3
```

`reference_upper_n23.json` is the output of the independent public upper
implementation at commit
`7a4a19468771766cb4f20e10dfa5cf770cc2487b`. It separately reproduces 225
diameter cases, 187 cases with high points, 40,566 fixed-high branches, and
the exact upper total 45, tight at the same directions.

The lower witness was posted previously by BorisAlexeev and appears in the
public witness repository at commit
`09e5c5393943c881ab60118aa32fe5660539c8d5`; its source JSON is included and
no priority claim is made for it.
